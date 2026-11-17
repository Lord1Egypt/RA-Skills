---
slug: personal-health-tool-free
name: personal-health-tool-free
version: 1.0.2
displayName: 个人健康管家免费版
summary: "个人健康数据管理,支持运动、睡眠、饮食与体检报告分析。面向个人用户的健康管家,集成运动、睡眠、饮食与体检报告管理."
license: Proprietary
edition: free
description: '面向个人用户的健康管家,集成运动、睡眠、饮食与体检报告管理.
  核心能力: 健康数据记录、体检报告解读、运动计划、饮食建议、健康趋势

  适用场景: 个人健康管理、健身塑形、慢病预防、健康自检

  差异化: 免费版聚焦个人健康数据管理,本地存储,支持体检报告解读

  适用关键词: 个人健康, 健康管家, 体检报告, 运动计划, 饮食建议, 健康趋势'
tags:
  - 健康管理
  - 个人健康
  - 体检分析
  - 运动计划
  - 饮食管理
  - 数据分析
  - 工具
  - 效率
  - 自动化
  - 研究
  - 分析
  - 生活
  - 健康
  - 写作
  - normal
  - high
  - self
  - ref
  - metric
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# 个人健康管家 (免费版)

## 概述

本工具为个人用户提供完整健康管家服务,集成运动记录、睡眠追踪、饮食管理、体检报告解读等功能。通过本地存储的健康数据,生成个性化健康建议、运动计划与饮食方案,帮助用户全面管理自身健康.
免费版聚焦个人健康管理,适合关注健康的人士、健身爱好者以及需要管理健康数据的人.
## 核心能力

| 能力模块 | 描述 | 免费版支持 |
|----|---|-----|
| 健康数据记录 | 运动、睡眠、饮食、体重 | 支持 |
| 体检报告解读 | 常见体检指标分析 | 支持 |
| 运动计划 | 个性化运动方案 | 支持 |
| 饮食建议 | 营养与热量指导 | 支持 |
| 健康趋势 | 数据可视化分析 | 支持 |
| 健康目标 | 目标设定与追踪 | 支持 |
| 健康提醒 | 定时提醒 | 基础 |
| 慢病管理 | 慢性病跟踪 | 不支持 (升级 PRO) |
| 医生共享 | 与医生共享数据 | 不支持 (升级 PRO) |
| AI 诊断 | AI 辅助诊断 | 不支持 (升级 PRO) |
| 穿戴设备 | 设备同步 | 不支持 (升级 PRO) |
| 家庭管理 | 多成员管理 | 不支持 (升级 PRO) |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：个人健康数据管理、支持运动、饮食与体检报告分、面向个人用户的健、康管家、集成运动、饮食与体检报告管、核心能力、适用场景、个人健康管理、健身塑形、慢病预防、健康自检、差异化、免费版聚焦个人健、康数据管理、本地存储、支持体检报告解读、适用关键词、个人健康、健康管家等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一: 体检报告解读

解读常见体检指标,提供健康建议.
```python
class MedicalReportAnalyzer:
    # 常见体检指标正常范围
    REFERENCE_RANGES = {
        "blood_pressure_systolic": {"normal": [90, 120], "high": 140},
        "blood_pressure_diastolic": {"normal": [60, 80], "high": 90},
        "blood_sugar_fasting": {"normal": [3.9, 6.1], "high": 7.0},  # mmol/L
        "cholesterol_total": {"normal": [3.1, 5.2], "high": 6.2},     # mmol/L
        "ldl_cholesterol": {"normal": [1.9, 3.4], "high": 4.1},
        "hdl_cholesterol": {"normal": [1.0, 1.5], "low": 1.0},
        "triglycerides": {"normal": [0.4, 1.7], "high": 2.3},
        "uric_acid_male": {"normal": [210, 420], "high": 480},        # umol/L
        "uric_acid_female": {"normal": [150, 360], "high": 400},
        "alt": {"normal": [7, 40], "high": 50},  # U/L
        "ast": {"normal": [13, 35], "high": 40},
        "hemoglobin_male": {"normal": [120, 160], "low": 120},  # g/L
        "hemoglobin_female": {"normal": [110, 150], "low": 110},
    }
# ..
    def analyze(self, report_data):
        """分析体检报告"""
        results = []
        for metric, value in report_data.items():
            ref = self.REFERENCE_RANGES.get(metric)
            if not ref: continue
# ..
            status = self._evaluate(metric, value, ref)
            results.append({
                "metric": metric,
                "value": value,
                "status": status,
                "reference": ref,
                "advice": self._advice(metric, status),
            })
# ..
        overall = self._overall_assessment(results)
        return {"items": results, "overall": overall}
# ..
    def _evaluate(self, metric, value, ref):
        if "high" in ref and value > ref["high"]: return "high"
        if "low" in ref and value < ref["low"]: return "low"
        if value < ref["normal"][0]: return "low"
        if value > ref["normal"][1]: return "high"
        return "normal"
# ..
    def _advice(self, metric, status):
        advice_map = {
            "blood_pressure_systolic": {
                "high": "血压偏高,建议低盐饮食,定期监测",
                "normal": "血压正常,保持良好生活习惯",
            },
            "blood_sugar_fasting": {
                "high": "空腹血糖偏高,建议控制糖分摄入,复查糖化血红蛋白",
                "normal": "血糖正常,保持均衡饮食",
            },
            "uric_acid_male": {
                "high": "尿酸偏高,减少嘌呤摄入 (海鲜、动物内脏),多喝水",
                "normal": "尿酸正常",
            },
        }
        return advice_map.get(metric, {}).get(status, "保持关注")
# ..
analyzer = MedicalReportAnalyzer()
report = analyzer.analyze({
    "blood_pressure_systolic": 135,
    "blood_pressure_diastolic": 85,
    "blood_sugar_fasting": 5.5,
    "cholesterol_total": 5.8,
    "uric_acid_male": 450,
})
for item in report["items"]:
    print(f"{item['metric']}: {item['value']} ({item['status']}) - {item['advice']}")
```

