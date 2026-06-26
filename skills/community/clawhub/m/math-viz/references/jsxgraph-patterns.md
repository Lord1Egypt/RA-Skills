# JSXGraph 代码模式参考

> SKILL.md 引用本文档获取 JSXGraph 常用代码模式。
> 搜索关键词：可拖拽点、滑块、动画、轨迹、函数图像、辅助线

---

## 1. 画板初始化

```javascript
const board = JXG.JSXGraph.initBoard('jxgbox', {
  boundingbox: [-5, 5, 5, -5],  // [left, top, right, bottom]
  axis: true,
  grid: true,
  keepAspectRatio: true,
  showCopyright: false,
  pan: { enabled: true },
  zoom: { enabled: true }
});
```

**boundingbox 选择指南：**
- 代数题：`[-8, 8, 8, -8]`
- 几何题（单图形）：`[-3, 5, 7, -3]`（根据图形范围调整）
- 函数题：`[-8, 10, 8, -2]`（上大下小，适合看曲线）

---

## 2. 基本几何元素

### 点

```javascript
// 固定点
const A = board.create('point', [2, 3], {
  name: 'A', size: 3, face: 'o',
  strokeColor: '#333', fillColor: '#333',
  label: { fontSize: 14, offset: [8, 8] }
});

// 可拖拽点（默认即可拖）
const P = board.create('point', [1, 0], {
  name: 'P', size: 5, face: 'o',
  strokeColor: '#2980b9', fillColor: '#3498db',
  label: { fontSize: 14, color: '#2980b9' }
});

// 约束点到线段上（如P在BC上移动）
P.on('drag', function() {
  let x = P.X();
  x = Math.max(B.X(), Math.min(C.X(), x));
  P.setPosition(JXG.COORDS_BY_USER, [x, 0]);
  board.update();
});

// 函数点（坐标由函数决定）
const F = board.create('point', [
  function() { return slider.Value(); },
  function() { return Math.sin(slider.Value()); }
], { name: '', size: 3 });
```

### 线段/直线/射线

```javascript
// 线段
board.create('segment', [A, B], { strokeColor: '#333', strokeWidth: 2 });

// 直线
board.create('line', [A, B], { strokeColor: '#999', dash: 2 });

// 射线
board.create('ray', [A, B], { strokeColor: '#999' });

// 虚线辅助线
board.create('segment', [A, B], {
  strokeColor: '#e74c3c', strokeWidth: 1.5, dash: 3
});
```

### 多边形

```javascript
board.create('polygon', [A, B, C, D], {
  fillColor: '#f8f9fa', fillOpacity: 0.3,
  strokeColor: '#333', strokeWidth: 2,
  vertices: { visible: false }  // 隐藏自动生成的顶点
});
```

### 圆

```javascript
// 圆心+半径
board.create('circle', [center, radius], {
  strokeColor: '#e94560', strokeWidth: 2,
  fillColor: '#e94560', fillOpacity: 0.05
});

// 圆心+过一点
board.create('circle', [center, pointOnCircle], { ... });

// 外接圆（过三点）
board.create('circumcircle', [A, B, C], { ... });
```

### 角度

```javascript
board.create('angle', [A, B, C], {
  radius: 0.5,
  fillColor: '#fbbc04', fillOpacity: 0.2,
  strokeColor: '#fbbc04', strokeWidth: 1,
  name: '60°',
  label: { fontSize: 12 }
});
```

---

## 3. 滑块控制

```javascript
// 在画板内创建滑块
const slider = board.create('slider', [
  [1, -3], [5, -3], [0, 2, 8]  // [起点, 终点, [最小, 初始, 最大]]
], {
  name: '参数 t',
  strokeColor: '#e94560',
  fillColor: '#e94560',
  size: 8,
  label: { fontSize: 12 }
});

// 读取滑块值
const val = slider.Value();

// 滑块控制几何元素
const A = board.create('point', [
  function() { return 2 * Math.cos(slider.Value()); },
  function() { return 2 * Math.sin(slider.Value()); }
], { name: 'A' });
```

### HTML滑块（更灵活）

```html
<input type="range" id="mySlider" min="0" max="8" step="0.1" value="4">
<span id="myVal">4.0</span>
<script>
document.getElementById('mySlider').addEventListener('input', function() {
  const val = parseFloat(this.value);
  document.getElementById('myVal').textContent = val.toFixed(1);
  // 更新几何元素
  P.setPosition(JXG.COORDS_BY_USER, [val, 0]);
  board.update();
  updateData();
});
</script>
```

---

## 4. 动画

### requestAnimationFrame 动画

```javascript
let animId = null;
let animRunning = false;
let animDir = 1;

function startAnimation() {
  animRunning = true;
  let px = 0;
  animDir = 1;
  function step() {
    if (!animRunning) return;
    px += animDir * 0.03;
    if (px >= 8) { px = 8; animDir = -1; }
    if (px <= 0) { px = 0; animDir = 1; }
    P.setPosition(JXG.COORDS_BY_USER, [px, 0]);
    board.update();
    updateData();
    animId = requestAnimationFrame(step);
  }
  step();
}

function stopAnimation() {
  animRunning = false;
  cancelAnimationFrame(animId);
}
```

### 旋转动画

```javascript
function rotatePoint(point, center, angle) {
  const dx = point.X() - center.X();
  const dy = point.Y() - center.Y();
  const cos = Math.cos(angle), sin = Math.sin(angle);
  return [
    center.X() + dx * cos - dy * sin,
    center.Y() + dx * sin + dy * cos
  ];
}
```

