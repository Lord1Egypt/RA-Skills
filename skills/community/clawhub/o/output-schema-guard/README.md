# output-schema-guard · 结构化输出校验护栏 / Output Schema Guard

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

Treat model JSON as *untrusted external input*. Validate required fields · types · enums · nesting against a schema before it ever reaches your code; on failure emit an actionable fix hint (`{field, expected, got, hint}`) instead of a raw crash. Ships a zero-dependency `schema_guard.py`.

### Why it beats "just json.loads() and hope"

| Pain | This skill |
|---|---|
| LLM drops a required field → downstream None crash | Required-field gate fails *before* business code |
| Type drifts str↔int | Type check returns expected vs got |
| Enum out of range | Whitelist enum enforcement |
| "Works once, breaks next time" | Deterministic contract, not luck |

### What's inside

- `SKILL.md` — 4-dimension schema check + 2-step flow + schema example + iron rule
- `scripts/schema_guard.py` — zero-dependency CLI: validate JSON/text against a schema JSON, emit per-field pass/fail + fix hint

```bash
python scripts/schema_guard.py --schema schema.json --text '{"name":"x","status":"pending"}'
python scripts/schema_guard.py --schema schema.json --file out.jsonl --json
```

### Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| pydantic (python only) | No language-agnostic, no fix-hint for re-prompt |
| JSON Schema libs | Heavy, no LLM retry-gate pattern |
| "try/except json.loads" | Catches nothing semantic |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `context-engineering` and `skill-quality-gate`.

## 中文

把模型 JSON 当不可信外部输入：进代码前用 schema 卡必填·类型·枚举·嵌套，失败吐可执行修复提示（`{field, expected, got, hint}`）而非裸崩。附零依赖 `schema_guard.py`。

### 为什么比「json.loads 然后听天由命」强

| 痛点 | 本技能 |
|---|---|
| LLM 少给必填字段 → 下游 None 崩溃 | 必填字段门禁在业务代码之前拦截 |
| 类型 str/int 漂移 | 类型检查返回期望 vs 实际 |
| 枚举越界 | 白名单枚举强制 |
| "这次能跑、下次就挂" | 确定性契约，不靠运气 |

### 里面有什么

- `SKILL.md` — 四维 schema 校验 + 两步流程 + schema 示例 + 铁律
- `scripts/schema_guard.py` — 零依赖 CLI：按 schema JSON 校验 JSON/文本，逐字段通过/失败 + 修复提示

```bash
python scripts/schema_guard.py --schema schema.json --text '{"name":"x","status":"pending"}'
python scripts/schema_guard.py --schema schema.json --file out.jsonl --json
```

### 与同类对比

| 工具 | 本技能补的缺口 |
|---|---|
| pydantic（仅 Python） | 语言无关、给重提示修复建议 |
| JSON Schema 库 | 轻量、带 LLM 重试门禁模式 |
| "try/except json.loads" | 抓不住任何语义问题 |

理论根基：**LGD 三律**（有籍 · 有证 · 有门禁）。与 `context-engineering`、`skill-quality-gate` 配套。

---

© 2026 SynomosAI. All rights reserved.

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
