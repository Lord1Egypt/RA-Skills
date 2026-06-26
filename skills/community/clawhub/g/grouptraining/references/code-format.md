# Likes Training Code Format Reference

Complete specification for the `name` field in push_plans API.

## Syntax Overview

```
plan := task (";" task)*
task := interval | simple
interval := "{" plan "}" "x" number
simple := duration "@" "(" intensity ")"
duration := number unit
unit := "min" | "s" | "m" | "km" | "c"
intensity := type "+" range | "rest"
range := low "~" high
```

## Simple Tasks

### Format
```
duration@(TYPE+low~high)
```

### Examples

**Heart Rate Reserve (HRR)**
```
10min@(HRR+1.0~2.0)    # 10 min warmup, zone 1-2
40min@(HRR+2.0~3.0)    # 40 min aerobic, zone 2-3
```

**VDOT Pace**
```
1000m@(VDOT+4.0~5.0)   # 1km at VDOT zone 4-5
800m@(VDOT+3.0~4.0)    # 800m at tempo pace
```

**Absolute Pace (PACE)**
Format: `min'sec` (slow to fast)
```
30min@(PACE+5'30~4'50)  # 30 min, pace between 5:30 and 4:50/km
5km@(PACE+6'00~5'30)    # 5km run, 6:00 to 5:30 pace
```

**Threshold Pace % (t/)**
```
30min@(t/0.88~0.99)     # 30 min at 88-99% of threshold pace
20min@(t/0.95~1.05)     # 20 min at threshold
```

**Max Heart Rate % (MHR)**
```
400m@(MHR+0.85~0.95)    # 400m at 85-95% max HR
```

**Lactate Threshold HR % (LTHR)**
```
5min@(LTHR+1.0~1.05)    # 5 min at 100-105% LTHR
```

**Perceived Effort (EFFORT)**
```
3min@(EFFORT+0.8~1.0)   # 3 min hard effort (RPE 8-10)
```

**FTP Power % (cycling)**
```
40min@(FTP+0.75~0.85)   # Sweet spot interval
5min@(FTP+0.95~1.05)    # Threshold interval
```

**Critical Swim Speed % (swimming)**
```
1000m@(CSS+0.95~1.05)   # CSS pace
100m@(CSS+1.05~1.10)    # Above CSS pace
```

## Interval Groups

### Format
```
{task1;task2;...} x repetitions
```

### Examples

**Basic Intervals**
```
{5min@(HRR+3.0~4.0);1min@(rest)}x3
# 5 min hard, 1 min rest, repeat 3 times
```

**Track Intervals**
```
{1000m@(VDOT+4.0~5.0);2min@(rest)}x5
# 5 x 1km with 2 min rest
```

**Pyramid Intervals**
```
{400m@(VDOT+4.0~5.0);90s@(rest)};{800m@(VDOT+4.0~5.0);2min@(rest)};{400m@(VDOT+4.0~5.0);90s@(rest)}
# 400, 800, 400 with rest
```

**Mixed Intervals**
```
{5min@(HRR+2.0~3.0);1min@(HRR+1.0~2.0)}x4
# Cruise intervals with active recovery
```

## Rest Periods

### Format
```
duration@(rest)
```

**Important**: The parentheses are required even for rest!

### Examples
```
2min@(rest)     # 2 minute complete rest
90s@(rest)      # 90 second rest
3min@(rest)     # 3 minutes walking recovery
```

## Complex Plans

### Warmup + Main + Cooldown
```
10min@(HRR+1.0~2.0);40min@(HRR+2.0~3.0);10min@(HRR+1.0~2.0)
# 10 min warmup, 40 min main, 10 min cooldown
```

### Warmup + Intervals + Cooldown
```
10min@(HRR+1.0~2.0);{1000m@(VDOT+4.0~5.0);2min@(rest)}x5;10min@(HRR+1.0~2.0)
# 10 min warmup, 5 x 1km with 2 min rest, 10 min cooldown
```

### Fartlek (Unstructured)
```
10min@(HRR+1.0~2.0);30min@(EFFORT+0.7~0.9);10min@(HRR+1.0~2.0)
# 10 min warmup, 30 min varied effort, 10 min cooldown
```

### Progressive Run
```
10min@(HRR+1.0~2.0);10min@(HRR+2.0~3.0);10min@(HRR+3.0~4.0);10min@(HRR+1.0~2.0)
# Gradually increasing intensity
```

## Duration Units Reference

| Unit | Meaning | Example |
|------|---------|---------|
| min | Minutes | `30min@(HRR+1.0~2.0)` |
| s | Seconds | `90s@(rest)` |
| m | Meters | `1000m@(VDOT+4.0~5.0)` |
| km | Kilometers | `5km@(PACE+5'00~4'30)` |
| c | Count/Reps | `10c@(OPEN+1)` (strength) |

## Common Patterns

### Easy Recovery Day
```
30min@(HRR+1.0~2.0)
```

### Tempo Run
```
10min@(HRR+1.0~2.0);20min@(t/0.95~1.05);10min@(HRR+1.0~2.0)
```

### Long Run with Marathon Pace
```
10min@(HRR+1.0~2.0);60min@(HRR+2.0~3.0);{2km@(PACE+4'30~4'20);1km@(HRR+1.0~2.0)}x3;10min@(HRR+1.0~2.0)
```

### HIIT Intervals
```
10min@(HRR+1.0~2.0);{1min@(MHR+0.90~0.95);2min@(rest)}x8;10min@(HRR+1.0~2.0)
```

## Error Prevention

### Common Mistakes

❌ `10min@HRR+1.0~2.0` (missing parentheses)
✅ `10min@(HRR+1.0~2.0)`

❌ `2min@rest` (rest needs parentheses)
✅ `2min@(rest)`

❌ `{5min@(HRR+3.0~4.0);1min@rest}x3` (rest in interval needs parentheses)
✅ `{5min@(HRR+3.0~4.0);1min@(rest)}x3`

❌ `5'30` without quotes in JSON
✅ Use `"5'30"` or escape in JSON strings

### Validation Tips

1. Every intensity specification must be in parentheses
2. Rest must be `duration@(rest)` with parentheses
3. Intervals use curly braces `{...}` followed by `xN`
4. Use `~` (tilde) to separate low-high range, not `-`
