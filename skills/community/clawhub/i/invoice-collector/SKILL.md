---
name: invoice-collector
version: 1.2.0
description: Collect invoices/receipts from Gmail and send a summary email with attachments. Automatically downloads PDF attachments or takes screenshots of emails without PDFs. Use when user wants to gather invoices, receipts, or billing emails and forward them to another address. Requires gogcli (gog) to be configured with Gmail access.
metadata:
  openclaw:
    emoji: "🧾"
    requires:
      bins: ["gog", "node", "jq"]
      npm: ["puppeteer"]
    env:
      GOG_ACCOUNT: "Gmail account email (e.g. user@gmail.com)"
      GOG_KEYRING_PASSWORD: "Password for gogcli keyring storage"
---

# Invoice Collector

Collect invoices from Gmail and send them as a summary email with all attachments.

## Security Considerations

### Puppeteer `--no-sandbox` Flag

This skill uses `--no-sandbox` when launching Puppeteer/Chromium. This is **required** in many environments:

- **WSL (Windows Subsystem for Linux)**: Chrome sandbox requires kernel features not available in WSL1/WSL2
- **Docker containers**: Unless running with `--privileged` or specific seccomp profiles
- **CI/CD environments**: Most runners don't support Chrome's sandbox

**Risk**: Disabling the sandbox means if a malicious HTML email were rendered, it could potentially execute code outside the browser context.

**Mitigation**: This skill only renders emails from your own Gmail inbox. The risk is limited to emails you've already received. If you're concerned, review emails before processing or run in an isolated environment.

### Installation via `curl | tar`

The gogcli installation example uses `curl -sL ... | tar xz`, which is a common pattern but carries supply chain risks if the source were compromised.

**Safer alternative** (verify checksum):
```bash
# Download and verify
curl -sLO https://github.com/steipete/gogcli/releases/latest/download/gogcli_linux_amd64.tar.gz
curl -sLO https://github.com/steipete/gogcli/releases/latest/download/checksums.txt
sha256sum -c checksums.txt --ignore-missing
tar xzf gogcli_linux_amd64.tar.gz
mv gog ~/.local/bin/
```

**macOS users**: Use `brew install steipete/tap/gogcli` which handles verification automatically.

---

## Prerequisites & Setup

### 1. Install gogcli

```bash
# Linux (download binary)
curl -sL https://github.com/steipete/gogcli/releases/latest/download/gogcli_linux_amd64.tar.gz | tar xz
mv gog ~/.local/bin/

# macOS
brew install steipete/tap/gogcli
```

### 2. Setup Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Gmail API
3. Create OAuth credentials (Desktop app)
4. Download JSON

```bash
gog auth credentials ~/path/to/client_secret.json
gog auth add your@gmail.com
```

### 3. Install Puppeteer (for email screenshots)

```bash
cd /tmp && npm install puppeteer
```

### 4. Install Japanese fonts (optional, for JP emails)

```bash
sudo apt install fonts-noto-cjk
```

---

## Usage

### Generic Invoice Search

Search for any invoice/receipt without specifying specific senders:

```bash
export GOG_ACCOUNT="user@gmail.com"
export GOG_KEYRING_PASSWORD="your-password"

# Search all invoices in date range
gog gmail search '(invoice OR receipt OR 請求書 OR 領収書 OR billing OR payment) after:2026/01/01 before:2026/02/01'

# Search with specific criteria
gog gmail search 'subject:(invoice OR receipt) has:attachment after:2026/01/01'
```

### Workflow

1. **Search** - Find invoice emails
2. **Download** - Get PDFs or screenshot emails
3. **Summarize** - Create summary with amounts
4. **Send** - Email to destination with attachments

### Step 1: Search Invoices

```bash
# All invoices from last month
LAST_MONTH=$(date -d "1 month ago" +%Y/%m/01)
THIS_MONTH=$(date +%Y/%m/01)
gog gmail search "(invoice OR receipt OR 請求書 OR 領収書) after:$LAST_MONTH before:$THIS_MONTH" --json
```

