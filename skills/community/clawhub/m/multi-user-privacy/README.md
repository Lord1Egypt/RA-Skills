# Multi-User Privacy Skill

> **版本**: v0.9.0  
> **作者**: 狗子 🐶  
> **最后更新**: 2026-03-12  
> **GitHub**: https://github.com/lz84/multi-user-privacy

用 Markdown 写公众号文章，像发朋友圈一样简单

---

## 🌟 核心功能

### 1. 多用户隐私保护
- ✅ 自动身份识别（管理员/普通用户）
- ✅ 记忆隔离（每个用户独立记忆空间）
- ✅ 敏感词检查（词库独立配置）
- ✅ 隐私检查（回复前自动检查）

### 2. 子代理路由系统
- ✅ Gateway 自动创建子代理
- ✅ 消息自动路由到对应子代理
- ✅ Pending 队列机制
- ✅ 路由器数据库

### 3. 配额管理系统
- ✅ 按用户类型设置配额（VIP/普通/管理员）
- ✅ 配额继承（组配额）
- ✅ 配额借用（临时增加）
- ✅ 配额报表（导出 CSV）
- ✅ CLI 管理工具

### 4. 监控告警系统
- ✅ 子代理运行状态监控
- ✅ 配额使用情况监控
- ✅ 飞书消息告警
- ✅ 告警阈值配置

### 5. Web 管理界面
- ✅ 查看子代理状态
- ✅ 调整用户配额
- ✅ 查看使用统计
- ✅ 操作日志

### 6. Session 持久化
- ✅ 保存 Session 状态到磁盘
- ✅ 重启后自动恢复
- ✅ 状态迁移（活跃→休眠→归档）

### 7. Session 模板
- ✅ 管理员模板（高配额、完整权限）
- ✅ 普通用户模板（标准配额）
- ✅ 访客模板（低配额、只读）
- ✅ 自定义模板支持

### 8. 自动扩缩容
- ✅ 监控 Session 负载
- ✅ 自动创建新 Session（负载高时）
- ✅ 自动合并 Session（负载低时）
- ✅ 负载均衡

---

## 🚀 快速开始

### 1. 安装技能

```bash
npx clawhub install multi-user-privacy
```

安装位置：`~/.openclaw/skills/multi-user-privacy/`

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

### 5. 管理配额

```bash
# Node.js CLI
node scripts/quota-manager.js list

# Python 高级功能
python3 quota-manager/quota_manager.py -a check -u user_001
```

---

## 📁 目录结构

```
multi-user-privacy/
├── 核心模块
│   ├── privacy-guard.js              # 隐私检查器（核心）
│   ├── gateway-hook.js               # Gateway 集成
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
│   │   ├── quota_manager.py          # Python 配额管理器
│   │   └── test_quota_manager.py     # Python 测试套件
│   ├── scripts/
│   │   └── quota-manager.js          # Node.js 配额管理 CLI
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
│   └── web-admin/
│       ├── server.js                 # 后端服务器
│       ├── index.html                # 前端界面
│       └── scripts/
│           ├── start.sh              # 启动脚本
│           └── test.js               # 测试脚本
│
├── Session 管理
│   ├── session-persistence/
│   │   ├── session-manager.js        # Session 管理器
│   │   ├── session-templates.js      # Session 模板
│   │   └── test-session-persistence.js # 测试套件
│   └── config/session-templates/
│       └── templates-config.json     # 模板配置
│
├── 自动扩缩容
│   └── auto-scaling/
│       ├── session-autoscaler.js     # 核心模块
│       ├── autoscaler-config.json    # 配置文件
│       ├── start-autoscaler.js       # 服务管理脚本
│       └── README.md                 # 使用文档
│
├── 文档
│   ├── docs/
│   │   ├── SENSITIVE_WORDS_GUIDE.md  # 敏感词使用指南
│   │   ├── 高级配额管理系统.md        # 高级配额文档
│   │   ├── session-templates.md      # Session 模板文档
│   │   └── PROJECT_SUMMARY.md        # 项目总结
│   ├── README.md                     # 本文件
│   ├── STRUCTURE.md                  # 目录结构说明
│   └── SKILL.md                      # 技能定义
│
└── 配置
    ├── .multi-user-config.json       # 多用户配置
    ├── .user-context.json            # 用户上下文
    ├── .router-db.json               # 路由器数据库
    └── .quota-db.json                # 配额数据库
```

---

## 🔧 配置说明

### 敏感词词库

**位置**: `sensitive-words.txt`

**格式**:
```
# 类型 | 模式 | 动作 | 说明
regex|/ou_[a-f0-9]{32}/g|block|飞书账号 ID 检测
keyword|管理员|alert|管理员角色提及
```

**管理命令**:
```bash
# 列出所有规则
node sensitive-word-loader.js list

# 添加规则
node sensitive-word-loader.js add regex "/test/g" block "测试规则"

# 测试文本
node sensitive-word-loader.js test "这是测试文本"

# 重新加载
node sensitive-word-loader.js reload
```

### 配额配置

**位置**: `.quota-db.json`

