# 残留层 · 英文规则库 (English Residue Rulebook · Grading RL1–RL4)

版本 1.0.0 ｜ 2026-10-11 ｜ 英文叠加包 ｜ 30 条规则

> 本规则库检测**英文 AI 产物**中的残留痕迹。它与 `rules-residue-zh.md` **结构平行**（结构 > 词汇、密度门控、先保护后判定），但词条与模式全部在英文语料上重建，非翻译迁移。
> 当待检产物语言为英文（或中英混合且英文为主体）时加载本包，替代/叠加中文残留规则库。
> 命中是线索，不是判决——每条规则都配「保护边界」，命中后必须回到上下文判断是否真的影响交付。
> 描述症状，**不鉴定作者身份**。

---

## 使用原则（先读这三条）

### 1. 结构 > 词汇
词表会随模型迭代退化，**句法结构与语用功能才是稳定信号**。孤立出现一个 "leverage" 不报；出现 "On one hand… on the other hand" 的对称骨架才报。

### 2. 密度门控（最大的误报杀手）
除非标注「单次即报」，否则一律按**滑动窗口密度**判定：150–200 词窗口内同类命中 ≥3 次才成立。同一簇不重复计数——五处 AI 词只报一条。

### 3. 先保护，后判定
每条规则都有「保护边界」。**保护条件命中时，不报。** 术语、引语、法律表述、作者明确判断、必要的礼貌与免责，一律保留。

---

## 规则分级（超集关系）

| 级别 | 名称 | 含义 | 默认 |
|:--:|---|---|:--:|
| **RL1** | 硬阻断 | 单次命中即报，直接影响可交付性 | ✅ 启用 |
| **RL2** | 高精度 | 结构与短语，高精度 | ✅ 启用 |
| **RL3** | 风格 | 主观风格与密度，场景严格档才启用 | 严格档 |
| **RL4** | 聚合 | 统计型，可能误报 | 偏执档 |

**场景决定启用到哪一级**——见 `scenarios.md`。

---

## 规则冲突与去重（仲裁阶梯）

同一片段常被多条规则同时命中。**只出一条报告项**，其余降级为「附带命中」写进该条的证据行。

### 仲裁四步（依次判断，命中即停）
| 步 | 原则 | 内容 |
|:--:|---|---|
| **1** | **层级优先** | RL1 硬阻断 > RL2 高精度 > RL3 风格 > RL4 聚合 |
| **2** | **危害优先** | 同层级内：**事实性危害**（RZE-24 自述泄露）> **结构性残留**（RZE-11/12 排比与对称）> **词汇性**（RZE-08/09/16/17 空词）> **纯风格**（RZE-04/05/19/20） |
| **3** | **覆盖优先** | 命中片段相互包含时，取**覆盖范围更大**的那条 |
| **4** | **结构 > 词汇** | 仍平手时，取结构性规则（见使用原则第 1 条） |

### 常见冲突对裁定表
| 冲突对 | 取哪一条 | 理由 |
|---|---|---|
| RZE-24 × RZE-01（AI 自述 × 对话尾巴） | **RZE-24** | 层级优先（RL1 内按危害，自述更严重） |
| RZE-07 × RZE-08（unlock the power × empower） | **各报一条** | 不相交，属两个独立缺陷 |
| RZE-11 × RZE-12（三连排比 × 对称骨架） | **取结构更明显者** | 覆盖优先 |
| RZE-27 × RZE-09（not just X it's Y × elevate） | **RZE-27** | 结构 > 词汇 |

---

## 规则清单

### RL1 · 硬阻断（单次即报）

**RZE-01　对话尾巴 / 收尾客服腔**
- 模式（正则，不区分大小写）：`\b(let me know if you (would|'d) like|i hope this helps|feel free to (ask|reach out)|if you have any (questions|further questions)|don't hesitate to|happy to help|hope that helps)\b`
- 示例：`Let me know if you'd like me to expand on any section.`
- 保护边界：用户原文确实在结尾发起对话（如咨询报告）→ 不报；作为独立邮件签名语 → 不报。
- 判定：RL1，单次即报。类比 zh 的 RZ-01。

