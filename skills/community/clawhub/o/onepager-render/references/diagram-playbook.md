# 图示手册

## 1. 先判断关系类型

| 关系 | 用什么 | 例子 |
|---|---|---|
| 先后步骤、请求链路 | 横向或纵向流程图 | 一次 SQL 查询经过哪些层 |
| 多角色交互、消息顺序 | 时序图 | 客户端、网关、服务、数据库 |
| 分支判断 | 流程图（菱形） | 命中索引 / 回表 |
| 状态迁移 | 状态图 | 连接池：空闲 → 使用 → 归还 |
| 层级、分类 | 树或思维导图 | 索引类型分类 |
| 多对象同维度对比 | **表格优先** | B 树 / B+ 树 / 哈希 |
| 数量随时间变化 | 折线或柱状 | QPS、延迟 |
| 两个维度定位 | 四象限 | 一致性 vs 可用性 |

如果一张图删掉后信息没有损失，就不要画，改成表格或一句话。

## 2. 画图前三个问题

1. 读者要在图上回答什么问题？（例如"为什么树矮"）
2. 最少需要几个节点才能回答？超过 8 个就拆图或改表。
3. 黑白打印后，是否还能靠文字、箭头、线型区分？

## 3. SVG 约定

- 内联 `<svg>`，带 `viewBox`，`width="100%"`，`height="auto"`，`max-height` 由 CSS 控制。
- 文字用系统字体栈，`font-size` 在 13–14（viewBox 680 宽时约等于 9.5–10.5pt）。
- 线宽 1.5–2；箭头用 `<marker>`；不要阴影、渐变、圆角过大。
- 一个强调色 + 两级灰。颜色不承载分类。
- 每个图形加 `<title>` 和 `aria-label`，方便屏幕阅读器。
- 节点文字不超过两行；超了就用编号，在图下列注释。

## 4. 三个可直接改的骨架

### 4.1 纵向流程

```html
<svg viewBox="0 0 680 220" role="img" aria-label="流程示意">
  <title>流程示意</title>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#1a1a1a"/>
    </marker>
  </defs>
  <g font-family="'Source Han Sans SC','Microsoft YaHei',sans-serif" font-size="13" fill="#1a1a1a">
    <rect x="40" y="20" width="180" height="46" fill="#fff" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="130" y="48" text-anchor="middle">步骤一</text>
    <line x1="130" y1="66" x2="130" y2="94" stroke="#1a1a1a" stroke-width="1.6" marker-end="url(#arrow)"/>
    <rect x="40" y="96" width="180" height="46" fill="#fff" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="130" y="124" text-anchor="middle">步骤二</text>
    <line x1="220" y1="119" x2="300" y2="119" stroke="#1a1a1a" stroke-width="1.6" marker-end="url(#arrow)"/>
    <rect x="302" y="96" width="180" height="46" fill="#fff" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="392" y="124" text-anchor="middle">步骤三</text>
  </g>
</svg>
```

### 4.2 层级树（适合 B+ 树、分类、目录）

```html
<svg viewBox="0 0 680 200" role="img" aria-label="三层结构示意">
  <title>三层结构示意</title>
  <g font-family="'Source Han Sans SC','Microsoft YaHei',sans-serif" font-size="13" fill="#1a1a1a">
    <rect x="270" y="16" width="140" height="40" fill="#fff" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="340" y="42" text-anchor="middle">根节点</text>
    <path d="M340,56 L340,78 M180,78 L500,78" stroke="#1a1a1a" stroke-width="1.6" fill="none"/>
    <path d="M180,78 L180,96 M340,78 L340,96 M500,78 L500,96"
          stroke="#1a1a1a" stroke-width="1.6" fill="none"/>
    <rect x="110" y="98" width="140" height="40" fill="#fff" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="180" y="124" text-anchor="middle">分支 A</text>
    <rect x="270" y="98" width="140" height="40" fill="#fff" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="340" y="124" text-anchor="middle">分支 B</text>
    <rect x="430" y="98" width="140" height="40" fill="#fff" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="500" y="124" text-anchor="middle">分支 C</text>
    <text x="340" y="176" text-anchor="middle" font-size="12" fill="#5b5b5b">在图下方用一句话说明这张图要回答的问题</text>
  </g>
</svg>
```

### 4.3 时序（只画 3 个参与者和 3 条消息）

```html
<svg viewBox="0 0 680 220" role="img" aria-label="时序示意">
  <title>时序示意</title>
  <g font-family="'Source Han Sans SC','Microsoft YaHei',sans-serif" font-size="13" fill="#1a1a1a">
    <rect x="60" y="16" width="120" height="36" fill="#fff" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="120" y="39" text-anchor="middle">客户端</text>
    <rect x="280" y="16" width="120" height="36" fill="#fff" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="340" y="39" text-anchor="middle">服务</text>
    <rect x="500" y="16" width="120" height="36" fill="#fff" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="560" y="39" text-anchor="middle">数据库</text>
    <line x1="120" y1="52" x2="120" y2="190" stroke="#d8d8d8" stroke-width="1.4" stroke-dasharray="4 4"/>
    <line x1="340" y1="52" x2="340" y2="190" stroke="#d8d8d8" stroke-width="1.4" stroke-dasharray="4 4"/>
    <line x1="560" y1="52" x2="560" y2="190" stroke="#d8d8d8" stroke-width="1.4" stroke-dasharray="4 4"/>
    <line x1="120" y1="80" x2="336" y2="80" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="228" y="74" text-anchor="middle" font-size="12">① 请求</text>
    <line x1="340" y1="118" x2="556" y2="118" stroke="#1a1a1a" stroke-width="1.6"/>
    <text x="448" y="112" text-anchor="middle" font-size="12">② 查询</text>
    <line x1="560" y1="156" x2="344" y2="156" stroke="#1a1a1a" stroke-width="1.6" stroke-dasharray="6 4"/>
    <text x="452" y="150" text-anchor="middle" font-size="12">③ 返回</text>
  </g>
</svg>
```

## 5. Mermaid 离线方案

```bash
cat > diagram.mmd <<'EOF'
flowchart LR
  A[请求] --> B{命中索引?}
  B -- 是 --> C[返回]
  B -- 否 --> D[全表扫描]
EOF
npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg -b transparent
```

把生成的 `diagram.svg` 内容内联进 HTML，不要用 `<script src="...mermaid...">`。如果必须保留 Mermaid 源码，把它放进 HTML 注释里，方便以后修改。

## 6. 打印检查

- 缩小到 80% 预览，文字是否仍然可读。
- 转灰度预览，分类是否仍然可区分。
- 图是否跨页；跨页就加 `break-inside: avoid` 或缩小图。
- 图中是否有纯色块承载关键信息；有就加文字标签。
