# 技术图表形状词汇表（Shape Vocabulary）

技术图表中的形状是**语义符号**——每种形状传达特定概念。本词汇表定义 14 种标准化形状模板，确保跨图表的语义一致性。

**所有 SVG 代码遵守 PPT 大师禁用特性黑名单**：无 `<style>`、无 `class`、无 `<symbol>+<use>`、无 `textPath`、无 `@font-face`、无 `<animate>`。使用 inline 属性（`fill="..."` `stroke="..."`）。

---

## 形状速查表

| # | 概念 | 形状名称 | 视觉特征 | 典型场景 |
|---|------|----------|----------|----------|
| 1 | User / Human | 人形头像 | 圆形头 + 弧形肩 | 用户输入、Actor |
| 2 | LLM / Model | 双边框圆角矩形 | 圆角矩形 + 内框 + ⚡ | AI 模型节点 |
| 3 | Agent / Orchestrator | 六边形 | 正六边形 | 主控调度器 |
| 4 | Memory (short-term) | 虚线圆角矩形 | 虚线边框 | 会话级/临时记忆 |
| 5 | Memory (long-term) | 圆柱体 | 上下椭圆 + 侧线 | 持久化存储 |
| 6 | Vector Store | 带内环圆柱体 | 圆柱体 + 网格线 | 向量数据库 |
| 7 | Graph DB | 三圆重叠 | 3 个交叠圆形 | 图数据库、知识图谱 |
| 8 | Tool / Function | 齿轮矩形 | 圆角矩形 + ⚙ 图标 | 工具调用、函数节点 |
| 9 | API / Gateway | 六边形（小型） | 单边框六边形 | API 入口、网关 |
| 10 | Queue / Stream | 水平管道 | 左右椭圆帽 + 管体 | 消息队列、数据流管道 |
| 11 | File / Document | 折角矩形 | 矩形 + 右上折角 | 文件、文档 |
| 12 | Browser / UI | 标题栏矩形 | 矩形 + 三色圆点标题栏 | 浏览器、Web 客户端 |
| 13 | Decision | 菱形 | 旋转 45° 的正方形 | 流程图中的判断节点 |
| 14 | Swim Lane Container | 虚线容器 | 大尺寸虚线矩形 + 标签 | 层级分组、泳道 |

---

## 详细模板

### 1. User / Human（用户/人形）

**概念**：终端用户、操作者、Actor 角色。

**使用场景**：架构图的输入层、用例图的 Actor、Agent 图的用户端。

```xml
<!-- 参数：cx=中心X, cy=中心Y -->
<!-- 推荐尺寸：宽 30px, 高 50px -->
<g id="user-node">
  <!-- 头部 -->
  <circle cx="{cx}" cy="{cy-18}" r="10"
          fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>
  <!-- 肩/身体 -->
  <path d="M {cx-14},{cy+16} Q {cx-14},{cy-4} {cx},{cy-4} Q {cx+14},{cy-4} {cx+14},{cy+16}"
        fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>
  <!-- 标签 -->
  <text x="{cx}" y="{cy+30}" text-anchor="middle"
        fill="{text-color}" font-size="12"
        font-family="Microsoft YaHei, Arial, sans-serif">User</text>
</g>
```

### 2. LLM / Model（大语言模型）

**概念**：AI 模型节点，信号"智能处理"。

**使用场景**：Agent 架构的核心推理节点、RAG Pipeline 中的生成节点。

```xml
<!-- 参数：x, y, w=宽度, h=高度 -->
<!-- 推荐尺寸：w=160, h=60 -->
<g id="llm-node">
  <!-- 外框 -->
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"
        fill="{fill}" stroke="{stroke-outer}" stroke-width="2.5"/>
  <!-- 内框（双边框效果） -->
  <rect x="{x+3}" y="{y+3}" width="{w-6}" height="{h-6}" rx="8"
        fill="none" stroke="{stroke-inner}" stroke-width="0.8"
        stroke-opacity="0.5"/>
  <!-- 闪电图标 -->
  <text x="{cx}" y="{cy-6}" text-anchor="middle" font-size="14">⚡</text>
  <!-- 模型名称 -->
  <text x="{cx}" y="{cy+10}" text-anchor="middle"
        fill="{text-color}" font-size="13" font-weight="600"
        font-family="Microsoft YaHei, Arial, sans-serif">GPT-4o</text>
</g>
```

### 3. Agent / Orchestrator（智能体/编排器）

**概念**：主控调度器，信号"主动控制"。

**使用场景**：Agent 架构中心、Multi-Agent 编排器、Planner 节点。

