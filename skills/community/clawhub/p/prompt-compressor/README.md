# prompt-compressor · 提示/上下文压缩 / Prompt Compressor

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

Compress by *information density*, not by cutting chars: keep keyword-dense & position-weighted sentences, drop filler/repetition. Runnable `compress_prompt.py` scores sentences and trims to a target ratio while protecting constraints, numbers, and code. Pairs with `context-engineering` (it decides *what* to put in; this decides *how short*).

### Why it beats "just truncate"

| Pain | This skill |
|---|---|
| Truncating loses the key sentence | Density+position scoring keeps constraints |
| Numbers/code get mangled | Structural tokens protected |
| Blind ratio cut | Target-ratio trim from lowest score up |

### What's inside

- `SKILL.md` — 3 principles + 3-step flow + iron rule
- `scripts/compress_prompt.py` — zero-dependency CLI: score & trim sentences to a ratio

```bash
python scripts/compress_prompt.py --text "长文本..." --ratio 0.5
python scripts/compress_prompt.py --file doc.txt --ratio 0.4
```

### Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Manual copy-edit | Slow, subjective | Scored, repeatable |
| Head/tail truncate | Cuts mid-thought | Keeps high-value sentences |
| LLM summarize | Costs a call | Local, free, deterministic |

Theoretical root: **LGD Three Laws** — convergence (drop redundancy). Pairs with `context-engineering`.

## 中文

按信息密度压缩：保留关键词密集/位置靠前的句子，删冗余与复述。附可运行脚本（按密度+位置打分删句），护住约束句/数字/代码。与 `context-engineering` 互补（它管「放什么」，本技能管「压多短」）。

### 为什么比「直接截断」强

| 痛点 | 本技能 |
|---|---|
| 截断把关键句切没了 | 密度+位置打分保住约束句 |
| 数字/代码被弄坏 | 结构 token 保护 |
| 盲目按比例砍 | 从最低分往上按目标比例裁剪 |

### 里面有什么

- `SKILL.md` — 三原则 + 三步流程 + 铁律
- `scripts/compress_prompt.py` — 零依赖 CLI：按打分把句子裁到目标比例

```bash
python scripts/compress_prompt.py --text "长文本..." --ratio 0.5
python scripts/compress_prompt.py --file doc.txt --ratio 0.4
```

### 与同类对比

| 工具 | 它做什么 | 本技能补的缺口 |
|---|---|---|
| 人工改稿 | 慢、主观 | 打分、可重复 |
| 头/尾截断 | 拦腰砍断思路 | 保住高价值句子 |
| LLM 摘要 | 花一次调用 | 本地、免费、确定性 |

理论根基：**LGD 三律**——收敛（删除冗余）。与 `context-engineering` 配套。

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
