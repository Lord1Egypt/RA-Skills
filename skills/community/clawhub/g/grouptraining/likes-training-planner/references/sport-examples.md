# Sport-Specific Training Examples

Complete examples for running, cycling, swimming, and strength training.

## Running (sports: 1)

### Base Building Phase

**Week 1-4: Easy Aerobic Focus**

| Day | Type | Code | Weight |
|-----|------|------|--------|
| Mon | Easy | `40min@(HRR+1.0~2.0)` | q3 |
| Wed | Easy | `40min@(HRR+1.0~2.0)` | q3 |
| Fri | Easy | `35min@(HRR+1.0~2.0)` | q3 |
| Sun | Long | `60min@(HRR+1.0~2.0)` | q3 |

**Week 5-8: Add Tempo**

| Day | Type | Code | Weight |
|-----|------|------|--------|
| Tue | Tempo | `10min@(HRR+1.0~2.0);20min@(t/0.88~0.98);10min@(HRR+1.0~2.0)` | q2 |
| Thu | Easy | `40min@(HRR+1.0~2.0)` | q3 |
| Sat | Long | `75min@(HRR+1.0~2.0)` | q3 |

### Marathon Training

**12-Week Plan Sample**

**Week 1 (Base)**
```json
[
  {"name": "40min@(HRR+1.0~2.0)", "title": "轻松跑", "weight": "q3", "type": "qingsong"},
  {"name": "10min@(HRR+1.0~2.0);{800m@(VDOT+4.0~5.0);90s@(rest)}x4;10min@(HRR+1.0~2.0)", "title": "间歇训练", "weight": "q2", "type": "i"},
  {"name": "45min@(HRR+1.0~2.0)", "title": "轻松跑", "weight": "q3", "type": "qingsong"},
  {"name": "10min@(HRR+1.0~2.0);8km@(PACE+5'30~5'15);10min@(HRR+1.0~2.0)", "title": "马拉松配速", "weight": "q2", "type": "m"},
  {"name": "休息", "title": "休息日", "weight": "xuanxiu", "type": "xiuxi"},
  {"name": "60min@(HRR+1.0~2.0)", "title": "长距离慢跑", "weight": "q3", "type": "lsd"}
]
```

**Week 6 (Build)**
```json
[
  {"name": "45min@(HRR+1.0~2.0)", "title": "恢复跑", "weight": "q3", "type": "qingsong"},
  {"name": "10min@(HRR+1.0~2.0);{1000m@(VDOT+4.0~5.0);2min@(rest)}x5;10min@(HRR+1.0~2.0)", "title": "亚索800", "weight": "q1", "type": "i"},
  {"name": "40min@(HRR+1.0~2.0)", "title": "轻松跑", "weight": "q3", "type": "qingsong"},
  {"name": "10min@(HRR+1.0~2.0);12km@(PACE+5'15~5'00);10min@(HRR+1.0~2.0)", "title": "马拉松配速跑", "weight": "q2", "type": "m"},
  {"name": "休息", "title": "休息日", "weight": "xuanxiu", "type": "xiuxi"},
  {"name": "90min@(HRR+1.0~2.5)", "title": "长距离有氧", "weight": "q2", "type": "lsd"}
]
```

**Week 12 (Taper)**
```json
[
  {"name": "30min@(HRR+1.0~2.0)", "title": "放松跑", "weight": "q3", "type": "qingsong"},
  {"name": "10min@(HRR+1.0~2.0);{400m@(VDOT+4.5~5.0);90s@(rest)}x4;10min@(HRR+1.0~2.0)", "title": "短间歇", "weight": "q2", "type": "i"},
  {"name": "20min@(HRR+1.0~2.0)", "title": "轻松跑", "weight": "q3", "type": "qingsong"},
  {"name": "休息", "title": "休息日", "weight": "xuanxiu", "type": "xiuxi"},
  {"name": "30min@(HRR+1.0~2.0)", "title": "赛前激活", "weight": "q3", "type": "qingsong"},
  {"name": "马拉松比赛", "title": "比赛日", "weight": "q1", "type": "other"}
]
```

### 5K/10K Training

**Speed Focus**
```json
{
  "name": "10min@(HRR+1.0~2.0);{400m@(VDOT+5.0~5.5);2min@(rest)}x8;10min@(HRR+1.0~2.0)",
  "title": "速度间歇",
  "weight": "q1",
  "type": "r"
}
```

**Tempo Progression**
```json
{
  "name": "10min@(HRR+1.0~2.0);10min@(t/0.88~0.95);10min@(t/0.95~1.05);10min@(HRR+1.0~2.0)",
  "title": "渐进 tempo",
  "weight": "q2",
  "type": "t"
}
```

### Fat Loss / Fitness

