# MButton 按钮

文档: https://docs.masastack.com/blazor/ui-components/buttons

## 基础用法
```razor
<MButton Color="primary">Primary</MButton>
<MButton Color="secondary">Secondary</MButton>
<MButton Color="success">Success</MButton>
<MButton Color="error">Error</MButton>
<MButton Color="warning">Warning</MButton>
<MButton Color="info">Info</MButton>
```

## 按钮样式
```razor
<!-- 凸起按钮(默认) -->
<MButton Color="primary">Raised</MButton>

<!-- 平面按钮 -->
<MButton Color="primary" Depressed>Depressed</MButton>

<!-- 描边按钮 -->
<MButton Color="primary" Outlined>Outlined</MButton>

<!-- 纯文本按钮 -->
<MButton Color="primary" Text>Text</MButton>

<!-- 块级按钮 -->
<MButton Color="primary" Block>Block</MButton>
```

## 图标按钮
```razor
<MButton Icon Color="primary">
    <MIcon>mdi-thumb-up</MIcon>
</MButton>

<!-- 带图标的按钮 -->
<MButton Color="primary">
    <MIcon Left>mdi-cloud-upload</MIcon>
    Upload
</MButton>
```

## 浮动按钮(FAB)
```razor
<MButton Fab Color="primary">
    <MIcon>mdi-plus</MIcon>
</MButton>

<MButton Fab Small Color="primary">
    <MIcon>mdi-pencil</MIcon>
</MButton>

<MButton Fab Dark Color="pink">
    <MIcon>mdi-heart</MIcon>
</MButton>
```

## 加载状态
```razor
<MButton Color="primary" Loading="@_loading" OnClick="Load">
    Click Me
</MButton>

@code {
    bool _loading = false;
    async Task Load()
    {
        _loading = true;
        await Task.Delay(2000);
        _loading = false;
    }
}
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Color | String | 颜色(primary/secondary/success/error/warning/info) |
| Dark | Boolean | 暗色主题 |
| Disabled | Boolean | 禁用 |
| Depressed | Boolean | 平面按钮(无阴影) |
| Elevation | Int | 阴影层级(0-24) |
| Fab | Boolean | 浮动操作按钮 |
| Icon | Boolean | 图标按钮 |
| Large | Boolean | 大尺寸 |
| Loading | Boolean | 加载状态 |
| Outlined | Boolean | 描边按钮 |
| Plain | Boolean | 朴素样式 |
| Rounded | Boolean | 圆角 |
| Small | Boolean | 小尺寸 |
| Text | Boolean | 文本按钮 |
| Tile | Boolean | 直角(无圆角) |
| Block | Boolean | 块级(100%宽度) |
| Href | String | 链接地址 |
| Target | String | 链接打开方式 |
| Type | String | 按钮类型(button/submit/reset) |
| OnClick | EventCallback | 点击事件 |

## 事件
| 事件 | 说明 |
|------|------|
| OnClick | 点击时触发 |
| OnMouseDown | 鼠标按下时触发 |
| OnMouseUp | 鼠标抬起时触发 |
