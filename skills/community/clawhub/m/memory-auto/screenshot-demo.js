#!/usr/bin/env node
// screenshot-generator.js
// Generates ASCII/simulated screenshots for documentation

console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                   📸 Memory Auto Archive                     ║
║                     Plugin in Action                          ║
╚═══════════════════════════════════════════════════════════════╝

┌─ BEFORE (Without Plugin) ─────────────────────────────────────┐
│                                                                │
│  User: 龙虾今天还不支持微信吗？                               │
│  Assistant: 目前只配置了飞书通道，没有微信支持               │
│  User: 帮我写个自动化脚本                                     │
│  Assistant: 好的，这是脚本...                                 │
│                                                                │
│  ❌ Next day: "龙虾，昨天我们说啥来着？"                      │
│     (Memory lost, starting from scratch)                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘

┌─ AFTER (With Plugin) ──────────────────────────────────────────┐
│                                                                │
│  ✅ Startup triggers archive                                 │
│     » Checking memory/2026-03-11.md...                      │
│     » Scanning transcripts...                               │
│     » Found 28 messages from yesterday                      │
│     » Extracted 7 highlights                                │
│     » Wrote memory/2026-03-11.md                            │
│                                                                │
│  📄 Generated Daily Log:                                    │
│                                                                │
│  # 2026-03-11 Work Log                                      │
│                                                                │
│  ## Summary                                                 │
│  User: 12                                                   │
│  Assistant: 15                                              │
│                                                                │
│  ## Highlights                                             │
│  • User: 龙虾今天还不支持微信...                            │
│  • Assistant: 从状态看，目前只配置了飞书...                  │
│  • User: 帮我写个小红书文章关于OpenClaw...                  │
│  • Assistant: 已生成三篇笔记...                              │
│                                                                │
│  ---                                                        │
│  Auto-archived by openclaw-memory-auto                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘

┌─ File Structure ──────────────────────────────────────────────┐
│                                                                │
│  workspace/                                                   │
│  ├── memory/                                                 │
│  │   ├── 2026-03-10.md                                       │
│  │   ├── 2026-03-11.md  ← Today's newly archived log       │
│  │   └── .2026-03-11.archived  (marker)                    │
│  ├── logs/                                                   │
│  │   ├── memory-archive.log                                 │
│  │   └── last_refine_prompt.txt                             │
│  ├── MEMORY.md                                               │
│  └── openclaw.config.js                                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘

┌─ Configuration Example ───────────────────────────────────────┐
│                                                                │
│  import memoryAuto from 'openclaw-memory-auto';              │
│                                                                │
│  export default {                                            │
│    plugins: [memoryAuto],                                    │
│    memoryAuto: {                                             │
│      keywords: [                                             │
│        '任务', '部署', 'OpenClaw', '龙虾',                   │
│        'task', 'deploy', 'config', 'password'               │
│      ],                                                      │
│      schedule: { archiveHour: 9 }                           │
│    }                                                         │
│  };                                                          │
│                                                                │
└────────────────────────────────────────────────────────────────┘

┌─ Installation Steps ───────────────────────────────────────────┐
│                                                                │
│  1️⃣  npm install openclaw-memory-auto                       │
│  2️⃣  Add to openclaw.config.js (see above)                 │
│  3️⃣  Restart OpenClaw                                       │
│  4️⃣  Done! ✨                                               │
│                                                                │
│  📦  Standalone usage (no npm):                             │
│      Download standalone-archive.js                         │
│      Add to heartbeat: node standalone-archive.js           │
│                                                                │
└────────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════╗
║  🦞  Universal . Works for everyone. Zero config needed.   ║
╚═══════════════════════════════════════════════════════════════╝
`);
