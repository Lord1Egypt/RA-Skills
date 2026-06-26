# GSAP Animation Rules — Heyvideogen

## 核心原则

- **只动画视觉属性**：`opacity`, `x`, `y`, `scale`, `rotation`, `color`, `backgroundColor`, `borderRadius`, `transform`
- **禁止动画**：`visibility`, `display`；**禁止直接动画 `<video>` 元素本身**（会导致帧停止更新），用 wrapper div 包裹再动画
- **同步构建**：所有 timeline 在 `<script>` 顶层同步构建，不在 `async`/`setTimeout`/`Promise` 里
- **`repeat: -1` 禁止**：`repeat: Math.ceil(duration / cycle) - 1` 计算有限次数

## Timeline 结构模板

```js
const tl = gsap.timeline({ paused: true });

// 场景入场
tl.from("#scene-title",    { y: 60, opacity: 0, duration: 0.6, ease: "power3.out" }, sceneStart + 0.2);
tl.from("#scene-subtitle", { y: 40, opacity: 0, duration: 0.5, ease: "power2.out" }, sceneStart + 0.4);
tl.from("#scene-tag",      { scale: 0.8, opacity: 0, duration: 0.4, ease: "back.out(1.7)" }, sceneStart + 0.3);

// 场景内循环动画（呼吸/脉冲）— 必须用有限次数
const breatheCycles = Math.ceil(sceneDuration / 3) - 1;
tl.from("#bg-glow", {
  scale: 1.02, opacity: 0.3, duration: 1.5, ease: "sine.inOut",
  repeat: breatheCycles, yoyo: true
}, sceneStart + 0.5);

// 延长 timeline（防止被截断）
tl.set({}, {}, sceneStart + sceneDuration);

window.__timelines["main"] = tl;
```

## 动画 Guardrails

| 参数 | 推荐值 | 禁止 |
|------|-------|------|
| 首个动画偏移 | 0.1-0.3s（不用 t=0） | t=0 |
| ease 种类 | 每场景至少 3 种不同 ease | 全用同一种 |
| 动画时长 | 0.3–0.7s | < 0.2s 或 > 1.5s |
| stagger | 每元素 delay 18-20 帧 | < 12 帧 |
| 呼吸动画 scale | ±1.5-3% | ±5% 以上 |

## Video Clip 的转场淡出（必须用 Wrapper）

```html
<!-- 错误：直接动画 video 元素 -->
<video id="clip-1" ...></video>
<script>
  tl.to("#clip-1", { opacity: 0, duration: 0.5 }, 4.5); // BANNED
</script>

<!-- 正确：包一层 wrapper，动画 wrapper -->
<div style="position:absolute;inset:0;">
  <video id="clip-1" ...></video>
</div>
<script>
  // wrapper-overlay 在 clip 结束前淡出，实现平滑转场
  tl.to("#clip-1-wrapper", { opacity: 0, duration: 0.5 }, 4.5);
</script>
```

## Apple 风格动画公式

```js
// fade-up（主标题）
tl.from("#title", { y: 30, opacity: 0, duration: 0.5, ease: "power3.out" }, start + 0.2);

// scale（节点出现）
tl.from("#node", { scale: 0.4, opacity: 0, duration: 0.5, ease: "back.out(1.7)" }, start + 0.3);

// translateX（列表依次出现）
tl.from(".list-item", { x: -24, opacity: 0, duration: 0.4, stagger: 0.18 }, start + 0.4);
```

## 字幕动画

```js
// 标准字幕淡入淡出
tl.from("#cap-1", { opacity: 0, y: 16, duration: 0.4 }, start + 0.2);
tl.to("#cap-1",   { opacity: 0, duration: 0.3 }, end - 0.3);

// 卡拉OK效果（逐字）→ 见 references/captions.md
```

## 数字/图表动画

```js
// 数字递增（需配合 FitText 或 Auto-Fit）
tl.from("#stat-number", { textContent: 0, duration: 1.2, ease: "power2.out" }, start + 0.5);

// 卡片堆叠入场
tl.from(".card", { y: 60, opacity: 0, duration: 0.5, stagger: 0.15 }, start + 0.3);
```

## 装饰元素（背景层）

```js
// 径向光晕呼吸（正确：有限次数）
const glowCycles = Math.ceil(totalDuration / 2.5) - 1;
tl.from("#glow", {
  scale: 1.02, opacity: 0.25, duration: 2.5,
  repeat: glowCycles, yoyo: true, ease: "sine.inOut"
}, start);

// 缓慢漂移（正确：有限次数）
const driftCycles = Math.ceil(totalDuration / 8) - 1;
tl.from("#ghost-text", {
  x: -20, y: -10, duration: 8,
  repeat: driftCycles, yoyo: true, ease: "sine.inOut"
}, start);
```
