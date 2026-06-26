# Memory Auto Archive

> 🤖 OpenClaw universal memory plugin - Never forget important chats

**Automatically archives your daily conversations into structured markdown logs.** Works out of the box for any OpenClaw user, no configuration needed.

---

## ✨ Features

- **Zero Config** - Works immediately with smart defaults
- **Universal** - Language-agnostic, platform-agnostic, user-agnostic
- **Smart Archiving** - Only saves conversations with meaningful keywords
- **Startup Integration** - Runs automatically on every agent start
- **Cron Support** - Also works with scheduled heartbeat tasks
- **Privacy-Focused** - No external APIs, everything stays local
- **Customizable** - Keywords, templates, paths all configurable

---

## 🚀 Quick Start (30 seconds)

### 1. Install

```bash
npm install openclaw-memory-auto
```

### 2. Enable

Add to your `openclaw.config.js`:

```javascript
import memoryAuto from 'openclaw-memory-auto';

export default {
  plugins: [memoryAuto]
};
```

### 3. Done!

Restart OpenClaw. On next startup, yesterday's chat will be automatically archived to `memory/2026-03-11.md`.

---

## 📸 Screenshots

### Before & After

**Before** (no memory):
```
每次启动都像失忆，忘了之前聊过什么...
```

**After** (with Memory Auto):
```
# 2026-03-11 Work Log

## Summary
User: 12
Assistant: 15

### Highlights
- User: 龙虾今天还不支持微信，但听说支持QQ了
- Assistant: 从状态看，目前只配置了飞书通道...
- User: 帮我写一篇小红书文章关于OpenClaw...
```

### File Structure

```
your-workspace/
├── memory/
│   ├── 2026-03-10.md
│   ├── 2026-03-11.md    ← Auto-created
│   └── .2026-03-11.archived
├── logs/
│   └── memory-archive.log
└── MEMORY.md            ← Your long-term memory (manual updates)
```

---

## ⚙️ Configuration (Optional)

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
      archiveHour: 9,       // 9 AM local time
      checkOnStartup: true  // Also check on startup
    },
    
    // Enable AI refinement (beta)
    refine: {
      enabled: true,
      model: 'stepfun/step-3.5-flash:free'
    }
  }
};
```

---

## 🎯 How It Works

1. **On Startup** - Plugin checks if `memory/YYYY-MM-DD.md` exists for yesterday
2. **Transcript Scan** - Reads all `agents/*/sessions/*.jsonl` files
3. **Time Filter** - Extracts only yesterday's messages (timezone-aware)
4. **Keyword Match** - Highlights conversations containing important terms
5. **Archive** - Writes structured daily log with summary
6. **Refine** (optional) - AI analyzes and updates `MEMORY.md`

---

## 📊 Keyword Matching

Keywords are case-insensitive and support Unicode:

```javascript
// Default keywords (30+ terms)
[
  // Chinese work terms
  '任务', '记得', '记住', '重要', '明天', '计划',
  '问题', '修复', '部署', '安装', '配置',
  
  // English work terms
  'task', 'remember', 'important', 'tomorrow',
  'issue', 'fix', 'deploy', 'install', 'config',
  
  // Technical
  'API', 'token', 'password', 'key', 'secret',
  'error', 'success', 'script', 'command'
]
```

Add your domain-specific terms in config.

---

## 💡 Use Cases

- **Personal AI assistant** - Never lose important decisions or preferences
- **Developer workflow** - Track tasks, configs, commands automatically
- **Project management** - Auto-document meetings and planning sessions
- **Learning journal** - Capture skills and insights as you work
- **Team knowledge** - Share archived logs across agents

---

## 📝 FAQ

**Q: Does it archive EVERY message?**  
A: No. Only messages containing keywords (default: 30+ common terms). This keeps logs meaningful and reduces noise.

**Q: Where are transcripts stored?**  
A: OpenClaw automatically saves sessions to `agents/*/sessions/*.jsonl`. The plugin reads these files.

**Q: Can I run on a schedule instead of startup?**  
A: Yes! Use OpenClaw heartbeat cron:

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
A: Absolutely. Scans all `agents/*/sessions/` directories automatically.

**Q: Can I customize the daily log format?**  
A: Yes, via `templates.dailyLog` in config. Mustache-style placeholders: `{date}`, `{userCount}`, `{assistantCount}`, `{highlights}`.

**Q: Is my data sent to external APIs?**  
A: No. All processing is local. Optional AI refinement uses your configured OpenClaw model (local or cloud).

---

## 🛠️ Development

```bash
git clone https://github.com/openclaw-plugins/memory-auto.git
cd memory-auto
npm install
npm test
```

---

## 📄 License

MIT - Free for personal and commercial use.

---

**Made with 🦞 by the OpenClaw Community**

*Keep your memories alive.*
