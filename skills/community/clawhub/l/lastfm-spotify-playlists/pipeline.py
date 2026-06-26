from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from lastfm import LastFMClient, get_artist_top_tracks, get_recent_tracks, get_similar_tracks, get_top_artists
from spotify import add_tracks_to_playlist, create_playlist, get_access_token, search_tracks


def normalized_key(artist: str, track: str) -> tuple[str, str]:
    return artist.strip().casefold(), track.strip().casefold()


@dataclass(slots=True)
class TrackSeed:
    artist: str
    track: str
    url: str | None = None
    playcount: int = 0
    listeners: int = 0
    origin_artist: str | None = None


@dataclass(slots=True)
class CandidateSource:
    seed: str
    match: float


@dataclass(slots=True)
class RankedCandidate:
    artist: str
    track: str
    score: float = 0.0
    source_count: int = 0
    sources: list[CandidateSource] = field(default_factory=list)
    url: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "artist": self.artist,
            "track": self.track,
            "score": self.score,
            "source_count": self.source_count,
            "sources": [{"seed": source.seed, "match": source.match} for source in self.sources],
            "url": self.url,
        }


def merge_candidate(
    merged: dict[tuple[str, str], RankedCandidate],
    *,
    key: tuple[str, str],
    artist: str,
    track: str,
    match: float,
    seed_label: str,
    root_artist: str | None = None,
    url: str | None = None,
) -> None:
    if not artist or not track:
        return
    if root_artist and artist.casefold() == root_artist.casefold():
        return

    if key not in merged:
        merged[key] = RankedCandidate(artist=artist, track=track, url=url)

    candidate = merged[key]
    candidate.score += float(match or 0.0)
    candidate.source_count += 1
    candidate.sources.append(CandidateSource(seed=seed_label, match=float(match or 0.0)))
    if not candidate.url and url:
        candidate.url = url


def rank_candidates(candidates: dict[tuple[str, str], RankedCandidate]) -> list[RankedCandidate]:
    return sorted(candidates.values(), key=lambda item: (item.source_count, item.score), reverse=True)


def artist_top_track_seeds(
    client: LastFMClient,
    *,
    artist: str,
    seed_count: int,
    autocorrect: int = 1,
) -> list[TrackSeed]:
    items = get_artist_top_tracks(client, artist=artist, limit=seed_count, autocorrect=autocorrect)
    return [
        TrackSeed(
            artist=item.get("artist") or artist,
            track=item.get("track") or "",
            url=item.get("url"),
            playcount=item.get("playcount", 0),
            listeners=item.get("listeners", 0),
            origin_artist=artist,
        )
        for item in items
        if item.get("track")
    ]


def recent_track_seeds(client: LastFMClient, *, user: str, limit: int) -> list[TrackSeed]:
    items = get_recent_tracks(client, user=user, limit=limit, page=1)
    seeds: list[TrackSeed] = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        artist = item.get("artist") or ""
        track = item.get("track") or ""
        if not artist or not track:
            continue
        key = normalized_key(artist, track)
        if key in seen:
            continue
        seen.add(key)
        seeds.append(TrackSeed(artist=artist, track=track, url=item.get("url")))
    return seeds


def top_artist_names(client: LastFMClient, *, user: str, period: str, limit: int) -> list[str]:
    items = get_top_artists(client, user=user, period=period, limit=limit, page=1)
    return [item["artist"] for item in items if item.get("artist")]


def _build_from_seeds(
    client: LastFMClient,
    *,
    seeds: list[TrackSeed],
    similar_per_seed: int,
    autocorrect: int = 1,
    root_artist: str | None = None,
) -> list[RankedCandidate]:
    merged: dict[tuple[str, str], RankedCandidate] = {}
    for seed in seeds:
        similar_tracks = get_similar_tracks(
            client,
            artist=seed.artist,
            track=seed.track,
            limit=similar_per_seed,
            autocorrect=autocorrect,
        )
        for item in similar_tracks:
            artist = item.get("artist") or ""
            track = item.get("track") or ""
            merge_candidate(
                merged,
                key=normalized_key(artist, track),
                artist=artist,
                track=track,
                match=float(item.get("match", 0.0) or 0.0),
                seed_label=f"{seed.artist} - {seed.track}",
                root_artist=root_artist or seed.artist,
                url=item.get("url"),
            )
    return rank_candidates(merged)


def build_from_artist_top_tracks(
    client: LastFMClient,
    *,
    artist: str,
    seed_count: int,
    similar_per_seed: int,
    autocorrect: int = 1,
) -> tuple[list[TrackSeed], list[RankedCandidate]]:
    seeds = artist_top_track_seeds(client, artist=artist, seed_count=seed_count, autocorrect=autocorrect)
    ranked = _build_from_seeds(
        client,
        seeds=seeds,
        similar_per_seed=similar_per_seed,
        autocorrect=autocorrect,
        root_artist=artist,
    )
    return seeds, ranked


