#!/usr/bin/env python3
"""
outlook_auth.py — OAuth 2.0 device code flow pour Microsoft Outlook/Graph.

Flow exact documenté par Fred :
  1. POST /devicecode  → reçoit { device_code, user_code, verification_uri }
  2. Poll /token avec grant_type=urn:ietf:params:oauth:grant-type:device_code
  3. Stocke access_token + refresh_token + expires_at

Usage :
    python outlook_auth.py              # Lance le device code flow
    python outlook_auth.py --status     # Affiche le statut du token
    python outlook_auth.py --revoke     # Révoque et supprime le token
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

DEBUG = os.getenv("DEBUG", "").lower() in ("true", "1", "yes")

def _debug_request(method, url, payload, headers, resp):
    if not DEBUG:
        return
    print(f"\n[DEBUG] >>> {method} {url}", file=sys.stderr)
    print(f"[DEBUG]     headers: {headers}", file=sys.stderr)
    safe = {k: (v[:8] + "…" if len(str(v)) > 40 else v) for k, v in payload.items()}
    print(f"[DEBUG]     payload: {safe}", file=sys.stderr)
    print(f"[DEBUG] <<< {resp.status_code} {resp.reason}", file=sys.stderr)
    try:
        body = resp.json()
        safe_body = {k: (v[:20] + "…" if isinstance(v, str) and len(v) > 40 else v) for k, v in body.items()}
        print(f"[DEBUG]     body: {json.dumps(safe_body, indent=2)}", file=sys.stderr)
    except Exception:
        print(f"[DEBUG]     body: {resp.text[:200]}", file=sys.stderr)

sys.path.insert(0, str(Path(__file__).parent))

import requests

# Chargement du .env
for _env in [Path(__file__).parent.parent / ".env", Path(__file__).parent / ".env"]:
    if _env.exists():
        with open(_env) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    v = v.strip('"').strip("'")
                    import os as _os
                    _os.environ.setdefault(k, v)

import outlook_token as ot

# ── Device Code Flow ───────────────────────────────────────────────────────────

def device_code_flow(req):
    """Implémente RFC 8628 — device code flow pour Microsoft OAuth."""

    missing = [v for v, k in [("AZURE_CLIENT_ID", ot.CLIENT_ID),
                               ("AZURE_TENANT_ID", ot.TENANT_ID)]
               if not k]
    if missing:
        print(f"Variables manquantes dans .env : {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    headers_dc = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # ── Step 1 : demander un device code ──────────────────────────────────────
    print("Demande d'autorisation a Microsoft…", file=sys.stderr)
    payload_dc = {
        "client_id": ot.CLIENT_ID,
        "scope": ot.SCOPES_DEVICE_CODE,
    }
    resp = req.post(ot.DEVICE_CODE_URL, data=payload_dc, headers=headers_dc,
                    timeout=ot.REQUEST_TIMEOUT)
    _debug_request("POST", ot.DEVICE_CODE_URL, payload_dc, headers_dc, resp)
    resp.raise_for_status()
    data = resp.json()
    device_code = data["device_code"]
    user_code   = data["user_code"]
    verif_uri   = data["verification_uri"]
    interval    = int(data.get("interval", 5))
    expires_in  = int(data.get("expires_in", 300))
    message     = data.get("message", "")

    # ── Step 2 : afficher les instructions ──────────────────────────────────────
    print()
    print("=" * 60)
    print("  AUTHENTIFICATION MICROSOFT — OFFICE 365")
    print("=" * 60)
    print()
    print(f"  1. Ouvrez cette URL dans votre navigateur :")
    print()
    print(f"     {verif_uri}")
    print()
    print(f"  2. Entrez ce code :  {user_code}")
    print()
    if message:
        print(f"  Message Microsoft : {message}")
    print(f"  Delai : {expires_in}s")
    print("=" * 60, flush=True)

    # ── Step 3 : poll le token endpoint ───────────────────────────────────────
    payload_token = {
        "grant_type":  "urn:ietf:params:oauth:grant-type:device_code",
        "client_id":   ot.CLIENT_ID,
        "device_code": device_code,
    }

    start = time.time()
    while time.time() - start < expires_in:
        resp = req.post(ot.TOKEN_URL, data=payload_token, timeout=ot.REQUEST_TIMEOUT)
        _debug_request("POST", ot.TOKEN_URL, payload_token, {"Content-Type": "application/x-www-form-urlencoded"}, resp)
        data = resp.json()

        if resp.status_code == 200 and "access_token" in data:
            token_data = data.copy()
            token_data["expires_at"] = time.time() + token_data.get("expires_in", 3600)
            ot.save_token(token_data)
            print(file=sys.stderr)
            print("Authentification reussie !", file=sys.stderr)
            print(f"   access_token  : {token_data['access_token'][:20]}…", file=sys.stderr)
            print(f"   refresh_token : {token_data.get('refresh_token', 'N/A')[:20]}…",
                  file=sys.stderr)
            print(f"   expires_in    : {token_data.get('expires_in', '?')}s",
                  file=sys.stderr)
            return

        error = data.get("error")
        desc  = data.get("error_description", "")

        if error == "authorization_pending":
            time.sleep(interval)
            continue
        if error == "slow_down":
            interval = max(interval + 5, 10)
            time.sleep(interval)
            continue

        # Autres erreurs (y compris 400 HTTP) — on log et on sort
        print(f"Erreur Microsoft : [{error}] {desc}", file=sys.stderr)
        sys.exit(1)

    print("Delai d'authentification expire. Relancez la commande.", file=sys.stderr)
    sys.exit(1)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Outlook OAuth 2.0 — device code flow")
    ap.add_argument("--status",      action="store_true", help="Afficher le statut du token")
    ap.add_argument("--revoke",      action="store_true", help="Revoquer le token et deconnecter")
    args = ap.parse_args()

    if args.status:
        token = ot.get_token()
        if not token:
            print("Aucun token stocke (non authentifie).")
            sys.exit(1)
        expired = ot.is_token_expired(token)
        remaining = max(0, int(token.get("expires_at", 0) - time.time()))
        status = "EXPIRE" if expired else f"Valide ({remaining}s restantes)"
        print(f"Token : {status}")
        print(f"Token type : {token.get('token_type', '?')}")
        print(f"Scope       : {token.get('scope', '?')}")
        sys.exit(0)

    if args.revoke:
        ot.revoke_token()
        print("Token revoque et supprime.")
        sys.exit(0)

    # Par defaut : lancer le device code flow
    device_code_flow(requests)


if __name__ == "__main__":
    main()
