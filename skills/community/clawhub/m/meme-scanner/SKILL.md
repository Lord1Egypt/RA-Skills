---
name: meme-scanner
version: 2.0.0
description: "基于 GMGN 官方 API 的 Meme 币扫链工具。自动扫描热门代币，进行 AI 评分与风险分析，并推送格式化通知。完全使用 GMGN API，数据准确可靠。"
---

# Meme Scanner v2.0 - 基于 GMGN 官方 API

## 概述

此技能提供全自动化的 Meme 币扫描和分析解决方案。完全使用 GMGN 官方 API，通过浏览器 CDP 绕过 Cloudflare，实现高效准确的数据抓取。

## 核心改进 (v2.0)

### 重大更新
- ✅ 完全使用 GMGN 官方 API
- ✅ 移除 Ave.ai 依赖
- ✅ 通过浏览器 CDP 绕过 Cloudflare
- ✅ 数据更准确可靠
- ✅ 更快的响应速度

## 核心能力

### 1. 数据源
- **GMGN Rank API**: 扫描 1小时交易最活跃代币
- **GMGN Gainers API**: 扫描 24小时涨幅榜
- **GMGN Token API**: 获取代币详细信息
- **GMGN Security API**: 安全检测
- **GMGN Stat API**: 持有者统计

### 2. 智能筛选条件
- 市值：$10K - $5M
- 流动性：≥ $4K
- 持有者：≥ 50
- 24小时涨幅：≥ 100%
- 交易量/市值比：≥ 30%
- Bundler 比例：≤ 50%
- 非蜜罐
- Early Score：≥ 8/10

### 3. AI 评分系统
- **Early Score (1-10分)**: 综合评估代币潜力
  - 流动性评分
  - 市值评分
  - 持有者评分
  - 交易量评分
  - 涨幅评分
  - Bundler 惩罚

### 4. 风险识别
- Bundler 比例过高
- Top10 持仓集中度
- 流动性不足
- 税率异常

## 使用说明

### 前置条件

需要配置浏览器 CDP 连接（与 Token Analyzer 相同）：

1. 启动带插件的 Chrome（端口 9222）
2. 配置 OpenClaw 连接到远程 Chrome
3. 确保 websockets 依赖已安装

详细配置请参考 Token Analyzer 技能文档。

### 执行方式

#### 1. 手动执行
```bash
python3 /root/.openclaw/workspace/skills/meme-scanner/scripts/meme_scanner_v2.py
```

#### 2. 定时任务（推荐）
通过 OpenClaw cron 设置定时扫描：
```bash
# 每小时扫描一次
openclaw cron add --schedule "0 * * * *" --task "扫描 Meme 币"
```

### 输出格式

脚本输出 JSON 数组，每个元素是格式化的 Markdown 消息：

```json
[
  "🔔 扫链发现 | SOL\n**Token Name ($SYMBOL)**\n\nCA: ...\n...",
  "🔔 扫链发现 | BSC\n**Token Name ($SYMBOL)**\n\nCA: ...\n..."
]
```

## 技术说明

### 依赖
- Python 3.7+
- websockets
- urllib (标准库)

### API 接口
使用以下 GMGN API：
- `/defi/quotation/v1/rank/{chain}/swaps/1h` - 交易活跃榜
- `/defi/quotation/v1/rank/{chain}/gainers/24h` - 涨幅榜
- `/vas/api/v1/search_v3` - 代币搜索
- `/api/v1/mutil_window_token_security_launchpad` - 安全检测
- `/api/v1/token_stat` - 持有者统计
- `/api/v1/mutil_window_token_link_rug_vote` - 社交链接

### 去重机制
- 使用 `scanned_tokens.json` 记录已扫描代币
- 24小时内不重复推送同一代币
- 自动清理过期记录

## 配置调整

可在脚本中调整以下参数：

```python
MIN_MCAP = 10000        # 最小市值
MAX_MCAP = 5000000      # 最大市值
MIN_LIQUIDITY = 4000    # 最小流动性
MIN_HOLDERS = 50        # 最小持有者
MIN_CHANGE_24H = 100    # 最小24h涨幅
MIN_VOL_MCAP_RATIO = 0.3  # 最小交易量/市值比
MAX_BUNDLER_RATE = 0.5  # 最大Bundler比例
MIN_EARLY_SCORE = 8     # 最小早期得分
```

## 更新日志

### v2.0.0 (2026-03-05)
- ✅ 完全重构为使用 GMGN 官方 API
- ✅ 移除 Ave.ai 依赖
- ✅ 通过浏览器 CDP 绕过 Cloudflare
- ✅ 优化筛选逻辑
- ✅ 改进评分算法
- ✅ 更准确的数据

### v1.0.0
- 初始版本
- 使用 gmgn.ai + Ave.ai
