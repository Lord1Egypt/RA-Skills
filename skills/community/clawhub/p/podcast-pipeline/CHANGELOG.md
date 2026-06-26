# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] — 2026-05-12

### Added
- **Chapter / timestamp generation** in Mode 2: real chapter markers derived from transcript topic shifts, with estimated timestamps and specific curiosity-inducing chapter titles (6-12 chapters per episode)
- **Social clip suggestions** in Mode 2: 3-5 clip-worthy moments identified from the transcript with hooks, payoffs, suggested captions, and estimated locations
- **Platform-specific social posts** in Modes 2 and 3: separately optimized posts for X (thread + quote), LinkedIn (long-form), Instagram (caption with clip suggestion), Facebook (story-driven), and Threads (mini-thread); replaces the previous generic "three posts that work everywhere"
- **Hook variants (A/B/C)** in Mode 3: three opening-line options (story hook, question hook, stake hook) for testing
- **Title rationale** in Mode 3: each of the five title options now ships with a one-line note on strategic intent (SEO, CTR, share-bait, etc.) plus a recommendation based on the user's platform mix
- **Backup question bank** in Mode 1: 8-10 safety-net questions (reset, story, provocation, audience-pulling) for when conversations stall
- **Conversation map** in Mode 1: optional one-screen flow with time allocations per question section
- **Evergreen tagging** in Mode 3 for re-promotion decisions later
- **Cross-mode episode tracking** via a new `podcast-data.json` data file with podcasts, episodes, sponsors, and seasons
- **Sponsor / ad placement tracking** with campaign windows and per-episode placement records
- **Season / series management** with theme, planned episode count, and progress views
- **Quick lookups** across episode history ("what episodes have I done with [guest]?", "what's tagged evergreen?", "how many episodes left in Season 2?")

### Changed
- Frontmatter `version` field now quoted as a string per ClawHub CLI requirements
- Description expanded substantially with new triggers for chapters, clips, sponsor tracking, evergreen, and season management
- YouTube description in Mode 2 now references chapters from the new Chapter Generation output instead of producing its own placeholder timestamps
- "Social Media Posts" sections in both Mode 2 and Mode 3 split from a single generic block into per-platform deliverables

### Notes
- The Data Persistence section is new for this skill; previous versions had no persistent state. Drafts produced in any mode are NOT auto-saved — the user must explicitly say "log this episode" to write to the JSON file. This preserves the lightweight feel for one-off use while enabling history for users who want it.

## [1.0.0] — 2026-04-12

### Added
- Initial release
- Three production modes detected automatically from context: Interview Prep (pre-recording), Post-Recording (transcript to show notes), and Solo Episode Planning
- Mode 1: guest research brief, 15-20 question interview set organized by section, guest prep email
- Mode 2: structured show notes (400-600 words), three social media posts, YouTube description with placeholder timestamps
- Mode 3: five title options, episode outline, pre-recording show notes, social media posts
- Em-dash avoidance rule baked into General Guidelines
