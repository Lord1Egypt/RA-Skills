# 默认不自动播放

课件里的动图和淡入，一律等老师按一下才动。进帧即播会把节奏抢走：老师还在讲上一句，画面自己动了，回头没法复原。

这条是硬规则，不因页面"看起来更活"而放宽。

## 交互动图

进帧只摆静态初始状态：圆、定点、动点摆在起始位置，一条折痕都不画。之后靠两种方式启动。

- 按钮：`<button data-act="play">自动演示</button>`，再点一次暂停
- 直接拖：拖动动点本身

实现上，挂载函数不要监听 `frameenter` 去调 `start()`，也不要起 `requestAnimationFrame` 循环。播放状态只由按钮和拖拽切换。

```ts
// 错的：一进帧就动
document.addEventListener('frameenter', (e) => {
  if (e.target === frame) start()
})

// 对的：只挂按钮
playBtn?.addEventListener('click', () => (running ? stop() : start()))
```

需要自动演示的动图，顺带配一个"清空"，让老师可以重来一次。

## 淡入

帧内淡入不用自动串联，改成按 `PgDn` 一步一步放。

- 元素写 `data-enter="up"`，分步的再加 `data-step="2"`、`data-step="3"`
- 进帧只放第 1 步
- `PgDn` 若本帧还有没放的步骤，就先放下一步，放完才翻页
- `PgUp` 回上一帧时把那帧所有步骤一次放全，免得内容缺一半

引擎侧对应 `playEnter(frame, step)`、`stepsOf`、`hideLaterSteps`、`revealAll`。

## 出图

无头浏览器截图要看到"完整一页"，进场后先 `revealAll(frame)`，交互图再替老师点一下播放按钮，等动画跑够再截。
