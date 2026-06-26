---
name: mac-reminders-agent
version: 1.4.0
author: swancho
license: MIT
description: |
  Integrate with macOS Reminders app to check, add, edit, delete, and complete reminders.
  Supports multiple reminder lists (calendars), priority levels (high/medium/low), and title search.
  Supports native recurrence (매주/weekly/毎週/每周) via Swift EventKit - creates single reminder with repeat rule.
  Supports editing and deleting reminders by ID (calendarItemIdentifier from EventKit).
  Supports multiple languages (en, ko, ja, zh) for trigger detection and response formatting.
  When users request recurring reminders, MUST use --repeat option (daily|weekly|monthly|yearly).
  Supports parsing meeting notes to extract action items and suggest reminders (parse command).
  Parse command is pure text processing - no Reminders app access required.
requirements:
  runtime:
    - node >= 18.0.0
    - npm
    - macOS with Xcode Command Line Tools (includes Swift compiler)
  permissions:
    - macOS Reminders access (system prompt on first use)
repository: https://github.com/swancho/mac-reminders-agent
install: |
  cd $SKILL_DIR && npm install
---

# Mac Reminders Agent

## Overview

This skill integrates with the local macOS **Reminders** app to:

- View and organize today's/this week's reminders (with unique IDs)
- **Multiple lists**: View all reminder lists, filter/add to specific lists
- **Priority**: Set and view priority levels (high/medium/low)
- **Search**: Find reminders by title keyword
- Add new reminders based on natural language requests
- **Edit reminders**: Modify title, due date, notes, priority by ID
- **Delete reminders**: Remove reminders by ID
- **Complete reminders**: Mark reminders as done by ID
- **Native recurrence**: Weekly, daily, monthly, yearly repeating reminders
- **Parse meeting notes**: Extract action items from text and suggest reminders
- **Multi-language support**: English, Korean, Japanese, Chinese

The skill uses the following files relative to its directory:

- `cli.js` (unified entry point)
- `reminders/apple-bridge.js` (backend: AppleScript + `applescript` npm module)
- `reminders/eventkit-bridge.swift` (native recurrence via Swift EventKit)
- `reminders/meeting-parser.js` (meeting notes parser for action item extraction)
- `locales.json` (language-specific triggers and responses)

## Language Support

The skill automatically detects user language or can be explicitly set via `--locale` parameter.

### Supported Languages

| Code | Language | Example Trigger |
|------|----------|-----------------|
| `en` | English | "What do I have to do today?" |
| `ko` | 한국어 | "오늘 할 일 뭐 있어?" |
| `ja` | 日本語 | "今日のタスクは？" |
| `zh` | 中文 | "今天有什么任务？" |

### Language Detection

1. **Explicit**: Use `--locale` parameter
2. **Automatic**: Detect from user's message language
3. **Default**: Falls back to `en` (English)

---

## How It Works

User natural language requests are handled in two cases:

1. **List reminders (list)**
2. **Add reminder (add)**

For each case, call the Node.js CLI, receive JSON results, and format them using locale-specific templates.

---

## 0) View Reminder Lists

### Command Invocation

```bash
node skills/mac-reminders-agent/cli.js lists --locale ko
```

### Output Format

Returns JSON with calendars array:

```json
{
  "calendars": [
    { "id": "cal-id-1", "name": "Reminders", "isDefault": true },
    { "id": "cal-id-2", "name": "Work", "isDefault": false }
  ]
}
```

---

## 1) List Reminders

### Trigger Examples (by language)

**English:**
- "What do I have to do today?"
- "Show me today's reminders"
- "What's on my schedule this week?"

**Korean (한국어):**
- "오늘 할 일 뭐 있어?"
- "오늘 미리알림 정리해줘"
- "이번 주 일정 뭐 있어?"

**Japanese (日本語):**
- "今日のタスクは？"
- "今日のリマインダーを見せて"

**Chinese (中文):**
- "今天有什么任务？"
- "显示今天的提醒"

### Command Invocation

