# Podcast Highlights Deck

Create a premium editorial long-scroll highlight deck from a podcast episode, with:

- 8-12 curated highlights (not full transcript)
- per-highlight playable original audio clips
- global multilingual toggle (such as `en`, `ja`, `zh`)
- sticky left rail for metadata and table of contents

## Author

- GitHub: [@RamseyChen1997](https://github.com/RamseyChen1997)

## Skill Files

- `SKILL.md`: full agent workflow and operating instructions
- `scripts/clip_audio.py`: clip generation for highlight segments
- `assets/template/`: Vite template assets (`Home.tsx`, `index.css`, `index.html`)

## Typical Input

- Episode URL (Apple Podcasts, Spotify, RSS feed, direct MP3, or YouTube)
- Target language codes (for example: `en`, `ja`, `zh`)

## Output

- A bundled static site with translated UI/content and playable clips per highlight
