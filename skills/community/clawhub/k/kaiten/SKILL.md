---
name: kaiten
description: Manage Kaiten.ru project boards via REST API. Use when the user asks to create, view, update, move, or search cards (tasks), list spaces/boards/columns, manage tags, add comments, work with checklists, track time, or perform any project management action in Kaiten. Also triggers on mentions of "кайтен", "kaiten", "доска", "карточка", "задача" in project management context. NOT for: generic todo lists unrelated to Kaiten, or Jira/Trello/other PM tools.
metadata:
  { "openclaw": { "requires": { "env": ["KAITEN_TOKEN", "KAITEN_DOMAIN"] }, "primaryEnv": "KAITEN_TOKEN" } }
---

# Kaiten Skill

Manage Kaiten project boards via REST API (`api/latest`).

## Configuration

Environment variables (loaded from `~/.openclaw/secrets/kaiten.env`):
- `KAITEN_TOKEN` — Bearer API token
- `KAITEN_DOMAIN` — Company subdomain (e.g. `company.kaiten.ru`)

Before any API call, source the env file:
```bash
source ~/.openclaw/secrets/kaiten.env
```

## API Base

All requests go to: `https://$KAITEN_DOMAIN/api/latest/`

Auth header: `Authorization: Bearer $KAITEN_TOKEN`

## Quick Reference

### Read Operations

| Action | Endpoint | Method |
|--------|----------|--------|
| List spaces | `/spaces` | GET |
| Get space | `/spaces/{id}` | GET |
| List boards in space | `/spaces/{space_id}/boards` | GET |
| Get board | `/boards/{id}` | GET |
| List columns | `/boards/{board_id}/columns` | GET |
| List lanes | `/boards/{board_id}/lanes` | GET |
| List cards | `/cards?limit=N&offset=M` | GET |
| Get card | `/cards/{card_id}` | GET |
| Get card comments | `/cards/{card_id}/comments` | GET |
| Get card checklists | `/cards/{card_id}/checklists` | GET |
| Get card members | `/cards/{card_id}/members` | GET |
| Get card files | `/cards/{card_id}/files` | GET |
| Get card tags | `/cards/{card_id}/tags` | GET |
| Get card children | `/cards/{card_id}/children` | GET |
| Get card time logs | `/cards/{card_id}/time` | GET |
| List all tags | `/tags` | GET |
| List users | `/users` | GET |
| Current user | `/users/current` | GET |
| Search | `/search?query=TEXT` | GET |

### Write Operations

| Action | Endpoint | Method |
|--------|----------|--------|
| Create card | `/cards` | POST |
| Update card | `/cards/{card_id}` | PATCH |
| Move card | `/cards/{card_id}/location` | PATCH |
| Delete card | `/cards/{card_id}` | DELETE |
| Add comment | `/cards/{card_id}/comments` | POST |
| Add tag to card | `/cards/{card_id}/tags` | POST |
| Remove tag | `/cards/{card_id}/tags/{tag_id}` | DELETE |
| Add member | `/cards/{card_id}/members` | POST |
| Remove member | `/cards/{card_id}/members/{id}` | DELETE |
| Create checklist | `/cards/{card_id}/checklists` | POST |
| Add checklist item | `/cards/{card_id}/checklists/{cl_id}/items` | POST |
| Toggle checklist item | `/cards/{card_id}/checklists/{cl_id}/items/{item_id}` | PATCH |
| Log time | `/cards/{card_id}/time` | POST |
| Create board | `/spaces/{space_id}/boards` | POST |
| Create column | `/boards/{board_id}/columns` | POST |

## Card Creation (POST /cards)

Required fields:
```json
{
  "title": "Card title",
  "board_id": 123,
  "column_id": 456,
  "lane_id": 789
}
```

Optional fields: `description`, `owner_id`, `type_id`, `size`, `size_text`, `asap`, `due_date`, `planned_start`, `planned_end`, `tag_ids`, `member_ids`, `sort_order`.

## Card States

- `1` — active (default)
- `2` — archived

## Card Movement (PATCH /cards/{card_id}/location)

```json
{
  "board_id": 123,
  "column_id": 456,
  "lane_id": 789
}
```

## State & Defaults

State file: `SKILL_DIR/scripts/kaiten-state.json`

Stores `default_space_id`, `default_board_id`, `last_space_id`, `last_board_id`, `last_column_id`, `last_lane_id`.

**Rules:**
- When user sets a default space/board → update `default_*` fields
- After any operation on a space/board/column/lane → update `last_*` fields
- When creating a card without explicit board → use `default_board_id`, fall back to `last_board_id`
- When user says "текущая доска" / "та же доска" → use `last_board_id`
- Read state before operations, write state after

```bash
# Read state
bash SKILL_DIR/scripts/kaiten.sh state

# Set default space
bash SKILL_DIR/scripts/kaiten.sh set-default-space <space_id>

# Set default board
bash SKILL_DIR/scripts/kaiten.sh set-default-board <board_id>
```

## Workflow

1. Source env: `source ~/.openclaw/secrets/kaiten.env`
2. Check state: `bash SKILL_DIR/scripts/kaiten.sh state`
3. Use `scripts/kaiten.sh` for common operations
4. For complex queries, use curl directly with the API base

## Script Usage

The `scripts/kaiten.sh` helper wraps common operations:

```bash
# Source env first
source ~/.openclaw/secrets/kaiten.env

# List spaces
bash SKILL_DIR/scripts/kaiten.sh spaces

# List boards in a space
bash SKILL_DIR/scripts/kaiten.sh boards <space_id>

# List columns on a board
bash SKILL_DIR/scripts/kaiten.sh columns <board_id>

# List lanes on a board
bash SKILL_DIR/scripts/kaiten.sh lanes <board_id>

# Get cards (with optional limit/offset)
bash SKILL_DIR/scripts/kaiten.sh cards [limit] [offset]

# Search cards
bash SKILL_DIR/scripts/kaiten.sh search "query text"

# Get single card
bash SKILL_DIR/scripts/kaiten.sh card <card_id>

# Create card
bash SKILL_DIR/scripts/kaiten.sh create-card <board_id> <column_id> <lane_id> "title" ["description"]

# Update card
bash SKILL_DIR/scripts/kaiten.sh update-card <card_id> '{"title":"new title"}'

# Move card
bash SKILL_DIR/scripts/kaiten.sh move-card <card_id> <board_id> <column_id> <lane_id>

# Add comment
bash SKILL_DIR/scripts/kaiten.sh comment <card_id> "comment text"

# List tags
bash SKILL_DIR/scripts/kaiten.sh tags

# Add tag to card
bash SKILL_DIR/scripts/kaiten.sh add-tag <card_id> <tag_id>

# List users
bash SKILL_DIR/scripts/kaiten.sh users

# Current user
bash SKILL_DIR/scripts/kaiten.sh me

# Card checklists
bash SKILL_DIR/scripts/kaiten.sh checklists <card_id>

# Create checklist
bash SKILL_DIR/scripts/kaiten.sh create-checklist <card_id> "checklist name"

# Add checklist item
bash SKILL_DIR/scripts/kaiten.sh add-checklist-item <card_id> <checklist_id> "item text"

# Log time
bash SKILL_DIR/scripts/kaiten.sh log-time <card_id> <minutes> ["comment"]
```

## API Details

For full endpoint documentation and field schemas, see `references/api-reference.md`.
