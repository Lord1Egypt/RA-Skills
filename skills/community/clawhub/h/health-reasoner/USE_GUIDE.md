# Health Reasoner 使用指南

## 安装

```bash
# 克隆仓库
git clone https://github.com/你的用户名/health-reasoner.git
cd health-reasoner

# 无需安装依赖（纯标准库）
```

或者直接复制 `health_reasoner.py` 到你的项目目录。

## 基础使用

### CLI 模式

```bash
python health_reasoner.py --cli
```

按提示逐项输入数据。

### JSON 输入模式

```bash
python health_reasoner.py --input data.json --format json
```

### Python 导入

```python
from health_reasoner import HealthReasoner

hr = HealthReasoner()

result = hr.assess({
    "age": 35,
    "gender": "female",
    "sleep_hours": 7.5,
    "sleep_quality": "good",
    "diet_type": "balanced",
    "exercise_frequency": "daily",
    "stress_level": "low",
})
print(f"评分: {result.score}/100")
print(f"风险: {result.risk_level}")
for s in result.suggestions:
    print(f"[{s['priority']}] {s['category']}: {s['message']}")

# 批量评估
results = hr.batch_assess([profile1, profile2])

# 趋势分析（需要传入历史记录或指定 --history 文件）
trend = hr.trend_analysis(history_7days)
```

## 注意事项

- ⚠️ **本工具不提供医疗诊断或治疗建议**，健康问题请咨询专业医师
- 历史记录为**可选功能**：不传 `--history` 参数则不留存任何数据
- 所有数据本地处理，不自动上传云端
- 评分规则基于通用生活习惯指南，仅供参考
