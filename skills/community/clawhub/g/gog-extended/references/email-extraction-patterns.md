# Email Extraction Patterns

Common workflows for extracting structured data from emails using `gog`.

## Order Tracking Workflow

**Goal**: Track an order from confirmation email to shipping notification.

```bash
# 1. Find order confirmation
gog gmail messages search 'from:orders@lululemon.com subject:"We got your order"' --max 1 --account liyanjia92@gmail.com

# 2. Extract message ID from results
# 3. Read full email body
gog gmail get <messageId> --format=full --account liyanjia92@gmail.com

# 4. Extract relevant fields (grep, sed, awk as needed)
gog gmail get <messageId> --format=full --account liyanjia92@gmail.com | grep -A 2 "Items Purchased"
```

**Real example:**
```bash
$ gog gmail get 19d33029153e8b10 --format=full --account liyanjia92@gmail.com | grep -i "item\|product\|cap"
Structured Classic Ball Cap *Golf L
1 x
Subtotal (1 item)
$44.00
```

## Invoice Extraction

**Goal**: Extract invoice amounts and dates from transactional emails.

```bash
# Search for invoice emails
gog gmail messages search 'subject:invoice from:billing@example.com after:2026-01-01' --max 50 --account you@example.com

# Extract invoice details
for msgId in <list of message IDs>; do
  echo "=== Invoice $msgId ==="
  gog gmail get $msgId --format=full --account you@example.com | grep -E "Invoice|Total|Due Date"
done
```

## Attachment Download

**Goal**: Extract and save attachments from emails (e.g., receipts, invoices).

```bash
# 1. Find email with attachment
gog gmail messages search 'has:attachment subject:receipt' --max 1 --account you@example.com

# 2. Get full message to find attachment ID
gog gmail get <messageId> --format=full --account you@example.com

# 3. Extract attachment (look for attachmentId in output)
gog gmail attachment <messageId> <attachmentId>
```

## Multi-Account Search

**Goal**: Search across multiple configured Gmail accounts.

```bash
# List all accounts
gog auth list

# Search personal Gmail
gog gmail search 'newer_than:7d' --max 10 --account liyanjia92@gmail.com

# Search Berkeley account
gog gmail search 'newer_than:7d' --max 10 --account yanjia.li@berkeley.edu
```

## Unread Message Triage

**Goal**: Process all unread emails from a sender.

```bash
# Find unread from specific sender
gog gmail messages search 'is:unread from:important@example.com' --max 50 --account you@example.com --json

# Process each (example: extract subject and sender)
gog gmail messages search 'is:unread from:important@example.com' --json --account you@example.com | \
  jq -r '.messages[] | "\(.from) - \(.subject)"'
```

## Payment Status Tracking

**Goal**: Monitor order/payment status from transactional emails.

```bash
# Search for status updates
gog gmail messages search 'from:order@example.com (status OR "on its way" OR shipped OR delivered)' --max 20

# Extract each status update
for msgId in <ids>; do
  echo "Date: $(gog gmail get $msgId --format=full | grep -i date | head -1)"
  echo "Status: $(gog gmail get $msgId --format=full | grep -i 'on its way\|shipped\|delivered')"
  echo "---"
done
```

## JSON Output for Scripting

**Goal**: Parse Gmail data programmatically.

```bash
# Get JSON output
gog gmail messages search 'from:sender@example.com' --max 20 --json --account you@example.com

# Parse with jq
gog gmail messages search 'from:sender@example.com' --json --account you@example.com | \
  jq '.messages[] | {date: .date, from: .from, subject: .subject}'
```

Example output:
```json
{
  "date": "2026-03-29 21:13",
  "from": "lululemon <noreply@e.lululemon.com>",
  "subject": "Your gear is on its way! [c177467696945199]"
}
```

## Automation Notes

- Always use `--account` when multiple accounts are configured
- Use `--json` for programmatic parsing
- Use `--no-input` to skip confirmations in scripts
- Use `gog gmail get --format=full` for complete email body (don't rely on search metadata)
- Test grep/sed patterns on sample emails first before automating
