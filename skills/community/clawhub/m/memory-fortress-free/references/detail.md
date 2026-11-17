# 详细参考 - memory-fortress-free

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (text)

```text
┌─────────────────────────────────────────────────────────────────┐
│                      记忆堡垒 (MEMORY FORTRESS)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   热内存     │  │   温存储     │  │   冷存储     │             │
│  │  HOT RAM    │  │  WARM STORE │  │  COLD STORE │             │
│  │             │  │             │  │             │             │
│  │ SESSION-    │  │  向量数据库  │  │  Git-Notes  │             │
│  │  STATE.md   │  │  语义搜索    │  │  知识图谱    │             │
│  │             │  │             │  │             │             │
│  │ (抗压缩     │  │ (语义检索)  │  │ (永久决策)  │             │
│  │  抗重启)    │  │             │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │  MEMORY.md  │  ← 策展长期记忆                 │
│                  │  + 日志目录  │    (人类可读)                  │
│                  └─────────────┘                                │
│                          │                                      │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │  云备份      │  ← 跨设备同步 (可选)           │
│                  │  Cloud Sync │                                │
│                  └─────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 代码示例 (json)

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "local",
    "sources": ["memory"],
    "minScore": 0.3,
    "maxResults": 10
  },
  "plugins": {
    "entries": {
      "memory-manager": {
        "enabled": true,
        "config": {
          "autoCapture": false,
          "autoRecall": true,
          "captureCategories": ["preference", "decision", "fact"],
          "minImportance": 0.7
        }
      }
    }
  }
}
```

## 代码示例 ()

```
workspace/
├── SESSION-STATE.md          # 当前活跃项目
├── MEMORY.md                 # 跨项目通用偏好
└── memory/
    ├── projects/
    │   ├── project-a.md      # 项目A专属记忆
    │   ├── project-b.md      # 项目B专属记忆
    │   └── project-c.md      # 项目C专属记忆
    ├── people/
    │   └── contacts.md       # 联系人信息
    ├── decisions/
    │   └── 2026-01.md        # 决策记录
    └── lessons/
        └── mistakes.md       # 通用经验教训
```

## 代码示例 ()

```
workspace/
├── SESSION-STATE.md          # 当前活跃项目
├── MEMORY.md                 # 跨项目通用偏好
└── memory/
    ├── projects/
    │   ├── project-a.md      # 项目A专属记忆
    │   ├── project-b.md      # 项目B专属记忆
    │   └── project-c.md      # 项目C专属记忆
    ├── people/
    │   └── contacts.md       # 联系人信息
    ├── decisions/
    │   └── 2026-01.md        # 决策记录
    └── lessons/
        └── mistakes.md       # 通用经验教训
```

## 架构总览
```text
┌─────────────────────────────────────────────────────────────────┐
│                      记忆堡垒 (MEMORY FORTRESS)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   热内存     │  │   温存储     │  │   冷存储     │             │
│  │  HOT RAM    │  │  WARM STORE │  │  COLD STORE │             │
│  │             │  │             │  │             │             │
│  │ SESSION-    │  │  向量数据库  │  │  Git-Notes  │             │
│  │  STATE.md   │  │  语义搜索    │  │  知识图谱    │             │
│  │             │  │             │  │             │             │
│  │ (抗压缩     │  │ (语义检索)  │  │ (永久决策)  │             │
│  │  抗重启)    │  │             │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │  MEMORY.md  │  ← 策展长期记忆                 │
│                  │  + 日志目录  │    (人类可读)                  │
│                  └─────────────┘                                │
│                          │                                      │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │  云备份      │  ← 跨设备同步 (可选)           │
│                  │  Cloud Sync │                                │
│                  └─────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```



### 完整搭建（<300秒）
配置Agent平台集成，启用自动记忆管理：

在 `~/.agent/agent-config.json` 中配置：

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "local",
    "sources": ["memory"],
    "minScore": 0.3,
    "maxResults": 10
  },
  "plugins": {
    "entries": {
      "memory-manager": {
        "enabled": true,
        "config": {
          "autoCapture": false,
          "autoRecall": true,
          "captureCategories": ["preference", "decision", "fact"],
          "minImportance": 0.7
        }
      }
    }
  }
}
```