```bash
# List with default locale (en)
node skills/mac-reminders-agent/cli.js list --scope today

# List with specific locale
node skills/mac-reminders-agent/cli.js list --scope week --locale ko

# List from specific list
node skills/mac-reminders-agent/cli.js list --scope week --list "Work"

# Search by title keyword
node skills/mac-reminders-agent/cli.js list --query "meeting" --scope all
```

### Parameters

- `--scope` (optional): `today`, `week` (default), `all`
- `--list` (optional): Filter by reminder list name (omit for all lists)
- `--query` (optional): Filter by title keyword (case-insensitive)
- `--locale` (optional): Response language (en, ko, ja, zh)

### Output Format

Returns JSON with items array:

```json
[
  {
    "id": "ABC-123-DEF",
    "title": "Task title",
    "due": "2026-02-05T16:30:00+09:00",
    "list": "Work",
    "priority": "high",
    "completed": false
  }
]
```

### Response Formatting

Use `locales.json` templates to format responses in user's language:

**English:**
```
[Incomplete Reminders]
- 2/2 (Mon) 09:00 [Work] Meeting
- 2/3 (Tue) 14:00 [Personal] Visit bank

[Completed]
- 2/1 (Sun) [Work] Submit report ✅
```

**Korean:**
```
[미완료 미리알림]
- 2/2 (월) 09:00 [업무] 회의
- 2/3 (화) 14:00 [개인] 은행 방문

[완료됨]
- 2/1 (일) [업무] 보고서 제출 ✅
```

---

## 2) Add Reminder

### Trigger Examples (by language)

**English:**
- "Add a meeting reminder for 9am tomorrow"
- "Set a reminder to submit report by Friday"

**Korean (한국어):**
- "내일 아침 9시에 회의 미리알림 추가해줘"
- "이번 주 금요일까지 보고서 제출 미리알림 넣어줘"

**Japanese (日本語):**
- "明日の朝9時に会議のリマインダーを追加して"

**Chinese (中文):**
- "添加明天早上9点的会议提醒"

### Command Invocation

```bash
# Add with locale
node skills/mac-reminders-agent/cli.js add --title "Meeting" --due "2026-02-05T09:00:00+09:00" --locale ko

# Add with priority and specific list
node skills/mac-reminders-agent/cli.js add --title "Urgent Report" --due "2026-02-05T17:00:00+09:00" --priority high --list "Work" --locale ko
```

### Parameters

- `--title` (required): Reminder title
- `--due` (optional): ISO 8601 format (`YYYY-MM-DDTHH:mm:ss+09:00`)
- `--note` (optional): Additional notes
- `--priority` (optional): `high`, `medium`, `low`, `none` (default: none)
- `--list` (optional): Target reminder list name (default: system default list)
- `--locale` (optional): Response language (en, ko, ja, zh)

### Response Examples

**English:**
- "Added 'Meeting' reminder for 9am tomorrow."
- "Added 'Submit report' reminder without a due date."

**Korean:**
- "'회의' 미리알림을 추가했어요 (내일 오전 9시)."
- "'보고서 제출' 미리알림을 추가했어요 (마감일 없음)."

---

## 3) Edit Reminder

### Trigger Examples (by language)

**English:**
- "Change the meeting reminder to 10am"
- "Update the report deadline to next Monday"

**Korean (한국어):**
- "회의 미리알림 10시로 바꿔줘"
- "보고서 마감일 다음 주 월요일로 수정해줘"

### Command Invocation

```bash
# Edit title
node skills/mac-reminders-agent/cli.js edit --id "ABC123" --title "New Meeting Title" --locale ko

# Edit due date
node skills/mac-reminders-agent/cli.js edit --id "ABC123" --due "2026-03-01T10:00:00+09:00"

# Edit priority
node skills/mac-reminders-agent/cli.js edit --id "ABC123" --priority high

# Edit note
node skills/mac-reminders-agent/cli.js edit --id "ABC123" --note "Updated notes"
```

### Parameters

