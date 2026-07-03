#!/usr/bin/env python3
"""
outlook_graph.py — Appels Microsoft Graph API pour Outlook (mail, calendar, contacts).

Usage :
    python outlook_graph.py folders                          # Liste des dossiers mail
    python outlook_graph.py messages [--folder Inbox] [--top 10]   # Liste messages
    python outlook_graph.py message <id>                     # Détail d'un message
    python outlook_graph.py attachments <id>                 # Liste pièces jointes
    python outlook_graph.py download <id> --attach <aid> [--output file]  # Télécharger pièce jointe
    python outlook_graph.py events [--top 10]               # Événements calendrier
    python outlook_graph.py contacts [--top 20]             # Contacts
    python outlook_graph.py search <query>                  # Rechercher dans les mails
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import html2text
import requests

# Load .env
for _env in [Path(__file__).parent.parent / ".env", Path(__file__).parent / ".env"]:
    if _env.exists():
        with open(_env) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    v = v.strip('"').strip("'")
                    os.environ.setdefault(k, v)

import outlook_token as ot

GRAPH_BASE = ot.GRAPH_BASE
TIMEOUT    = ot.REQUEST_TIMEOUT

# ── HTTP helpers ───────────────────────────────────────────────────────────────

def graph_get(path: str, params: dict = None, token: str = None) -> dict:
    token = token or ot.ensure_valid_token()
    url   = f"{GRAPH_BASE}{path}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    resp = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
    _handle_error(resp)
    return resp.json()

def graph_get_raw(path: str, token: str = None) -> requests.Response:
    token = token or ot.ensure_valid_token()
    url   = f"{GRAPH_BASE}{path}"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    _handle_error(resp)
    return resp

def _handle_error(resp):
    if resp.status_code >= 400:
        try:
            err = resp.json()
            msg = err.get("error", {}).get("message", err.get("error", "Unknown"))
            code = err.get("error", {}).get("code", "")
        except Exception:
            msg = resp.text[:200]
            code = ""

        # 401 InvalidAuthenticationToken → token expiré ou révoqué
        if resp.status_code == 401 and code == "InvalidAuthenticationToken":
            token_path = Path(ot.TOKEN_FILE)
            if token_path.exists():
                token_path.unlink()
            raise RuntimeError(
                f"Graph API 401 — token invalidé. "
                f"Relancez l'authentification : python scripts/outlook_auth.py"
            )

        raise RuntimeError(f"Graph API {resp.status_code}: {msg}")

# ── Formatters ────────────────────────────────────────────────────────────────

def fmt_message(m: dict) -> str:
    sender  = m.get("from",  {}).get("emailAddress", {})
    received = m.get("receivedDateTime", "")
    subj    = m.get("subject", "(sans objet)")
    read    = "✅" if m.get("isRead", False) else "📩"
    attach  = "📎" if m.get("hasAttachments", False) else ""
    return f"{read}{attach}  [{received[:10]}] {sender.get('name','?')} — {subj}\n   ID: {m.get('id','?')}"

def fmt_event(e: dict) -> str:
    start = e.get("start", {}).get("dateTime", "?")
    end   = e.get("end",   {}).get("dateTime", "?")
    loc   = e.get("location", {}).get("displayName", "")
    att   = len(e.get("attendees", []))
    return f"📅  {start[:16]} → {end[:16]}  |  {e.get('subject','?')}\n   📍 {loc}  | 👥 {att} attendees\n   ID: {e.get('id','?')}"

def fmt_contact(c: dict) -> str:
    name = f"{c.get('givenName','?')} {c.get('surname','?')}".strip()
    email = c.get("emailAddresses", [{}])[0].get("address", "?")
    return f"👤 {name}  <{email}>"

# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_folders(_args):
    data = graph_get("/me/mailFolders")
    for f in data.get("value", []):
        print(f"  📁 [{f.get('totalItemCount','?')} msgs] {f.get('displayName','?')}  (id: {f.get('id','?')})")

def cmd_messages(args):
    folder = args.folder or "Inbox"
    top    = args.top or 10
    data   = graph_get(f"/me/mailFolders/{folder}/messages",
                       params={"$top": top, "$orderby": "receivedDateTime desc",
                               "$select": "id,subject,from,receivedDateTime,isRead,hasAttachments"})
    for m in data.get("value", []):
        print(fmt_message(m))

def cmd_message(args):
    m = graph_get(f"/me/messages/{args.message_id}",
                  params={"$select": "id,subject,from,toRecipients,receivedDateTime,isRead,body,hasAttachments"})
    print(f"De    : {m.get('from',{}).get('emailAddress',{})}")
    print(f"À     : {[r['emailAddress']['address'] for r in m.get('toRecipients',[])]}")
    print(f"Date  : {m.get('receivedDateTime','?')}")
    print(f"Lu    : {'Oui' if m.get('isRead') else 'Non'}")
    print(f"Pièces: {'Oui' if m.get('hasAttachments') else 'Non'}")
    print()
    print("── Corps ──")
    body = m.get("body", {})
    raw_html = body.get("content", "(vide)")
    body_type = body.get("contentType", "")
    if "html" in body_type.lower():
        h2t = html2text.HTML2Text()
        h2t.body_width = 0  # no wrap
        h2t.ignore_links = False
        md = h2t.handle(raw_html).strip()
        print(md if md else raw_html)
    else:
        print(raw_html)

def cmd_attachments(args):
    data = graph_get(f"/me/messages/{args.message_id}/attachments",
                     params={"$select": "id,name,size,contentType"})
    items = data.get("value", [])
    if not items:
        print("  (aucune pièce jointe)")
        return
    for a in items:
        size_kb = a.get("size", 0) / 1024
        print(f"  📎 {a.get('name','?')}  ({size_kb:.1f} KB, {a.get('contentType','?')})")
        print(f"     ID: {a.get('id','?')}")

def cmd_download(args):
    data = graph_get(f"/me/messages/{args.message_id}/attachments/{args.attach_id}",
                     params={"$select": "id,name,size,contentType,contentBytes"})
    name = data.get("name", "attachment")
    content_bytes = data.get("contentBytes")
    out_path = Path(args.output) if args.output else Path(name)

    if content_bytes:
        raw = base64.b64decode(content_bytes)
    else:
        resp = graph_get_raw(f"/me/messages/{args.message_id}/attachments/{args.attach_id}/$value")
        raw = resp.content

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    print(f"✅ {name} → {out_path} ({len(raw)} bytes)")

def cmd_events(args):
    top = args.top or 10
    data = graph_get("/me/calendar/events",
                     params={"$top": top, "$orderby": "start/dateTime asc",
                             "$select": "id,subject,start,end,location,attendees"})
    for e in data.get("value", []):
        print(fmt_event(e))
        print()

def cmd_contacts(args):
    top = args.top or 20
    data = graph_get("/me/contacts",
                     params={"$top": top, "$orderby": "givenName",
                             "$select": "id,givenName,surname,emailAddresses"})
    for c in data.get("value", []):
        print(fmt_contact(c))

def cmd_search(args):
    data = graph_get("/me/messages",
                     params={"$top": args.top or 10,
                             "$search": f'"{args.query}"',
                             "$select": "id,subject,from,receivedDateTime,isRead"})
    print(f"Résultats pour « {args.query} » :")
    for m in data.get("value", []):
        print(fmt_message(m))

def cmd_profile(_args):
    me = graph_get("/me")
    print(f"Nom      : {me.get('displayName','?')}")
    print(f"Email    : {me.get('mail','?')}")
    print(f"ID Entra : {me.get('id','?')}")

# ── CLI parser ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(prog="outlook_graph",
                                    description="Microsoft Graph API — Outlook")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("folders", help="Lister les dossiers mail")

    p_msgs = sub.add_parser("messages", help="Lister les messages")
    p_msgs.add_argument("--folder", default="Inbox")
    p_msgs.add_argument("--top", type=int, default=10)

    p_msg = sub.add_parser("message", help="Détail d'un message")
    p_msg.add_argument("message_id")
    p_msg.add_argument("--raw", action="store_true", help="Renvoyer le HTML brut (sans conversion Markdown)")

    p_att = sub.add_parser("attachments", help="Lister les pièces jointes")
    p_att.add_argument("message_id")

    p_dl = sub.add_parser("download", help="Télécharger une pièce jointe")
    p_dl.add_argument("message_id")
    p_dl.add_argument("--attach-id", required=True, help="ID de la pièce jointe")
    p_dl.add_argument("--output", "-o", default=None, help="Chemin de destination")

    p_events = sub.add_parser("events", help="Événements calendrier")
    p_events.add_argument("--top", type=int, default=10)

    p_contacts = sub.add_parser("contacts", help="Contacts")
    p_contacts.add_argument("--top", type=int, default=20)

    p_search = sub.add_parser("search", help="Rechercher dans les mails")
    p_search.add_argument("query")
    p_search.add_argument("--top", type=int, default=10)

    sub.add_parser("profile", help="Profil utilisateur")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        sys.exit(0)

    cmds = {
        "folders":      cmd_folders,
        "messages":     cmd_messages,
        "message":      cmd_message,
        "attachments":  cmd_attachments,
        "download":     cmd_download,
        "events":       cmd_events,
        "contacts":     cmd_contacts,
        "search":       cmd_search,
        "profile":      cmd_profile,
    }

    try:
        cmds[args.cmd](args)
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Interrompu.", file=sys.stderr)
        sys.exit(130)

if __name__ == "__main__":
    main()
