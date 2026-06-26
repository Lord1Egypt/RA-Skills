# Draw.io 图表输出规范

本文档定义将 Mermaid 图表转换为 Draw.io 格式的输出标准，仅在用户选择 Draw.io 输出时使用。

---

## MCP 工具调用方式

使用 `use_mcp_tool` 调用 Draw.io MCP，将生成的 XML 写入 `.drawio` 文件：

```
use_mcp_tool(
  server_name: "drawio",
  tool_name: "create_drawio_file",
  arguments: {
    "path": "<OUTPUT_DIR>/[名称]-[图表类型]-YYYYMMDD.drawio",
    "content": "<XML内容>"
  }
)
```

> MCP 不可用时的降级方案：将 XML 内容直接输出到 `.drawio` 文件，并告知用户「MCP 不可用，已直接生成 .drawio 文件，可用 Draw.io 桌面版或 app.diagrams.net 打开」。

---

## 文件命名规范

| 图表类型 | 文件名 |
|---------|-------|
| 业务流程图 | `[名称]-业务流程图-YYYYMMDD.drawio` |
| 功能架构图 | `[名称]-功能架构图-YYYYMMDD.drawio` |
| 状态机图 | `[名称]-状态机-YYYYMMDD.drawio` |
| 泳道图 | `[名称]-泳道图-YYYYMMDD.drawio` |
| 时序图 | `[名称]-时序图-YYYYMMDD.drawio` |

所有文件保存至 Phase 3 持久化的专属目录（路径从 `/tmp/pa_output_dir.txt` 读取）。

---

## 图表类型规范

---

### 1. 流程图（对应 Mermaid `flowchart TD/LR`）

**转换原则**：
- Mermaid 矩形节点 `[步骤]` → Draw.io `mxCell` 矩形
- Mermaid 菱形判断 `{判断}` → Draw.io `mxCell` 菱形（`rhombus` 样式）
- Mermaid 圆角开始/结束 `([开始])` → Draw.io 椭圆
- Mermaid 箭头 `-->` → Draw.io 实线连接
- Mermaid 虚线 `-.->` → Draw.io 虚线连接（`dashed=1`）

**标准 XML 模板**：

```xml
<mxfile>
  <diagram name="业务流程图">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="1169" pageHeight="827"
                  math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- 开始节点（椭圆） -->
        <mxCell id="2" value="开始" style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
                vertex="1" parent="1">
          <mxGeometry x="80" y="40" width="120" height="60" as="geometry"/>
        </mxCell>

        <!-- 普通步骤节点（矩形） -->
        <mxCell id="3" value="步骤名称" style="rounded=1;whiteSpace=wrap;html=1;"
                vertex="1" parent="1">
          <mxGeometry x="80" y="160" width="120" height="60" as="geometry"/>
        </mxCell>

        <!-- 判断节点（菱形） -->
        <mxCell id="4" value="判断条件?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
                vertex="1" parent="1">
          <mxGeometry x="60" y="290" width="160" height="80" as="geometry"/>
        </mxCell>

        <!-- 结束节点（椭圆） -->
        <mxCell id="5" value="结束" style="ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
                vertex="1" parent="1">
          <mxGeometry x="80" y="450" width="120" height="60" as="geometry"/>
        </mxCell>

        <!-- 连接线（实线） -->
        <mxCell id="6" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="2" target="3" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="7" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="3" target="4" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- 连接线（带标签） -->
        <mxCell id="8" value="是" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="4" target="5" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- 连接线（虚线，异常路径） -->
        <mxCell id="9" value="否" style="edgeStyle=orthogonalEdgeStyle;dashed=1;strokeColor=#FF0000;"
                edge="1" source="4" target="3" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

### 2. 状态机图（对应 Mermaid `stateDiagram-v2`）

**转换原则**：
- Mermaid 状态 `待支付` → Draw.io 圆角矩形
- Mermaid 初始状态 `[*]` → Draw.io 实心圆（`ellipse;fillColor=#000000`）
- Mermaid 终止状态 `[*]`（末尾） → Draw.io 双圆（`ellipse;shape=doubleEllipse`）
- Mermaid 转换 `A --> B: 事件` → Draw.io 带标签箭头

