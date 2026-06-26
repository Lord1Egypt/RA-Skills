from __future__ import annotations

import argparse

from common import dump_json
from pipeline import build_pipeline_output


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--final-limit", type=int, default=20)
    parser.add_argument("--market")
    parser.add_argument("--autocorrect", type=int, choices=[0, 1], default=1)
    parser.add_argument("--output-mode", choices=["spotify", "lastfm-only"], default="spotify")
    parser.add_argument("--create-playlist", action="store_true")
    parser.add_argument("--playlist-name")
    parser.add_argument("--playlist-description")
    parser.add_argument("--playlist-public", action="store_true")
    parser.add_argument("--creds", help="Path to Last.fm credentials JSON file.")
    parser.add_argument("--spotify-creds", help="Path to Spotify credentials JSON file.")
    parser.add_argument("--spotify-token", help="Path to Spotify token JSON file.")



def main() -> None:
    parser = argparse.ArgumentParser(description="Build Last.fm-driven Spotify playlists in one command.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    artist_parser = subparsers.add_parser("artist-rule-c", help="Use one artist's top tracks as Last.fm similar-track seeds.")
    artist_parser.add_argument("artist")
    artist_parser.add_argument("--seed-count", type=int, default=5)
    artist_parser.add_argument("--similar-per-seed", type=int, default=10)
    add_common_arguments(artist_parser)

    seed_track_parser = subparsers.add_parser("seed-track", help="Use one specific artist/track pair as the Last.fm similar-track seed.")
    seed_track_parser.add_argument("--artist", required=True)
    seed_track_parser.add_argument("--track", required=True)
    seed_track_parser.add_argument("--similar-per-seed", type=int, default=20)
    add_common_arguments(seed_track_parser)

    recent_parser = subparsers.add_parser("recent-tracks", help="Use recent scrobbles as track-level Last.fm seeds.")
    recent_parser.add_argument("--user")
    recent_parser.add_argument("--recent-count", type=int, default=10)
    recent_parser.add_argument("--similar-per-seed", type=int, default=5)
    add_common_arguments(recent_parser)

    top_parser = subparsers.add_parser("top-artists-blend", help="Use the user's top artists for a period, then blend Rule C candidates across them.")
    top_parser.add_argument("--user")
    top_parser.add_argument("--period", default="1month", choices=["7day", "1month", "3month", "6month", "12month", "overall"])
    top_parser.add_argument("--artist-count", type=int, default=5)
    top_parser.add_argument("--seed-count-per-artist", type=int, default=3)
    top_parser.add_argument("--similar-per-seed", type=int, default=5)
    add_common_arguments(top_parser)

    args = parser.parse_args()

    output = build_pipeline_output(
        mode=args.mode,
        lastfm_creds_path=args.creds,
        spotify_creds_path=args.spotify_creds,
        spotify_token_path=args.spotify_token,
        user=getattr(args, "user", None),
        artist=getattr(args, "artist", None),
        track=getattr(args, "track", None),
        period=getattr(args, "period", "1month"),
        final_limit=args.final_limit,
        market=args.market,
        autocorrect=args.autocorrect,
        output_mode=args.output_mode,
        create_playlist_flag=args.create_playlist,
        playlist_name=args.playlist_name,
        playlist_description=args.playlist_description,
        seed_count=getattr(args, "seed_count", 5),
        similar_per_seed=getattr(args, "similar_per_seed", 10),
        recent_count=getattr(args, "recent_count", 10),
        artist_count=getattr(args, "artist_count", 5),
        seed_count_per_artist=getattr(args, "seed_count_per_artist", 3),
        playlist_public=args.playlist_public,
    )
    dump_json(output)


if __name__ == "__main__":
    main()
