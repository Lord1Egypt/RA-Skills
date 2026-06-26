#!/bin/bash
# Export macOS notifications to date-based folder

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTIF_SCRIPT="$SCRIPT_DIR/read_notifications.py"

TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Default output directory (user's memory folder)
OUTPUT_DIR="${HOME}/.openclaw/workspace/memory/$TODAY/computer_io/notification"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="$OUTPUT_DIR/$TIMESTAMP.md"

# Read notifications from the last 24 hours
python3 "$NOTIF_SCRIPT" --hours 24 --output "/tmp/notif_$TIMESTAMP.txt" 2>/dev/null

# Convert to markdown format
python3 - "$OUTPUT_FILE" "$TODAY" "$TIMESTAMP" << 'PYEOF'
import sys
import os

output_file = sys.argv[1]
today = sys.argv[2]
timestamp = sys.argv[3]

temp_file = f"/tmp/notif_{timestamp}.txt"

if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# macOS Notifications\n- Date: {today}\n- Timestamp: {timestamp}\n\nNo notifications recorded.\n")
    print(f"Exported to {output_file} (no notifications)")
    exit(0)

with open(temp_file, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')[1:]  # Skip header

# Write markdown
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"# macOS Notifications Export\n")
    f.write(f"- Date: {today}\n")
    f.write(f"- Timestamp: {timestamp}\n")
    f.write(f"- Total: {len([l for l in lines if '|' in l])} items\n\n")
    f.write(f"## Notifications\n\n")
    f.write(f"| Time | App | Content |\n")
    f.write(f"|------|-----|--------|\n")
    
    for line in lines:
        if '|' in line:
            parts = line.split('|', 2)
            if len(parts) >= 3:
                time = parts[0].strip()
                app = parts[1].strip()
                content = parts[2].strip().replace('|', '\\|')[:100]
                f.write(f"| {time} | {app} | {content} |\n")

# Clean up temp file
os.remove(temp_file)

print(f"Exported to {output_file}")
