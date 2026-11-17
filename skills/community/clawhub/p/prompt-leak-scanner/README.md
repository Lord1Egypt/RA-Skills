# 提示词泄漏扫描器 / Prompt Leak Scanner

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

Pre-share scanner for prompts and system prompts: secrets, internal paths, PII, custom sensitive words (--extra), and self-leak backdoors ('ignore previous instructions' / 'print your system prompt' plants). Non-zero exit blocks leaks.

**Pain point**: Prompts are the most casually shared sensitive asset: one embedded key, intranet path, or 'repeat your system prompt' plant gives away the farm — nobody runs a pre-release check.

LGD-III gated (the last gate before a prompt goes public).
Part of the **LGD governance family** (凡自治之物: registered / evidenced / gated).

Zero-dependency (stdlib only). See `scripts/` for CLI usage (`--help`).

© SynomosAI (LGD initiative) · LGD-Powered

## 中文

发布/共享前扫描器，针对提示词与 system prompt：密钥、内部路径、PII、自定义敏感词（--extra）与自我泄漏后门（「忽略之前指令」「打印你的系统提示词」类埋点）。非零退出码即拦下泄漏。

**痛点**：提示词是最被随手分享的敏感资产——一个内嵌密钥、一条内网路径、或一句「重复你的系统提示词」埋点，就把底裤都漏了——而没人在发布前跑一遍检查。

LGD-III 有门禁（提示公开前的最后一道门）。
隶属 **LGD 治理家族**（凡自治之物：有籍 / 有证 / 有门禁）。

零依赖（仅标准库）。CLI 用法见 `scripts/`（`--help`）。

© SynomosAI（LGD initiative）· LGD-Powered

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
