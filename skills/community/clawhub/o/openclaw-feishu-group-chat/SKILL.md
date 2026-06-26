---
name: openclaw-feishu-group-chat
description: Teach OpenClaw how to work in Feishu (Lark) group chats — recognize who's talking, behave properly in groups vs DMs, respect multi-user privacy, and format messages for the platform. Use when connecting OpenClaw to Feishu and you want your agent to be a competent group participant, not just a responder.
---

# OpenClaw Feishu Group Chat

Everything your OpenClaw agent needs to be a good Feishu group chat participant.

## 1. Know who you're talking to

Feishu group messages include sender names in metadata. DMs don't — they only include an opaque `open_id`. Without setup, your agent will assume all DMs come from one person.

**Fix**: Embed an `open_id → name` lookup table in USER.md. Since workspace files are injected into the system prompt, the agent matches senders instantly — no tool calls.

Run the bundled sync script to pull your org's contacts:

```bash
python3 scripts/sync_feishu_contacts.py <openclaw_config> <feishu_account> <user_md_path>
```

This populates a table in USER.md:

```markdown
## 飞书通讯录 (App Name)
飞书 DM 不携带发送者姓名。用 inbound metadata 的 chat_id（格式 `user:ou_xxx`）匹配下表识别发送者。
| 姓名 | open_id |
|------|---------|
| Alice | ou_abc123 |
| Bob | ou_def456 |
```

**Important**: Feishu `open_id` is per-app. Multiple OpenClaw instances using different Feishu apps must each pull contacts with their own credentials.

**After updating USER.md, restart the gateway.** Workspace files are cached at startup; `/new` alone won't pick up changes.

Set up weekly auto-sync via crontab:
```bash
0 7 * * 1 python3 /path/to/scripts/sync_feishu_contacts.py ~/.openclaw/openclaw.json my_app ~/workspace/USER.md
```

## 2. Group chat etiquette

Add to AGENTS.md or SOUL.md:

**When to respond:**
- Directly @mentioned
- Can add real value to the conversation
- Something witty or relevant fits naturally

**When to stay silent:**
- Casual banter you have nothing to add to
- Someone already answered well
- "Yeah" / "Nice" / emoji-only territory

**General rules:**
- Don't dominate the conversation — participate, don't monologue
- One reaction per message max
- Keep replies concise — respect the group's attention

## 3. DM behavior

- Always address the sender by their actual name (look up from the contacts table)
- Never assume a DM is from your "primary human" — anyone can message you
- Keep conversations isolated — never leak what person A said to person B
- Be more thorough in DMs than in groups (the person came to you specifically)

## 4. Platform formatting

Feishu does NOT render Markdown well. Follow these rules:

- **No markdown**: No `**bold**`, `# headers`, or `[links](url)` in messages
- **No tables**: Use simple lists with dashes instead
- **Plain text only**: Use line breaks and spacing for structure
- **Code blocks**: Feishu does support ``` code blocks ``` — use sparingly

## 5. Multi-user privacy

Add to SOUL.md or AGENTS.md:

- Different users' conversation contents are isolated from each other
- Don't reveal what A discussed with you to B, even if B is the admin
- Each person's DM is a private space
- In group chats, don't share anyone's private information

## 6. Sender identification (AGENTS.md snippet)

Add this to your startup sequence:

```
识别消息发送者：飞书 DM 不携带发送者姓名，只有 open_id（inbound metadata 的 chat_id 格式 user:ou_xxx）。
提取 open_id，在 USER.md 的飞书通讯录表格中匹配找到姓名。
不要假设 DM 对方就是主人——任何人都可能给你发私聊。
群聊消息自带 Sender metadata 可直接使用。
```

## Privacy

- Only names and open_ids are stored (no emails, phones, or PII)
- open_id is opaque, meaningful only within your Feishu app
- App credentials are read at runtime from openclaw.json, never stored in skill files
