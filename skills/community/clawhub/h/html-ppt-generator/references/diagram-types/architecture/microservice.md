# microservice · 微服务拓扑图

**适用：** 微服务架构、服务依赖关系、API 调用链、系统组件连接图
**高度：** 240px

**结构公式：** 圆形/方形服务节点 + 有向连线（实线=同步调用，虚线=异步消息）。

```html
<svg viewBox="0 0 700 240" style="width:100%;height:240px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ms-arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#475569"/>
    </marker>
    <marker id="ms-arr-async" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#8b5cf6"/>
    </marker>
  </defs>

  <!-- 客户端层 -->
  <rect x="10" y="100" width="90" height="40" rx="20" fill="rgba(59,130,246,0.15)" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="55" y="124" text-anchor="middle" font-size="9" fill="#93c5fd" font-weight="700">Client</text>

  <!-- API Gateway -->
  <rect x="150" y="88" width="100" height="64" rx="6" fill="rgba(245,158,11,0.12)" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="200" y="118" text-anchor="middle" font-size="10" fill="#fcd34d" font-weight="700">API</text>
  <text x="200" y="132" text-anchor="middle" font-size="10" fill="#fcd34d" font-weight="700">Gateway</text>

  <!-- 服务层 -->
  <rect x="320" y="20"  width="100" height="44" rx="6" fill="rgba(139,92,246,0.12)" stroke="#8b5cf6" stroke-width="1.5"/>
  <text x="370" y="46" text-anchor="middle" font-size="9.5" fill="#c4b5fd" font-weight="700">User Service</text>

  <rect x="320" y="98"  width="100" height="44" rx="6" fill="rgba(139,92,246,0.12)" stroke="#8b5cf6" stroke-width="1.5"/>
  <text x="370" y="124" text-anchor="middle" font-size="9.5" fill="#c4b5fd" font-weight="700">Order Service</text>

  <rect x="320" y="176" width="100" height="44" rx="6" fill="rgba(139,92,246,0.12)" stroke="#8b5cf6" stroke-width="1.5"/>
  <text x="370" y="202" text-anchor="middle" font-size="9.5" fill="#c4b5fd" font-weight="700">Pay Service</text>

  <!-- 消息队列 -->
  <rect x="480" y="98" width="90" height="44" rx="6" fill="rgba(245,158,11,0.1)" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="525" y="118" text-anchor="middle" font-size="9" fill="#fcd34d">Message</text>
  <text x="525" y="131" text-anchor="middle" font-size="9" fill="#fcd34d">Queue</text>

  <!-- 数据层 -->
  <rect x="610" y="20"  width="80" height="40" rx="6" fill="rgba(6,182,212,0.12)" stroke="#06b6d4" stroke-width="1.5"/>
  <text x="650" y="44" text-anchor="middle" font-size="9" fill="#67e8f9">User DB</text>

  <rect x="610" y="98"  width="80" height="40" rx="6" fill="rgba(6,182,212,0.12)" stroke="#06b6d4" stroke-width="1.5"/>
  <text x="650" y="122" text-anchor="middle" font-size="9" fill="#67e8f9">Order DB</text>

  <rect x="610" y="176" width="80" height="40" rx="6" fill="rgba(6,182,212,0.12)" stroke="#06b6d4" stroke-width="1.5"/>
  <text x="650" y="200" text-anchor="middle" font-size="9" fill="#67e8f9">Pay DB</text>

  <!-- 同步连线（实线） -->
  <line x1="100" y1="120" x2="150" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#ms-arr)"/>
  <line x1="250" y1="104" x2="320" y2="52"  stroke="#475569" stroke-width="1.5" marker-end="url(#ms-arr)"/>
  <line x1="250" y1="120" x2="320" y2="120" stroke="#475569" stroke-width="1.5" marker-end="url(#ms-arr)"/>
  <line x1="250" y1="136" x2="320" y2="188" stroke="#475569" stroke-width="1.5" marker-end="url(#ms-arr)"/>
  <line x1="420" y1="42"  x2="610" y2="40"  stroke="#475569" stroke-width="1.5" marker-end="url(#ms-arr)"/>
  <line x1="420" y1="118" x2="610" y2="118" stroke="#475569" stroke-width="1.5" marker-end="url(#ms-arr)"/>
  <line x1="420" y1="196" x2="610" y2="196" stroke="#475569" stroke-width="1.5" marker-end="url(#ms-arr)"/>

  <!-- 异步连线（虚线，紫色） -->
  <line x1="420" y1="126" x2="480" y2="120" stroke="#8b5cf6" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#ms-arr-async)"/>
  <line x1="420" y1="200" x2="480" y2="130" stroke="#8b5cf6" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#ms-arr-async)"/>

  <!-- 图例 -->
  <line x1="10" y1="228" x2="40" y2="228" stroke="#475569" stroke-width="1.5" marker-end="url(#ms-arr)"/>
  <text x="45" y="231" font-size="8" fill="#64748b">同步调用</text>
  <line x1="120" y1="228" x2="150" y2="228" stroke="#8b5cf6" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#ms-arr-async)"/>
  <text x="155" y="231" font-size="8" fill="#64748b">异步消息</text>
</svg>
```

**参数说明：**
- 圆角矩形服务节点：rx=6（服务），rx=20（客户端，椭圆感）
- 同步调用：实线 + 灰色箭头；异步消息：虚线 + 紫色箭头
- 节点色系：客户端=蓝，网关=橙，服务=紫，队列=橙虚线，数据库=青
- 水平分层：Client → Gateway → Services → Queue/DB
