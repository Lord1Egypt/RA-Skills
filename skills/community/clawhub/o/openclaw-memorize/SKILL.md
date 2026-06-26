---
name: openclaw-memorize
description: Simple memory management for OpenClaw. Save, retrieve, and search important information. Store facts, decisions, preferences, and anything you want to remember across sessions. Use when you need to persist information for future reference.
---

# OpenClaw Memorize

Store and retrieve important information across sessions. Never forget a decision or preference again.

## Installation

```bash
npx clawhub@latest install openclaw-memorize
```

## Usage

```bash
# Save a memory
node ~/.openclaw/skills/openclaw-memorize/memorize.js save "key" "value"

# Retrieve a memory
node ~/.openclaw/skills/openclaw-memorize/memorize.js get "key"

# List all memories
node ~/.openclaw/skills/openclaw-memorize/memorize.js list

# Search memories
node ~/.openclaw/skills/openclaw-memorize/memorize.js search "keyword"

# Delete a memory
node ~/.openclaw/skills/openclaw-memorize/memorize.js delete "key"
```

## Features

- ✅ Save key-value memories
- ✅ Retrieve memories by key
- ✅ Search memory contents
- ✅ List all stored memories
- ✅ Delete unwanted memories
- ✅ Persistent storage in workspace

## Examples

```bash
# Save a decision
node ~/.openclaw/skills/openclaw-memorize/memorize.js save "model-choice" "Use Claude Sonnet 4.6 for code review"

# Save a preference
node ~/.openclaw/skills/openclaw-memorize/memorize.js save "preferred-editor" "Cursor"

# Retrieve a memory
node ~/.openclaw/skills/openclaw-memorize/memorize.js get "model-choice"

# Search memories
node ~/.openclaw/skills/openclaw-memorize/memorize.js search "editor"

# List all memories
node ~/.openclaw/skills/openclaw-memorize/memorize.js list
```

## Use Cases

- 📝 **Project decisions**: Remember important technical choices
- 👤 **User preferences**: Store settings and preferences
- 📊 **Key metrics**: Track important numbers
- 💡 **Ideas**: Capture thoughts for later
- 🔗 **Links**: Save important URLs

## Need Help?

If you need help with OpenClaw:
- 📧 **Installation Service**: ¥99-299
- 🔗 **Landing Page**: https://yang1002378395-cmyk.github.io/openclaw-install-service/

## License

MIT
