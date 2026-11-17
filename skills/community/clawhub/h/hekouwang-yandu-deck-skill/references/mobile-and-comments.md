# 移动端 safe-area · 留言板开关 · 视频交叉引用

## 移动端 safe-area

演示引擎默认 `viewport-fit=cover`，全屏翻页时顶底栏要留 **safe-area**：

```css
.deck-toolbar {
  padding-bottom: max(12px, env(safe-area-inset-bottom));
  padding-left: max(16px, env(safe-area-inset-left));
  padding-right: max(16px, env(safe-area-inset-right));
}
```

- iOS 刘海/底条：没写 `env(safe-area-inset-*)` 时，翻页按钮和进度条会被挡。
- 横屏演示：左右 inset 同样要留，别只照顾 bottom。
- 验收：真机 Safari「添加到主屏幕」全屏翻 3 页，拇指区按钮必须可点。

## 留言板（可选子系统）

默认 **hekouwang.pages.dev 线上开着**；新站或纯静态演示可关：

1. 删或移走 `演读DECK/functions/`（Pages Functions 不再挂载）
2. `wrangler.toml` 里去掉 `[[d1_databases]]` 绑定
3. `home.html` / 引擎模板里去掉留言入口 DOM 与 fetch 调用

排错见 `references/留言板-D1.md`；**database_id 必须是自己的**，副本里是占位符。

## 与 HyperFrames 视频产线

- **演读 DECK** = 一屏一镜 **可翻页 HTML**，适合长文拆解、国标系列、教程跟读。
- **HyperFrames 视频** = 同选题的 **ffmpeg 成片**（harness 内 `EP-*/video/` 或动画 Skill）。
- 同一 EP 可两条线并存：文章母本 → 演示版 HTML（本 skill）+ 可选视频目录；**不要**在 deck 引擎里引外链视频或 `Date.now()`/`Math.random()`（与 harness `AGENTS.md` 视频红线一致）。
