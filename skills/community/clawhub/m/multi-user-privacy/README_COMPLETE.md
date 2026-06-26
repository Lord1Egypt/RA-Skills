# Multi-User Privacy 技能 - 完整功能目录

> **版本**: v0.9.0  
> **更新时间**: 2026-03-12 12:10  
> **位置**: `~/.openclaw/skills/multi-user-privacy/`

---

## 📁 目录结构

```
multi-user-privacy/
├── 核心模块
│   ├── privacy-guard.js              # 隐私检查器（核心）
│   ├── gateway-hook.js               # Gateway 集成（自动创建子代理）
│   ├── sensitive-word-loader.js      # 敏感词词库加载器
│   ├── sensitive-word-manager.js     # 敏感词管理工具
│   └── sensitive-words.txt           # 敏感词词库（用户可编辑）
│
├── 子代理管理
│   ├── subagent-integration.js       # 子代理集成
│   ├── auto-mount.js                 # 自动挂载脚本
│   ├── auto-create-subagents.sh      # 自动创建脚本
│   └── .router-db.json               # 路由器数据库
│
├── 配额管理
│   ├── quota-manager/
│   │   ├── quota_manager.py          # 配额管理器核心
│   │   └── test_quota_manager.py     # 测试套件
│   ├── scripts/quota-manager.js      # 配额管理 CLI
│   └── .quota-db.json                # 配额数据库
│
├── 监控系统
│   ├── monitoring/
│   │   ├── monitor.js                # 监控核心
│   │   ├── alert-config.json         # 告警配置
│   │   ├── install.sh                # 安装脚本
│   │   └── start.sh                  # 启动脚本
│   └── gateway-watchdog/
│       └── gateway-watchdog.js       # Gateway 监控守护
│
├── Web 管理界面
│   ├── web-admin/
│   │   ├── server.js                 # 后端服务器
│   │   ├── index.html                # 前端界面
│   │   └── scripts/
│   │       ├── start.sh              # 启动脚本
│   │       └── test.js               # 测试脚本
│
├── Session 管理
│   ├── session-persistence/
│   │   ├── session-manager.js        # Session 管理器
│   │   ├── session-templates.js      # Session 模板
│   │   └── test-session-persistence.js # 测试套件
│   └── config/session-templates/
│       └── templates-config.json     # 模板配置
│
├── 文档
│   ├── docs/
│   │   ├── SENSITIVE_WORDS_GUIDE.md  # 敏感词使用指南
│   │   ├── 高级配额管理系统.md        # 高级配额文档
│   │   ├── session-templates.md      # Session 模板文档
│   │   └── PROJECT_SUMMARY.md        # 项目总结
│   ├── README.md                     # 技能说明
│   ├── SKILL.md                      # 技能定义
│   ├── QUICK_START.md                # 快速入门
│   └── IMPLEMENTATION_SUMMARY.md     # 实现总结
│
├── 测试
│   ├── test-auto-create.js           # 自动创建测试
│   ├── test-quota.js                 # 配额测试
│   └── test-session-persistence.js   # Session 持久化测试
│
└── 配置
    ├── .multi-user-config.json       # 多用户配置
    ├── .user-context.json            # 用户上下文
    └── .projects-config.json         # 项目配置
```

---

## 🎯 核心功能模块

### 1. 多用户隐私保护
**文件**: `privacy-guard.js`, `sensitive-word-loader.js`

**功能**:
- ✅ 自动身份识别（管理员/普通用户）
- ✅ 记忆隔离（每个用户独立记忆空间）
- ✅ 敏感词检查（词库独立配置）
- ✅ 隐私检查（回复前自动检查）

**配置**:
- `sensitive-words.txt` - 敏感词词库（用户可编辑）
- `.user-context.json` - 用户上下文

---

### 2. 子代理路由系统
**文件**: `gateway-hook.js`, `subagent-integration.js`

**功能**:
- ✅ Gateway 自动创建子代理
- ✅ 消息自动路由到对应子代理
- ✅ Pending 队列机制
- ✅ 路由器数据库

