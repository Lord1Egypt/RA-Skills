#!/usr/bin/env python3
"""
Spotify Recently Played Tracker
Fetches recently played tracks from Spotify API and outputs JSON.
Requires SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_REFRESH_TOKEN environment variables.
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Pull recent Spotify listening history into music ConsumptionSignals.')
    print("Usage: spotify_history_puller.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)
import os
import json
import requests
from datetime import datetime, timedelta
import sys

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 spotify_history_puller.py")
    sys.exit(0)


def get_access_token():
    """Exchange refresh token for access token."""
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
    
    # Enumerate which credentials are present vs missing for diagnostics
    missing = []
    if not client_id:
        missing.append("SPOTIFY_CLIENT_ID")
    if not client_secret:
        missing.append("SPOTIFY_CLIENT_SECRET")
    if not refresh_token:
        missing.append("SPOTIFY_REFRESH_TOKEN")
    
    if missing:
        present = []
        if client_id:
            present.append("SPOTIFY_CLIENT_ID")
        if client_secret:
            present.append("SPOTIFY_CLIENT_SECRET")
        if refresh_token:
            present.append("SPOTIFY_REFRESH_TOKEN")
        
        msg = f"Missing Spotify credentials: {', '.join(missing)}"
        if present:
            msg += f" (present: {', '.join(present)})"
        msg += ". The refresh token requires completing the OAuth Authorization Code flow interactively."
        raise ValueError(msg)
    
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret
        }
    )
    response.raise_for_status()
    return response.json()["access_token"]

def get_recently_played(access_token, limit=50):
    """Fetch recently played tracks."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played",
        headers=headers,
        params={"limit": limit}
    )
    response.raise_for_status()
    return response.json()

def main():
    try:
        token = get_access_token()
        data = get_recently_played(token)
        
        tracks = []
        for item in data.get("items", []):
            track = item.get("track", {})
            played_at = item.get("played_at")
            
            if played_at:
                dt = datetime.strptime(played_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                played_at = dt.isoformat() + "Z"
            
            tracks.append({
                "id": track.get("id"),
                "name": track.get("name"),
                "artist": ", ".join(artist.get("name") for artist in track.get("artists", [])),
                "album": track.get("album", {}).get("name"),
                "played_at": played_at,
                "duration_ms": track.get("duration_ms")
            })
        
        print(json.dumps(tracks, indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=__import__("sys").stderr)
        exit(1)

if __name__ == "__main__":
    main()