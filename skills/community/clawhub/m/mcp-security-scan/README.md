# mcp-security-scan · MCP 安全扫描

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

An MCP server is a *third party to audit*. Before connecting, scan its tool list for command-exec / file-write / network-egress / credential-exposure risks, rate each tool and advise least-privilege. Ships a zero-dependency `mcp_scan.py`.

### Why it beats "connect and trust"
| Pain | This skill |
|---|---|
| MCP can run shell | command-exec flagged high |
| Silent data exfil | network-egress flagged |
| Token in tool description | credential-exposure flagged |
| "Just enable all tools" | least privilege, disable extras |

### What's inside
- `SKILL.md` — 4-risk model + 3-step audit flow + hard rules
- `scripts/mcp_scan.py` — zero-dependency CLI: scan a tools.json (name+description), rate risk per tool plus overall advice

```bash
python scripts/mcp_scan.py --tools tools.json
python scripts/mcp_scan.py --tools tools.json --json
```

### Benchmark vs alternatives
| Tool | Gap this fills |
|---|---|
| MCP auth scopes | pre-connect tool-level risk rating |
| Manual read of tools | repeatable lexical scan |
| "It's official" | explicit high-risk flag, not trust |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `tool-call-guard` and `prompt-injection-shield`.

## 中文

把 MCP server 当需审查的第三方：接前扫工具清单的命令执行/文件写/网络外联/凭证暴露四类风险，给评级与最小授权建议。零依赖 `mcp_scan.py`。

### 为什么胜过「接上就信」
| 痛点 | 本技能 |
|---|---|
| MCP 能跑 shell | 命令执行标高危 |
| 静默数据外传 | 网络外联标红 |
| 工具描述里带 token | 凭证暴露标红 |
| 「全部工具开了再说」 | 最小授权，多余禁用 |

### 包内构成
- `SKILL.md` — 四类风险模型 + 三步审计流程 + 铁律
- `scripts/mcp_scan.py` — 零依赖 CLI：扫 tools.json（名称+描述），逐工具评级并给总体建议

```bash
python scripts/mcp_scan.py --tools tools.json
python scripts/mcp_scan.py --tools tools.json --json
```

### 与替代方案的对比
| 工具 | 本技能补的位 |
|---|---|
| MCP 授权域 | 接前工具级风险评级 |
| 人工读工具列表 | 可复现的词法扫描 |
| 「官方的没事」 | 显式高危标记，不靠信任 |

理论根基：**LGD 三律**（有籍·有证·有门禁）。与 `tool-call-guard`、`prompt-injection-shield` 配套。

---

© 2026 SynomosAI. All rights reserved.

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI · China. All rights reserved.
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
