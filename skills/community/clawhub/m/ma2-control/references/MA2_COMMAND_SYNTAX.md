# MA2 命令行语法详解

> 来源: 官方帮助文档

---

## 1. 命令结构

### 基本语法
```
[Function] [Object] [Options]

例如:
Fixture 1 Thru 10
At Full
Store Cue 1
```

### 常用关键字

| 关键字 | 说明 |
|--------|------|
| Thru | 范围 |
| + | 添加到选择 |
| At | 设置值 |
| If | 条件 |

---

## 2. 选择器语法

### Fixture 选择
```
Fixture 1              -- 单个
Fixture 1 Thru 10     -- 范围
Fixture 1 + 3 + 5    -- 多选
Fixture Thru          -- 全部
Fixture 1.5           -- 子属性
```

### Group 选择
```
Group 1
Group 1 Thru 5
Group 1 + 2 + 3
```

### 特殊选择
```
Selected                 -- 当前选中
Programmer              -- 编程器
Executor 1              -- 执行器
```

---

## 3. At 关键字

### 亮度
```
At Full                -- 100%
At 0                  -- 0%
At 50                 -- 50%
At +10                -- 相对+10%
At -10                -- 相对-10%
At Cue 1              -- 应用Cue1的值
```

### 属性值
```
At Preset 1.5         -- 应用预设
At Effect 1          -- 应用效果
At EffectLow          -- 效果低值
At EffectHigh         -- 效果高值
```

---

## 4. Store 命令

### 基本存储
```
Store Cue 1            -- 存Cue
Store Cue 1 "名称"     -- 带名存
Store Group 1         -- 存组
Store Effect 1        -- 存效果
Store Preset 1.1      -- 存预设
```

### 存储选项
```
Store Cue 1 /merge     -- 合并
Store Cue 1 /overwrite -- 覆盖
Store Cue 1 /noconfirm -- 无确认
Store Cue 1 /cueonly   -- 仅Cue
```

---

## 5. Assign 命令

### 赋值
```
Assign Cue 1 To Executor 1.1    -- Cue到执行器
Assign Cue 1 To Button 101      -- Cue到按钮
Assign Cue 1 To Group 1         -- Cue到组
Assign Sequence 1 To Executor 1  -- 序列到执行器
```

### 参数赋值
```
Assign Fade 3 To Cue 1           -- Fade时间
Assign Delay 1 To Cue 1         -- 延迟
```

---

## 6. 条件关键字

### If 条件
```
If Fixture 1 At Full Then ...
If Group 1 > 50% Then ...
```

---

## 7. 宏命令

### 常用宏
```
Macro 1                -- 执行宏1
Store Macro 1         -- 存宏
Go Macro 1            -- 运行宏
```

---

## 8. 查询命令

### List
```
List Cue               -- 列表Cue
List Cue 1 Thru 10    -- 列表范围
List Executor         -- 列表执行器
List Fixture          -- 列表灯具
List Group            -- 列表组
List Preset           -- 列表预设
List Attribute        -- 列表属性
```

### Info
```
Info Cue 1             -- Cue信息
Info Fixture 1        -- 灯具信息
Info Group 1          -- 组信息
```

---

## 9. 快捷键

| 按键 | 功能 |
|------|------|
| Please | 确认 |
| @ | 应用 |
| + | 添加 |
| - | 减去 |
| Thru | 范围 |
| / | 选项 |

---

## 10. 常用组合

### 开灯+颜色
```
Fixture 1 Thru 10
At Full
Attribute "Color1" At 30
```

### 存Cue
```
Fixture 1 Thru 10
At Full
Store Cue 1
Assign Cue 1 To Executor 1.1
```

### 批量
```
Copy Cue 1 Thru 10 At 11
Move Cue 1 Thru 5 At 6
Delete Cue 1
```

---

*最后更新: 2026-03-25*
