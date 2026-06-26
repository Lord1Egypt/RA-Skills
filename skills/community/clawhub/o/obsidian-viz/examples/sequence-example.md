# 时序图示例 - 用户下单流程

## 示例说明

本示例展示如何使用 obsidian-viz skill 创建时序图，说明系统组件之间的交互顺序。

## 使用方法

在 OpenClaw 中发送以下文字：

> 创建一个用户下单的时序图，包含：
> 1. 用户选择商品并加入购物车
> 2. 用户点击结算
> 3. 系统查询购物车商品信息
> 4. 调用库存服务检查库存
> 5. 创建订单
> 6. 调用支付服务发起支付
> 7. 用户完成支付
> 8. 支付回调更新订单状态
> 9. 通知仓储系统发货

## 生成的 Mermaid 代码

```mermaid
sequenceDiagram
    participant User as 用户
    participant Cart as 购物车服务
    participant Stock as 库存服务
    participant Order as 订单服务
    participant Pay as 支付服务
    participant Warehouse as 仓储服务

    User->>Cart: 选择商品加入购物车
    User->>Cart: 点击结算
    Cart->>Stock: 查询商品库存
    Stock-->>Cart: 返回库存信息
    Cart->>Order: 创建订单
    Order->>Pay: 发起支付
    Pay->>User: 跳转支付页面
    User->>Pay: 完成支付
    Pay-->>Order: 支付回调
    Order->>Order: 更新订单状态
    Order->>Warehouse: 通知发货
    Warehouse-->>User: 发货通知
```

## 详细时序图（带更多细节）

```mermaid
sequenceDiagram
    participant User as 用户
    participant Frontend as 前端应用
    participant API as API 网关
    participant Order as 订单服务
    participant Stock as 库存服务
    participant Pay as 支付服务
    participant DB as 数据库

    Note over User,Pay: 1. 用户下单流程
    User->>Frontend: 选择商品
    Frontend->>API: 添加到购物车
    API->>Order: 请求处理
    Order->>DB: 写入购物车数据
    DB-->>Order: 保存成功
    Order-->>Frontend: 返回成功
    Frontend-->>User: 显示购物车

    User->>Frontend: 点击结算
    Frontend->>API: 发起结算请求
    API->>Stock: 验证库存
    alt 库存充足
        Stock-->>API: 库存充足
    else 库存不足
        Stock-->>API: 库存不足
        API-->>Frontend: 返回错误
        Frontend-->>User: 提示库存不足
    end

    API->>Order: 创建订单
    Order->>DB: 写入订单数据
    DB-->>Order: 订单创建成功
    Order-->>API: 返回订单信息
    API-->>Frontend: 返回订单号
    Frontend-->>User: 显示订单金额

    Note over User,Pay: 2. 支付流程
    User->>Frontend: 点击支付
    Frontend->>API: 发起支付
    API->>Pay: 调用支付接口
    Pay-->>Frontend: 返回支付页面
    User->>Pay: 完成支付
    Pay->>Order: 支付回调
    Order->>DB: 更新订单状态
    DB-->>Order: 更新成功
    Order-->>API: 返回更新结果
    API-->>Frontend: 通知支付成功
    Frontend-->>User: 显示支付成功
```

## 适用场景

- API 调用流程说明
- 系统交互分析
- 技术方案文档
- Bug 复现步骤
- 接口设计沟通

## 工具选择建议

| 场景 | 推荐工具 |
|------|---------|
| 简单时序图 | Mermaid |
| 复杂交互流程 | Mermaid |
| 带分支逻辑 | Mermaid (alt/else) |
| 并发流程 | Mermaid (par) |
