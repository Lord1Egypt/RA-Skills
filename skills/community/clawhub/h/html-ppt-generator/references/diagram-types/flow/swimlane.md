# swimlane · 泳道图

**适用：** 跨部门流程、审批流转、角色协作、服务交互
**高度：** 200px（3泳道）；每增加一道 +67px

**结构公式：** 竖向分隔为 N 个泳道（每道代表一个角色），每道内水平排列流程步骤，跨道箭头表示交接。

```html
<svg viewBox="0 0 940 200" style="width:100%;height:200px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="sw-arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#475569"/>
    </marker>
  </defs>
  <!-- 泳道外框 -->
  <rect x="0" y="0" width="940" height="200" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.06)" stroke-width="1" rx="4"/>
  <!-- 泳道1：客户 -->
  <rect x="0" y="0" width="70" height="66" fill="rgba(59,130,246,0.15)" stroke="rgba(59,130,246,0.2)" stroke-width="1"/>
  <text x="35" y="37" text-anchor="middle" font-size="9" font-weight="700" fill="#3b82f6">客户</text>
  <rect x="0" y="66" width="70" height="67" fill="rgba(139,92,246,0.12)" stroke="rgba(139,92,246,0.2)" stroke-width="1"/>
  <text x="35" y="103" text-anchor="middle" font-size="9" font-weight="700" fill="#8b5cf6">销售</text>
  <rect x="0" y="133" width="70" height="67" fill="rgba(16,185,129,0.12)" stroke="rgba(16,185,129,0.2)" stroke-width="1"/>
  <text x="35" y="170" text-anchor="middle" font-size="9" font-weight="700" fill="#10b981">财务</text>
  <!-- 泳道分割线 -->
  <line x1="0" y1="66" x2="940" y2="66" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="0" y1="133" x2="940" y2="133" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
  <line x1="70" y1="0" x2="70" y2="200" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
  <!-- 步骤：客户道 -->
  <rect x="90" y="16" width="100" height="34" rx="5" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="140" y="37" text-anchor="middle" font-size="9.5" font-weight="600" fill="#93c5fd">提交需求</text>
  <rect x="400" y="16" width="100" height="34" rx="5" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="450" y="37" text-anchor="middle" font-size="9.5" font-weight="600" fill="#93c5fd">确认方案</text>
  <rect x="720" y="16" width="100" height="34" rx="5" fill="rgba(59,130,246,0.2)" stroke="rgba(59,130,246,0.4)" stroke-width="1"/>
  <text x="770" y="37" text-anchor="middle" font-size="9.5" font-weight="600" fill="#93c5fd">验收签字</text>
  <!-- 步骤：销售道 -->
  <rect x="245" y="82" width="100" height="34" rx="5" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="295" y="103" text-anchor="middle" font-size="9.5" font-weight="600" fill="#c4b5fd">分析需求</text>
  <rect x="555" y="82" width="100" height="34" rx="5" fill="rgba(139,92,246,0.2)" stroke="rgba(139,92,246,0.4)" stroke-width="1"/>
  <text x="605" y="103" text-anchor="middle" font-size="9.5" font-weight="600" fill="#c4b5fd">提交报价</text>
  <!-- 步骤：财务道 -->
  <rect x="720" y="149" width="100" height="34" rx="5" fill="rgba(16,185,129,0.2)" stroke="rgba(16,185,129,0.4)" stroke-width="1"/>
  <text x="770" y="170" text-anchor="middle" font-size="9.5" font-weight="600" fill="#6ee7b7">开具发票</text>
  <!-- 跨道连接箭头 -->
  <line x1="190" y1="33" x2="245" y2="33" stroke="#475569" stroke-width="1.5"/>
  <line x1="245" y1="33" x2="245" y2="82" stroke="#475569" stroke-width="1.5" marker-end="url(#sw-arr)"/>
  <line x1="345" y1="99" x2="400" y2="99" stroke="#475569" stroke-width="1.5"/>
  <line x1="400" y1="99" x2="400" y2="33" stroke="#475569" stroke-width="1.5" marker-end="url(#sw-arr)"/>
  <line x1="655" y1="99" x2="720" y2="99" stroke="#475569" stroke-width="1.5"/>
  <line x1="720" y1="99" x2="720" y2="33" stroke="#475569" stroke-width="1.5" marker-end="url(#sw-arr)"/>
  <line x1="820" y1="33" x2="870" y2="33" stroke="#475569" stroke-width="1.5"/>
  <line x1="820" y1="166" x2="870" y2="166" stroke="#475569" stroke-width="1.5"/>
</svg>
```

**参数说明：**
- 泳道标签列宽 70px，每道高 67px（3道共 200px）
- 每道用独立色系（蓝/紫/绿），步骤框 100×34px，rx=5
- 跨道箭头：先水平延伸至目标列 x，再垂直进入目标道
- 每增加一个泳道：高度 +67px，在对应 y 区间添加标签和步骤
