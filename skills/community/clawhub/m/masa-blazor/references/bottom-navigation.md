# 底部导航与分页

## MBottomNavigation 底部导航

文档: https://docs.masastack.com/blazor/ui-components/bottom-navigation

### 基础用法
```razor
<MBottomNavigation @bind-Value="_selected" App Color="primary">
    <MButton Value="home">
        <span>首页</span>
        <MIcon>mdi-home</MIcon>
    </MButton>
    <MButton Value="search">
        <span>搜索</span>
        <MIcon>mdi-magnify</MIcon>
    </MButton>
    <MButton Value="favorites">
        <span>收藏</span>
        <MIcon>mdi-heart</MIcon>
    </MButton>
    <MButton Value="profile">
        <span>我的</span>
        <MIcon>mdi-account</MIcon>
    </MButton>
</MBottomNavigation>
```

### 带颜色
```razor
<MBottomNavigation App Color="primary" Dark>
    <MButton><MIcon>mdi-history</MIcon></MButton>
    <MButton><MIcon>mdi-heart</MIcon></MButton>
    <MButton><MIcon>mdi-map-marker</MIcon></MButton>
</MBottomNavigation>
```

### 水平模式
```razor
<MBottomNavigation App Horizontal>
    <MButton Value="home">
        <span>首页</span>
    </MButton>
    <MButton Value="search">
        <span>搜索</span>
    </MButton>
</MBottomNavigation>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | StringNumber | 当前选中值 |
| App | Boolean | 布局模式 |
| Color | String | 颜色 |
| Dark | Boolean | 暗色主题 |
| Fixed | Boolean | 固定定位 |
| Grow | Boolean | 增长模式 |
| HideOnScroll | Boolean | 滚动隐藏 |
| Horizontal | Boolean | 水平布局 |
| InputValue | Boolean | 是否显示 |
| Mandatory | Boolean | 必须选中 |
| ScrollTarget | String | 滚动目标 |
| ScrollThreshold | Int | 滚动阈值 |
| Shift | Boolean | 移位模式 |
| BackgroundColor | String | 背景色 |

---

## MPagination 分页

文档: https://docs.masastack.com/blazor/ui-components/paginations

### 基础用法
```razor
<MPagination @bind-Value="_page" Length="10" />
```

### 带边界页码
```razor
<MPagination @bind-Value="_page" Length="20" TotalVisible="7" />
```

### 圆形/图标
```razor
<MPagination @bind-Value="_page" Length="10" Circle />
<MPagination @bind-Value="_page" Length="10" NextIcon="mdi-chevron-right" PrevIcon="mdi-chevron-left" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Int/StringNumber | 当前页 |
| Length | Int | 总页数 |
| TotalVisible | Int | 可见页码数 |
| Circle | Boolean | 圆形页码 |
| Dark | Boolean | 暗色主题 |
| Disabled | Boolean | 禁用 |
| NextIcon | String | 下一页图标 |
| PrevIcon | String | 上一页图标 |
| FirstIcon | String | 首页图标 |
| LastIcon | String | 末页图标 |
| Page | Int | 当前页(别名) |
| Size | Int/String | 尺寸 |

---

## MInfiniteScroll 无限滚动

文档: https://docs.masastack.com/blazor/ui-components/infinite-scroll

```razor
<MInfiniteScroll OnLoad="LoadMore" Parent="scrollContainer">
    @foreach (var item in _items)
    {
        <MCard Class="ma-2">
            <MCardText>@item</MCardText>
        </MCard>
    }
</MInfiniteScroll>

@code {
    async Task LoadMore(InfiniteScrollLoadEventArgs args)
    {
        // 加载更多数据
        await Task.Delay(1000);
        _items.AddRange(GetMoreData());
        args.Status = InfiniteScrollLoadStatus.Ok;
    }
}
```

---

## MScrollToTarget 滚动定位

文档: https://docs.masastack.com/blazor/ui-components/scroll-to-target

```razor
<MScrollToTarget Target="section1" Offset="64">
    <MButton>跳转到章节1</MButton>
</MScrollToTarget>
```

---

## MSticky 吸顶

文档: https://docs.masastack.com/blazor/ui-components/sticky

```razor
<MSticky OffsetTop="64">
    <MCard Class="pa-4">
        <MCardTitle>吸顶内容</MCardTitle>
    </MCard>
</MSticky>
```


## 事件
### MBottomNavigation
| 事件 | 说明 |
|------|------|
| ValueChanged | 选中项改变时触发 |

### MPagination
| 事件 | 说明 |
|------|------|
| ValueChanged | 当前页改变时触发 |
| OnInput | 输入页码时触发 |

### MInfiniteScroll
| 事件 | 说明 |
|------|------|
| OnLoad | 滚动到底部加载更多时触发 |