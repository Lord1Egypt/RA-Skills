# 触发时机参考表

| 扩展点 | 触发时机 | 适用场景 |
|--------|---------|---------|
| **Builder** | 构建执行阶段，在`perform()`调用时 | 自定义构建步骤 |
| **Publisher** | 构建完成后（成功/失败/不稳定） | 通知、归档、报告 |
| **Trigger** | 按Cron表达式或SCM变更 | 定时构建、自动触发 |
| **SCM** | 轮询检测到变更时 | Git/SVN变更检测 |
| **Action** | 用户点击链接/按钮时 | 手动操作、数据查看 |
| **RunListener** | 构建开始/结束/状态变更 | 审计、监控、指标 |
| **ItemListener** | 项目创建/删除/重命名 | 项目生命周期管理 |
| **ComputerListener** | 节点上线/离线/配置变更 | 节点监控、资源管理 |
| **QueueTaskDispatcher** | 任务分配节点时 | 负载均衡、节点过滤 |
| **BuildWrapper** | 构建前后（包装构建） | 环境准备、清理 |
| **EnvironmentContributor** | 构建开始时 | 环境变量注入 |
| **SCMBrowser** | 查看SCM变更时 | 自定义SCM浏览 |