**配置**:
- `.router-db.json` - 路由器数据库
- `.pending-sessions.json` - Pending 队列

---

### 3. 配额管理系统
**文件**: `quota-manager/quota_manager.py`, `scripts/quota-manager.js`

**功能**:
- ✅ 按用户类型设置配额（VIP/普通/管理员）
- ✅ 配额继承（组配额）
- ✅ 配额借用（临时增加）
- ✅ 配额报表（导出 CSV）
- ✅ CLI 管理工具

**配置**:
- `.quota-db.json` - 配额数据库

**使用**:
```bash
# 查看配额
node scripts/quota-manager.js list

# 设置用户配额
node scripts/quota-manager.js set ou_xxx --disk=100 --token=100000

# Python 高级配额
python3 quota-manager/quota_manager.py -a check -u user_001
```

---

### 4. 监控告警系统
**文件**: `monitoring/monitor.js`

**功能**:
- ✅ 子代理运行状态监控
- ✅ 配额使用情况监控
- ✅ 飞书消息告警
- ✅ 告警阈值配置

**配置**:
- `monitoring/alert-config.json` - 告警阈值

**使用**:
```bash
cd monitoring
./start.sh start    # 启动监控
./start.sh status   # 查看状态
./start.sh log      # 查看日志
```

---

### 5. Web 管理界面
**文件**: `web-admin/server.js`, `web-admin/index.html`

**功能**:
- ✅ 查看子代理状态
- ✅ 调整用户配额
- ✅ 查看使用统计
- ✅ 操作日志

**使用**:
```bash
cd web-admin
node server.js      # 启动服务器
# 访问 http://localhost:3456
```

---

### 6. Session 持久化
**文件**: `session-persistence/session-manager.js`

**功能**:
- ✅ 保存 Session 状态到磁盘
- ✅ 重启后自动恢复
- ✅ 状态迁移（活跃→休眠→归档）

**使用**:
```javascript
const { getSessionManager } = require('./session-persistence/session-manager');
const manager = getSessionManager();
await manager.initialize();
```

---

### 7. Session 模板
**文件**: `session-persistence/session-templates.js`

**功能**:
- ✅ 管理员模板（高配额、完整权限）
- ✅ 普通用户模板（标准配额）
- ✅ 访客模板（低配额、只读）
- ✅ 自定义模板支持

**配置**:
- `config/session-templates/templates-config.json` - 模板配置

---

## 🚀 快速开始

### 1. 安装技能

```bash
npx clawhub install multi-user-privacy
```

### 2. 查看敏感词词库

```bash
cd ~/.openclaw/skills/multi-user-privacy
node sensitive-word-loader.js list
```

### 3. 启动监控

```bash
cd monitoring
./start.sh start
```

### 4. 启动 Web 管理界面

```bash
cd web-admin
node server.js
# 访问 http://localhost:3456
```

---

## 📊 版本历史

### v0.9.0 (2026-03-12)
- ✅ 敏感词词库独立配置
- ✅ Gateway 自动创建子代理
- ✅ 配额管理启用
- ✅ 监控告警系统
- ✅ Web 管理界面
- ✅ Session 持久化
- ✅ Session 模板
- ✅ 高级配额管理

### v0.8.2 (2026-03-11)
- ✅ 多用户隐私隔离
- ✅ 子代理手动创建
- ✅ 记忆复制

---

## 📋 维护命令

```bash
# 敏感词管理
node sensitive-word-loader.js list
node sensitive-word-loader.js add regex "/pattern/g" block "说明"
node sensitive-word-loader.js test "测试文本"

# 配额管理
node scripts/quota-manager.js list
node scripts/quota-manager.js set ou_xxx --disk=100
node scripts/quota-manager.js reset ou_xxx

# 监控
cd monitoring
./start.sh start
./start.sh status

# Web 管理
cd web-admin
node server.js
```

---

**技能位置**: `~/.openclaw/skills/multi-user-privacy/`  
**文档**: `docs/` 目录  
**版本**: v0.9.0
