# Action Type — 让知识图谱从"只读"变成"可写"

## 7阶段执行生命周期

```
阶段1 表单渲染    → 字段类型、条件显示、默认值
阶段2 前端校验    → 必填、格式、跨字段联动（仅用户体验，不是安全边界）
阶段3 提交请求    → HTTPS POST → Foundry Action API
阶段4 权限检查    → 执行权限 + 对象写权限（服务端强制）
阶段5 后端校验    → Validation Function（TypeScript）← 真正的安全边界
阶段6 副作用执行  → 事务性操作
阶段7 审计日志    → 自动、不可篡改
```

## 7种副作用类型

| 类型 | 事务保障 | 执行方式 |
|------|---------|---------|
| Modify Object | 原子提交 | 同步 |
| Create Object | 原子提交 | 同步 |
| Delete Object（软删除） | 原子提交 | 同步 |
| Create Link | 原子提交 | 同步 |
| Delete Link | 原子提交 | 同步 |
| Trigger Webhook | 最终一致 | 异步 |
| Trigger Workflow | 异步启动 | 异步 |

前5种同步事务（要么全成要么全败）；Webhook/Workflow 异步，本体操作成功不代表 Webhook 一定送达。

## 高级特性：Parameter Derivation

选择 Project 后自动过滤出该项目的 Manager 作为 Approver 候选，减少输入错误。

## 设计原则

- 一个 Action 只做一件事（反例：把"分配员工"和"发送通知"放在同一 Action，事务边界混乱）
- **永远不信任前端数据**：后端 Validation Function 才是安全边界
- Webhook 接收端必须幂等，使用唯一 Action 执行 ID 作为幂等键
