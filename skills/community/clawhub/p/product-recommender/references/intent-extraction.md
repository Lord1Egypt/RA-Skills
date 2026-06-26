# Intent Extraction Guide

## Signal Extraction Patterns

### Budget Parsing
```
"500以内" / "500块以下"    → { max: 500 }
"200-500"                  → { min: 200, max: 500 }
"大概500"/ "500左右"       → { min: 400, max: 600 }  (±20% range)
"不贵的" / "便宜点的"      → { max: "low_tier" }  → use bottom 33% of catalog by price
"好一点的" / "不差钱"      → { min: "high_tier" } → use top 33% of catalog by price
```

### Recipient Mapping
| User says | Internal tag |
|-----------|-------------|
| 妈妈/母亲/老妈 | recipient:mother, gender:female, age:40+ |
| 爸爸/父亲/老爸 | recipient:father, gender:male, age:40+ |
| 男朋友/老公/先生 | recipient:partner_male, gender:male |
| 女朋友/老婆/太太 | recipient:partner_female, gender:female |
| 老人/长辈/爷爷/奶奶 | recipient:elderly, age:60+ |
| 小孩/孩子/宝宝 | recipient:child, age:<12 |
| 朋友/闺蜜/哥们 | recipient:friend |
| 自用/自己/我 | recipient:self |
| 同事/上司/老板 | recipient:colleague, formality:high |

### Occasion Mapping
| User says | Occasion tag |
|-----------|-------------|
| 生日 | occasion:birthday |
| 结婚/婚礼/新婚 | occasion:wedding |
| 毕业/升学 | occasion:graduation |
| 节日/过节/春节/中秋 | occasion:holiday |
| 面试/求职/正式场合 | occasion:formal, style:professional |
| 日常/平时穿/随便 | occasion:casual, style:everyday |
| 旅行/出游/户外 | occasion:travel, style:casual |
| 运动/健身/跑步 | occasion:sports, style:athletic |
| 海边/夏天 | occasion:beach, season:summer |

### Style/Preference Keywords → Product Tags
| User says | Filter tag |
|-----------|-----------|
| 素色/简约/低调 | style:minimal |
| 花哨/图案/印花 | style:printed |
| 轻便/轻薄 | attribute:lightweight |
| 保暖/厚实 | attribute:warm |
| 纯棉/棉质 | material:cotton |
| 防水/防泼水 | attribute:waterproof |
| 不含酒精 | ingredient:alcohol_free |
| 温和/敏感肌 | attribute:gentle, skin:sensitive |

---

## Clarification Decision Tree

Ask only when the query can't be answered without the missing info:

```
Has budget?
  No → Ask: "请问预算大概多少？"
  Yes → continue

Has recipient or is self-purchase clear?
  No + it's a gift query → Ask: "是送给谁的呢？"
  Otherwise → continue

Has enough context to filter?
  Yes → run filtering, return results
  No (too vague, e.g. just "推荐一下") → Ask: "您是自用还是送人？有没有预算范围？"
```

Never ask more than one question at a time.
If the customer has already provided context in the same session, don't ask again.

---

## Fallback Intent Handling

| Situation | Action |
|-----------|--------|
| No products match filters | Relax budget by 20%, re-filter; if still nothing → say so honestly |
| Customer says "这些都不行" | Ask what specifically doesn't fit; adjust one filter at a time |
| Very vague intent ("推荐一个好的") | Return top 3 bestsellers from knowledge base |
| Contradictory signals ("便宜的好一点的") | Show 2 options: best value vs. best quality in range |
