# MEMORY.md Manager for OpenClaw

🧠 自动管理长期记忆文件

---

## 快速开始

### 1. 安装

```bash
cd ~/.openclaw/workspace/skills/memory-manager
./install.sh
```

### 2. 初始化

```bash
# 创建 MEMORY.md
./scripts/init-memory.sh
```

### 3. 配置自动更新

```bash
# 已包含在 install.sh 中，自动创建 cron 任务
# 每天午夜 00:00 自动更新
```

---

## 功能

- ✅ 自动创建 MEMORY.md 模板
- ✅ 每日午夜自动更新
- ✅ **智能筛选** - 规则预过滤 + LLM 分析
- ✅ **脱敏检测** - 自动识别 Token/Secret
- ✅ **成本优化** - 无匹配时跳过 LLM 调用

---

## 文件结构

```
memory-manager/
├── SKILL.md
├── README.md
├── install.sh
├── templates/
│   └── MEMORY.md.template
└── scripts/
    ├── init-memory.sh
    └── update-memory.sh
```

---

## 管理命令

```bash
# 查看 cron 任务
openclaw cron list

# 手动触发更新
openclaw cron run --jobId <任务 ID>

# 暂停任务
openclaw cron update --jobId <任务 ID> --enabled false
```

---

## 许可证

MIT
