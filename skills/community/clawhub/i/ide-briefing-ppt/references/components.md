# Components

只使用模板 `<style>` 里已经定义的 class。下面是原 PPT 的用法，不是新皮肤。

颜色语义已经写进模板：琥珀只做主强调，青色表示链接或成功，绿色表示新建，蓝色表示输出，紫色表示更新，红色表示输入或警告。状态色不能升级成第二套品牌色，也不要手写新的色值。

## Chrome

| 元素 | 作用 | 可改？ |
|---|---|---|
| `#bar` | 顶部 3px 琥珀进度条 | 不改结构 |
| `#stage` / `#deck` | 1280×720 缩放舞台 | 不改尺寸 |
| `#counter` | `1 / N · 标题` | 由 JS 写 |
| `#hint` | 左下快捷键 | 文案可留原句 |
| `#notes` | `N` 键讲稿层 | 每页写 `aside.notes` |
| `.foot` | 页内左右页脚 | 只改文字 |

每页：

```html
<aside class="notes">这一页台上要补的话。</aside>
```

## Text

- `.kicker`：英文大写 + 等宽 + 琥珀。封面和章节页都要有。
- `h1` / `h2` / `h3`：不要改成别的标题标签来「变小」。
- `.sub`：标题下的一行解释。
- `.small`：面板里的说明。
- `.mono`：需要等宽的短词。
- `.tag`：胶囊标签。分层时用 `.tag.raw` / `.wiki` / `.out`。

## Panel / callout / points

```html
<div class="panel">...</div>
<div class="panel tight">更紧的内边距</div>
<div class="callout">琥珀结论</div>
<div class="callout teal">青色结论</div>
<ul class="pts">
  <li><span class="n">1</span><span><b>标题：</b>说明。</span></li>
</ul>
```

一页最多一个 callout。`.pts` 最多 4 条。

## Terminal

```html
<div class="term">
  <span class="fname">path/file.md</span>
  <div class="body">
    <span class="h1">标题</span><span class="hr"></span>
    普通文本 <span class="lk">[[链接]]</span> <span class="em">强调</span>
    <span class="cm">注释</span>
    <div class="p">$ command</div>
    <div class="o">output</div>
  </div>
</div>
```

三色灯是 `::before` 画的，不要自己加圆点。

## File tree

必须保留 SVG sprite（`#i-folder` / `#i-file`）。树行 class：

- `.nm.hl` 当前文件
- `.nm.rawc` / `.wikic` / `.outc` 分层着色
- `.desc` 右侧说明
- `.cnt` 数量胶囊

## Conversation / steps / glossary

- `.pcard.on` + `.u` / `.a`：`你 ›` 和 `AI ›` 由 CSS 自动加前缀，正文里不要再写。
- `.steps` 横排，`.steps.v` 竖排。序号由 `counter` 画琥珀方块。
- `.glossary .g`：两列名词卡，`<b>` 是等宽词条。
- `.two` + `.who`：收束页左右职责。左边琥珀边，右边青绿边，和原 PPT 一致。

## Graph / tree / log（高级）

这些 CSS 已经在模板里，需要时直接用，不要重写：

- `svg.mg`：中心节点 `.c`，四周 `.n.on`，连线 `line.on`
- `svg.tree`：配合模板里的 `renderTree()`
- `.log` + `.ln.think/.read/.write/.rule/.ans`
- `.meter` 上下文用量条
- `.bigno` 大号数字
- `.lanes` / `.lane` 并发进度
- `.loop` 闭环节点
- `.git` / `.mr` Git 示意

没有过程动画需求时，优先用静态面板，不要为了「看起来炫」强上 SVG。
