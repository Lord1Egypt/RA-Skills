# 样式与动画

文档: https://docs.masastack.com/blazor/styles-and-animations/

## Border Radius (圆角)

文档: https://docs.masastack.com/blazor/styles-and-animations/border-radius

```razor
<!-- 基础圆角 -->
<div class="rounded">圆角</div>
<div class="rounded-sm">小圆角</div>
<div class="rounded-lg">大圆角</div>
<div class="rounded-xl">超大圆角</div>
<div class="rounded-pill">胶囊圆角</div>
<div class="rounded-circle">圆形</div>
<div class="rounded-0">无圆角</div>

<!-- 单边圆角 -->
<div class="rounded-t">顶部圆角</div>
<div class="rounded-r">右侧圆角</div>
<div class="rounded-b">底部圆角</div>
<div class="rounded-l">左侧圆角</div>
```

## Elevation (阴影)

文档: https://docs.masastack.com/blazor/styles-and-animations/elevation

```razor
<div class="elevation-0">无阴影</div>
<div class="elevation-1">阴影1</div>
<div class="elevation-2">阴影2</div>
<div class="elevation-4">阴影4</div>
<div class="elevation-8">阴影8</div>
<div class="elevation-12">阴影12</div>
<div class="elevation-24">阴影24</div>
```

组件参数:
```razor
<MCard Elevation="4">阴影卡片</MCard>
```

## Flex (弹性布局)

文档: https://docs.masastack.com/blazor/styles-and-animations/flex

```razor
<!-- Flex容器 -->
<div class="d-flex">
    <div>Flex Item</div>
</div>

<!-- 方向 -->
<div class="d-flex flex-row">水平</div>
<div class="d-flex flex-column">垂直</div>
<div class="d-flex flex-row-reverse">水平反向</div>

<!-- 对齐 -->
<div class="d-flex justify-start">左对齐</div>
<div class="d-flex justify-center">居中</div>
<div class="d-flex justify-end">右对齐</div>
<div class="d-flex justify-space-between">两端对齐</div>
<div class="d-flex justify-space-around">等距分布</div>

<!-- 交叉轴对齐 -->
<div class="d-flex align-start">顶部</div>
<div class="d-flex align-center">垂直居中</div>
<div class="d-flex align-end">底部</div>

<!-- 换行 -->
<div class="d-flex flex-wrap">自动换行</div>

<!-- flex-grow/shrink -->
<div class="flex-grow-1">填充剩余空间</div>
<div class="flex-grow-0">不填充</div>
```

## Spacing (间距)

文档: https://docs.masastack.com/blazor/styles-and-animations/spacing

格式: `{property}{direction}-{size}`

- **property**: m(margin), p(padding)
- **direction**: t(top), b(bottom), l(left), r(right), x(left+right), y(top+bottom), a(all)
- **size**: 0-16 (4px为单位)

```razor
<!-- Margin -->
<div class="ma-0">无边距</div>
<div class="ma-2">8px边距</div>
<div class="ma-4">16px边距</div>
<div class="mx-auto">水平居中</div>
<div class="mt-4">顶部16px</div>
<div class="mb-4">底部16px</div>
<div class="ml-4">左侧16px</div>
<div class="mr-4">右侧16px</div>

<!-- Padding -->
<div class="pa-0">无内边距</div>
<div class="pa-2">8px内边距</div>
<div class="pa-4">16px内边距</div>
<div class="px-4">左右16px</div>
<div class="py-4">上下16px</div>

<!-- 负边距 -->
<div class="mt-n4">负顶部边距</div>
```

## Display (显示控制)

文档: https://docs.masastack.com/blazor/styles-and-animations/display-helpers

```razor
<!-- Display -->
<div class="d-none">隐藏</div>
<div class="d-inline">行内</div>
<div class="d-inline-block">行内块</div>
<div class="d-block">块级</div>
<div class="d-flex">Flex容器</div>
<div class="d-table">表格</div>

<!-- 响应式显示 -->
<div class="d-none d-md-flex">md以上显示</div>
<div class="d-flex d-md-none">md以下显示</div>

<!-- 可见性 -->
<div class="visible">可见</div>
<div class="invisible">不可见(占位)</div>

<!-- 溢出 -->
<div class="overflow-auto">自动溢出</div>
<div class="overflow-hidden">隐藏溢出</div>
<div class="overflow-visible">显示溢出</div>
```

## Text & Typography (文字排版)

文档: https://docs.masastack.com/blazor/styles-and-animations/text-and-typography

```razor
<!-- 文本对齐 -->
<p class="text-left">左对齐</p>
<p class="text-center">居中</p>
<p class="text-right">右对齐</p>

<!-- 文本装饰 -->
<p class="text-decoration-none">无装饰</p>
<p class="text-decoration-underline">下划线</p>
<p class="text-decoration-overline">上划线</p>
<p class="text-decoration-line-through">删除线</p>

<!-- 文本转换 -->
<p class="text-lowercase">lowercase</p>
<p class="text-uppercase">uppercase</p>
<p class="text-capitalize">capitalize</p>

<!-- 字体粗细 -->
<p class="font-weight-thin">Thin 100</p>
<p class="font-weight-light">Light 300</p>
<p class="font-weight-regular">Regular 400</p>
<p class="font-weight-medium">Medium 500</p>
<p class="font-weight-bold">Bold 700</p>
<p class="font-weight-black">Black 900</p>

<!-- 字体斜体 -->
<p class="font-italic">斜体</p>

<!-- 文本溢出 -->
<p class="text-truncate">这是一段很长的文本会被截断...</p>

<!-- 标题类 -->
<h1 class="text-h1">H1</h1>
<h2 class="text-h2">H2</h2>
<h3 class="text-h3">H3</h3>
<h4 class="text-h4">H4</h4>
<h5 class="text-h5">H5</h5>
<h6 class="text-h6">H6</h6>
<p class="subtitle-1">Subtitle 1</p>
<p class="subtitle-2">Subtitle 2</p>
<p class="body-1">Body 1</p>
<p class="body-2">Body 2</p>
<p class="caption">Caption</p>
<p class="overline">Overline</p>
```

## Transitions (过渡动画)

文档: https://docs.masastack.com/blazor/styles-and-animations/transitions

```razor
<!-- 预设动画 -->
<MButton OnClick="() => _show = !_show">切换</MButton>

<!-- Fade 淡入淡出 -->
<MTransition>
    <div Show="@_show">淡入淡出</div>
</MTransition>

<!-- Scale 缩放 -->
<MDialog Transition="dialog-transition">
    ...
</MDialog>

<!-- Slide 滑动 -->
<MNavigationDrawer Transition="scroll-x-transition">
    ...
</MNavigationDrawer>

<!-- Scroll 滚动 -->
<MScrollXTransition>
    <div Show="@_show">滚动</div>
</MScrollXTransition>
```

预设动画类:
- `fade-transition` - 淡入淡出
- `scale-transition` - 缩放
- `scroll-x-transition` - 水平滚动
- `scroll-y-transition` - 垂直滚动
- `slide-x-transition` - 水平滑动
- `slide-y-transition` - 垂直滑动
- `expand-transition` - 展开
- `fab-transition` - 浮动按钮动画
