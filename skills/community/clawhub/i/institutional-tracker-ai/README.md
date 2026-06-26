# institutional-tracker-ai

AI链条机构建仓探测算法 — A股 AI 赛道（算力/芯片/大模型/应用）机构建仓行为识别系统。

## 核心特点

- **5维信号评分**：资金流(30%) + 量价(24%) + 筹码(18%) + 北向(16%) + 事件(12%)
- **统计显著**：544次买入信号，10日胜率55.3%（P=0.007），样本外59.0%（P=0.006）
- **论文支撑**：资金流市值归一化（Kang 2025）、量价反转逻辑、散户反向过滤
- **BEAR禁入**：熊市自动屏蔽所有买入信号
- **日内分钟线**：支持 Tushare Level-2 分钟K线分析
- **只做买入**：卖出信号已砍掉（41.9%=无效），改为机械止损-15%

## 安装

### CodeBuddy / WorkBuddy

```bash
# 直接在 WorkBuddy 中使用
# Skill 会被自动识别并加载
```

### 手动安装

```bash
bash scripts/install.sh ~/institutional_tracker
```

## 使用

```bash
# 每日扫描
cd ~/institutional_tracker && python3 main.py

# 大规模回测
cd ~/institutional_tracker && python3 backtest_v2.py
```

## 数据源

需要 Tushare 代理 Token（闲鱼约38元/月，15000积分权限）。

## 免责声明

本算法仅供研究参考，不构成投资建议。投资有风险，决策需谨慎。

## License

MIT License
