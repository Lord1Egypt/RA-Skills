# go-stargazing 范围扫描策略

更新日期：2026-03-28

## 核心原则

### 1. 以实际天气扫描结果为准
候选区域必须先来自当前查询范围内的实际天气扫描结果，不能先靠人工经验预设“热门地点子集”代替主流程扫描。

### 2. spot check 不能冒充主流程
手工地点复核、热门地点抽查、经验点位验证，都只能视为补充检查；不能拿来代表全国或区域级默认结论。

### 3. 全国问题默认全国扫描
如果用户没有指定省份/区域：
- 默认按全国范围（或明确声明的全国 box 集合）扫描
- 不能私自缩成西部、热门区、传统拍星地等少数候选集

## 输出要求

每次正式输出都应带：
- `scope_mode`
  - `national`
  - `regional`
  - `point_check`
- `scope_coverage`
  - 本次实际扫描的省份 / box / 点位说明
- `scope_reduction_reason`
  - 若无缩范围，填 `none`
  - 若是看起来像“局部全国子集”，填 `partial_national_subset`
- `scope_guardrail`
  - 对 national 范围做覆盖完整性自检
  - 在 `--strict-national-scope` 下可直接阻止可疑 national 输出

## 推荐解释口径

- 主流程：真实范围扫描
- 补充复核：spot check / refinement / manual probe
- 不能把补充复核结果包装成主流程结论
