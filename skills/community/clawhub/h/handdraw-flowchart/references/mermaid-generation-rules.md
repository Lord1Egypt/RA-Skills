# Mermaid Generation Rules

## Global Rules

- Output one complete Mermaid diagram, not multiple diagrams.
- Use only `flowchart`, `sequenceDiagram`, or `classDiagram`.
- Put the diagram declaration on the first non-comment line.
- Do not use Markdown code fences in `.mmd` files.
- Do not use YAML frontmatter, custom CSS, external images, or HTML-heavy labels.
- Use concise labels. Split overloaded process steps into separate nodes/messages/classes.
- Prefer ASCII IDs such as `Start`, `CheckStock`, `PayCallback`; put Chinese text inside labels.

## Flowchart

Use flowcharts for process orchestration, decision paths, retries, compensation, and fallback flows.

Preferred starts:

```mermaid
flowchart TD
```

```mermaid
flowchart LR
```

Allowed core syntax:

```mermaid
flowchart TD
  Start([开始]) --> Validate[参数校验]
  Validate --> HasStock{库存充足?}
  HasStock -->|是| CreateOrder[创建订单]
  HasStock -->|否| Reject[返回库存不足]
```

Guidelines:

- Use rectangles for actions, diamonds for decisions, and rounded nodes for start/end.
- Use `subgraph` only when it improves readability.
- Avoid Mermaid's experimental `@{ shape: ... }` syntax because Excalidraw conversion support can lag Mermaid syntax support.
- Keep edges directional and labeled only when the branch condition is meaningful.

## Sequence Diagram

Use sequence diagrams for actor-to-system calls, callbacks, async notifications, and retry flows.

Allowed core syntax:

```mermaid
sequenceDiagram
  autonumber
  participant User as 用户
  participant App as 下单服务
  participant MQ as RocketMQ
  User->>App: 提交订单
  App-->>MQ: 发送扣库存消息
  MQ-->>App: 投递结果
```

Guidelines:

- Declare participants explicitly.
- Use `->>` for synchronous requests and `-->>` for async or return messages.
- Use `alt` / `else` / `end` for branches and `loop` / `end` for retries.
- Keep message text short; long descriptions belong outside the diagram.

## Class Diagram

Use class diagrams for domain model sketches, DTO/DO/VO separation, aggregate relationships, and interface contracts.

Allowed core syntax:

```mermaid
classDiagram
  class Order {
    +String orderNo
    +Integer status
    +pay()
  }
  class OrderItem {
    +String skuId
    +Integer quantity
  }
  Order "1" --> "*" OrderItem
```

Guidelines:

- Keep class names ASCII and put Chinese meaning in comments outside the diagram if needed.
- Prefer `+`, `-`, `#` visibility markers only when they add value.
- Avoid deeply nested generics and long method signatures.
- Use simple relationships: `<|--`, `*--`, `o--`, `-->`, `..>`.
