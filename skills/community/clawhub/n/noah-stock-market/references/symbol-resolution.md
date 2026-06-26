# Symbol Resolution

## Supported Markets

一期默认只重点支持：
- 港股 `HK`
- 美股 `US`

## Standard Code Format

- 港股标准代码：`HK-00700`
- 美股标准代码：`US-AAPL`

## Input Normalization

用户可能输入：
- 中文名称：腾讯控股、苹果、英伟达
- 英文名称：Tencent, Apple, NVIDIA
- 裸代码：00700、AAPL、NVDA
- 标准代码：HK-00700、US-AAPL

执行时应尽量统一为标准代码再请求接口。

## Resolution Rules

1. 如果已经是 `HK-xxxxx` / `US-xxxxx`，直接使用。
2. 如果是 5 位左右纯数字代码，优先按港股候选处理，例如 `00700 -> HK-00700`。
3. 如果是纯字母代码，优先按美股候选处理，例如 `AAPL -> US-AAPL`。
4. 对高频名称可先用本地 hint 做第一轮映射，例如：腾讯控股→HK-00700、苹果→US-AAPL、英伟达→US-NVDA。
5. 如果是中文名或英文名，优先通过基础信息或名称匹配能力解析后再转标准代码。
6. 如果名称存在歧义，不要猜，先让用户确认。

## Ambiguity Examples

- “阿里巴巴” 可能对应美股或港股
- “腾讯” 可能需要明确是否腾讯控股
- “苹果” 默认候选可能是 `US-AAPL`，但仍应允许用户纠正

## Output Rule

对用户回复时，可以同时展示：
- 股票名称
- 标准代码
- 市场

例如：
- 腾讯控股（HK-00700）
- Apple Inc.（US-AAPL）
