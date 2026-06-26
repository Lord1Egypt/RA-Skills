# Investment Framework 完整技能清单 📊

**统计时间**：2026-04-07 07:20  
**版本**：v3.4.0

---

## 📊 技能总数统计

| 类别 | 数量 | 状态 |
|------|------|------|
| **已实现技能** | 12 个 | ✅ 完成 |
| **Schema 已适配** | 4 个 | ✅ 100% |
| **Schema 适配中** | 8 个 | 🔄 进行中 |
| **规划中技能** | 6 个 | ⏳ 待实现 |
| **总计** | 18 个 | - |

**注意**：之前提到的"26 个"或"29 个"可能包含了：
- 规划但未实现的 6 个进阶技能
- 其他投资相关技能（peak-wealth-calculator、fund-operation-workflow、ttfund-skills、life-experience-investor）
- 子技能/模块（calculators、templates 等）

---

## ✅ 已实现技能（10 个）

### 核心技能（5 个）

| # | 技能 | 基于经典 | 核心功能 | 触发场景 |
|---|------|---------|---------|---------|
| 1 | **value-analyzer** | 《聪明的投资者》格雷厄姆 | 格雷厄姆标准价值分析、防御型/积极型评估 | "分析这只股票" |
| 2 | **moat-evaluator** | 《巴菲特致股东的信》巴菲特 | 护城河评估、专利可持续性分析 | "这家公司有护城河吗" |
| 3 | **intrinsic-value-calculator** | 《证券分析》格雷厄姆&多德 | 内在价值计算、7 种估值方法 | "计算内在价值" |
| 4 | **decision-checklist** | 《穷查理宝典》芒格 + 《投资王道》 | 认知偏差检查 + 投资十诫 | "帮我检查投资逻辑" |
| 5 | **asset-allocator** | 《漫步华尔街》马尔基尔 | 生命周期资产配置、CFA 框架 | "如何配置资产" |

### 趋势与未来（1 个）

| # | 技能 | 基于经典 | 核心功能 | 触发场景 |
|---|------|---------|---------|---------|
| 6 | **future-forecaster** | 《必然》《失控》KK | 未来趋势预测、技术层级判断 | "这是趋势还是泡沫" |

### 《投资王道》新增（3 个）⭐ 2026-04-06

| # | 技能 | 基于经典 | 核心功能 | 触发场景 |
|---|------|---------|---------|---------|
| 7 | **market-patent-evaluator** 🆕 | 《投资王道》林森池 | 市场经济专利评估、两类生意分类 | "这家公司有市场经济专利吗" |
| 8 | **industry-specialist** 🆕 | 《投资王道》林森池 | 行业特解指标库（6+ 大行业） | "这个行业值得投资吗" |
| 9 | **thousand-mile-horse-screener** 🆕 | 《投资王道》林森池 | 千里马七准则筛选 | "哪些公司值得长期持有" |

### 风险与情绪分析（2 个）⭐ 2026-04-07

| # | 技能 | 核心功能 | 触发场景 |
|---|------|---------|---------|
| 10 | **risk-assessor** 🆕 | 独立风险评估（波动率/下行风险/集中度）、仓位上限计算 | "这只股票风险有多大" |
| 11 | **sentiment-analyzer** 🆕 | 市场情绪分析（新闻/社交/分析师评级）、反向信号识别 | "市场怎么看这家公司" |

### 主技能（1 个）

| # | 技能 | 核心功能 | 触发场景 |
|---|------|---------|---------|
| 10 | **investment-framework** | 主技能（路由到子技能）、完整投资流程 | "投资价值分析" |

---

## ⏳ 规划中技能（6 个）

**来源**：COMPLETE_SUMMARY.md（第二阶段：6 本进阶经典）

| # | 技能 | 基于经典 | 核心功能 | 优先级 |
|---|------|---------|---------|--------|
| 11 | **second-level-thinker** | 《投资最重要的事》霍华德·马克斯 | 第二层思维训练、市场周期判断 | ⭐⭐⭐ |
| 12 | **bias-detector** | 《思考，快与慢》卡尼曼 | 认知偏差识别、25 种偏差检查 | ⭐⭐⭐ |
| 13 | **stock-picker** | 《彼得·林奇的成功投资》林奇 | 林奇选股法、6 类型公司分析 | ⭐⭐ |
| 14 | **simple-investor** | 《投资中最简单的事》邱国鹭 | 价值投资中国化、估值品质时机 | ⭐⭐ |
| 15 | **portfolio-designer** | 《机构投资者的创新之路》史文森 | 耶鲁模式配置、另类投资 | ⭐ |
| 16 | **global-allocator** | 《资产配置的艺术》达斯特 | 全球分散、再平衡策略 | ⭐ |

---

## 📁 技能目录结构

```
skills/investment-framework/
├── SKILL.md                          # 主技能（总览）
├── asset-allocator/
│   └── SKILL.md                      # ✅ 资产配置
├── decision-checklist/
│   └── SKILL.md                      # ✅ 决策检查
├── future-forecaster/
│   └── SKILL.md                      # ✅ 趋势预测
├── industry-specialist/
│   └── SKILL.md                      # ✅ 行业分析（新增）
├── intrinsic-value-calculator/
│   └── SKILL.md                      # ✅ 内在价值计算
├── market-patent-evaluator/
│   └── SKILL.md                      # ✅ 市场经济专利（新增）
├── moat-evaluator/
│   └── SKILL.md                      # ✅ 护城河评估
├── thousand-mile-horse-screener/
│   └── SKILL.md                      # ✅ 千里马筛选（新增）
├── value-analyzer/
│   └── SKILL.md                      # ✅ 价值分析
├── references/                       # 📚 参考资料
├── examples/                         # 📝 使用示例
├── templates/                        # 📋 报告模板
└── data_sources/                     # 📊 数据源配置
```

