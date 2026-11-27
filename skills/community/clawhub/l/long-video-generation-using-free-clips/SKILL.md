---
name: long-video-generation-using-free-clips
description: Plan, script and render 5 to 30+ minute YouTube videos from free stock footage (Pexels, Pixabay, Mixkit, Wikimedia Commons, Internet Archive, Unsplash), AI or own voiceover (Piper, ElevenLabs, Whisper subtitles) and automated FFmpeg editing, with per-clip licence tracking and YouTube originality checks. Use this skill whenever the user wants a long-form or faceless video made from stock clips, a video from a script or topic with voiceover and subtitles, automatic scene-by-scene editing, 1080p rendering, or a YouTube title, description, chapters and thumbnail for such a video, even if they just say "make a long video", "video from free clips", or "faceless YouTube video".
---

# Long-form video from free clips

Turns a topic into a finished 1080p video: research and outline, script, scenes, footage search, voiceover, edit, subtitles, music, title, description, chapters and thumbnail. The scripts are standard-library Python plus FFmpeg. Replies to the user follow their language preference; file contents and commands stay in English.

## Read this first: the real risk

YouTube demonetizes channels whose uploads are mass-produced, repetitive or template-like ("inauthentic content") and compilations without meaningful commentary or change ("reused content"). Stock clips plus a synthetic voice and no original angle is exactly that pattern, and the policy applies to the whole channel. So this skill automates the labour (searching, downloading, syncing, rendering) but not the value. Every project needs an original angle, real research and sources, and a human watching the whole video before upload. Say this plainly to the user at the start, in one or two sentences, and do not promise that a fully automatic video will earn money. Details and gates: `references/youtube-policy-and-originality.md`.

## Workflow

Create a project folder and keep everything in `project.json` (schema in `references/scripting-and-packaging.md`).

