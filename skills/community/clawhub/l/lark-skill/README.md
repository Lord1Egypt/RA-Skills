# feishu-lark — Comprehensive Feishu / Lark Skill for OpenClaw

> The most complete Feishu/Lark integration skill for OpenClaw agents. Covers every major API surface including messaging, group chat, Bitable, documents, calendar, video conferencing, meeting minutes, tasks, approvals, contacts, cloud drive, and wiki.

---

## ✨ What This Skill Does

This skill teaches your OpenClaw agent how to use the **official Feishu/Lark MCP server** (`@larksuiteoapi/lark-mcp`) to automate virtually anything in your Feishu/Lark workspace — from sending messages to managing meeting recordings.

### Covered API Areas

| Area | What you can do |
|------|----------------|
| **Messaging** | Send/edit/delete messages, all message types (text, cards, rich text), reactions, read receipts, pins, threads |
| **Group Chat** | Create/manage groups, members, announcements, tabs, forward messages, @mentions, interactive cards |
| **Bitable** | Create apps and tables, manage fields, search/create/update/delete records (batch), views, collaborators |
| **Documents** | Create docs, read content and blocks, insert content programmatically |
| **Cloud Drive** | List/move/copy/delete files, manage folders, permissions, comments |
| **Calendar** | Create/update/delete events, manage attendees, recurring events, free/busy checks |
| **Video Conferencing** | Schedule/manage meetings, invite/kick participants, recordings, attendance export, conference rooms |
| **Meeting Minutes** | Get transcripts with speaker labels, participant stats, audio/video file access |
| **Tasks** | Create/complete/delete tasks, task lists, sections, comments, member assignment |
| **Approvals** | Submit, approve, reject, cancel approval instances; add comments |
| **Contacts** | Look up users by email/phone, browse departments |
| **Wiki** | List spaces, browse/search nodes, create and move pages |

---

## ⚠️ Prerequisites

You **must** have the official Lark MCP server installed and running before this skill will work.

### 1. Install the MCP server
```bash
npm install -g @larksuiteoapi/lark-mcp
```

### 2. Create a Feishu/Lark app
1. Go to [Feishu Open Platform](https://open.feishu.cn/app) (or [Lark Open Platform](https://open.larksuite.com/app) for international)
2. Create a new custom app
3. Copy your **App ID** and **App Secret**
4. Enable the required permission scopes (see [Permissions](#permissions) below)

### 3. Start the MCP server
```bash
# App identity (background automation)
npx -y @larksuiteoapi/lark-mcp mcp -a <APP_ID> -s <APP_SECRET>

# User identity (recommended for interactive use)
npx -y @larksuiteoapi/lark-mcp login -a <APP_ID> -s <APP_SECRET>
npx -y @larksuiteoapi/lark-mcp mcp -a <APP_ID> -s <APP_SECRET>
```

### 4. Enable Video Conferencing + Minutes APIs
These are not enabled by default. Add the `-t` flag:
```bash
npx -y @larksuiteoapi/lark-mcp mcp -a <APP_ID> -s <APP_SECRET> \
  -t preset.calendar.default,vc.v1.reserve.apply,vc.v1.meeting.get,\
vc.v1.meetingRecording.get,minutes.v1.minute.get,\
minutes.v1.minuteTranscript.get,minutes.v1.minuteStatistic.get
```

For **Lark international** tenants, add `--domain https://open.larksuite.com`.

---

## 📦 Installation

### Via ClawHub CLI (recommended)
```bash
npm i -g clawhub
clawhub install feishu-lark
```

### Via GitHub URL
```bash
clawhub install https://github.com/YOUR_USERNAME/feishu-lark-skill
```

### Manual
Copy `SKILL.md` into your OpenClaw skills directory:
```bash
# Workspace-level (takes precedence)
cp SKILL.md <your-openclaw-workspace>/skills/feishu-lark/SKILL.md

# Or shared across all agents
cp SKILL.md ~/.openclaw/skills/feishu-lark/SKILL.md
```

Restart your OpenClaw session to activate.

---

## 🚀 Example Usage

Once installed, just talk to your OpenClaw agent naturally:

```
"Send a message to the #engineering group saying the deployment is done"

"Query all Bitable records in the Tasks table where Status = In Progress"

"Schedule a meeting with Alice and Bob tomorrow at 2pm and send them a calendar invite"

"Get the transcript from today's product meeting and summarize the action items, 
 then create tasks for each one and assign them to the right people"

"Show me who attended last week's all-hands meeting"
```

---

## 🔐 Permissions

Grant these scopes in your Feishu Open Platform app console:

| Feature | Required Scopes |
|---------|----------------|
| Send/read messages | `im:message`, `im:message:readonly` |
| Group management | `im:chat`, `im:chat:write` |
| Bitable | `bitable:app`, `bitable:app:readonly` |
| Documents | `docs:doc`, `docs:doc:readonly` |
| Cloud Drive | `drive:drive` |
| Calendar | `calendar:calendar`, `calendar:calendar:readonly` |
| Tasks | `task:task:write` |
| Contacts | `contact:user.base:readonly` |
| Wiki | `wiki:wiki:readonly` |
| Approvals | `approval:approval:readonly`, `approval:instance` |
| Video Conferencing | `vc:meeting`, `vc:record` |
| Meeting Minutes | `minutes:minute:readonly` |

---

## 🆚 Compared to Other Feishu Skills

| Feature | [FeiShuSkill](https://github.com/whatevertogo/feishuskill) | This Skill |
|---------|-------|------------|
| Messaging | ✅ Basic | ✅ Full (reactions, receipts, pins, threads, forward) |
| Group chat | ✅ Basic | ✅ Full (announcements, tabs, cards, @mentions) |
| Bitable | ✅ Basic | ✅ Full (batch ops, views, field management) |
| Documents | ✅ Read | ✅ Read + create + insert blocks |
| Calendar | ❌ | ✅ Full (events, attendees, recurrence, free/busy) |
| Video Conferencing | ❌ | ✅ Full (vc.v1 — schedule, manage, recordings, rooms) |
| Meeting Minutes | ❌ | ✅ Full (minutes.v1 — transcript, speakers, stats) |
| Tasks | ❌ | ✅ Full (task.v2 — create, assign, complete, lists) |
| Approvals | ❌ | ✅ Full (submit, approve/reject, track) |
| Cloud Drive | ❌ | ✅ Full (move, copy, permissions, comments) |
| Wiki | ✅ Search | ✅ Full (browse, search, create, move pages) |
| Pre-built workflows | ❌ | ✅ 12+ multi-step workflow patterns |
| Permissions reference | ❌ | ✅ Complete table |
| Error reference | ❌ | ✅ Common error codes + fixes |

---

## 📖 Full Documentation

See [SKILL.md](./SKILL.md) for the complete reference including all tool names, parameter structures, and workflow examples.

---

## 🙏 Credits

- Inspired by [FeiShuSkill](https://github.com/whatevertogo/feishuskill) by whatevertogo
- Built on the [official Feishu/Lark OpenAPI MCP](https://github.com/larksuite/lark-openapi-mcp) by larksuite
- For use with [OpenClaw](https://openclaw.ai) (formerly Clawdbot / Moltbot)

---

## 📄 License

[MIT](./LICENSE)
