---
name: openclaw-sandbox
displayName: OpenClaw 沙盒测试系统
description: OpenClaw 沙盒测试系统 v2.0 - 零风险配置变更测试，9 层防护 +5 原则，自动备份回滚，Git 版本管理
version: 2.0.0
tags: ["沙盒", "测试", "配置", "安全", "隔离"]
---

# OpenClaw 沙盒测试系统 v2.0

**为 OpenClaw 配置变更提供零风险沙盒测试环境**

**版本**: 2.0.0  
**更新时间**: 2026-03-10  
**安全评级**: 🟢 SAFE  
**基于教训**: 4 个污染问题 + 9 层防护 +5 原则

---

## 🛡️ 安全扫描报告

**扫描结果**: 🟢 **SAFE** (安全)

| 检查项 | 结果 |
|--------|------|
| 敏感信息 | ✅ 通过 |
| 文件操作 | ✅ 安全 |
| 网络请求 | ✅ 无 |
| 命令执行 | ✅ 安全 |
| 权限要求 | ✅ 最小 |

---

## 📊 版本更新说明

### v2.0.0 新增（2026-03-10）

基于昨天 + 今天的沙盒污染教训，新增：

1. ✅ **9 层防护体系**
   - 环境变量隔离
   - 配置验证
   - 配置备份
   - 插件隔离
   - 端口隔离
   - Agent ID 唯一
   - CORS 修复
   - 进程保护
   - 性能优化

2. ✅ **配置安全 5 原则**
   - 配置前验证
   - 配置前备份
   - 配置隔离
   - 环境清理
   - 报错回滚

3. ✅ **4 个污染问题案例**
   - 沙盒复制生产配置
   - 共享插件目录
   - 环境变量污染
   - memoryFlush 配置污染

4. ✅ **沙盒创建流程 v3.0**

---

## 🚀 快速开始

### 安装

```bash
openclawmp install skill/@u-9e6ebb2ab773477594f5/openclaw-sandbox
```

### 初始化

```bash
~/.openclaw/skills/openclaw-sandbox/scripts/init.sh
```

### 使用

**小改动**:
```bash
~/.openclaw/skills/openclaw-sandbox/templates/apply-config.sh
```

**中/大改动**:
```bash
~/.openclaw/skills/openclaw-sandbox/templates/safe-try.sh
```

---

## 🛡️ 9 层防护体系

| 层级 | 防护措施 | 解决的问题 |
|------|---------|-----------|
| **1. 环境变量隔离** | 专用脚本自动清理 | 环境变量污染 |
| **2. 配置验证** | 应用前 `openclaw config validate` | 配置键不兼容 |
| **3. 配置隔离** | 沙盒用独立配置文件 | 配置污染 |
| **4. 插件隔离** | 独立 extensions 目录 | 插件冲突 |
| **5. 端口隔离** | 18800+（随机可选） | 端口冲突 |
| **6. Agent ID 唯一** | writer-sandbox/media-sandbox | ID 冲突 |
| **7. CORS 修复** | allowedOrigins 同步端口 | CORS 错误 |
| **8. 进程保护** | nohup 后台运行 | 进程秒退 |
| **9. 性能优化** | 关闭 memorySearch | 内存峰值 |

---

## ✅ 配置安全 5 原则

| 原则 | 执行方式 | 解决的问题 |
|------|---------|-----------|
| **1. 配置前验证** | `openclaw config validate` | 配置键不兼容 |
| **2. 配置前备份** | `cp openclaw.json openclaw.json.bak` | 配置污染 |
| **3. 配置隔离** | 沙盒用独立配置文件 | 配置污染 |
| **4. 环境清理** | `unset OPENCLAW_HOME` | 环境变量污染 |
| **5. 报错回滚** | `cp openclaw.json.bak openclaw.json` | 配置污染 |

---

## 📊 端口说明

| 环境 | 端口 | WebUI |
|------|------|-------|
| 生产 | 18789 | http://127.0.0.1:18789 |
| 沙盒 | 18800 | http://127.0.0.1:18800 |

