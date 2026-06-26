---
name: portfolio-diagnosis (Public)
description: 持仓诊断技能(Tushare驱动版)——专为A股投资者设计。当用户说"帮我诊断持仓"、"看看我的股票组合"、"仓位合理吗"、"持仓风险大吗"、"我的组合夏普比率多少"时触发。使用Tushare
  SDK获取实时行情和历史数据，进行包含波动率、Beta、夏普比率、最大回撤在内的量化风险诊断，并生成专业诊断报告,包含：英雄区 + 综合评分环形图;持仓概览关键指标卡片;个股明细表格（含仓位进度条）;四大量化指标卡片（波动率/Beta/夏普/回撤）;四张交互式
  Chart.js 图表（雷达图/饼图/柱状图/盈亏对比）;六维诊断卡片、风险提示、优化建议;得分明细条形图。
skill_key: portfolio_diagnosis_public
original_skill_key: portfolio_diagnosis
input_format: "支持以下格式输入持仓数据：\n\n格式1 - 文本格式：\n股票名称 | 买入均价 | 现价 | 持仓数量\n贵州茅台 | 1650\
  \ | 1720 | 100\n五粮液 | 135.5 | 142 | 500\n\n格式2 - JSON格式：\n{\n  \"holdings\": [\n\
  \    {\"code\": \"600519\", \"name\": \"贵州茅台\", \"cost\": 1650, \"shares\": 100},\n\
  \    {\"code\": \"000858\", \"name\": \"五粮液\", \"cost\": 135.5, \"shares\": 500}\n\
  \  ]\n}\n"
trigger:
- 帮我诊断持仓
- 看看我的股票组合
- 仓位合理吗
- 我的持仓有没有问题
- 帮我分析一下我买的股票
- 持仓风险大吗
- 帮我做风险分析
- 我的组合夏普比率多少
- 诊断一下我的持仓
---
本技能为 Prana 封装共享包：`skill_key`（`portfolio_diagnosis_public`）为公开包标识；`original_skill_key`（`portfolio_diagnosis`）为 Prana 上实际调用的专业技能。

运行方式：使用 `scripts/prana_skill_client.py` 或渠道集成入口。

