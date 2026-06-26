# lastfm-spotify-playlists (simple script layout)

This version is intentionally blunt and self-contained.

It does **not** require:
- `pip install -e .`
- a Python package layout
- `PYTHONPATH` hacks
- ACP agents

## Main commands

Recommend from recent Last.fm listening:

```bash
python run_pipeline.py recent-tracks --user "YOUR_LASTFM_USERNAME" --output-mode lastfm-only
```

Recommend from a seed artist:

```bash
python run_pipeline.py artist-rule-c "Massive Attack" --output-mode lastfm-only
```

Create a Spotify playlist:

```bash
python run_pipeline.py recent-tracks --user "YOUR_LASTFM_USERNAME" --create-playlist
```

Run Spotify OAuth first:

```bash
python auth.py
```
