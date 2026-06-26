# Mermaid 图表类型参考

本文档列出 mermaid-renderer skill 支持的图表类型及语法示例。

## 流程图 (Graph / Flowchart)

### 方向说明
- `TB` / `TD`: 从上到下
- `BT`: 从下到上
- `LR`: 从左到右
- `RL`: 从右到左

### 节点形状
```
graph LR
    A[矩形] --> B(圆角矩形)
    B --> C((圆形))
    C --> D{菱形}
    D --> E[[子程序]]
```

### 连线样式
```
graph LR
    A --> B      %% 实线箭头
    C --- D      %% 实线无箭头
    E -.-> F     %% 虚线箭头
    G ==> H      %% 粗线箭头
    I --文字--> J  %% 带文字
```

## 时序图 (Sequence Diagram)

### 基本语法
```
sequenceDiagram
    participant 用户
    participant dodo
    participant 后端
    用户->>dodo: 发送请求
    dodo->>后端: 转发处理
    后端-->>dodo: 返回结果
    dodo-->>用户: 响应消息
```

### 箭头类型
- `->>`: 实线箭头（请求）
- `-->>`: 虚线箭头（响应）
- `-)`: 实线开放箭头（异步）
- `--)`: 虚线开放箭头（异步返回）
- `->x`: 实线叉号（拒绝）

### 激活框
```
sequenceDiagram
    participant A
    participant B
    activate A
    A->>B: 请求
    activate B
    B-->>A: 响应
    deactivate B
    deactivate A
```

## 类图 (Class Diagram)

### 基本语法
```
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +String breed
        +bark()
    }
    Animal <|-- Dog : 继承
```

### 关系类型
- `<|--`: 继承
- `*--`: 组合
- `o--`: 聚合
- `-->`: 关联
- `--`: 链接
- `..>`: 依赖
- `..|>`: 实现

### 可见性
- `+`: public
- `-`: private
- `#`: protected
- `~`: package/internal

## 饼图 (Pie Chart)

### 基本语法
```
pie title 用户分布
    "前端工程师" : 35
    "后端工程师" : 40
    "测试工程师" : 15
    "其他" : 10
```

## Git 分支图 (Git Graph)

### 基本语法
```
gitGraph
    commit id: "初始化"
    branch develop
    checkout develop
    commit id: "添加功能A"
    commit id: "修复bug"
    checkout main
    merge develop id: "v1.0"
    branch feature
    checkout feature
    commit id: "新特性"
    checkout main
    merge feature id: "v1.1"
```

### 支持的操作
- `commit`: 提交
- `branch`: 创建分支
- `checkout`: 切换分支
- `merge`: 合并分支
- `cherry-pick`: 摘取提交

## 状态图 (State Diagram)

### 基本语法
```
stateDiagram-v2
    [*] --> 待处理
    待处理 --> 处理中: 开始处理
    处理中 --> 已完成: 处理完成
    处理中 --> 失败: 处理出错
    失败 --> 处理中: 重试
    已完成 --> [*]
```

## ER 图 (Entity Relationship)

### 基本语法
```
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "ordered in"
    USER {
        int id PK
        string name
        string email
    }
    ORDER {
        int id PK
        date created_at
        string status
    }
```

### 关系符号
- `||--||`: 一对一
- `||--o{`: 一对多
- `}o--o{`: 多对多

## 输出模式选择

| 图表类型 | 终端 ASCII | 图片导出 |
|----------|------------|----------|
| 流程图 | ✅ | ✅ |
| 时序图 | ✅ | ✅ |
| 类图 | ✅ | ✅ |
| 饼图 | ✅ | ✅ |
| Git分支图 | ✅ | ✅ |
| 状态图 | ✅ | ✅ |
| ER图 | ✅ | ✅ |

图例：✅ 支持
