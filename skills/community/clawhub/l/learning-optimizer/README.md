# Learning Optimizer - 学习优化器

分析学习模式，识别低效环节，提供优化建议

## Quick Start

```bash
# 分析学习模式
python3 scripts/main.py analyze --schedule "每天2小时" --subjects "数学,英语"

# 获取优化建议
python3 scripts/main.py optimize --problem "容易分心" --current "长时间连续学习"

# 时间分配建议
python3 scripts/main.py allocate --total 120 --priorities "数学高,英语中"

# 查看本地数据目录
python3 scripts/main.py data

# 隔离测试/演示数据
LEARNING_OPTIMIZER_HOME=/tmp/learning-demo python3 scripts/main.py analyze --schedule "每天2小时" --subjects "数学,英语"
```

## Commands
- `analyze` - Analyze study patterns
- `optimize` - Get optimization suggestions
- `allocate` - Time allocation plan
- `data` - Show local storage path

## Verification

```bash
python3 -m py_compile scripts/main.py scripts/verify.py
python3 scripts/verify.py
```

Runtime logs are stored under `~/.learning-optimizer/` by default, or under
`LEARNING_OPTIMIZER_HOME` when that environment variable is set.
