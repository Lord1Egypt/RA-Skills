# Research, script, scenes and packaging

## 1. Research and outline

- Collect 5 to 15 facts with links before writing. Use WebSearch/WebFetch; note what is verified and what is the author's opinion.
- Decide the angle: a claim, comparison, myth-busting, timeline with a thesis, or "what changed and why". Write it in one sentence.
- Check what already ranks for the topic (titles, lengths, gaps). If `viral-content-research` or `content-strategy` exist, use them for the evidence.
- Outline 4 to 8 chapters for 10 to 20 minutes. Each chapter has one question it answers.

## 2. Script rules for long form

- Open with the most interesting concrete thing in the first 15 seconds; no "welcome back" preamble.
- Plant a reason to stay every 60 to 90 seconds: an unanswered question, a contrast, a reveal, a number.
- Write for the ear: short sentences, active verbs, no lists of more than three items. Read it aloud.
- 150 words per minute is the default pace (`wpm` in `project.json`; 130 for careful narration, 165 for energetic). A 10-minute video is about 1500 words, 20 minutes about 3000.
- Vary scene openings and structure. Repeating one pattern in every scene reads as templated.
- Do not add claims the research does not support. Mark opinions as opinions.
- End with the takeaway and one specific next step or question, not a generic "like and subscribe".

## 3. Splitting into scenes

- One idea per scene, 40 to 160 words (15 to 60 seconds). A scene is the unit for audio, search and caching.
- Visual keywords: 2 to 3 per scene, concrete and filmable, ordered from most to least important. Add the place, object or action, not the emotion.
- `chapter` marks where a chapter starts (the first scene of it). Chapters need to start at 0:00, be at least 10 seconds long, and there must be at least three.
- Plan shot length: about 5 to 8 seconds per shot (`shot_seconds`). A 45-second scene wants 6 to 8 shots; if the search cannot supply them, shorten the scene, add images (slow zoom) or the user's own footage.

## 4. `project.json`

```json
{
  "title": "Working title",
  "language": "en",
  "target_minutes": 12,
  "topic_category": "general",
  "angle": "One sentence: what this video adds.",
  "sources": ["https://..."],
  "fps": 30,
  "resolution": "1920x1080",
  "wpm": 150,
  "shot_seconds": 6,
  "voice": {"engine": "piper", "voice": "en_US-lessac-medium", "pad": 0.4},
  "music": {"file": "assets/music.mp3", "volume": 0.15, "duck": true, "license": "", "attribution_text": ""},
  "sfx": [{"file": "assets/whoosh.wav", "scene": "s03", "offset": 0.5, "volume": 0.8}],
  "review": {"human_checked": false, "notes": ""},
  "youtube": {"title": "", "description": "", "tags": [], "disclosure": ""},
  "scenes": [
    {"id": "s01", "chapter": "Intro", "narration": "...", "keywords": ["harbor", "fishing boat"],
     "on_screen_text": "Optional short text shown at the start of the scene"}
  ]
}
```

Fields the scripts add: `candidates`, `media`, `audio_file`, `audio_duration`, `audio_hash` per scene. `fps` must be 24, 25, 30, 50 or 60. `sfx` entries use `at` (seconds from the start) or `scene` plus `offset`. Scene ids use letters, digits, `-` and `_`.

## 5. YouTube package

**Title.** Under 70 characters so it is not cut off (hard limit 100). Put the specific subject first, add one reason to click (a number, contrast or question), and keep it true. Offer three options with different angles and say which is recommended and why. Do not copy a competitor's title.

**Description.** First two lines carry the promise and keywords, since they show before "more". Then chapters (generated), sources (the facts' links), credits (generated), and the synthetic-voice line if used. No `<` or `>`. Limit 5000 bytes. `package_youtube.py credits` assembles it into `out/description.txt` and reports issues.

**Tags.** Few and specific; they matter little. Total under 500 characters.

**Thumbnail.** 1280x720 JPG or PNG under 2 MB. One focal point, 1 to 4 words of large text, high contrast, readable at phone size, no misleading promise. `package_youtube.py thumbnail DIR --text "..." [--source FILE]` makes a base from a frame or image; offer two concepts (for example subject close-up vs. before/after) and let the user pick, or finish it in their own design tool.

**Chapters.** Generated from `chapter` fields into `out/chapters.txt`; paste them at the top of the description block.

**Upload settings to review in Studio:** captions (upload `out/subtitles.srt`), altered/synthetic-content question, category, end screen, and monetization eligibility for the channel as a whole.
