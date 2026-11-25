# 帧内入场动画

原则：先排整帧的版面，再给需要强调的元素安排入场顺序。动画只补充节奏，不承担信息结构。

## 用法

```html
<p class="bullet" data-enter="up">第一条</p>
<p class="bullet" data-enter="up" data-enter-delay="90">第二条</p>
<p class="bullet" data-enter="up" data-enter-delay="180">第三条</p>
```

| 属性 | 取值 | 默认 |
| --- | --- | --- |
| `data-enter` | `up` `down` `left` `right` `fade` | `up` |
| `data-enter-delay` | 毫秒 | 按 DOM 顺序，每条加 70 |
| `data-enter-duration` | 毫秒 | 420 |

不写 `data-enter-delay` 时自动错峰；写死数字会覆盖自动值。元素初始不可见由动画的 `fill: both` 保证，JS 失效时元素仍然可见。

## 分步与触发

淡入不自动串联，交给 PgDn 一步一步放：

```html
<p class="lead" data-enter="up">第一层，进帧就有</p>
<p class="lead" data-enter="up" data-step="2" data-enter-delay="60">第二层，按 PgDn 才出</p>
```

| 动作 | 结果 |
| --- | --- |
| 翻到某帧 | 只放 `data-step="1"` 的元素 |
| PgDn | 本帧还有未放的步骤就先放，放完才翻页 |
| PgUp | 回到上一帧，并把那帧所有步骤一次放全 |

翻页仍只认 PgUp/PgDn、方向键、空格与缩略图点击。

## 与 morph 的分工

- `data-k` 管跨帧共享元素，做位移、缩放与交叉淡化
- `data-enter` 管帧内入场，做淡入与位移
- 同一个元素不要同时用，两个动画都写 `transform`，会打架
- 含 `[data-enter]` 的帧直接子元素，morph 不再做整体淡入，避免透明度叠加

## 设计顺序

1. 先定版面：标题、图、要点的位置与大小
2. 再定阅读顺序：哪些先出现，哪些后出现
3. 最后加 `data-enter` 与延迟
4. 用 PgDn 走一遍，每帧停半秒看节奏；延迟总量控制在 300ms 以内，不让人等

## 减少动态

`prefers-reduced-motion: reduce` 时直接显示，不播动画。
