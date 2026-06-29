# 数据分析维度与算法参考

## 核心分析维度

### 1. 周期规律分析
- 平均周期长度 (mean_cycle_length)
- 周期长度标准差 (cycle_length_std) — 规律性指标
- 周期长度趋势 (近3/6周期滑动平均)
- 周期变异系数 (CV) — CV<0.1为非常规律
- 最短/最长周期
- 经期持续天数均值与波动

### 2. 症状模式分析
- 各症状出现频率 (occurrence_rate)
- 症状与周期阶段的关联热力图
- 症状严重程度趋势
- 高频症状Top5
- 新出现症状标记

### 3. 体征趋势
- 基础体温曲线与双相确认
- 体重波动与周期阶段的关联
- 睡眠质量变化模式
- 运动表现与周期阶段

### 4. 预测引擎
- 下次经期预测（基于平均周期+近期趋势）
- 排卵期估算（下次预测前14天±2天）
- 易孕期窗口
- 预测置信区间

### 5. 影响因素关联
- 标记事件（旅行、压力、疾病等）与周期变化的时间关联
- 延迟/提前的可能归因
- 季节模式识别

## 数据存储格式

建议使用JSON文件存储：

```json
{
  "user_profile": {
    "life_stage": "menstruating|pregnant|postpartum|perimenopause|postmenopause|premenarche",
    "age": null,
    "typical_cycle_length": null,
    "typical_period_length": null,
    "conditions": [],
    "medications": [],
    "created_at": "ISO datetime"
  },
  "cycles": [
    {
      "id": "uuid",
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD",
      "flow_level": "light|medium|heavy",
      "symptoms": {
        "cramps": {"present": true, "severity": 3},
        "headache": {"present": true, "severity": 2}
      },
      "mood": "irritable|anxious|low|stable|energetic",
      "mood_score": 6,
      "bbt": 36.5,
      "weight": null,
      "notes": "string",
      "events": ["travel", "stress", "illness"],
      "medications_taken": [],
      "exercise": "light|moderate|intense|none"
    }
  ],
  "daily_logs": [
    {
      "date": "YYYY-MM-DD",
      "cycle_day": null,
      "symptoms": {},
      "mood_score": null,
      "bbt": null,
      "weight": null,
      "sleep_hours": null,
      "exercise": null,
      "notes": ""
    }
  ],
  "events": [
    {
      "date": "YYYY-MM-DD",
      "type": "travel|stress|illness|medication_change|lifestyle_change|other",
      "description": "string",
      "severity": 3
    }
  ]
}
```

## 可视化规范

### 配色方案（女性健康主题）
- 主色：柔紫 #9B7EC4 (calm purple)
- 经期红：柔和版 #E8737A (soft coral)
- 卵泡期绿：#7EC49B (follicular green)  
- 黄体期金：#C4A87E (luteal gold)
- 排卵期粉：#E89BB4 (ovulation pink)
- 背景：暖白 #FAF7F5
- 暗色背景：深紫灰 #1E1B2E
- 文字：深灰 #2D2A3E
- 强调：温暖琥珀 #F0A060

### 图表类型选择
- 周期趋势：折线图 (cycle length over time)
- 症状分布：雷达图 (symptom frequency radar)
- 经期日历：热力图日历 (heatmap calendar)
- 预测时间线：甘特图风格 (prediction timeline)
- 阶段体征：多轴折线图 (multi-axis phase chart)
- 影响因素：桑基图/关联图 (correlation)
- 周期波动：箱线图 (cycle variability)
- 情绪曲线：面积图 (mood curve)

## 建议生成算法

### 触发条件分级
- Level 1 (信息性)：每次记录后 → 周期阶段信息 + 小贴士
- Level 2 (模式发现)：3个周期后 → 个人模式洞察
- Level 3 (预警)：异常值检测 → 温柔提醒 + 科学解释
- Level 4 (深度分析)：6个周期后 → 综合健康报告

### 建议分类
1. 营养建议 (nutrition)
2. 运动建议 (exercise)
3. 生活方式 (lifestyle)
4. 心理调节 (mental)
5. 医疗咨询 (medical_referral)

### 压力测试规则
每条建议生成后必须：
1. 核实数据支撑（是否基于用户真实数据）
2. 交叉验证（是否有医学文献支持）
3. 安全边界检查（是否可能有害）
4. 个性化程度评分（1-5分，低于3分重写）
5. 可执行性检查（用户现在能否做到）
