# LogClip

Quickly extract and reformat timestamped log entries from raw text using a simple date range filter. Perfect for developers who need to isolate log events from unstructured or mixed log data.

## Usage

```bash
# Filter logs from stdin between two dates
echo -e "2023-10-05 13:45:10 Error connecting\n2023-10-06 10:11:12 OK" | python logclip.py "2023-10-05" "2023-10-05"

# Filter logs from a file and reformat timestamps
python logclip.py "2023-10-01" "2023-10-31" -i app.log -f '%b %d %H:%M'

# Use custom timestamp pattern
python logclip.py "2023-10-01" "2023-10-31" -i server.log -r '(\d{4})/(\d{2})/(\d{2})\s+(\d{2}):(\d{2})'
```

## Price

$2.50
