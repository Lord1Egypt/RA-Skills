# openclaw-memory-auto

> Automatic memory archiving for OpenClaw. Works for everyone.

## Features

- **Zero Configuration**: Works out of the box with smart defaults
- **Cross-Platform**: Pure TypeScript, runs on Windows/Mac/Linux
- **Universal**: Language-agnostic keywords, customizable to your workflow
- **Non-Intrusive**: Runs on startup or cron, no manual work needed
- **Respectful**: Only archives what matters, not every chat

## Installation

```bash
npm install openclaw-memory-auto
```

## Quick Start

Add to your `openclaw.config.js`:

```javascript
import memoryAuto from 'openclaw-memory-auto';

export default {
  plugins: [memoryAuto]
};
```

That's it! The plugin will:
- ✅ On every agent startup, archive yesterday's chat
- ✅ Highlight key moments using smart keyword matching
- ✅ Store daily logs in `memory/YYYY-MM-DD.md`
- ✅ Prepare prompts for AI-assisted MEMORY.md updates

## Configuration (Optional)

Customize behavior in `openclaw.config.js`:

```javascript
import memoryAuto from 'openclaw-memory-auto';

export default {
  plugins: [memoryAuto],
  
  memoryAuto: {
    // Add your own keywords (case-insensitive)
    keywords: [
      '任务', '部署', 'API', 'token', 'OpenClaw',
      'task', 'deploy', 'config', 'password', 'secret'
    ],
    
    // Custom paths (relative to workspace)
    paths: {
      memoryDir: 'memory',
      logsDir: 'logs'
    },
    
    // Schedule settings
    schedule: {
      archiveHour: 9,      // 9 AM local time
      checkOnStartup: true // always check on startup
    },
    
    // Enable AI refinement (beta)
    refine: {
      enabled: true,
      model: 'stepfun/step-3.5-flash:free',
      prompt: `Extract long-term memories from today's log.`
    }
  }
};
```

## How It Works

1. **On Startup**: Plugin checks if yesterday's daily log exists
2. **If Missing**: Scans all transcript files (`agents/*/sessions/*.jsonl`)
3. **Time Filter**: Extracts only yesterday's messages (local timezone aware)
4. **Highlighting**: Matches messages against your keyword list
5. **Archive**: Writes `memory/YYYY-MM-DD.md` with summary and highlights
6. **Refine** (optional): Calls AI to update `MEMORY.md` with structured memory

## File Structure

After running:

```
workspace/
├── memory/
│   ├── 2026-03-11.md      # Auto-generated daily log
│   └── .2026-03-11.archived  # Marker (prevents re-archive)
├── logs/
│   ├── memory-archive.log
│   └── last_refine_prompt.txt  # For AI refinement
└── MEMORY.md              # Your long-term memory (manually or auto-updated)
```

## Custom Keywords

Add to your config:

```javascript
memoryAuto: {
  keywords: [
    // Defaults already included - just add yours
    '项目名', '客户', '截止日期',
    'project', 'client', 'deadline'
  ]
}
```

Keywords are case-insensitive and support Unicode (中文, emoji, etc.).

## AI Refinement

Enable in config to automatically update `MEMORY.md`:

```javascript
memoryAuto: {
  refine: {
    enabled: true,
    model: 'stepfun/step-3.5-turbo:free',
    prompt: `Extract: skills learned, project milestones, user preferences, important data, inside jokes.`
  }
}
```

The AI will append structured sections to `MEMORY.md` daily.

## FAQ

**Q: Does it archive everything?**  
A: No. Only messages containing your keywords (default: 30+ common terms). This keeps logs meaningful and privacy-friendly.

**Q: Where are transcripts stored?**  
A: OpenClaw automatically saves sessions to `agents/*/sessions/*.jsonl`. The plugin reads these.

**Q: Can I run on a schedule instead of startup?**  
A: Yes. Use OpenClaw's heartbeat cron:
```javascript
agents: {
  defaults: {
    heartbeat: {
      tasks: [{
        name: 'memory-auto-archive',
        cron: '0 9 * * *', // daily 9 AM
        command: 'npx openclaw-memory-auto --archive'
      }]
    }
  }
}
```

**Q: I have multiple agents. Will it work?**  
A: Yes. Scans all `agents/*/sessions/` directories.

## Development

```bash
git clone https://github.com/openclaw-plugins/memory-auto.git
cd memory-auto
npm install
npm run build
```

## License

MIT - Free for personal and commercial use.

## Contributing

PRs welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

---

**Made with 🦞 by the OpenClaw Community**
