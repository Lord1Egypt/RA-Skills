---
name: openclaw-cfg-safe-edit
description: OpenClaw 配置文件修改前的验证规则。用于在修改 openclaw.json 或任何配置文件之前查询文档确认配置项可用性，避免因 OpenClaw 版本更新导致配置不兼容的问题。
---

# 配置验证规则

## 触发条件

当用户请求修改以下内容时自动触发：
- `openclaw.json`
- `config/*.json`
- 任何 OpenClaw 配置文件

## 验证流程

### 1. 查询本地文档

在修改配置前，先查询文档目录：

```bash
# 列出文档结构
ls /home/root1/.npm-global/lib/node_modules/openclaw/docs

# 搜索相关配置项
grep -r "<配置项名称>" /home/root1/.npm-global/lib/node_modules/openclaw/docs/ --include="*.md"
```

### 2. 查阅配置 schema

查询配置 schema 确认字段定义：

```bash
# 查看配置 schema 目录
ls /home/root1/.npm-global/lib/node_modules/openclaw/docs/cli/

# 或使用 gateway 工具查询 schema
openclaw gateway config.schema.lookup <dot-path>
```

### 3. 验证后再修改

确认配置项：
- 存在于当前版本的文档中
- 用法正确
- 类型匹配

如果文档中没有该配置项：
- 查看在线文档: https://docs.openclaw.ai
- 或检查 OpenClaw 更新日志

## 常见配置项参考

- `gateway.*` - 网关配置
- `plugins.*` - 插件配置
- `channels.*` - 通道配置
- `models.*` - 模型配置
- `storage.*` - 存储配置