---

## 📚 理论覆盖（11 本书）

### 已覆盖（6 本）

| # | 书籍 | 作者 | 对应技能 | 状态 |
|---|------|------|---------|------|
| 1 | 《聪明的投资者》 | 格雷厄姆 | value-analyzer | ✅ |
| 2 | 《证券分析》 | 格雷厄姆&多德 | intrinsic-value-calculator | ✅ |
| 3 | 《巴菲特致股东的信》 | 巴菲特 | moat-evaluator | ✅ |
| 4 | 《穷查理宝典》 | 芒格 | decision-checklist | ✅ |
| 5 | 《漫步华尔街》 | 马尔基尔 | asset-allocator | ✅ |
| 6 | 《必然》《失控》 | 凯文·凯利 | future-forecaster | ✅ |
| 7 | 《投资王道》 | 林森池 | market-patent/industry/horse-screener | ✅ |

### 未覆盖（6 本）

| # | 书籍 | 作者 | 规划技能 | 状态 |
|---|------|------|---------|------|
| 8 | 《投资最重要的事》 | 霍华德·马克斯 | second-level-thinker | ⏳ |
| 9 | 《思考，快与慢》 | 卡尼曼 | bias-detector | ⏳ |
| 10 | 《彼得·林奇的成功投资》 | 林奇 | stock-picker | ⏳ |
| 11 | 《投资中最简单的事》 | 邱国鹭 | simple-investor | ⏳ |
| 12 | 《机构投资者的创新之路》 | 史文森 | portfolio-designer | ⏳ |
| 13 | 《资产配置的艺术》 | 达斯特 | global-allocator | ⏳ |

---

## 🔄 技能演进历史

### v1.0.0（2026-03-12）
- 初始版本：5 个核心技能
- value-analyzer, moat-evaluator, intrinsic-value-calculator, decision-checklist, asset-allocator

### v1.1.0（2026-03-16）
- 新增：future-forecaster

### v2.0.0（2026-03-19）
- 按照 SKILL-STANDARD-v2.md 深度重构
- 增强 decision-checklist（CFA 框架）
- 增强 moat-evaluator（护城河趋势）

### v3.0.0（2026-03-23）
- 集成 problem-mapper 作为元技能
- 更新技能关系图

### v3.2.0（2026-04-06）⭐ 当前版本
- 新增 3 个《投资王道》技能
- market-patent-evaluator, industry-specialist, thousand-mile-horse-screener
- 增强 4 个现有技能
- moat-evaluator（专利可持续性）
- decision-checklist（投资十诫）
- value-analyzer（八步分析法）
- intrinsic-value-calculator（专业估值方法）

---

## 📊 技能使用追踪

**追踪文件**：`memory/skill-usage.jsonl`

**查询命令**：
```bash
# 查看最近 7 天使用情况
python3 skills/skill-tracker/scripts/tracker.py analyze --days 7

# 查看所有技能使用统计
python3 skills/skill-tracker/scripts/tracker.py report
```

**高频技能**（预期）：
1. value-analyzer - 个股分析最常用
2. moat-evaluator - 护城河评估
3. decision-checklist - 决策前检查

**低频技能**（预期）：
- future-forecaster - 趋势分析较少用
- asset-allocator - 配置方案不常用

---

## 🎯 下一步优化计划

### 高优先级（本周）
- [ ] 创建 risk-assessor 技能（独立风险评估）
- [ ] 创建 sentiment-analyzer 技能（市场情绪分析）
- [ ] 标准化输出 Schema（9 个子技能）

### 中优先级（本月）
- [ ] 创建 orchestrator 技能（协调器）
- [ ] 增强数据驱动能力
- [ ] 创建 backtester 技能（回测）

### 低优先级（下月）
- [ ] 实现规划中的 6 个进阶技能
- [ ] growth-investigator（Phil Fisher 框架）

---

## 📝 相关投资技能（不在 investment-framework 内）

**其他投资相关技能**：

| 技能 | 路径 | 功能 |
|------|------|------|
| peak-wealth-calculator | `skills/peak-wealth-calculator/` | 财富峰点计算器 |
| fund-operation-workflow | `skills/fund-operation-workflow/` | 基金运营工作流 |
| ttfund-skills | `skills/ttfund-skills/` | 天天基金查询 |
| life-experience-investor | `skills/life-experience-investor/` | 人生体验投资顾问 |

---

**总结**：
- **已实现**：10 个技能（9 个子技能 + 1 个主技能）
- **规划中**：6 个进阶技能
- **本次新增**：3 个《投资王道》技能
- **增强**：4 个现有技能

**GitHub**: https://github.com/lj22503/one-person-ceo-skills/tree/main/skills/investment-framework

---

*一人 CEO，不是一个人干所有事，是用工具和 AI 放大个人能力。* 🔗
