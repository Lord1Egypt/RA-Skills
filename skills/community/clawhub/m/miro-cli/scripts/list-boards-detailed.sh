#!/bin/bash
# List boards with detailed information in a readable format

OUTPUT_FORMAT="${1:-table}"  # table or json

case "$OUTPUT_FORMAT" in
  table)
    echo "🎨 Miro Boards (Table View)"
    echo ""
    mirocli boards list --json 2>/dev/null | jq -r '
      .[] |
      "\(.name | .[:30] | @json) | \(.owner.name // "Unknown" | @json) | \(.id | @json)"
    ' | column -t -s'|' -N'BOARD NAME,OWNER,BOARD ID'
    ;;
  
  json)
    echo "Fetching boards as JSON..."
    mirocli boards list --json
    ;;
  
  csv)
    echo "Board Name,Owner,Team ID,Board ID,Created,Modified"
    mirocli boards list --json 2>/dev/null | jq -r '
      .[] |
      "\(.name),\(.owner.name // "Unknown"),\(.team_id // ""),\(.id),\(.created_at // ""),\(.modified_at // "")"
    '
    ;;
  
  owners)
    echo "📊 Board Count by Owner"
    echo ""
    mirocli boards list --json 2>/dev/null | jq -r '
      group_by(.owner.name) |
      map({owner: .[0].owner.name, count: length}) |
      sort_by(-.count) |
      .[] |
      "\(.count) boards | \(.owner)"
    '
    ;;
  
  teams)
    echo "📊 Board Count by Team"
    echo ""
    mirocli boards list --json 2>/dev/null | jq -r '
      group_by(.team_id) |
      map({team_id: .[0].team_id, count: length}) |
      sort_by(-.count) |
      .[] |
      "\(.count) boards | Team: \(.team_id)"
    '
    ;;
  
  *)
    echo "Usage: $0 [format]"
    echo ""
    echo "Formats:"
    echo "  table   - Readable table format (default)"
    echo "  json    - Full JSON output"
    echo "  csv     - CSV format"
    echo "  owners  - Board count by owner"
    echo "  teams   - Board count by team"
    exit 1
    ;;
esac