**标准 XML 模板**：

```xml
<mxfile>
  <diagram name="状态机">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- 初始状态（实心圆） -->
        <mxCell id="2" value="" style="ellipse;fillColor=#000000;strokeColor=#000000;"
                vertex="1" parent="1">
          <mxGeometry x="120" y="40" width="40" height="40" as="geometry"/>
        </mxCell>

        <!-- 状态节点（圆角矩形） -->
        <mxCell id="3" value="待支付" style="rounded=1;whiteSpace=wrap;html=1;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="80" y="140" width="120" height="50" as="geometry"/>
        </mxCell>

        <mxCell id="4" value="已支付" style="rounded=1;whiteSpace=wrap;html=1;arcSize=50;"
                vertex="1" parent="1">
          <mxGeometry x="80" y="250" width="120" height="50" as="geometry"/>
        </mxCell>

        <!-- 终止状态（双圆） -->
        <mxCell id="5" value="" style="ellipse;shape=doubleEllipse;fillColor=#000000;strokeColor=#000000;"
                vertex="1" parent="1">
          <mxGeometry x="120" y="370" width="40" height="40" as="geometry"/>
        </mxCell>

        <!-- 状态转换箭头（带事件标签） -->
        <mxCell id="6" value="" edge="1" source="2" target="3" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="7" value="支付成功" edge="1" source="3" target="4" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="8" value="确认完成" edge="1" source="4" target="5" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

### 3. 泳道图（对应 Mermaid 多角色 `subgraph`）

**转换原则**：
- Mermaid `subgraph 用户` → Draw.io 水平泳道（`swimlane` 样式）
- 每个角色为独立泳道
- 泳道内节点坐标相对于泳道容器计算
- 跨泳道连线使用普通箭头

**标准 XML 模板**：

```xml
<mxfile>
  <diagram name="泳道图">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- 泳道容器（水平排列） -->
        <mxCell id="2" value="业务流程" style="shape=pool;startSize=20;horizontal=1;"
                vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="800" height="450" as="geometry"/>
        </mxCell>

        <!-- 泳道1：用户 -->
        <mxCell id="3" value="用户" style="swimlane;startSize=30;horizontal=0;"
                vertex="1" parent="2">
          <mxGeometry x="0" y="20" width="800" height="140" as="geometry"/>
        </mxCell>

        <!-- 泳道2：系统 -->
        <mxCell id="4" value="系统" style="swimlane;startSize=30;horizontal=0;"
                vertex="1" parent="2">
          <mxGeometry x="0" y="160" width="800" height="140" as="geometry"/>
        </mxCell>

        <!-- 泳道3：物流 -->
        <mxCell id="5" value="物流" style="swimlane;startSize=30;horizontal=0;"
                vertex="1" parent="2">
          <mxGeometry x="0" y="300" width="800" height="140" as="geometry"/>
        </mxCell>

        <!-- 泳道1内的节点 -->
        <mxCell id="6" value="提交订单" style="rounded=1;whiteSpace=wrap;html=1;"
                vertex="1" parent="3">
          <mxGeometry x="60" y="50" width="120" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="7" value="确认收货" style="rounded=1;whiteSpace=wrap;html=1;"
                vertex="1" parent="3">
          <mxGeometry x="600" y="50" width="120" height="50" as="geometry"/>
        </mxCell>

        <!-- 泳道2内的节点 -->
        <mxCell id="8" value="验证订单" style="rounded=1;whiteSpace=wrap;html=1;"
                vertex="1" parent="4">
          <mxGeometry x="200" y="50" width="120" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="9" value="创建物流单" style="rounded=1;whiteSpace=wrap;html=1;"
                vertex="1" parent="4">
          <mxGeometry x="380" y="50" width="120" height="50" as="geometry"/>
        </mxCell>

        <!-- 泳道3内的节点 -->
        <mxCell id="10" value="配送" style="rounded=1;whiteSpace=wrap;html=1;"
                vertex="1" parent="5">
          <mxGeometry x="480" y="50" width="120" height="50" as="geometry"/>
        </mxCell>

        <!-- 跨泳道连线 -->
        <mxCell id="11" edge="1" source="6" target="8" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="12" edge="1" source="9" target="10" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="13" edge="1" source="10" target="7" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