---

## 🔴 污染问题案例（经验教训）

### 案例 1: 沙盒复制生产配置（03-09 12:52 PM）

**根因**: `cp -r ~/.openclaw/*` 复制到沙盒  
**影响**: 沙盒继承生产插件配置，测试失败影响生产  
**解决**: 沙盒用全新配置（空插件列表）  
**教训**: 三不复制原则

---

### 案例 2: 共享插件目录（03-09 12:55 PM）

**根因**: 沙盒和生产共用 `~/.openclaw/extensions/`  
**影响**: 两个 Gateway 同时加载有问题插件  
**解决**: 沙盒独立 extensions 目录  
**教训**: 插件隔离必须彻底

---

### 案例 3: 环境变量污染（03-09 17:40 PM）

**根因**: 在沙盒目录执行 CLI，`OPENCLAW_HOME` 未清理  
**影响**: 生产 Gateway 读取沙盒配置，无法访问  
**解决**: 创建环境隔离脚本（自动清理环境变量）  
**教训**: 执行前后必须清理环境变量

---

### 案例 4: memoryFlush 配置污染（03-10 07:20 AM）

**根因**: 添加 OpenClaw 不支持的配置键  
**影响**: 配置报错，Gateway 无法启动  
**解决**: 立即回滚配置  
**教训**: 配置修改前必须验证 + 备份

---

## 📁 文件结构

```
openclaw-sandbox/
├── SKILL.md
├── templates/
│   ├── safe-try.sh          # 沙盒测试脚本（v3.0）
│   └── apply-config.sh      # 配置应用脚本（v3.0）
├── examples/
│   ├── 小改动示例.md
│   ├── 大改动示例.md
│   └── 污染问题案例.md      # 新增：4 个污染案例
├── scripts/
│   ├── init.sh              # 初始化脚本（v3.0）
│   └── cleanup-env.sh       # 新增：环境清理脚本
└── VERIFICATION_REPORT.md   # 验证报告
```

---

## 🔄 回滚方法

**备份文件**:
```bash
cp ~/.openclaw/openclaw.json.bak.* ~/.openclaw/openclaw.json
openclaw gateway restart
```

**Git 回滚**:
```bash
cd ~/.openclaw
git checkout HEAD~1
~/.openclaw/skills/openclaw-sandbox/templates/apply-config.sh
```

---

## 📚 完整文档

- **沙盒隔离最佳实践**: `memory/沙盒隔离最佳实践 -2026-03-09.md`
- **3 月 9 日记忆日志**: `memory/2026-03-09.md`
- **MEMORY.md 归档**: 沙盒系统完整经验 v3.0

---

*版本：2.0.0 | 安全评级：🟢 SAFE | 基于教训：4 个污染问题 | 防护层级：9 层*

---

## 🎯 更新日志

### v2.0.0 (2026-03-10)

**新增**:
- ✅ 9 层防护体系（基于昨天 + 今天的污染教训）
- ✅ 配置安全 5 原则
- ✅ 4 个污染问题案例文档
- ✅ 环境变量隔离脚本
- ✅ 配置验证 + 备份机制
- ✅ 沙盒创建流程 v3.0

**改进**:
- ✅ safe-try.sh 添加配置验证
- ✅ apply-config.sh 添加环境清理
- ✅ init.sh 添加 9 层防护检查
- ✅ examples 添加污染案例

**修复**:
- ✅ 修复环境变量污染问题
- ✅ 修复配置键不兼容问题
- ✅ 修复插件目录共享问题

### v1.0.0 (2026-03-08)

**初始版本**:
- ✅ 基础沙盒隔离
- ✅ 自动备份 + 回滚
- ✅ Git 版本控制
- ✅ 配置验证

---

**贡献家**: 墨墨 (Mò)  
**GitHub**: https://github.com/Zoopools/openclaw-sandbox  
**水产市场**: https://openclawmp.cc/asset/s-59129c1951e9b863