1. **Intake.** Topic, audience, language, length, voice choice (Piper free, ElevenLabs, or the user's own recording), available API keys, music file. Ask only for what is missing. If the topic is health, legal, finance, politics or news, read the sensitive-topic rules in the policy reference before going on.
2. **Research and outline.** Use WebSearch/WebFetch (and `viral-content-research` or `content-strategy` if present) to collect facts with links. Write the one-sentence `angle` (what this video says that others do not) and `sources`. Outline in chapters. Never invent facts, numbers or quotes.
3. **Script.** Write narration for the spoken word, about 150 words per minute, one idea per scene, 40 to 160 words per scene. Vary structure; open with the payoff, not a greeting.
4. **Scenes.** Fill `scenes` in `project.json` with `id`, `chapter`, `narration`, 2 to 3 concrete `keywords` (nouns, not abstractions), optional `on_screen_text`.
5. **Check the plan.** `python scripts/project.py validate DIR` and `estimate DIR`. Fix warnings that are real.
6. **Voiceover.** `python scripts/voiceover.py DIR`. Gives exact per-scene durations, which drive everything else.
7. **Find footage.** `python scripts/stock_search.py DIR` (Pexels and Pixabay by default; keys in env vars). Results are ranked by how well each result's own tags match the keyword (`relevance`, 0 to 1) before resolution or video vs photo; the output says how many kept candidates are on-topic. If a scene has few on-topic results, use plainer nouns or `--kinds image` for that scene (`--scene ID`). Then `python scripts/fetch_clips.py pick DIR`, which skips weak matches (relevance under 0.3) unless `--allow-offtopic`. Mixkit has no API in the sources checked: tell the user to download by hand and register files with `fetch_clips.py add-local`. Commons, Internet Archive and Unsplash results need a per-file licence check before use.
8. **Review every shot, then draft.** `python scripts/fetch_clips.py review DIR` writes `build/review.html` with one frame per shot next to its narration: look at all of them (tags still mislead, and logos or identifiable people slip in). Remove wrong ones with `fetch_clips.py reject DIR SCENE ID` and top up with `pick DIR --scene SCENE --fill`; replace a whole scene with `pick DIR --scene SCENE --redo`. Then `python scripts/build_video.py DIR --draft` (640x360, fast), watch it, repeat.
9. **Subtitles.** `python scripts/subtitles.py DIR` (timings from the script) or `--mode whisper` for real word timings with faster-whisper. Proofread.
10. **Final render.** `python scripts/build_video.py DIR` writes `out/video.mp4` at 1080p, with music ducked under the voice and loudness normalized. Add `--burn-subs` only if the user wants hard-coded captions; otherwise upload the SRT.
11. **Packaging.** Fill `youtube` in `project.json` (title, description, tags, disclosure), then `python scripts/package_youtube.py credits DIR` and `thumbnail DIR --text "..."`. Offer 3 title options and 2 thumbnail concepts with reasons.
12. **Human review.** The user watches the whole video, checks facts and licences, then sets `review.human_checked` to true. Do not call the video ready before this.

Each step can be rerun: audio, shots and scenes are cached, so fixing one scene re-renders only that scene.

## Commands

```bash
python scripts/project.py init DIR --title "..." --minutes 12
python scripts/project.py validate DIR [--strict] | estimate DIR | status DIR
python scripts/voiceover.py DIR [--engine piper|elevenlabs|own|silent] [--scene ID] [--force] [--dry-run]
python scripts/stock_search.py DIR [--sources pexels,pixabay,commons] [--kinds video,image] [--max-requests 120]
python scripts/fetch_clips.py pick DIR [--prefer video|image|mixed] [--scene IDS] [--redo | --fill] [--allow-offtopic] [--dry-run]
python scripts/fetch_clips.py review DIR | reject DIR SCENE ID [ID ...] | add-local DIR SCENE FILE --license "..." --confirmed | list DIR
python scripts/subtitles.py DIR [--mode script|whisper]
python scripts/build_video.py DIR [--draft] [--only s01,s02] [--burn-subs] [--transition fade,dissolve] [--no-text]
python scripts/package_youtube.py credits DIR | thumbnail DIR --text "THREE WORDS" [--source FILE]
```

Keys come from environment variables only: `PEXELS_API_KEY`, `PIXABAY_API_KEY`, `UNSPLASH_ACCESS_KEY` (opt-in), `ELEVENLABS_API_KEY`. Never write a key into a file, a log or the chat.

## Rules that keep the output honest and safe

- Respect the sources' API terms: rate limits, caching, no bulk downloading, show the source. Download only the files that were chosen. See `references/sources-and-licenses.md`.
- Every file used is recorded with source, creator, page URL and licence in `project.json`; `credits` turns that into the description credits. Anything not marked `license_status: ok` blocks publishing until checked.
- Do not stitch unrelated clips behind the narration just to fill time; each shot should show something the sentence is about. Prefer fewer, better-matched shots, add maps, charts, diagrams or the user's own footage where stock is generic.
- Do not present a synthetic voice or avatar as a real person or expert. Follow the platform's "altered or synthetic content" disclosure rules; the user decides, Claude flags it.
- Do not use footage of identifiable people in a way that implies endorsement or misleads, and do not download photos of public figures from the web into the video.
- If a step fails because the sandbox blocks the network, say so and give the exact command for the user's own machine; never fake search results or downloads.
- Report only what was verified. The scripts were tested with local test media and mocked API responses, not live APIs; if a live call fails, show the error and adjust, do not guess.

## References

- `references/youtube-policy-and-originality.md`: what YouTube's rules target, originality gates, sensitive topics, disclosure.
- `references/sources-and-licenses.md`: per-source terms, limits, confidence level, attribution text.
- `references/scripting-and-packaging.md`: research, outline, script rules, scene splitting, `project.json` schema, titles, description, chapters, thumbnail.
- `references/voiceover.md`: Piper, ElevenLabs, own recording, Whisper, pacing and pronunciation.
- `references/editing-and-render.md`: how timing, transitions, Ken Burns, music ducking and loudness work, tuning, troubleshooting, and why FFmpeg is used instead of MoviePy.
