# Podcast Production Pipeline

An OpenClaw skill that handles the most tedious parts of podcast production: before the mic turns on, after the recording stops, and across episodes over time.

**Current version: 1.1.0**

## What's new in 1.1.0

- **Real chapter/timestamp generation** from transcripts (not just placeholders) — identifies topic shifts and produces YouTube-ready chapter markers
- **Social clip suggestions** for short-form video — surfaces the 60-90 second moments worth clipping for Reels, Shorts, and TikTok
- **Platform-specific social posts** — separate, optimized posts for X (thread), LinkedIn (long-form), Instagram (caption + clip suggestion), Facebook, and Threads, instead of a single generic blast
- **Hook A/B/C variants** for solo episodes — three opening-line options (story, question, stake) to test against
- **Title rationale** — every title option comes with a one-line "best for X" note so you can pick by strategic intent
- **Backup question bank** for interviews — 8-10 safety-net questions for when conversations stall or run short
- **Cross-mode episode tracking** — lightweight `podcast-data.json` for episode history, sponsor placements, and season management
- **Sponsor / ad placement tracking** with campaign windows and per-episode placement records
- **Evergreen tagging** so you know which episodes to re-promote later

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

## What It Does

Drop in your guest's name, paste a transcript, or describe a solo episode topic. The skill detects what you need and produces ready-to-use content without a lengthy back-and-forth.

It operates in three modes plus a cross-mode tracking layer.

**Mode 1: Interview Prep (Pre-Recording)**
Give it a guest name and topic. Returns a guest research brief, a 15-20 question interview set organized by section, a backup question bank for safety, a conversation map with time allocations, and a guest prep email you can send directly.

**Mode 2: Post-Recording (Transcript to Show Notes)**
Paste your raw transcript. Produces structured show notes (400-600 words), real chapter/timestamp markers, 3-5 social clip suggestions with hooks and captions, platform-specific social posts for X/LinkedIn/Instagram/Facebook/Threads, and a YouTube description with the chapters embedded.

**Mode 3: Solo Episode Planning**
Give it a topic and any key points you want to hit. Returns five title options *with strategic rationale*, three hook variants (story/question/stake), a full recording outline, pre-recording show notes, evergreen-vs-timely tagging, and platform-specific social posts.

**Cross-mode: Episode History & Sponsor Tracking**
Log episodes to a persistent `podcast-data.json` for searchable history, sponsor campaign tracking with placement records, and season/series management with progress views.

## How to Trigger It

The skill detects mode from context automatically. Examples:

- "I have a guest coming on Thursday — her name is Sarah Chen..."
- "Just finished recording. Here's the transcript: ..."
- "I want to record a solo episode about why most small businesses ignore email lists."
- "Generate chapters from this transcript."
- "Find the clip-worthy moments in this episode."
- "Log this episode under Season 2."
- "Which episodes did I do with [guest]?"

It also responds to casual phrasing: "I need show notes," "Can you prep me for my interview," "I have a guest this week."

## Installation

1. In your OpenClaw workspace, navigate to `.openclaw/workspace/skills/`
2. Create a folder named `podcast-pipeline`
3. Copy `SKILL.md` into that folder
4. Restart OpenClaw or reload skills

The `podcast-data.json` file is created automatically the first time you log an episode or sponsor.

## Notes

- The skill works best when given a guest name and some context. It will make reasonable assumptions if details are missing and flag them at the end of the output.
- If your OpenClaw instance has web access enabled, Interview Prep mode will search for current information on the guest. If not, it works from what you provide.
- Chapter timestamps are estimates derived from transcript pacing; verify against the actual recording before publishing.
- All outputs are clearly labeled and formatted so you can copy each section directly.

## Skill Metadata

| Field | Value |
|---|---|
| Name | podcast-pipeline |
| Version | 1.1.0 |
| Author | Chris (zocase) |
| Compatible with | OpenClaw |
| Category | Content Production |
| Modes | Interview Prep, Post-Recording, Solo Episode, Cross-Mode Tracking |
