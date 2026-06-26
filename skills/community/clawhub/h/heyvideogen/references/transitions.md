# Scene Transitions — Heyvideogen

> 摘自 [hyperframes references/transitions.md](https://github.com/heygen-com/hyperframes)

## 核心规则

多场景合成 **必须使用转场**，禁止跳切。

| 规则 | 说明 |
|------|------|
| 内容元素 | 禁止在非最后场景做 `gsap.to` 退出动画，转场本身就是 exit |
| Video Clip | 用 wrapper div 包裹，动画 wrapper 的 opacity 实现转场淡出 |
| 最后场景 | 允许 `gsap.to(..., { opacity: 0 })` 整体淡出 |

## 转场类型

| 类型 | 适用场景 | 实现方式 |
|------|---------|---------|
| 淡入淡出 | 通用，默认 | GSAP opacity（wrapper） |
| 滑入 | 节奏感强 | GSAP x + overflow:hidden |
| 溶解 | 柔和过渡 | GSAP opacity + scale |
| 推送 | 强方向感 | GSAP x + overflow:hidden |
| Shader | 电影感 | @hyperframes/shader-transitions |

## HTML 结构规范（必须）

Video clip 必须包 wrapper，绝不可直接动画 `<video>` 元素：

```html
<!-- ✅ 正确：video + wrapper -->
<div id="clip-1-wrapper" style="position:absolute;inset:0;overflow:hidden;">
  <video id="clip-1"
    data-start="0" data-duration="5" data-track-index="0"
    src="clips/clip_01.mp4" muted playsinline
    style="width:100%;height:100%;object-fit:cover;">
  </video>
</div>
```

## 淡入淡出（最常用）

```js
// 场景1（5秒）→ 场景2（接续）
// 场景1 wrapper 淡出（最后 0.5s）
tl.to("#clip-1-wrapper", { opacity: 0, duration: 0.5 }, 4.5);

// 场景2 从 opacity:0 开始淡入
tl.from("#clip-2-wrapper", { opacity: 0, duration: 0.5 }, 5.0);
// 内容同步入场
tl.from("#s2-title", { y: 30, opacity: 0, duration: 0.5 }, 5.1);
```

## 滑入（方向感强）

```js
// 场景2 从右侧滑入
tl.from("#clip-2-wrapper", { x: 1080, opacity: 0, duration: 0.6, ease: "power3.out" }, 5.0);
tl.from("#s2-title", { x: 1080, opacity: 0, duration: 0.5, ease: "power3.out" }, 5.2);
```

## CSS Scale 溶解（柔和）

```js
// 场景1 缩放+透明
tl.to("#clip-1-wrapper", { scale: 1.05, opacity: 0, duration: 0.6 }, 4.4);
// 场景2 缩放进入
tl.from("#clip-2-wrapper", { scale: 0.95, opacity: 0, duration: 0.6 }, 5.0);
```

## 完整两场景模板（含正确 wrapper 结构）

```html
<!-- 完整结构示例 -->
<div id="main" data-composition-id="main" data-start="0" data-width="1080" data-height="1920">

  <!-- 场景1：5秒 -->
  <div id="clip-1-wrapper" style="position:absolute;inset:0;overflow:hidden;">
    <video id="clip-1" data-start="0" data-duration="5" data-track-index="0"
      src="clips/clip_01.mp4" muted playsinline
      style="width:100%;height:100%;object-fit:cover;"></video>
  </div>
  <div id="s1-title" data-start="0.3" data-duration="4.5"
    data-track-index="1" style="position:absolute;top:200px;left:60px;font-size:80px;color:#fff;">
    标题一
  </div>

  <!-- 场景2：接续 -->
  <div id="clip-2-wrapper" style="position:absolute;inset:0;overflow:hidden;opacity:0;">
    <video id="clip-2" data-start="5" data-duration="10" data-track-index="0"
      src="clips/clip_02.mp4" muted playsinline
      style="width:100%;height:100%;object-fit:cover;"></video>
  </div>
  <div id="s2-title" data-start="5.3" data-duration="9.5"
    data-track-index="1" style="position:absolute;top:200px;left:60px;font-size:80px;color:#fff;opacity:0;">
    标题二
  </div>

</div>
```

```js
const tl = gsap.timeline({ paused: true });
const TOTAL = 57;

// ========== 场景1 入场 ==========
tl.from("#s1-title", { y: 60, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.3);

// ========== 场景1→2 转场 ==========
// clip-1 淡出（最后 0.5s）→ 动画 wrapper
tl.to("#clip-1-wrapper", { opacity: 0, duration: 0.5 }, 4.5);

// ========== 场景2 ==========
// clip-2 淡入
tl.to("#clip-2-wrapper", { opacity: 1, duration: 0.5 }, 5.0);
// 内容入场
tl.from("#s2-title", { y: 40, opacity: 0, duration: 0.6, ease: "expo.out" }, 5.3);
tl.from("#s2-points", { y: 30, opacity: 0, duration: 0.5, stagger: 0.15 }, 5.5);

// ========== 延长 timeline ==========
tl.set({}, {}, TOTAL);

window.__timelines["main"] = tl;
```

## ⚠️ 常见错误

| 错误 | 正确做法 |
|------|---------|
| `tl.to("#clip-1", { opacity: 0 })` 直接动画 video | 包 wrapper，动画 wrapper |
| 场景1 内容做 `gsap.to` 退出 | 不做 exit，内容随 clip 一起被 unmount |
| `repeat: -1` 循环 | `repeat: Math.ceil(total/single) - 1` |
| 最后场景不做任何动画 | 允许整体 fade to black |

## Shader 转场（进阶）

需要 `@hyperframes/shader-transitions` 包，适合电影感强的高级制作。
