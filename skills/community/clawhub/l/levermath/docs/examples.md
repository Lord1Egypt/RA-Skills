# 示例与可回收的机制

本仓库把可复用的引擎与具体课堂例子分开。`src/engine/` 实现翻页、缩略图、分步、公式与交互图的挂载；`templates/basic/` 是起步布局；`examples/` 展示如何把这些机制用于实际数学讲解。

## 折纸生成椭圆

`examples/origami-ellipse/` 是完整的 13 帧课堂示例：从折纸作品照片引入，经历折痕包络、交点轨迹、椭圆定义、坐标系、标准方程、化简与方程对比。`interactive/crease.ts` 展示同一几何构造的两种交互模式；`geometry/` 保留 GeoGebra 文件与 TikZ 源，便于检查构造，而不是模板的运行时依赖。构建产物在 `dist/examples/origami-ellipse/index.html`。

## 向量范数

`examples/vector-p-norm/` 是完整的 10 帧示例：向量空间、内积空间、赋范空间、p-范数定义、数值计算、单位圆形变、范数等价与总结。互动模块使用 JSXGraph，通过滑块修改参数，提供课堂演示按钮；帧内按键分步不自动播放。构建产物在 `dist/examples/vector-p-norm/index.html`。

## 新课件的原则

不要从原始讲课目录向通用引擎复制课程专有的照片、证明、坐标数据和字体子集。若需参考做法，阅读本仓库中的精简示例，再为新课件制作自己的内容、图形和字集。更改 CSS 主题变量时，同时检查 SVG 中写死的颜色。
