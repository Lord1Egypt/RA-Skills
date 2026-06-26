#!/usr/bin/env python3
"""
Orchestrateur du pipeline comptable.

Enchaîne, dans l'ordre, les petites briques mono-tâche — comme une assistante
qui traite son courrier du matin :

  ① tri-courrier-entrant   → ce mail me concerne ? quelles pièces ?
  ② analyse-piece-comptable → qu'est-ce que c'est ? quels montants ?
  ③ identification-client   → à quel client ça appartient ?
  ④ classement-document     → je range au bon endroit.

Chaque brique reste indépendante : l'orchestrateur ne fait que les appeler dans
l'ordre et passer le « dossier » JSON de l'une à l'autre. Si une brique évolue,
l'orchestrateur n'a pas à changer.

Deux modes :
  python3 pipeline.py --email <mail.json> [--clients-root <dir>]
      Part d'un mail : tri ① puis ②③④ pour chaque pièce.
  python3 pipeline.py --inbox <dossier> [--clients-root <dir>]
      Part d'un dossier de pièces déjà déposées : ②③④ pour chaque fichier
      (pas de mail, donc pas d'étape ①).

Sortie : un rapport JSON consolidé sur stdout + un résumé lisible sur stderr.
"""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

PY = sys.executable or "python3"
SKILLS = Path(__file__).resolve().parents[2]   # …/workspace/skills

TRI = SKILLS / "tri-courrier-entrant" / "scripts" / "tri.py"
ANALYSE = SKILLS / "analyse-piece-comptable" / "scripts" / "analyse.py"
IDENT = SKILLS / "identification-client" / "scripts" / "identifier.py"
CLASSER = SKILLS / "classement-document" / "scripts" / "classer.py"
RAPPRO = SKILLS / "rapprochement-paiements" / "scripts" / "main.py"


def _run(cmd, stdin_obj=None):
    """Lance une brique et renvoie son JSON de sortie (ou {'error': …})."""
    res = subprocess.run([PY, *map(str, cmd)],
                         input=json.dumps(stdin_obj) if stdin_obj is not None else None,
                         capture_output=True, text=True)
    if res.returncode != 0:
        return {"error": res.stderr.strip() or f"échec de {cmd[0]}"}
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return {"error": f"sortie illisible de {Path(str(cmd[0])).name}: {res.stdout[:200]}"}


def ensure_root(clients_root):
    """Crée tout depuis zéro si rien n'existe : dossier racine + registre vide."""
    root = Path(clients_root)
    root.mkdir(parents=True, exist_ok=True)
    cj = root / "clients.json"
    if not cj.exists():
        cj.write_text("[]", encoding="utf-8")


def analyse_piece(src_path, filename, email, today):
    """② seulement : lit la pièce, renvoie un dossier non encore identifié."""
    analyse = _run([ANALYSE, src_path, "--date-ref", today])
    return {"source": {"path": str(src_path), "filename": filename},
            "email": email or {}, "analyse": analyse}


def identify_and_file(dossier, clients_root):
    """③ puis ④ : reconnaît le client, puis range."""
    dossier = _run([IDENT, "--clients", str(Path(clients_root) / "clients.json")], dossier)
    dossier = _run([CLASSER, "--clients-root", str(clients_root)], dossier)
    return dossier


def process_batch(dossiers, clients_root):
    """Comme le ferait une assistante : on traite d'abord les relevés bancaires
    (ils créent/identifient les clients avec certitude), puis tout le reste, pour
    que les factures puissent être rattachées aux clients fraîchement connus."""
    def is_statement(d):
        return (d.get("analyse") or {}).get("kind") == "bank-statement"
    ordered = [d for d in dossiers if is_statement(d)] + [d for d in dossiers if not is_statement(d)]
    return [identify_and_file(d, clients_root) for d in ordered]


_DOC_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp", ".heic"}


