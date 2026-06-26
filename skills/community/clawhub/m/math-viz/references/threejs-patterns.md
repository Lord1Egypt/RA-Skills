# Three.js 代码模式参考（立体几何）

> SKILL.md 引用本文档获取 Three.js 立体几何可视化代码模式。
> 搜索关键词：3D初始化、多面体、球体、截面、动画

---

## 1. 场景初始化

```javascript
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0f0f1a);

const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 100);
camera.position.set(6, 5, 8);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
const wrap = document.getElementById('canvasWrap');
renderer.setSize(wrap.clientWidth, wrap.clientHeight);
wrap.insertBefore(renderer.domElement, wrap.firstChild);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;

// 光照
const ambientLight = new THREE.AmbientLight(0x404060, 0.6);
scene.add(ambientLight);
const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
dirLight.position.set(5, 10, 7);
scene.add(dirLight);

// 网格
const gridHelper = new THREE.GridHelper(10, 10, 0x333355, 0x222244);
scene.add(gridHelper);

// 坐标轴
const axesHelper = new THREE.AxesHelper(2);
scene.add(axesHelper);

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', function() {
  camera.aspect = wrap.clientWidth / wrap.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(wrap.clientWidth, wrap.clientHeight);
});
```

---

## 2. 多面体绘制

### 通用多面体（自定义顶点+面）

```javascript
function drawPolyhedron(vertices, indices, color, opacity) {
  const geo = new THREE.BufferGeometry();
  const verts = [];
  vertices.forEach(v => verts.push(v[0], v[1], v[2]));
  geo.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();

  const mat = new THREE.MeshPhongMaterial({
    color: color, transparent: true, opacity: opacity,
    side: THREE.DoubleSide, depthWrite: false
  });
  const mesh = new THREE.Mesh(geo, mat);
  scene.add(mesh);

  // 线框
  const wireGeo = new THREE.WireframeGeometry(geo);
  const wireMat = new THREE.LineBasicMaterial({ color: 0x8888cc });
  const wire = new THREE.LineSegments(wireGeo, wireMat);
  scene.add(wire);

  return mesh;
}
```

### 常见多面体顶点

```javascript
// 正三棱锥（底面正三角形在xz平面，顶点在y轴）
function regularTriPyramid(a, h) {
  const r = a / Math.sqrt(3);
  return {
    vertices: [[r,0,0], [-r/2,0,r*Math.sqrt(3)/2], [-r/2,0,-r*Math.sqrt(3)/2], [0,h,0]],
    indices: [0,1,2, 0,1,3, 1,2,3, 2,0,3]
  };
}

// 正四棱锥
function regularQuadPyramid(a, h) {
  const half = a / 2;
  return {
    vertices: [[half,0,half], [-half,0,half], [-half,0,-half], [half,0,-half], [0,h,0]],
    indices: [0,1,2, 0,2,3, 0,1,4, 1,5,4, ...]  // 需补全面
  };
}

// 长方体
function cuboid(a, b, c) {
  const ha=a/2, hb=b/2, hc=c/2;
  return {
    vertices: [
      [ha,0,hb], [-ha,0,hb], [-ha,0,-hb], [ha,0,-hb],
      [ha,c,hb], [-ha,c,hb], [-ha,c,-hb], [ha,c,-hb]
    ],
    indices: [/* 12个三角形面 */]
  };
}
```

---

## 3. 球体

```javascript
function drawSphere(center, radius, color, alpha) {
  const geo = new THREE.SphereGeometry(radius, 32, 24);
  const mat = new THREE.MeshPhongMaterial({
    color: color, transparent: true, opacity: alpha,
    side: THREE.DoubleSide, depthWrite: false
  });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.set(center[0], center[1], center[2]);
  scene.add(mesh);

  // 球面线框
  const wireGeo = new THREE.WireframeGeometry(geo);
  const wireMat = new THREE.LineBasicMaterial({
    color: color, transparent: true, opacity: 0.2
  });
  const wire = new THREE.LineSegments(wireGeo, wireMat);
  wire.position.set(center[0], center[1], center[2]);
  scene.add(wire);

  return mesh;
}
```

### 外接球计算

