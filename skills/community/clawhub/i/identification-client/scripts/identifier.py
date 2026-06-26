#!/usr/bin/env python3
"""
Étape ③ du pipeline comptable — IDENTIFICATION DU CLIENT.

Action humaine : regarder une pièce déjà analysée et reconnaître à quel dossier
client elle appartient — et, pour une facture, si c'est un achat (le client est
le destinataire) ou une vente (le client est l'émetteur).

Cette brique est la SEULE à connaître et à tenir le registre clients
(`clients.json`). Elle le lit pour reconnaître, et l'enrichit quand elle apprend
quelque chose de sûr (nouveau client vu sur un relevé, SIREN/IBAN/domaine confirmé).
Elle ne range aucun fichier (c'est classement-document).

Signaux fiables, du plus sûr au moins sûr :
  1. Relevé bancaire     → le titulaire EST le client (certitude).
                           Rattachement par IBAN d'abord (clé EXACTE et stable),
                           puis par nom (indépendant de l'ordre et de la civilité).
  2. SIREN / IBAN / mail  → correspondance exacte avec une fiche client.
  3. Raison sociale       → similarité ≥ 0.82 (ou inclusion), si UN seul côté matche.
Aucun signal fiable → on ne devine pas : needs_review + question au comptable.

Pourquoi l'IBAN et le name_match indépendant de l'ordre : un même titulaire écrit
différemment d'un mois à l'autre (OCR, ordre nom/prénom, M./Mme) ne doit JAMAIS
créer un 2ᵉ dossier. C'est la garantie « 1 relevé = 1 client ».

Usage :
  echo '<dossier.json>' | python3 identifier.py [--clients <clients.json>]

Entrée : un dossier produit par les étapes amont, contenant au minimum
  { "analyse": { "kind", "fields": {...} }, "email": { "from","domain" } }

Sortie : le même dossier, enrichi d'un bloc "client" :
  { ..., "client": {
      "slug": "acme-sa" | null,
      "role": "out" | "in" | "holder" | null,   # out=vente, in=achat
      "counterparty": "Hôtel Bellevue" | null,
      "method": "iban|relevé|siren|domaine|raison-sociale*|null",
      "confidence": "haute|moyenne|faible",
      "needs_review": false,
      "is_new": false,                            # client tout juste créé → à valider
      "question": null
  }}
"""

import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

FUZZY_THRESHOLD = 0.82
_CIV_TOKENS = {"m", "mr", "mme", "mlle", "mm", "monsieur", "madame", "mademoiselle"}


# ── Helpers ───────────────────────────────────────────────────────────────

def slugify(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def norm_siren(s):
    """SIREN (9 chiffres). Un SIRET (14) → ses 9 premiers. '' si non plausible."""
    d = re.sub(r"\D", "", s or "")
    if len(d) == 14:
        d = d[:9]
    return d if len(d) == 9 else ""


def norm_iban(iban):
    """IBAN normalisé : sans espaces/ponctuation, majuscules. None si vide."""
    if not iban:
        return None
    s = re.sub(r"[^A-Za-z0-9]", "", iban).upper()
    return s or None


def _name_tokens(slug):
    return {t for t in (slug or "").split("-") if len(t) >= 2 and t not in _CIV_TOKENS}


def name_match(a, b):
    """Similarité de noms INDÉPENDANTE DE L'ORDRE et de la civilité.
    « novac-liviu » ≡ « liviu-novac », « ibrahim-tawfik » ≡ « tawfik-ibrahim »,
    « maison-pelletier » ⊂ « maison-pelletier-patisserie »."""
    ta, tb = _name_tokens(a), _name_tokens(b)
    if not ta or not tb:
        return 0.0
    if ta == tb:
        return 1.0
    jacc = len(ta & tb) / len(ta | tb)
    if (ta <= tb or tb <= ta) and len(ta & tb) >= 2:   # nom tronqué ⊂ nom complet
        return max(jacc, 0.9)
    return max(jacc, SequenceMatcher(None, a, b).ratio())


def amount_str(x):
    return f"{x:.2f}" if isinstance(x, (int, float)) else None


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path, data):
    # Écriture ATOMIQUE (.tmp + rename) : un run interrompu ne laisse jamais un
    # clients.json / company.json tronqué → la relecture aval (serveur) ne casse pas.
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


