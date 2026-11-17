---
name: lgd-certify
slug: lgd-certify
display_name: LGD 三律闭环认证（有籍→有证→有门禁）
displayName: LGD 三律闭环认证（有籍→有证→有门禁）
title: LGD 三律闭环认证（有籍→有证→有门禁）
version: 1.1.0
category: ai-agent
platforms: [windows, macos, linux]
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch, WebSearch
description: 当用户要『给 AI 产物发可信护照 / 做三律合规认证 / 生成可挂载徽章』时用。这是把『有籍护照签发 → 有证证据链 → 有门禁签发 → 可挂载徽章』做成闭环的 CLI：register 签发算法护照(三锚一票同源+SHA-256指纹)、evidence 扫六类证据工件链式哈希、gate 三律评审 PASS/FAIL 并签发认证 + medxpert.cn 徽章嵌入码。LGD 三律旗舰执行器，对标调研显示治理生态多为单点工具。触发词：LGD 认证、三律闭环、算法护照、可信徽章、有籍有证有门禁认证、护照签发。
tags: [LGD, 三律闭环, 算法护照, 认证, 徽章, 有籍, 有证, 有门禁, 闭环]
display_name_en: LGD Three-Laws Closed-Loop Certifier
summary: 当用户要『给 AI 产物发可信护照 / 做三律合规认证 / 生成可挂载徽章』时用。
agent_created: true
copyright: SynomosAI
read_when: 
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
---








# LGD 三律闭环认证（有籍→有证→有门禁） / LGD 三律闭环认证（有籍→有证→有门禁）

**lgd-certify** v1.1.0 · LGD-Powered 家族 · 零依赖·确定性输出 · 退出码 rc=0/1/2

![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

## 痛点
当用户要『给 AI 产物发可信护照 / 做三律合规认证 / 生成可挂载徽章』时用。这是把『有籍护照签发 → 有证证据链 → 有门禁签发 → 可挂载徽章』做成闭环的 CLI：register 签发算法护照(三锚一票同源+SHA-256指纹)、evidence 扫六类证据工件链式哈希、gate 三律评审 PASS/FAIL 并签发认证 + medxpert.cn 徽章嵌入码。LGD 三律旗舰执行器，对标调研显示治理生态多为单点工具。触发词：LGD 认证、三律闭环、算法护照、可信徽章、有籍有证有门禁认证、护照签发。

## 能力边界
- 认证结论基于你放入的证据工件，**不替代**监管/法律合规审查。
- 门禁未过（证据未齐）属正常，放齐六类后重跑 `evidence → gate` 即可。
- 不编造：缺工件即标缺失，绝不伪造通过。

## 用法
| 命令 | 律 | 作用 |
|---|---|---|
| `register` | 有籍 REGISTERED | 凡造必登：生成算法护照（schema v1.0 三锚一票同源）+ SHA-256 指纹 |
| `evidence` | 有证 EVIDENCED | 凡所行必有证据：扫描六类证据工件 → 链式哈希证据链（防篡改） |
| `gate` | 有门禁 GATED | 凡演化必经门禁：三律评审 → PASS/FAIL → 签发认证 + 官方徽章嵌入码 |

## 输出示例（真机）
（运行上方 `--help` 查看完整参数；带参运行即得确定性输出）

## 退出码与错误码
- `rc=0` 通过 / `rc=1` 发现问题 / `rc=2` 用法或环境错误

（无预定义错误码常量；失败时以非零 rc + 人类可读错误信息退出，不抛原始栈帧）

## 反模式 FAQ
**Q：LGD 三律闭环认证（有籍→有证→有门禁）能完全自动搞定吗？**
A：不能。本技能是方法论/规程，关键判断与跨技能执行需人工或协同技能确认。

**Q：可以直接当法规/专业意见用吗？**
A：不能。仅作辅助框架，最终以官方最新文本与持证专业意见为准。

## 理论依据
| 命令 | 律 | 作用 |
|---|---|---|
| `register` | 有籍 REGISTERED | 凡造必登：生成算法护照（schema v1.0 三锚一票同源）+ SHA-256 指纹 |
| `evidence` | 有证 EVIDENCED | 凡所行必有证据：扫描六类证据工件 → 链式哈希证据链（防篡改） |
| `gate` | 有门禁 GATED | 凡演化必经门禁：三律评审 → PASS/FAIL → 签发认证 + 官方徽章嵌入码 |

## 免责 / Disclaimer
- 认证结论基于你放入的证据工件，**不替代**监管/法律合规审查。
- 门禁未过（证据未齐）属正常，放齐六类后重跑 `evidence → gate` 即可。
- 不编造：缺工件即标缺失，绝不伪造通过。

---

© SynomosAI · LGD-Powered · [![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)

## 安装与使用矩阵
```bash
# 一键获取（skills CLI）
npx skills@1.7.0 add https://github.com/zhaoxinghua09-cell/agent-skills/tree/v2026.09.28.1/skills/lgd-certify

# 或手动：克隆后拷贝本技能到你的 Agent 技能目录
git clone --branch v2026.09.28.1 --depth 1 https://github.com/zhaoxinghua09-cell/agent-skills.git
# 校验：git -C agent-skills rev-parse HEAD 应与发布标签 v2026.09.28.1 一致
cp -r agent-skills/skills/lgd-certify ~/.workbuddy/skills/
```

| Agent | 技能目录 | 运行示例 |
|---|---|---|
| Claude Code | `~/.claude/skills/lgd-certify/` | 让 Claude 按本技能 SKILL.md 工作流调用脚本 |
| Codex / Cursor / WorkBuddy | 各自 skills 目录 | 同上，SKILL.md 即操作规程 |
| 直接命令行 | 任意位置 | `python scripts/*.py --help`（代码件） |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `lgd_certify.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包 = MIT (see LICENSE)
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `lgd_certify.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-certify
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-certify/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
