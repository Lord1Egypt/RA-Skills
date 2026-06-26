# Current Status Summary

## What is already in place

> 说明：该 skill 的可运行性依赖公司行情服务的 API token。没有 `NOAH_MARKET_APIKEY` 时，只能查看 skill 结构与文档，不能执行真实查询。


- `SKILL.md`：定义 skill 的触发边界、范围和执行规则
- `references/`：已拆分意图映射、鉴权、行情、K线、盘口、资金流向、限制说明、输出模板、使用说明
- `scripts/quote_client.py`：统一 API 访问
- `scripts/normalize_symbol.py`：代码标准化与少量名称 hint
- `scripts/summarize_market.py`：结构化摘要
- `scripts/format_market_text.py`：用户可读文本输出
- `scripts/run_query.py`：统一查询入口
- `scripts/route_query.py`：自然语言路由入口
- `scripts/smoke_test.py`：接口级 smoke test
- `scripts/nl_smoke_test.py`：自然语言 smoke test

## Verified One-Phase Capabilities

- 港股：快照、市场状态、全局市场状态、分时、逐笔、经纪队列、K线、时间区间 K 线、资金流向、基础信息、交易日历、IPO 列表、排行榜、财务数据、股东增减持
- 美股：分析接口 `us_analysis` 已验证可用；财务数据已验证可用
- 自然语言问法：腾讯相关主路径已基本可用
- 枚举协议：已将 `openapi.yaml / enum.yaml / entity.yaml` 沉淀到 skill references，并开始按 enum 严格取值；财务与股东增减持场景已确认需取 `x-enum-varnames`

## Not Yet Ready For Phase-1 Promise

- 股东增减持按时间范围查询（`shareholder_inc_red_hold_by_date`）尚未接入主脚本
- 美股 K 线（当前环境仍需继续确认）

## Recommended Next Step

如果继续开发，优先方向：
1. 排查美股 K 线 404 根因
2. 增强名称解析，减少对本地 hint 的依赖
3. 将 `run_query.py` / `route_query.py` 嵌入真正的 agent 调用流程
