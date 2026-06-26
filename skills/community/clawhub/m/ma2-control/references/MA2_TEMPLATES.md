# MA2 命令模板库

---

## 🎯 模板使用说明

每个模板可直接复制使用，只需替换 `[]` 中的内容。

---

## 1. 基础模板

### 1.1 开灯
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At Full"
  ]
}
```

### 1.2 关灯
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At 0"
  ]
}
```

### 1.3 调光
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At [50]"
  ]
}
```

---

## 2. 颜色模板

### 2.1 单色
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At Full",
    "Attribute \"COLOR1\" At [30]"
  ]
}
```

### 2.2 渐变色
```json
{
  "commands": [
    "Fixture [1] Thru [5]",
    "At Full",
    "Attribute \"COLOR1\" At [0]"
  ],
  "notes": "红色"
}
```
```json
{
  "commands": [
    "Fixture [6] Thru [10]",
    "At Full",
    "Attribute \"COLOR1\" At [60]"
  ],
  "notes": "蓝色"
}
```

---

## 3. 位置模板

### 3.1 居中
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At Full",
    "Attribute \"PAN\" At [127]",
    "Attribute \"TILT\" At [50]"
  ]
}
```

### 3.2 三角形
```json
{
  "commands": [
    "Fixture [1]",
    "At Full",
    "Attribute \"PAN\" At [0]",
    "Attribute \"TILT\" At [50]"
  ],
  "notes": "左"
}
```
```json
{
  "commands": [
    "Fixture [2]",
    "At Full",
    "Attribute \"PAN\" At [127]",
    "Attribute \"TILT\" At [0]"
  ],
  "notes": "中"
}
```
```json
{
  "commands": [
    "Fixture [3]",
    "At Full",
    "Attribute \"PAN\" At [255]",
    "Attribute \"TILT\" At [50]"
  ],
  "notes": "右"
}
```

---

## 4. 存储模板

### 4.1 存 Cue
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At Full",
    "Attribute \"COLOR1\" At [30]",
    "Store Cue [1]"
  ]
}
```

### 4.2 带名存 Cue
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At Full",
    "Attribute \"COLOR1\" At [30]",
    "Store Cue [1] \"[名称]\""
  ]
}
```

### 4.3 存多 Cue
```
# Cue 1: 红色
fixture 1 thru 10
at full
attribute "color1" at 0
store cue 1

# Cue 2: 绿色
fixture 1 thru 10
at full
attribute "color1" at 30
store cue 2

# Cue 3: 蓝色
fixture 1 thru 10
at full
attribute "color1" at 60
store cue 3
```

---

## 5. Assign 模板

### 5.1 Assign 到按钮
```json
{
  "commands": [
    "Assign Cue [1] To Button [101]"
  ]
}
```

### 5.2 Assign 到执行器
```json
{
  "commands": [
    "Assign Cue [1] To Executor [1.1]"
  ]
}
```

### 5.3 Assign 序列
```json
{
  "commands": [
    "Assign Sequence [1] To Executor [1.1]"
  ]
}
```

---

## 6. 播放模板

### 6.1 播放
```json
{
  "commands": [
    "Go Executor [1.1]"
  ]
}
```

### 6.2 暂停
```json
{
  "commands": [
    "Pause Sequence [1]"
  ]
}
```

### 6.3 跳转
```json
{
  "commands": [
    "Goto Cue [5] Sequence [1]"
  ]
}
```

---

## 7. 效果模板

### 7.1 频闪
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At Full",
    "Attribute \"SHUTTER\" At [100]"
  ]
}
```

### 7.2 图案
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At Full",
    "Attribute \"GOBO1\" At [20]"
  ]
}
```

### 7.3 棱镜
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At Full",
    "Attribute \"PRISMA1\" At [50]"
  ]
}
```

### 7.4 柔光
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At Full",
    "Attribute \"FROST\" At [50]"
  ]
}
```

---

## 8. 完整效果模板

### 8.1 派对效果
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At Full",
    "Attribute \"PAN\" At [127]",
    "Attribute \"TILT\" At [0]",
    "Attribute \"COLOR1\" At [60]",
    "Attribute \"GOBO1\" At [30]",
    "Attribute \"PRISMA1\" At [100]"
  ]
}
```

### 8.2 柔和渐变
```json
{
  "commands": [
    "Fixture [1] Thru [10]",
    "At [50]",
    "Attribute \"PAN\" At [127]",
    "Attribute \"TILT\" At [50]",
    "Attribute \"COLOR1\" At [30]",
    "Attribute \"FROST\" At [30]"
  ]
}
```

---

## 9. 歌曲编程模板

### 9.1 120BPM 基础序列
```
# 每小节 2秒 (120BPM, 4/4拍)

# Cue 1: Intro - 红色
fixture 1 thru 10
at full
attribute "color1" at 0
store cue 1

# Cue 2: Verse - 绿色
fixture 1 thru 10
at full
attribute "color1" at 30
store cue 2

# Cue 3: Chorus - 蓝色
fixture 1 thru 10
at full
attribute "color1" at 60
store cue 3

# Assign 到执行器
assign sequence 1 at executor 1.1
```

---

## 10. 颜色值参考

| 颜色 | 值 | 备注 |
|------|-----|------|
| 红 | 0 | |
| 橙 | 10 | |
| 黄 | 20 | |
| 绿 | 30 | |
| 青 | 40 | |
| 蓝 | 60 | |
| 紫 | 70 | |
| 品红 | 80 | |

---

## 11. 位置值参考

| 方向 | PAN | TILT |
|------|-----|------|
| 左 | 0 | - |
| 中 | 127 | 50 |
| 右 | 255 | - |
| 上 | - | 0 |
| 下 | - | 100 |

---

*最后更新: 2026-03-24*