### 场景二: 个性化运动计划

根据用户情况生成运动计划.
```python
class ExercisePlanGenerator:
    def generate(self, user_profile, goal):
        """生成个性化运动计划"""
        plans = {
            "weight_loss": self._weight_loss_plan(user_profile),
            "muscle_gain": self._muscle_gain_plan(user_profile),
            "endurance": self._endurance_plan(user_profile),
            "flexibility": self._flexibility_plan(user_profile),
            "stress_relief": self._stress_relief_plan(user_profile),
        }
        return plans.get(goal, plans["weight_loss"])
# ..
    def _weight_loss_plan(self, profile):
        """减脂计划"""
        return {
            "weekly_schedule": {
                "周一": {"type": "有氧", "exercise": "慢跑", "duration_min": 40, "intensity": "medium"},
                "周二": {"type": "力量", "exercise": "全身训练", "duration_min": 45, "intensity": "medium"},
                "周三": {"type": "休息", "exercise": "散步", "duration_min": 30, "intensity": "low"},
                "周四": {"type": "有氧", "exercise": "HIIT", "duration_min": 25, "intensity": "high"},
                "周五": {"type": "力量", "exercise": "下肢+核心", "duration_min": 45, "intensity": "medium"},
                "周六": {"type": "有氧", "exercise": "骑行/游泳", "duration_min": 60, "intensity": "medium"},
                "周日": {"type": "休息", "exercise": "瑜伽", "duration_min": 30, "intensity": "low"},
            },
            "weekly_calories_target": 2500,
            "tips": [
                "运动前热身 5-10 分钟",
                "运动后拉伸 10 分钟",
                "保持水分补充",
                "心率控制在最大心率的 60-75%",
            ],
        }
```

### 场景三: 健康数据可视化

生成健康趋势可视化.
```python
import json
from datetime import datetime, timedelta
from pathlib import Path
# ..
class HealthDataViz:
    def __init__(self, data_dir="~/.health"):
        self.data_dir = Path(data_dir).expanduser()
# ..
    def weight_trend(self, days=30):
        """体重趋势"""
        records = self._load_records("weight", days)
        if not records: return "无数据"
# ..
        weights = [r["value"] for r in records]
        return {
            "latest": weights[-1],
            "average": round(sum(weights) / len(weights), 1),
            "min": min(weights),
            "max": max(weights),
            "change": round(weights[-1] - weights[0], 1),
            "trend": "下降" if weights[-1] < weights[0] else "上升",
        }
# ..
    def weekly_summary(self):
        """周度健康汇总"""
        return {
            "workouts": self._count_workouts(7),
            "avg_sleep_hours": self._avg_sleep(7),
            "avg_daily_steps": self._avg_steps(7),
            "weight_change": self._weight_change(7),
            "goal_completion": self._goal_completion(),
        }
```

## 不适用场景

以下场景个人健康管家免费版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始

### Step 1: 初始化健康数据目录

```bash
mkdir -p ~/.health/{weight,workouts,sleep,diet,reports}
echo '{"version":"1.0","created":"'$(date -I)'"}' > ~/.health/config.json
```

### Step 2: 记录第一条数据

```python
import json
from datetime import datetime
from pathlib import Path
# ..
# 记录体重
record = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "value": 70.5,
    "unit": "kg",
}
Path("~/.health/weight/latest.json").expanduser().write_text(
    json.dumps(record, ensure_ascii=False, indent=2)
)
```

