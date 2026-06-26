from __future__ import annotations

import argparse

from common import dump_json
from spotify import authorize, get_access_token, request_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Spotify OAuth and save a reusable token.")
    parser.add_argument(
        "--scope",
        action="append",
        dest="scopes",
        default=None,
        help="Spotify scope. Repeat as needed. If omitted, a sensible default is used.",
    )
    parser.add_argument("--spotify-creds", help="Path to Spotify credentials JSON file.")
    parser.add_argument("--spotify-token", help="Path to Spotify token JSON file.")
    parser.add_argument("--no-browser", action="store_true", help="Print auth URL instead of opening browser.")
    args = parser.parse_args()

    scopes = args.scopes or [
        "playlist-modify-private",
        "playlist-modify-public",
    ]
    token = authorize(
        scopes,
        creds_path=args.spotify_creds,
        token_path=args.spotify_token,
        open_browser=not args.no_browser,
    )
    access_token = get_access_token(creds_path=args.spotify_creds, token_path=args.spotify_token)
    me = request_json("https://api.spotify.com/v1/me", token=access_token)
    dump_json({
        "saved": True,
        "scope": token.get("scope"),
        "access_token_present": bool(token.get("access_token")),
        "refresh_token_present": bool(token.get("refresh_token")),
        "user_id": me.get("id"),
        "display_name": me.get("display_name"),
    })


if __name__ == "__main__":
    main()
