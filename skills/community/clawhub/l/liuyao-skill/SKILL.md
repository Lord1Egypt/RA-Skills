---
name: liuyao-skill
description: Use when the user asks for Liuyao / Zhou Yi (I Ching) divination, hexagram interpretation, or fortune-telling. Triggers on 六爻, 占卜, 起卦, 解卦, 算卦, 周易, 易经, 卦象, divination, hexagram.
metadata:
  hermes:
    tags: [divination, liuyao, zhouyi, iching, hexagram]
    category: divination
---

# 六爻

## 概述

基于周易原理进行占卜与解卦。支持铜钱法伪随机起卦、蓍草法伪随机起卦和手动输入起卦，解卦覆盖卦辞原文、传统注解和 AI 个性化解读。

## 三不占原则（占卜前必须检查）

1. **不诚不占** — 心中无敬意、不真诚者不占
2. **不义不占** — 所问之事不合道义者不占
3. **不疑不占** — 心中无疑问、无困惑者不占

用户请求占卜时，先判断是否符合三不占原则。不符合则拒绝并说明原因。

## 占卜流程

### 第一步：起卦

询问用户选择起卦方式：

**方式一：自动铜钱法（推荐）**
```
python3 scripts/qigua.py --method coin --json
```

**方式二：手动输入**
用户自己摇卦后输入结果。每爻输入0-3的数字（背面数量）：
- 0 = 老阴(×)，动爻
- 1 = 少阳(—)，静爻
- 2 = 少阴(--)，静爻
- 3 = 老阳(〇)，动爻

```
python3 scripts/qigua.py --method manual --input "1,2,3,0,1,2" --json
```

**方式三：蓍草法**
伪随机模拟传统蓍草"三变成一爻"，自动演算六爻：
```
python3 scripts/qigua.py --method shicao --json
```
脚本按经典蓍草法爻值概率建模：老阴6=1/16、少阳7=5/16、少阴8=7/16、老阳9=3/16。

### 第二步：读取结果

脚本输出 JSON，关键字段：
- `ben_gua['name']` — 本卦名
- `bian_gua['name']` — 变卦名
- `yao_details` — 各爻详情
- `moving_yao` — 动爻标签列表
- `shicao_value` — 蓍草法输出时的爻值（6/7/8/9）

### 第三步：查卦辞

在 `references/guaci-full.md` 中查找本卦的卦辞原文。

### 第四步：查爻辞

在 `references/yaoci-full.md` 中查找本卦的爻辞原文。重点关注动爻的爻辞。

### 第五步：解卦

根据 `references/jiegu-guide.md` 中的规则解卦：

| 动爻数量 | 解卦侧重 |
|----------|---------|
| 0（静卦） | 本卦卦辞为主 |
| 1 | 该动爻爻辞为主 |
| 2 | 两爻辞为主，上爻为主 |
| 3 | 本卦卦辞为体，变卦卦辞为用 |
| 4 | 变卦中两不变爻辞为主，下爻为主 |
| 5 | 变卦中唯一不变爻辞为主 |
| 6（全动） | 乾→用九，坤→用六，其他→变卦卦辞 |

### 第六步：综合解读

结合以下要素给出个性化解读：
1. 卦辞和爻辞原文
2. 动爻含义与变化趋势
3. 本卦→变卦的演变方向
4. 用户的具体问题
5. 传统注解参考

## 解卦输出格式

```
## 占卜结果

**本卦**：[卦名]（上[上卦] 下[下卦]）
**变卦**：[卦名]（如有动爻）

### 卦象
[从下往上列出六爻，标注动爻]

### 卦辞
[卦辞原文]

### 动爻爻辞
[动爻标签]：[爻辞原文]

### 解读
[根据动爻数量规则，结合用户问题给出解读]

### 建议
[基于卦象给出的具体建议]
```

## 常见问题

**Q: 用户没有明确问题怎么办？**
A: 提示用户说出心中所问之事。周易占卜必须有明确的疑问。

**Q: 用户想重复占同一件事？**
A: 提醒"同一事不占第二卦"，一件事问了就是问了，不要反复占。

**Q: 动爻很多怎么办？**
A: 动爻越多，变化越大，局势越不稳定。按解卦规则处理，重点分析变卦。

## 参考文件

- `references/64gua-table.md` — 六十四卦速查表
- `references/guaci-full.md` — 六十四卦卦辞全文
- `references/yaoci-full.md` — 六十四卦爻辞全文
- `references/jiegu-guide.md` — 解卦方法与注解指引
- `assets/gua-data.json` — 卦象结构化数据
- `scripts/regenerate_guaci.py` — 从脚本内置资料重新生成 `references/guaci-full.md`
