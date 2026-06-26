---
name: quant-tools
description: 学术导向量化研究工具集。包含7大核心库（因子分析、组合优化、AI增强、因果验证、衍生品定价、回测引擎、情感分析）和5大投研工具（VeighNa交易框架、Qlib AI投研、WTP高性能框架、AkShare数据接口、JupyterHub研究环境）。适用于策略研发、因子挖掘、论文复现、资产配置、API服务化等投研任务。触发词：量化、quant、因子、组合优化、因子分析、回测、交易框架、数据接口、学术研究。
---

# 量化投研工具集 (Quant Tools)

## 概述

本 skill 提供完整的量化投研工具链，覆盖：
- **学术研究库** (7个): 算法创新、数学模型验证、理论实现
- **投研工具** (5个): 交易执行、AI研究、数据获取、团队协作

---

## 学术研究库

### 1. AlphaLens - 因子分析
- **定位**: Quantopian 开源，经典因子评估框架
- **功能**: 因子 IC、IR、分层回测指标
- **用途**: 因子有效性检验、多因子模型评估
- **GitHub**: https://github.com/quantopian/alphalens
- **API化**: ⭐⭐⭐⭐ 极易封装为报告生成 API

### 2. VectorBT - 高性能回测
- **定位**: 基于 NumPy/Pandas 向量化计算
- **功能**: 参数网格搜索、敏感性分析
- **用途**: 大规模因子测试、快速验证
- **GitHub**: https://github.com/polakowo/vectorbt
- **API化**: ⭐⭐⭐⭐ 可封装回测引擎 API
- **注意**: 内存占用大，需计算优化型实例

### 3. PyPortfolioOpt - 组合优化
- **定位**: 现代投资组合理论 (MPT)
- **功能**: Black-Litterman、风险平价、权重优化
- **用途**: 资产配置研究、权重优化服务
- **GitHub**: https://github.com/robertmartin8/PyPortfolioOpt
- **API化**: ⭐⭐⭐⭐ 极易封装为计算 API

### 4. FinRL - 强化学习交易
- **定位**: 斯坦福/CMU 等多校联合
- **功能**: PPO、A2C 等 RL 算法，环境丰富
- **用途**: AI策略生成、强化学习论文复现
- **GitHub**: https://github.com/AI4Finance-Foundation/FinRL
- **API化**: ⭐⭐⭐ 需封装训练/推理接口
- **注意**: 训练不稳定，超参敏感

### 5. FinBERT - 金融情感分析
- **定位**: 基于 BERT 的金融领域微调
- **功能**: 金融语境情感分析
- **用途**: 舆情监控、新闻因子挖掘
- **GitHub**: https://github.com/ProsusAI/finBERT
- **API化**: ⭐⭐⭐ 需封装模型推理 API
- **注意**: 需要 GPU，推理延迟较高

### 6. EconML - 因果推断
- **定位**: 微软研究院
- **功能**: 因果效应分析、策略归因
- **用途**: 验证策略是否真的有效、避免过拟合
- **GitHub**: https://github.com/microsoft/EconML
- **API化**: ⭐⭐⭐⭐ 适合封装为分析 API
- **重要性**: **必须使用以验证策略有效性**

### 7. QuantLib - 衍生品定价
- **定位**: 经典量化金融数学
- **功能**: 期权、利率、信用定价
- **用途**: 复杂结构化产品研究、风险模型验证
- **GitHub**: https://github.com/lballabio/QuantLib
- **API化**: ⭐⭐⭐ PyQL 封装后可提供 API
- **注意**: 学习曲线极陡

---

## 投研工具

### 1. VeighNa (vn.py) - 综合交易框架
- **定位**: 社区最活跃的综合交易与投研框架
- **功能**: 期货/股票/crypto接口、插件丰富
- **用途**: 实盘交易、策略回测、云端交易网关
- **GitHub**: https://github.com/vnpy/vnpy
- **部署**: ⭐⭐⭐⭐⭐ 官方 Docker/K8s
- **API**: ⭐⭐⭐⭐ 内置 RpcService，可封装 REST

