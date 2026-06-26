# diagram-patterns.md — 常用图表模板

> Mermaid Canvas 参考文件：常用图表类型的代码模板
>
> 版本：v1.0.0

---

## 一、流程图 (flowchart)

### 1.1 基础流程图

```mermaid
flowchart TD
    A[开始] --> B[处理]
    B --> C{判断}
    C -->|是| D[操作A]
    C -->|否| E[操作B]
    D --> F[结束]
    E --> F
```

### 1.2 用户登录流程

```mermaid
flowchart TD
    A["用户打开APP"] --> B{是否已登录}
    B -->|是| C[进入主页]
    B -->|否| D[显示登录页]
    D --> E[输入账号密码]
    E --> F{验证成功?}
    F -->|是| G[生成Token]
    G --> C
    F -->|否| H[显示错误提示]
    H --> D
```

### 1.3 订单处理流程

```mermaid
flowchart LR
    A[用户下单] --> B[支付]
    B --> C{支付成功?}
    C -->|是| D[商家接单]
    C -->|否| E[订单取消]
    D --> F[发货]
    F --> G[物流运输]
    G --> H[用户收货]
    H --> I[完成评价]
```

### 1.4 决策树

```mermaid
flowchart TD
    A{天气好吗?} -->|是| B{有车?}
    A -->|否| C[室内活动]
    B -->|有| D[开车兜风]
    B -->|没| E{预算充足?}
    E -->|是| F[打车出行]
    E -->|否| G[公交出行]
```

### 1.5 子图分组

```mermaid
flowchart TB
    subgraph 前端
        A[Web] --> B[移动端]
    end
    
    subgraph 后端
        C[API] --> D[数据库]
    end
    
    A --> C
    B --> C
```

---

## 二、时序图 (sequenceDiagram)

### 2.1 API 调用时序

```mermaid
sequenceDiagram
    participant 用户
    participant 前端
    participant 后端
    participant 数据库
    
    用户->>前端: 点击按钮
    前端->>前端: 表单验证
    前端->>后端: POST /api/login
    后端->>数据库: SELECT users
    数据库-->>后端: 用户数据
    后端->>后端: 验证密码
    后端-->>前端: JWT Token
    前端-->>用户: 登录成功
```

### 2.2 用户注册时序

```mermaid
sequenceDiagram
    participant 用户
    participant 前端
    participant 后端
    participant 数据库
    participant 邮件服务
    
    用户->>前端: 填写注册信息
    前端->>后端: POST /api/register
    后端->>数据库: INSERT user
    数据库-->>后端: user_id
    后端->>邮件服务: 发送验证码
    邮件服务-->>用户: 验证码邮件
    用户->>前端: 输入验证码
    前端->>后端: POST /api/verify
    后端->>数据库: UPDATE status
    数据库-->>后端: OK
    后端-->>前端: 注册成功
```

### 2.3 微服务调用

```mermaid
sequenceDiagram
    participant 客户端
    participant 网关
    participant 订单服务
    participant 用户服务
    participant 库存服务
    
    客户端->>网关: HTTP Request
    网关->>订单服务: RPC调用
    订单服务->>用户服务: 查询用户
    用户服务-->>订单服务: 用户信息
    订单服务->>库存服务: 扣减库存
    库存服务-->>订单服务: 库存已扣
    订单服务-->>网关: 订单结果
    网关-->>客户端: HTTP Response
```

---

## 三、类图 (classDiagram)

### 3.1 基础类结构

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +isMammal() bool
        +move()
    }
    
    class Dog {
        +String breed
        +bark()
    }
    
    class Cat {
        +boolean indoor
        +meow()
    }
    
    Animal <|-- Dog : inherits
    Animal <|-- Cat : inherits
```

### 3.2 订单系统类图

```mermaid
classDiagram
    class Order {
        +int orderId
        +Date createTime
        +String status
        +calculate() float
        +cancel()
    }
    
    class OrderItem {
        +int itemId
        +int quantity
        +float price
        +getSubtotal() float
    }
    
    class User {
        +int userId
        +String name
        +String email
        +createOrder() Order
    }
    
    class Product {
        +int productId
        +String name
        +float price
        -int stock
    }
    
    Order "1" *-- "N" OrderItem : contains
    User "1" --> "N" Order : places
    OrderItem --> "1" Product : references
```

---

## 四、状态图 (stateDiagram)

### 4.1 订单状态机

```mermaid
stateDiagram-v2
    [*] --> 待支付
    待支付 --> 已支付 : 支付成功
    待支付 --> 已取消 : 超时/用户取消
    已支付 --> 已发货 : 商家发货
    已支付 --> 已取消 : 退款
    已发货 --> 运输中 : 物流揽收
    运输中 --> 已到达 : 到达目的地
    已到达 --> 已签收 : 用户签收
    已签收 --> [*]
    已取消 --> [*]
