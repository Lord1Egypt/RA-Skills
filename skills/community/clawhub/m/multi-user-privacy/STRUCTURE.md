# Multi-User Privacy 技能 - 最终目录结构

> **版本**: v0.9.0  
> **更新时间**: 2026-03-12 12:20  
> **位置**: `~/.openclaw/skills/multi-user-privacy/`

---

## 📁 完整目录结构

```
multi-user-privacy/
│
├── 📦 核心模块
│   ├── privacy-guard.js              # 隐私检查器（核心）
│   ├── gateway-hook.js               # Gateway 集成（自动创建子代理）
│   ├── sensitive-word-loader.js      # 敏感词词库加载器
│   ├── sensitive-word-manager.js     # 敏感词管理工具
│   └── sensitive-words.txt           # 敏感词词库（用户可编辑）
│
├── 🤖 子代理管理
│   ├── subagent-integration.js       # 子代理集成
│   ├── auto-mount.js                 # 自动挂载脚本
│   ├── auto-create-subagents.sh      # 自动创建脚本
│   └── .router-db.json               # 路由器数据库
│
├── 💰 配额管理
│   ├── quota-manager/
│   │   ├── quota_manager.py          # Python 配额管理器
│   │   └── test_quota_manager.py     # Python 测试套件
│   ├── scripts/
│   │   └── quota-manager.js          # Node.js 配额管理 CLI
│   └── .quota-db.json                # 配额数据库
│
├── 📊 监控系统
│   ├── monitoring/
│   │   ├── monitor.js                # 监控核心
│   │   ├── alert-config.json         # 告警配置
│   │   ├── install.sh                # 安装脚本
│   │   ├── start.sh                  # 启动脚本
│   │   └── openclaw-monitor.service  # systemd 服务
│   └── gateway-watchdog/
│       └── gateway-watchdog.js       # Gateway 监控守护
│
├── 🌐 Web 管理界面
│   └── web-admin/
│       ├── server.js                 # 后端服务器
│       ├── index.html                # 前端界面 (31KB)
│       ├── scripts/
│       │   ├── start.sh              # 启动脚本
│       │   └── test.js               # 测试脚本
│       └── README.md                 # 使用说明
│
├── 💾 Session 管理
│   ├── session-persistence/
│   │   ├── session-manager.js        # Session 管理器
│   │   ├── session-templates.js      # Session 模板
│   │   ├── test-session-persistence.js # 测试套件
│   │   └── README.md                 # 模块说明
│   └── config/session-templates/
│       └── templates-config.json     # 模板配置
│
├── 🔄 自动扩缩容
│   └── auto-scaling/
│       ├── session-autoscaler.js     # 核心模块 (19KB)
│       ├── autoscaler-config.json    # 配置文件
│       ├── start-autoscaler.js       # 服务管理脚本
│       ├── demo-autoscaler.js        # 演示脚本
│       ├── start.sh                  # Shell 包装脚本
│       ├── README.md                 # 使用文档 (14KB)
│       └── IMPLEMENTATION_REPORT.md  # 实现报告 (13KB)
│
├── 📚 文档
│   ├── docs/
│   │   ├── SENSITIVE_WORDS_GUIDE.md  # 敏感词使用指南
│   │   ├── 高级配额管理系统.md        # 高级配额文档
│   │   ├── session-templates.md      # Session 模板文档
│   │   ├── PROJECT_SUMMARY.md        # 项目总结 (22.6KB)
│   │   └── ...                       # 其他文档
│   ├── README.md                     # 技能说明
│   ├── README_COMPLETE.md            # 完整功能文档 (新增)
│   ├── SKILL.md                      # 技能定义 (v0.9.0)
│   ├── QUICK_START.md                # 快速入门
│   ├── IMPLEMENTATION_SUMMARY.md     # 实现总结
│   ├── IMPLEMENTATION_STATUS.md      # 实现状态
│   ├── QUOTA_ENABLE_SUMMARY.md       # 配额启用总结
│   ├── QUOTA_VERIFICATION.md         # 配额验证清单
│   ├── ROADMAP.md                    # 路线图
│   └── STATUS.md                     # 当前状态
│
├── 🧪 测试
│   ├── test-auto-create.js           # 自动创建测试
│   ├── test-quota.js                 # 配额测试
│   └── test-session-persistence.js   # Session 持久化测试
│
├── ⚙️ 配置
│   ├── .multi-user-config.json       # 多用户配置
│   ├── .user-context.json            # 用户上下文
│   ├── .projects-config.json         # 项目配置
│   ├── .router-db.json               # 路由器数据库
│   ├── .quota-db.json                # 配额数据库
│   └── .pending-sessions.json        # Pending 队列
│
└── 📜 版本历史
    ├── CHANGELOG_v0.6.0.md
    ├── CHANGELOG_v0.7.0.md
    ├── UPGRADE_v0.4.0.md
    └── ...
```