**格式**:
```json
{
  "ou_b96f5424607baf3a0455b55e0f4a2213": {
    "diskQuotaMB": -1,
    "tokenQuota": -1,
    "messageQuota": -1,
    "maxConcurrentSessions": -1,
    "isAdmin": true
  },
  "default": {
    "diskQuotaMB": 100,
    "tokenQuota": 100000,
    "messageQuota": 1000,
    "maxConcurrentSessions": 5,
    "isAdmin": false
  }
}
```

**管理命令**:
```bash
# 查看配额
node scripts/quota-manager.js list

# 设置用户配额
node scripts/quota-manager.js set ou_xxx123 --disk=100 --token=100000 --message=1000

# 重置配额
node scripts/quota-manager.js reset ou_xxx123
```

### 路由器数据库

**位置**: `.router-db.json`

**格式**:
```json
{
  "ou_b96f5424607baf3a0455b55e0f4a2213": {
    "userId": "ou_b96f5424607baf3a0455b55e0f4a2213",
    "userName": "老刘",
    "sessionKey": "7783c42e-e974-490a-9609-607327c4509f",
    "memoryPath": "/memory/sessions/7783c42e-e974-490a-9609-607327c4509f/user.md",
    "status": "active"
  }
}
```

---

## 📊 监控告警

### 启动监控

```bash
cd monitoring
./start.sh start
```

### 查看状态

```bash
./start.sh status
```

### 查看日志

```bash
./start.sh log
```

### 告警配置

**位置**: `monitoring/alert-config.json`

**配置项**:
- 检查间隔：60 秒
- 子代理最大并发数：10
- 子代理最大运行时间：2 小时
- Token/消息/磁盘配额预警阈值：80%
- Gateway 连续失败阈值：3 次

---

## 🌐 Web 管理界面

### 启动

```bash
cd web-admin
node server.js
```

### 访问

http://localhost:3456

### 功能

- 查看所有子代理状态
- 调整用户配额
- 查看使用统计
- 操作日志

---

## 🧪 测试

### 运行测试

```bash
# 敏感词测试
node sensitive-word-loader.js test "测试文本"

# 配额测试
node scripts/test-quota.js

# Session 持久化测试
node session-persistence/test-session-persistence.js

# 自动创建测试
node test-auto-create.js
```

---

## 📚 文档

### 完整文档

- `STRUCTURE.md` - 目录结构说明
- `SKILL.md` - 技能定义
- `docs/SENSITIVE_WORDS_GUIDE.md` - 敏感词使用指南
- `docs/高级配额管理系统.md` - 高级配额文档
- `docs/session-templates.md` - Session 模板文档
- `docs/PROJECT_SUMMARY.md` - 项目总结

### 快速参考

- `QUICK_START.md` - 快速入门
- `README_COMPLETE.md` - 完整功能文档

---

## 🎯 使用场景

### 场景 1: 新用户自动隔离

```
用户首次发送消息 → 自动检测 → 创建子代理 → 路由到子代理
```

### 场景 2: 配额超限处理

```
用户请求 → 配额检查 → 超限拒绝 → 记录日志 → 发送告警
```

### 场景 3: Session 自动扩缩容

```
监控负载 → 负载高 (≥0.8) → 创建新 Session
监控负载 → 负载低 (≤0.3) → 合并 Session
```

### 场景 4: Web 管理

```
访问 Web 界面 → 查看状态 → 调整配额 → 实时生效
```

---

## ❓ 常见问题

### Q1: 如何添加新的敏感词？

```bash
node sensitive-word-loader.js add keyword "敏感词" block "说明"
```

### Q2: 如何查看当前活跃子代理？

```bash
cd web-admin
node server.js
# 访问 http://localhost:3456 查看
```

### Q3: 如何调整用户配额？

```bash
node scripts/quota-manager.js set ou_xxx --disk=100 --token=100000
```

### Q4: 监控告警如何配置？

编辑 `monitoring/alert-config.json`，然后重启监控：
```bash
cd monitoring
./start.sh stop
./start.sh start
```

### Q5: Session 持久化在哪里？

自动启用，无需配置。Session 状态保存在：
- `memory/session-state.json`
- `memory/sessions/{id}/`

---

## 📈 版本历史

### v0.9.0 (2026-03-12)
- ✅ 敏感词词库独立配置
- ✅ Gateway 自动创建子代理
- ✅ 配额管理启用
- ✅ 监控告警系统
- ✅ Web 管理界面
- ✅ Session 持久化
- ✅ Session 模板
- ✅ 高级配额管理
- ✅ 自动扩缩容

### v0.8.2 (2026-03-11)
- ✅ 多用户隐私隔离
- ✅ 子代理手动创建
- ✅ 记忆复制

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**GitHub**: https://github.com/lz84/multi-user-privacy

---

## 📄 许可证

MIT License

---

## 📞 联系方式

- **作者**: 狗子 🐶
- **GitHub**: https://github.com/lz84/multi-user-privacy
- **问题反馈**: GitHub Issues

---

**最后更新**: 2026-03-12 12:53  
**版本**: v0.9.0
