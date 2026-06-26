#!/usr/bin/env python3
"""
Moteur du skill `organisation-documents`.

Classe un dossier de documents bruts (factures + relevés bancaires mélangés)
dans l'arborescence `clients/<slug>/<AAAA>/<MM>/...`, déduit `clients.json`
depuis les relevés bancaires, et produit un rapport.

Usage :
  python3 main.py <dossier_inbox> [<racine_clients>]

  <racine_clients> par défaut : ./clients

Tout est déterministe. Aucun montant ni numéro n'est deviné : on utilise
l'extraction de extract.py. Un document dont le client est indéterminable
part dans `clients/_a-identifier/` avec une question dans le rapport ; un
document dont l'extraction est incomplète part dans `clients/_incomplet/`.

Sortie :
  clients/clients.json         — liste des clients (déduite des relevés)
  clients/_index.json          — sha256 -> chemin classé (dédup)
  clients/_report.json         — rapport machine
  + résumé lisible sur stdout
"""

import hashlib
import json
import re
import shutil
import sys
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402


# ── Helpers ───────────────────────────────────────────────────────────────

def slugify(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s


def short_name(s, n=14):
    """Composant de nom de fichier : alphanumérique condensé, sans accents."""
    if not s:
        return "inconnu"
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")
    return (s[:n].strip("-") or "inconnu")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def amount_str(x):
    return f"{x:.2f}" if isinstance(x, (int, float)) else None


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Identification client ─────────────────────────────────────────────────

def find_client(name, clients):
    """Retourne le slug du client dont la raisonSociale correspond à `name`."""
    if not name:
        return None
    target = slugify(name)
    if not target:
        return None
    best, best_r = None, 0.0
    for c in clients:
        cand = slugify(c.get("raisonSociale", "")) or c.get("slug", "")
        if not cand:
            continue
        if cand == target:
            return c["slug"]
        r = similar(cand, target)
        if r > best_r:
            best, best_r = c["slug"], r
    return best if best_r >= 0.82 else None


def upsert_client(clients, slug, raison, statut, **extra):
    for c in clients:
        if c["slug"] == slug:
            c.setdefault("siren", [])
            c.setdefault("contacts", [])
            c.setdefault("domains", [])
            c.setdefault("sources", [])
            for k, v in extra.items():
                if isinstance(v, list):
                    for item in v:
                        if item and item not in c[k]:
                            c[k].append(item)
            return c
    entry = {
        "slug": slug, "raisonSociale": raison, "statut": statut,
        "confiance": 0.9 if statut == "auto-from-bank-statement" else 1.0,
        "aValider": False,
        "siren": [], "contacts": [], "domains": [], "sources": [],
    }
    for k, v in extra.items():
        entry[k] = list(v) if isinstance(v, list) else v
    clients.append(entry)
    return entry


# ── Classement physique ───────────────────────────────────────────────────

def place(src, dest_rel, clients_root):
    dest = clients_root / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest = dest.with_name(f"{dest.stem}__{src.stem[:8]}{dest.suffix}")
    shutil.copy2(src, dest)
    return dest


# ── Pipeline ──────────────────────────────────────────────────────────────

def run(inbox, clients_root):
    inbox = Path(inbox)
    clients_root = Path(clients_root)
    clients_root.mkdir(parents=True, exist_ok=True)

    clients = load_json(clients_root / "clients.json", [])
    index = load_json(clients_root / "_index.json", {})

    pdfs = sorted(p for p in inbox.rglob("*.pdf") if p.is_file())
    report = {
        "ran_at": datetime.utcnow().isoformat() + "Z",
        "inbox": str(inbox), "clients_root": str(clients_root),
        "classified": [], "questions": [], "incomplete": [], "duplicates": [], "ignored": [],
    }

    # ── Pré-extraction ────────────────────────────────────────────────────
    docs = []
    for p in pdfs:
        h = sha256_file(p)
        if h in index:
            report["duplicates"].append({"file": p.name, "already_at": index[h]})
            continue
        data = extract.classify_and_extract(extract.pdftext(p))
        docs.append({"path": p, "sha": h, "data": data})

    # ── Phase 1 — relevés bancaires → bootstrap clients.json ──────────────
    for d in [x for x in docs if x["data"].get("kind") == "bank-statement"]:
        st = d["data"]
        holder = st.get("holder")
        if not holder:
            report["incomplete"].append({"file": d["path"].name, "reason": "titulaire du relevé introuvable"})
            place(d["path"], Path("_incomplet") / d["path"].name, clients_root)
            continue
        slug = slugify(holder)
        upsert_client(clients, slug, holder, "auto-from-bank-statement",
                      sources=["bank-statement"])
        ps = st.get("period_start") or st.get("period_end")
        if ps:
            yyyy, mm = ps[:4], ps[5:7]
        else:
            yyyy, mm = "0000", "00"
        bank_slug = slugify(st.get("bank") or "banque")
        dest_rel = Path(slug) / yyyy / mm / "bank-statements" / f"{yyyy}-{mm}_{bank_slug}.pdf"
        placed = place(d["path"], dest_rel, clients_root)
        index[d["sha"]] = str(placed.relative_to(clients_root))
        report["classified"].append({
            "file": d["path"].name, "kind": "bank-statement", "client": slug,
            "period": f"{yyyy}-{mm}", "operations": len(st.get("operations", [])),
            "dest": index[d["sha"]],
        })

    # ── Phase 2 — factures ────────────────────────────────────────────────
    for d in [x for x in docs if x["data"].get("kind") == "invoice"]:
        inv = d["data"]
        emitter, recipient = inv.get("emitter"), inv.get("recipient")
        c_em = find_client(emitter, clients)
        c_re = find_client(recipient, clients)

        # client indéterminé → onboarding
        if not c_em and not c_re:
            place(d["path"], Path("_a-identifier") / d["path"].name, clients_root)
            report["questions"].append({
                "file": d["path"].name,
                "invoice_id": inv.get("invoice_id"),
                "amount_ttc": inv.get("total_ttc"),
                "emitter": emitter, "recipient": recipient,
                "question": f"Document : facture {inv.get('invoice_id') or '(n° inconnu)'}. "
                            f"Émetteur « {emitter} », destinataire « {recipient} ». Lequel est votre client ?",
            })
            continue
        if c_em and c_re:
            place(d["path"], Path("_a-identifier") / d["path"].name, clients_root)
            report["questions"].append({
                "file": d["path"].name, "invoice_id": inv.get("invoice_id"),
                "emitter": emitter, "recipient": recipient,
                "question": "Émetteur ET destinataire sont des clients suivis — préciser le dossier cible.",
            })
            continue

        if c_em:
            client_slug, direction, counterparty = c_em, "out", recipient
        else:
            client_slug, direction, counterparty = c_re, "in", emitter

        date = inv.get("issue_date")
        ttc = inv.get("total_ttc")
        if not date or ttc is None:
            place(d["path"], Path("_incomplet") / d["path"].name, clients_root)
            report["incomplete"].append({
                "file": d["path"].name, "client": client_slug,
                "reason": "date d'émission ou montant TTC introuvable",
                "extracted": inv,
            })
            continue

        inv_no = inv.get("invoice_id") or "SANS-NUM"
        inv_no_safe = re.sub(r"[^A-Za-z0-9\-]+", "-", inv_no).strip("-") or "SANS-NUM"
        yyyy, mm = date[:4], date[5:7]
        fname = f"{date}_{inv_no_safe}_{short_name(counterparty)}_{amount_str(ttc)}.pdf"
        dest_rel = Path(client_slug) / yyyy / mm / "invoices" / direction / fname
        placed = place(d["path"], dest_rel, clients_root)
        index[d["sha"]] = str(placed.relative_to(clients_root))
        # enrichir la fiche client avec le SIREN si lisible
        if inv.get("siren_found"):
            upsert_client(clients, client_slug,
                          next((c["raisonSociale"] for c in clients if c["slug"] == client_slug), client_slug),
                          next((c["statut"] for c in clients if c["slug"] == client_slug), "confirmed"),
                          siren=inv["siren_found"])
        report["classified"].append({
            "file": d["path"].name, "kind": "invoice", "client": client_slug,
            "direction": direction, "invoice_id": inv_no, "amount_ttc": ttc,
            "date": date, "dest": index[d["sha"]],
        })

    # ── Phase 3 — autres ──────────────────────────────────────────────────
    for d in [x for x in docs if x["data"].get("kind") not in ("bank-statement", "invoice")]:
        place(d["path"], Path("_non-attribue") / d["path"].name, clients_root)
        report["ignored"].append({"file": d["path"].name, "reason": "ni facture ni relevé reconnaissable"})

    # ── Persistance ───────────────────────────────────────────────────────
    save_json(clients_root / "clients.json", clients)
    save_json(clients_root / "_index.json", index)
    save_json(clients_root / "_report.json", report)

    # ── Résumé ────────────────────────────────────────────────────────────
    nb_inv = sum(1 for c in report["classified"] if c["kind"] == "invoice")
    nb_bank = sum(1 for c in report["classified"] if c["kind"] == "bank-statement")
    print(f"✓ {len(pdfs)} documents reçus")
    print(f"  Clients : {', '.join(c['slug'] for c in clients) or '(aucun)'}")
    print(f"  Classés : {nb_inv} factures, {nb_bank} relevés bancaires")
    if report["duplicates"]:
        print(f"  Doublons ignorés : {len(report['duplicates'])}")
    if report["incomplete"]:
        print(f"  ⚠ Extraction incomplète (→ _incomplet/) : {len(report['incomplete'])}")
        for it in report["incomplete"]:
            print(f"      - {it['file']} : {it['reason']}")
    if report["questions"]:
        print(f"  ❓ Client à confirmer (→ _a-identifier/) : {len(report['questions'])}")
        for q in report["questions"]:
            print(f"      - {q['question']}")
    if report["ignored"]:
        print(f"  Non comptables (→ _non-attribue/) : {len(report['ignored'])}")
    print(f"  Rapport : {clients_root / '_report.json'}")


def main():
    if len(sys.argv) < 2:
        print("usage: main.py <dossier_inbox> [<racine_clients>]")
        sys.exit(1)
    inbox = sys.argv[1]
    clients_root = sys.argv[2] if len(sys.argv) > 2 else "clients"
    run(inbox, clients_root)


if __name__ == "__main__":
    main()
