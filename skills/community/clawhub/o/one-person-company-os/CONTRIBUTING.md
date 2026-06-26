# Contributing

## What Good Contributions Look Like

- 强化“验证需求 -> MVP -> 小范围上线 -> 收反馈 -> 迭代 -> 增长”的可见主循环
- 保持回合、校准与阶段作为内部控制结构，而不是增加用户负担
- 提升中文工作区与中文角色说明的清晰度
- 减少不必要的重文档和无效复杂度
- 保持风险动作必须由创始人确认

## Before Opening A PR

- 保持改动聚焦
- 公共行为变化时更新 `README.md` 或 `SAMPLE-OUTPUTS.md`
- 脚本或模板变动时运行 `python3 scripts/validate_release.py`
- 不要重新引入以周复盘为中心的旧心智

## Basic Validation

From the repository root:

```bash
python3 scripts/init_company.py "北辰实验室" --path /tmp/opc-check --product-name "北辰助手" --stage 构建期 --target-user "独立开发者" --core-problem "还没有一个真正能持续推进产品和成交的一人公司系统" --product-pitch "一个帮助独立开发者把产品做出来并卖出去的一人公司控制系统" --confirmed
python3 scripts/start_round.py /tmp/opc-check/北辰实验室 --round-name "完成首页首屏" --goal "完成首页首屏结构与注册入口"
python3 scripts/validate_release.py
```
