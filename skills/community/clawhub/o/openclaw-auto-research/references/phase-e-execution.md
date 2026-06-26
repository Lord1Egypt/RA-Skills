# Phase E: Experiment Execution (S12-S13)

## S12: EXPERIMENT_RUN — 实验执行

### 输入
- `stage-10/experiment.py`（及其他代码文件）

### 产出
- `stage-12/runs/run-1.json` — 实验结果（JSON 格式的 metrics）

### 特殊：需要 exec 执行代码

这个 stage 不是纯 LLM 调用，需要用 `exec` 在沙盒中运行实验代码。

### 执行步骤

1. 将 `stage-10/` 下的所有 .py 文件复制到临时执行目录
2. 用 `exec` 运行主实验脚本：
   ```bash
   cd /tmp/researchclaw_sandbox && timeout 300 python3 experiment.py 2>&1
   ```
3. 捕获 stdout 中的 JSON metrics 输出
4. 将运行结果（stdout, stderr, exit_code, duration）写入 `stage-12/runs/run-1.json`
5. 如果运行失败（非零退出码或超时），记录错误信息
6. 推送中文摘要（运行是否成功、耗时、是否有 metrics 输出）

### 超时和安全

- 最大运行时间：300 秒
- 不允许网络访问（纯本地计算）
- 不允许写入实验目录以外的路径

---

## S13: ITERATIVE_REFINE — 迭代优化

### 输入
- `stage-12/runs/` — 实验运行结果
- `stage-10/` — 原始代码

### 产出
- `stage-13/experiment_final.py` — 优化后的最终代码
- `stage-13/refinement_log.json` — 迭代日志

### 机制：LLM 分析 → 修复 → 重跑循环

最多迭代 10 轮，每轮：

1. **分析**：将上一轮的运行结果（stdout/stderr/metrics）发送给 LLM
2. **修复**：LLM 生成修改后的代码
3. **验证**：AST 语法检查
4. **重跑**：exec 执行修改后的代码
5. **判断**：如果 metrics 改善则保留，否则回退

### LLM 修复 Prompt

**System:**
```
You are a debugging expert. Fix the experiment code based on the error output.
```

**User:**
```
The experiment code produced the following output:
stdout: {stdout}
stderr: {stderr}
exit_code: {exit_code}
duration: {duration}s

Original code:
{code}

Fix the code so it:
1. Runs without errors
2. Produces valid JSON metrics to stdout
3. Completes within 300 seconds

Return the complete fixed code.
```

### 收敛条件

停止迭代的条件（任一满足）：
- 连续 2 轮没有 metrics 改善
- 代码运行成功且产出有效 metrics
- 达到最大迭代次数（10）

### 执行步骤

1. 读取 `stage-12/runs/run-1.json` 获取初始运行结果
2. 如果运行成功且有 metrics → 直接进入 S14
3. 如果失败 → 进入迭代循环
4. 每轮：分析 → LLM 修复 → 验证 → 重跑
5. 保存最终代码到 `stage-13/experiment_final.py`
6. 保存迭代日志到 `stage-13/refinement_log.json`
7. 推送中文摘要（迭代了多少轮、最终是否成功）
