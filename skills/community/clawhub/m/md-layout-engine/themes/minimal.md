---
name: minimal
display_name: 极简主题
---

<!-- 要求 -->
1. 全 P 标签架构 (代码块\表格除外)：全篇仅允许使用 `p` 标签嵌套在唯一的全局 `div` 内。
2. 有序列表和无序列表：转为代码块格式，清除列表样式和编号前缀。
3. 表格：(1)p 标签嵌入 span 标签;(2)table 标签 width 为 100%;(3)td 标签 width 为自动计算平均宽度;(4)td 标签里面的 p 标签 margin 为 4px auto;(5)表头 td 标签背景颜色为#f5f5f5，字体颜色为#212121。
4. em 标签：字体颜色为#616161。
5. 正文内容：字体大小为 16px，字体颜色为#525252，高亮颜色为#212121。


- 卡片容器：border-radius:14px; box-shadow:0 2px 12px rgba(0,0,0,0.08); color:#525252;
<!-- 标题 -->
- h1/h2/h3: color:#212121;
<!-- 链接 -->
- 链接 a: color:#424242;
<!-- 引用 -->
- 引用块 blockquote: border-left:4px solid #bdbdbd; background:#f5f5f5; margin:1em 0; padding: 1em 1em;
<!-- 代码块 -->
- 代码 pre, code: background:#f5f5f5;
- 水平线 hr: border-top:1px solid #e0e0e0;
- 表格 table: border:1px solid #e0e0e0;
<!-- 删除线 -->
- 删除线 s: text-decoration: line-through;
<!-- 任务列表 -->
- 任务列表 ul, ol: list-style-type: disc;
