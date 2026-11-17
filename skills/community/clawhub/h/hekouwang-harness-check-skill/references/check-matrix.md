# Harness 检查矩阵

本文件只解释现有检查入口的职责，不另建一套规则。规则和断言以 `.harness/scripts/`、`.harness/tests/` 与 `.harness/contracts/` 为准。

## 入口与范围

| 入口 | 运行范围 | 适用场景 | 关键边界 |
| --- | --- | --- | --- |
| `verify.sh --working-tree` | 工作区空白、Harness 总检查、Hook 配置、适配、Runtime Governance、可观测性、Task Contract、Safety Gate、Episode、失败台账 | 本地完整体检 | 会读取本机 Skill 和 Memory；Memory 未提交可以只是警告 |
| `verify.sh --staged` | 先检查暂存区；治理文件进入暂存区时运行完整 Harness | 提交前验收 | 普通内容改动可能只做暂存区空白检查 |
| `verify.sh --ci` | 使用仓库 fixture；跳过本机外部 Skill/Command 链接和内容 EP 实例 | CI 或可复现回归 | 不能证明本机宿主链接和真实宿主 Hook |
| `harness-check.sh --local` | 规则真源、薄适配、Skill、四端 Hook、生成物、Memory、治理契约、失败台账、Profile、文档链接 | 结构诊断 | 不是完整正反例回归 |
| `harness-check.sh --ci` | CI 可用的结构诊断 | 远端最小体检 | 使用 fixture Memory，跳过本机依赖 |

## Scorecard 与检查数量的关系

`harness_score.py` 是独立的量化和证据汇总入口，不复制 `verify.sh` 的断言。它可以先做静态扫描，也可以通过 `--mode` 调用目标仓库的真实验证入口；输出中的 `executions[].governanceCounts` 只记录日志观察到的数量，`score.value` 则由评分规则计算。

```bash
python3 harness_score.py /path/to/repo \
  --profile content-agent \
  --format json --output ./harness-scorecard.json \
  --mode working-tree --mode ci
```

建议把 JSON 作为网页、GIF 或 CI artifact 的唯一输入。不要从终端截图中手工抄分，也不要把一次运行的检查数量固化成质量基线。

## 当前数字的正确表述

Runtime Governance 会在 `test-runtime-governance.sh` 的当前仓库正例中输出检查数量。数量随断言变化，必须区分历史基线和当前结果：

- 基础闭环基线：本地 722 项、CI 165 项治理检查通过；
- 独立 Skill 早期参考快照：本地 728 项、CI 171 项治理检查通过；当前目标仓库应以实际日志为准。

这两个数字是输出中的当前观测值，不是 `verify.sh` 的永久总分，也不是整套内容质量得分。后续新增或删除断言后，必须以实际日志为准更新数字。

推荐写法：

> `verify.sh --working-tree` 自动化通过；其中 Runtime Governance 的具体数量以当次日志为准。四端真实宿主烟测仍需另行确认。

不推荐写法：

> Harness 722 分，所有事情都已完成。

## 最小审计记录

```text
模式：working-tree / staged / ci
提交：<git rev-parse HEAD>
入口：<完整命令>
自动化：通过 / 失败 / 警告
Runtime Governance：本地 N 项 / CI M 项 / 未输出
失败项：<原始标签与复现命令>
宿主烟测：已完成 / 待补，列出宿主和事件
人工验收：已完成 / 待补，列出视觉、事实、来源或外部副作用
```
