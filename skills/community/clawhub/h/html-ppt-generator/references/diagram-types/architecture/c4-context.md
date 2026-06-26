# c4-context · C4 上下文图

**适用：** 系统边界划定、外部依赖关系、用户与系统交互视图
**高度：** 220px

**结构公式：** 中心系统大框 + 四周用户/外部系统小框 + 带标注的交互箭头。

```
布局规则：
  中心系统：约 200×70px，主色填充，置于 SVG 中央
  外部用户/角色：圆形图标 r=18 + 文字，上方或左右
  外部系统：80×36px 小框，虚线边框，围绕中心排布
  连接线：带标注的直线或曲线，label 说明数据流向
  内部系统：实线边框；外部系统：虚线边框区分
```

```html
<svg viewBox="0 0 700 220" style="width:100%;height:220px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="c4-arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="#475569"/>
    </marker>
  </defs>
  <!-- 中心系统 -->
  <rect x="245" y="74" width="210" height="70" rx="6" fill="var(--p)" opacity="0.9"/>
  <text x="350" y="103" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">核心系统</text>
  <text x="350" y="120" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.75)">[Software System]</text>
  <text x="350" y="135" text-anchor="middle" font-size="8.5" fill="rgba(255,255,255,0.6)">系统简要描述</text>
  <!-- 用户（上方） -->
  <circle cx="350" cy="20" r="14" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
  <text x="350" y="24" text-anchor="middle" font-size="11" fill="var(--mt)">👤</text>
  <text x="350" y="44" text-anchor="middle" font-size="9" font-weight="600" fill="var(--t)">最终用户</text>
  <text x="350" y="54" text-anchor="middle" font-size="8" fill="var(--dt)">[Person]</text>
  <!-- 用户→系统箭头 -->
  <line x1="350" y1="58" x2="350" y2="74" stroke="#475569" stroke-width="1.5" marker-end="url(#c4-arr)"/>
  <text x="360" y="68" font-size="7.5" fill="#64748b">使用</text>
  <!-- 外部系统（左） -->
  <rect x="30" y="89" width="130" height="40" rx="4" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.15)" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="95" y="107" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--mt)">外部服务 A</text>
  <text x="95" y="120" text-anchor="middle" font-size="7.5" fill="var(--dt)">[External System]</text>
  <!-- 左←→中 -->
  <line x1="160" y1="109" x2="245" y2="109" stroke="#475569" stroke-width="1.5" marker-end="url(#c4-arr)"/>
  <text x="200" y="104" text-anchor="middle" font-size="7.5" fill="#64748b">调用API</text>
  <!-- 外部系统（右） -->
  <rect x="540" y="89" width="130" height="40" rx="4" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.15)" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="605" y="107" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--mt)">外部服务 B</text>
  <text x="605" y="120" text-anchor="middle" font-size="7.5" fill="var(--dt)">[External System]</text>
  <!-- 中→右 -->
  <line x1="455" y1="109" x2="540" y2="109" stroke="#475569" stroke-width="1.5" marker-end="url(#c4-arr)"/>
  <text x="496" y="104" text-anchor="middle" font-size="7.5" fill="#64748b">推送消息</text>
  <!-- 外部系统（下） -->
  <rect x="245" y="174" width="210" height="40" rx="4" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.15)" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="350" y="192" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--mt)">下游数据库/存储</text>
  <text x="350" y="207" text-anchor="middle" font-size="7.5" fill="var(--dt)">[External Storage]</text>
  <!-- 中→下 -->
  <line x1="350" y1="144" x2="350" y2="174" stroke="#475569" stroke-width="1.5" marker-end="url(#c4-arr)"/>
  <text x="360" y="162" font-size="7.5" fill="#64748b">读写</text>
</svg>
```

**参数说明：**
- 中心系统：主色填充（var(--p)），圆角 rx=6，内含系统名+类型标注+描述
- 外部系统：低透明度填充 + 虚线边框（stroke-dasharray="4,3"）
- 用户角色：圆形背景 + 图标，置于中心上方
- 箭头标注：贴近连线，font-size 7.5px，fill="#64748b"
