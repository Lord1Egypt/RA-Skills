---
name: prompt-buttons
version: 1.0.2
description: A comprehensive helper skill that wraps agent prompts with short, consistent tappable button menus (Yes/No, single digits, or small option sets) so users can interact via Telegram inline buttons or fall back gracefully to numbered lists on channels without button support.
author: jin
license: MIT
tags: [ux, buttons, prompts, telegram, interaction]
---

# prompt-buttons

Purpose
- Standardize how agents present choice-driven prompts so users can respond with one tap.
- Prefer true Telegram inline buttons when channel supports them; otherwise render a compact numbered list as fallback.
- Enforce short labels and one-line option descriptions so menus remain scannable on mobile.

Design rules (enforced by the skill)
- Button label length: 1–3 characters preferred; allow up to 10 chars only when necessary. Examples: `Yes`, `No`, `1`, `2`, `A`.
- Option descriptions: one sentence / one short clause. Keep each option on a single line.
- Message header: single-line title (question or short instruction).
- Always include buttons metadata in the outgoing message payload. Do not rely on free-text only.
- For menus >6 items, prefer paginated menus (ask user to choose a page) or hierarchical choices (1–3 then deeper options).
- Log the user’s last button-style preference in memory (scope: agent:main) to persist UX.

Capabilities
- Build Yes/No prompts with canonical callback payloads.
- Build numbered menus (1–9) with mapped callback actions.
- Render channel-appropriate fallback text when inline buttons are unavailable.
- Validate button payloads before sending (short labels, callback_data present).
- Optionally include metadata in callback_data (compact JSON base64) for routing back to the calling skill.

API / Integration
- Other skills call `prompt-buttons` by sending a message via the `message` tool with `action=send` and a `buttons` array in the recommended format.

Recommended payload (Telegram inline buttons):
{
  "action": "send",
  "channel": "telegram",
  "message": "Title: Pick an option\n1 — Show top 10 entries\n2 — Triage noisy entries",
  "buttons": [[
    {"text":"1","callback_data":"{\"a\":\"show_top10\"}"},
    {"text":"2","callback_data":"{\"a\":\"triage\"}"}
  ]]
}

Notes on callback_data
- Keep callback_data compact (<=64 bytes recommended for safety across channels).
- When you need to send structured data, encode a short action key and state id (e.g., `{\"a\":\"triage\",\"id\":42}`), optionally base64-encode if required by the channel provider.
- The skill listening for button presses should expect callback_data and map the short action key back to handler functions.

Fallback rendering (channels without inline button support)
- Produce a numbered list in the message body identical to the button order.
- Example fallback body:
  "Pick an option:\n1 — Show top 10 entries\n2 — Triage noisy entries\nReply with the number to choose."

Implementation details (for skill authors)
- Use `message(action=send, channel=..., message=..., buttons=...)` to show the ask.
- Register a callback handler for the channel’s button callbacks (Telegram: listen for callback_query). The handler should:
  1. Parse callback_data.
  2. Acknowledge the callback (Telegram answerCallbackQuery) to remove the loading spinner.
  3. Dispatch to the appropriate internal handler (map action keys to functions).
- When dispatching long-running work from a button press, acknowledge immediately and spawn a background subagent for the task — return a brief confirmation message to the user.

Security & privacy
- Never include raw secrets or tokens in callback_data. Use short opaque identifiers that map to server-side state.
- When storing user preferences (e.g., prefers buttons vs typed replies), store only non-sensitive flags in memory with scope agent:main.

Examples
- Yes/No (implementation):
  message: "Run self-improving now?\nYes — Run and execute now.\nNo — Not now."
  buttons: [[{"text":"Y","callback_data":"{\"a\":\"self_imp_yes\"}"},{"text":"N","callback_data":"{\"a\":\"self_imp_no\"}"}]]

- Multi-step menu (page 1 of 2):
  message: "Pick what to do next (page 1):\n1 — Show top 10 entries\n2 — Triage entries\n3 — Propose promotions\n4 — Next page"
  buttons: [[{"text":"1","callback_data":"{\"a\":\"show_top10\"}"},{"text":"2","callback_data":"{\"a\":\"triage\"}"},{"text":"3","callback_data":"{\"a\":\"promote\"}"},{"text":"4","callback_data":"{\"a\":\"page2\"}"}]]

Developer notes
- Keep the skill code minimal: message builders + validation + callback dispatch map.
- Include unit tests that validate: button label length, callback_data structure, fallback body matches buttons order.
- Provide an example handler in index.js that demonstrates mapping compact action keys to functions and acknowledging Telegram callback queries.

Installation / discovery
- Place the skill under `/data/workspace/skills/prompt-buttons/` and ensure a discovery copy in `/data/workspace/skills/skills/prompt-buttons/` so OpenClaw discovers it.
- The skill entry in /data/.openclaw/openclaw.json should be enabled: `skills.entries.prompt-buttons.enabled = true`.

Compatibility
- Channels with native inline button support: Telegram (full), some webchat adapters (if configured).
- Channels without button support: gracefully fall back to numbered list; the calling skill must accept numeric replies.

Versioning & changelog
- v1.0.2 — Detailed SKILL.md, explicit Telegram inline button guidance, validation rules, and dev notes.

Contact
- Author: jin
- Repo / Local path: /data/workspace/skills/prompt-buttons/

