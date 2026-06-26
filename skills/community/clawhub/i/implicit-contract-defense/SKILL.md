---
name: implicit-contract-defense
description: >
  Rust + SeaORM + 任意前端的隐式契约防御规范。
  当项目涉及 Rust 后端 + 前端 + 数据库开发时激活。
  核心：所有跨边界交互收敛到隔离仓，内部壳只写纯 Rust 逻辑。
---

# 隐式契约防御

> 两段代码假设了同一件事，但没有机制保证一致。改了一处，另一处静默腐坏。这就是隐式契约。

适用：前端（任意）+ Rust + SeaORM + 数据库（任意）

## 架构：隔离仓（外壳）/ 内壳

```
┌─────────────────────────────────────────────┐
│  隔离仓（外壳）— 所有跨边界交互在此收敛      │
│                                             │
│  ┌─────────────┐  ┌────────┐  ┌──────────┐ │
│  │ contracts   │  │ consts │  │ entity/  │ │
│  │ (API 类型)  │  │ (常量) │  │ (数据表) │ │
│  └─────────────┘  └────────┘  └──────────┘ │
├─────────────────────────────────────────────┤
│  内壳 — 纯 Rust 业务逻辑                     │
│  只引用隔离仓的类型和常量，不碰外部数据       │
└─────────────────────────────────────────────┘
```

---

## 分区一：API 契约（contracts.rs）

后端有且仅有一个文件定义所有与前端交互的请求/响应结构体。

- 所有 `#[ts(export)]` 只允许出现在此文件
- API 边界用到的枚举也定义在此文件
- 前端类型由 `gen_types.sh` 自动生成（`cargo test` → ts-rs 导出 → 合并到前端指定路径），禁止手动修改

```rust
// contracts.rs
use serde::{Deserialize, Serialize};
use ts_rs::TS;

#[derive(Serialize, Deserialize, TS)]
#[ts(export)]
pub struct CreateTaskRequest {
    pub title: String,
    pub prompt: String,
    pub agent_type: AgentType,
}

#[derive(Serialize, Deserialize, TS)]
#[ts(export)]
pub struct TaskResponse {
    pub id: String,
    pub status: TaskStatus,
    pub created_at: String,
}
```

---

## 分区二：常量（consts.rs）

有且仅有一个文件集中定义所有业务常量。`true`/`false`/`0`/`1` 除外，其余字面量都算魔法值。

- 能用 enum 穷举的优先 enum，不用常量
- 路径/文件名用 struct 方法封装，不用字符串常量

```rust
// consts.rs
pub const DEFAULT_TIMEOUT_MS: u64 = 5000;
pub const MAX_ROUNDS: usize = 3;
pub const DEFAULT_PAGE_SIZE: usize = 20;
```

---

## 分区三：数据库实体（entity/*.rs）

一个文件完全表达一张表。打开 entity 文件就能知道表的一切，无需连数据库、无需看 DDL。

### 类型映射

| 数据表特性 | Rust 写法 |
|---|---|
| NOT NULL | `pub name: String` |
| 可为 NULL | `pub name: Option<String>` |
| 枚举字段 | Rust enum + `DeriveActiveEnum` |
| JSON 字段 | 强类型 struct + `FromJsonQueryResult` |
| 时间字段 | `DateTimeUtc` |
| 默认值 | `#[sea_orm(default_value = "xxx")]` |

### 状态枚举带流转检查

有状态流转的枚举必须实现 `can_transition_to()`，状态变更前必须调用：

```rust
#[derive(Clone, Debug, PartialEq, Eq, EnumIter, DeriveActiveEnum, Serialize, Deserialize)]
#[sea_orm(rs_type = "String", db_type = "String(StringLen::N(20))")]
pub enum TaskStatus {
    #[sea_orm(string_value = "pending")]
    Pending,
    #[sea_orm(string_value = "running")]
    Running,
    #[sea_orm(string_value = "success")]
    Success,
    #[sea_orm(string_value = "failed")]
    Failed,
}

impl TaskStatus {
    pub fn can_transition_to(&self, next: &TaskStatus) -> bool {
        matches!((self, next),
            (Self::Pending, Self::Running)
            | (Self::Running, Self::Success)
            | (Self::Running, Self::Failed)
            | (Self::Failed, Self::Pending)
        )
    }
}
```

