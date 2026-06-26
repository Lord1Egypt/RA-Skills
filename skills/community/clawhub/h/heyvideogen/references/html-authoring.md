# HyperFrames HTML Authoring — Heyvideogen Reference

> 摘自 [heygen-com/hyperframes skills/hyperframes/SKILL.md](https://github.com/heygen-com/hyperframes)
> 仅保留 heyvideogen 流水线中最常用的规则。

## 视觉身份门控（HARD-GATE）

**写任何 HTML 之前，必须先确定视觉规范。**

按顺序检查：
1. `DESIGN.md` 存在 → 读它，用它的颜色/字体/规则
2. `visual-style.md` 存在 → 读它，应用 `style_prompt_full`
3. 用户指定了风格名称 → 读 `../hyperframes/visual-styles.md` 的 8 个预设
4. 都没有 → 先问 3 个问题再写代码：
   - 氛围？（ explosively / cinematic / fluid / technical / warm）
   - 亮色还是暗色画布？
   - 有无品牌色/字体？

## 布局优先于动画

**先写静态 CSS，再加 GSAP 动画。**

```css
/* ✅ 正确：flex 布局，内容区填充 */
.scene-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 120px 80px;
  gap: 24px;
  box-sizing: border-box;
}

/* ❌ 错误：绝对定位的内容容器 */
.scene-content {
  position: absolute;
  top: 200px;
  left: 160px;
  width: 1920px;
}
```

## Data Attributes

### 必须属性

| 属性 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 唯一标识符 |
| `data-start` | 是 | 开始时间（秒）或 clip ID 引用（`"clip-1 + 2"`） |
| `data-track-index` | 是 | 轨道索引，同轨道不能重叠 |
| `data-duration` | 视频/音频除外 | 持续秒数 |

### 视频元素

```html
<video
  id="clip-1"
  data-start="0"
  data-duration="5"
  data-track-index="0"
  src="clips/clip_01.mp4"
  muted playsinline>
</video>
<audio
  id="vo"
  data-start="0"
  data-duration="57"
  data-track-index="2"
  data-volume="1"
  src="voiceover.mp3">
</audio>
```

**⚠️ 必须 `muted playsinline`** — 未静音的视频在渲染时会出错。

## 合成结构

### 主文件（index.html）

```html
<div id="main"
  data-composition-id="main"
  data-start="0"
  data-width="1080"
  data-height="1920">
  <!-- clips -->
</div>
```

**不要用 `<template>` 包裹主合成** — 主文件直接写 `<div>`。

### 子合成（compositions/*.html）

```html
<template id="scene-01-template">
  <div data-composition-id="scene-01" data-width="1080" data-height="1920">
    <div class="content">...</div>
    <style>...</style>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.from(".content", { opacity: 0, y: 30, duration: 0.6 });
      window.__timelines["scene-01"] = tl;
    </script>
  </div>
</template>
```

### 加载子合成

```html
<div id="scene-01-load"
  data-composition-id="scene-01"
  data-composition-src="compositions/scene-01.html"
  data-start="0"
  data-duration="10"
  data-track-index="1">
</div>
```

## GSAP Timeline 规范

### 注册规则

```js
window.__timelines["main"] = tl;  // 必须
```

### 必禁止规则

| 禁止 | 正确做法 |
|------|---------|
| `Math.random()` | 用 seeded PRNG |
| `repeat: -1` | 算好次数：`repeat: Math.ceil(dur/cycle) - 1` |
| 动画 `visibility`/`display` | 用 `opacity` |
| 调用 `video.play()` | 框架自己管 |
| 在 `async`/`setTimeout` 里建 timeline | 同步构建 |

### 扩展 Timeline 长度

如果视频要长过最后一个 tween：
```js
tl.set({}, {}, 283); // 在 283 秒处添加空操作点
```

## 场景转场规则

多场景必须遵循：

1. **必须用转场** — 不允许跳切
2. **必须用入场动画** — 每个元素 `gsap.from()` 淡入
3. **禁止在非最后场景做退出动画** — 转场本身就是 exit
4. **仅最后场景** — 允许 `gsap.to(..., { opacity: 0 })` 淡出

```js
// ✅ 正确：入场 + 转场处理 exit
tl.from("#s2-title", { y: 40, opacity: 0, duration: 0.5 }, 5.3);
// 不需要 to — 转场淡出 clip 自己

// ❌ 错误：场景1 退出动画
tl.to("#s1-title", { opacity: 0, y: -40 }, 6.5); // BANNED
```

## 字幕规范

```html
<div id="cap-1"
  data-start="0.3"
  data-duration="3.5"
  data-track-index="1"
  class="caption">
  这是字幕文字
</div>
```

```css
.caption {
  position: absolute;
  bottom: 200px;
  left: 60px;
  right: 60px;
  font-size: 56px;
  font-weight: 600;
  color: #fff;
  text-align: center;
  text-shadow: 0 4px 20px rgba(0,0,0,0.8);
  font-family: "Inter", "Noto Sans SC", sans-serif;
  line-height: 1.4;
}
```

## 竖屏安全区（9:16 1080×1920）

```
┌────────────────────────────────┐
│ ██ 顶部 UI 遮挡区 (~120px) ██  │
├────────────────────────────────┤
│  top: 8%   页面大标题            │
│                                  │
│  top: 24%  主体内容（图表/卡片）   │
│                                  │
│  bottom: 10% 标签组/字幕          │
├────────────────────────────────┤
│ ██ 底部 UI 遮挡区 (~100px) ██  │
└────────────────────────────────┘
```

所有内容不得超出安全区。字幕放 `bottom: 160-200px`。

## 质量检查

```bash
npx hyperframes lint
npx hyperframes validate
```

对比度：WCAG AA（正文 4.5:1，大字 3:1）。`hyperframes validate` 自动检查。
