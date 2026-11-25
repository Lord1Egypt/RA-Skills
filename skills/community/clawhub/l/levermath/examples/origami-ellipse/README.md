# 示例：折纸生成椭圆

完整的 13 帧课堂示例：折纸作品照片 → 折纸四步 → 折痕包络 → 交点轨迹 → 椭圆定义 → 坐标系 → 标准方程 → 化简 → b 的引入 → 焦点在 y 轴 → 两种方程对比 → 圆外取点 → 结束页。

## 直接播放

打开构建产物 [`dist/examples/origami-ellipse/index.html`](../../dist/examples/origami-ellipse/index.html)，双击即可离线放映。`examples/origami-ellipse/index.html` 只是源码开发入口，直接双击会显示指路说明。

## 构建与开发

```bash
bun run build:ellipse
bun run dev:ellipse
```

产物是 `dist/examples/origami-ellipse/index.html`。`geometry/` 保留原始 GeoGebra 文件、TikZ 源与生成的 SVG，仅作可检查的几何资料；放映时不依赖 GeoGebra。

`interactive/crease.ts` 给出 `crease`、`trace` 两种 JSXGraph 模式。动画不随切帧自动播放，点“自动演示”或拖动点后才开始。`assets/fonts/` 中的 WOFF2 只覆盖当前示例用字；修改文案后构建会自动重做字体子集。
