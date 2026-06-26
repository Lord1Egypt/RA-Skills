# tree · 树状层级图

**适用：** 组织架构、分类体系、知识树、攻击树
**高度：** 120px（横向展开）

```html
<svg viewBox="0 0 580 120" style="width:100%;height:120px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <!-- 根节点 -->
  <rect x="0" y="45" width="100" height="30" rx="4" fill="var(--p)"/>
  <text x="50" y="64" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">根节点</text>
  <!-- 连接线 -->
  <path d="M100,60 C130,60 130,25 160,25" fill="none" stroke="#1e293b" stroke-width="1.5"/>
  <path d="M100,60 C130,60 130,60 160,60" fill="none" stroke="#1e293b" stroke-width="1.5"/>
  <path d="M100,60 C130,60 130,95 160,95" fill="none" stroke="#1e293b" stroke-width="1.5"/>
  <!-- 二级节点 -->
  <rect x="160" y="10" width="100" height="28" rx="4" fill="var(--pm)" stroke="var(--bd)" stroke-width="1"/>
  <text x="210" y="28" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">分类 A</text>
  <rect x="160" y="46" width="100" height="28" rx="4" fill="var(--pm)" stroke="var(--bd)" stroke-width="1"/>
  <text x="210" y="64" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">分类 B</text>
  <rect x="160" y="82" width="100" height="28" rx="4" fill="var(--pm)" stroke="var(--bd)" stroke-width="1"/>
  <text x="210" y="100" text-anchor="middle" font-size="9.5" font-weight="600" fill="var(--t)">分类 C</text>
  <!-- A的子节点 -->
  <path d="M260,24 C290,24 290,16 320,16" fill="none" stroke="#1e293b" stroke-width="1"/>
  <path d="M260,24 C290,24 290,32 320,32" fill="none" stroke="#1e293b" stroke-width="1"/>
  <rect x="320" y="6"  width="100" height="22" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="370" y="21" text-anchor="middle" font-size="8.5" fill="var(--mt)">子项 A1</text>
  <rect x="320" y="32" width="100" height="22" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="370" y="47" text-anchor="middle" font-size="8.5" fill="var(--mt)">子项 A2</text>
  <!-- B的子节点 -->
  <path d="M260,60 H320" fill="none" stroke="#1e293b" stroke-width="1"/>
  <rect x="320" y="49" width="100" height="22" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="370" y="64" text-anchor="middle" font-size="8.5" fill="var(--mt)">子项 B1</text>
  <!-- C的子节点 -->
  <path d="M260,96 C290,96 290,85 320,85" fill="none" stroke="#1e293b" stroke-width="1"/>
  <path d="M260,96 C290,96 290,107 320,107" fill="none" stroke="#1e293b" stroke-width="1"/>
  <rect x="320" y="74"  width="100" height="22" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="370" y="89"  text-anchor="middle" font-size="8.5" fill="var(--mt)">子项 C1</text>
  <rect x="320" y="99"  width="100" height="22" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <text x="370" y="114" text-anchor="middle" font-size="8.5" fill="var(--mt)">子项 C2</text>
</svg>
```

**参数说明：**
- 根节点：实色填充（最高优先级感）
- 二级节点：var(--pm) + var(--bd) 边框
- 三级节点：低透明度填充（层级弱化感）
- 连接线用 cubic bezier path（C）使曲线更自然
