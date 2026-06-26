# 🎧 Podcast-Intel: OpenClaw Skill

Convert passive podcast consumption into active knowledge capture. Transcribes, segments, summarizes, scores, and recommends podcast episodes with a "worth your time" signal before you commit to listening.

## Features

- **Hands-free operation**: Fetch episodes from configured RSS feeds automatically
- **Smart transcription**: Audio → text using OpenAI Whisper (with caching)
- **Topical segmentation**: Automatically identify and label distinct topics
- **Relevance scoring**: Episodes scored against your interests
- **Novelty detection**: Compare against consumption diary to avoid redundant content
- **Cross-source deduplication**: Identify overlapping coverage across shows
- **Local diary**: Append-only JSONL log of everything you've been briefed on
- **Multiple output formats**: JSON, Markdown, or TTS-ready text

## Installation

### 1. Copy skill to OpenClaw workspace

```bash
cp -r podcast-intel ~/.openclaw/workspace/skills/
cd ~/.openclaw/workspace/skills/podcast-intel
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install system dependencies

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Fedora
sudo dnf install ffmpeg
```

### 4. Set up environment

```bash
# Required: OpenAI API key
export OPENAI_API_KEY="sk-..."

# Optional: Custom Whisper model (default: whisper-1)
export WHISPER_MODEL="whisper-1"

# Optional: Use local whisper instead of API
export WHISPER_USE_LOCAL=false
```

### 5. Configure feeds and interests

```bash
# Copy example configs
cp config/feeds.example.yaml ~/.openclaw/config/podcast-intel-feeds.yaml
cp config/interests.example.yaml ~/.openclaw/config/podcast-intel-interests.yaml

# Edit with your subscriptions and interests
nano ~/.openclaw/config/podcast-intel-feeds.yaml
nano ~/.openclaw/config/podcast-intel-interests.yaml
```

## Quick Start

### Get podcast briefing

```bash
python3 scripts/main.py
```

Options:
- `--hours 24` — Only look at last 24 hours
- `--top 5` — Only show top 5 recommendations
- `--output markdown` — Markdown format (default)
- `--output json` — JSON format
- `--output tts` — TTS-optimized text
- `--dry-run` — Analyze but don't update diary

### Show consumption diary

```bash
python3 scripts/diary.py --show
```

### Analyze a single episode

```bash
python3 scripts/main.py --episode-url "https://example.com/episode.mp3"
```

## Configuration

### Feeds (feeds.yaml)

List your favorite podcasts:

```yaml
feeds:
  - name: "Huberman Lab"
    url: "https://feeds.megaphone.fm/hubermanlab"
    category: "health-science"
  - name: "Lex Fridman Podcast"
    url: "https://lexfridman.com/feed/podcast/"
    category: "tech-science"
```

Get RSS URLs from these podcast hosts:
- **Apple Podcasts**: Open in Podcast app, subscribe, copy RSS from show feed
- **Spotify**: Find RSS feed URL using https://www.podcastaddict.com/
- **Megaphone**: Use direct feed URL from show details

### Interests (interests.yaml)

Define what matters to you:

```yaml
interests:
  primary:  # 0.8-1.0 weight
    - "artificial intelligence"
    - "neuroscience"
  secondary:  # 0.5-0.7 weight
    - "health optimization"
    - "physics"
  casual:  # 0.2-0.4 weight
    - "history"
    - "philosophy"

anti_interests:  # Negative weight
  - "celebrity gossip"
  - "sports"

boost_keywords:  # Always boost these
  - "neural networks"
  - "energy efficiency"
```

## How It Works

### Pipeline Architecture

```
1. FETCH (fetch_feeds.py)
   RSS feeds → Episode metadata (title, URL, published date)

2. TRANSCRIBE (transcribe.py)
   Audio URL → Whisper API → Timestamped transcript
   (Cached to avoid re-transcription)

3. SEGMENT (segment.py)
   Transcript → Topic identification → Segment boundaries & labels
   (LLM-powered topical segmentation)

4. ANALYZE (analyze.py)
   Segments → Relevance score (vs. interests)
              Novelty score (vs. diary history)
              Information density
              Cross-episode deduplication

5. DIARY (diary.py)
   Analyses → JSONL diary entry + Markdown memory note
```

### Scoring Formula

**Worth Your Time (WYT)** = (Novel minutes / Total minutes) × Information density

For each segment:
- **Relevance** (0-1): How well does it match your interests?
- **Novelty** (0-1): How much new info vs. what's already in your diary?
- **Density** (0-1): Information per minute
- **Composite** = 0.3×relevance + 0.4×novelty + 0.3×density

Episodes are ranked by WYT score. Recommendations are:
- **LISTEN** (WYT > 70%): High-value content
- **CONSIDER** (WYT 40-70%): Mixed value, selective listening
- **SKIP** (WYT < 40%): Minimal new content

## Data & Privacy

- **All local**: Transcripts, diary, cache stored in `~/.openclaw/`
- **Diary is yours**: JSONL format, human-readable, append-only
- **No telemetry**: No external calls except RSS feeds, Whisper API, LLM API
- **Consumption tracked locally**: Personal knowledge graph seed

## Caching

Transcripts and segmentations are cached by episode ID:

```
~/.openclaw/cache/podcast-intel/
├── transcripts/         # Cached transcripts (episode_id.json)
├── segmentations/       # Cached segmentations (episode_id.json)
└── analyses/            # Cached analyses (episode_id.json)
```

To clear cache:
```bash
rm -rf ~/.openclaw/cache/podcast-intel/
```

## Cost Estimates

- **OpenAI Whisper API**: ~$0.006/min → ~$0.72 for a 2-hour episode
- **LLM segmentation/analysis**: ~$0.05-0.10 per episode (gpt-4o-mini)
- **Total per 10-episode briefing**: ~$8-10

Use `--recommend-only` flag to skip transcription and use cached data.

## Troubleshooting

### "No OPENAI_API_KEY set"
```bash
export OPENAI_API_KEY="sk-..."
```

### "ffmpeg not found"
Install ffmpeg for your OS (see Installation section)

### "Feed unreachable"
Check feed URL is valid:
```bash
curl -I https://example.com/feed.xml
```

### "Transcript too short"
Some feeds return summaries instead of full descriptions. Transcription requires actual audio files.

## Contributing

This is an open-source OpenClaw skill. Contributions welcome!

- Bug reports and feature requests: GitHub issues
- Code contributions: Fork, branch, PR
- Ideas for scoring algorithms: Discussions

## License

MIT License. See LICENSE file.

## References

- [OpenClaw Skills Documentation](https://openclaw.ai/docs/skills)
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [Podcast Standards (RSS 2.0)](https://www.rssboard.org/rss-spec)
