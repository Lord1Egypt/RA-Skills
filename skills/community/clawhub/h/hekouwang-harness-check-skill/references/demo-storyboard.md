# Harness Check 演示页与 GIF 分镜

## 目标

让访客在 30–60 秒内看到一条完整证据链：扫描一个真实 Harness → 分数不是测试数量 → 点击维度看到证据 → 看到真实失败/阻断 → 修复后通过 baseline 看到变化 → 宿主和人工边界仍然诚实保留。

## GIF 分镜

| 时间 | 画面 | 说清楚什么 |
| --- | --- | --- |
| 0–5s | 终端输入 `python3 harness_score.py ...` | 它检查的是仓库，不是让模型自评 |
| 5–12s | Score、Confidence、Maturity、Decision 四个指标出现 | 分数和置信度不是一回事 |
| 12–22s | 12 维横条从总分展开 | 检查规则、CI、安全、恢复、证据和回归 |
| 22–32s | 点击 `no_negative_regression` 或 `no_evidence_contract` | 缺关键证据会触发硬上限，长 README 也绕不过去 |
| 32–42s | 展开 `executions`，显示命令、exit code、N/M | 检查数量只从真实日志读取，不是质量分 |
| 42–50s | Host matrix 显示 configured / unknown | 配置存在不等于真实宿主触发 |
| 50–60s | 用 `--baseline` 重新扫描，显示 delta | 修复能留下可审计变化，可直接用于 CI/网页 |

## 网页最小数据模型

网页第一版只需要消费一个 JSON：

- 顶部指标：`score.value`、`score.confidence`、`score.maturity`、`score.decision`；
- 维度卡片：`dimensions[].earned`、`weight`、`status`、`signals[]`；
- 硬门槛：`score.caps[]`；
- 证据抽屉：`signals[].evidence`，只显示仓库相对路径和行号；
- 执行轨迹：`executions[]`，渲染 `command`、`exitCode`、`governanceCounts`、`failureLabels`；
- 宿主矩阵：`hosts[]` 的 `configured` 与 `smokeTest`；
- 内容领域卡：可选的 `profile.score`、`profile.controls[]`；
- 修复前后：可选的 `comparison.dimensionDeltas[]`。

不要把完整正文、提示词、敏感路径或外部平台 token 放进页面数据。页面应能在离线环境打开 JSON；真实宿主烟测和人工内容验收用明确的 `unknown` / `pending` 状态呈现。
