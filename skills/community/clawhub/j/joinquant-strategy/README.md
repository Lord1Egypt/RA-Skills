# joinquant-strategy Skill

帮助在Cursor中编写聚宽(JoinQuant)量化策略的工具集。

## 主要功能
- 提供聚宽策略的标准模板
- 包含常用代码片段
- 提供API快速参考
- 集成最佳实践示例

## 目录结构

```
joinquant-strategy/
├── README.md            # Skill 说明文档
├── templates/           # 策略模板目录
│   ├── basic_template.py            # 基础策略模板
│   ├── dual_strategy_template.py    # 双策略模板
│   └── etf_rotation_template.py     # ETF轮动策略模板
├── snippets/            # 代码片段目录
│   ├── data_fetching.md       # 数据获取常用代码
│   ├── order_handling.md      # 下单处理代码
│   ├── risk_control.md        # 风险控制代码
│   └── technical_analysis.md  # 技术分析代码
├── api_reference/       # API参考文档
│   ├── core_functions.md      # 核心函数说明
│   ├── data_functions.md      # 数据获取函数说明
│   └── order_functions.md     # 下单函数说明
└── examples/            # 示例策略
    └── momentum_etf_strategy.py    # 动量ETF策略
```

## 功能说明

### 策略模板
- **basic_template.py**: 基础策略模板，包含完整的策略结构和基本逻辑
- **dual_strategy_template.py**: 双策略模板，基于示例实现的双策略框架
- **etf_rotation_template.py**: ETF轮动策略模板，用于实现ETF轮动交易策略

### 代码片段
- **data_fetching.md**: 数据获取常用代码，包括历史数据、财务数据等获取方法
- **order_handling.md**: 下单处理代码，包括委托下单、撤单等操作
- **risk_control.md**: 风险控制代码，包括止损、止盈、仓位管理等
- **technical_analysis.md**: 技术分析代码，包括常用技术指标计算

### API参考文档
- **core_functions.md**: 核心函数说明，包括策略初始化、运行等核心功能
- **data_functions.md**: 数据获取函数说明，详细介绍数据API的使用方法
- **order_functions.md**: 下单函数说明，详细介绍下单API的使用方法

### 示例策略
- **momentum_etf_strategy.py**: 动量ETF策略，基于示例整理的完整策略实现

## 使用方法

在Cursor中使用此skill时，可以：

1. **快速开始**：使用`/template`命令选择策略模板
2. **代码补全**：输入`/snippet`查看常用代码片段
3. **API查询**：输入`/api 函数名`快速查看API用法
4. **最佳实践**：参考`examples/`目录学习复杂策略的编写

## 注意事项

- 本工具包提供的代码和模板仅供参考，实际使用时需要根据具体情况进行调整
- 策略开发过程中，应注意风险管理和回测验证
- 请遵守 JoinQuant 平台的相关规定和限制

## 版本信息

- 版本: 1.0.0
- 最后更新: 2026-03-10
