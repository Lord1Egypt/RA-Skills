# 箭头语义编码规范（Arrow Semantics）

技术图表中的箭头不仅是连线，更是**语义编码**。本规范定义 7 种标准化语义箭头，确保同类含义在所有图表中保持一致的视觉表达。

---

## 铁律

> 当图表中使用 **2 种及以上**不同语义的箭头时，**必须**在画布右下角添加图例（Legend）面板，列出所有使用的箭头类型及其含义。

---

## 7 种语义箭头定义

### 标准色版

| # | 语义 | 颜色 | 粗细 | 虚线模式 | 含义 |
|---|------|------|------|----------|------|
| 1 | **Primary data flow** | `#2563eb`（蓝） | 2px | 无（实线） | 主请求/响应路径，核心数据流 |
| 2 | **Control / trigger** | `#ea580c`（橙） | 1.5px | 无（实线） | 系统触发另一个系统，控制信号 |
| 3 | **Memory read** | `#059669`（绿） | 1.5px | 无（实线） | 从存储中检索/读取数据 |
| 4 | **Memory write** | `#059669`（绿） | 1.5px | `5,3` | 向存储写入/持久化数据 |
| 5 | **Async / event** | `#6b7280`（灰） | 1.5px | `4,2` | 非阻塞、事件驱动的异步通信 |
| 6 | **Embedding / transform** | `#7c3aed`（紫） | 1px | 无（实线） | 数据转换、向量化、格式变换 |
| 7 | **Feedback / loop** | `#7c3aed`（紫） | 1.5px | 无（实线） | 迭代推理循环、反馈回路（使用曲线路径） |


---

## SVG 代码模板

### Marker 定义（放在 `<defs>` 内）

所有 marker 严格遵守 `shared-standards.md` §1.1 的三项条件：
- `orient="auto"`
- 3 顶点三角形（`<polygon>` 或闭合 `<path>`）
- `fill` 匹配父线条的 `stroke` 颜色

```xml
<defs>
  <!-- 1. Primary data flow — 蓝色 -->
  <marker id="arrow-primary" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#2563eb"/>
  </marker>

  <!-- 2. Control / trigger — 橙色 -->
  <marker id="arrow-control" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#ea580c"/>
  </marker>

  <!-- 3. Memory read — 绿色实心 -->
  <marker id="arrow-mem-read" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#059669"/>
  </marker>

  <!-- 4. Memory write — 绿色（配合虚线使用） -->
  <marker id="arrow-mem-write" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#059669"/>
  </marker>

  <!-- 5. Async / event — 灰色（配合虚线使用） -->
  <marker id="arrow-async" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#6b7280"/>
  </marker>

  <!-- 6. Embedding / transform — 紫色细线 -->
  <marker id="arrow-embed" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#7c3aed"/>
  </marker>

  <!-- 7. Feedback / loop — 紫色（配合曲线路径） -->
  <marker id="arrow-feedback" markerWidth="10" markerHeight="7"
          refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#7c3aed"/>
  </marker>
</defs>
```


### 箭头使用示例

```xml
<!-- 1. Primary data flow — 实线蓝色 -->
<line x1="100" y1="200" x2="400" y2="200"
      stroke="#2563eb" stroke-width="2"
      marker-end="url(#arrow-primary)"/>

<!-- 2. Control / trigger — 实线橙色 -->
<line x1="100" y1="250" x2="400" y2="250"
      stroke="#ea580c" stroke-width="1.5"
      marker-end="url(#arrow-control)"/>

<!-- 3. Memory read — 实线绿色 -->
<line x1="100" y1="300" x2="400" y2="300"
      stroke="#059669" stroke-width="1.5"
      marker-end="url(#arrow-mem-read)"/>

<!-- 4. Memory write — 虚线绿色 -->
<line x1="100" y1="350" x2="400" y2="350"
      stroke="#059669" stroke-width="1.5" stroke-dasharray="5,3"
      marker-end="url(#arrow-mem-write)"/>

<!-- 5. Async / event — 虚线灰色 -->
<line x1="100" y1="400" x2="400" y2="400"
      stroke="#6b7280" stroke-width="1.5" stroke-dasharray="4,2"
      marker-end="url(#arrow-async)"/>

<!-- 6. Embedding / transform — 细实线紫色 -->
<line x1="100" y1="450" x2="400" y2="450"
      stroke="#7c3aed" stroke-width="1"
      marker-end="url(#arrow-embed)"/>

<!-- 7. Feedback / loop — 曲线紫色 -->
<path d="M 400,200 C 450,100 500,100 400,200"
      fill="none" stroke="#7c3aed" stroke-width="1.5"
      marker-end="url(#arrow-feedback)"/>
```

---

## 图例模板（Legend）

当使用 2+ 种箭头时，在画布右下角放置图例面板：

```xml
<!-- Legend 面板 — 定位于右下角 -->
<g id="legend" transform="translate(980, 580)">
  <!-- 背景 -->
  <rect x="0" y="0" width="260" height="120" rx="8"
        fill="#ffffff" stroke="#e5e7eb" stroke-width="1"/>
  <text x="12" y="22" font-size="11" font-weight="700" fill="#374151"
        font-family="Microsoft YaHei, Arial, sans-serif">LEGEND</text>

  <!-- 行 1: Primary data flow -->
  <line x1="12" y1="42" x2="52" y2="42"
        stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-primary)"/>
  <text x="62" y="46" font-size="10" fill="#374151"
        font-family="Microsoft YaHei, Arial, sans-serif">Primary data flow</text>

  <!-- 行 2: Control / trigger -->
  <line x1="12" y1="62" x2="52" y2="62"
        stroke="#ea580c" stroke-width="1.5" marker-end="url(#arrow-control)"/>
  <text x="62" y="66" font-size="10" fill="#374151"
        font-family="Microsoft YaHei, Arial, sans-serif">Control / trigger</text>

  <!-- 行 3: Memory read -->
  <line x1="12" y1="82" x2="52" y2="82"
        stroke="#059669" stroke-width="1.5" marker-end="url(#arrow-mem-read)"/>
  <text x="62" y="86" font-size="10" fill="#374151"
        font-family="Microsoft YaHei, Arial, sans-serif">Memory read</text>

  <!-- 行 4: Memory write -->
  <line x1="12" y1="102" x2="52" y2="102"
        stroke="#059669" stroke-width="1.5" stroke-dasharray="5,3"
        marker-end="url(#arrow-mem-write)"/>
  <text x="62" y="106" font-size="10" fill="#374151"
        font-family="Microsoft YaHei, Arial, sans-serif">Memory write</text>
</g>
```

> 图例高度按实际使用的箭头类型数动态调整：每行 20px，顶部标题 30px，底部留白 10px。
> 计算公式：`height = 30 + N × 20 + 10`（N = 使用的箭头类型数）。

---

## 使用规则

1. **语义优先**：先确定箭头的含义（数据流？控制信号？内存操作？），再选择对应的颜色和线型
2. **不要混用同色不同义**：同一图表中，蓝色箭头必须始终代表 Primary data flow
3. **Memory read vs write 必须区分**：同为绿色但 read 是实线、write 是虚线——这是关键视觉差异
4. **Feedback loop 用曲线**：反馈/循环箭头使用 cubic bezier 曲线路径（`C` 或 `Q` 命令），不用直线
5. **图例不可省略**：使用 2+ 种箭头时，图例是强制性的——不是装饰
6. **标签必须有背景**：箭头上的文字标签必须有 `<rect>` 背景，参见 `svg-layout-best-practices.md`