# ── Reconnaissance par identifiant STABLE (IBAN, SIREN, e-mail) ─────────────
# Un nom peut être mal OCRisé ou réordonné ; l'IBAN d'un compte et le SIREN d'une
# société sont des clés EXACTES. On les essaie AVANT le fuzzy de nom.

def find_client_by_iban(iban, clients):
    n = norm_iban(iban)
    if not n:
        return None
    for c in clients:
        if n in {norm_iban(x) for x in c.get("iban", []) if x}:
            return c["slug"]
    return None


def siren_client(siren_found, clients):
    """Si les SIREN de la pièce désignent UN seul client connu, son slug, sinon None."""
    s = {norm_siren(x) for x in (siren_found or []) if norm_siren(x)}
    s.discard("")
    if not s:
        return None
    hits = {c["slug"] for c in clients if s & {norm_siren(x) for x in c.get("siren", [])}}
    return next(iter(hits)) if len(hits) == 1 else None


def find_client_by_email(sender, domain, clients):
    """E-mail expéditeur → client connu (contact exact, sinon domaine)."""
    email = (sender or "").strip().lower()
    dom = (domain or (email.split("@")[-1] if "@" in email else "")).lower()
    for c in clients:
        if email and email in {(x.get("email") or "").lower() for x in c.get("contacts", [])}:
            return c["slug"]
        if dom and dom in {d.lower() for d in c.get("domains", [])}:
            return c["slug"]
    return None


# ── Reconnaissance par raison sociale ──────────────────────────────────────

def match_side(name, clients):
    """Reconnaît un client par sa raison sociale (indépendant de l'ordre/civilité).
    Renvoie (slug, method) ou (None, None)."""
    if not name:
        return None, None
    target = slugify(name)
    if not target:
        return None, None
    best, best_r = None, 0.0
    for c in clients:
        cand = slugify(c.get("raisonSociale", "")) or c.get("slug", "")
        if not cand:
            continue
        if cand == target:
            return c["slug"], "raison-sociale-exacte"
        r = name_match(cand, target)
        if r > best_r:
            best, best_r = c["slug"], r
    if best_r >= FUZZY_THRESHOLD:
        return best, "raison-sociale"
    return None, None


def client_name(clients, slug):
    return next((c.get("raisonSociale", slug) for c in clients if c["slug"] == slug), slug)


def upsert_client(clients, slug, raison, statut, **extra):
    for c in clients:
        if c["slug"] == slug:
            for k in ("siren", "contacts", "domains", "sources", "iban"):
                c.setdefault(k, [])
            for k, v in extra.items():
                if k not in c or not isinstance(c[k], list):
                    c[k] = list(v) if isinstance(v, list) else [v]
                    continue
                for item in (v if isinstance(v, list) else [v]):
                    if item and item not in c[k]:
                        c[k].append(item)
            return c, False
    entry = {"slug": slug, "raisonSociale": raison, "statut": statut,
             "confiance": 0.9 if statut.startswith("auto-") else 1.0,
             "aValider": False, "siren": [], "contacts": [], "domains": [],
             "sources": [], "iban": []}
    for k, v in extra.items():
        entry[k] = list(v) if isinstance(v, list) else [v]
    clients.append(entry)
    return entry, True


# ── Remontée backend Pocket-Claw : company.json (+ seed rapprochement.json) ──
# Le backend lit, PAR CLIENT, company.json (identité) + rapprochement.json (suivi).
# On sème les deux dès l'identification ; rapprochement-paiements ⑤ remplit ensuite
# le rapprochement.json (on ne l'écrase jamais s'il existe déjà).

