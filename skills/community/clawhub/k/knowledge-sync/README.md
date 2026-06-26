# Knowledge Sync Skill

> 知识库同步机制 - 实时文件同步和 Git 备份

## 📦 发布说明

**版本**: 1.0  
**发布日期**: 2026-03-15  
**许可**: MIT  
**作者**: 虾球 🦐

## 🎯 功能特性

- ✅ **实时同步** - inotifywait 监听，3-10 秒延迟
- ✅ **Git 备份** - 每 5 分钟 push，每小时 pull
- ✅ **多端一致** - 服务器→坚果云→Mac Obsidian
- ✅ **systemd 服务** - 24/7 守护进程

## 📁 包含文件

```
knowledge-sync/
├── SKILL.md
├── README.md
├── scripts/
│   ├── sync-realtime.sh
│   ├── git-auto-push.sh
│   └── git-auto-pull.sh
└── docs/
    ├── QUICKSTART.md
    └── sync-guide.md
```

## 🚀 安装方法

```bash
clawhub install knowledge-sync
```

## 💡 使用场景

### 1. 实时同步

```bash
systemctl --user enable sync-realtime.service
systemctl --user start sync-realtime.service
```

### 2. Git 备份

```bash
*/5 * * * * /path/to/git-auto-push.sh
0 * * * * cd /path/to/workspace && git pull
```

## 📊 同步架构

```
服务器 → 坚果云 (3-10 秒) → Gitee (5 分钟) → Mac (5 分钟)
```

## 📝 更新日志

### v1.0 (2026-03-15)

- ✅ 初始版本发布

---

**维护者**: 虾球 🦐  
**许可**: MIT
