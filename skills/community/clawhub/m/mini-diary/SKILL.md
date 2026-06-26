---
name: mini-diary
description: AI-powered minimal diary with smart auto-tagging and optional cloud sync. Perfect for daily journaling, work logs, or project tracking.
allowed-tools: Bash(mini-diary:*)
---

# 📓 Mini Diary Skill

Your AI-powered mini diary. Small footprint, smart features.

## ✨ Features

- **📝 Simple Daily Logging**: Clean Markdown format with date, weather, notes, and todos
- **🏷️ Smart Auto-Tagging**: AI analyzes content and adds relevant tags automatically
- **🔍 Powerful Search**: Search by tags, date, or content with context
- **📊 Basic Statistics**: Tag frequency and completion rate tracking
- **☁️ Cloud Sync Ready**: Optional NextCloud integration with detailed guide
- **🔓 Open Format**: Plain Markdown files - you own your data

## 🚀 Quick Start

### Installation

```bash
# Install via ClawHub
clawhub install mini-diary
```

### Basic Usage

```bash
# Add a note (auto-tagging happens automatically)
mini-diary add "Met with client about P1S delivery"

# Add a todo item (use [ ] for pending, [x] for completed)
# The todo will be added to the current day's todo section
echo "- [ ] Follow up with supplier" >> ~/diary.md
echo "- [x] Submit monthly report" >> ~/diary.md

# Search by tag
mini-diary search --tag "📦"

# Search by date
mini-diary search --date "2024-02-22"

# Search in content
mini-diary search "client meeting"

# View statistics
mini-diary search --stats

# List all available tags
mini-diary search --list-tags
```

## 📁 Diary Format

Mini Diary uses a simple Markdown format:

```markdown
# 📓 My Diary

## 📅 2024-02-22 Thursday

### 📝 Notes

- Met with client about P1S delivery 📦🎋
- Fixed heating issue on X1C printer 🔧🎋
- Submitted monthly invoice 💰

### ✅ Todos

- [ ] Follow up with supplier
- [x] Update inventory spreadsheet
```

## ✅ Managing Todos

### Adding Todos
Since todos are simple Markdown task lists, you can add them directly:

```bash
# Add a pending todo
echo "- [ ] Call client for follow-up" >> ~/diary.md

# Add a completed todo  
echo "- [x] Submit weekly report" >> ~/diary.md

# Add multiple todos
cat >> ~/diary.md << 'EOF'
- [ ] Order more filament
- [x] Backup server data
- [ ] Schedule team meeting
EOF
```

### Todo Best Practices
1. **Start with date**: Ensure you're adding to the correct day's section
2. **Use clear descriptions**: "Call John re: P1S delivery" not just "Call John"
3. **Update status**: Change `[ ]` to `[x]` when completed
4. **Review daily**: Check todos at start/end of each day

### Finding Todos
```bash
# Search for pending todos
grep "\[ \]" ~/diary.md

# Search for completed todos
grep "\[x\]" ~/diary.md

# Count todos by status
grep -c "\[ \]" ~/diary.md  # Pending count
grep -c "\[x\]" ~/diary.md  # Completed count
```

## 🏷️ Auto-Tagging System

The AI automatically adds tags based on content:

| Tag | Meaning | Example Triggers |
|-----|---------|------------------|
| 🏠 | Family | home, family, household |
| 💰 | Finance | invoice, payment, accounting |
| 📦 | Order | order, purchase, stock |
| 🚚 | Shipping | shipping, delivery, logistics |
| 💻 | Tech | software, system, computer |
| 🔧 | Support | repair, fix, issue, problem |
| 🎋 | Bambu | bambu, 3d print, printer |
| 📋 | Form | form, report, data, spreadsheet |
| 📅 | Daily | (default for routine notes) |

## ☁️ NextCloud Integration (Optional)

### Setup

1. Set environment variable:
```bash
export NEXTCLOUD_SYNC_DIR="/path/to/nextcloud/diary"
```

2. Mini Diary will automatically sync to this directory.

### ⚠️ Important Notes

**File Permissions**: NextCloud requires specific file ownership:
```bash
# After copying files to NextCloud directory:
chown www-data:www-data /path/to/diary.md

# Or using Docker:
docker exec nextcloud_app chown www-data:www-data /var/www/html/data/...
```

**Scan Command Required**: NextCloud won't detect changes automatically:
```bash
docker exec nextcloud_app php occ files:scan [username]
```

## ⚙️ Configuration

### Environment Variables

```bash
# Diary file location
export DIARY_FILE="$HOME/my-diary.md"

# NextCloud sync directory
export NEXTCLOUD_SYNC_DIR="/path/to/nextcloud"

# Custom tag definitions (JSON file)
export TAGS_CONFIG="/path/to/tags.json"
```

### Custom Tags

Create a JSON file to define custom tags:

```json
{
  "custom_tags": {
    "project-x": "🚀",
    "urgent": "⚠️",
    "meeting": "👥"
  },
  "rules": {
    "project-x": ["project x", "px", "feature"],
    "urgent": ["urgent", "asap", "important"],
    "meeting": ["meeting", "call", "discussion"]
  }
}
```

## 📊 Advanced Usage

### Weekly Report

```bash
# Generate weekly summary
mini-diary search --date $(date -d "last week" +%Y-%m-%d) --stats
```

### Tag Analysis

```bash
# See most used tags
mini-diary search --stats | grep -A5 "Tag Statistics"
```

### Export Data

```bash
# Export to CSV for analysis
grep "^- " diary.md | sed 's/^- //' > notes.csv
```

## 🔧 Troubleshooting

### Common Issues

1. **Tags not appearing**: Check content keywords match tag rules
2. **NextCloud files not showing**: Did you run the scan command?
3. **Permission errors**: Check file ownership in NextCloud directory
4. **Search not working**: Ensure diary file exists and has content

### Debug Mode

```bash
# Enable debug output
export MINI_DIARY_DEBUG=1
mini-diary add "test note"
```

## 🤝 Contributing

Found a bug? Have a feature request? Contributions welcome!

1. Fork the [repository](https://github.com/PrintXDreams/mini-diary)
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with [OpenClaw](https://openclaw.ai)
- Inspired by real-world need for simple, smart journaling
- Thanks to all contributors and users

---

**Mini Diary** - Because journaling should be simple, smart, and yours.