def backend_company(entry):
    entry = entry or {}
    out = {}
    name = entry.get("raisonSociale")
    if name:
        out["name"] = name
    sirens = [s for s in (entry.get("siren") or []) if s]
    if sirens:
        d = re.sub(r"\D", "", str(sirens[0]))
        out["siren"] = d[:9] if len(d) >= 9 else str(sirens[0])
    emails = [c.get("email") for c in (entry.get("contacts") or []) if c.get("email")]
    if emails:
        out["email"] = emails[0]
    m = re.search(r"\b(SASU|SARL|SAS|EURL|SELARL|SCEA|GAEC|SCM|EIRL|SCI|SNC|SCP|SA)\b",
                  name or "", re.I)
    if m:
        out["legal_form"] = m.group(1).upper()
    ibans = [i for i in (entry.get("iban") or []) if i]
    if ibans:
        out["iban"] = ibans[0]
    return out


def seed_backend_files(clients, slug, clients_path):
    """Écrit clients/<slug>/company.json et seede rapprochement.json vide si absent."""
    entry = next((c for c in clients if c["slug"] == slug), None)
    if not entry:
        return
    cdir = Path(clients_path).parent / slug
    save_json(cdir / "company.json", backend_company(entry))
    rj = cdir / "rapprochement.json"
    if not rj.exists():
        save_json(rj, {"periods": []})


# ── Identification ─────────────────────────────────────────────────────────

