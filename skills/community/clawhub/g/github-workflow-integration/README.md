# GitHub 工作流集成 / GitHub Workflow Integration

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> `github-workflow-integration` v1.0.0 · LGD-Powered Dev-Productivity Family · Zero-dependency

**中文**：纯 stdlib 包装 GitHub REST API——开 PR / 列 PR / 查 commit status / Git Data API 推单文件。令牌从 `GITHUB_TOKEN` 环境变量读取，零存储零回显。用 PAT 不用 OAuth；`--dry-run` 先演练。rc=0 成功 / rc=1 API 错 / rc=2 用法或令牌缺失。

**EN**: Pure-stdlib wrapper over the GitHub REST API — open/list PRs, query commit status, push a single file via Git Data API. Token read from `GITHUB_TOKEN` env at call time, never stored or echoed. PAT auth, no OAuth flow; `--dry-run` to preview. rc=0 ok / rc=1 API error / rc=2 usage or missing token.

## Setup / 前置
Mint a classic PAT on github.com → Settings → Developer settings → Personal access tokens, tick `repo`, then:
```bash
export GITHUB_TOKEN=ghp_xxx
```

## Usage / 用法
```bash
python scripts/gh_workflow.py pr list --repo owner/repo
python scripts/gh_workflow.py pr create --repo owner/repo --title "Fix" --head fix --base main --dry-run
python scripts/gh_workflow.py status --repo owner/repo --ref main
```

## OAuth boundary / OAuth 边界
This skill uses a **PAT from env**, not OAuth. Gmail/Calendar/Notion/Slack OAuth integrations are **not** provided — recorded as an open gap, not a half-product.
本技能用**环境变量里的 PAT**，不是 OAuth。Gmail/Calendar/Notion/Slack 等需 OAuth 同意页的集成**不**提供——记为开放缺口，不做半成品。

## Disclaimer / 免责
Write ops change remote state; confirm target repo/branch/message before dropping --dry-run. / 写操作改远端状态，去 --dry-run 前请确认目标。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
生产参考部署 (production reference, self-reported) : 无
                    ← 非认证、非背书、非监管认可
代码许可 (code license) : 本包代码 MIT
引用格式 (cite as)      : 本资产无 DOI
```