def build_from_recent_tracks(
    client: LastFMClient,
    *,
    user: str,
    recent_count: int,
    similar_per_seed: int,
    autocorrect: int = 1,
) -> tuple[list[TrackSeed], list[RankedCandidate]]:
    seeds = recent_track_seeds(client, user=user, limit=recent_count)
    ranked = _build_from_seeds(
        client,
        seeds=seeds,
        similar_per_seed=similar_per_seed,
        autocorrect=autocorrect,
        root_artist=None,
    )
    return seeds, ranked


def build_from_track_seed(
    client: LastFMClient,
    *,
    artist: str,
    track: str,
    similar_per_seed: int,
    autocorrect: int = 1,
) -> tuple[list[TrackSeed], list[RankedCandidate]]:
    seeds = [TrackSeed(artist=artist, track=track, origin_artist=artist)]
    ranked = _build_from_seeds(
        client,
        seeds=seeds,
        similar_per_seed=similar_per_seed,
        autocorrect=autocorrect,
        root_artist=artist,
    )
    return seeds, ranked


def build_from_top_artists(
    client: LastFMClient,
    *,
    user: str,
    period: str,
    artist_count: int,
    seed_count_per_artist: int,
    similar_per_seed: int,
    autocorrect: int = 1,
) -> tuple[list[TrackSeed], list[RankedCandidate]]:
    artist_names = top_artist_names(client, user=user, period=period, limit=artist_count)
    all_seeds: list[TrackSeed] = []
    merged: dict[tuple[str, str], RankedCandidate] = {}

    for artist in artist_names:
        artist_seeds, artist_ranked = build_from_artist_top_tracks(
            client,
            artist=artist,
            seed_count=seed_count_per_artist,
            similar_per_seed=similar_per_seed,
            autocorrect=autocorrect,
        )
        all_seeds.extend(artist_seeds)
        for candidate in artist_ranked:
            key = normalized_key(candidate.artist, candidate.track)
            if key not in merged:
                merged[key] = RankedCandidate(
                    artist=candidate.artist,
                    track=candidate.track,
                    score=candidate.score,
                    source_count=candidate.source_count,
                    sources=list(candidate.sources),
                    url=candidate.url,
                )
                continue
            existing = merged[key]
            existing.score += candidate.score
            existing.source_count += candidate.source_count
            existing.sources.extend(candidate.sources)
            if not existing.url and candidate.url:
                existing.url = candidate.url

    return all_seeds, rank_candidates(merged)


def match_candidates_on_spotify(
    candidates: list[RankedCandidate],
    *,
    access_token: str,
    final_limit: int,
    market: str | None = None,
) -> tuple[list[dict], list[str], list[dict]]:
    matched: list[dict] = []
    unmatched: list[dict] = []
    uris: list[str] = []

    for candidate in candidates:
        if len(uris) >= final_limit:
            break
        query = f'track:"{candidate.track}" artist:"{candidate.artist}"'
        result = search_tracks(query, access_token=access_token, limit=5, market=market)
        items = result.get("tracks", {}).get("items", [])
        pick = None

        for item in items:
            item_name = (item.get("name") or "").strip().casefold()
            artist_names = [(a.get("name") or "").strip().casefold() for a in item.get("artists", [])]
            if item_name == candidate.track.strip().casefold() and candidate.artist.strip().casefold() in artist_names:
                pick = item
                break

        if not pick and items:
            pick = items[0]

        if not pick:
            unmatched.append({
                "artist": candidate.artist,
                "track": candidate.track,
                "score": candidate.score,
            })
            continue

        if pick["uri"] in uris:
            continue

        uris.append(pick["uri"])
        matched.append({
            "artist": candidate.artist,
            "track": candidate.track,
            "score": candidate.score,
            "spotify_name": pick.get("name"),
            "spotify_artists": ", ".join(a.get("name") for a in pick.get("artists", [])),
            "uri": pick.get("uri"),
            "url": pick.get("external_urls", {}).get("spotify"),
        })

    return matched, uris, unmatched


def maybe_create_playlist(
    name: str,
    description: str,
    uris: list[str],
    *,
    creds_path: str | None = None,
    token_path: str | None = None,
    public: bool = False,
) -> dict[str, Any]:
    token = get_access_token(creds_path=creds_path, token_path=token_path)
    playlist = create_playlist(name, access_token=token, public=public, description=description)
    add_tracks_to_playlist(playlist["id"], uris, access_token=token)
    return {
        "id": playlist.get("id"),
        "name": playlist.get("name"),
        "url": playlist.get("external_urls", {}).get("spotify"),
    }


