---
name: gmail-enhanced
description: Enhanced Gmail integration with advanced features including label management, attachment handling, advanced search, email parsing, and automated email processing workflows.
tags:
  - gmail
  - email
  - google
  - automation
  - attachment
version: 1.0.0
author: chenq
---

# Gmail Enhanced

Advanced Gmail integration with powerful automation features.

## Features

### 1. Advanced Search
- Complex query building (AND, OR, NOT)
- Date range filters
- Attachment filters
- Label filters
- Search within attachments

### 2. Label Management
- Create, rename, delete labels
- Nested labels (folders)
- Color customization
- Label statistics

### 3. Attachment Handling
- Download attachments
- Upload and send attachments
- Filter attachments by type/size
- Extract attachments to cloud storage

### 4. Email Processing
- Auto-categorize emails
- Extract data from emails
- Auto-reply rules
- Email templates
- Bounce detection

### 5. Email Parsing
- Extract structured data
- Parse invoices, receipts
- Extract contact info
- HTML parsing

## Prerequisites

1. Enable Gmail API in Google Cloud Console
2. Create OAuth 2.0 credentials
3. Download credentials.json
4. Generate tokens.json (run once with authentication)

## Configuration

```bash
export GMAIL_CREDENTIALS_PATH="/path/to/credentials.json"
export GMAIL_TOKEN_PATH="/path/to/tokens.json"
```

Or place credentials in default locations:
- `~/.credentials/gmail-credentials.json`
- `~/.credentials/gmail-token.json`

## Usage

### Send Email
```python
from gmail_enhanced import GmailClient

gmail = GmailClient()

# Simple email
gmail.send(
    to="recipient@example.com",
    subject="Hello",
    body="Email content"
)

# With attachment
gmail.send(
    to="recipient@example.com",
    subject="Report",
    body="Please find the report attached",
    attachments=["report.pdf"]
)
```

### Advanced Search
```python
# Complex queries
results = gmail.search(
    query="from:boss@company.com",
    label="INBOX",
    after="2024/01/01",
    has_attachments=True
)

# Search with OR
results = gmail.search_or([
    "subject:urgent",
    "label:important"
])
```

### Label Management
```python
# Create label
label = gmail.create_label("Projects/Work/Q1", color="#4A90E2")

# Get label stats
stats = gmail.get_label_stats("INBOX")

# Apply labels
gmail.add_labels(["Label1", "Label2"], message_ids)
```

### Attachment Handling
```python
# Download attachments from search results
attachments = gmail.search_attachments(
    query="subject:invoice",
    save_dir="./downloads"
)

# Upload attachment
gmail.send(
    to="recipient@example.com",
    subject="File",
    attachments=["/path/to/file.pdf"]
)
```

### Auto-categorization
```python
# Create rule
gmail.add_rule(
    name="Categorize invoices",
    query="subject:invoice has:attachment",
    add_labels=["Processed/Invoices"]
)

# Run rules
gmail.process_rules()
```

## API Reference

### Core Methods
| Method | Description |
|--------|-------------|
| `send(to, subject, body, attachments, cc, bcc)` | Send email |
| `search(query, max_results, label)` | Search emails |
| `get_message(msg_id, format)` | Get email details |
| `delete_message(msg_id)` | Move to trash |
| `archive_message(msg_id)` | Archive email |

### Label Methods
| Method | Description |
|--------|-------------|
| `create_label(name, color)` | Create label |
| `rename_label(old_name, new_name)` | Rename label |
| `delete_label(name)` | Delete label |
| `get_labels()` | List all labels |
| `get_label_stats(label)` | Get label statistics |

### Attachment Methods
| Method | Description |
|--------|-------------|
| `download_attachment(msg_id, attachment_id, save_path)` | Download attachment |
| `search_attachments(query, save_dir)` | Search and download |
| `get_attachment_info(msg_id)` | List attachments |

### Automation Methods
| Method | Description |
|--------|-------------|
| `add_rule(name, query, actions)` | Create processing rule |
| `process_rules()` | Run all rules |
| `create_template(name, subject, body)` | Create email template |
| `send_template(template_name, to, variables)` | Send using template |

### Parsing Methods
| Method | Description |
|--------|-------------|
| `parse_email(msg_id)` | Extract structured data |
| `extract_invoice(msg_id)` | Parse invoice data |
| `extract_contacts(msg_id)` | Extract email addresses |

## Email Query Syntax

```
Basic:
  from:user@example.com
  to:user@example.com
  subject:keyword
  "exact phrase"

Filters:
  after:2024/01/01
  before:2024/12/31
  older_than:7d
  newer_than:2h

Flags:
  has:attachment
  has:drive
  is:unread
  is:starred
  is:important

Labels:
  label:INBOX
  label:Work

Combinations:
  from:boss AND subject:urgent
  (from:alice OR from:bob) AND is:unread
```

## Error Handling

Common errors:
- `invalid_credentials`: Re-authenticate
- `rate_limit`: Wait and retry
- `not_found`: Message ID invalid
- `permission_denied`: Check scopes

## Scopes Required

```
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.labels
https://www.googleapis.com/auth/gmail.modify
```

## Links

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google Cloud Console](https://console.cloud.google.com)
- [OAuth Setup Guide](https://developers.google.com/gmail/api/quickstart/python)
