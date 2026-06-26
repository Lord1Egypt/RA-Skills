# Personal Growth Advisor - 基础测试

## 测试环境
- Python 3.8+

## 测试用例

### Test 1: 目标设定

```bash
python3 scripts/main.py goal --goal "学习Python" --timeline "6个月"
```

预期：输出 SMART 分解和里程碑

### Test 2: 习惯养成

```bash
python3 scripts/main.py habit --habit "每天运动"
```

预期：输出习惯循环和技巧

### Test 3: 复盘模板

```bash
python3 scripts/main.py review
```

预期：输出复盘问题清单

### Test 4: 动机激励

```bash
python3 scripts/main.py motivation
```

预期：输出励志语录

### Test 5: 时间管理

```bash
python3 scripts/main.py time
```

预期：输出时间管理技巧

## 验收标准

- [x] 目标设定功能正常
- [x] 习惯养成功能正常
- [x] 复盘模板功能正常
- [x] 动机激励功能正常
- [x] 时间管理功能正常