### Entity 文件要求

- 文件级 `//!` doc comment（业务规则、状态流转、关联关系）
- 每个字段 `///` 注释（业务含义，不是字段名复述）
- 使用 SeaORM Entity First 自动建表，不手写 migration
- 跨表操作用事务（`db.transaction`）
- 软删除表查询过滤 `is_deleted`

### Entity 示例

```rust
//! # tasks 表 — 编码任务
//!
//! ## 业务规则
//! - 一个 task 对应一次容器执行，容器内 agent 自主完成编码
//! - prompt 是用户提交的原始需求，不可修改；执行中的补充指令走 exec_plan
//! - rounds_used 由 entrypoint wrapper 回报，不由业务代码直接写入
//!
//! ## 状态流转
//! Pending → Running → Success/Failed，Failed → Pending（重试）
//! cancel 操作：Running → Cancelled（需 kill 容器）
//!
//! ## 关联
//! - container_id 关联 Docker/Podman 容器（逻辑外键，不建物理外键）
//! - 未来 Phase 2 会关联 projects 表
//!
//! ## 软删除
//! 此表使用软删除（is_deleted），查询活跃记录必须过滤

use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Eq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "tasks")]
pub struct Model {
    /// 主键 UUID，由后端生成
    #[sea_orm(primary_key, auto_increment = false)]
    pub id: String,

    /// 任务标题，用于列表展示
    pub title: String,

    /// 用户提交的原始 prompt，创建后不可修改
    #[sea_orm(column_type = "Text")]
    pub prompt: String,

    /// 任务状态，变更前必须调用 TaskStatus::can_transition_to()
    #[sea_orm(default_value = "pending")]
    pub status: TaskStatus,

    /// agent 实际执行的轮次数，由 entrypoint wrapper 的 report.json 回填
    #[sea_orm(default_value = 0)]
    pub rounds_used: i32,

    /// 软删除标记，false=活跃，true=已删除
    #[sea_orm(default_value = false)]
    pub is_deleted: bool,

    /// 创建时间 UTC
    pub created_at: DateTimeUtc,

    /// 完成时间 UTC，任务结束（成功/失败/取消）时写入
    pub finished_at: Option<DateTimeUtc>,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}
impl ActiveModelBehavior for ActiveModel {}
```

---

## 内壳规则

隔离仓之外的 Rust 代码：

1. 所有外部数据（用户输入、LLM 输出、API 返回、容器产出）在入口处立即 `serde` 反序列化到强类型，失败即 Error
2. 引用 `consts.rs` 的常量或 enum 变体，不内联字面量
3. 通过 SeaORM Entity/ActiveModel 操作数据库，不写裸 SQL

## 并发

优先消灭共享可变状态：单线程 event loop > Actor 模型（tokio channel）> 不可变数据 + 消息传递。避免在业务代码中用 Mutex/RwLock。

## 演化

改类型定义 → 编译器报错 → 逐个修复 → 全部通过。改 contracts.rs → 重新 `gen_types.sh` → 前端编译报错 → 修复。隔离仓的价值：把变更传播交给编译器。

---

## 脚本

| 脚本 | 用途 | 用法 |
|------|------|------|
| `check_contracts.sh` | CI 检测，拦截违规 | `./check_contracts.sh [src_dir]` |
| `gen_types.sh` | 生成前端类型文件 | `./gen_types.sh <ts_rs_output_dir> <frontend_types_path>`，在后端目录下运行 |

脚本顶部有 CONFIG 区域，agent 根据项目实际路径修改。

---

## Agent 行动指南

**初始化**：创建 contracts.rs + consts.rs + entity/ 目录，将两个脚本放入项目并配置路径，Cargo.toml 加 ts-rs 依赖。

**开发**：新增 API → 先在 contracts.rs 定义类型 → 再写逻辑。新增表 → 先写 entity 文件。新增常量 → 加到 consts.rs。每次改完跑 `check_contracts.sh`。

**先看 entity 文件**了解数据表，一个文件 = 一张表的全部信息。
