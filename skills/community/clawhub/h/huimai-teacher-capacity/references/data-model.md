# 数据模型参考

## 核心实体

### 教师 (Teacher)
```
teacherId       string
name            string
subjects        []string    # 教学科目列表
grades          []int       # 任教年级
classes         []string    # 任教班级ID列表
title           string      # 职称 (初级/中级/高级/特级)
joinDate        date        # 入职日期
```

### 教学评估记录 (EvaluationRecord)
```
evalId          string
teacherId       string
subjectId       string
classId         string
semester        string      # 如 "2026春"
evalDate        date
dimensions      EvalDimensions
overallScore    float       # 综合评分 (0-100)
sourceDataRef   string      # 引用的 homework-grading-assessment 数据快照ID
```

### 评估维度 (EvalDimensions)
```
kpCoverage      float       # 知识点覆盖度：实际讲授知识点 / 应有知识点
studentProgress float       # 学生进步度：班级平均掌握率提升量 (学期初 → 当前)
balanceIndex    float       # 均衡性指数：1 - (班级内掌握率标准差 / 满分标准差)
feedbackTimely  float       # 反馈时效：作业批改到返回的平均时长(小时)，得分归一化
trendDirection  float       # 趋势方向：历次测验平均分的线性回归斜率，得分归一化
```

### 班级对比维度 (ClassComparison)
```
classIdA        string
classIdB        string
subjectId       string
gradeLevel      int
metrics         {
    avgScoreDiff     float   # 平均分差
    kpMasteryDiff    map[string]float   # 各知识点掌握率差
    stdDevDiff       float   # 标准差差异
    trendCorrelation float   # 趋势相关性 (-1 ~ 1)
}
```

## 综合评分算法（示例）

```
overallScore = 
    kpCoverage * 0.20 +
    studentProgress * 0.30 +
    balanceIndex * 0.20 +
    feedbackTimely * 0.15 +
    trendDirection * 0.15
```

各维度权重可根据学校实际偏重调整。支持 A/B 权重方案对比。