---

## 5. 函数图像

```javascript
// 基本函数
board.create('functiongraph', [
  function(x) { return x * x - 2; }
], { strokeColor: '#e94560', strokeWidth: 2 });

// 带参数的函数
board.create('functiongraph', [
  function(x) { return aSlider.Value() * x * x + bSlider.Value() * x; }
], { strokeColor: '#4285f4', strokeWidth: 2 });

// 多函数对比
board.create('functiongraph', [f1], { strokeColor: '#e94560', name: 'f(x)' });
board.create('functiongraph', [f2], { strokeColor: '#4285f4', name: 'g(x)' });

// 切线
board.create('tangent', [pointOnCurve], {
  strokeColor: '#27ae60', strokeWidth: 1.5, dash: 2
});
```

---

## 6. 轨迹曲线

```javascript
// 参数曲线
board.create('curve', [
  function(t) { return t; },           // x(t)
  function(t) { return f(t); },        // y(t)
  tMin, tMax                            // 参数范围
], { strokeColor: '#ee5a24', strokeWidth: 2 });

// 动点轨迹（自动记录）
P.setAttribute({ trace: true, traceAttributes: { strokeColor: '#ee5a24', strokeWidth: 1 } });

// 轨迹清除
board.clearTraces();
```

---

## 7. 辅助线开关

```javascript
// 创建辅助线
const auxLine1 = board.create('segment', [A, B], {
  strokeColor: '#e74c3c', strokeWidth: 1.5, dash: 3, visible: false
});
const auxLine2 = board.create('segment', [C, D], {
  strokeColor: '#e74c3c', strokeWidth: 1.5, dash: 3, visible: false
});

// HTML checkbox 控制
document.getElementById('showAux').addEventListener('change', function() {
  auxLine1.setAttribute({ visible: this.checked });
  auxLine2.setAttribute({ visible: this.checked });
  board.update();
});
```

---

## 8. 实时数据计算与显示

```javascript
function updateData() {
  const x = P.X();
  const ep = Math.sqrt((x-4)*(x-4) + 36);
  const pd = Math.sqrt((x-8)*(x-8) + 36);

  document.getElementById('epVal').textContent = ep.toFixed(3);
  document.getElementById('pdVal').textContent = pd.toFixed(3);
  document.getElementById('sumVal').textContent = (ep + pd).toFixed(3);
}

// 在点拖拽时更新
P.on('drag', function() {
  // ...约束逻辑
  updateData();
});
```

---

## 9. 两直线交点

```javascript
// 自动计算交点
const intersection = board.create('intersection', [line1, line2, 0], {
  name: 'E', size: 4, face: 'o',
  strokeColor: '#fbbc04', fillColor: '#f1c40f'
});
```

---

## 10. 常见几何变换

```javascript
// 平移
board.create('transform', [2, 1], { type: 'translate' });

// 旋转
board.create('transform', [Math.PI/4, center], { type: 'rotate' });

// 对称（关于点）
board.create('transform', [center], { type: 'reflect' });

// 对称（关于直线）
board.create('transform', [line], { type: 'reflect' });

// 应用变换
const Ap = board.create('point', [A, transform1, transform2], { name: "A'" });
```

---

## 11. 布局模式

### 左画板 + 右控制面板

```html
<style>
.main { display: flex; gap: 14px; padding: 14px; }
.graph-panel { flex: 1; }
.panel { width: 340px; }
@media (max-width: 900px) {
  .main { flex-direction: column; }
  .panel { width: 100%; }
}
</style>
<div class="main">
  <div class="graph-panel"><div id="jxgbox"></div></div>
  <div class="panel">
    <!-- 控制面板内容 -->
  </div>
</div>
```

---

## ⚠️ 12. 常见陷阱与避坑指南（实战血泪教训）

以下陷阱都在真实项目中导致过白屏、渲染残留、数值错误等问题。

### 陷阱1：`angle` 复合元素渲染残留

**现象：** 每次 `draw()` 重绘后，角度标注会累积（如左上角出现一排黄色扇形）。

**根因：** `angle` 是 JSXGraph 的复合元素，`board.removeObject()` 无法彻底清除其内部SVG节点。

**修复：** 用 `arc` + `text` 原生元素替代。详见 SKILL.md 常见陷阱修复指南。

### 陷阱2：`create()` 调用缺少外层数组闭合 `]`

**现象：** 整个 `<script>` 块 SyntaxError，画板白屏。

**根因：** `create(['type', [...], {...}]);` 需要精确的3对括号：`([])`。

**检查：** 对每处 `create(` 调用手动数括号：`(`+1 `[`+1 `{`+1，`)`-1 `]`-1 `}`-1，深度归零时后跟 `;`。

### 陷阱3：`suspendUpdate`/`unsuspendUpdate`

**现象：** 调用后画板白屏（TypeError）。

**修复：** 直接操作 + `board.update()`，不使用这些API。

### 陷阱4：text元素的 `CSS` 属性传对象

**现象：** text 创建失败。

**修复：** 用 `fontSize`、`color` 等原生属性替代 CSS 对象。

### 陷阱5：`line`（无限直线）渲染残留

**现象：** 画板边缘多余端点标记。

**修复：** 改用 `segment`，手动计算延长端点。

### 陷阱6：`clearElements` 正向遍历遗漏

**修复：** 始终反向遍历删除（`i--`）。

### 陷阱7：HTML中多个 `<script>` 标签导致提取错位

**现象：** `node --check` 误报。

**修复：** 始终用 `html.rfind('<script>')` 定位内联脚本。
