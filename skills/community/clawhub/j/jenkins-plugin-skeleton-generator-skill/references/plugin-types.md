# 插件类型 / 扩展点参考

| 插件类型 | 核心类/接口 | 触发时机 | 主要方法 |
|---------|------------|---------|---------|
| Builder | Builder | 构建执行阶段 | `perform()` |
| Publisher | Publisher | 构建完成后 | `perform()` |
| Trigger | Trigger | 定时/轮询触发 | `run()` |
| Action | Action | 界面交互 | `doXxx()` |
| RunListener | RunListener | 构建生命周期事件 | `onStarted()`, `onCompleted()` |
| ComputerListener | ComputerListener | 节点状态变更 | `onOnline()`, `onOffline()` |
| QueueTaskDispatcher | QueueTaskDispatcher | 任务分配时 | `canTake()` |

## 插件类型选择指南

根据目标场景选择对应的扩展点：

- **Builder**：自定义构建步骤 — 适用模板 `templates/builder.md`
- **Publisher**：构建完成后执行 — 与 Builder 类似，父类为 `Publisher`
- **Trigger**：定时/Cron 触发 —  实现 `Trigger` 并重写 `run()`
- **Action**：手动操作、数据查看 — 实现 `Action` 接口
- **RunListener**：构建生命周期审计 — 适用模板 `templates/run-listener.md`
- **ComputerListener**：节点上线/离线监控 — 实现 `ComputerListener`
- **QueueTaskDispatcher**：任务分配过滤 — 实现 `QueueTaskDispatcher`
