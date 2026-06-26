---
name: minemap-skills
display-name: MineMap 3D Map Engine Skills
description: >
  MineMap 地图引擎（4.23）完整技能库。覆盖地图初始化、二三维叠加、3D Tiles、SceneModel、地形分析、粒子系统、视频投影、漫游跟踪、后处理、GaussianSplatting 等四十余个主题。技能均经源码与 demo 双重验证，可直接落地。
license: MIT-0
---

# MineMap Skills（基于 MineMap 4.23 源码）

MineMap 是一套"二维地图引擎能力 + 三维场景引擎能力"统一 runtime，主入口为 `Map`。  
本技能库按主题拆包，让 AI 编码助手在生成 MineMap 代码时，优先使用源码一致、版本匹配、可直接落地的 API 与模式。

> GitHub 源仓库: https://github.com/ming1zhou88/minemap-skills

---

## 使用方式

按需求主题加载对应 `SKILL.md`：

| 需求 | 对应技能包 |
|------|-----------|
| 初始化地图、控件、生命周期 | `minemap-fundamentals` |
| 官网入口、账号开通、文档导航 | `minemap-official-resources-and-onboarding` |
| key/solution、域名与资源配置 | `minemap-global-configuration` |
| 控件体系、自定义控件 | `minemap-widget-and-controls` |
| Marker / Popup / DOM 覆盖物 | `minemap-marker-and-popup` |
| 图层、Source、样式更新 | `minemap-style-and-data` |
| 图层系统与渲染顺序 | `minemap-layer-system` |
| style v8 结构、setStyle() | `minemap-style-system` |
| 二三维叠加、贴地、贴模型 | `minemap-2d-3d-overlay-and-classification` |
| ThreeLayer / threejs 融合 | `minemap-threejs-integration` |
| SceneModel / SceneTileset / SceneObject | `minemap-scene-components` |
| 3D Tiles 运行时着色、显隐 | `minemap-3d-tiles-runtime-control` |
| 模型运行时调试、线框、材质更新 | `minemap-model-runtime-debug` |
| Primitive、几何、材质 | `minemap-primitives-and-materials` |
| 包围体、碰撞检测、BVH | `minemap-collision-and-bounding` |
| 坐标变换与锚点矩阵 | `minemap-transforms` |
| 数学对象与姿态表达 | `minemap-math-foundations` |
| 光照、阴影 | `minemap-lighting-and-shadows` |
| 材质选型与着色 | `minemap-material-system-and-shading` |
| Primitive 贴地 | `minemap-primitive-adapt-terrain` |
| 屏幕空间反射（SSR） | `minemap-screen-space-reflection` |
| 水面材质、折射/反射 | `minemap-water-surface-and-refraction` |
| 事件、hover、GPU 拾取 | `minemap-events-and-picking` |
| 地形、量算、空间分析 | `minemap-terrain-and-analysis` |
| WebGL 后端选择、性能实践 | `minemap-performance-and-backend` |
| 后处理链、描边、雨雪、雾效 | `minemap-post-process-and-render-pipeline` |
| 抗锯齿与图像质量 | `minemap-anti-aliasing` |
| 相机限制、近裁剪面、截图 | `minemap-camera-constraints-and-screenshot` |
| 卷帘对比 Compare 插件 | `minemap-plugin-compare-swipe` |
| 编辑插件 | `minemap-plugin-edit` |
| ECharts 叠加插件 | `minemap-plugin-echarts-integration` |
| 在线示例编辑器 | `minemap-plugin-demo-editor` |
| 视频投影 | `minemap-business-video-projection` |
| 可视域 / 通视 | `minemap-business-visibility-analysis` |
| 淹没 / 阴影分析 | `minemap-business-flood-and-shadow` |
| 漫游 / 跟踪 | `minemap-business-roaming-and-tracking` |
| 粒子系统与特效 | `minemap-business-particle-and-special-effects` |
| 北斗网格码 | `minemap-business-beidou-grid` |
| 行政区划拉伸 | `minemap-business-admin-division` |
| Gaussian Splatting | `minemap-business-gaussian-splatting` |
| 倾斜摄影 / BIM / 3D Tiles 装载 | `minemap-business-oblique-bim` |
| 航线、飞线、流动轨迹 | `minemap-business-airline-and-lines` |
| 三维量算、贴地面积 | `minemap-business-measurement` |
| 地形裁剪面 | `minemap-business-spatial-analysis-suite` |

---

## 适用原则

1. **优先新接口**：3D 数据优先 `map.addSceneComponent()`，避免继续扩散废弃的 `3d-tiles` source/layer 写法。
2. **先判断加载状态**：关键操作挂到 `load` / `style.load` 后执行，避免时序错误。
3. **围绕渲染后端做兜底**：默认 `auto`，按 `webgpu -> webgl2 -> webgl1` 降级，针对特效做能力判断。
4. **优先可维护写法**：采用引擎公开类（`minemap.SceneModel`、`minemap.SceneTileset`、`minemap.Primitive` 等）而非内部私有对象。

---

## 版本基线

- **引擎版本**：`minemap-3d-engine@4.23.0`  
- **校验依据**：`source/api/map.js`、`source/index.js`、`source/style/style.js`、`demo/html/*.html`

---

## Quick Start

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <script src="https://minedata.cn/minemapapi/v4.23.0/minemap.js"></script>
  <link href="https://minedata.cn/minemapapi/v4.23.0/minemap.css" rel="stylesheet" />
</head>
<body>
  <div id="map" style="width:100%;height:100vh;"></div>
  <script>
    minemap.key = "YOUR_KEY";
    minemap.solution = YOUR_SOLUTION_ID;
    minemap.domainUrl = "https://minedata.cn";

    const map = new minemap.Map({
      container: "map",
      style: "minemap://styles/street",
      position: [116.39, 39.9, 3000],
      pitch: 60,
      bearing: 0,
      renderBackend: "auto"   // auto -> webgpu / webgl2 / webgl1
    });

    map.on("load", () => {
      // 加三维模型
      map.addSceneComponent({
        id: "building",
        type: "3d-model",
        data: "https://example.com/building.glb",
        position: new minemap.Math.Vector3(116.39, 39.9, 0),
        rotation: [90, 0, 0],
        scale: [1, 1, 1],
        allowPick: true
      });
    });
  </script>
</body>
</html>
```

---

## See Also

- [MineMap 官网](https://minedata.cn)  
- [GitHub 源仓库](https://github.com/ming1zhou88/minemap-skills)
