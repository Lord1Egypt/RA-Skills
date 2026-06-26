# OpenClaw Skill: Kaiten

AgentSkill for managing [Kaiten.ru](https://kaiten.ru) project boards via REST API.

## Features

- List spaces, boards, columns, lanes
- Create, update, move, delete cards
- Search cards
- Manage tags, members, comments
- Checklists and time tracking
- **Default space & board** — set once, use everywhere
- **State tracking** — remembers last-used space/board/column/lane
- Full CLI wrapper script

## Installation

```bash
# Copy skill to your OpenClaw workspace
cp -r kaiten/ ~/.openclaw/workspace/skills/

# Set up credentials
mkdir -p ~/.openclaw/secrets
cat > ~/.openclaw/secrets/kaiten.env << 'ENVEOF'
KAITEN_TOKEN=your-bearer-token
KAITEN_DOMAIN=yourcompany.kaiten.ru
ENVEOF
chmod 600 ~/.openclaw/secrets/kaiten.env
```

## State & Defaults

The skill maintains a `kaiten-state.json` file to remember your preferred workspace context.

### Setting defaults

```bash
# Set default space (used when no space is specified)
bash scripts/kaiten.sh set-default-space <space_id>

# Set default board (used when creating cards without explicit board)
bash scripts/kaiten.sh set-default-board <board_id>

# View current state
bash scripts/kaiten.sh state
```

### How it works

- **`default_space_id`** / **`default_board_id`** — your preferred space and board, set explicitly
- **`last_space_id`** / **`last_board_id`** / **`last_column_id`** / **`last_lane_id`** — auto-updated after every operation

When you ask the agent to create a card without specifying a board, it uses the default board. If no default is set, it falls back to the last-used board.

### State file example

```json
{
  "default_space_id": 213469,
  "default_board_id": 673200,
  "last_space_id": 180884,
  "last_board_id": 442783,
  "last_column_id": 1529792,
  "last_lane_id": 585730
}
```

> **Note:** `kaiten-state.json` is gitignored — it's user-specific runtime data.

## Usage

The skill is automatically triggered when you mention Kaiten, tasks, boards, or cards in your conversations with the OpenClaw agent.

### CLI commands

```
STATE:
  state                          Show current defaults & last used
  set-default-space <space_id>   Set default space
  set-default-board <board_id>   Set default board

READ:
  spaces                         List all spaces
  boards <space_id>              List boards in a space
  columns <board_id>             List columns on a board
  lanes <board_id>               List lanes on a board
  cards [limit] [offset]         List cards
  card <card_id>                 Get card details
  search <query>                 Search cards
  tags                           List all tags
  users                          List all users
  me                             Current user info

WRITE:
  create-card <board> <col> <lane> <title> [desc]
  update-card <card_id> '{"field":"value"}'
  move-card <card_id> <board> <col> <lane>
  delete-card <card_id>
  comment <card_id> <text>
  add-tag <card_id> <tag_id>
  remove-tag <card_id> <tag_id>
  add-member <card_id> <user_id>
  remove-member <card_id> <member_id>
  create-checklist <card_id> <name>
  add-checklist-item <card_id> <cl_id> <text>
  toggle-checklist-item <card_id> <cl_id> <item_id>
  log-time <card_id> <minutes> [comment]
```

## API Documentation

Full Kaiten API docs: https://developers.kaiten.ru

## License

MIT
