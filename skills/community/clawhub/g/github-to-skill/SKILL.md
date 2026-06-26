---
name: github-to-skill
version: 2.0.1
description: GitHub 项目转 OpenClaw 技能参考指南 - 提供转换流程说明（纯文档，无可执行代码）
license: MIT-0
metadata:
    skill-author: OpenClaw Community
    created: 2026-03-27
    updated: 2026-03-31
    type: documentation
---

# GitHub 项目转 OpenClaw 技能参考指南

**GitHub to OpenClaw Skill Conversion Reference Guide**

---

## ⚠️ 重要说明 / Important Notice

**本技能为纯文档指南，不包含任何可执行代码。**

**This skill is documentation-only, containing no executable code.**

- 📚 仅提供转换流程参考说明 / Provides conversion process reference
- 🔒 无代码执行风险 / No code execution risk
- 🎯 用户自行决定如何操作 / User decides how to operate
- ✅ 所有步骤需用户确认执行 / All steps require user confirmation

---

## 📖 概述 / Overview

本指南提供将 GitHub 项目转换为 OpenClaw 技能的**参考流程**，帮助用户理解转换过程中需要考虑的各个环节。

This guide provides a **reference process** for converting GitHub projects to OpenClaw skills, helping users understand the considerations involved.

**适用场景 / Use Cases:**
- 发现优秀的 GitHub 项目想复用到 OpenClaw / Find great GitHub projects to reuse in OpenClaw
- 学习如何封装开源代码为技能 / Learn how to package open-source code as skills
- 理解 OpenClaw 技能结构 / Understand OpenClaw skill structure

---

## 📋 转换流程参考 / Conversion Process Reference

### 阶段 1：项目评估 / Project Evaluation

**考虑因素 / Considerations:**

| 因素 / Factor | 说明 / Description |
|--------------|-------------------|
| 许可证 / License | 确认是否允许复用（MIT/Apache/BSD 通常可以）/ Verify reuse is allowed |
| 项目规模 / Project size | 评估转换工作量 / Estimate conversion effort |
| 依赖复杂度 / Dependency complexity | 评估依赖安装难度 / Assess dependency installation difficulty |
| 代码质量 / Code quality | 检查代码是否规范 / Check code quality |

---

### 阶段 2：文件分析 / File Analysis

**需要识别的文件类型 / File Types to Identify:**

| 类别 / Category | 文件示例 / Examples | 用途 / Purpose |
|----------------|-------------------|---------------|
| 技能定义 / Skill definition | SKILL.md | OpenClaw 技能必需文件 / Required for OpenClaw |
| 入口文件 / Entry point | index.js, main.py | 程序入口 / Program entry |
| 依赖配置 / Dependency config | package.json, requirements.txt | 依赖声明 / Dependency declaration |
| 文档 / Documentation | README.md | 使用说明 / Usage instructions |
| 源代码 / Source code | src/, lib/, *.js, *.py | 功能实现 / Functionality |

**需要排除的文件 / Files to Exclude:**

| 文件 / File | 原因 / Reason |
|------------|--------------|
| .env | 可能包含敏感信息 / May contain sensitive info |
| *.key, *.pem | 密钥文件 / Key files |
| node_modules/ | 依赖包目录 / Dependencies directory |
| .git/ | 版本控制 / Version control |

---

### 阶段 3：技能结构创建 / Skill Structure Creation

**参考目录结构 / Reference Directory Structure:**

```
新技能目录/
├── SKILL.md          # 技能定义（必需）/ Skill definition (required)
├── package.json      # Node.js 项目元数据 / Node.js metadata
├── README.md         # 使用说明 / Usage instructions
├── index.js          # 入口文件（如适用）/ Entry point (if applicable)
└── src/              # 源代码目录 / Source code directory
```

---

### 阶段 4：依赖处理 / Dependency Handling

**常见依赖类型 / Common Dependency Types:**

| 类型 / Type | 配置文件 / Config File | 安装方式参考 / Installation Reference |
|------------|----------------------|-------------------------------------|
| Python | requirements.txt | `pip install -r requirements.txt` |
| Node.js | package.json | `npm install` |