**RZE-24　AI 自述残留**
- 模式：`\b(as an ai( language)? model|as a large language model|i am an ai|i cannot|i don't have (access|opinions|feelings))\b`
- 示例：`As an AI language model, I cannot provide personal opinions.`
- 保护边界：文章**讨论 AI/伦理/模型能力**本身且该表述是论点所需 → 不报；否则必报（等同 zh 的「AI 自述」）。
- 判定：RL1，单次即报，危害最高。

---

### RL2 · 高精度

**RZE-02　套话开场**
- 模式：`\b(in (today's|the|this) (fast-?paced|ever-evolving|modern|digital) (world|landscape|era)|with the (rapid |recent )?development of|in recent years,?)\b`
- 示例：`In today's fast-paced world, data drives everything.`
- 判定：RL2；密度门控。

**RZE-03　"It is worth noting that" 式填充**
- 模式：`\b(it is (worth|important|notable|critical) (to note|noting) that|note that)\b`
- 示例：`It is worth noting that results may vary.`
- 保护边界：后接**具体数据/限定**且有实质信息 → 可报为可改；纯填充 → 必改候选。

**RZE-06　"Navigate the complexities/landscape of" 空动词**
- 模式：`\bnavigate(s)? (the )?(complexities|complexity|landscape|challenges|nuances) of\b`
- 示例：`We help you navigate the complexities of modern logistics.`

**RZE-07　"Unlock / Harness / Unleash the power of" 赋能类**
- 模式：`\b(unlock|harness|unleash|tap into) (the )?(power|potential|value|magic) of\b`
- 示例：`Unlock the power of your data.`（英文版「赋能/闭环」黑话）
- 判定：RL2；单次即报（高特征）。

**RZE-08　"Empower / Empowering" 空 uplift 动词**
- 模式：`\bempower(s|ing|ed|ment)?\b`
- 示例：`Our platform empowers teams to do more.`
- 保护边界：确指「赋予某项具体能力（如权限/工具）」且有宾语 → 可保留；作为泛化拔高 → 报。

**RZE-09　"Elevate" 空拔高**
- 模式：`\belevate(s|d|ing)? (your |the )?(experience|brand|performance|business|journey)\b`
- 示例：`Elevate your customer experience.`

**RZE-10　"Delve / Delve into" 经典 GPT 词**
- 模式：`\bdelv(e|ing) (into|deeper)\b`
- 示例：`Let's delve into the details.`

**RZE-11　三连排比 / Rule of three**
- 模式（结构）：同一句或相邻三句出现 **三项并列同构**（如 `faster, smarter, better`；`seamless, efficient, powerful`；`speed, quality, trust`）。检测：连续逗号/顿号并列且项数 = 3 且词性趋同。
- 示例：`Our solution is faster, smarter, and better than the rest.`
- 判定：RL2，结构优先；单次即报。类比 zh 的 RZ-16。

**RZE-12　对称骨架**
- 模式（结构）：`\b(on one hand.*on the other hand|not only.*but (also|too)|both.*and.*|it's not (just|merely) .* it's)\b`（跨句匹配）
- 示例：`It's not just a tool — it's a partner.`
- 判定：RL2，结构优先。类比 zh 的 RZ-15。

**RZE-15　公式化收尾**
- 模式：`\b(in conclusion|to sum up|to summarize|in summary|overall,? (we|it))\b`
- 示例：`In conclusion, the framework is sound.`
- 保护边界：学术论文/长报告确需收束段 → 可保留，但 Empty 收尾（无新信息）才报。

**RZE-16　"Seamless / Effortless / Frictionless" 填充形容词**
- 模式：`\b(seamless|effortless|frictionless|painless)\b`
- 示例：`Enjoy a seamless, effortless onboarding.`

