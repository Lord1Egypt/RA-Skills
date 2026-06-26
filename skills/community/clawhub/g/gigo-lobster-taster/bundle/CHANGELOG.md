# Changelog

## v2.0.0 - 2026-04-24

### 重大变更（Breaking）
- 评测形态从"prompt → text 黑盒"改为"临时工作目录 + CLI agent 真实操作"
- 题包从 `fallback_tasks.json` 单文件改为 `tasks/<id>/` 目录式
- AI judge 从本地调用改为云端 `/judge` 接口（rubric 永不下发）
- v1 与 v2 评分不可比；云端排行榜按 bundle_version 分桶

### 新增
- 50 题完整题库（30 行为题 + 20 对话题）
- 5 类评估器：pytest / state_hash / trace / rule / llm_judge
- 7 维度评分：肉质、脑子、爪子、壳、灵魂、钱包、脚力
- shell shim 与 risky_cmd 检测
- canary 文件机制
- canonical trace schema（多 agent 兼容）
- harness_reference 参考实现
- CI 自检脚本

### 已知限制
- 本期不含 pass^k 稳定性指标
- 不含 Docker 隔离（v2.1）
- 不含 prompt injection 大规模对抗集（v2.1）
