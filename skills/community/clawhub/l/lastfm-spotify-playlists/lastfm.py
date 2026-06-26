from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_ROOT = "https://ws.audioscrobbler.com/2.0/"
DEFAULT_CREDS_PATH = Path.home() / ".openclaw" / "lastfm-credentials.json"


class LastFMError(RuntimeError):
    pass


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


class LastFMClient:
    def __init__(self, *, explicit_path: str | None = None, api_key: str | None = None) -> None:
        self._api_key = api_key or self.load_credentials(explicit_path).get("api_key")
        if not self._api_key:
            raise LastFMError(
                "Missing Last.fm API key. Set LASTFM_API_KEY or create ~/.openclaw/lastfm-credentials.json"
            )

    @staticmethod
    def load_credentials(explicit_path: str | None = None) -> dict[str, str]:
        creds: dict[str, str] = {}

        env_key = os.getenv("LASTFM_API_KEY")
        env_secret = os.getenv("LASTFM_SHARED_SECRET")
        env_user = os.getenv("LASTFM_USERNAME")
        if env_key:
            creds["api_key"] = env_key
        if env_secret:
            creds["shared_secret"] = env_secret
        if env_user:
            creds["username"] = env_user

        path = Path(explicit_path) if explicit_path else DEFAULT_CREDS_PATH
        if path.exists():
            file_creds = json.loads(path.read_text(encoding="utf-8"))
            for key in ("api_key", "shared_secret", "username"):
                if file_creds.get(key) and key not in creds:
                    creds[key] = str(file_creds[key])
        return creds

    def get(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        query: dict[str, Any] = {
            "method": method,
            "api_key": self._api_key,
            "format": "json",
        }
        if params:
            for key, value in params.items():
                if value is not None:
                    query[key] = value

        url = API_ROOT + "?" + urllib.parse.urlencode(query)
        with urllib.request.urlopen(url) as response:
            payload = response.read().decode("utf-8")
        data = json.loads(payload)

        if "error" in data:
            raise LastFMError(f"Last.fm error {data['error']}: {data.get('message', 'Unknown error')}")
        return data


def normalize_recent_track(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "track": item.get("name"),
        "artist": item.get("artist", {}).get("#text") if isinstance(item.get("artist"), dict) else item.get("artist"),
        "album": item.get("album", {}).get("#text") if isinstance(item.get("album"), dict) else item.get("album"),
        "nowplaying": item.get("@attr", {}).get("nowplaying") == "true",
        "played_at": item.get("date", {}).get("#text"),
        "uts": item.get("date", {}).get("uts"),
        "url": item.get("url"),
        "loved": item.get("loved") == "1",
    }


def normalize_top_artist(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "artist": item.get("name"),
        "playcount": int(item.get("playcount", 0) or 0),
        "listeners": int(item.get("listeners", 0) or 0),
        "mbid": item.get("mbid") or None,
        "url": item.get("url"),
    }


def normalize_top_track(item: dict[str, Any]) -> dict[str, Any]:
    artist = item.get("artist", {}) if isinstance(item.get("artist"), dict) else {}
    return {
        "track": item.get("name"),
        "artist": artist.get("name") or artist.get("#text"),
        "playcount": int(item.get("playcount", 0) or 0),
        "listeners": int(item.get("listeners", 0) or 0),
        "mbid": item.get("mbid") or None,
        "url": item.get("url"),
    }


def normalize_similar_artist(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "artist": item.get("name"),
        "match": float(item.get("match", 0.0) or 0.0),
        "mbid": item.get("mbid") or None,
        "url": item.get("url"),
    }


def normalize_similar_track(item: dict[str, Any]) -> dict[str, Any]:
    artist = item.get("artist", {}) if isinstance(item.get("artist"), dict) else {}
    return {
        "track": item.get("name"),
        "artist": artist.get("name") or artist.get("#text"),
        "match": float(item.get("match", 0.0) or 0.0),
        "mbid": item.get("mbid") or None,
        "url": item.get("url"),
    }


def normalize_seed_track(item: dict[str, Any]) -> dict[str, Any]:
    artist = item.get("artist", {}) if isinstance(item.get("artist"), dict) else {}
    return {
        "track": item.get("name"),
        "artist": artist.get("name") or artist.get("#text"),
        "playcount": int(item.get("playcount", 0) or 0),
        "listeners": int(item.get("listeners", 0) or 0),
        "url": item.get("url"),
    }


def get_recent_tracks(client: LastFMClient, *, user: str, limit: int, page: int = 1) -> list[dict]:
    data = client.get(
        "user.getrecenttracks",
        {"user": user, "limit": limit, "page": page, "extended": 0},
    )
    tracks = ensure_list(data.get("recenttracks", {}).get("track"))
    return [normalize_recent_track(item) for item in tracks]


def get_top_artists(client: LastFMClient, *, user: str, period: str, limit: int, page: int = 1) -> list[dict]:
    data = client.get(
        "user.gettopartists",
        {"user": user, "period": period, "limit": limit, "page": page},
    )
    artists = ensure_list(data.get("topartists", {}).get("artist"))
    return [normalize_top_artist(item) for item in artists]


def get_top_tracks(client: LastFMClient, *, user: str, period: str, limit: int, page: int = 1) -> list[dict]:
    data = client.get(
        "user.gettoptracks",
        {"user": user, "period": period, "limit": limit, "page": page},
    )
    tracks = ensure_list(data.get("toptracks", {}).get("track"))
    return [normalize_top_track(item) for item in tracks]


def get_artist_top_tracks(client: LastFMClient, *, artist: str, limit: int, autocorrect: int = 1) -> list[dict]:
    data = client.get(
        "artist.gettoptracks",
        {"artist": artist, "limit": limit, "autocorrect": autocorrect},
    )
    tracks = ensure_list(data.get("toptracks", {}).get("track"))
    return [normalize_seed_track(item) for item in tracks]


def get_similar_artists(client: LastFMClient, *, artist: str, limit: int, autocorrect: int = 1) -> list[dict]:
    data = client.get(
        "artist.getsimilar",
        {"artist": artist, "limit": limit, "autocorrect": autocorrect},
    )
    artists = ensure_list(data.get("similarartists", {}).get("artist"))
    return [normalize_similar_artist(item) for item in artists]


def get_similar_tracks(client: LastFMClient, *, artist: str, track: str, limit: int, autocorrect: int = 1) -> list[dict]:
    data = client.get(
        "track.getsimilar",
        {"artist": artist, "track": track, "limit": limit, "autocorrect": autocorrect},
    )
    tracks = ensure_list(data.get("similartracks", {}).get("track"))
    return [normalize_similar_track(item) for item in tracks]
