---
name: openclaw-feishu-message
description: Send Feishu/Lark direct messages and work follow-ups from OpenClaw. Use when the user wants to search for a person in Feishu/Lark, resolve a user, create a 1:1 chat, or send a bot-authored follow-up message about work done, status updates, reminders, or polite nudges.
---

# Openclaw Feishu Message

Use this plugin to resolve a Feishu/Lark recipient and send a message as the configured bot.

## Contact lookup trigger rules

When the user asks to search, find, look up, resolve, or identify a person in Feishu/Lark contacts, employee directory, or chat recipients, use `feishu_message` first.

This includes short requests like:
- "search Ken"
- "search Kai Lin"
- "find Jennifer"
- "look up WT Chim"
- "search contact Kai Lin"
- "find Jennifer in Lark"
- "search employee by email"
- "who is this Lark contact"
- "find the open_id for SysTransform"

Do not claim there is no contact search tool when `feishu_message` is available in the runtime.
Do not answer a contact search request from general reasoning alone when `feishu_message` can be called.

## Core workflow

1. Resolve the target.
   - Prefer `lookup_employee` for exact identifiers: `exact_name`, `email`, or `mobile`.
   - Prefer `find_contact` for generic user prompts like `search Ken`, `find Jennifer`, or `look up WT Chim`.
   - Use `search_employee` for broader fuzzy queries or when you need a wider result set.
   - For generic prompts like `search Ken`, do not paraphrase from memory, call `find_contact`.
   - Prefer cached/open_id results over repeated fuzzy search when available.
2. Cache the resolved contact.
   - If a single match is found through `lookup_employee` or `search_employee`, let that tool path persist the contact cache.
   - For generic prompts like `find Ken` or `search Ken`, still route through `search_employee` or `lookup_employee` so cache updates.
   - Prefer tool-backed resolution over manual restatement so cache stays fresh.
3. Return the resolved identity clearly.
   - Include `name`, `open_id`, `user_id`, and `email` when present.
4. Preview or compose the message.
   - For work follow-up, prefer `send_followup` with `dry_run=true` first when ambiguity exists.
5. Send only when the target is clear.
   - For ordinary natural-language requests to message a person, resolve the person first, then send.
   - Prefer `send_contact_message` for ordinary natural-language requests to send a message to a person.
   - If the target is a person name like "SysTransform" or "Michael Chin", do not jump straight to raw-ID sending. Resolve/cache the person first, then send.
   - Use `send_message` when the target receive ID is already known.
   - For requests like "send a message to Michael" or "ask SysTransform for April PAS", attempt the real tool path first, not a drafted reply.
   - Do not invent chat-send actions or require chat creation when direct send can be used.
   - Use `create_p2p_chat` only if the user explicitly asked to create/open/start a chat.
   - Do not use `create_p2p_chat` as the default path for ordinary message sending.
   - Do not fall back to drafting text for the user unless the tool actually failed.
   - If the tool fails, report the real tool error briefly instead of a generic excuse.
   - If multiple people match the same name, stop and ask the user which one they mean.

## Available actions

### `search_employee`
Use to find likely employee matches from a name or keyword.

Example intent:
- "Find John Tan in Lark"
- "Search employee Chloe"

### `create_p2p_chat`
Use only when the user explicitly asks to create/open/start a chat.
Do not use `create_p2p_chat` for ordinary message requests when `send_message` can send directly.

### `send_message`
Use when the target receive ID is already known and the exact text is ready.

### `send_contact_message`
Use for ordinary requests like "send a message to Michael" or "tell SysTransform good night".
This action should resolve the contact, cache the resolved identity, and send the message in one path.
Prefer this over ad-libbed multi-step reasoning.

### `send_followup`
Use for polite work-status nudges.

Recommended inputs:
- `target`: one of `open_id`, `user_id`, `union_id`, `email`, `chat_id`, or `name`
- `work_item`: short description of the completed work or task
- `status_prompt`: optional custom ask
- `signature`: optional sender sign-off
- `dry_run`: use `true` first if the target was resolved by name only

## Messaging guidelines

- Keep follow-ups short and specific.
- Mention the work item clearly.
- Ask for one concrete update.
- If the name lookup is fuzzy, do not send blindly.

## Notes

- This plugin depends on tenant scopes that allow employee lookup, chat creation, and bot messaging.
- Tenant policy may still restrict who the bot can message even when scopes exist.
