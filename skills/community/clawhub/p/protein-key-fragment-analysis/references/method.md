# 分析方法细节

## 1. 共识序列提取算法

```python
for 每个比对位置 i:
    统计该列所有非 gap 氨基酸频次
    保守率 = 最高频氨基酸出现次数 / 非 gap 总数
    if 保守率 >= THRESHOLD:
        consensus[i] = 最高频氨基酸
    else:
        consensus[i] = 'X'   # 变异度高，无主导氨基酸

最终去除所有 gap（-）得到连续共识序列
```

## 2. 高保守连续区检测算法

```python
扫描共识序列（含逐位保守率）：
    找连续区段，满足：
      - 每个位置保守率 >= HIGH_CONSERVATION (默认 0.90)
      - 氨基酸 != 'X'
      - 连续长度 >= MIN_LEN (默认 6aa)
    记录：起止位置、序列、平均保守率、长度
去重：与已知保守块重叠的区段不重复计入
```

## 3. 大样本采样策略

- 触发条件：序列数 > MAX_SEQ
- 方式：`random.sample()`，固定 `seed=42` 保证可复现
- 建议采样数：50-100 条（兼顾代表性与 MSA 耗时）
- ClustalOmega 耗时参考：50条约5分钟，100条约20分钟，200+条超1小时

## 4. 重要性分级

| 等级 | 判定依据 |
|------|---------|
| 🔴 极关键 | 命中 Pfam S1 已知催化/活性位点保守块 |
| 🟠 关键 | 命中其他已知功能相关保守块 |
| 🟡 结构关键 | 共识序列中检测到 ≥2 个保守 Cys 残基 |
| 🔵 高保守待确认 | 连续保守率 ≥90%，长度 ≥6aa，但未命中已知功能块 |

## 5. 氨基酸组成分析（Step 4.5）

对每个关键片段统计各功能类别氨基酸的出现频率。

**分类方案（与 aa-pair-analysis 统一，⚠️ A/G/P 排除，不归入任何类别）**：

```python
AA_CATEGORIES = {
    'S': 'Nucleophilic', 'T': 'Nucleophilic', 'C': 'Nucleophilic',
    'V': 'Hydrophobic',  'L': 'Hydrophobic',  'I': 'Hydrophobic', 'M': 'Hydrophobic',
    'F': 'Aromatic',     'Y': 'Aromatic',     'W': 'Aromatic',
    'N': 'Amide',        'Q': 'Amide',
    'D': 'Acidic',       'E': 'Acidic',
    'H': 'Cationic',     'K': 'Cationic',     'R': 'Cationic',
}
EXCLUDED = set('XAGP')  # X/A/G/P 均不参与统计
```

**输出字段（写入 `_key_fragments.json` 的 `composition` 字段）**：

```json
"composition": {
  "category_counts": {"Hydrophobic": N, "Nucleophilic": N, ...},
  "category_ratios": {"Hydrophobic": 26.8, "Nucleophilic": 24.3, ...},
  "total_valid": N,
  "unclassified_count": N,
  "dominant_category": "Mixed | Hydrophobic | ...",
  "dominant_ratio": 26.8,
  "physicochemical_property": "描述文字"
}
```

**主导类别判定**：某类别占比 ≥ 35% 则为该类主导，否则为 Mixed（混合型）。

## 6. 功能预测（Step 5）

基于 Step 4.5 的氨基酸组成比例，按优先级规则推断主要功能，结果写入 `function_prediction` 字段：

| 优先级 | 判断条件 | 功能预测标签 |
|--------|---------|------------|
| 1 | Pfam已知功能块命中 | 🔴 丝氨酸蛋白酶催化位点 |
| 2 | 片段Cys比例 ≥ 12% | 🟡 二硫键网络/结构骨架 |
| 3 | Nucleophilic ≥ 40% | 🟢 催化活性位点/磷酸化调控区 |
| 4 | Hydrophobic ≥ 45% | ⬛ 疏水折叠核心/跨膜区 |
| 5 | Aromatic ≥ 20% | 🟣 底物识别/π-π堆叠区 |
| 6 | Cationic ≥ 35% | ⚡ 正电荷底物结合区 |
| 7 | Acidic ≥ 35% | 🔵 金属离子螯合/催化酸基区 |
| 8 | N ≥ 25% + Ca ≥ 15% | 🔵 亲核-阳离子协作底物识别区 |
| 9 | H ≥ 25% + N ≥ 25% | ⬛ 两亲性蛋白-蛋白相互作用界面 |
| 10 | Ac ≥ 20% + Ca ≥ 20% | ⚡ 电荷互补区（盐桥/静电引导） |
| 11 | Amide ≥ 20% | 🔵 酰胺富集区（氢键网络/N-糖基化） |
| 12 | 以上均不满足 | 🔵 混合型功能区（Linker/多功能界面） |

**参考脚本**：`skills/fragment_aa_stats_and_predict.py`（可对已有 JSON 结果补跑此步骤）。

## 5. 已知局限性

| 局限 | 影响 |
|------|------|
| 大样本采样 | 代表性略降，极少数物种特有序列可能被漏采 |
| 共识阈值固定 | 部分保守区可能被 X 遮蔽（可调整 THRESHOLD） |
| 保守块预设有限 | 仅覆盖 Pfam S1 经典家族，特殊子家族可能漏检 |
| 高保守区功能未验证 | 需 AlphaFold2 结构预测或实验验证方可确认 |
| 全局比对假设 | 长度差异极大的序列比对质量可能下降 |
