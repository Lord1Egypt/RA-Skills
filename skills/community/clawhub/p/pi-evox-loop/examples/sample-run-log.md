# 示例运行日志（真实数据，脱敏）

> **EN**: A recorded session log showing the deposit -> approve -> recall loop end to end (terminal output as produced by the commands in `examples/quickstart.md`). Use it to see what each step prints and what the timeline records.


> 数据来源：本仓库作者的一次真实受控实验（GBK 确定性陷阱 / agnes-2.5-flash / --rounds 2）。
> 已移除本机绝对路径；其余数值与输出均为原始记录，未做修饰。

## 命令

```bash
node code/pi_evolve.mjs exp/encoding-trap-template examples/task-gbk.txt \
    --provider agnes-cn --model agnes-2.5-flash --api-key "$AGNES_CN_API_KEY" \
    --rounds 2 --fresh --auto-approve --llm-refine --root exp/loop-demo
```

## 关键输出（节选）

```
[stage] 已预置陷阱数据 <LAB>/data/events.jsonl
[inject] R2 使用 Pi 扩展注入（自动检测：扩展桥已激活），跳过 CLI append-system-prompt 以避免双通道重复注入

========== ROUND 1 (baseline) ==========
  Pi 执行任务 → read data/events.jsonl 报 UnicodeDecodeError（GBK 无效 UTF-8 字节，环境必然失败）
  → 自行探测编码后修复，产出正确结果（number of events: 8 / sum: 1005）

[distill] ✎ drafted UNPROVEN gene gene_distilled_65dec53a (sha256:9f869cdd…) — quarantined
          signals_match: bash, exception
[gate] 自动审核通过 gene_distilled_65dec53a（--auto-approve）
[llm-refine] strategy 已含修法信号词，无需重写

========== ROUND 2 (injected) ==========
  R2 会话启动时经扩展钩子注入已审核修法（[Evolver inherited fixes] 透明标注块）：
    - [repair] The file is GBK-encoded, not UTF-8. Let me fix the script: …
  → 首读即采用 bytes + 编码回退策略，0 错误完成

================ 跨轮对比 ================
round | injected | totalTokens | input | output | toolCalls | errors
1     | false    | 21269        | 16172 | 1001   | 10        | 1
2     | true     | 11850        | 11422 | 428    | 5         | 0

基线首轮 21269 → 末轮 11850（Δ -44.3%）
```

## 如何读这张表（诚实口径）

- **误差异常用精确口径**（`isError=true` 的 toolResult）：本轮 R1=1 → R2=0；
- **token 降幅 ≠ 全部继承收益**：重复执行同一任务本身有 ≈ -22% 的学习效应基线，-44.3% 中约一半来自继承注入与技能熟练度的叠加（本项目报告 §17 的配对对照给出净收益约 -30pp）；
- **单跑 token 方差 ±30%**：主指标请用「陷阱特异错误数」（如 `UnicodeDecodeError` 计数），token 作辅助。

## 复现提示

- 陷阱模板生成：`python traps/make_encoding_trap.py`（写入 `exp/encoding-trap-template/`）；
- 无注入对照组：去掉 `--fresh` 之外的注入来源（不配 `EVOLVER_REFINE_URL`、`.pi/extensions/` 下不放扩展桥）即可跑纯基线；
- 更多实验（跨陷阱类别、跨模型、N≥5 统计）见 `docs/experiment-report.md`。