### Step 2: Process Each Email

```bash
mkdir -p /tmp/invoices
```

**For emails WITH PDF attachments:**
```bash
# Get message details
MSG_ID="<message_id_here>"
EMAIL_JSON=$(gog gmail read $MSG_ID --json)

# Find PDF attachment
ATTACH_INFO=$(echo "$EMAIL_JSON" | jq -r '.thread.messages[0].payload.parts[]? | select(.filename | test("\\.pdf$"; "i")) | "\(.body.attachmentId)|\(.filename)"' | head -1)
ATTACH_ID=$(echo "$ATTACH_INFO" | cut -d'|' -f1)
FILENAME=$(echo "$ATTACH_INFO" | cut -d'|' -f2)

# Download
gog gmail attachment $MSG_ID "$ATTACH_ID" --out "/tmp/invoices/$FILENAME"
```

**For emails WITHOUT PDF (take screenshot):**
```bash
MSG_ID="<message_id_here>"

# Extract HTML
gog gmail read $MSG_ID --json | node -e "
const fs = require('fs');
let data = '';
process.stdin.on('data', chunk => data += chunk);
process.stdin.on('end', () => {
  const json = JSON.parse(data);
  const msg = json.thread.messages[0];
  let html = '';
  const findHtml = (p) => {
    if (p.mimeType === 'text/html' && p.body?.data) {
      html = Buffer.from(p.body.data, 'base64').toString('utf-8');
    }
    if (p.parts) p.parts.forEach(findHtml);
  };
  (msg.payload.parts || []).forEach(findHtml);
  if (!html && msg.payload.body?.data) {
    html = Buffer.from(msg.payload.body.data, 'base64').toString('utf-8');
  }
  fs.writeFileSync('/tmp/invoices/email.html', html || '<html><body>No content</body></html>');
});
"

# Screenshot
node -e "
const puppeteer = require('puppeteer');
const fs = require('fs');
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 800, height: 1200 });
  await page.setContent(fs.readFileSync('/tmp/invoices/email.html', 'utf-8'), { waitUntil: 'networkidle0' });
  await page.screenshot({ path: '/tmp/invoices/receipt.png', fullPage: true });
  await browser.close();
})();
"
```

### Step 3: Extract Invoice Info

Parse email for sender, date, amount:
```bash
# Get basic info from email
gog gmail read $MSG_ID --json | jq '{
  from: .thread.messages[0].payload.headers[] | select(.name=="From") | .value,
  subject: .thread.messages[0].payload.headers[] | select(.name=="Subject") | .value,
  date: .thread.messages[0].payload.headers[] | select(.name=="Date") | .value
}'
```

### Step 4: Send Summary Email

```bash
gog gmail send \
  --to "recipient@example.com" \
  --subject "【$(date +%Y年%m月)】請求書まとめ" \
  --body "請求書・領収書を添付します。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 請求書まとめ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【添付ファイル】
1. Invoice-001.pdf - Service A
2. Receipt.png - Service B (メールスクショ)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

このメールは自動生成されました。
" \
  --attach /tmp/invoices/Invoice-001.pdf \
  --attach /tmp/invoices/Receipt.png
```

---

## Example Prompts

**Generic:**
- "先月の請求書を全部集めてまとめて送って"
- "invoiceで検索して今月届いた請求書をkeiri@company.comに転送して"
- "has:attachment receipt で検索して請求書集めて"

**Specific:**
- "AnthropicとVercelとAWSの請求書を集めて"
- "from:stripe の請求書を過去3ヶ月分まとめて"

---

## Tips

- **Date format**: `YYYY/MM/DD` for gog search
- **PDF priority**: Always prefer PDF attachments over screenshots
- **Japanese fonts**: Required for correct rendering of JP emails
- **Cleanup**: `rm -rf /tmp/invoices` after sending
- **Cron**: Set up monthly cron job for recurring collection