---

## 🎯 模块说明

### 核心模块（必须）
- **privacy-guard.js** - 隐私检查核心，所有消息都经过这里
- **sensitive-word-loader.js** - 敏感词词库加载和检查
- **gateway-hook.js** - Gateway 消息拦截和子代理自动创建

### 子代理管理（必须）
- **subagent-integration.js** - 子代理集成和配额框架
- **auto-create-subagents.sh** - 定时检查并创建 pending 子代理

### 配额管理（可选但推荐）
- **quota-manager/** - Python 高级配额管理（VIP/组配额/借用）
- **scripts/quota-manager.js** - Node.js 快速配额管理 CLI

### 监控系统（推荐）
- **monitoring/** - 实时监控和飞书告警
- **gateway-watchdog/** - Gateway 健康监控

### Web 管理界面（可选）
- **web-admin/** - Web 管理后台，可视化管理所有功能

### Session 管理（必须）
- **session-persistence/** - Session 持久化和模板系统

### 自动扩缩容（可选）
- **auto-scaling/** - Session 负载监控和自动扩缩容

---

## 📊 统计信息

| 类别 | 数量 | 代码量 |
|------|------|--------|
| **核心模块** | 5 文件 | ~50KB |
| **子代理管理** | 4 文件 | ~30KB |
| **配额管理** | 4 文件 | ~50KB |
| **监控系统** | 5 文件 | ~20KB |
| **Web 管理界面** | 3 文件 | ~50KB |
| **Session 管理** | 5 文件 | ~50KB |
| **自动扩缩容** | 7 文件 | ~40KB |
| **文档** | 20+ 文件 | ~150KB |
| **配置** | 7 文件 | ~5KB |
| **测试** | 3 文件 | ~30KB |
| **总计** | **60+ 文件** | **~475KB** |

---

## 🚀 快速开始

### 1. 查看敏感词词库
```bash
cd ~/.openclaw/skills/multi-user-privacy
node sensitive-word-loader.js list
```

### 2. 启动监控
```bash
cd monitoring
./start.sh start
```

### 3. 启动 Web 管理界面
```bash
cd web-admin
node server.js
# 访问 http://localhost:3456
```

### 4. 启动自动扩缩容
```bash
cd auto-scaling
./start.sh start
```

### 5. 管理配额
```bash
# Node.js CLI
node scripts/quota-manager.js list

# Python 高级功能
python3 quota-manager/quota_manager.py -a check -u user_001
```

---

## 📋 模块依赖关系

```
┌─────────────────────────────────────────────────────┐
│                  Gateway 消息输入                    │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              privacy-guard.js (核心)                 │
│   - 身份识别                                         │
│   - 敏感词检查                                        │
│   - 隐私检查                                         │
└────────────┬────────────────────┬────────────────────┘
             │                    │
             ▼                    ▼
    ┌─────────────────┐  ┌─────────────────┐
    │ gateway-hook.js │  │ monitoring/     │
    │ - 自动创建子代理 │  │ - 状态监控      │
    │ - 消息路由      │  │ - 告警通知      │
    └────────┬────────┘  └─────────────────┘
             │
             ▼
    ┌─────────────────────────────────────────┐
    │        subagent-integration.js          │
    │   - 配额检查                             │
    │   - Session 管理                         │
    └────┬──────────────────┬─────────────────┘
         │                  │
         ▼                  ▼
┌─────────────────┐ ┌──────────────────────┐
│ session-        │ │ quota-manager/       │
│ persistence/    │ │ - 配额管理           │
│ - 持久化        │ │ - 组配额             │
│ - 模板          │ │ - 借用               │
└─────────────────┘ └──────────────────────┘
         │
         ▼
┌─────────────────┐
│ auto-scaling/   │
│ - 负载监控      │
│ - 自动扩缩容    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ web-admin/      │
│ - 可视化管理    │
│ - 统计图表      │
└─────────────────┘
```

---

## ✅ 整合说明

**web-admin**、**session-persistence**、**auto-scaling** 等都是 **multi-user-privacy 技能的子模块**，不是独立技能。

**原因**：
1. 它们都服务于多用户管理系统
2. 共享相同的配置和数据库
3. 通过 privacy-guard.js 统一入口
4. 统一版本管理（v0.9.0）

**优势**：
- ✅ 单一技能，统一管理
- ✅ 模块化设计，可按需启用
- ✅ 共享配置，减少冗余
- ✅ 统一文档，易于维护

---

**技能位置**: `~/.openclaw/skills/multi-user-privacy/`  
**版本**: v0.9.0  
**最后更新**: 2026-03-12 12:20