### 2. Microsoft Qlib - AI量化投研
- **定位**: 微软开源 AI 量化平台
- **功能**: Transformer/LSTM、因子挖掘、流程标准化
- **用途**: 机器学习模型训练、Alpha研究
- **GitHub**: https://github.com/microsoft/qlib
- **部署**: ⭐⭐⭐⭐⭐ 支持分布式训练
- **API**: ⭐⭐⭐ 库形式，需自行封装 FastAPI

### 3. WonderTrader (WTP) - 高性能框架
- **定位**: C++核心高性能量化框架
- **功能**: Tick级回测、低延迟
- **用途**: 高频策略、对性能要求高的回测
- **GitHub**: https://github.com/wondertrader/wondertrader
- **部署**: ⭐⭐⭐⭐ Docker支持，资源占用低
- **API**: ⭐⭐⭐⭐ HTTP监控，易扩展微服务

### 4. AkShare - 金融数据接口
- **定位**: 完全免费的金融数据接口库
- **功能**: 宏观/基金/股票数据源覆盖极广
- **用途**: 数据获取、基本面数据清洗、统一数据源
- **GitHub**: https://github.com/akfamily/akshare
- **部署**: ⭐⭐⭐⭐ 无状态，极易容器化
- **API**: ⭐⭐⭐ 库形式，建议封装为数据网关 API
- **注意**: 依赖第三方网站稳定性

### 5. JupyterHub - 交互式研究环境
- **定位**: 分析师零成本上手
- **功能**: Notebook、团队协作
- **用途**: 数据探索、研究报告生成、团队协作开发
- **GitHub**: https://github.com/jupyterhub/jupyterhub
- **部署**: ⭐⭐⭐⭐⭐ 原生支持 K8s 多用户
- **API**: ⭐⭐⭐⭐ 可通过 Papermill/Voila 转 API

---

## 推荐组合方案

| 需求场景 | 推荐组合 |
|---------|---------|
| 实盘交易 + 基础回测 | VeighNa |
| AI选股/因子研究 | Qlib + FastAPI |
| 资产配置优化 | PyPortfolioOpt |
| 因果验证(防过拟合) | EconML |
| 高频策略 | WonderTrader |
| 数据中台 | AkShare + ClickHouse |
| 团队协作研究 | JupyterHub + VeighNa/Qlib |
| 完整投研平台 | 学术库组合 + FastAPI封装 |

---

## 完整投研架构

```
数据层: AkShare
    ↓
因子分析层: AlphaLens + VectorBT
    ↓
策略优化层: PyPortfolioOpt
    ↓
AI增强层: FinRL / FinBERT
    ↓
因果验证层: EconML (必须!)
    ↓
服务封装: FastAPI + Docker
    ↓
可选: VeighNa (实盘) / Qlib (AI研究)
```

---

## 使用示例

### 因子有效性分析
```
使用 AlphaLens 分析 [因子名称] 的 IC、IR 表现
```

### 组合优化
```
使用 PyPortfolioOpt 基于 [风险偏好] 优化 [资产列表] 的权重
```

### 因果验证
```
使用 EconML 验证 [策略] 是否真的有效，用因果推断排除过拟合
```

### 回测验证
```
使用 VectorBT 对 [策略] 进行大规模参数扫描和敏感性分析
```

### 舆情因子
```
使用 FinBERT 分析 [公司/行业] 的新闻情感作为因子
```

### 强化学习策略
```
使用 FinRL 训练 [市场环境] 下的强化学习交易策略
```

### 数据获取
```
使用 AkShare 获取 [股票/宏观/基金] 的 [数据类型]
```

---

## 注意事项

### 过拟合风险
- 学术库易在历史数据上完美表现，实盘失效
- **务必使用 EconML 或出样本测试验证**

### 计算资源
- VectorBT 和 FinBERT 对资源要求高
- 建议计算优化型实例

### 依赖管理
- QuantLib/PyQL 环境复杂
- 建议用 Conda 管理环境并打包 Docker

### 合规风险
- 仅用于内部投研
- 避免涉及公开荐股或非法经营证券业务

### API 封装
- 大多数工具是 Library 而非 Service
- 需要用 FastAPI 进行封装
- 网络安全：Nginx反向代理 + HTTPS + API Key认证
