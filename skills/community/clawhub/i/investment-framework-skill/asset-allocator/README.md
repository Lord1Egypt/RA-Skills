# asset-allocator 技能包

> 基于《漫步华尔街》- 伯顿·马尔基尔的资产配置技能

---

## 📁 目录结构

```
asset-allocator/
├── SKILL.md                      # 技能定义（核心）
├── README.md                     # 本文件（目录导航）
├── examples/                     # 示例集合
│   ├── balanced-example.md       # 平衡型配置示例
│   ├── conservative-example.md   # 保守型配置示例（待创建）
│   └── aggressive-example.md     # 积极型配置示例（待创建）
├── references/                   # 参考资料
│   └── allocation-theory.md      # 资产配置理论
├── templates/                    # 模板文件
│   └── allocation-template.md    # 配置方案模板
├── scripts/                      # 计算脚本（待创建）
│   └── allocation-calculator.py  # 配置比例计算
└── calculators/                  # 计算工具（待创建）
    └── rebalance-calculator.md   # 再平衡计算公式
```

---

## 🚀 快速开始

### 1. 查看技能定义
```bash
cat SKILL.md
```

### 2. 查看示例
```bash
cat examples/balanced-example.md
```

### 3. 使用模板
```bash
cat templates/allocation-template.md
```

### 4. 参考理论
```bash
cat references/allocation-theory.md
```

---

## 📊 技能功能

**核心功能**：根据生命周期设计资产配置方案

**输入**：
- 年龄
- 风险偏好（保守/平衡/积极）
- 投资目标
- 资产规模

**输出**：
- 资产配置比例（股票/债券/现金/另类）
- 基金推荐
- 再平衡策略
- 定投计划

---

## 🔗 相关技能

- **portfolio-designer**: 组合构建（更专业的组合设计）
- **global-allocator**: 全球配置（全球分散）
- **simple-investor**: 简单投资（简化版配置）
- **decision-checklist**: 决策检查（配置前检查）

---

## 📐 核心公式

### 股票比例
```
股票比例 = 100 - 年龄
```

### 再平衡阈值
```
偏离 > 5% → 调整回目标比例
```

### 定投金额
```
月度定投 = 月度可投资金额 × 配置比例
```

---

## 🧪 使用示例

**输入**：
```
我 35 岁，平衡型风险，有 100 万，如何配置？
```

**输出**：
```
【35 岁平衡型配置方案】

股票：65%（65 万）
  - 国内指数：40%（26 万，沪深 300ETF）
  - 国际指数：25%（16.25 万，标普 500ETF）

债券：25%（25 万）
  - 国债 ETF：15%（15 万）
  - 信用债基金：10%（10 万）

现金：5%（5 万，货币基金）

另类：5%（5 万，黄金 ETF）

再平衡：每年 1 次，偏离>5% 调整
```

---

## ⚠️ 常见错误

1. **机械套用公式**：忽视个人差异
2. **忽视应急资金**：全仓投资
3. **频繁调整**：不遵守再平衡纪律
4. **过度分散**：买太多基金
5. **忽视成本**：高费率侵蚀收益

详见 `SKILL.md` 的"⚠️ 常见错误"章节。

---

## 📚 学习路径

1. 阅读 `SKILL.md` 了解功能
2. 查看 `examples/` 学习实战
3. 使用 `templates/` 制定方案
4. 参考 `references/` 深入理论
5. 使用 `scripts/` 和 `calculators/` 计算

---

## 🛠️ 工具脚本

### allocation-calculator.py
```bash
# 计算配置比例
python scripts/allocation-calculator.py --age 35 --risk balanced --assets 1000000
```

### rebalance-calculator.md
```markdown
# 再平衡计算
目标：股票 60%，债券 40%
当前：股票 70%，债券 30%
操作：卖出 10% 股票，买入债券
```

---

## 📊 版本历史

- v2.0.0 (2026-03-19): 按 SKILL-STANDARD-v2.md 重构
- v1.0.0 (2026-03-13): 初始版本

---

*资产配置是唯一的免费午餐。用纪律战胜情绪，用时间换取复利。*