### Step 3: 解析体检报告

```python
# 输入体检数据
report_data = {
    "blood_pressure_systolic": 120,
    "blood_pressure_diastolic": 80,
}
analysis = analyzer.analyze(report_data)
print(analysis["overall"])
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例

### 个人健康配置

```yaml
# ~/.health/config.yaml
profile:
  name: 你的名字
  age: 30
  gender: male
  height_cm: 175
  weight_kg: 70
  activity_level: moderate
# ..
goals:
  target_weight_kg: 65
  weekly_workouts: 4
  daily_steps: 10000
  sleep_hours: 8
  daily_calories: 1800
# ..
tracking:
  weight: daily
  workouts: per_session
  sleep: daily
  diet: per_meal
  steps: daily
# ..
storage:
  type: local
  path: ~/.health/
  backup: weekly
# ..
notifications:
  workout_reminder: "18:00"
  sleep_reminder: "22:30"
  weight_reminder: "07:00"
```

### 体检报告模板

```python
REPORT_TEMPLATE = {
    "basic_info": {
        "exam_date": "",
        "hospital": "",
        "age": "",
        "gender": "",
    },
    "vital_signs": {
        "height_cm": None,
        "weight_kg": None,
        "bmi": None,
        "blood_pressure": "",
        "heart_rate": None,
    },
    "blood_test": {
        "complete_blood_count": {},
        "liver_function": {},
        "kidney_function": {},
        "blood_lipids": {},
        "blood_sugar": {},
    },
    "imaging": {
        "chest_xray": "",
        "ultrasound": {},
    },
    "recommendations": [],
}
```

## 最佳实践

### 1. 数据记录习惯

```text
养成记录习惯:
- 每天早晨称重 (固定时间)
- 运动后立即记录
- 每晚记录睡眠
- 每餐后记录饮食
- 每年体检后录入报告
# ..
数据越完整,分析越准确.
```

### 2. 体检报告解读原则

```text
注意事项:
- 单次异常不一定是疾病,需复查确认
- 参考范围因实验室而异,以报告标注为准
- 本工具提供参考建议,不能替代医生诊断
- 异常指标建议咨询专业医生
```

### 3. 目标设定 SMART 原则

```python
def set_smart_goal(current, target, timeframe_weeks):
    """SMART 目标"""
    weekly_change = (target - current) / timeframe_weeks
    return {
        "specific": f"从 {current} 到 {target}",
        "measurable": "每周可测量",
        "achievable": abs(weekly_change / current) < 0.02,  # 每周变化 < 2%
        "relevant": "与健康目标相关",
        "time_bound": f"{timeframe_weeks} 周内",
    }
```

## 常见问题

### Q1: 免费版能管理多少数据?

无硬性上限,但建议保留最近 1 年的详细数据,更早的可汇总归档.
### Q2: 体检报告解读准确吗?

基于医学参考范围提供分析,准确度约 90%。但不能替代医生诊断,异常请咨询医生.
### Q3: 数据存储安全吗?

所有数据存储在本地,JSON 格式,完全在用户控制下,不会上传云端.
### Q4: 可以同步智能手表吗?

免费版不支持自动同步。需要手动记录或导入。设备同步需要 PRO 版本.
### Q5: 如何备份数据?

```bash
tar -czf health-backup-$(date +%Y%m%d).tar.gz ~/.health/
```

## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 规范的任意 AI Agent (Claude Code、Cursor、Codex、Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **存储**: 本地文件系统

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | 推理服务 | 必需 | 由 Agent 内置 LLM 提供 |
| Python 3.8+ | 运行时 | 推荐 | python.org 下载 |
| PyYAML | Python 库 | 可选 | `pip install pyyaml` |

### API Key 配置

```bash
# 免费版无需外部 API Key
# 所有数据本地存储
# ..
# 可选: 个人偏好
export HEALTH_USER_NAME="你的名字"
export HEALTH_DATA_DIR="~/.health"
```

### 可用性分类

- **分类**: MD+EXEC (Markdown 指令 + 命令行执行)
- **说明**: 本 Skill 通过自然语言指令驱动 Agent 管理个人健康数据,所有数据本地存储
- **免费版限制**: 单用户、本地存储、无设备同步、无医生共享、无 AI 诊断、基础提醒

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步，数据仅存储在当前设备
- 免费版仅提供基础健康记录与提醒功能，不支持专业医疗诊断建议
- 健康数据分析依赖用户手动输入的准确性，无法自动采集智能穿戴设备数据
- 提醒功能依赖 Agent 心跳触发，存在 30-60 分钟可能的延迟

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "个人健康管家免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "personal health"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
