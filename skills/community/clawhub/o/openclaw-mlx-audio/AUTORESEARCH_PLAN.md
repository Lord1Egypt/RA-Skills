# openclaw-mlx-audio 改进计划
**目标**: 使用 autoresearch 循环改进 openclaw-mlx-audio

---

## 改进目标

### Goal 1: 提高 TTS 成功率到 99%
```
Goal: Improve TTS success rate to 99%
Scope: src/index.ts, python-runtime/tts_server.py
Metric: Success rate percentage (higher is better)
Verify: Run TTS 10 times, count successes
Direction: maximize

### Goal 2: 降低 STT 延迟到 <10 秒
Goal: Reduce STT transcription latency to under 10 seconds for 1-minute audio
Scope: src/index.ts, python-runtime/stt_server.py
Metric: Average latency in seconds (lower is better)
Verify: time / mlx-stt transcribe /tmp/1min-audio.wav | grep real
Direction: minimize

### Goal 3: 添加完整的测试覆盖
Goal: Add comprehensive test coverage for TTS/STT
Scope: test/**/*.ts, test/**/*.py
Metric: Test coverage percentage (higher is better)
Verify: bun test --coverage | grep "Line coverage"

### Goal 4: 改进错误处理
Goal: Improve error handling with clear messages and recovery
Scope: src/index.ts
Metric: Number of unhandled errors (lower is better)
Verify: Run error scenarios, count graceful failures

## 使用 autoresearch 循环

### 运行改进循环
```bash
/autoresearch
Goal: Improve openclaw-mlx-audio TTS/STT reliability and performance
Scope: src/index.ts, python-runtime/*.py
Metric: Combined score (success rate * 0.5 + (30 - latency) * 0.3 + coverage * 0.2)
Verify: ./test/run_all_tests.sh
Iterations: 20

## 基线测量

### 当前状态 (Iteration 0)
TTS 成功率, 值=?%, 目标=99%
STT 延迟, 值=?s, 目标=<10s
测试覆盖, 值=?%, 目标=80%
错误处理, 值=?/10, 目标=9/10

## 日志格式
```tsv
iteration commit metric delta status description
0 abc123 75.0 0.0 baseline initial state
1 def456 78.5 +3.5 keep add retry logic
2 - 76.2 -2.3 discard changed model (broke compatibility)
3 ghi789 82.1 +5.9 keep improve error handling

# 计划向导
/autoresearch:plan

# 调试
/autoresearch:debug

# 修复
/autoresearch:fix

# 安全审计
/autoresearch:security

# 发布
/autoresearch:ship

**创建时间**: 2026-03-20
**基于**: uditgoenka/autoresearch