```xml
<!-- 参数：cx=中心X, cy=中心Y, r=外接圆半径 -->
<!-- 推荐尺寸：r=36（宽约 62px，高约 72px） -->
<g id="agent-node">
  <polygon points="{cx},{cy-r} {cx+r*0.866},{cy-r*0.5} {cx+r*0.866},{cy+r*0.5} {cx},{cy+r} {cx-r*0.866},{cy+r*0.5} {cx-r*0.866},{cy-r*0.5}"
           fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
  <text x="{cx}" y="{cy+5}" text-anchor="middle"
        fill="{text-color}" font-size="12" font-weight="600"
        font-family="Microsoft YaHei, Arial, sans-serif">Agent</text>
</g>
```

### 4. Memory — Short-term（短期记忆）

**概念**：会话级、临时性记忆，虚线边框信号"短暂"。

**使用场景**：Context Window、Working Memory、Session Cache。

```xml
<!-- 参数：x, y, w=宽度, h=高度 -->
<!-- 推荐尺寸：w=140, h=60 -->
<g id="memory-short">
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
        fill="{fill}" stroke="{stroke}" stroke-width="1.5"
        stroke-dasharray="6,3"/>
  <text x="{cx}" y="{cy-6}" text-anchor="middle"
        fill="{text-color}" font-size="10" fill-opacity="0.7"
        font-family="Microsoft YaHei, Arial, sans-serif">MEMORY</text>
  <text x="{cx}" y="{cy+8}" text-anchor="middle"
        fill="{text-color}" font-size="13"
        font-family="Microsoft YaHei, Arial, sans-serif">Short-term</text>
</g>
```

### 5. Memory — Long-term（长期记忆/数据库圆柱体）

**概念**：持久化存储，实线圆柱体信号"永久保存"。

**使用场景**：数据库、Long-term Memory、Knowledge Store。

```xml
<!-- 参数：cx=中心X, top=顶部Y, w=宽度, h=高度 -->
<!-- 推荐尺寸：w=80, h=70 -->
<g id="memory-long">
  <!-- 顶部椭圆 -->
  <ellipse cx="{cx}" cy="{top}" rx="{w/2}" ry="{w/6}"
           fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
  <!-- 柱体 -->
  <rect x="{cx-w/2}" y="{top}" width="{w}" height="{h}"
        fill="{fill}" stroke="none"/>
  <!-- 左侧线 -->
  <line x1="{cx-w/2}" y1="{top}" x2="{cx-w/2}" y2="{top+h}"
        stroke="{stroke}" stroke-width="1.5"/>
  <!-- 右侧线 -->
  <line x1="{cx+w/2}" y1="{top}" x2="{cx+w/2}" y2="{top+h}"
        stroke="{stroke}" stroke-width="1.5"/>
  <!-- 底部椭圆 -->
  <ellipse cx="{cx}" cy="{top+h}" rx="{w/2}" ry="{w/6}"
           fill="{fill-dark}" stroke="{stroke}" stroke-width="1.5"/>
  <!-- 标签 -->
  <text x="{cx}" y="{top+h/2+5}" text-anchor="middle"
        fill="{text-color}" font-size="12"
        font-family="Microsoft YaHei, Arial, sans-serif">Database</text>
</g>
```

### 6. Vector Store（向量数据库）

**概念**：向量存储，圆柱体加内环信号"结构化向量"。

**使用场景**：Embedding 存储、RAG 检索层、Similarity Search。

```xml
<!-- 参数：cx=中心X, top=顶部Y, w=宽度, h=高度 -->
<!-- 推荐尺寸：w=80, h=70 -->
<g id="vector-store">
  <!-- 顶部椭圆 -->
  <ellipse cx="{cx}" cy="{top}" rx="{w/2}" ry="{w/6}"
           fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
  <!-- 柱体 -->
  <rect x="{cx-w/2}" y="{top}" width="{w}" height="{h}"
        fill="{fill}" stroke="none"/>
  <line x1="{cx-w/2}" y1="{top}" x2="{cx-w/2}" y2="{top+h}"
        stroke="{stroke}" stroke-width="1.5"/>
  <line x1="{cx+w/2}" y1="{top}" x2="{cx+w/2}" y2="{top+h}"
        stroke="{stroke}" stroke-width="1.5"/>
  <!-- 内环（向量网格线） -->
  <ellipse cx="{cx}" cy="{top+h*0.33}" rx="{w/2}" ry="{w/6}"
           fill="none" stroke="{stroke}" stroke-width="0.7"
           stroke-opacity="0.5"/>
  <ellipse cx="{cx}" cy="{top+h*0.66}" rx="{w/2}" ry="{w/6}"
           fill="none" stroke="{stroke}" stroke-width="0.7"
           stroke-opacity="0.5"/>
  <!-- 底部椭圆 -->
  <ellipse cx="{cx}" cy="{top+h}" rx="{w/2}" ry="{w/6}"
           fill="{fill-dark}" stroke="{stroke}" stroke-width="1.5"/>
  <!-- 标签 -->
  <text x="{cx}" y="{top+h/2+5}" text-anchor="middle"
        fill="{text-color}" font-size="11" font-weight="700"
        font-family="Microsoft YaHei, Arial, sans-serif">Pinecone</text>
</g>
```

