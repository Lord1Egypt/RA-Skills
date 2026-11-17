# ChatGPT configuration

- Name: HR Decision Packet
- Description: Turn messy people issues into evidence-backed HR decision briefs while keeping consequential decisions human-owned.
- Category: Productivity
- Builder: Mike Winkler
- Homepage: https://github.com/mwclaw/openclaw-hr-workflows/tree/main/skills/hr-decision-packet

## Conversation starters

- Turn this de-identified people issue into a decision-ready packet.
- Separate the facts, allegations, assumptions, and missing evidence in this case.
- Compare realistic options and show the affected-party tradeoffs.
- Test whether this HR packet is actually ready for a human decision.

## Optional knowledge files

The core instructions are self-contained. These canonical files may also be uploaded when the builder supports knowledge-file uploads:

- `templates/decision-packet.md`
- `references/evals.md`
- `examples/synthetic-input.md`
- `examples/synthetic-output.md`

## Capabilities

Leave web search, image generation, data analysis, apps, and actions disabled. This GPT prepares text packets from information the user supplies; it does not retrieve employee data or act in external systems.

## Current sharing boundary

The GPT was created and live-tested on 2026-08-16. The current ChatGPT publish dialog for the creator account offered private visibility only and stated that public GPT sharing was unavailable. The public, portable edition is therefore this source package until ChatGPT exposes an eligible public sharing option.
