# 帧内平移：先加速、后减速

此预设只处理**同一帧里已经显示的元素改变位置**，不负责入场淡入，也不替代跨帧 `data-k` morph。

```html
<div data-move-step="2" data-move-x="754" data-move-y="0" data-move-duration="650">
  始终可见的对象
</div>
```

- `data-move-step="2"`：这一帧进入时对象停在原处；教师按 PgDn 到第 2 步才启动平移。若有入场元素也用 `data-step="2"`，两者同一次按键触发。
- `data-move-x`、`data-move-y`：相对原始位置的目标位移，单位 px，可取负值，默认 0。
- `data-move-duration`：持续时间，默认 650ms。位移采用 `cubic-bezier(.4,0,.2,1)`，从静止加速再减速停止。
- 动画不改透明度：对象从头到尾都可见，不是“平移入场”。
- `prefers-reduced-motion: reduce` 时直接到终点；PgUp 从下一帧回看本帧时直接显示终态。

完整示例在 `templates/basic/frames/04-translate.html`，运行 `bun run build`，先导航到“帧内平移”，再按 PgDn。不要在有 `data-k` morph、已经有自定义 `transform` 的同一个元素上直接复用本预设；可给元素包一层容器，把不同动画放到不同层。
