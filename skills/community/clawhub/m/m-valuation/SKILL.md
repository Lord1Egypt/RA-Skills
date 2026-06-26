# M估值法

基于ROIC和CAPM的股票估值方法，由蟹老板创建。

## 概述

完整的5步股票估值分析框架：
1. 资格筛选（ROIC > w）
2. 核心参数计算
3. 内在价值计算
4. 估值决策与风险分析
5. 情景分析

## 使用方法

当用户说"用M估值法分析[股票]"时，使用此skill：

```bash
python3 ~/.openclaw/workspace/skills/m-valuation/valuation.py <股票代码> [名称]

# 示例
python3 ~/.openclaw/workspace/skills/m-valuation/valuation.py 000333 美的集团
python3 ~/.openclaw/workspace/skills/m-valuation/valuation.py 600036 招商银行
```

## 触发词

- "M估值法"
- "用M估值法分析"
- "M估值"

## 数据来源

1. **Tushare API** - A股财务数据
2. **Tavily搜索** - 获取β系数、非A股数据

## 核心公式

- w = Rf + β × (Rm - Rf)
- d = 分红率 = D₀/E
- g = (1-d) × ROIC
- PE = d × (1+g) / (w - g)
- 预期收益率 = 股息率 + g

## 输出内容

- 资格筛选结果
- 核心参数（股息率、预期收益率）
- 内在价值
- 风险分析（股息风险、成长风险）
- 情景分析（零增长/3%增长PE）
- 投资建议
