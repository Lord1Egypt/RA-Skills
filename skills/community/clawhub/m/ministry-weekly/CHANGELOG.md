# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] — 2026-06-08

### Added
- **Privacy and Data Handling** section in SKILL.md describing assistant-mediated reads/writes against `ministry-data.json` and honest disclosure of the (opt-in, confirmation-gated) Telegram delivery instruction; adds an explicit no-congregant-PII rule (no named prayer requests, attendance, or giving records)
- **Permissions and Privacy** section in README.md so users see the scope (local file write, optional confirmation-gated Telegram delivery, social/email outputs as drafts only) and congregant privacy rules before installing

### Changed
- Narrowed the activation triggers in the `description` frontmatter to require an explicit weekly-content-production context (sermon brief, series management, specific output requests), with a "do NOT trigger" guardrail for casual church-related chat, theology discussions, and general scripture lookups
- Unquoted the `version` field in frontmatter (matches updated ClawHub CLI semver requirements)

## [1.1.0] — 2026-05-12

### Added
- **Church Profile** (one-time setup): captures church name, tradition, audience, voice preferences, service times, social handles, and delivery channels, then auto-applies to every weekly brief
- **Sermon Series Threading**: recognizes when a brief is part of an active series, carries context forward week to week with optional callbacks, and maintains a current-week pointer
- **Series Recap** generation on demand: produces "where we've been, where we are, where we're going" summaries for catch-up emails and mid-series posts
- **Scripture Context Block**: 4-6 sentence factual context with 1-2 cross-references and an optional discussion question; included in the weekly output and available standalone
- **Platform-Specific Social Posts**: separate, optimized posts for Facebook (3 posts), Instagram (caption + story prompts), X (thread + quote tweet), Threads (mini-thread), and a community/members group post; replaces the previous "three posts that work on Facebook or Instagram"
- **Image Generation Prompts**: ready-to-use prompts for AI image tools covering sermon slide, IG square, vertical story, and optional scripture quote graphic; anchored to the active series' `graphicsTheme` for visual consistency
- **Optional Liturgy Block** in the bulletin for traditions that use one (anglican, lutheran, mainline)
- **Telegram Delivery Hook**: format and send the full package to a configured Telegram channel after generation
- **Data Persistence**: `ministry-data.json` stores church profile, sermon series, and weekly brief history across sessions
- **Optional email segments**: youth/family note, volunteer prompt, prayer request invitation

### Changed
- Frontmatter `version` field now quoted as a string per ClawHub CLI requirements
- Description expanded substantially with new triggers for series, graphics, scripture prep, and Telegram delivery
- Output Format section expanded to reflect the new sections and per-platform breakdowns
- Tone and Voice section now defers to the church profile's `voicePreferences` and `tradition` instead of always defaulting to general-Protestant

### Notes
- The one-message-in promise is preserved: a basic Sunday brief still produces a full content package without lengthy back-and-forth. The new layers (scripture context, series threading, image prompts, Telegram delivery) layer on top without slowing the basic flow.
- All persistence is opt-in. Drafts are not auto-saved; the user must explicitly say "save this brief" or "log this week" to write to the JSON file.

## [1.0.0] — 2026-03-20

### Added
- Initial release
- Bulletin draft generation from a one-message Sunday briefing
- Three social media posts (mid-week hype, day-of reminder, post-service reflection)
- Weekly email announcement with subject line
- Em-dash avoidance rule baked into Tone and Voice
- Reasonable-assumption-and-flag behavior so the skill doesn't pepper the user with questions