**Beginner 3-Day Plan**
```json
[
  {"name": "30min@(HRR+1.0~2.0)", "title": "快走/慢跑", "weight": "q3", "type": "qingsong"},
  {"name": "{2min@(HRR+2.0~3.0);2min@(HRR+1.0~2.0)}x5", "title": "走跑交替", "weight": "q3", "type": "ft"},
  {"name": "35min@(HRR+1.0~2.0)", "title": "轻松有氧", "weight": "q3", "type": "e"}
]
```

**HIIT for Fat Loss**
```json
{
  "name": "5min@(HRR+1.0~2.0);{30s@(EFFORT+0.9~1.0);90s@(HRR+1.0~2.0)}x10;5min@(HRR+1.0~2.0)",
  "title": "HIIT燃脂",
  "weight": "q1",
  "type": "i"
}
```

## Cycling (sports: 2)

### Base Phase

**Zone 2 Endurance**
```json
{
  "name": "10min@(FTP+0.55~0.65);90min@(FTP+0.65~0.75);10min@(FTP+0.55~0.65)",
  "title": "有氧基础",
  "weight": "q3",
  "type": "e",
  "sports": 2
}
```

**Sweet Spot Intervals**
```json
{
  "name": "10min@(FTP+0.55~0.65);{10min@(FTP+0.88~0.94);5min@(FTP+0.55~0.65)}x3;10min@(FTP+0.55~0.65)",
  "title": "甜区间歇",
  "weight": "q2",
  "type": "t",
  "sports": 2
}
```

**Threshold Intervals**
```json
{
  "name": "10min@(FTP+0.55~0.65);{5min@(FTP+0.95~1.05);5min@(FTP+0.55~0.65)}x4;10min@(FTP+0.55~0.65)",
  "title": "阈值间歇",
  "weight": "q1",
  "type": "i",
  "sports": 2
}
```

### VO2 Max Development

**5-Minute Intervals**
```json
{
  "name": "10min@(FTP+0.55~0.65);{5min@(FTP+1.05~1.15);5min@(FTP+0.55~0.65)}x4;10min@(FTP+0.55~0.65)",
  "title": "VO2 Max",
  "weight": "q1",
  "type": "i",
  "sports": 2
}
```

### Power-Based Workouts

**Absolute Power Target**
```json
{
  "name": "10min@(FTP+0.55~0.65);20min@(CP+200~220);10min@(FTP+0.55~0.65)",
  "title": "功率二区",
  "weight": "q2",
  "type": "e",
  "sports": 2
}
```

## Swimming (sports: 5)

### Technique Focus

**Drill Set**
```json
{
  "name": "200m@(CSS+0.80~0.90);{50m@(OPEN+1);30s@(rest)}x4;200m@(CSS+0.80~0.90)",
  "title": "技术训练",
  "weight": "q3",
  "type": "other",
  "sports": 5
}
```

### Threshold Development

**CSS Intervals**
```json
{
  "name": "200m@(CSS+0.80~0.90);{100m@(CSS+1.05~1.10);30s@(rest)}x8;200m@(CSS+0.80~0.90)",
  "title": "阈值间歇",
  "weight": "q2",
  "type": "t",
  "sports": 5
}
```

**Long Distance**
```json
{
  "name": "200m@(CSS+0.80~0.90);1000m@(CSS+0.95~1.05);200m@(CSS+0.80~0.90)",
  "title": "长距离配速",
  "weight": "q2",
  "type": "e",
  "sports": 5
}
```

### Sprint Training

**Speed Work**
```json
{
  "name": "200m@(CSS+0.80~0.90);{25m@(EFFORT+0.9~1.0);45s@(rest)}x8;200m@(CSS+0.80~0.90)",
  "title": "冲刺训练",
  "weight": "q1",
  "type": "r",
  "sports": 5
}
```

## Strength Training (sports: 3)

### Full Body

**Circuit**
```json
{
  "name": "10min@(HRR+1.0~2.0);rest!10*3;pushup!15*3;squat!20*3;plank!60s*3;10min@(HRR+1.0~2.0)",
  "title": "全身循环",
  "weight": "q2",
  "type": "jili",
  "sports": 3
}
```

### Core Focus

**Plank Variations**
```json
{
  "name": "5min@(HRR+1.0~2.0);{plank!60s;30s@(rest)}x4;sider!45s*2;30s@(rest);bird!10c*2;5min@(HRR+1.0~2.0)",
  "title": "核心训练",
  "weight": "q3",
  "type": "jili",
  "sports": 3
}
```

## Combined Sports (Cross Training)

### Triathlon Base

**Swim-Bike Brick**
```json
[
  {"name": "200m@(CSS+0.80~0.90);500m@(CSS+0.95~1.05);200m@(CSS+0.80~0.90)", "title": "游泳", "weight": "q2", "type": "e", "sports": 5},
  {"name": "30min@(FTP+0.65~0.75)", "title": "骑行", "weight": "q2", "type": "e", "sports": 2}
]
```

### Weekly Structure Example

| Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|-----|-----|-----|-----|-----|-----|-----|
| 跑休 | 跑步i | 游泳e | 休息 | 跑步t | 骑行LSD | 跑步LSD |
