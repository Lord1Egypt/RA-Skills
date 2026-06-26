# 🦞 投资框架技能包

> 基于 5 本经典投资书籍的实战工具箱

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/lj22503/one-person-ceo-skills)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-5-orange)](#核心技能)

---

## 🚀 快速开始

**新手必读**：[QUICKSTART.md](QUICKSTART.md)（5 分钟上手）

**详细指南**：[USAGE.md](USAGE.md)（完整使用手册）

---

## 📚 理论来源

基于 5 本投资经典：

| 书籍 | 作者 | 核心贡献 |
|------|------|----------|
| 📘 《聪明的投资者》 | 格雷厄姆 | 安全边际、市场先生 |
| 📗 《证券分析》 | 格雷厄姆 & 多德 | 内在价值、财务分析 |
| 📙 《巴菲特致股东的信》 | 巴菲特 | 护城河、能力圈 |
| 📕 《穷查理宝典》 | 芒格 | 多元思维、逆向思考 |
| 📔 《漫步华尔街》 | 马尔基尔 | 指数基金、资产配置 |

---

## 🚀 核心技能

### 1. value-analyzer（价值分析师）

**功能**：基于格雷厄姆原则分析股票价值

**触发词**：
- "分析这只股票"
- "是否符合格雷厄姆标准"
- "安全边际是多少"

**输出**：
- 防御型/积极型评估
- 7 大标准检查
- 安全边际计算
- 投资建议

**示例**：
```
@ant 分析贵州茅台，是否符合格雷厄姆标准？
```

---

### 2. moat-evaluator（护城河评估师）

**功能**：评估企业护城河类型和强度

**触发词**：
- "评估护城河"
- "这家公司有竞争优势吗"
- "是否符合巴菲特标准"

**输出**：
- 5 大护城河识别（品牌、网络、转换成本、规模、特许）
- 护城河强度评分（0-25 分）
- 持续性分析
- 投资建议

**示例**：
```
@ant 评估腾讯控股的护城河
```

---

### 3. intrinsic-value-calculator（内在价值计算器）

**功能**：计算企业内在价值和安全边际

**触发词**：
- "计算内在价值"
- "安全边际是多少"
- "估值分析"

**输出**：
- 4 种估值方法（格雷厄姆公式、资产价值、盈利价值、DCF）
- 安全边际计算
- 敏感性分析
- 投资建议

**示例**：
```
@ant 计算茅台的内在价值，当前价格安全吗？
```

---

### 4. decision-checklist（决策清单）

**功能**：基于多元思维和认知偏差检查

**触发词**：
- "检查这个投资想法"
- "决策清单"
- "是否有认知偏差"

**输出**：
- 能力圈检查
- 8 种认知偏差识别
- 逆向思考分析
- 综合评分和建议

**示例**：
```
@ant 我想买入宁德时代，帮我检查这个决策
```

---

### 5. asset-allocator（资产配置师）

**功能**：根据生命周期设计资产配置方案

**触发词**：
- "资产配置方案"
- "我应该如何配置资产"
- "定投计划"

**输出**：
- 风险承受能力评估
- 资产配置比例（股票/债券/现金/另类）
- 基金推荐
- 再平衡策略
- 定投计划

**示例**：
```
@ant 我 35 岁，平衡型风险，如何配置 100 万资产？
```

---

## 📖 使用流程

### 完整投资流程

```
1. value-analyzer → 初步筛选（是否符合格雷厄姆标准）
         ↓
2. moat-evaluator → 护城河评估（是否有持续竞争优势）
         ↓
3. intrinsic-value-calculator → 价值计算（内在价值和安全边际）
         ↓
4. decision-checklist → 决策检查（避免认知偏差）
         ↓
5. asset-allocator → 资产配置（仓位控制）
         ↓
执行买入，定期复盘
```

---

## 📋 快速参考

### 格雷厄姆 7 大标准（防御型）

```
□ 适当规模（行业前 30%）
□ 财务稳健（负债率<50%）
□ 盈利稳定（连续 10 年）
□ 分红记录（连续 20 年）
□ 盈利增长（10 年>33%）
□ P/B < 1.5
□ P/E < 15
```

### 护城河 5 类型

```
□ 品牌优势    □ 网络效应    □ 转换成本
□ 规模优势    □ 特许经营权
```

### 安全边际标准

```
>50%：极佳 - 强烈买入
30-50%：良好 - 买入
10-30%：一般 - 观察
<10%：不足 - 不买入
```

### 认知偏差检查

```
□ 奖励机制偏见  □ 喜好偏见    □ 厌恶偏见
□ 从众心理      □ 锚定效应    □ 过度自信
□ 确认偏误      □ 损失厌恶
```

---

## 📁 文件结构

```
investment-framework/
├── SKILL.md                    # 技能包总览
├── THEORY.md                   # 核心理论详解
├── USAGE.md                    # 使用指南
├── README.md                   # 本文件
├── value-analyzer/
│   └── SKILL.md               # 价值分析技能
├── moat-evaluator/
│   └── SKILL.md               # 护城河评估技能
├── intrinsic-value-calculator/
│   └── SKILL.md               # 内在价值计算技能
├── decision-checklist/
│   └── SKILL.md               # 决策检查技能
└── asset-allocator/
    └── SKILL.md               # 资产配置技能
```

---

## 🎯 使用场景

### 场景 1：分析个股

```
@ant 分析贵州茅台
1. 是否符合格雷厄姆标准？
2. 护城河类型和强度？
3. 内在价值是多少？
4. 当前价格是否值得买入？
```

### 场景 2：检查决策

```
@ant 我想买入 XX 公司，帮我检查：
1. 是否在我的能力圈内？
2. 我有哪些认知偏差？
3. 逆向思考：什么情况下会失败？
```

### 场景 3：资产配置

```
@ant 我 35 岁，有 100 万，如何配置资产？
→ 输出：股债比例、基金推荐、定投计划、再平衡策略
```

---

## ⚠️ 重要原则

### 能力圈原则

> "只投资你理解的公司"

**测试**：
1. 能否用一句话说清公司如何赚钱？
2. 能否预测 10 年后行业格局？
3. 是否有行业专业知识？
4. 能否列出 3 个主要风险？

### 安全边际原则

> "用 4 毛钱买 1 块钱的东西"

- 没有安全边际，不买入
- 安全边际不足，等待更好价格
- 好公司 + 好价格=好投资

### 长期思维

> "如果你不愿意持有 10 年，就不要持有 10 分钟"

- 最少持有：3-5 年
- 理想持有：10 年+
- 最佳持有：永久（最佳公司）

### 避免杠杆

> "永远不要用借来的钱投资"

- 杠杆放大波动
- 可能导致爆仓
- 心理压力影响决策

---

## 📚 延伸阅读

### 入门
- 《聪明的投资者》- 格雷厄姆
- 《漫步华尔街》- 马尔基尔

### 进阶
- 《巴菲特致股东的信》- 巴菲特
- 《穷查理宝典》- 芒格

### 专业
- 《证券分析》- 格雷厄姆 & 多德
- 《投资最重要的事》- 霍华德·马克斯

---

## 🔧 安装

```bash
# 技能位于 OpenClaw 工作区
cd ~/.openclaw/workspace/skills/investment-framework/

# 无需额外依赖，开箱即用
```

---

## 📁 文件结构

```
investment-framework-skill/
├── QUICKSTART.md          ← 【入口】5 分钟快速入门
├── README.md              ← 项目介绍（你在这里）
├── USAGE.md               ← 详细使用指南
│
├── value-analyzer/        ← 价值分析师
├── moat-evaluator/        ← 护城河评估师
├── intrinsic-value-calculator/
├── decision-checklist/
├── asset-allocator/
│
├── docs/                  ← 理论文档（可选读）
├── scripts/               ← 工具脚本
└── config/                ← 配置文件
```

---

## 📞 支持

- **问题反馈**：GitHub Issues
- **理论详解**：[docs/THEORY.md](docs/THEORY.md)
- **使用指南**：[USAGE.md](USAGE.md)
- **快速入门**：[QUICKSTART.md](QUICKSTART.md)

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

**Copyright (c) 2026 燃冰 (燃冰 & ant)**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**简单来说：**
- ✅ 你可以自由使用、修改、分发、商用
- ✅ 需要保留原作者版权和许可证声明
- ❌ 不提供任何担保，使用风险自负

**合规声明：**
- 本技能仅提供投资框架教育和数据分析
- 不推荐具体基金/股票
- 不承诺收益/保本
- 所有输出仅供参考，不构成投资建议

详见 [LICENSE](LICENSE) 和 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 🌟 核心理念

> "投资很简单，但不容易。简单的是原则，不容易的是执行。"

**三大基石**：
1. 🛡️ **安全边际** - 价格必须低于价值
2. 🏰 **护城河** - 只投资有持续竞争优势的公司
3. 🧠 **理性决策** - 避免认知偏差，逆向思考

---

*最后更新：2026-04-14*
*版本：v1.0.0*
