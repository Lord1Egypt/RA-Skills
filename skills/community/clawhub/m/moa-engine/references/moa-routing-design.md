# MoA 智能路由规则 (v2.1)

## 目录

- [定位](#定位)
- [执行状态对象](#执行状态对象)
- [一、标签过滤路由](#一标签过滤路由)
- [二、依赖感知路由](#二依赖感知路由)
- [三、优先级路由](#三优先级路由)
- [四、动态批判者指派](#四动态批判者指派)
- [五、跨角色信息回流](#五跨角色信息回流)
- [RHI 可进化的路由项](#rhi-可进化的路由项)

## 定位

智能路由属于同步执行层——模型在 MoA 运行中的自主路由判断。RHI 修改的是路由规则的定义和标签体系（异步进化层），但路由的执行逻辑本身是 MoA 系统的设计能力。

## 执行状态对象

模型内部维护以下执行状态，在角色切换时参考它决定当前角色应看到什么、做什么：

```
ExecutionState {
  current_phase: 0-4
  subtasks: {
    A: { status: ready|blocked|unblocked|done, dependencies: [] },
    B: { status: blocked, dependencies: [A] },
    ...
  }
  critics: [
    { role, target, source: planned|dynamic, attacks: [...] }
  ]
  attacks_queue: [
    { id, severity, status: pending|addressed|disputed|resolved }
  ]
  conflict_queue: [未解决的冲突和反驳]
  termination: null | clear | needs_more_rounds
  signals: [已产出的信号标签]
}
```

## 一、标签过滤路由

### 按需加载规则

`<technical_detail>` 对批判者是"按需"可见。批判者采用渐进式加载：

1. 先看所有 `<proposal>` 和 `<boundary>`（摘要层）
2. 根据 `domain` 属性匹配判断哪些方案需要深入
3. 对需要深入的方案，拉取完整 `<technical_detail>`
4. 对不需要深入的方案，仅做摘要级审视
5. 摘要级发现疑点时，再拉取 `<technical_detail>` 验证

### 信息请求机制

批判者可以主动请求更多信息：

```xml
<request_info target="expert_role" tag="technical_detail" section="需要展开的部分"/>
```

被请求的专家在下一轮产出中用 `<technical_detail visible_to="critic" section="指定部分">` 回应。

## 二、依赖感知路由

### 依赖图管理

Phase 1 的 `<decomposition>` 定义 `<dependency>` 关系。路由引擎维护依赖图：

- subtask A (无依赖) → ready → expert 产出 → done
- subtask B (依赖 A) → blocked → 等待 A 的 `<proposal>` → A 完成后 unblocked
- subtask C (依赖 A,B) → blocked → 等待 A 和 B 都产出 → unblocked

### 依赖信息传递

当 B 依赖 A，A 产出后：
- B 的 expert 自动收到 A 的 `<proposal>` 摘要
- B 的 expert 用 `<referenced_dependency source="subtask:A">` 引用 A 的结论
- 若 B 发现与 A 冲突，用 `<conflict_ref source="subtask:A" point="...">` 标记
- 冲突标记自动路由给 molder 在 Phase 4 处理

### 循环依赖检测

Phase 1 输出后显式检测循环依赖：
- 若发现 A→B→A 循环，标记 `<circular_detected>`
- 路由回 planner 要求重新分解
- 不进入 Phase 2 直到循环消除

## 三、优先级路由

### 严重度驱动的处理顺序

| severity | 处理顺序 | 行为 |
|----------|---------|------|
| 致命 | 第一优先 | 立即修正，修正前不处理其他攻击 |
| 重要 | 第二优先 | 处理完致命问题后修正 |
| 次要 | 批量处理 | 所有致命和重要问题处理后批量回应 |

### 反驳触发的优先级调整

当专家使用 `<response type="反驳">` 时：
- 被反驳的 attack 标记 disputed，进入争议队列
- 该攻击从"已修正"队列移出
- 批判者下轮回应：撤回攻击或提供更深论据
- 未解决的争议路由给 molder 在 Phase 4 裁决
- 反驳不阻塞其他非争议攻击的处理

### 终止信号优先级

- `status="clear"` → 进入 Phase 4
- `status="needs_more_rounds"` → 路由回 Phase 3 新一轮
- 高风险任务中 molder 可 override 终止信号强制追加轮次，须在 `<decision_chain>` 记录 override 理由

## 四、动态批判者指派

### 机制

Phase 2 产出后，路由引擎扫描所有 `<proposal>` 的 `domain` 属性：

```
Phase 2 专家产出 → <proposal> 携带 domain 属性
    ↓
路由引擎扫描 domain 覆盖情况
    ↓
发现某 domain 未被任何 planned critic 覆盖
    ↓
标记 <critic_gap domain="未覆盖的域">
    ↓
planner 动态追加 <critic role="新头衔" target="相关专家" source="dynamic">
    ↓
新批判者在 Phase 3 加入对抗
```

### 约束

1. **只增不减**：动态机制只能追加批判者，不能移除 Phase 1 指派的批判者
2. **数量上限**：动态追加不超过初始批判者数量
3. **来源标记**：`source="dynamic"` 与 `source="planned"` 区分
4. **不修改已有批判**：动态批判者只对尚未被批判的内容发起攻击

## 五、跨角色信息回流

### 专家间可见性

默认不可见（防同质化），例外：
- 依赖驱动可见：B 依赖 A 时，B 可见 A 的 `<proposal>` 摘要
- 冲突标记触发：B 用 `<conflict_ref>` 标记与 A 的冲突时，A 被通知，可见 B 的冲突标记段落

### 批判者间可见性

默认不可见（防趋同），例外：
- 多个批判者对同一 expert 同一 proposal 攻击时，后发者可看到先发者的 `<attack>` 标题和 severity（不含完整内容），避免重复
- 动态追加的批判者可看到已有批判者的 `<attack>` 列表

### molder 渐进解锁

Phase 4 开始时获得全量解锁，加载顺序：
1. 所有 `<proposal>` + `<boundary>` + `<revision>` 摘要
2. 所有 `<attack>` 和 `<response>` 完整内容
3. `<termination_signal>` 和 `<signal>` 标签
4. 争议队列中未解决的 `<conflict_ref>`
5. 产出 `<highlights>` → `<conflict_resolution>` → `<final_answer>`

## RHI 可进化的路由项

| 可进化项 | 说明 |
|---------|------|
| visible_to 默认值 | 调整信息可见性 |
| domain 匹配规则 | 当前字符串匹配，RHI 可升级为语义匹配 |
| critic_gap 检测逻辑 | 当前 domain 未覆盖即追加，RHI 可加入复杂度评估 |
| 动态批判者数量上限 | 当前不超过初始数量，RHI 可按复杂度调整 |
| 严重度优先规则 | 可调整优先级策略（但下限不可降） |
| 反驳争议处理流程 | 可调整争议流转逻辑 |
| 跨角色可见性规则 | 可调整回流触发条件 |
| molder 解锁策略 | 可调整加载顺序和粒度 |
| source 类型 | 可增加新来源（如 "rhi_suggested"） |
