# Captions & Subtitles — Heyvideogen

> 摘自 [hyperframes references/captions.md](https://github.com/heygen-com/hyperframes)

## 基础字幕

```html
<div id="cap-1"
  data-start="0.5"
  data-duration="3.8"
  data-track-index="1"
  class="caption">
  这是第一句台词
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
}
```

```js
tl.from("#cap-1", { opacity: 0, y: 16, duration: 0.4 }, 0.3);
tl.to("#cap-1", { opacity: 0, duration: 0.3 }, 3.8);
```

## 卡拉OK字幕（逐字高亮）

适用于 TTS 配音，需要词级别同步。

```html
<div id="karaoke-1" data-start="0.5" data-duration="4.5" data-track-index="1">
  <span class="kword" data-start="0.00" data-end="0.35">这句</span>
  <span class="kword" data-start="0.35" data-end="0.70">歌词</span>
  <span class="kword" data-start="0.70" data-end="1.10">需要</span>
  <span class="kword" data-start="1.10" data-end="1.50">逐字</span>
  <span class="kword" data-start="1.50" data-end="2.00">高亮</span>
</div>
```

```css
.kword {
  display: inline-block;
  color: #8E8E93;
  transition: color 0.1s;
}
.kword.active {
  color: #fff;
}
```

```js
// GSAP timeline 用 opacity 控制逐字
words.forEach((word, i) => {
  const s = parseFloat(word.dataset.start);
  const e = parseFloat(word.dataset.end);
  tl.from(word, { color: "#8E8E93" }, s + 0.5);
  tl.to(word,   { color: "#007AFF" },  s + 0.5);
});
```

## 下划线/高亮字幕

```css
.caption-highlight {
  background: linear-gradient(transparent 60%, rgba(0,122,255,0.3) 60%);
}
```

## 字幕转场

```js
// 淡出前一字幕 → 淡入后一字幕（留 0.2s 间隙）
tl.to("#cap-1", { opacity: 0, y: -8, duration: 0.25 }, 3.5);
tl.from("#cap-2", { opacity: 0, y: 16, duration: 0.35 }, 3.7);
```

## 底部安全区

字幕 `bottom` 值建议 **160-220px**（竖屏 1080×1920），确保在系统 UI 下方可见。