### 7. Graph DB（图数据库）

**概念**：图结构存储，三圆重叠信号"关系网络"。

**使用场景**：知识图谱、Neo4j、Graph Store。

```xml
<!-- 参数：cx=中心X, cy=中心Y -->
<!-- 推荐尺寸：整体约 60×50px -->
<g id="graph-db">
  <circle cx="{cx-12}" cy="{cy-8}" r="16"
          fill="{fill}" stroke="{stroke}" stroke-width="1.2"
          fill-opacity="0.7"/>
  <circle cx="{cx+12}" cy="{cy-8}" r="16"
          fill="{fill}" stroke="{stroke}" stroke-width="1.2"
          fill-opacity="0.7"/>
  <circle cx="{cx}" cy="{cy+8}" r="16"
          fill="{fill}" stroke="{stroke}" stroke-width="1.2"
          fill-opacity="0.7"/>
  <text x="{cx}" y="{cy+32}" text-anchor="middle"
        fill="{text-color}" font-size="11"
        font-family="Microsoft YaHei, Arial, sans-serif">Graph DB</text>
</g>
```

### 8. Tool / Function（工具/函数调用）

**概念**：可执行的工具或函数节点。

**使用场景**：Tool Call、Function Node、Search Tool、Code Execution。

```xml
<!-- 参数：x, y, w=宽度, h=高度 -->
<!-- 推荐尺寸：w=120, h=50 -->
<g id="tool-node">
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"
        fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
  <!-- 齿轮图标 -->
  <text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="16">⚙</text>
  <!-- 工具名 -->
  <text x="{cx}" y="{cy+12}" text-anchor="middle"
        fill="{text-color}" font-size="12"
        font-family="Microsoft YaHei, Arial, sans-serif">Tool Name</text>
</g>
```

### 9. API / Gateway（API 网关）

**概念**：系统入口、API 端点，六边形信号"接口节点"。

**使用场景**：API Gateway、Load Balancer、Service Entry。

```xml
<!-- 参数：cx=中心X, cy=中心Y -->
<!-- 推荐尺寸：约 48×56px -->
<g id="api-gateway">
  <polygon points="{cx},{cy-28} {cx+24},{cy-14} {cx+24},{cy+14} {cx},{cy+28} {cx-24},{cy+14} {cx-24},{cy-14}"
           fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
  <text x="{cx}" y="{cy+5}" text-anchor="middle"
        fill="{text-color}" font-size="11"
        font-family="Microsoft YaHei, Arial, sans-serif">API</text>
</g>
```

### 10. Queue / Stream（消息队列/数据流管道）

**概念**：异步消息管道，水平管道形信号"流动中的数据"。

**使用场景**：Kafka、RabbitMQ、Event Stream、Message Buffer。

```xml
<!-- 参数：x1=左端X, x2=右端X, cy=中心Y, ry=半径 -->
<!-- 推荐尺寸：长 120px, ry=18 -->
<g id="queue-node">
  <!-- 左端帽 -->
  <ellipse cx="{x1}" cy="{cy}" rx="{ry*0.6}" ry="{ry}"
           fill="{fill-dark}" stroke="{stroke}" stroke-width="1.5"/>
  <!-- 管体 -->
  <rect x="{x1}" y="{cy-ry}" width="{x2-x1}" height="{ry*2}"
        fill="{fill}" stroke="none"/>
  <line x1="{x1}" y1="{cy-ry}" x2="{x2}" y2="{cy-ry}"
        stroke="{stroke}" stroke-width="1.5"/>
  <line x1="{x1}" y1="{cy+ry}" x2="{x2}" y2="{cy+ry}"
        stroke="{stroke}" stroke-width="1.5"/>
  <!-- 右端帽 -->
  <ellipse cx="{x2}" cy="{cy}" rx="{ry*0.6}" ry="{ry}"
           fill="{fill-light}" stroke="{stroke}" stroke-width="1.5"/>
  <!-- 标签 -->
  <text x="{(x1+x2)/2}" y="{cy+4}" text-anchor="middle"
        fill="{text-color}" font-size="11"
        font-family="Microsoft YaHei, Arial, sans-serif">Queue</text>
</g>
```

### 11. File / Document（文件/文档）

**概念**：数据文件、文档资源，折角矩形信号"文件"。

