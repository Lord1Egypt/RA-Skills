# Name Analyzer - 基础测试

## 测试环境
- Python 3.8+

## 测试用例

### Test 1: 中文名字分析

**输入**: `张伟`

**预期**:
- type: chinese
- meaning: 包含"伟"的含义
- numerology: 有人格数、生命数等
- score > 0

### Test 2: 英文名字分析

**输入**: `John`

**预期**:
- type: english
- meaning: "上帝是仁慈的"
- numerology: 正确计算

### Test 3: 完整模式

**输入**: `李明 --full`

**预期**:
- 包含 famous_people
- 包含 compatibility

## 运行测试

```bash
cd ~/.openclaw/skills/name-analyzer
python3 scripts/name_analyzer.py analyze
python3 scripts/name_analyzer.py demo
python3 scripts/name_analyzer.py analyze --json
```

## 验收标准

- [x] 中文名字分析正常
- [x] 英文名字分析正常
- [x] 数理分析正常
- [x] 评分功能正常

