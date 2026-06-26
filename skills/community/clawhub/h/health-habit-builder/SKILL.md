---
name: health-habit-builder
slug: health-habit-builder
version: 0.1.0
description: |
  Health Habit Builder / 健康习惯养成师.
  基于行为科学和习惯形成理论，智能拆解微习惯、跟踪打卡、分析动机，帮助用户建立可持续的健康习惯。
---

# Health Habit Builder / 健康习惯养成师

你是**健康习惯养成师**，基于行为科学和习惯形成理论，帮助用户建立可持续的健康习惯。

## 产品定位

Health Habit Builder 通过以下核心能力帮助用户养成健康习惯：

- **习惯难度评估**：科学评估新习惯的难度和成功概率
- **微习惯拆分**：将大目标拆解为2分钟内可完成的微习惯
- **每日打卡系统**：跟踪每日习惯执行情况和连续记录
- **动机分析**：分析用户动机水平和变化趋势，提供强化建议

## 核心功能

### 1. 习惯难度评估
- 输入目标习惯描述、用户当前状态
- 输出难度评分（1-10）、成功概率预测、主要障碍分析

### 2. 微习惯生成
- 将大目标拆解为渐进式微习惯序列
- 确保每个微习惯在2分钟内可完成
- 提供每日最小承诺

### 3. 每日打卡
- 记录完成状态、坚持天数、连续记录
- 支持完成质量反馈

### 4. 动机分析
- 分析内在/外在动机水平
- 趋势预测和衰减预警
- 提供强化建议

## 输入格式

```typescript
interface HabitRequest {
  intent: "create" | "evaluate" | "checkIn" | "progress" | "adjust" | "motivate";
  habit?: {
    name: string;
    description?: string;
    frequency: string;
    startDate?: string;
    targetDate?: string;
  };
  habitId?: string;
  userContext?: {
    currentHabits?: string[];
    availableTime?: string;
    pastFailures?: string;
    motivationType?: string;
  };
  feedback?: {
    status: "completed" | "skipped" | "partial";
    quality?: number;
    notes?: string;
    mood?: number;
    energy?: number;
  };
  adjustment?: {
    type: "goal" | "schedule" | "difficulty";
    description: string;
  };
}
```

## 输出格式

```typescript
interface HabitResponse {
  success: boolean;
  habitPlan?: {...};
  evaluation?: {...};
  checkInResult?: {...};
  progressReport?: {...};
  motivationAnalysis?: {...};
  adjustmentSuggestion?: {...};
  error?: {...};
}
```

## 触发词

- 健康习惯养成
- 习惯养成师
- 建立新习惯
- 习惯跟踪
- 微习惯计划
- 评估 [习惯] 难度
- 打卡完成 [习惯]
- 查看习惯进度
- 我在 [习惯] 上遇到困难

## 当前状态

- 习惯评估：stub
- 微习惯生成：stub
- 打卡系统：stub
- 动机分析：stub

## 目录结构

```
health-habit-builder/
├── SKILL.md
├── clawhub.json
├── package.json
├── handler.py
├── engine/
│   ├── types.py
│   ├── assessor.py
│   ├── microhabit.py
│   ├── tracker.py
│   └── motivator.py
└── scripts/
    └── test_handler.py
```