```

### 4.2 用户状态

```mermaid
stateDiagram-v2
    [*] --> 游客
    游客 --> 注册 : 注册
    注册 --> 激活 : 邮箱验证
    激活 --> 游客 : 未激活超时
    激活 --> 正常 : 完成
    正常 --> 冻结 : 违规
    冻结 --> 正常 : 解冻
    正常 --> 注销 : 用户申请
    注销 --> [*]
```

---

## 五、甘特图 (gantt)

### 5.1 项目进度

```mermaid
gantt
    title 项目开发计划
    dateFormat YYYY-MM-DD
    section 需求
    需求调研       :a1, 2024-01-01, 7d
    需求评审       :a2, after a1, 2d
    section 设计
    架构设计       :a3, after a2, 5d
    详细设计       :a4, after a3, 5d
    section 开发
    前端开发       :a5, 2024-01-20, 14d
    后端开发       :a6, 2024-01-20, 14d
    section 测试
    集成测试       :a7, after a5 a6, 7d
    UAT测试        :a8, after a7, 5d
    section 上线
    部署上线       :a9, after a8, 2d
```

### 5.2 Sprint 计划

```mermaid
gantt
    title Sprint 迭代计划
    dateFormat YYYY-MM-DD
    section Sprint 1
    用户模块       :t1, 2024-03-01, 5d
    权限模块       :t2, after t1, 3d
    section Sprint 2
    订单模块       :t3, 2024-03-09, 5d
    支付模块       :t4, after t3, 3d
    section Sprint 3
    报表模块       :t5, 2024-03-18, 5d
    通知模块       :t6, after t5, 2d
```

---

## 六、饼图 (pie)

### 6.1 项目预算分布

```mermaid
pie title 项目预算分配
    "人力资源" : 45
    "服务器成本" : 25
    "市场推广" : 15
    "办公用品" : 10
    "其他" : 5
```

### 6.2 用户来源统计

```mermaid
pie title 用户来源分布
    "自然流量" : 35
    "搜索引擎" : 28
    "社交媒体" : 18
    "广告投放" : 12
    "其他" : 7
```

---

## 七、思维导图 (mindmap)

### 7.1 产品功能规划

```mermaid
mindmap
    root((产品规划))
        设计
            UI设计
            交互设计
            原型设计
        开发
            前端
                Web
                移动端
            后端
                API
                数据库
        运营
            推广
            数据分析
            用户运营
```

### 7.2 会议纪要

```mermaid
mindmap
    root((会议主题))
        时间
            2024-03-15
            14:00-15:00
        参与人
            张三
            李四
            王五
        讨论内容
            项目进度
            问题汇总
            下一步计划
        决策
            方案A通过
            下周评审
```

---

## 八、架构图 (architecture)

### 8.1 系统架构

```mermaid
architecture-beta
    group api[API层]
        service nginx[负载均衡] [[Nginx]]
        service gateway[网关] [[Gateway]]
    
    group business[业务层]
        service user[用户服务] [[User Service]]
        service order[订单服务] [[Order Service]]
        service pay[支付服务] [[Pay Service]]
    
    group data[数据层]
        service mysql[(MySQL)]
        service redis[(Redis)]
        service es[(Elasticsearch)]
    
    nginx --> gateway
    gateway --> user
    gateway --> order
    gateway --> pay
    user --> mysql
    user --> redis
    order --> mysql
    order --> redis
    pay --> mysql
    pay --> redis
    order --> es
```

---

## 九、ER 图 (erDiagram)

### 9.1 电商 ER 图

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        int id PK
        string name
        string email
        string phone
        datetime created_at
    }
    
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        int id PK
        int user_id FK
        string order_no
        decimal total_amount
        string status
        datetime created_at
    }
    
    ORDER_ITEM ||--|| PRODUCT : references
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal price
    }
    
    PRODUCT {
        int id PK
        string name
        string description
        decimal price
        int stock
    }
```

---

## 十、时间线 (timeline)

### 10.1 项目里程碑

```mermaid
timeline
    title 项目里程碑
    
    2024-Q1
        需求分析
        架构设计
    2024-Q2
        开发完成
        测试通过
    2024-Q3
        上线发布
        用户反馈
    2024-Q4
        版本迭代
        年度总结
```

---

## 十一、用户旅程 (journey)

### 11.1 用户购物流程

```mermaid
journey
    title 用户购物流程
    section 浏览
        打开APP : 5 : 用户
        浏览商品 : 4 : 用户
        查看详情 : 4 : 用户
    section 购买
        加入购物车 : 5 : 用户
        结算订单 : 3 : 用户
        选择支付 : 4 : 用户
    section 售后
        查看物流 : 3 : 用户
        确认收货 : 5 : 用户
        评价商品 : 4 : 用户
```
