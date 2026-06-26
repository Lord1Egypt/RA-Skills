---
name: non-annoying-news
description: Create, configure, and render a source-grounded personal newspaper/news digest from URLs, bookmarks, X/Twitter bookmarks, browser reading lists/bookmarks, read-later apps, feeds, newsletters, web research, or pasted notes. Use for first-run onboarding, recurring digest setup, personal newspaper naming/design/cadence customization, source/signal configuration, magazine-style PDF/HTML issues, bookmark/news roundups, editorial QA, rendering, and release-quality layout proofing. On first setup, require a personalized onboarding interview before creating a config, cron, or personal issue.
---

# Non-Annoying News

Create a personal newspaper that explains what matters without clickbait, dashboard cards, vague link summaries, or filler boxes.

Package version: v0.2.1.

## Use modes

- **First-run setup:** user wants the skill installed/configured, recurring issues, source adapters, X/bookmark inputs, naming, cadence, cron, delivery, or design choices.
- **One-off issue:** user supplies URLs, notes, files, feeds, or a topic and asks for a digest now.
- **Recurring production:** user already has a completed local config/signals and wants the next issue rendered and delivered.
- **Demo issue:** user explicitly asks for a generic demo/sample, not a personalized newspaper.

## Required workflow

1. Load `references/editorial-standard.md` before selecting stories or writing an issue.
2. For first-run setup, missing/incomplete config, recurring setup, cron/schedule, or customization requests, load `references/onboarding.md`, `references/config-schema.md`, `references/source-adapters.md`, and `references/design-presets.md`.
3. Apply the **Personalization Gate** from `references/onboarding.md`: do not create a personal issue, recurring config, delivery automation, or cron job until the required onboarding choices are answered or explicitly confirmed by the user.
4. Before rendering or delivering a PDF/HTML issue, load `references/layout-and-render-qa.md`; load `references/design-presets.md` if any visual choice is involved.
5. Use elevated reasoning/Thinking when available (`xhigh` recommended) for onboarding synthesis, story selection, editorial proof-reading, and final QA.
6. Gather user-provided sources first. Then use configured signal sources only when credentials/tools already exist or the user provides exported data.
7. Treat bookmarks, reading-list entries, likes, saved items, and read-later queues as **signals of intent**, not automatically verified facts. Fetch/read linked content where possible and mark access limits.
8. Write every article so it is understandable without seeing the original source, bookmark, or thread.
9. Render HTML first, then PDF when possible. Create PNG previews/screenshots for every page and inspect them before delivery.
10. If PDF rendering is unavailable, deliver the HTML and state the missing renderer clearly. Do not fake a PDF.

## Personalization Gate

When a user asks to install, configure, “set this up”, create a recurring digest, or make their personal newspaper for the first time, the agent must start with onboarding questions. It may propose defaults, but it must not silently assume:

- newspaper title/subtitle/language;
- reader promise and intended use;
- topics and exclusions;
- source/signal mix, including whether to use X/Twitter bookmarks, browser reading lists/bookmarks, read-later apps, RSS/newsletters, web search, and pasted URLs;
- cadence/frequency and whether a cron/scheduled job should be created;
- delivery mode/channel and output format;
- design preset, density, page count, and image policy.

If the user wants speed, offer a concise suggested config and ask for confirmation/corrections before saving it or generating the first personalized issue. Never create a cron job, external delivery, or credentialed-source workflow without explicit approval.

Exception: if the user explicitly asks for a generic demo/sample, you may generate a clearly labeled demo issue with sample content. Do not present it as personalized.

## Non-negotiable output standard

- The issue must read like a compact newspaper or magazine, not a link dump.
- Each issue needs an editorial spine: why these stories belong together now.
- Every article must contain: concrete event/claim, mechanism or argument, relevance/consequence, source/evidence boundary.
- No internal process language inside the newspaper: no TODOs, queues, QA notes, placeholders, automation commentary, or excuses.
- No filler boxes to patch layout holes. Empty side columns and lower thirds are layout failures; fix text or layout and render again.
- Sources must be cited discreetly under articles or in a source note. Links are proof, not the content.

## Recommended files and scripts

- `references/onboarding.md`: first-run setup flow, required Personalization Gate, and user-facing questions.
- `references/config-schema.md`: local configuration shape and copyable starter config.
- `references/source-adapters.md`: portable source/signal options including X bookmarks and browser reading lists.
- `references/design-presets.md`: newspaper naming, visual presets, and personalization knobs.
- `assets/config.example.json`: starter config the agent may copy into a local project outside the public skill; it is intentionally incomplete until onboarding is done.
- `assets/newspaper-template/base.css`: print CSS with theme/density tokens.
- `assets/newspaper-template/issue-template.html`: minimal issue structure with balanced side rails.
- `scripts/check_config.py`: validate local config before a recurring run.
- `scripts/collect_sources.py`: normalize pasted URL/title/note lists into a source manifest.
- `scripts/render_issue.mjs`: render HTML to PDF and PNG previews with Playwright when available.
- `scripts/qa_text.py`: scan visible HTML/text for common editorial and privacy failures.

## Privacy and portability

This skill is deliberately generic. Do not include user-specific names, accounts, private topics, local paths, workspace memories, handles, credentials, or channel IDs in reusable skill files or generated public examples. Put user-specific settings in a local project config outside the skill.

## Delivery checklist

Before final answer:

- Confirm onboarding is complete or explicitly state this is only a generic demo/sample.
- Confirm PDF/HTML artifact path exists.
- Confirm previews/screenshots were inspected page by page.
- Confirm text QA and config validation passed when applicable.
- Attach with an absolute `MEDIA:` path when the channel supports attachments.
- Mention any source access limitations in the message, not as an excuse inside the issue.
- If a publish/send/schedule action beyond delivering a local artifact is requested, require explicit approval.
