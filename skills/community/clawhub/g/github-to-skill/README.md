# GitHub 项目转 OpenClaw 技能参考指南

**纯文档技能 - 提供转换流程参考说明**

**Documentation-Only Skill - Provides conversion process reference**

---

## ⚠️ 重要说明 / Important Notice

**本技能为纯文档指南，不包含任何自动化工具或可执行代码。**

**This skill is documentation-only, containing no automation tools or executable code.**

- 📚 仅提供转换流程参考 / Provides conversion process reference only
- 🔒 无自动执行功能 / No automation features
- 🎯 用户自行操作所有步骤 / User performs all steps manually
- ✅ 所有决定需用户确认 / All decisions require user confirmation

---

## 📖 用途 / Purpose

**中文：** 本指南帮助理解将 GitHub 项目转换为 OpenClaw 技能时需要考虑的各个环节，提供系统化的参考流程。

**English:** This guide helps understand the considerations involved in converting GitHub projects to OpenClaw skills, providing a systematic reference process.

**适用场景 / Use Cases:**
- 学习如何封装开源代码为 OpenClaw 技能 / Learn how to package open-source code as OpenClaw skills
- 理解 OpenClaw 技能结构和规范 / Understand OpenClaw skill structure and standards
- 参考转换流程中的注意事项 / Reference considerations in conversion process

---

## 📋 转换流程参考 / Conversion Process Reference

### 阶段 1：项目评估 / Project Evaluation

**评估因素 / Evaluation Factors:**

| 因素 / Factor | 说明 / Description |
|--------------|-------------------|
| 许可证检查 / License check | 确认是否允许复用（MIT/Apache/BSD 通常可以）/ Verify reuse is allowed |
| 项目规模 / Project size | 评估工作量 / Estimate effort |
| 依赖复杂度 / Dependency complexity | 评估依赖安装难度 / Assess dependency difficulty |
| 代码质量 / Code quality | 检查代码规范性 / Check code quality |

---

### 阶段 2：文件分析 / File Analysis

**识别关键文件 / Identify Key Files:**

| 类别 / Category | 文件示例 / Examples |
|----------------|-------------------|
| 技能定义 / Skill definition | SKILL.md |
| 入口文件 / Entry point | index.js, main.py |
| 依赖配置 / Dependency config | package.json, requirements.txt |
| 文档 / Documentation | README.md |
| 源代码 / Source code | src/, lib/, *.js, *.py |

**排除敏感文件 / Exclude Sensitive Files:**

| 文件 / File | 原因 / Reason |
|------------|--------------|
| .env | 可能含 API Key / May contain API keys |
| *.key, *.pem | 密钥文件 / Key files |
| credentials | 凭据 / Credentials |

---

### 阶段 3：技能创建 / Skill Creation

**参考结构 / Reference Structure:**

```
新技能目录/
├── SKILL.md          # 技能定义（必需）
├── package.json      # Node.js 元数据
├── README.md         # 使用说明
├── index.js          # 入口文件（如适用）
└── src/              # 源代码目录
```

---

### 阶段 4：依赖处理 / Dependency Handling

**依赖类型参考 / Dependency Types Reference:**

| 类型 / Type | 配置文件 / Config | 安装参考 / Installation Reference |
|------------|------------------|----------------------------------|
| Python | requirements.txt | pip install -r requirements.txt |
| Node.js | package.json | npm install |

**⚠️ 注意 / Notes:**
- 检查依赖可信度 / Verify dependency trustworthiness
- 评估冲突风险 / Assess conflict risks
- 考虑隔离环境 / Consider isolated environments

---

### 阶段 5：验证 / Verification

**验证步骤参考 / Verification Steps Reference:**

1. **技能识别检查 / Skill recognition check**
   - 确认 SKILL.md 格式 / Verify SKILL.md format
   - 重启 OpenClaw / Restart OpenClaw

2. **功能测试 / Functionality test**
   - 测试基本功能 / Test basic functionality
   - 检查错误 / Check for errors

3. **依赖验证 / Dependency verification**
   - 确认依赖安装 / Verify dependencies installed
   - 测试导入 / Test imports

---

## 🔒 安全考虑 / Security Considerations

### 许可证合规 / License Compliance

| 许可证 / License | 是否可用 / Usable | 注意事项 / Notes |
|-----------------|------------------|-----------------|
| MIT | ✅ 是 / Yes | 保留版权声明 / Retain copyright |
| Apache-2.0 | ✅ 是 / Yes | 含专利授权 / Includes patent grant |
| BSD | ✅ 是 / Yes | 类似 MIT / Similar to MIT |
| GPL | ⚠️ 注意 / Caution | 衍生作品需开源 / Derivatives must be open |
| 专有 / Proprietary | ❌ 否 / No | 禁止复用 / Reuse prohibited |

---

## 📝 SKILL.md 模板 / SKILL.md Template

```markdown
---
name: 技能名
version: 1.0.0
description: 技能功能描述
license: MIT
metadata:
    skill-author: 作者名
    source: GitHub 仓库链接
---

# 技能名称

## 功能说明
（描述功能）

## 使用方式
（说明使用方法）

## 依赖
（列出需要的包）
```

---

## ❓ 常见问题 / FAQ

### Q: 如何确定项目是否可以转换？
**A:** 检查许可证。MIT/Apache/BSD 通常允许，GPL 需开源衍生作品，专有许可证禁止。

### Q: 转换后技能不显示怎么办？
**A:** 检查 SKILL.md 格式，重启 OpenClaw，查看日志。

### Q: 如何处理依赖冲突？
**A:** 使用虚拟环境（Python）或本地 node_modules（Node.js）隔离。

---

## 📄 版本历史 / Version History

| 版本 / Version | 日期 / Date | 更新内容 / Changes |
|---------------|-------------|-------------------|
| 2.0.1 | 2026-03-31 | 纯文档参考指南，移除所有自动化描述 / Documentation-only reference guide, removed all automation claims |
| 2.0.0 | 2026-03-31 | 改为纯文档技能 / Converted to documentation-only |
| 1.x | 2026-03-27 | 历史版本（已弃用）/ Historical versions (deprecated) |

---

## 🔗 相关资源 / Related Resources

- [OpenClaw 技能规范](https://agentskills.io/specification)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [ClawHub 技能市场](https://clawhub.ai)

---

**作者 / Author:** OpenClaw Community  
**更新日期 / Updated:** 2026-03-31  
**版本 / Version:** 2.0.1  
**类型 / Type:** 纯文档参考指南 / Documentation-Only Reference Guide

**⚠️ 声明 / Disclaimer:** 本指南仅供参考，所有操作需用户自行决定和执行。/ This guide is for reference only; all operations are at user's discretion.
