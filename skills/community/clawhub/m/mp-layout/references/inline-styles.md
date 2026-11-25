# 公众号内联样式表

公众号编辑器会剥离 `<style>`、`class`、`id` 与 `<script>`，只保留元素上的 `style=""`。下表是 `scripts/md2mp.py` 使用的样式，手写时照抄。`{C}` 替换为品牌色 HEX。

| 元素 | 内联样式 |
|---|---|
| 外层容器 `<section>` | `padding: 0 16px; font-size: 16px; line-height: 1.75; letter-spacing: 1px; color: #3A3A3A; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;` |
| 段落 `<p>` | `margin: 0 0 1.2em; text-align: left;` |
| H2 `<h2>` | `font-size: 20px; font-weight: 700; color: {C}; margin: 2em 0 1em; line-height: 1.4; letter-spacing: 1px;` |
| H2 前的品牌符号 `<span>` | `display: inline-block; width: 6px; height: 20px; background: {C}; border-radius: 3px; vertical-align: -3px; margin-right: 10px;` |
| H3 `<h3>` | `font-size: 17px; font-weight: 700; color: #3A3A3A; margin: 1.6em 0 0.8em; line-height: 1.5;` |
| 重点 `<strong>` | `color: {C}; font-weight: 700;` |
| 强调 `<em>` | `font-style: normal; border-bottom: 2px solid {C}; padding-bottom: 1px;` |
| 引用 `<blockquote>` | `margin: 1.5em 0; padding: 0.2em 0 0.2em 14px; border-left: 3px solid {C}; color: #8A8A8A; font-size: 15px;` |
| 无序列表 `<ul>` / 有序 `<ol>` | `margin: 0 0 1.2em; padding-left: 1.4em;`；`<li>`：`margin: 0.3em 0;` |
| 图片 `<img>` | `display: block; width: 100%; border-radius: 6px; margin: 1.6em auto 0.5em;` |
| 图片说明 `<p>` | `text-align: center; font-size: 13px; color: #8A8A8A; margin: 0 0 1.6em; letter-spacing: 0;` |
| 分隔线 `<p>` | `text-align: center; color: {C}; margin: 2em 0; letter-spacing: 8px;` 内容为 `· · ·` |
| 脚注区 `<p>` | `font-size: 13px; color: #8A8A8A; margin: 2em 0 0; word-break: break-all;` |
| 结尾行动 `<p>` | 与正文相同，最后一句用 `<strong>` |

三色约束：`#3A3A3A`（正文）、`{C}`（品牌色）、`#8A8A8A`（辅助）。不要再引入第四个颜色。
