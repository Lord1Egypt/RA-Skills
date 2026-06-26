# 反馈与选择

## MEmptyState 空状态

文档: https://docs.masastack.com/blazor/ui-components/empty-states

```razor
<MEmptyState Icon="mdi-folder-open-outline" Label="暂无数据" Description="请添加数据后查看">
    <MButton Color="primary" OnClick="AddData">添加数据</MButton>
</MEmptyState>

<MEmptyState Image="empty.png" Label="搜索无结果" Description="换个关键词试试" />
```

---

## MRating 评分

文档: https://docs.masastack.com/blazor/ui-components/ratings

```razor
<MRating @bind-Value="_rating" />
<MRating @bind-Value="_rating" Color="yellow darken-3" BackgroundColor="grey lighten-1" />
<MRating @bind-Value="_rating" Length="10" HalfIncrements />
<MRating @bind-Value="_rating" Readonly />
<MRating @bind-Value="_rating" Icon="mdi-heart" Color="red" EmptyIcon="mdi-heart-outline" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Double | 评分值 |
| Length | Int | 评分数量 |
| HalfIncrements | Boolean | 半星评分 |
| Dense | Boolean | 紧凑模式 |
| Readonly | Boolean | 只读 |
| Clearable | Boolean | 可清除 |
| Color | String | 颜色 |
| BackgroundColor | String | 背景色 |
| Icon | String | 图标 |
| EmptyIcon | String | 空图标 |
| FullIcon | String | 满图标 |
| HalfIcon | String | 半星图标 |
| Hover | Boolean | 悬停效果 |
| Size | Int/String | 尺寸 |
| Dark | Boolean | 暗色主题 |

---

## MToggle 切换按钮

文档: https://docs.masastack.com/blazor/ui-components/toggles

```razor
<MToggle @bind-Value="_value">
    <MButton><MIcon>mdi-format-bold</MIcon></MButton>
</MToggle>
```

---

## MBadge 徽章

文档: https://docs.masastack.com/blazor/ui-components/badges

```razor
<MBadge Content="5" Color="red" Overlap>
    <MIcon>mdi-bell</MIcon>
</MBadge>

<MBadge Content="99+" Color="red" Overlap>
    <MButton>消息</MButton>
</MBadge>

<MBadge Dot Color="green" OffsetX="10" OffsetY="10">
    <MAvatar><MImage Src="avatar.jpg" /></MAvatar>
</MBadge>

<MBadge Icon="mdi-check" Color="green">
    <MButton>已完成</MButton>
</MBadge>
```

---

## MHover 悬停效果

文档: https://docs.masastack.com/blazor/ui-components/hover

```razor
<MHover>
    <MCard Class="@($"mx-auto {(context.Hover ? "elevation-12" : "elevation-2")}")"
           @attributes="context.Attrs">
        <MCardTitle>悬停效果</MCardTitle>
    </MCard>
</MHover>
```

---

## MTooltip 工具提示

文档: https://docs.masastack.com/blazor/ui-components/tooltips

```razor
<MTooltip Top>
    <ActivatorContent>
        <MButton @attributes="context.Attrs">悬停</MButton>
    </ActivatorContent>
    <ChildContent>提示内容</ChildContent>
</MTooltip>

<MTooltip Bottom Color="primary" OpenDelay="500">
    <ActivatorContent>
        <MIcon @attributes="context.Attrs">mdi-help</MIcon>
    </ActivatorContent>
    <ChildContent>延迟显示的提示</ChildContent>
</MTooltip>
```

---

## MEnqueuedSnackbars 消息队列

文档: https://docs.masastack.com/blazor/ui-components/enqueued-snackbars

```razor
<MEnqueuedSnackbars @ref="_snackbars" />

<MButton OnClick="ShowMessage">显示消息</MButton>

@code {
    MEnqueuedSnackbars _snackbars;
    
    async Task ShowMessage()
    {
        await _snackbars.EnqueueSnackbarAsync("操作成功", AlertTypes.Success);
    }
}
```

---

## MErrorHandler 错误处理

文档: https://docs.masastack.com/blazor/ui-components/error-handler

```razor
<MErrorHandler>
    <ErrorContent>
        <MAlert Type="AlertTypes.Error">
            发生错误: @context.Message
        </MAlert>
    </ErrorContent>
    <ChildContent>
        <!-- 应用内容 -->
    </ChildContent>
</MErrorHandler>
```


## 事件
### MEmptyState
| 事件 | 说明 |
|------|------|
| OnClickAction | 操作按钮点击时触发 |

### MRating
| 事件 | 说明 |
|------|------|
| ValueChanged | 评分值改变时触发 |
| OnInput | 输入时触发 |

### MBadge
| 事件 | 说明 |
|------|------|
| (无常用事件) | 主要用于展示 |

### MToggle
| 事件 | 说明 |
|------|------|
| ValueChanged | 切换状态改变时触发 |

### MHover
| 事件 | 说明 |
|------|------|
| HoverChanged | 悬停状态改变时触发 |