# 论文与开源引用

## 学术论文

### 核心方法论

| 论文 | 年份 | 贡献 | 在算法中的应用 |
|------|------|------|---------------|
| Kang et al. "Institutional Trading and Stock Market Microstructure" | 2025 | 机构持仓变动需按市值归一化 | `score_fund_flow()` 中 `norm_ratio = net_main_yi / mv_yi` |
| 量价趋势研究 | 2023 | A股放量上涨预测反转而非延续 | `score_volume_price()` 放量温和上涨降权至+30 |
| 国金证券研报 | 2022 | 缩量横盘是机构吸筹的典型模式 | `score_volume_price()` 缩量横盘加权至+55 |
| 上交大 散户交易行为研究 | 2019 | 散户净买入后1-20日显著跑输 | `score_fund_flow()` 散户跟风买入-15分 |
| Ravina "Individual Investor Activity and Performance" | 2023 | 散户订单流与未来收益负相关 | `score_fund_flow()` 主力买+散户卖+10分 |
| Campbell et al. | 2009 | 预测顶部比趋势难一个量级 | v11 砍掉卖出信号，改机械止损 |
| Campbell "Intraday Trading" | 2009 | 机构在开盘/收盘30分钟集中操作 | `analyze_intraday_pattern()` 尾盘/开盘放量检测 |
| 开源金工 | 2023 | 尾盘异常放量是机构行为关键特征 | `analyze_intraday_pattern()` 尾盘>35%=+20分 |

### 补充参考

| 论文/报告 | 贡献 |
|----------|------|
| Kang (2025) | 机构使用VWAP/TWAP算法，成交均匀 |
| 恒生指数联动研究 | 港A联动相关系数r=0.69 |
| 外部情绪回测 | r=0.069, p=0.028（弱但显著） |

## 开源项目引用

### 技术指标

| 项目 | 用途 | 算法中的实现 |
|------|------|-------------|
| [build-web/ta](https://github.com/build-web/ta) | OBV、CMF技术指标 | `calc_obv()`, `calc_cmf()` |
| [liumenglife/ChipDistribution](https://github.com/liumenglife/ChipDistribution) | 筹码分布计算 | `calc_chip_distribution()` |
| [Siva7891/smart-money-concepts](https://github.com/Siva7891/smart-money-concepts) | BOS/CHoCH结构检测 | `detect_structure_break()` |

### 数据源

| 数据源 | 用途 | 接口 |
|--------|------|------|
| Tushare (代理版) | 日线/资金流/融资/北向/分钟线 | `TushareFetcher` 全部接口 |
| NeoData | 辅助板块排名 | `NeoDataFetcher.query()` |
| YouTube RSS | 外部情绪(英文财经频道) | `sentiment_aggregator.py` |
| 东方财富/AKShare | 外部情绪(中文财经) | `sentiment_aggregator.py` |

## 引用格式 (BibTeX)

```bibtex
@article{kang2025institutional,
  title={Institutional Trading and Stock Market Microstructure},
  author={Kang, Wenjin and others},
  year={2025},
  note={资金流按市值归一化}
}

@article{campbell2009intraday,
  title={Intraday Trading Patterns and the Role of Institutional Investors},
  author={Campbell, John Y and others},
  year={2009},
  note={机构尾盘/开盘集中操作}
}

@techreport{sjtu2019retail,
  title={散户交易行为的信息含量研究},
  institution={上海交通大学},
  year={2019},
  note={散户净买入后跑输}
}

@article{ravina2023individual,
  title={Individual Investor Activity and Performance},
  author={Ravina, Enrichetta and others},
  year={2023},
  note={散户订单流与未来收益负相关}
}
```
