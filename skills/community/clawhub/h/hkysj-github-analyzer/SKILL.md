---
name: github-analyzer
description: "GitHub 项目分析工具 - 技术栈识别、许可证合规评估、部署方案建议。Analyze GitHub repos for tech stack, license compliance, and deployment options. 用途：商业使用合规检查、技术选型调研、开源依赖尽调。"
metadata:
  openclaw:
    emoji: "🔍"
    author: "hkysj"
    version: "1.0.2"
    requires:
      bins: ["curl", "jq"]
---

# GitHub Analyzer / GitHub 项目分析器

Analyze GitHub repositories and generate comprehensive evaluation reports.
分析 GitHub 仓库，生成完整的评估报告。

---

## Features / 功能特性

| Feature | Description |
|---------|-------------|
| 📊 Project Overview / 项目概览 | Stars, Forks, language, activity, issue status |
| 📜 License Compliance / 许可证合规 | Commercial use, modification rights, copyleft requirements |
| 🔧 Tech Stack Detection / 技术栈识别 | Node.js / Python / Go / Rust / Docker / etc. |
| 🚀 Deployment Guide / 部署建议 | Recommended deployment methods based on project type |
| 📄 Report Export / 报告导出 | Auto-generated Markdown report saved locally |

---

## Usage / 使用方法

```bash
# Analyze a repository / 分析项目
./scripts/analyze_repo.sh owner/repo

# Specify output directory / 指定输出目录
./scripts/analyze_repo.sh owner/repo ~/path/to/reports
```

**Default output directory / 默认输出目录：** `~/Desktop/github-reports/`

---

## License Compliance Reference / 许可证合规参考

| License | Commercial Use<br/>商业使用 | Modification<br/>修改权 | Copyleft<br/>传染性 | Risk Level<br/>风险等级 |
|---------|:--------------------------:|:----------------------:|:-------------------:|:-----------------------:|
| MIT | ✅ Permitted | ✅ Permitted | ❌ None | 🟢 Low / 低 |
| Apache-2.0 | ✅ Permitted | ✅ Permitted | ❌ None | 🟢 Low / 低 |
| BSD-3-Clause | ✅ Permitted | ✅ Permitted | ❌ None | 🟢 Low / 低 |
| GPL-3.0 | ⚠️ With conditions | ✅ Permitted | ✅ Strong | 🔴 High / 高 |
| AGPL-3.0 | ⚠️ With conditions | ✅ Permitted | ✅ Very Strong | 🔴 High / 高 |
| LGPL-3.0 | ✅ Permitted (as library) | ✅ Permitted | ⚠️ Partial | 🟡 Medium / 中 |
| MPL-2.0 | ✅ Permitted | ✅ Permitted | ⚠️ File-level | 🟡 Medium / 中 |
| No License | ❌ Unclear | ❌ Unclear | - | 🔴 High / 高 |

**Note / 说明：** "Commercial Use" refers to the right to use the software in proprietary software products. Always consult the full license text and legal advice when in doubt.
"Commercial Use" 指在专有软件产品中使用该软件的权利。如有疑问，请查阅完整许可证文本并咨询法律意见。

Full reference / 完整对照表： [references/licenses.md](references/licenses.md)

---

## Report Sample / 报告示例

```markdown
# GitHub Repository Analysis Report

## Project Info / 项目信息
| Field | Value |
|-------|-------|
| Repository | owner/repo |
| Stars | 10,000+ |
| License | MIT |
| Risk Level | 🟢 Low |

## License Compliance / 许可证合规
| Check | Result |
|-------|--------|
| Commercial Use / 商业使用 | ✅ Permitted |
| Modification / 修改 | ✅ Permitted |
| Copyleft / 传染性 | ❌ None |

## Deployment / 部署建议
Docker recommended:
docker-compose up -d
```

---

## Resources / 资源

### scripts/
- `analyze_repo.sh` — Main analysis script / 主分析脚本

### references/
- `licenses.md` — Complete open-source license reference / 完整许可证参考

---

**Author / 作者：** hkysj  
**Version / 版本：** 1.0.2  
**Feedback / 反馈：** https://clawhub.com/skills/hkysj-github-analyzer

---

*Respect open-source licenses. Contribute back when possible.*
*尊重开源许可证，尽可能回馈社区。*