def build_pipeline_output(
    *,
    mode: str,
    lastfm_creds_path: str | None,
    spotify_creds_path: str | None,
    spotify_token_path: str | None,
    user: str | None,
    artist: str | None,
    track: str | None,
    period: str,
    final_limit: int,
    market: str | None,
    autocorrect: int,
    output_mode: str,
    create_playlist_flag: bool,
    playlist_name: str | None,
    playlist_description: str | None,
    seed_count: int = 5,
    similar_per_seed: int = 10,
    recent_count: int = 10,
    artist_count: int = 5,
    seed_count_per_artist: int = 3,
    playlist_public: bool = False,
) -> dict[str, Any]:
    if output_mode == "lastfm-only" and create_playlist_flag:
        raise SystemExit("--create-playlist cannot be used with --output-mode lastfm-only.")

    lastfm_client = LastFMClient(explicit_path=lastfm_creds_path)
    creds = lastfm_client.load_credentials(lastfm_creds_path)
    username = user or creds.get("username")

    if mode == "artist-rule-c":
        if not artist:
            raise SystemExit("artist is required for artist-rule-c")
        seeds, ranked = build_from_artist_top_tracks(
            lastfm_client,
            artist=artist,
            seed_count=seed_count,
            similar_per_seed=similar_per_seed,
            autocorrect=autocorrect,
        )
        summary = {
            "mode": mode,
            "seed_artist": artist,
            "seed_tracks": [asdict(seed) for seed in seeds],
        }
        default_name = f"Last.fm Rule C - {artist}"
        default_description = f"Built from {artist} top tracks expanded through Last.fm similar tracks."
    elif mode == "seed-track":
        if not artist or not track:
            raise SystemExit("artist and track are required for seed-track")
        seeds, ranked = build_from_track_seed(
            lastfm_client,
            artist=artist,
            track=track,
            similar_per_seed=similar_per_seed,
            autocorrect=autocorrect,
        )
        summary = {
            "mode": mode,
            "seed_artist": artist,
            "seed_track": track,
            "seed_tracks": [asdict(seed) for seed in seeds],
        }
        default_name = f"Beep Beep - {artist} - {track}"
        default_description = f"Built from the Last.fm similar tracks graph for {artist} - {track}."
    elif mode == "recent-tracks":
        if not username:
            raise SystemExit("Missing Last.fm username. Pass --user or set LASTFM_USERNAME / credentials file username.")
        seeds, ranked = build_from_recent_tracks(
            lastfm_client,
            user=username,
            recent_count=recent_count,
            similar_per_seed=similar_per_seed,
            autocorrect=autocorrect,
        )
        summary = {
            "mode": mode,
            "user": username,
            "seed_tracks": [asdict(seed) for seed in seeds],
        }
        default_name = f"Last.fm Recent Blend - {username}"
        default_description = "Built from recent Last.fm scrobbles expanded through Last.fm similar tracks."
    elif mode == "top-artists-blend":
        if not username:
            raise SystemExit("Missing Last.fm username. Pass --user or set LASTFM_USERNAME / credentials file username.")
        seeds, ranked = build_from_top_artists(
            lastfm_client,
            user=username,
            period=period,
            artist_count=artist_count,
            seed_count_per_artist=seed_count_per_artist,
            similar_per_seed=similar_per_seed,
            autocorrect=autocorrect,
        )
        summary = {
            "mode": mode,
            "user": username,
            "period": period,
            "seed_tracks": [asdict(seed) for seed in seeds[:50]],
        }
        default_name = f"Last.fm Top Artists Blend - {username} - {period}"
        default_description = f"Built from top Last.fm artists for {period}, expanded through similar tracks."
    else:
        raise SystemExit(f"Unsupported mode: {mode}")

    candidates = ranked[: max(final_limit * 3, final_limit)]

    if output_mode == "lastfm-only":
        return {
            **summary,
            "output_mode": output_mode,
            "candidate_count_considered": len(candidates),
            "suggestion_count": min(len(ranked), final_limit),
            "suggestions": [candidate.to_dict() for candidate in ranked[:final_limit]],
        }

    access_token = get_access_token(creds_path=spotify_creds_path, token_path=spotify_token_path)
    matched, uris, unmatched = match_candidates_on_spotify(
        candidates,
        access_token=access_token,
        final_limit=final_limit,
        market=market,
    )
    output: dict[str, Any] = {
        **summary,
        "output_mode": output_mode,
        "candidate_count_considered": len(candidates),
        "matched_count": len(matched),
        "matched_tracks": matched,
        "unmatched_tracks": unmatched,
    }

    if create_playlist_flag:
        output["playlist"] = maybe_create_playlist(
            playlist_name or default_name,
            playlist_description or default_description,
            uris,
            creds_path=spotify_creds_path,
            token_path=spotify_token_path,
            public=playlist_public,
        )

    return output