```javascript
// 正棱锥外接球
function circumSphereRegularPyramid(baseCircumR, height) {
  const yc = (height*height - baseCircumR*baseCircumR) / (2*height);
  const R = Math.sqrt(yc*yc + baseCircumR*baseCircumR);
  return { center: [0, Math.max(0, yc), 0], radius: R };
}

// 长方体外接球
function circumSphereCuboid(a, b, c) {
  const R = Math.sqrt(a*a + b*b + c*c) / 2;
  return { center: [0, c/2, 0], radius: R };
}
```

### 内切球计算

```javascript
// 正棱锥内切球
function inspherePyramid(baseArea, lateralArea, height) {
  const volume = baseArea * height / 3;
  const surfaceArea = baseArea + lateralArea;
  const r = 3 * volume / surfaceArea;
  return r;
}

// 长方体内切球（仅正方体时存在）
function insphereCuboid(a, b, c) {
  return Math.min(a, b, c) / 2;
}
```

---

## 4. 辅助线

```javascript
// 虚线
function drawDashedLine(p1, p2, color) {
  const geo = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(p1[0], p1[1], p1[2]),
    new THREE.Vector3(p2[0], p2[1], p2[2])
  ]);
  const mat = new THREE.LineDashedMaterial({
    color: color, dashSize: 0.15, gapSize: 0.1, transparent: true, opacity: 0.6
  });
  const line = new THREE.Line(geo, mat);
  line.computeLineDistances();
  scene.add(line);
  return line;
}

// 球心标记
function drawPoint(pos, color) {
  const geo = new THREE.SphereGeometry(0.1, 12, 12);
  const mat = new THREE.MeshBasicMaterial({ color: color });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.set(pos[0], pos[1], pos[2]);
  scene.add(mesh);
  return mesh;
}
```

---

## 5. 截面

```javascript
// 水平截面（y = h 处）
function drawHorizontalSection(pyramidVertices, h) {
  // 计算截面多边形：每条棱与 y=h 平面的交点
  const sectionPoints = [];
  for (let i = 0; i < pyramidVertices.length; i++) {
    const a = pyramidVertices[i];
    const b = pyramidVertices[(i+1) % pyramidVertices.length]; // 或 apex
    if ((a[1] - h) * (b[1] - h) < 0) {
      const t = (h - a[1]) / (b[1] - a[1]);
      sectionPoints.push([
        a[0] + t*(b[0]-a[0]),
        h,
        a[2] + t*(b[2]-a[2])
      ]);
    }
  }
  // 绘制截面多边形
  if (sectionPoints.length >= 3) {
    const geo = new THREE.BufferGeometry();
    const verts = [];
    sectionPoints.forEach(p => verts.push(p[0], p[1], p[2]));
    geo.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
    geo.setIndex(/* 三角化索引 */);
    geo.computeVertexNormals();
    const mat = new THREE.MeshPhongMaterial({
      color: 0xff6b6b, transparent: true, opacity: 0.3,
      side: THREE.DoubleSide
    });
    scene.add(new THREE.Mesh(geo, mat));
  }
}
```

---

## 6. 资源清理

```javascript
function clearGroup(group) {
  while (group.children.length > 0) {
    const child = group.children[0];
    if (child.geometry) child.geometry.dispose();
    if (child.material) {
      if (Array.isArray(child.material)) child.material.forEach(m => m.dispose());
      else child.material.dispose();
    }
    group.remove(child);
  }
}
```

---

## 7. 完整页面结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <style>
    .main { display: flex; height: calc(100vh - 72px); }
    .canvas-wrap { flex: 1; position: relative; }
    .panel { width: 340px; background: #1a1a2e; overflow-y: auto; padding: 16px; }
  </style>
</head>
<body>
  <div class="header">...</div>
  <div class="main">
    <div class="canvas-wrap" id="canvasWrap">
      <div class="hint">🖱 拖拽旋转 | 滚轮缩放 | 右键平移</div>
    </div>
    <div class="panel">
      <!-- 参数滑块、显示控制、实时数据 -->
    </div>
  </div>
  <script>
    // 初始化场景
    // 绑定控件事件
    // 重建函数
  </script>
</body>
</html>
```
