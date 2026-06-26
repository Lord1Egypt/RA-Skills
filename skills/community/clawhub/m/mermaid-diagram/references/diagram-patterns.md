# Mermaid 图模式库

产品经理常用图的完整示例代码。

---

## 1. 产品架构图（分层）

```mermaid
flowchart TB
    subgraph UX["用户体验层"]
        A1[Web端] 
        A2[移动端] 
        A3[API接入]
    end
    subgraph Product["产品功能层"]
        B1[核心功能A]
        B2[核心功能B]
        B3[核心功能C]
    end
    subgraph AI["AI/数据层"]
        C1[推荐模型]
        C2[用户画像]
        C3[内容理解]
    end
    subgraph Infra["基础设施层"]
        D1[计算集群]
        D2[数据存储]
        D3[消息队列]
    end
    UX --> Product
    Product --> AI
    AI --> Infra
```

---

## 2. 用户旅程图

```mermaid
journey
    title 用户使用流程
    section 发现
      看到广告: 3: 用户
      搜索产品: 4: 用户
    section 注册
      点击注册: 5: 用户
      填写信息: 3: 用户
      验证邮箱: 2: 用户
    section 首次使用
      引导教程: 4: 用户, 系统
      完成任务: 5: 用户
    section 留存
      次日回访: 3: 用户
      付费转化: 4: 用户
```

---

## 3. 业务流程图（带判断）

```mermaid
flowchart TD
    Start([用户触发]) --> A[系统接收请求]
    A --> B{用户已登录?}
    B -- 否 --> C[跳转登录页]
    C --> D[完成登录] --> B
    B -- 是 --> E{权限检查}
    E -- 无权限 --> F[返回403]
    E -- 有权限 --> G[处理业务逻辑]
    G --> H{处理成功?}
    H -- 是 --> I[返回结果]
    H -- 否 --> J[记录错误日志]
    J --> K[返回错误提示]
    I --> End([结束])
    K --> End
```

---

## 4. 系统交互时序图

```mermaid
sequenceDiagram
    participant U as 用户
    participant FE as 前端
    participant BE as 后端
    participant AI as AI服务
    participant DB as 数据库

    U->>FE: 输入请求
    FE->>BE: API调用
    BE->>DB: 查询用户数据
    DB-->>BE: 返回用户画像
    BE->>AI: 推理请求(+上下文)
    AI-->>BE: 返回结果
    BE-->>FE: 响应数据
    FE-->>U: 展示结果
    
    Note over BE,DB: 异步写入行为日志
```

---

## 5. 推荐系统策略流程图

```mermaid
flowchart LR
    Input[用户请求] --> Recall{召回层}
    Recall --> R1[协同过滤]
    Recall --> R2[内容召回]
    Recall --> R3[热门兜底]
    R1 & R2 & R3 --> Merge[合并去重]
    Merge --> Rank[粗排\n轻量模型]
    Rank --> Rerank[精排\n精准模型]
    Rerank --> Filter{业务过滤}
    Filter -- 安全/去重/打散 --> Result[返回结果]
```

---

## 6. 用户状态机

```mermaid
stateDiagram-v2
    [*] --> 新用户
    新用户 --> 活跃用户 : 完成首次核心操作
    活跃用户 --> 付费用户 : 订阅/购买
    活跃用户 --> 沉睡用户 : 7天未访问
    付费用户 --> 活跃用户 : 订阅到期
    沉睡用户 --> 活跃用户 : 召回成功
    沉睡用户 --> 流失用户 : 30天未访问
    流失用户 --> 活跃用户 : 重激活
    流失用户 --> [*] : 注销账号
```

---

## 7. 功能脑图

```mermaid
mindmap
  root((产品功能))
    用户管理
      注册/登录
      个人资料
      权限管理
    核心功能
      功能模块A
        子功能1
        子功能2
      功能模块B
    数据与分析
      数据看板
      报表导出
    设置
      通知设置
      账号安全
```

---

## 8. 产品时间线（Roadmap）

```mermaid
timeline
    title 产品路线图 2026
    Q1 : MVP上线
       : 核心功能验证
    Q2 : 用户规模化
       : AI能力增强
    Q3 : 商业化探索
       : 付费功能上线
    Q4 : 生态建设
       : 开放平台
```
