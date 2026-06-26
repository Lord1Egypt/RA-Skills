# OpenClaw Knowledge Base Index

This index lists main categories and key documents from OpenClaw official docs. The full knowledge base is in `assets/default-snapshot.json`.

## How to Use

1. Find relevant category below based on user's issue
2. Load the document using: `JSON.parse(read('assets/default-snapshot.json')).pages[slug]`

## Document Categories

### 🔧 Configuration & Core
| Document | Slug | Description |
|----------|------|-------------|
| Configure | 4d8dc153 | Interactive config wizard |
| Config | 618dc813 | Config management commands |
| Agents | da8f37ca | Agent management |
| Auth Credential Semantics | c35ad50f | Auth credential semantics |

### 📱 Channels
| Document | Slug | Description |
|----------|------|-------------|
| Channels Overview | 6569d3b4 | Channels overview |
| WhatsApp | d09047a0 | WhatsApp Web integration |
| Telegram | d423ce29 | Telegram Bot API |
| Discord | a024b6ce | Discord Bot |
| Feishu | 90a33c43 | Feishu/Lark integration |
| Slack | b6515af4 | Slack Socket Mode |
| Signal | 02cd55ea | Signal CLI integration |
| iMessage | e75baa37 | iMessage integration |
| Group Messages | 008888be | Group message handling |
| Groups | 0bfb808e | Group permissions config |
| Channel Routing | a99b0ed8 | Message routing rules |
| Pairing | 919c126f | Pairing mechanism |

### ⚡ Automation
| Document | Slug | Description |
|----------|------|-------------|
| Cron Jobs | b239629c | Scheduled task execution |
| Cron Vs Heartbeat | e3051492 | Cron vs heartbeat comparison |
| Webhook | 5f6424ab | Webhook endpoints |
| Hooks | 66ed303 | Event-driven scripts |
| Poll | bd2804e1 | Poll functionality |
| Troubleshooting | a632126a | Automation troubleshooting |

### 🔍 Search & Tools
| Document | Slug | Description |
|----------|------|-------------|
| Brave Search | 3d8923e4 | Web search config |
| Browser | 30ca8912 | Browser control |

### 🛠️ CLI Commands
| Document | Slug | Description |
|----------|------|-------------|
| Approvals | 9704f115 | Exec approval management |
| Channels CLI | 05d32796 | Channel account management |
| Completion | 5747e039 | Shell completion |
| ACP | c08dd32a | ACP bridge |

## Diagnostic-Related Docs

### Group Message Issues
- `008888be` - Group Messages
- `0bfb808e` - Groups
- `a99b0ed8` - Channel Routing

### Auth Issues
- `c35ad50f` - Auth Credential Semantics
- `87e3285b` - Auth Monitoring
- `919c126f` - Pairing

### Automation Issues
- `a632126a` - Troubleshooting (Automation)
- `b239629c` - Cron Jobs
- `e3051492` - Cron Vs Heartbeat

### Channel Connection Issues
- `092023ff` - Troubleshooting (Channels)
- Channel-specific docs (WhatsApp, Telegram, etc.)