def identify(dossier, clients_path):
    clients = load_json(clients_path, [])
    analyse = dossier.get("analyse") or {}
    kind = analyse.get("kind")
    f = analyse.get("fields") or {}
    email = (dossier.get("email") or {})
    sender, domain = email.get("from"), email.get("domain")

    client = {"slug": None, "role": None, "counterparty": None,
              "method": None, "confidence": "faible",
              "needs_review": True, "is_new": False, "question": None}
    touched = None

    if kind == "bank-statement":
        holder = f.get("holder")
        iban = f.get("iban")
        if not holder:
            # Titulaire ambigu (plusieurs candidats) ou illisible → NE PAS inventer.
            cands = f.get("holder_candidates") or []
            if cands:
                client["question"] = (f"Relevé {f.get('bank') or ''} : titulaire ambigu. "
                                      f"Lequel est votre client ? Candidats : {', '.join(cands)}.")
            else:
                client["question"] = ("Relevé bancaire dont le titulaire est illisible — "
                                      "à quel client le rattacher ?")
        else:
            # 1 relevé = 1 client : IBAN (exact) > nom (ordre/civilité ignorés) > nouveau.
            slug = (find_client_by_iban(iban, clients)
                    or match_side(holder, clients)[0]
                    or slugify(holder))
            extra = {"sources": ["bank-statement"]}
            ni = norm_iban(iban)
            if ni:
                extra["iban"] = [ni]
            _, is_new = upsert_client(clients, slug, holder, "auto-from-bank-statement", **extra)
            if is_new:
                # backstop supervisé : nouveau client déduit d'un relevé → à valider.
                for c in clients:
                    if c["slug"] == slug:
                        c["aValider"] = True
            method = "iban" if find_client_by_iban(iban, clients) and ni else "relevé"
            client.update(slug=slug, role="holder", method=method,
                          confidence="haute", needs_review=False, is_new=is_new)
            touched = slug

    elif kind == "invoice":
        emitter, recipient = f.get("emitter"), f.get("recipient")
        siren = f.get("siren_found")
        c_em, m_em = match_side(emitter, clients)
        c_re, m_re = match_side(recipient, clients)
        inv = f.get("invoice_id") or "(n° inconnu)"

        # Signal FORT si aucun nom reconnu : un SIREN du document ou l'e-mail
        # expéditeur appartient à un client connu → ce client est sur la pièce même
        # si son nom est mal lu. On rattache le BON côté par ressemblance de nom
        # (à défaut, l'émetteur : le SIREN imprimé est le plus souvent le sien).
        if not c_em and not c_re:
            strong = siren_client(siren, clients) or find_client_by_email(sender, domain, clients)
            if strong:
                sn = slugify(client_name(clients, strong))
                if name_match(slugify(recipient or ""), sn) > name_match(slugify(emitter or ""), sn):
                    c_re, m_re = strong, "domaine"
                else:
                    c_em, m_em = strong, "domaine"

        if c_em and not c_re:
            client.update(slug=c_em, role="out", counterparty=recipient,
                          method=m_em, needs_review=False)
        elif c_re and not c_em:
            client.update(slug=c_re, role="in", counterparty=emitter,
                          method=m_re, needs_review=False)
        elif c_em and c_re:
            client["question"] = (f"Facture {inv} — émetteur « {emitter} » ET destinataire "
                                  f"« {recipient} » sont deux clients suivis. Lequel est concerné ?")
        else:
            sc = siren_client(siren, clients)
            if sc:
                rs = client_name(clients, sc)
                client["question"] = (f"Facture {inv} — pièce probablement liée à « {rs} » "
                                      f"(SIREN reconnu), mais le sens (achat / vente) n'est pas certain. "
                                      f"Confirmez le client et le sens.")
            else:
                client["question"] = (f"Facture {inv} — émetteur « {emitter} », destinataire "
                                      f"« {recipient} ». Lequel est votre client ?")

        if not client["needs_review"]:
            conf = "haute" if client["method"] == "raison-sociale-exacte" else "moyenne"
            if siren_client(siren, clients) == client["slug"]:
                conf = "haute"
            client["confidence"] = conf
            # Enrichir le SIREN du client — UNIQUEMENT le sien (vente = émetteur) ;
            # jamais celui de la contrepartie (sinon faux matchs futurs).
            if client["role"] == "out" and siren:
                own = norm_siren(siren[0])
                if own:
                    upsert_client(clients, client["slug"],
                                  client_name(clients, client["slug"]),
                                  next((c["statut"] for c in clients if c["slug"] == client["slug"]), "confirmé"),
                                  siren=[own])
            touched = client["slug"]

    elif kind == "note-de-frais":
        # Document INTERNE : la société imprimée (avec son SIRET) EST le client dont
        # on tient les comptes — signal aussi fiable qu'un titulaire de relevé.
        company = f.get("company")
        beneficiary = f.get("beneficiary")
        siren = [norm_siren(x) for x in (f.get("siren_found") or []) if norm_siren(x)]
        if company:
            slug, method = match_side(company, clients)
            is_new = False
            if not slug:
                slug = slugify(company)
                _, is_new = upsert_client(clients, slug, company, "auto-from-note-de-frais",
                                          siren=siren, sources=["note-de-frais"])
                if is_new:
                    for c in clients:
                        if c["slug"] == slug:
                            c["aValider"] = True
                method = "raison-sociale"
            elif siren:
                upsert_client(clients, slug, company, "confirmé", siren=siren)
            conf = "haute" if (method == "raison-sociale-exacte"
                               or siren_client(f.get("siren_found"), clients) == slug) else "moyenne"
            client.update(slug=slug, role="in", counterparty=beneficiary,
                          method=method, confidence=conf, needs_review=False, is_new=is_new)
            touched = slug
        else:
            client["question"] = ("Note de frais dont l'employeur (la société) est illisible — "
                                  "à quel client la rattacher ?")
    else:
        client["question"] = None
        client["needs_review"] = False  # pièce non comptable : rien à rattacher

    # Persiste toujours le registre (créé depuis zéro au 1er passage). Sème les
    # fichiers backend (company.json + rapprochement.json vide) du client touché.
    save_json(clients_path, clients)
    if touched:
        seed_backend_files(clients, touched, clients_path)

    dossier["client"] = client
    return dossier


def main():
    args = sys.argv[1:]
    clients_path = "clients/clients.json"
    if "--clients" in args:
        i = args.index("--clients")
        clients_path = args[i + 1]
        del args[i:i + 2]
    raw = sys.stdin.read() if not args else open(args[0], encoding="utf-8").read()
    try:
        dossier = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"entrée JSON invalide : {e}"}))
        sys.exit(1)
    print(json.dumps(identify(dossier, clients_path), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