def run_inbox(inbox, clients_root, today):
    ensure_root(clients_root)
    # PDF ET images : une facture / note de frais peut être scannée ou photographiée.
    # On ignore les artefacts d'archives macOS (« ._x », « __MACOSX »).
    pieces = sorted(p for p in Path(inbox).rglob("*")
                    if p.is_file() and p.suffix.lower() in _DOC_EXTS
                    and not p.name.startswith("._") and "__MACOSX" not in p.parts)
    dossiers = [analyse_piece(p, p.name, {}, today) for p in pieces]
    return process_batch(dossiers, clients_root)


def run_email(mail_path, clients_root, today):
    ensure_root(clients_root)
    mail = json.loads(Path(mail_path).read_text(encoding="utf-8"))
    tri = _run([TRI], mail)
    if not tri.get("relevant"):
        return {"tri": tri, "dossiers": []}
    dossiers = [analyse_piece(pc.get("path"), pc.get("filename"), tri.get("email"), today)
                for pc in tri.get("pieces", [])]
    return {"tri": tri, "dossiers": process_batch(dossiers, clients_root)}


def run_rapprochement(clients_root):
    """⑤ Rapproche les paiements une fois les pièces classées. Le moteur retraite
    tout le dossier (cache reconstructible), donc on le lance sur la racine entière."""
    res = subprocess.run([PY, str(RAPPRO), str(clients_root)], capture_output=True, text=True)
    return {"ok": res.returncode == 0, "summary": (res.stdout or res.stderr).strip()}


# ── Résumé lisible ─────────────────────────────────────────────────────────

def summarize(dossiers):
    lines, questions, incomplets = [], [], []
    counts = {"classé": 0, "doublon": 0, "_a-identifier": 0, "_incomplet": 0,
              "_non-attribue": 0, "erreur": 0}
    for d in dossiers:
        cl = (d.get("classement") or {})
        st = cl.get("status", "erreur")
        counts[st] = counts.get(st, 0) + 1
        q = (d.get("client") or {}).get("question")
        if q:
            questions.append(q)
        if st == "_incomplet":
            incomplets.append((d.get("source") or {}).get("filename"))
    lines.append(f"Pièces traitées : {len(dossiers)}")
    lines.append(f"  Rangées : {counts['classé']}   Doublons : {counts['doublon']}")
    if counts["_a-identifier"]:
        lines.append(f"  Client à confirmer : {counts['_a-identifier']}")
    if counts["_incomplet"]:
        lines.append(f"  Extraction incomplète : {counts['_incomplet']} ({', '.join(filter(None, incomplets))})")
    if counts["_non-attribue"]:
        lines.append(f"  Non comptables : {counts['_non-attribue']}")
    if counts["erreur"]:
        lines.append(f"  Erreurs : {counts['erreur']}")
    for q in questions:
        lines.append(f"  ❓ {q}")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    clients_root, mail_path, inbox = "clients", None, None
    no_rappro = "--no-rapprochement" in args
    if no_rappro:
        args.remove("--no-rapprochement")
    if "--clients-root" in args:
        i = args.index("--clients-root"); clients_root = args[i + 1]; del args[i:i + 2]
    if "--email" in args:
        i = args.index("--email"); mail_path = args[i + 1]; del args[i:i + 2]
    if "--inbox" in args:
        i = args.index("--inbox"); inbox = args[i + 1]; del args[i:i + 2]

    today = date.today().isoformat()

    if mail_path:
        out = run_email(mail_path, clients_root, today)
        dossiers = out["dossiers"]
        report = {"mode": "email", "tri": out["tri"], "dossiers": dossiers}
    elif inbox:
        dossiers = run_inbox(inbox, clients_root, today)
        report = {"mode": "inbox", "dossiers": dossiers}
    else:
        print("usage: pipeline.py --email <mail.json> | --inbox <dossier> "
              "[--clients-root <dir>] [--no-rapprochement]")
        sys.exit(1)

    # ⑤ Rapprochement automatique une fois les pièces classées.
    rappro = None
    if not no_rappro:
        rappro = run_rapprochement(clients_root)
        report["rapprochement"] = rappro

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\n" + summarize(dossiers), file=sys.stderr)
    if rappro:
        print("\nRapprochement des paiements :", file=sys.stderr)
        print("  " + rappro["summary"].replace("\n", "\n  "), file=sys.stderr)


if __name__ == "__main__":
    main()