**⚠️ 注意事项 / Notes:**
- 检查依赖是否可信 / Verify dependencies are trusted
- 评估依赖冲突风险 / Assess dependency conflict risks
- 考虑使用虚拟环境 / Consider using virtual environments

---

### 阶段 5：测试验证 / Testing and Verification

**验证步骤参考 / Verification Steps Reference:**

1. **检查技能识别 / Check skill recognition**
   - 确认 SKILL.md 格式正确 / Verify SKILL.md format
   - 重启 OpenClaw 查看技能列表 / Restart OpenClaw and check skill list

2. **功能测试 / Functionality testing**
   - 测试基本功能 / Test basic functionality
   - 检查是否有错误 / Check for errors

3. **依赖验证 / Dependency verification**
   - 确认依赖已安装 / Verify dependencies installed
   - 测试导入是否正常 / Test imports work correctly

---

## 🔒 安全考虑 / Security Considerations

### 敏感文件处理 / Sensitive File Handling

**不应包含的文件 / Files to Exclude:**

| 文件模式 / Pattern | 原因 / Reason |
|-------------------|--------------|
| .env | 环境变量（可能含 API Key）/ Environment vars |
| *.key, *.pem, *.crt | 加密密钥 / Encryption keys |
| credentials | 凭据 / Credentials |
| secrets | 机密信息 / Secrets |

### 许可证合规 / License Compliance

**常见许可证 / Common Licenses:**

| 许可证 / License | 是否可用 / Usable | 注意事项 / Notes |
|-----------------|------------------|-----------------|
| MIT | ✅ 是 / Yes | 保留版权声明 / Retain copyright notice |
| Apache-2.0 | ✅ 是 / Yes | 包含专利授权 / Includes patent grant |
| BSD | ✅ 是 / Yes | 类似 MIT / Similar to MIT |
| GPL | ⚠️ 注意 / Caution | 衍生作品需开源 / Derivatives must be open |
| 专有 / Proprietary | ❌ 否 / No | 禁止复用 / Reuse prohibited |

---

## 📝 SKILL.md 模板参考 / SKILL.md Template Reference

```markdown
---
name: 技能名
version: 1.0.0
description: 技能功能描述
license: MIT
metadata:
    skill-author: 作者名
    source: GitHub 仓库链接（如适用）
---

# 技能名称

## 功能说明
（描述技能的功能和用途）

## 使用方式
（说明如何使用）

## 依赖
（列出需要的包）
```

---

## ❓ 常见问题参考 / FAQ Reference

### Q: 如何确定项目是否有 SKILL.md？
**A:** 检查项目根目录。如没有，需创建新的 SKILL.md 文件。

### Q: 复制代码是否违反许可证？
**A:** 取决于原项目许可证。MIT/Apache/BSD 通常允许复用，GPL 要求衍生作品开源。

### Q: 如何处理依赖冲突？
**A:** 考虑使用虚拟环境（Python）或本地 node_modules（Node.js）隔离依赖。

### Q: 技能创建后不显示怎么办？
**A:** 检查 SKILL.md 格式是否正确，重启 OpenClaw，查看日志。

---

## 📄 版本历史 / Version History

| 版本 / Version | 日期 / Date | 更新内容 / Changes |
|---------------|-------------|-------------------|
| 2.0.1 | 2026-03-31 | 纯文档指南，移除所有可执行命令 / Documentation-only, removed all executable commands |
| 2.0.0 | 2026-03-31 | 改为纯文档技能 / Converted to documentation-only |
| 1.0.6 | 2026-03-27 | 初始版本（含可执行代码）/ Initial release (with executable code) |

---

## 🔗 相关资源 / Related Resources

- [OpenClaw 技能规范](https://agentskills.io/specification)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [ClawHub 技能市场](https://clawhub.ai)
- [GitHub](https://github.com)

---

**作者 / Author:** OpenClaw Community  
**更新日期 / Updated:** 2026-03-31  
**版本 / Version:** 2.0.1  
**类型 / Type:** 纯文档参考指南 / Documentation-Only Reference Guide
