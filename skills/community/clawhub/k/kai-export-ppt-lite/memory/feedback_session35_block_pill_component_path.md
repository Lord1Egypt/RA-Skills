# Session 35：block-level CTA pill 没走进胶囊组件路径

时间：2026-04-24

## 背景

Session 34 修掉了 centered wrapper packer 把 `_pair_with` 拆散的问题后，`data-story` 的胶囊确实比之前好，但用户继续指出：

- 胶囊“还是没做对”
- 之前在 `blue-sky` 和 `enterprise-dark` 里做对了
- 怀疑是不是胶囊组件设计器被改错了

## 结论

不是原来的胶囊组件路径整体被改坏了，而是：

- `blue-sky` / `enterprise-dark` 的胶囊大多是 `span`
- `data-story` 的大 CTA pill 是 `div.cta-pill`

旧逻辑只会把 `INLINE_TAGS` + visible bg/border + leaf text 识别成稳定的 pill-like component。

因此：

- `span.badge`
- `span.pill`
- `span.ent-pill`

都能走到：

- `forceSingleLine=True`
- `preferContentWidth=True`

但 `div.cta-pill` 之前没有走进去，虽然样式已经是典型胶囊：

- `display:inline-block`
- `padding: 12px 32px`
- `border-radius: 8px`
- 单行文本
- 有明显 background / border

## 本轮通用修复

在 `build_text_element()` 里扩展了 pill-like component 识别：

- 不再要求必须是 `INLINE_TAGS`
- 只要满足：
  - visible bg/border
  - leaf text container
  - `display:inline-block / inline-flex / flex`

就允许进入 `element_is_inline_box` / `shrink_wrap_inline` 路径

这样 block-level 但“视觉语义上是胶囊”的元素，也会走同一套稳定规则。

## 验证

新增测试：

- `test_build_text_element_block_cta_pill_uses_component_layout()`

它直接验证：

- block tag
- `display:inline-block`
- padding + border-radius + bg

仍然应该得到：

- `forceSingleLine=True`
- `preferContentWidth=True`

直接核对 `data-story` 的 `.cta-pill`：

- 修复前：
  - `forceSingleLine=False`
  - `preferContentWidth=False`
  - `bounds ≈ {w: 1.9111, h: 0.4888}`
- 修复后：
  - `forceSingleLine=True`
  - `preferContentWidth=True`
  - `bounds ≈ {w: 2.3778, h: 0.5184}`

## 不要再犯

1. 不要把“胶囊组件路径”默认等同于 `span`。
2. 对 block tag，如果它在视觉和 CSS 语义上就是 pill，也必须走同一条组件路径。
3. 以后再对比 `slide-creator` preset 时，先查：
   - tag 是什么
   - display 是什么
   - 是否 leaf text
   - 是否已经进入 `forceSingleLine + preferContentWidth`

## 当前影响

这轮主要增强的是：

- `data-story` 的 CTA pill
- 以及未来其他 `div` / `p` / block wrapper 形式的单行胶囊

这属于通用 pill component path 扩展，不是 `data-story` 特判。