**RZE-17　"Robust / Comprehensive" 空泛褒义**
- 模式：`\b(robust|comprehensive|powerful|scalable)\b`（作泛化定语且无量化）
- 保护边界：后接**具体指标/范围**（如 "robust to 10k QPS"）→ 保留。

**RZE-18　夸张 hype 词**
- 模式：`\b(game-?changer|paradigm shift|revolutionary|groundbreaking|cutting-?edge|disruptive|unprecedented)\b`
- 示例：`A revolutionary, game-changing approach.`
- 判定：RL2；密度门控（单处可报可改，≥2 处必报候选）。

**RZE-22　虚技术极限词（tech superlatives）**
- 模式：`\b(cutting-?edge|state-?of-?the-?art|next-?generation|world-?class|best-?in-?class|military-?grade)\b`
- 示例：`Our next-generation, state-of-the-art engine.`

**RZE-23　管理黑话 buzzword**
- 模式：`\b(holistic|synergistic|end-?to-?end|cross-?functional|value-?added|actionable|low-?hanging fruit)\b`
- 示例：`We deliver holistic, end-to-end value.`

**RZE-27　"Not just X, it's Y" 重构句式**
- 模式：`\bit's not (just|merely) .* it's\b`
- 示例：`It's not just software, it's a movement.`

**RZE-28　"Transform" 过度用作唯一变化动词**
- 模式：`\btransform(s|ing|ed|ation)?\b`（密度：窗口内 ≥3 次且无具体宾语）
- 示例：`We transform, transform, and transform your business.`（密集时）

**RZE-30　"Leverage" 商务套话**
- 模式：`\bleverag(e|ing|ed)\b`
- 示例：`Leverage the power of our platform.`
- 保护边界：金融/技术语境「杠杆」本义 → 保留。

---

### RL3 · 风格（严格档启用）

**RZE-04　过渡词堆叠**
- 模式：`\b(moreover|furthermore|additionally|in addition|besides|likewise)\b`（密度：段落内 ≥3 个）
- 示例：`Moreover, it is fast. Furthermore, it is cheap. Additionally, it is safe.`

**RZE-05　破折号（em-dash）滥用**
- 模式：句中 `—`（U+2014）出现 ≥2 次/段，且多用于「修辞停顿」而非解释插入。
- 示例：`The model — trained on vast data — is — surprisingly — fast.`
- 保护边界：成对使用作插入解释（"the city — once a capital —"）→ 保留。

**RZE-13　"A testament to / A reflection of" 空名词**
- 模式：`\b(a testament to|a reflection of|a symbol of)\b`

**RZE-14　陈词套语**
- 模式：`\b(at the end of the day|when all is said and done|in the final analysis|at its core)\b`

**RZE-19　虚开场介词**
- 模式：`\b(in the realm of|in the world of|in the context of|within the sphere of)\b`

**RZE-20　填充句首发语**
- 模式：`\b(crucially|importantly|notably|interestingly|essentially|fundamentally),?\b`

**RZE-21　"realize / unlock your potential" 励志腔**
- 模式：`\b(unlock|realize|achieve) (your |their )?(full )?potential\b`

**RZE-25　emoji 在正式/专业文本中滥用**
- 模式：连续 ≥3 个 emoji，或正式报告/论文中出现 emoji。
- 保护边界：社媒/营销物料中的功能性 emoji → 保留。

**RZE-26　"Please note that" 填充**
- 模式：`\bplease note that\b`

**RZE-29　空泛描述形容词**
- 模式：`\b(vibrant|dynamic|thriving|robust ecosystem|rich(ly)? (detailed|featured))\b`

---

## 与中文包的关系

- 中文产物 → 加载 `rules-residue-zh.md`（RZ-xx）。
- 英文产物 → 加载本包（RZE-xx）。
- 中英混合产物 → 两包**叠加**加载，分别用各自代号报告（RZ-xx / RZE-xx），不得混用。
- 仲裁阶梯、密度门控、保护边界三原则两包通用。
