---
name: podcast-to-script
description: >
  Turn a podcast episode link into a timestamped transcript AND a production-ready
  Chinese two-host script package (outline.md, script.md, notes.md) that faithfully
  translates/restores the original episode and passes the bundled format checker —
  self-contained, no external pipeline dependency. Use when the user pastes a podcast
  URL (open.spotify.com/episode/..., podcasts.apple.com/..., an RSS feed URL, or a
  direct audio link) and asks for 字幕/转录/transcript/文字稿/逐字稿, wants
  把播客转成文字 or 转成播客脚本, translate an episode into a 双人对谈中文脚本
  (翻译还原原播客), or batch-process episodes. Staged & resumable: preflight →
  fetch → outline → draft → notes, each stage gated by a script. No Spotify/Apple
  API key: metadata via oEmbed/iTunes, official <podcast:transcript> when available,
  otherwise public RSS audio + faster-whisper. SKIP: YouTube/video captions, music
  tracks, Spotify-exclusive shows with no public RSS feed (script reports this).
license: MIT-0
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎧"
    requires:
      bins: ["python3"]
    install:
      - kind: uv
        package: faster-whisper
        label: "faster-whisper (local ASR, pip install faster-whisper)"
---

# Podcast link → transcript / production script package

## The big picture

```
Skill layout                       Data flow
podcast-to-script/
  SKILL.md                         podcast episode link (Spotify / Apple / RSS / --audio)
  scripts/                           │  0 pipeline.py preflight  →  status (find resume point)
    transcribe.py                    ▼
    pipeline.py                    A transcribe.py: fetch + ASR (chunks cached, --workers)
    check_script.py                  ▼
  references/                      $TMPDIR/podcast-to-script/<slug>/   ← episode dir = ALL state
    script-spec.md                   raw.mp3  script.txt  script.srt/vtt  images/  chunks/
    notes-spec.md                    │  B1 agent: outline.md → verify-outline
  tests/                             │  B2 agent: script.md  → verify-script (per-segment resume)
    run_tests.py                     │  C  agent: notes.md   → verify-notes (draft-timeline)
                                     ▼
                                   episode package: raw audio + transcript + outline + script + notes
                                   script.md + notes.md → podcast production pipeline (generate_podcast.py)

Deterministic work is scripted; the agent only does semantic writing (outline /
draft / notes) and runs scripts. Every gate exits 0/1; an interrupted run
resumes at the first stage status does not mark OK.
```

## Resume protocol (do this first)

```bash
python3 scripts/pipeline.py preflight            # env & deps OK? fix what FAILs
python3 scripts/pipeline.py status --dir "<episode_dir>"   # or omit --dir to scan all
```

Continue from the first stage NOT marked OK. Never redo a stage whose gate
already passed (transcript chunks are cached; re-runs are cheap and safe).

**First run ever** (installs deps + warms the ASR model cache):

```bash
python3 scripts/pipeline.py preflight --install
```

## Stage A — Fetch transcript (script)

```bash
python3 scripts/transcribe.py "<episode_url>"        # ends with: [dir] <episode_dir>
```

Inputs: Spotify episode URL · Apple Podcasts URL · bare RSS feed (`--title`
picks the episode) · `--audio <url>` direct file. Options: `--model small
--lang zh` for non-English (default `small.en`); `--workers N` parallel chunk
transcription (default 4; 1-2 for medium/large models); `--proxy`; smoke test
`--max-seconds 180`. Performance: `small.en` ≈ 9x realtime × workers on Apple
Silicon.

Gate (script): `status` shows `A fetch OK` — episode dir has `raw.mp3` (always
kept; `raw{ext}` if not mp3) and non-empty `script.txt` with char/duration
stats. Official `<podcast:transcript>` is auto-converted to `script.txt`;
episode images (`itunes:image` + `<img>` in the description) land in `images/`
with `manifest.json` (filename → source URL). Limits: no public RSS = clear
error; no speaker diarization (single stream).

## Stage B1 — Outline (agent writes, script gates)

Read `script.txt`, write `<episode_dir>/outline.md`: episode title line
(`# {English} -- {中文副标题}`) + one segment header per topic
(`## 第 N 段 · 子标题`, same format as script.md) with 3-5 bullet points under
each naming the concepts/cases/numbers that segment MUST cover. Follow the
original episode's own content flow — the outline is the fidelity audit
trail: every part of the source maps to a segment, nothing dropped.

Gate (script): `python3 scripts/pipeline.py verify-outline --dir <episode_dir>`

## Stage B2 — Draft script.md (agent writes, script gates)

Read `references/script-spec.md` FIRST (full contract: format + quality bar +
旁白 guidelines). Write `<episode_dir>/script.md` segment by segment, per
outline.md. Hard rules (checker-enforced):

- Title `# {English title} -- {中文副标题}`; optional `> TTS 制作备注：…` quote
- Segments `## 第 N 段 · 子标题` matching outline.md
- Speaker whitelist ONLY: `**主持人**:` / `**嘉宾**:` / `**旁白**:`
- 旁白: segment head only, ≤ 4/episode, each ends exactly `好，回到对话。`
- Fixed closing: `## **主持人**：感谢收听，完整原文列表在 show notes 里。我们下期见`
- No URLs in any dialogue turn

Quality bar — **translate-and-restore first**: the script re-presents the
ORIGINAL episode's content in Chinese, faithfully covering every argument,
example and number — this is a translation of the source show, not new
commentary. 主持人/嘉宾 is only the delivery vehicle: host follow-ups exist to
draw out content the original already contains; never invent viewpoints or
drop arguments. Two-host deep-dive form (open `欢迎收听本期节目`, no
interview framing); conversational Chinese with English tech terms kept;
Chinese punctuation (TTS prosody); follow-ups split into separate turns;
transcript has no speaker labels — map the original speakers' exchange onto
主持人/嘉宾 naturally. ≈260 Chinese chars/min for duration.

Gate (script): `python3 scripts/pipeline.py verify-script --dir <episode_dir>`
— also reports which outline segments are still missing, so an interrupted
draft resumes per segment. Fix and re-run until exit 0.

## Stage C — notes.md (agent writes, script gates)

Read `references/notes-spec.md`. Write `<episode_dir>/notes.md`: hook line
(`本期…。一句话主线：…`), **内容速览** bullets, **时间轴**, **原文链接**
(source URLs live here, never in dialogue). Draft the timeline with:

```bash
python3 scripts/pipeline.py draft-timeline --dir <episode_dir>
```

Images: if `images/` is non-empty, reference them in notes.md with Markdown
image syntax (after the hook line / near the related bullet, per
notes-spec.md). Keep the local filenames from `images/` exactly — the publish
step matches TOS paths by filename.

Gate (script): `python3 scripts/pipeline.py verify-notes --dir <episode_dir>`

## Deliverable

`<episode_dir>/` with raw audio, transcript, images/, outline.md, script.md,
notes.md — all gates green. script.md/notes.md are directly consumable by the
podcast production pipeline (`generate_podcast.py --script … --notes …`);
keep them together in the episode dir.

## Tests

`python3 tests/run_tests.py` — stdlib-only; run after ANY change to
scripts/ or SKILL.md. Covers checker rules, stage-gate transitions, layout
end-to-end via file:// fixtures; downstream-parity and real-ASR cases
auto-skip when their prerequisites are missing.
