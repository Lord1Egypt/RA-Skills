# 使用 autoresearch 改进 openclaw-mlx-audio
**安装时间**: 2026-03-20
**基于**: uditgoenka/autoresearch (v1.7.5)

---

## 已安装

### SKILLS
```
~/.openclaw/skills/autoresearch/
├── SKILL.md # 主技能定义
└── references/ # 参考文档
 ├── autonomous-loop-protocol.md
 ├── core-principles.md
 ├── plan-workflow.md
 ├── security-workflow.md
 ├── ship-workflow.md
 ├── debug-workflow.md
 ├── fix-workflow.md
 ├── scenario-workflow.md
 ├── predict-workflow.md
 └── results-logging.md

### Commands
~/.openclaw/commands/
├── autoresearch.md # 主命令
└── autoresearch/
 ├── plan.md # /autoresearch:plan
 ├── security.md # /autoresearch:security
 ├── ship.md # /autoresearch:ship
 ├── debug.md # /autoresearch:debug
 ├── fix.md # /autoresearch:fix
 ├── scenario.md # /autoresearch:scenario
 └── predict.md # /autoresearch:predict

## 快速开始

### 1. 运行自主改进循环
```bash
/autoresearch
Goal: Improve openclaw-mlx-audio TTS/STT reliability to 99% success rate
Scope: src/index.ts, python-runtime/tts_server.py, python-runtime/stt_server.py
Metric: Test success rate percentage (higher is better)
Verify: bash /Users/user/.openclaw/workspace/openclaw-mlx-audio/test/run_tests.sh
Direction: maximize
Iterations: 20

### 2. 使用计划向导
如果不知道如何定义指标:

/autoresearch:plan
Goal: Make the TTS/STT more reliable and faster

向导会帮你:
1. 分析代码库
2. 建议合适的指标
3. 定义验证命令
4. 干运行验证

### 3. 调试模式
如果遇到问题:

/autoresearch:debug
Symptom: TTS fails intermittently with timeout errors
Scope: src/index.ts, python-runtime/tts_server.py
Iterations: 15

### 4. 自动修复
调试后自动修复:

/autoresearch:fix --from-debug
Iterations: 30

### 5. 安全审计
发布前安全检查:

/autoresearch:security
Scope: python-runtime/*.py, src/index.ts
Iterations: 10

### 6. 发布准备
准备发布到 ClawHub:

/autoresearch:ship --auto
Type: code-release

## 改进目标

### 当前优先级
TTS 成功率, 当前=?%, 目标=99%, 优先级=P0
STT 成功率, 当前=?%, 目标=99%, 优先级=P0
TTS 延迟, 当前=?s, 目标=<5s, 优先级=P1
STT 延迟, 当前=?s, 目标=<10s, 优先级=P1
测试覆盖, 当前=?%, 目标=80%, 优先级=P1
错误处理, 当前=?/10, 目标=9/10, 优先级=P2

# 综合改进
Goal: Improve overall openclaw-mlx-audio quality
Scope: src/index.ts, python-runtime/*.py
Metric: bash test/run_tests.sh | grep COMBINED_SCORE | cut -d= -f2
Verify: bash test/run_tests.sh

# 专注 TTS
Goal: Improve TTS success rate to 99%
Metric: bash test/run_tests.sh | grep SUCCESS_RATE | cut -d= -f2

# 专注性能
Goal: Reduce TTS latency to under 5 seconds
Metric: bash test/run_tests.sh | grep TTS_LATENCY | cut -d= -f2
Direction: minimize

## 结果追踪

### TSV 日志格式
每次迭代自动记录到 `results.tsv`:

```tsv
iteration commit metric delta status description
0 abc123 75.00 0.00 baseline initial state
1 def456 78.50 +3.50 keep add retry logic with exponential backoff
2 - 76.20 -2.30 discard changed default model (broke compatibility)
3 ghi789 82.10 +5.90 keep improve error handling and messages
4 jkl012 85.30 +3.20 keep add timeout protection
5 mno345 88.70 +3.40 keep optimize CLI argument parsing

### 进度摘要
每 10 次迭代自动打印:

 Progress Summary (Iterations 1-10):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Baseline: 75.00
Best: 88.70 (+13.70)
Current: 88.70
Kept: 4
Discarded: 1
Skipped: 0

## ️ 安全保护

### 使用 Guard 防止回归
Goal: Optimize TTS performance
Verify: bash test/run_tests.sh | grep TTS_LATENCY
Guard: bash test/run_tests.sh | grep "Success Rate" | grep -E "([89][0-9]|100)\.00%"

Guard 确保优化不会降低成功率.

## 8 条关键规则
在改进过程中始终遵守:

1. **Loop until done** - 循环直到完成(无限制:永远,有限制:N 次)
2. **Read before write** - 修改前阅读完整上下文
3. **One change per iteration** - 每次迭代一个原子改动
4. **Mechanical verification only** - 只用机械验证,不用主观判断
5. **Automatic rollback** - 失败自动回滚
6. **Simplicity wins** - 同等结果,更简单代码 = 保持
7. **Git is memory** - Git 提交保存历史
8. **When stuck, think harder** - 卡住时更深入思考

## 参考文档
- **autoresearch**: https://github.com/uditgoenka/autoresearch, **Karpathy's original**: https://github.com/karpathy/autoresearch, **完整指南**: `~/.openclaw/skills/autoresearch/references/`

# 主循环
/autoresearch [Goal: ... Scope: ... Metric: ... Verify: ...]

# 计划向导
/autoresearch:plan [Goal: ...]

# 调试
/autoresearch:debug [Symptom: ... Scope: ...]

# 修复
/autoresearch:fix [Target: ... Scope: ...]

# 安全审计
/autoresearch:security [Scope: ... Iterations: ...]

# 发布
/autoresearch:ship [--auto] [--dry-run]

# 场景探索
/autoresearch:scenario [Scenario: ... Domain: ...]

# 预测
/autoresearch:predict [Scope: ... Goal: ...]

**最后更新**: 2026-03-20
**维护者**: OpenClaw Community