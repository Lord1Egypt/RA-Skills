#!/usr/bin/env python3
"""
outlook_refresh.py — Rafraîchit le refresh_token Outlook avant expiration.
Utilise des requêtes HTTP directes (requests).
Sortie silencieuse si OK (pour cron), verbose si échec.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import outlook_token as ot

MARGIN_SECONDS = 300  # Refresh si < 5 min avant expiration


def main():
    token = ot.get_token()
    if not token:
        print("Aucun token stocke. Authentification requise.", file=sys.stderr)
        sys.exit(1)

    remaining = token.get("expires_at", 0) - time.time()
    if remaining > MARGIN_SECONDS:
        # Encore valide — sortie silencieuse pour cron
        print(f"Token valide ({int(remaining)}s restantes).rien a faire.")
        sys.exit(0)

    # Refresh via requete directe
    print(f"Token expiré ou proche ({int(remaining)}s). Refresh en cours...", file=sys.stderr)
    try:
        new_token = ot.refresh_token()
        print(
            f"Token rafraichi. Expire dans {new_token.get('expires_in','?')}s.",
            file=sys.stderr
        )
    except Exception as e:
        print(f"Refresh echoue : {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
