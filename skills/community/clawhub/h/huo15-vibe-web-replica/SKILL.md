---
name: huo15-vibe-web-replica
displayName: 星火织境
version: 1.0.0
description: >-
  复刻与创作视觉沉浸式网站：3D 渲染、滚动驱动动画、平滑滚动、沉浸式特效。
  技术栈 Three.js + WebGL2、GSAP 3.12 + ScrollTrigger、Lenis 平滑滚动、
  Draco 压缩 GLB、Web Audio、KTX2 纹理压缩、TagCloud。当用户说"复刻网站"
  "vibe coding""氛围编程""做个 3D 滚动页面""Three.js""GSAP""ScrollTrigger"
  "Lenis""WebGL"或提供 URL/截图要求还原网站时使用。脚本 scripts/scaffold.sh
  一键创建 Vite + Three.js + GSAP + Lenis 项目。
homepage: https://github.com/zhaobod1/huo15-skills
metadata:
  openclaw:
    emoji: "✦"
    tags: ["vibe-coding", "three-js", "gsap", "webgl", "frontend", "3d"]
    requires:
      bins: ["node", "npm"]
aliases:
  - 星火织境
  - Vibe Web Replica
  - 氛围编程
  - 网站复刻
  - 3D滚动页面
  - Three.js网页
  - GSAP动画
  - vibe coding
---

# 星火织境 (Vibe Web Replica)

> 火一五星火绽放，织造沉浸式 Web 境界。
> 复刻或创作视觉震撼的沉浸式网站：3D 渲染 + 滚动驱动动画 + 平滑滚动 + 沉浸式特效。
> 灵感来自 Codex vibe-coding 方法论 — 分析目标 → 脚手架 → 构建 → 迭代。

## 技术栈

| 层 | 库 | 版本 |
|----|----|------|
| 3D 渲染 | three | ^0.169.0 |
| 动画 | gsap | 3.12.7 |
| 滚动驱动 | gsap ScrollTrigger | (bundled) |
| 平滑滚动 | lenis | ^1.1.20 |
| 构建工具 | vite | ^6.0 |
| GLB 压缩 | draco3dg loader | (three addon) |
| 音频 | Web Audio API | native |

## 工作流

### Step 1: 分析目标

如果给了 URL，用 `web_fetch` 抓取页面。识别：
- 布局结构（hero、章节、footer）
- 视觉风格（色彩、字体、间距）
- 交互模式（滚动效果、hover、3D）
- 资源需求（3D 模型、纹理、音频）

将简要规格写入项目根目录 `vibe-spec.md`。

### Step 2: 脚手架

运行脚手架脚本：

```bash
bash ~/.catpaw/skills/huo15-vibe-web-replica/scripts/scaffold.sh my-project
cd my-project && npm install
```

创建 Vite + Three.js + GSAP + Lenis 项目，所有模板预接线。

### Step 3: 构建 3D 场景

以 `templates/three-scene.js` 为起点。关键模式：

1. **场景设置**：Scene, PerspectiveCamera (fov 45-70), WebGLRenderer (antialias, alpha)
2. **光照**：AmbientLight + DirectionalLight (主光) + 可选轮廓光
3. **GLB 加载**：GLTFLoader + DRACOLoader (解码路径从 CDN)
4. **相机动画**：将相机 Z/Y/旋转绑定到滚动进度
5. **性能**：pixelRatio 上限 2，resize 处理，可选后处理

### Step 4: 滚动动画

使用 `templates/gsap-scroll.js`。关键模式：

1. **ScrollTrigger**：pin 章节、scrub 动画到滚动进度
2. **Timeline**：链式 tween（淡入 → 移动 → 旋转 → 淡出）
3. **SplitText**：标题逐字/逐词揭示
4. **Observer**：追踪滚动方向，触发方向性效果
5. **Lenis 联动**：Lenis 驱动 RAF，ScrollTrigger 使用 Lenis 滚动位置

### Step 5: 平滑滚动设置

使用 `templates/lenis-setup.js`。将 Lenis 接入 GSAP ScrollTrigger：

```javascript
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
```

### Step 6: 特效与打磨

- **粒子系统**：BufferGeometry + Points 或 instanced meshes
- **标签云**：导入 TagCloud.js 或用 CSS 3D 变换构建
- **音频**：Web Audio API — AudioContext, gain node, click-to-unlock 模式
- **后处理**：EffectComposer + UnrealBloomPass 发光
- **纹理压缩**：KTX2Loader 处理大纹理

### Step 7: 迭代

1. `npm run dev` 启动开发服务器
2. 浏览器打开，视觉检查
3. 与目标比对（截图或实时 URL）
4. 调整时间、颜色、相机路径
5. 优化：减少 draw call，使用 instancing，懒加载重资产
6. 构建：`npm run build` → `dist/` 可部署

## 代码模板

- Three.js 场景样板：[three-scene.js](templates/three-scene.js)
- GSAP 滚动动画：[gsap-scroll.js](templates/gsap-scroll.js)
- Lenis 平滑滚动：[lenis-setup.js](templates/lenis-setup.js)
- HTML 入口：[index.html](templates/index.html)
- 主入口：[main.js](templates/main.js)

## API 参考

详细 API 模式见 [reference.md](reference.md)。

## 质量清单

- [ ] 页面 3 秒内加载（懒加载 3D 资产）
- [ ] 中端设备 60fps（限制像素比，降低多边形数）
- [ ] 滚动丝滑流畅（Lenis + RAF）
- [ ] 动画在正确位置触发
- [ ] 移动端响应（触摸事件，降级特效）
- [ ] 音频需用户交互触发（autoplay 策略）
- [ ] 无控制台错误
- [ ] 构建无警告

## Vibe Coding 心法

- 先抓"氛围" — 设计的情感内核（动感？静谧？神秘？）
- 选 2-3 个核心特效，不过载
- 用超长章节 (200vh+) 制造戏剧性滚动序列
- Pin 章节聚焦动画时刻
- 配色：深色背景 + 1-2 个强调色
- 排版：大号粗体，SplitText 滚动揭示
- 相机移动创造深度 — 滚动推近、枢轴旋转
