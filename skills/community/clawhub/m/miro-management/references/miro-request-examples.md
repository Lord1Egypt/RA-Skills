# Miro request examples

Use these as starter patterns for common write operations.

## Create a sticky note

```powershell
python scripts/miro_api.py create-sticky-note --board-id <board_id> "Hello from OpenClaw"
```

## Update a sticky note

```powershell
python scripts/miro_api.py update-sticky-note --board-id <board_id> --item-id <item_id> --content "Updated idea"
```

## Create text

```powershell
python scripts/miro_api.py create-text --board-id <board_id> "Roadmap draft" --x 300 --y 50
```

## Update text

```powershell
python scripts/miro_api.py update-text --board-id <board_id> --item-id <item_id> --content "Reworded text"
```

## Create a shape

```powershell
python scripts/miro_api.py create-shape --board-id <board_id> "API Layer" --shape rectangle --x 0 --y -200
```

## Update a shape

```powershell
python scripts/miro_api.py update-shape --board-id <board_id> --item-id <item_id> --content "Gateway" --fill-color light_green
```

## Create a card

```powershell
python scripts/miro_api.py create-card --board-id <board_id> "Task: OAuth flow" --description "Implement token refresh and board listing"
```

## Update a card

```powershell
python scripts/miro_api.py update-card --board-id <board_id> --item-id <item_id> --title "Task: done"
```

## Export board items

```powershell
python scripts/miro_api.py export-board-items --board-id <board_id> --format markdown --output-file board-report.md
python scripts/miro_api.py export-board-items --board-id <board_id> --format csv --output-file board-items.csv
python scripts/miro_api.py export-board-items --board-id <board_id> --format json --output-file board-items.json
```

## Preview a write before sending it

```powershell
python scripts/miro_api.py preview-write POST /boards/{board_id}/sticky_notes --body-file sticky.json
```

## Create a connector

```powershell
python scripts/miro_api.py create-connector --board-id <board_id> --start-item-id <item_a> --end-item-id <item_b>
```

## List board members

```powershell
python scripts/miro_api.py list-board-members --board-id <board_id>
```

## Brainstorm cluster helper

```powershell
python scripts/miro_api.py create-brainstorm-cluster --board-id <board_id> "Idea 1" "Idea 2" "Idea 3"
```

## Simple kanban helper

```powershell
python scripts/miro_api.py create-kanban-row --board-id <board_id> --columns "Backlog,Doing,Done"
```

## Architecture diagram helper

```powershell
python scripts/miro_api.py create-architecture-chain --board-id <board_id> --labels "Client,API,Database"
```

## Raw request with JSON body

```powershell
python scripts/miro_api.py raw POST /boards/{board_id}/sticky_notes --body-file sticky.json
```

## Access token shortcuts

Use either a saved token file or a direct token:

```powershell
$env:MIRO_ACCESS_TOKEN = '...'
python scripts/miro_api.py list-boards
```
