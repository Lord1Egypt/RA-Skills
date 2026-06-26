# 轮播与滑动

## MCarousel 轮播

文档: https://docs.masastack.com/blazor/ui-components/carousels

### 基础用法
```razor
<MCarousel>
    <MCarouselItem>
        <MImage Src="slide1.jpg" Height="400" />
    </MCarouselItem>
    <MCarouselItem>
        <MImage Src="slide2.jpg" Height="400" />
    </MCarouselItem>
    <MCarouselItem>
        <MImage Src="slide3.jpg" Height="400" />
    </MCarouselItem>
</MCarousel>
```

### 带控制
```razor
<MCarousel ShowArrows ShowArrowsOnHover HideDelimiterBackground>
    <MCarouselItem>
        <MImage Src="slide1.jpg" />
    </MCarouselItem>
    <MCarouselItem>
        <MImage Src="slide2.jpg" />
    </MCarouselItem>
</MCarousel>
```

### 垂直轮播
```razor
<MCarousel Vertical VerticalDelimiters>
    <MCarouselItem>内容1</MCarouselItem>
    <MCarouselItem>内容2</MCarouselItem>
</MCarousel>
```

### 自动播放
```razor
<MCarousel Continuous Cycle Interval="3000">
    <MCarouselItem>自动播放1</MCarouselItem>
    <MCarouselItem>自动播放2</MCarouselItem>
</MCarousel>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Int/StringNumber | 当前项 |
| Continuous | Boolean | 循环播放 |
| Cycle | Boolean | 自动轮播 |
| Interval | Int | 自动播放间隔(ms) |
| ShowArrows | Boolean | 显示箭头 |
| ShowArrowsOnHover | Boolean | 悬停显示箭头 |
| HideDelimiters | Boolean | 隐藏指示器 |
| HideDelimiterBackground | Boolean | 隐藏指示器背景 |
| DelimitersIcon | String | 指示器图标 |
| Vertical | Boolean | 垂直模式 |
| VerticalDelimiters | String | 垂直指示器位置 |
| Dark | Boolean | 暗色主题 |
| Height | Int/String | 高度 |
| MaxHeight | Int/String | 最大高度 |
| Progress | Boolean | 显示进度条 |
| ProgressColor | String | 进度条颜色 |
| Reverse | Boolean | 反向 |
| Transition | String | 过渡动画 |

---

## MSlideGroup 滑动组

文档: https://docs.masastack.com/blazor/ui-components/groups/slide-groups

### 基础用法
```razor
<MSlideGroup @bind-Value="_selected" ShowArrows>
    @foreach (var item in _items)
    {
        <MSlideGroupItem Value="item">
            <MCard Class="ma-2" Width="200">
                <MCardTitle>@item</MCardTitle>
            </MCard>
        </MSlideGroupItem>
    }
</MSlideGroup>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Object | 选中值 |
| Multiple | Boolean | 多选 |
| Mandatory | Boolean | 必须选中 |
| ShowArrows | Boolean | 显示箭头 |
| CenterActive | Boolean | 激活项居中 |
| NextIcon | String | 下一个图标 |
| PrevIcon | String | 上一个图标 |
| Dark | Boolean | 暗色主题 |
| Max | Int | 最大选中数 |
| ActiveClass | String | 激活CSS类 |



## 事件
### MCarousel
| 事件 | 说明 |
|------|------|
| ValueChanged | 当前项改变时触发 |
| OnChange | 切换时触发 |

### MSlideGroup
| 事件 | 说明 |
|------|------|
| ValueChanged | 选中项改变时触发 |