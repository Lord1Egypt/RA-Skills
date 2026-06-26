# Mermaid 图表语法速查

## 1. 流程图 (Flowchart)

### 基本语法

```mermaid
flowchart TD
    A[矩形] --> B{菱形}
    B -->|是| C[圆角矩形]
    B -->|否| D((圆形))
    C --> E[[子程序]]
    D --> F[(数据库)]
```

### 方向
- `TD` / `TB` - 从上到下
- `BT` - 从下到上
- `LR` - 从左到右
- `RL` - 从右到左

### 节点形状
| 语法 | 形状 |
|-----|------|
| `A[文字]` | 矩形 |
| `A(文字)` | 圆角矩形 |
| `A((文字))` | 圆形 |
| `A{文字}` | 菱形 |
| `A{{文字}}` | 六边形 |
| `A[[文字]]` | 子程序 |
| `A[(文字)]` | 数据库 |
| `A[(文字)]` | 圆柱 |

### 连接线
| 语法 | 样式 |
|-----|------|
| `-->` | 实线箭头 |
| `---` | 实线无箭头 |
| `-.->` | 虚线箭头 |
| `-.-` | 虚线无箭头 |
| `==>` | 粗线箭头 |
| `===` | 粗线无箭头 |
| `--文字-->` | 带文字 |

### 子图

```mermaid
flowchart TB
    subgraph 一组
        A --> B
    end
    subgraph 二组
        C --> D
    end
    B --> C
```

---

## 2. 状态图 (State Diagram)

### 基本语法

```mermaid
stateDiagram-v2
    [*] --> 状态A
    状态A --> 状态B: 触发条件
    状态B --> [*]
```

### 复合状态

```mermaid
stateDiagram-v2
    [*] --> 待处理
    
    state 处理中 {
        [*] --> 审核中
        审核中 --> 执行中
        执行中 --> [*]
    }
    
    待处理 --> 处理中: 开始处理
    处理中 --> 已完成: 处理完成
    已完成 --> [*]
```

### 并行状态

```mermaid
stateDiagram-v2
    state fork_state <<fork>>
    state join_state <<join>>
    
    [*] --> fork_state
    fork_state --> 分支A
    fork_state --> 分支B
    分支A --> join_state
    分支B --> join_state
    join_state --> [*]
```

---

## 3. 时序图 (Sequence Diagram)

### 基本语法

```mermaid
sequenceDiagram
    participant A as 参与者A
    participant B as 参与者B
    
    A->>B: 同步消息
    B-->>A: 返回消息
    A-)B: 异步消息
    A-xB: 失败消息
```

### 消息类型
| 语法 | 类型 |
|-----|------|
| `->>` | 实线箭头(同步) |
| `-->>` | 虚线箭头(返回) |
| `->>` | 实线开放箭头 |
| `--)` | 实线异步箭头 |
| `-x` | 实线叉号(失败) |

### 注释和框

```mermaid
sequenceDiagram
    participant A
    participant B
    
    Note over A,B: 跨参与者注释
    Note over A: 单参与者注释
    
    rect rgb(200, 220, 240)
        A->>B: 在框内的消息
    end
    
    loop 循环条件
        A->>B: 重复消息
    end
    
    alt 条件A
        A->>B: 分支A
    else 条件B
        A->>B: 分支B
    end
```

---

## 4. ER 图 (Entity Relationship)

### 基本语法

```mermaid
erDiagram
    ENTITY_A {
        type field1 PK
        type field2 FK
        type field3
    }
```

### 关系类型
| 语法 | 关系 |
|-----|------|
| `\|o--o\|` | 一对一 |
| `\|o--o{` | 一对多 |
| `}o--o{` | 多对多 |
| `\|\|--\|\|` | 必须关联 |

### 示例

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        bigint id PK
        string name
        string email UK
    }
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        bigint id PK
        string order_no UK
        decimal amount
    }
    PRODUCT ||--o{ ORDER_ITEM : "ordered in"
    PRODUCT {
        bigint id PK
        string name
        decimal price
    }
```

---

## 5. 类图 (Class Diagram)

### 基本语法

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
    }
    
    class Dog {
        +String breed
        +bark() void
    }
    
    Animal <|-- Dog : 继承
```

### 关系类型
| 语法 | 关系 |
|-----|------|
| `<\|--` | 继承 |
| `*--` | 组合 |
| `o--` | 聚合 |
| `-->` | 关联 |
| `--` | 链接 |
| `..>` | 依赖 |
| `..\|>` | 实现 |

### 可见性
| 符号 | 可见性 |
|-----|------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package/Internal |

---

## 常用模板

### 订单流程

```mermaid
flowchart TD
    A[用户下单] --> B{库存检查}
    B -->|充足| C[创建订单]
    B -->|不足| D[提示缺货]
    C --> E[等待支付]
    E -->|支付成功| F[扣减库存]
    E -->|超时| G[取消订单]
    F --> H[发货]
    H --> I[完成]
```

### 系统交互

```mermaid
sequenceDiagram
    participant U as 用户
    participant C as 客户端
    participant S as 服务端
    participant DB as 数据库
    
    U->>C: 发起请求
    C->>S: API调用
    S->>DB: 数据操作
    DB-->>S: 返回结果
    S-->>C: 响应数据
    C-->>U: 展示结果
```

### 状态流转

```mermaid
stateDiagram-v2
    [*] --> 草稿
    草稿 --> 待审核: 提交
    待审核 --> 已发布: 审核通过
    待审核 --> 草稿: 驳回
    已发布 --> 已下架: 下架
    已下架 --> 已发布: 重新发布
    已发布 --> [*]
```
