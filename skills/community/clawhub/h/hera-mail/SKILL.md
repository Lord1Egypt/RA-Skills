---
name: hera-mail
description: HERA system internal email system for agent-to-agent communication. Use when any HERA agent needs to: (1) Check their inbox for new messages, (2) Read specific emails from other agents, (3) Send emails to other agents with optional file attachments (papers, data, images), (4) Manage message status (read/unread). This is the primary communication method between HERA agents.
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "always": true
      }
  }
---

# HERA Mail System

Internal email system for agent-to-agent communication within the HERA research assistant framework.

## Quick Start

### Check Inbox
```bash
python3 {baseDir}/scripts/list_inbox.py <agent-name>
```

### Read a Message
```bash
python3 {baseDir}/scripts/read_mail.py <agent-name> <mail-file.md>
```

### Send a Message
```bash
python3 {baseDir}/scripts/send_mail.py <from-agent> <to-agent> "<subject>" <attachment-paths...>
```

## Agent Names

| Agent | Name for Scripts |
|-------|-----------------|
| Group Leader | `group-leader` |
| Rough Reader | `rough-reader` |
| Intensive Reader | `intensive-reader` |
| Code Guider | `code-guider` |
| Coordinator 1 | `coordinator-1` |
| Coordinator 2 | `coordinator-2` |
| Rough Checker 1 | `rough-checker-1` |
| Rough Checker 2 | `rough-checker-2` |
| Report Writer | `report-writer` |

## Email Format

```markdown
[FROM: agent-name]
[TO: agent-name]
[TIMESTAMP: YYYY-MM-DD HH:MM:SS]
[MAIL-ID: unique-id]
[SUBJECT: subject text]
[STATUS: unread]

---

Message body content here.
No formal greetings needed - be direct and concise.

---
[END]
```

## Attachments

Attachments are stored in:
```
hera-agents/<recipient>/inbox/attachments/<mail-id>/<files>
```

Supported: PDFs, images, data files, code, any file type.

## Workflows

### Workflow 1: Check and Read Messages

1. List inbox: `list_inbox.py <agent-name>`
2. Identify unread messages (marked with `[○]`)
3. Read specific message: `read_mail.py <agent-name> <file.md>`
4. Message automatically marked as read

### Workflow 2: Send Message with Attachment

```bash
# Send paper to Rough Reader
python3 send_mail.py group-leader rough-reader "Review this paper" /path/to/paper.pdf

# Send data visualization to Report Writer
python3 send_mail.py intensive-reader report-writer "Analysis results" /path/to/figure.png /path/to/data.csv
```

### Workflow 3: Interactive Send (with body from stdin)

```bash
cat <<EOF | python3 send_mail.py coordinator-1 code-guider "Code review needed"
Please review the attached code for:
1. Performance issues
2. Memory leaks
3. Best practices

Deadline: EOD
EOF
```

## Message Types

| Type | Sender | Recipient | Purpose |
|------|--------|-----------|---------|
| Task Assignment | Group Leader | Any agent | Assign new work |
| Work Submission | Any agent | Coordinator/Leader | Submit completed work |
| Review Request | Any agent | Rough Checker | Request quality check |
| Information Request | Any agent | Reader agents | Request analysis |
| Data Transfer | Any agent | Any agent | Share files/data |

## Best Practices

1. **Be direct** - No formal greetings, get straight to the point
2. **Clear subjects** - Subject line should summarize the task/request
3. **Attach relevant files** - Include papers, data, code as needed
4. **Check inbox regularly** - Agents should monitor their inbox
5. **Mark important messages** - Use mail ID for reference in future comms

## Directory Structure

```
hera-agents/
├── <agent-name>/
│   ├── inbox/           # Received messages
│   │   ├── *.md         # Mail files
│   │   ├── *.read       # Read markers
│   │   └── attachments/ # Attached files per mail
│   └── outbox/          # Sent message copies
│       └── *.md
└── skills/hera-mail/
    ├── scripts/
    │   ├── list_inbox.py
    │   ├── read_mail.py
    │   └── send_mail.py
    └── references/
```

## Examples

### Example 1: Group Leader assigns task to Rough Reader

```bash
cat <<EOF | python3 send_mail.py group-leader rough-reader "Scan arXiv papers on quantum error correction"
Priority: High
Scope: Last 6 months
Focus: Surface codes, LDPC codes

Deliverable: List of top 10 relevant papers with abstracts
Deadline: 2 hours
EOF
```

### Example 2: Intensive Reader sends analysis to Report Writer

```bash
python3 send_mail.py intensive-reader report-writer "Analysis complete: Quantum Error Correction" \
    /workspace/analysis/summary.md \
    /workspace/analysis/key_findings.csv \
    /workspace/figures/error_rates.png
```

### Example 3: Coordinator requests quality check

```bash
python3 send_mail.py coordinator-1 rough-checker-1 "QC needed: Literature review draft" \
    /workspace/drafts/lit_review_v1.md
```

## Troubleshooting

**Inbox not found**: Ensure agent directory exists under `hera-agents/`

**Mail not delivered**: Check recipient agent name is correct

**Attachment missing**: Verify file path is absolute and file exists

**Permission denied**: Ensure scripts are executable:
```bash
chmod +x /Users/zhaoruiwu/.openclaw/workspace/hera-agents/skills/hera-mail/scripts/*.py
```
