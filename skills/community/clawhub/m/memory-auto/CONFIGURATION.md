# Configuration Guide

## Full Configuration Reference

Place inside your `openclaw.config.js`:

```javascript
import memoryAuto from 'openclaw-memory-auto';

export default {
  plugins: [memoryAuto],
  
  memoryAuto: {
    // ──────────────────────────────────────
    // Keywords (case-insensitive, Unicode)
    // ──────────────────────────────────────
    keywords: [
      // Work terms (Chinese)
      '任务', '记得', '记住', '重要', '明天', '计划',
      '问题', '修复', '部署', '安装', '配置', '设置',
      'API', 'token', '密钥', '密码', '账号', '错误', '失败',
      // Work terms (English)
      'task', 'remember', 'important', 'tomorrow', 'plan',
      'issue', 'bug', 'fix', 'deploy', 'install', 'config',
      'password', 'api', 'token', 'key', 'secret', 'error',
      // OpenClaw-specific
      'OpenClaw', '龙虾', 'plugin', '脚本', '命令', '运行'
    ],
    
    // ──────────────────────────────────────
    // File Paths (relative to workspace)
    // ──────────────────────────────────────
    paths: {
      memoryDir: 'memory',     // daily logs go here
      logsDir: 'logs',         // logs and prompts
      markerSuffix: '.archived' // marker filename suffix
    },
    
    // ──────────────────────────────────────
    // Scheduling
    // ──────────────────────────────────────
    schedule: {
      archiveHour: 9,       // Run at 9 AM local time (cron)
      checkOnStartup: true  // Also check whenever agent starts
    },
    
    // ──────────────────────────────────────
    // Templates (Mustache-style placeholders)
    // ──────────────────────────────────────
    templates: {
      dailyLog: `# {date} Work Log

## Summary
User: {userCount}
Assistant: {assistantCount}

### Highlights
{highlights}

---
Auto-archived by openclaw-memory-auto
Refine needed: {refinePrompt}
`,
      memoryUpdate: `## [Auto] {date}
{summary}

---`
    },
    
    // ──────────────────────────────────────
    // AI Refinement (Beta)
    // ──────────────────────────────────────
    refine: {
      enabled: false, // Set true to enable auto MEMORY.md updates
      model: 'stepfun/step-3.5-flash:free',
      prompt: `Analyze the daily work log and extract long-term memories.

Return JSON with these keys (arrays of strings):
- skills: new abilities learned
- projects: project milestones
- preferences: user habits/preferences discovered
- data: important configs, passwords, tokens (be careful!)
- memes: inside jokes, nicknames, special terms

Be concise and factual.`
    }
  }
};
```

## Keyword Matching

- Case-insensitive: `Task` matches `task`
- Substring match: `install` matches `installation`
- Unicode safe: `任务` matches `任务`, `任务管理`
- Empty keywords → no highlights (still creates daily log)

## Path Resolution

All paths are relative to your OpenClaw **workspace** directory.

Default:
```
workspace/
├── memory/        ← daily logs
├── logs/          ← internal logs
└── MEMORY.md      ← long-term (manual or updated by refine)
```

## Disabling Features

To turn off startup check (only use cron):

```javascript
memoryAuto: {
  schedule: {
    checkOnStartup: false
  }
}
```

To disable refinement entirely:

```javascript
memoryAuto: {
  refine: {
    enabled: false
  }
}
```