- `--id` (required): Reminder ID (calendarItemIdentifier from list output)
- `--title` (optional): New title
- `--due` (optional): New due date in ISO 8601 format
- `--note` (optional): New note text
- `--priority` (optional): `high`, `medium`, `low`, `none`
- `--locale` (optional): Response language (en, ko, ja, zh)

### IMPORTANT: Use `list` first to get reminder IDs

Before editing, always run `list` to get the reminder's `id` field. The `id` is an EventKit `calendarItemIdentifier` (UUID-like string).

---

## 4) Delete Reminder

### Trigger Examples (by language)

**English:**
- "Delete the meeting reminder"

**Korean (한국어):**
- "회의 미리알림 삭제해줘"

### Command Invocation

```bash
node skills/mac-reminders-agent/cli.js delete --id "ABC123" --locale ko
```

### Parameters

- `--id` (required): Reminder ID (from list output)
- `--locale` (optional): Response language

---

## 5) Complete Reminder

### Trigger Examples (by language)

**English:**
- "Mark the meeting reminder as done"

**Korean (한국어):**
- "회의 미리알림 완료 처리해줘"

### Command Invocation

```bash
node skills/mac-reminders-agent/cli.js complete --id "ABC123" --locale ko
```

### Parameters

- `--id` (required): Reminder ID (from list output)
- `--locale` (optional): Response language

---

## 6) Recurring Reminders (Native Recurrence)

Use `--repeat` to create reminders with **native recurrence** (single reminder with repeat rule, not multiple copies).

### Command Invocation

```bash
# Weekly recurring reminder
node skills/mac-reminders-agent/cli.js add --title "Weekly standup" --due "2026-02-10T09:00:00+09:00" --repeat weekly

# Bi-weekly reminder
node skills/mac-reminders-agent/cli.js add --title "Sprint review" --due "2026-02-10T14:00:00+09:00" --repeat weekly --interval 2

# Monthly reminder until end of year
node skills/mac-reminders-agent/cli.js add --title "Monthly report" --due "2026-02-28T17:00:00+09:00" --repeat monthly --repeat-end 2026-12-31
```

### Parameters

- `--repeat` (optional): `daily`, `weekly`, `monthly`, `yearly`
- `--interval` (optional): Repeat interval (default: 1). Example: `--interval 2` = every 2 weeks
- `--repeat-end` (optional): End date in `YYYY-MM-DD` format

### IMPORTANT: Always use --repeat for recurring schedules

When user requests recurring reminders (매주, 격주, 매월, etc.), **MUST use --repeat option**.
Do NOT create multiple individual reminders manually.

**Correct:**
```bash
node cli.js add --title "주간 회의" --due "2026-02-10T09:00:00+09:00" --repeat weekly
```

**Wrong (DO NOT DO THIS):**
```bash
# Creating 12 separate reminders is WRONG
node cli.js add --title "주간 회의 - 2/10" --due "2026-02-10T09:00:00+09:00"
node cli.js add --title "주간 회의 - 2/17" --due "2026-02-17T09:00:00+09:00"
...
```

---

## 7) Parse Meeting Notes

Extract action items from meeting notes and suggest reminders. Pure text processing - no Reminders app access required.

### Trigger Examples (by language)

**English:**
- "Parse my meeting notes"
- "Extract action items from this text"

**Korean (한국어):**
- "회의록에서 할 일 추출해줘"
- "미팅 내용에서 할 일 뽑아줘"

**Japanese (日本語):**
- "議事録からアクションアイテムを抽出して"

**Chinese (中文):**
- "从会议记录中提取行动项"

### Command Invocation

```bash
# From inline text
node skills/mac-reminders-agent/cli.js parse --text "Q1 report due by March 20. John: prepare slides by Friday - URGENT" --locale en

# From a file
node skills/mac-reminders-agent/cli.js parse --file /path/to/meeting_notes.txt --locale ko
```

### Parameters

- `--text` (required if no --file): Meeting notes as a string
- `--file` (required if no --text): Path to a text file containing meeting notes
- `--locale` (optional): Language for pattern matching (en, ko, ja, zh). Auto-detected if omitted.

