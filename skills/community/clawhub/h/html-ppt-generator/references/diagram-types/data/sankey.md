# sankey · 桑基图

**适用：** 流量/预算流向、能源分配、用户路径分流、来源去向分析
**高度：** 180–220px

**结构公式：** 左侧来源节点（竖条）→ 流量路径（宽度=占比的 bezier 曲线）→ 右侧去向节点。

**SVG 构建步骤：**
```
1. 计算每个节点的 y 起点（累加各流出/流入量的高度，加 4px 间隔）
2. 左节点：<rect x="0" y="{start}" width="16" height="{nodeH}" fill="主色"/>
3. 右节点：<rect x="总宽-16" y="{start}" width="16" height="{nodeH}" fill="对比色"/>
4. 流量路径：
   <path d="M 16,{src_mid} C {W×0.4},{src_mid} {W×0.6},{dst_mid} {W-16},{dst_mid}"
         fill="none" stroke="var(--p)" stroke-width="{flowWidth}" opacity="0.35"/>
5. 节点标签：左节点 text-anchor="end" x=-4；右节点 text-anchor="start" x=总宽+4
```

```html
<svg viewBox="0 0 600 200" style="width:100%;height:200px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 左侧来源节点 -->
  <rect x="0"  y="10"  width="16" height="80" rx="2" fill="#3b82f6"/>
  <rect x="0"  y="96"  width="16" height="50" rx="2" fill="#8b5cf6"/>
  <rect x="0"  y="152" width="16" height="30" rx="2" fill="#06b6d4"/>
  <!-- 右侧去向节点 -->
  <rect x="584" y="10"  width="16" height="60" rx="2" fill="#10b981"/>
  <rect x="584" y="76"  width="16" height="55" rx="2" fill="#f59e0b"/>
  <rect x="584" y="137" width="16" height="45" rx="2" fill="#ef4444"/>
  <!-- 流量路径：来源A(10~50) → 去向1 -->
  <path d="M16,30 C240,30 360,30 584,30" fill="none" stroke="#3b82f6" stroke-width="20" opacity="0.3"/>
  <!-- 流量路径：来源A(50~90) → 去向2 -->
  <path d="M16,70 C240,70 360,90 584,90" fill="none" stroke="#3b82f6" stroke-width="20" opacity="0.2"/>
  <!-- 流量路径：来源B → 去向2 -->
  <path d="M16,111 C240,111 360,110 584,112" fill="none" stroke="#8b5cf6" stroke-width="22" opacity="0.25"/>
  <!-- 流量路径：来源C → 去向3 -->
  <path d="M16,162 C240,162 360,155 584,155" fill="none" stroke="#06b6d4" stroke-width="14" opacity="0.3"/>
  <!-- 左侧标签 -->
  <text x="-4" y="54"  text-anchor="end" font-size="9" fill="var(--mt)">渠道A · 40%</text>
  <text x="-4" y="124" text-anchor="end" font-size="9" fill="var(--mt)">渠道B · 25%</text>
  <text x="-4" y="170" text-anchor="end" font-size="9" fill="var(--mt)">渠道C · 15%</text>
  <!-- 右侧标签 -->
  <text x="604" y="44"  text-anchor="start" font-size="9" fill="var(--mt)">产品A · 30%</text>
  <text x="604" y="107" text-anchor="start" font-size="9" fill="var(--mt)">产品B · 28%</text>
  <text x="604" y="162" text-anchor="start" font-size="9" fill="var(--mt)">产品C · 22%</text>
</svg>
```

**参数说明：**
- 节点高度 = 总可用高度 × 该节点占比；节点间保留 4–6px 间距
- 流量路径 stroke-width = 对应流量值 × 缩放比例；opacity=0.25–0.35
- bezier 控制点 x 固定在 `总宽×0.4` 和 `总宽×0.6` 实现 S 形平滑过渡
- 多源多目时，流量路径颜色跟随**来源节点**色系，opacity 区分流量大小
