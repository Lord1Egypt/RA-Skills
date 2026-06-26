# Nex Vault

Local Contract and Document Vault with Expiry Alerts.

Track contracts, leases, insurance policies, SLAs, warranties, licenses, subscriptions, certificates, and other important documents. Never miss an expiration date or renewal deadline again.

## Features

- **Document Management**: Upload and track contracts, leases, insurance, SLAs, warranties, and more
- **Automatic Date Extraction**: Parse PDF, DOCX, TXT, and scanned documents to extract key dates
- **Key Clause Extraction**: Automatically identify termination, renewal, payment, liability, and confidentiality clauses
- **Expiry Alerts**: Get notified when documents are expiring, renewal deadlines approaching, or termination notice periods are due
- **Telegram Integration**: Optional push notifications via Telegram
- **Full-Text Search**: Search across document names, parties, notes, and extracted content
- **Cost Tracking**: Track monthly and yearly costs for budgeting
- **Auto-Renewal Detection**: Identify and track automatic renewal clauses
- **Export**: Export document lists as CSV or JSON
- **Local Storage**: All data stays on your machine—no cloud, no telemetry

## Installation

```bash
bash setup.sh
```

## Quick Start

Add a contract:
```bash
nex-vault add /path/to/contract.pdf --type contract --party "Vendor Inc" --end-date 2027-01-01
```

View expiring documents:
```bash
nex-vault expiring 30
```

Show all details of a document:
```bash
nex-vault show 1
```

Get statistics:
```bash
nex-vault stats
```

Set up Telegram alerts:
```bash
nex-vault config set-telegram-token YOUR_BOT_TOKEN
nex-vault config set-telegram-chat YOUR_CHAT_ID
```

Run daily checks:
```bash
nex-vault alerts check
```

## Documentation

For full command reference and examples, see SKILL.md.

## Requirements

- Python 3.9+
- pdftotext (for PDF parsing)
- tesseract (for OCR on images/scanned PDFs)
- Optional: python-docx (for DOCX parsing)
- Optional: Pillow (for image preprocessing)

## License

MIT-0

---

Built by [Nex AI](https://nex-ai.be) — Digital transformation for Belgian SMEs.