### Output Format

```json
{
  "ok": true,
  "locale": "en",
  "labels": {},
  "items": [
    {
      "title": "Submit Q1 report",
      "due": "2026-03-20T17:00:00+09:00",
      "priority": "high",
      "confidence": "high",
      "source_line": "Q1 report due by March 20 - URGENT"
    }
  ]
}
```

### Detected Patterns

| Language | Action Keywords | Date Patterns | Priority Signals |
|----------|----------------|---------------|-----------------|
| English | TODO:, action item:, by [date], deadline:, need to | by March 20, tomorrow, next Friday | urgent, important, nice to have |
| Korean | ~까지, ~해야, ~할 것, 담당:, 기한: | 3월 15일, 내일, 다음 주 | 긴급, 중요, 나중에 |
| Japanese | ~まで, ~する必要, 担当:, 期限: | 3月15日, 明日, 来週 | 緊急, 重要, できれば |
| Chinese | ~之前, ~需要, 负责:, 截止: | 3月15日, 明天, 下周 | 紧急, 重要, 如果可以 |

### IMPORTANT: Recommended Claude Workflow

1. Call `parse` to get suggested `items[]`
2. Present each item to the user with title, due date, and priority
3. Ask user which items to add (all / specific ones / none)
4. For each approved item, call `add --title ... --due ... --priority ...`

**The `parse` command only suggests. Claude MUST call `add` explicitly for each approved item.**
**Do NOT auto-add without user confirmation.**

---

## Error Handling

### Locale-aware Error Messages

**English:**
- "There was a problem accessing the Reminders app."

**Korean:**
- "미리알림 앱에 접근하는 데 문제가 생겼어요."

**Japanese:**
- "リマインダーアプリへのアクセスに問題が発生しました。"

### Fallback Suggestions

When automatic integration fails, offer alternatives in user's language.

---

## Requirements & Installation

### System Requirements

| Requirement | Details |
|-------------|---------|
| **OS** | macOS only (tested on macOS 13+) |
| **Node.js** | v18.0.0 or higher |
| **npm** | Included with Node.js |
| **Swift** | Included with Xcode Command Line Tools |

### Installation

```bash
# 1. Install Xcode Command Line Tools (if not already installed)
xcode-select --install

# 2. Install npm dependencies
cd $SKILL_DIR
npm install
```

### macOS Permissions

This skill requires access to the **Reminders** app. On first use:

1. macOS will display a permission dialog asking to allow access to Reminders
2. Click **"OK"** or **"Allow"** to grant access
3. If denied, go to **System Settings > Privacy & Security > Reminders** and enable access for Terminal/your IDE

> **Note**: The Swift EventKit bridge (`eventkit-bridge.swift`) is compiled on-the-fly when needed. No manual compilation required.

---

## Summary

- Multi-language support via `locales.json` (en, ko, ja, zh)
- Core commands:
  - `lists [--locale XX]` — view all reminder lists (calendars)
  - `list --scope today|week|all [--list "NAME"] [--query "KEYWORD"] [--locale XX]` — returns items with `id`, `list`, `priority` fields
  - `add --title ... [--due ...] [--priority high|medium|low|none] [--list "NAME"] [--repeat daily|weekly|monthly|yearly] [--interval N] [--repeat-end YYYY-MM-DD] [--locale XX]`
  - `edit --id ID [--title ...] [--due ...] [--note ...] [--priority ...] [--locale XX]`
  - `delete --id ID [--locale XX]`
  - `complete --id ID [--locale XX]`
- **Multiple lists**: Target specific reminder lists or search across all
- **Priority**: Set priority levels on reminders (high/medium/low)
- **Search**: Filter reminders by title keyword
- **Native recurrence**: Use `--repeat` for recurring reminders (creates single reminder with repeat rule)
- **Parse meeting notes**: `parse --text "..." [--file path] [--locale XX]` — extract action items and suggest reminders
- Automatically detect user language or use explicit `--locale` parameter
- Format responses using locale-specific templates
