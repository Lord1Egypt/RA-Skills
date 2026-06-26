# Panda Data Skill

本目录为 **ClawHub 技能包**。

- **安装全流程（OpenClaw / pip / 凭证）**：请优先阅读 **[INSTALL_GUIDE.md](INSTALL_GUIDE.md)**（结构与 [Tushare Skills 安装指南](https://tushare.pro/document/1) 类似，便于对照）。
- 仓库根目录说明见 [项目 README](../README.md)。

## 目录结构

```
panda-data-skill/
├── SKILL.md            # 技能元信息（ClawHub 必须）
├── README.md           # 本文档
├── INSTALL_GUIDE.md    # 安装指南（panda_data + panda-data-tools + 凭证）
├── CHANGELOG.md        # 版本变更记录
├── api_reference.md    # API 详细参考
└── scripts/call_tool.py
```

## 安装

见 [项目 README - 安装](../README.md#安装)

## 凭证配置

见 [项目 README](../README.md#使用方式)

## 快速开始

见 [项目 README - 使用方式](../README.md#使用方式)

## API 分类概览

| 分类 | 方法数 | 说明 |
|------|--------|------|
| market_data | 2 | 日线、分钟级行情 |
| market_ref | 20 | 股票/指数/概念/行业/龙虎榜等 |
| financial | 5 | 业绩预告、财务报告、因子、复权 |
| trade | 5 | 交易日历、在售股票等 |
| futures | 3 | 期货基本信息、后复权、主力合约 |

## 示例脚本

```bash
python scripts/call_tool.py get_market_data start_date=20250101 end_date=20250110 symbol=000001.SZ
```

## 功能对比

| 功能 | v1.0.0 | v2.0.0 |
|------|--------|--------|
| 35 个 API 封装 | ✓ | ✓ |
| 凭证管理 | ✓ | ✓ |
| DuckDB 缓存 | — | ✓ |
| 数据导出 | — | ✓ |

## 版本信息

- 当前版本：2.0.0
- 变更记录：[CHANGELOG.md](CHANGELOG.md)
