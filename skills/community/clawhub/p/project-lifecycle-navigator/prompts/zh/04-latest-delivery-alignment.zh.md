# 最新交付与当前目标对齐审查

本模式只审查一个当前交付边界，不重复执行全仓库审计。

## 输入

检查当前目标与验收标准、活动任务或 Work Order、最新交接、受影响源码与测试、当前 diff 或提交、验证配置，以及本次交付产生的证据。

## 审查规则

1. 保持只读。
2. 能确认时记录准确的提交、分支、脏工作树状态和交付边界。
3. 把每项完成声明与可观察验收及证据逐条对照。
4. 默认只检查本次交付必要的回归面；只有风险证据充分时才扩大范围。
5. 区分 implemented、partial、verified、unverified、unusable、documentation-conflict 和 not-executed。
6. `Developer Complete` 只是交接状态，不等于 `Accepted`。
7. 保持当前目标不变；目标变化必须转入 Owner 主导的重基线。

## 输出

- 本次审查的交付范围
- 当前目标与验收切片
- 已检查或执行的证据及最终退出状态
- 完成声明逐项对齐表
- 回归或用户可见缺口
- 文档或治理冲突
- 决定：Ready for Independent Acceptance、Needs Fix、Blocked 或 Cannot Confirm
- 限定范围的下一步和需要 Owner 决定的事项

本模式不得签署最终 QA 验收。
