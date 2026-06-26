# 时间线与面包屑

## MTimeline 时间线

文档: https://docs.masastack.com/blazor/ui-components/timelines

### 基础用法
```razor
<MTimeline Dense>
    <MTimelineItem Color="green" Icon="mdi-check">
        <MCard>
            <MCardTitle>事件1</MCardTitle>
            <MCardText>2024-01-01</MCardText>
        </MCard>
    </MTimelineItem>
    <MTimelineItem Color="blue" Icon="mdi-star">
        <MCard>
            <MCardTitle>事件2</MCardTitle>
            <MCardText>2024-02-01</MCardText>
        </MCard>
    </MTimelineItem>
    <MTimelineItem Color="red" Icon="mdi-heart">
        <MCard>
            <MCardTitle>事件3</MCardTitle>
            <MCardText>2024-03-01</MCardText>
        </MCard>
    </MTimelineItem>
</MTimeline>
```

### 交替显示
```razor
<MTimeline>
    <MTimelineItem Color="primary" FillDot Size="Large">
        <template #opposite>
            <span>2024-01-01</span>
        </template>
        <MCard>
            <MCardTitle>事件标题</MCardTitle>
            <MCardText>事件内容</MCardText>
        </MCard>
    </MTimelineItem>
</MTimeline>
```

### 常用参数

#### MTimeline
| 参数 | 类型 | 说明 |
|------|------|------|
| Dense | Boolean | 紧凑模式 |
| Dark | Boolean | 暗色主题 |
| Light | Boolean | 亮色主题 |
| Reverse | Boolean | 反向排列 |
| TruncateLine | String | 截断线(none/start/end/both) |

#### MTimelineItem
| 参数 | 类型 | 说明 |
|------|------|------|
| Color | String | 颜色 |
| Icon | String | 图标 |
| IconColor | String | 图标颜色 |
| FillDot | Boolean | 填充圆点 |
| HideDot | Boolean | 隐藏圆点 |
| Large | Boolean | 大尺寸 |
| Small | Boolean | 小尺寸 |
| Size | String | 尺寸(small/large) |

---

## MBreadcrumbs 面包屑

文档: https://docs.masastack.com/blazor/ui-components/breadcrumbs

### 基础用法
```razor
<MBreadcrumbs Items="@_items" />

@code {
    List<BreadcrumbItem> _items = new()
    {
        new() { Text = "首页", Href = "/" },
        new() { Text = "用户管理", Href = "/users" },
        new() { Text = "用户列表", Disabled = true }
    };
}
```

### 自定义分隔符
```razor
<MBreadcrumbs Items="@_items">
    <DividerContent>
        <MIcon>mdi-chevron-right</MIcon>
    </DividerContent>
</MBreadcrumbs>

<!-- 大于号分隔符 -->
<MBreadcrumbs Items="@_items" Large>
    <DividerContent>
        <MIcon>mdi-forward</MIcon>
    </DividerContent>
</MBreadcrumbs>
```

### 自定义插槽
```razor
<MBreadcrumbs Items="@_items">
    <ItemContent>
        @if (context.Item.Href != null)
        {
            <MBreadcrumbsItem Href="@context.Item.Href">
                @context.Item.Text
            </MBreadcrumbsItem>
        }
        else
        {
            <MBreadcrumbsItem Disabled>
                @context.Item.Text
            </MBreadcrumbsItem>
        }
    </ItemContent>
</MBreadcrumbs>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Items | List<BreadcrumbItem> | 面包屑项目 |
| Large | Boolean | 大尺寸 |
| Dark | Boolean | 暗色主题 |
| Light | Boolean | 亮色主题 |
| Divider | String | 分隔符 |
| JustifyCenter | Boolean | 居中 |
| JustifyEnd | Boolean | 右对齐 |

#### BreadcrumbItem
| 属性 | 类型 | 说明 |
|------|------|------|
| Text | String | 显示文本 |
| Href | String | 链接地址 |
| Disabled | Boolean | 禁用 |
| Exact | Boolean | 精确匹配 |


## 事件
### MTimeline
MTimeline 是纯展示组件，无常用事件。用于展示时间线流程。

### MBreadcrumbs
| 事件 | 说明 |
|------|------|
| OnItemClick | 面包屑项点击时触发 |