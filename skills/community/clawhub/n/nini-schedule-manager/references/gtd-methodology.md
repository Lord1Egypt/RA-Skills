# GTD 方法论指南

GTD (Getting Things Done) 是一套个人生产力方法论，核心思想是将所有待办事项从大脑转移到可靠的外部系统中。

## GTD 五步流程

```text
收集 → 处理 → 组织 → 回顾 → 执行
Capture → Clarify → Organize → Reflect → Engage
```

### 1. 收集 (Capture)

将所有「东西」从大脑中清空到收件箱：

- 想法、任务、承诺
- 会议、约会、截止日期
- 项目、目标、参考资料

**工具映射**：Reminders「收件箱」列表

```bash
# 快速收集
osascript -e 'tell application "Reminders" to tell list "收件箱" to make new reminder with properties {name:"<想法>"}'
```

### 2. 处理 (Clarify)

对收件箱中的每一项进行决策：

```text
这是什么？
  └─ 可执行吗？
       ├─ 是 → 下一步行动是什么？
       │    ├─ < 2 分钟 → 立即做
       │    ├─ 委派他人 → 等待列表
       │    └─ 推迟 → 日程或待办
       └─ 否 → 垃圾/参考资料/将来某天
```

### 3. 组织 (Organize)

将处理后的项目放入合适的系统：

| 类型 | 工具 | 说明 |
|------|------|------|
| 固定时间承诺 | Calendar | 会议、约会、截止日期 |
| 待办事项 | Reminders | 无固定时间的任务 |
| 项目 | Reminders 列表 | 多步骤目标 |
| 参考资料 | Notes/文件系统 | 非可执行信息 |

### 4. 回顾 (Reflect)

定期检查系统，保持信任：

- **每日回顾**：查看今日日程和待办
- **每周回顾**：全面检查所有列表和项目

### 5. 执行 (Engage)

根据以下因素选择下一步行动：

1. **情境**：你在哪里？有什么工具？
2. **可用时间**：有多少时间？
3. **可用精力**：精力状态如何？
4. **优先级**：什么最重要？

## Calendar vs Reminders 决策树

```text
这个任务有具体的时间约束吗？
├─ 是：必须在某个时间发生（会议、约会）
│    └─ 使用 Calendar
├─ 是：有截止日期但可灵活安排
│    └─ 使用 Reminders（设置 due date）
└─ 否：可以任何时间完成
     └─ 使用 Reminders（无 due date）
```

**Calendar 适用场景**：

- 会议、电话会议
- 约会、预约
- 航班、火车
- 他人设定的截止日期
- Time Blocking（专注工作时间段）

**Reminders 适用场景**：

- 购物清单
- 待办任务
- 想法收集
- 项目下一步行动
- 等待他人的事项

## Time Blocking 技巧

将重要任务安排到日历上的特定时间块：

```bash
# 创建 Time Block
osascript -e '
tell application "Calendar"
    tell calendar "工作"
        set startDate to (current date)
        set hours of startDate to 9
        set minutes of startDate to 0
        set endDate to startDate + (2 * hours)
        make new event with properties {
            summary:"[专注] 写报告",
            start date:startDate,
            end date:endDate,
            description:"勿扰时间"
        }
    end tell
end tell'
```

**Time Blocking 原则**：

- 为最重要的任务预留最佳精力时段
- 预留缓冲时间（计划时间 × 1.5）
- 标记为「专注」或「勿扰」
- 保护 Time Block，减少会议侵占

## 每日规划流程

1. **查看今日日历**

   ```bash
   icalBuddy eventsToday
   ```

2. **查看待办事项**

   ```bash
   osascript -e 'tell application "Reminders" to get name of (reminders whose completed is false)'
   ```

3. **选择 3 个最重要任务（MIT）**

4. **为 MIT 安排 Time Block**

## 周回顾检查清单

每周进行一次完整回顾（建议周日或周五）：

### 清空收件箱

- [ ] 处理 Reminders 收件箱中的所有项目
- [ ] 检查邮件收件箱
- [ ] 检查笔记中的待办

### 回顾日历

```bash
# 回顾过去一周
icalBuddy eventsFrom:"-7d" to:today

# 预览下周
icalBuddy eventsFrom:today to:"+7d"
```

### 回顾列表

- [ ] 检查所有 Reminders 列表
- [ ] 更新项目进度
- [ ] 清理已完成的项目
- [ ] 添加遗漏的任务

### 规划下周

- [ ] 确定下周 3 个最重要目标
- [ ] 为重要任务安排 Time Block
- [ ] 检查是否有准备工作需要提前完成

## 推荐 Reminders 列表结构

```text
收件箱        # 快速收集，待处理
工作          # 工作相关任务
个人          # 个人事务
购物清单      # 购物项目
等待中        # 等待他人的事项
将来/可能     # 暂不执行但不想忘记的
```

## 常见陷阱

1. **把日历当待办用**：日历应该只放有时间约束的事项
2. **收件箱堆积**：每日清空收件箱
3. **跳过周回顾**：周回顾是保持系统可信的关键
4. **过度规划**：专注于下一步行动，而非完美计划
5. **忽略情境**：根据当前情境选择任务，而非按顺序执行

## 参考资料

- David Allen, *Getting Things Done*
- [GTD 官方论坛](https://forum.gettingthingsdone.com/)
