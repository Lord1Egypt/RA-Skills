# MCard 卡片

文档: https://docs.masastack.com/blazor/ui-components/cards

## 基础用法
```razor
<MCard Class="mx-auto" MaxWidth="400">
    <MCardTitle>卡片标题</MCardTitle>
    <MCardSubtitle>副标题</MCardSubtitle>
    <MCardText>卡片内容文本</MCardText>
    <MCardActions>
        <MButton Text Color="primary">操作</MButton>
    </MCardActions>
</MCard>
```

## 带图片的卡片
```razor
<MCard Class="mx-auto" MaxWidth="400">
    <MImage Src="https://picsum.photos/400/200" Height="200" />
    <MCardTitle>图片卡片</MCardTitle>
    <MCardText>带封面图的卡片</MCardText>
</MCard>
```

## 带操作的卡片
```razor
<MCard Class="mx-auto" MaxWidth="400">
    <MCardTitle>
        标题
        <MSpacer />
        <MButton Icon><MIcon>mdi-dots-vertical</MIcon></MButton>
    </MCardTitle>
    <MCardText>卡片内容</MCardText>
    <MCardActions>
        <MButton Text Color="primary">分享</MButton>
        <MButton Text Color="primary">探索</MButton>
    </MCardActions>
</MCard>
```

## 卡片列表
```razor
<MRow>
    @foreach (var item in _items)
    {
        <MCol Cols="12" Md="4">
            <MCard>
                <MImage Src="@item.Image" Height="200" />
                <MCardTitle>@item.Title</MCardTitle>
                <MCardText>@item.Description</MCardText>
            </MCard>
        </MCol>
    }
</MRow>
```

## 可展开卡片
```razor
<MCard>
    <MCardTitle>
        可展开卡片
        <MSpacer />
        <MButton Icon OnClick="() => _show = !_show">
            <MIcon>@(_show ? "mdi-chevron-up" : "mdi-chevron-down")</MIcon>
        </MButton>
    </MCardTitle>
    <MExpandTransition>
        <MCardText Show="@_show">
            展开的内容...
        </MCardText>
    </MExpandTransition>
</MCard>
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Color | String | 卡片颜色 |
| Dark | Boolean | 暗色主题 |
| Elevation | Int | 阴影层级(0-24) |
| Flat | Boolean | 无阴影 |
| Hover | Boolean | 悬停效果 |
| Img | String | 背景图片URL |
| Loading | Boolean | 显示加载状态 |
| MaxWidth | Int/String | 最大宽度 |
| MinWidth | Int/String | 最小宽度 |
| MaxHeight | Int/String | 最大高度 |
| MinHeight | Int/String | 最小高度 |
| Outlined | Boolean | 描边样式 |
| Raised | Boolean | 凸起样式 |
| Rounded | Boolean/String | 圆角 |
| Shaped | Boolean | 左侧形状样式 |
| Tile | Boolean | 直角 |

## 子组件
- **MCardTitle** - 标题区域
- **MCardSubtitle** - 副标题
- **MCardText** - 内容区域
- **MCardActions** - 操作区域



## 事件
| 事件 | 说明 |
|------|------|
| OnClick | 点击卡片时触发 |
| OnMouseEnter | 鼠标进入时触发 |
| OnMouseLeave | 鼠标离开时触发 |