**使用场景**：配置文件、输出文档、数据 Artifact。

```xml
<!-- 参数：x, y, w=宽度, h=高度 -->
<!-- 推荐尺寸：w=80, h=90 -->
<g id="file-node">
  <!-- 折角矩形 -->
  <path d="M {x},{y} L {x+w-12},{y} L {x+w},{y+12} L {x+w},{y+h} L {x},{y+h} Z"
        fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
  <!-- 折角 -->
  <path d="M {x+w-12},{y} L {x+w-12},{y+12} L {x+w},{y+12}"
        fill="{fill-dark}" stroke="{stroke}" stroke-width="1"/>
  <!-- 内部线条 -->
  <line x1="{x+8}" y1="{y+h*0.45}" x2="{x+w-8}" y2="{y+h*0.45}"
        stroke="{stroke}" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="{x+8}" y1="{y+h*0.60}" x2="{x+w-8}" y2="{y+h*0.60}"
        stroke="{stroke}" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="{x+8}" y1="{y+h*0.75}" x2="{x+w-16}" y2="{y+h*0.75}"
        stroke="{stroke}" stroke-width="1" stroke-opacity="0.5"/>
</g>
```

### 12. Browser / UI（浏览器/Web 界面）

**概念**：Web 客户端、前端 UI，标题栏信号"浏览器窗口"。

**使用场景**：前端入口、Web Client、Dashboard。

```xml
<!-- 参数：x, y, w=宽度, h=高度 -->
<!-- 推荐尺寸：w=120, h=80 -->
<g id="browser-node">
  <!-- 主框 -->
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"
        fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
  <!-- 标题栏 -->
  <rect x="{x}" y="{y}" width="{w}" height="20" rx="6"
        fill="{fill-dark}" stroke="none"/>
  <rect x="{x}" y="{y+14}" width="{w}" height="6"
        fill="{fill-dark}" stroke="none"/>
  <!-- 红绿灯圆点 -->
  <circle cx="{x+12}" cy="{y+10}" r="4" fill="#ef4444" fill-opacity="0.8"/>
  <circle cx="{x+24}" cy="{y+10}" r="4" fill="#f59e0b" fill-opacity="0.8"/>
  <circle cx="{x+36}" cy="{y+10}" r="4" fill="#10b981" fill-opacity="0.8"/>
</g>
```

### 13. Decision（判断/菱形）

**概念**：条件分支，菱形信号"决策点"。

**使用场景**：流程图中的 if/else、条件路由。

```xml
<!-- 参数：cx=中心X, cy=中心Y, hw=半宽, hh=半高 -->
<!-- 推荐尺寸：hw=50, hh=35 -->
<g id="decision-node">
  <polygon points="{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}"
           fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>
  <text x="{cx}" y="{cy+5}" text-anchor="middle"
        fill="{text-color}" font-size="12"
        font-family="Microsoft YaHei, Arial, sans-serif">Condition?</text>
</g>
```

### 14. Swim Lane Container（泳道/分层容器）

**概念**：逻辑分组、层级容器，虚线边框信号"分区"。

**使用场景**：Architecture 图的分层、Agent 图的能力层、网络拓扑的 Zone。

```xml
<!-- 参数：x, y, w=宽度, h=高度 -->
<!-- 推荐尺寸：按实际内容调整，典型 w=400+, h=150+ -->
<g id="swim-lane">
  <!-- 容器背景 -->
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"
        fill="{fill}" fill-opacity="0.04"
        stroke="{stroke}" stroke-width="1"
        stroke-dasharray="6,4"/>
  <!-- 层级标签（左上角） -->
  <text x="{x+12}" y="{y+16}"
        fill="{label-color}" font-size="10" font-weight="600"
        letter-spacing="0.06em"
        font-family="Microsoft YaHei, Arial, sans-serif">LAYER NAME</text>
</g>
```

---

## 配色建议

形状的具体颜色取决于所选设计哲学。以下是通用推荐：

| 组件类型 | 推荐填充 | 推荐描边 | 文字色 |
|----------|----------|----------|--------|
| Agent/LLM（核心） | `#eff6ff` | `#3b82f6` | `#1e293b` |
| Memory（短期） | `#fefce8` | `#eab308` | `#1e293b` |
| Memory（长期）/DB | `#f0fdf4` | `#22c55e` | `#1e293b` |
| Tool/Function | `#faf5ff` | `#8b5cf6` | `#1e293b` |
| User/Browser | `#f8fafc` | `#94a3b8` | `#1e293b` |
| Queue/Stream | `#fff7ed` | `#f97316` | `#1e293b` |
| Container/Lane | `#f8fafc` | `#cbd5e1` | `#64748b` |
