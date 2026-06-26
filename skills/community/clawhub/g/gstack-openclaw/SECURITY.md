# Security Policy | 安全策略

## 概述

gstack-openclaw 是一个**纯文档型技能（Documentation-only Skill）**，仅通过 AI 角色提示词（prompts）提供工程最佳实践指导。

> **2026-04-10 更新**: 已移除 `install.sh` 脚本，以完全满足 ClawHub "documentation-only" 分类要求。

## 安全声明

### ✅ 本技能**不会**执行以下操作：

- 访问外部 API 或网络服务
- 读取或修改用户文件系统（除 OpenClaw 标准工具外）
- 执行系统命令或脚本
- 收集、存储或传输用户数据
- 要求 API Key、Token 或任何凭证
- 安装额外软件或依赖

### ✅ 本技能**仅**执行以下操作：

- 通过 AI 对话提供工程指导
- 使用 OpenClaw 标准工具（如文件读取、浏览器控制等，需用户授权）
- 生成代码、文档和建议

## 外部服务说明

本技能在对话中可能提及以下外部服务，但**仅用于指导目的**，不直接调用：

| 服务类型 | 示例 | 用途 |
|---------|------|------|
| 代码托管 | GitHub, GitLab | 指导 PR 管理、CI/CD 配置 |
| 云服务 | AWS, 阿里云, Vercel | 指导部署策略 |
| 监控工具 | Datadog, Grafana | 指导监控配置 |
| 设计工具 | Figma, Sketch | 指导设计评审方法 |

**重要**：这些服务的实际调用需要用户：
1. 自行配置相应的 API 凭证
2. 在 OpenClaw 中单独安装对应的 Skill
3. 明确授权工具使用

## 安装方式

本技能**无任何安装脚本**，符合 "documentation-only" 安全分类。

### ✅ 推荐安装方式

```bash
clawhub install openclaw/gstack
```

### ✅ 手动安装

```bash
mkdir -p ~/.openclaw/skills/gstack
cp SKILL.md ~/.openclaw/skills/gstack/
```

### 📋 历史说明

> **v2.5.10 之前版本** 曾包含一个可选的 `install.sh` 脚本（仅执行 `mkdir` 和 `cp` 命令）。
> 为避免 ClawHub 检测器的误报，该脚本已在 v2.5.10 版本中移除。
> 
> 移除 install.sh **不影响任何功能**，因为：
> - 推荐安装方式 `clawhub install` 不依赖该脚本
> - 手动安装只需一行 `cp` 命令
> - 该脚本从未是必需组件

## 报告安全问题

如果您发现任何安全问题，请通过以下方式报告：

1. **GitHub Issues**: https://github.com/openclaw/gstack-openclaw/issues
2. **标记为 Security 类型**：我们会优先处理

## 安全更新历史

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-04-10 | v2.5.10 | 移除 install.sh，完全满足 "documentation-only" 分类 |
| 2026-04-10 | v2.5.9 | 增强 install.sh 安全说明（后移除） |
| 2026-04-09 | v2.5.6 | 添加 SECURITY.md，增强透明度声明 |

## 审计信息

- **最后审计日期**: 2026-04-10
- **审计方式**: 手动代码审查
- **审计结果**: ✅ 无安全问题，纯文档型技能
- **ClawHub 扫描状态**: 等待重新扫描（已移除所有可执行文件）

---

**本技能遵循 OpenClaw 安全最佳实践，致力于提供透明、可信的 AI 辅助工程服务。**
