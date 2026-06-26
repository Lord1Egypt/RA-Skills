---
name: promo-calculator-claw
description: >
  促销方案测算虾 — 模拟不同折扣力度对利润的影响，在拍板促销方案前让数字说话。
  当以下情况时使用此 Skill：
  (1) 需要测算促销方案的利润影响（毛利率、净利率、总利润）；
  (2) 需要计算盈亏平衡点（最低不亏折扣、盈亏平衡销量）；
  (3) 需要对比多个折扣方案（7折/75折/8折等）的利润差异；
  (4) 需要批量测算多个SKU的促销方案；
  (5) 用户提到"促销"、"折扣"、"利润测算"、"盈亏平衡"、"毛利率"、"满减"、"活动方案"、"定价"、"清仓"、"套装"、"ROI"、"利润影响"；
  (6) 用户问"打X折还剩多少利润"、"满减后毛利率是多少"、"打几折清仓才不亏"。
---

# 促销方案测算虾

## 核心工作流

### 步骤 1：收集成本数据
必填字段：
- 采购成本（进货价）
- 原售价
- 平台佣金率（参考 `references/platform-fees.md`）
- 物流成本（元/件）
- 退货率
- 营销成本（广告费/件）

可选字段：仓储成本、固定成本（用于盈亏平衡销量计算）

如用户未提供某项成本，参考 `references/cost-structure.md` 中的行业默认值，并告知用户使用了估算值。

### 步骤 2：确认促销方案
- 直降/折扣：折扣率（如0.8表示8折）
- 满减：计算等效折扣率（优惠金额/原价）
- 赠品：将赠品成本计入营销成本

### 步骤 3：运行测算脚本

**单品单方案：**
```bash
python3 ~/.openclaw/skills/promo-calculator-claw/scripts/promo_calculator.py single \
  --cost <采购成本> --price <原售价> --discount <折扣率> \
  --commission <佣金率> --shipping <物流成本> --return-rate <退货率> \
  --marketing <营销成本> [--volume <预期销量>]
```

**多方案对比（推荐）：**
```bash
python3 ~/.openclaw/skills/promo-calculator-claw/scripts/promo_calculator.py compare \
  --cost <采购成本> --price <原售价> \
  --commission <佣金率> --shipping <物流成本> --return-rate <退货率> \
  --marketing <营销成本> \
  --discounts "0.7,0.75,0.8,0.85,0.9" [--volume <预期销量>]
```

**盈亏平衡分析：**
```bash
python3 ~/.openclaw/skills/promo-calculator-claw/scripts/promo_calculator.py breakeven \
  --cost <采购成本> --price <原售价> \
  --commission <佣金率> --shipping <物流成本> --return-rate <退货率> \
  --marketing <营销成本>
```

**批量SKU（CSV输入）：**
```bash
python3 ~/.openclaw/skills/promo-calculator-claw/scripts/promo_calculator.py batch \
  --input products.csv --discounts "0.7,0.75,0.8,0.85,0.9"
```

CSV格式（支持中文列名）：`SKU,采购成本,原售价,佣金率,物流成本,退货率,营销成本,预期销量`

### 步骤 4：输出决策建议
基于测算结果给出：
1. 各方案利润对比表（直接展示脚本输出）
2. 推荐方案及理由
3. 风险提示（亏损方案、销量敏感性）
4. 不亏本最低折扣底线

## 满减计算说明
满减等效折扣 = (原价 - 优惠金额) / 原价
例：满200减50 → 等效折扣 = 150/200 = 0.75（7.5折）

## 多情景分析
当用户需要评估风险时，建议同时测算三种情景：
- 乐观：预期销量 × 1.3
- 中性：预期销量
- 悲观：预期销量 × 0.6

## 参考资料
- `references/cost-structure.md`：各品类成本结构模板和行业默认值
- `references/platform-fees.md`：各平台佣金费率参考
- `references/promo-effect.md`：各类促销形式的销量拉升系数