### 4. 时序图（对应 Mermaid `sequenceDiagram`）

**转换原则**：
- Mermaid 参与者 `participant A` → Draw.io 生命线（`lifeline` 样式）
- Mermaid 消息 `A->>B: 操作` → Draw.io 水平实线箭头
- Mermaid 返回 `B-->>A: 返回` → Draw.io 虚线箭头
- Mermaid `activate/deactivate` → Draw.io 激活框（生命线上的矩形）

**标准 XML 模板**：

```xml
<mxfile>
  <diagram name="时序图">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- 参与者（顶部矩形框） -->
        <mxCell id="2" value="用户" style="shape=mxgraph.flowchart.actor;whiteSpace=wrap;html=1;"
                vertex="1" parent="1">
          <mxGeometry x="80" y="40" width="80" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="3" value="系统" style="rounded=1;whiteSpace=wrap;html=1;"
                vertex="1" parent="1">
          <mxGeometry x="320" y="40" width="80" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="4" value="数据库" style="shape=cylinder3;whiteSpace=wrap;html=1;"
                vertex="1" parent="1">
          <mxGeometry x="560" y="40" width="80" height="60" as="geometry"/>
        </mxCell>

        <!-- 生命线（虚线垂直线） -->
        <mxCell id="5" style="edgeStyle=none;dashed=1;endArrow=none;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points"/>
            <mxPoint x="120" y="120" as="sourcePoint"/>
            <mxPoint x="120" y="500" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="6" style="edgeStyle=none;dashed=1;endArrow=none;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="360" y="120" as="sourcePoint"/>
            <mxPoint x="360" y="500" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="7" style="edgeStyle=none;dashed=1;endArrow=none;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="600" y="120" as="sourcePoint"/>
            <mxPoint x="600" y="500" as="targetPoint"/>
          </mxGeometry>
        </mxCell>

        <!-- 消息（实线箭头，同步调用） -->
        <mxCell id="8" value="发起请求" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;"
                edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="120" y="160" as="sourcePoint"/>
            <mxPoint x="360" y="160" as="targetPoint"/>
          </mxGeometry>
        </mxCell>

        <!-- 消息（虚线箭头，返回） -->
        <mxCell id="9" value="返回结果" style="edgeStyle=orthogonalEdgeStyle;dashed=1;endArrow=open;"
                edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="360" y="280" as="sourcePoint"/>
            <mxPoint x="120" y="280" as="targetPoint"/>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 转换执行步骤

Claude 在执行 Draw.io 输出时，按以下步骤操作：

1. **识别当前文档中已生成的 Mermaid 图**（Step 2 流程图、Step 3 架构图，以及标准模式 Step 4 的状态机/泳道图）
2. **逐一对应图表类型**，选择本文档对应的 XML 模板
3. **将 Mermaid 节点和连线翻译为 XML 节点**：
   - 保持节点名称与 Mermaid 一致
   - 节点数量较多时，按从上至下/从左至右的顺序排列，每行间距 120px
4. **调用 MCP 工具**输出 `.drawio` 文件
5. **MCP 不可用时**：直接将 XML 写入 `.drawio` 文件并告知用户

---

## 质量检查

- [ ] 每个 Mermaid 图均有对应的 `.drawio` 文件输出
- [ ] 节点名称与 Mermaid 原图保持一致
- [ ] 连线方向、标签与原图一致
- [ ] 文件命名包含日期后缀
- [ ] 文件已保存至输出目录（`/tmp/pa_output_dir.txt` 所记录的路径）
