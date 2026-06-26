# Personal Growth Advisor - 使用示例

## 基本使用

### 1. 目标设定

```bash
cd ~/.openclaw/skills/personal-growth-advisor
python3 scripts/main.py goal --goal "学习Python" --timeline "6个月"
```

### 2. 习惯养成

```bash
python3 scripts/main.py habit --habit "每天运动" --frequency "Daily"
```

### 3. 定期复盘

```bash
python3 scripts/main.py review
```

### 4. 动机激励

```bash
python3 scripts/main.py motivation
```

### 5. 时间管理

```bash
python3 scripts/main.py time
```

### 6. 演示模式

```bash
python3 scripts/main.py demo
```

### 7. JSON 输出

```bash
python3 scripts/main.py goal --json
```

## 程序化调用

```python
from main import GrowthAdvisor

advisor = GrowthAdvisor()
result = advisor.create_goal('学习新技能', '3个月')
print(result['milestones'])
```

## 功能说明

| 功能 | 命令 | 说明 |
|------|------|------|
| 目标设定 | goal | SMART目标框架分解 |
| 习惯养成 | habit | 习惯循环模型 |
| 定期复盘 | review | 周/月复盘模板 |
| 动机激励 | motivation | 励志语录和技巧 |
| 时间管理 | time | 时间管理技巧 |

