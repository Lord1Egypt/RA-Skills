# 树形视图与水印

## MTreeview 树形视图

文档: https://docs.masastack.com/blazor/ui-components/treeview

### 基础用法
```razor
<MTreeview Items="@_items" ItemText="@(item => item.Name)" ItemChildren="@(item => item.Children)" />
```

### 可选择
```razor
<MTreeview Items="@_items"
           ItemText="@(item => item.Name)"
           ItemChildren="@(item => item.Children)"
           Selectable
           @bind-Selected="_selected" />
```

### 带图标
```razor
<MTreeview Items="@_items" ItemText="@(item => item.Name)" ItemIcon="@(item => item.Icon)">
    <PrependContent>
        <MIcon>@context.Item.Icon</MIcon>
    </PrependContent>
</MTreeview>
```

### 带复选框
```razor
<MTreeview Items="@_items"
           ItemText="@(item => item.Name)"
           ItemChildren="@(item => item.Children)"
           Selectable
           SelectionType="leaf"
           @bind-Selected="_selected" />
```

### 可搜索
```razor
<MTextField @bind-Value="_search" Label="搜索" Clearable HideDetails="auto" />
<MTreeview Items="@_items"
           ItemText="@(item => item.Name)"
           Search="@_search"
           Filter="Filter" />

@code {
    Func<object, string, bool> Filter = (item, search) =>
    {
        return item.ToString().Contains(search, StringComparison.OrdinalIgnoreCase);
    };
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Items | IEnumerable | 数据源 |
| ItemText | Func | 项文本映射 |
| ItemChildren | Func | 子节点映射 |
| ItemKey | Func | 项唯一键 |
| ItemIcon | Func | 项图标映射 |
| Selectable | Boolean | 可选中 |
| Selected | IEnumerable | 选中项 |
| Active | IEnumerable | 激活项 |
| Open | IEnumerable | 展开项 |
| OpenAll | Boolean | 全部展开 |
| Activatable | Boolean | 可激活 |
| Hoverable | Boolean | 悬停效果 |
| Dense | Boolean | 紧凑模式 |
| Dark | Boolean | 暗色主题 |
| Search | String | 搜索关键字 |
| Filter | Func | 搜索过滤函数 |
| SelectionType | String | 选择类型(leaf/all) |
| Shaped | Boolean | 形状样式 |
| Rounded | Boolean/String | 圆角 |
| IndeterminateIcon | String | 半选图标 |
| OnIcon | String | 选中图标 |
| OffIcon | String | 未选中图标 |
| LoadChildren | Func | 异步加载子节点 |
| OpenOnClick | Boolean | 点击展开 |

---

## MWatermark 水印

文档: https://docs.masastack.com/blazor/ui-components/watermark

### 基础用法
```razor
<MWatermark Content="公司机密">
    <MCard Class="pa-8">
        <MCardTitle>带水印的卡片</MCardTitle>
        <MCardText>内容区域</MCardText>
    </MCard>
</MWatermark>
```

### 图片水印
```razor
<MWatermark Image="watermark.png" ImageHeight="50" ImageWidth="100">
    <MContainer>内容</MContainer>
</MWatermark>
```

### 自定义样式
```razor
<MWatermark Content="CONFIDENTIAL"
            FontSize="16"
            FontColor="rgba(0, 0, 0, 0.1)"
            Rotate="-22"
            Gap="100">
    <MCard>内容</MCard>
</MWatermark>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Content | String | 水印文本 |
| Image | String | 水印图片URL |
| ImageWidth | Int | 图片宽度 |
| ImageHeight | Int | 图片高度 |
| FontSize | Int/String | 字体大小 |
| FontColor | String | 字体颜色 |
| FontFamily | String | 字体 |
| FontWeight | String | 字体粗细 |
| Rotate | Int | 旋转角度 |
| Gap | Int | 水印间距 |
| Offset | Int | 偏移 |
| Width | Int | 水印宽度 |
| Height | Int | 水印高度 |
| FullPage | Boolean | 全页水印 |
| ZIndex | Int | z-index |
| Fixed | Boolean | 固定定位 |
| IsRepeat | Boolean | 是否重复 |


## 事件
| 事件 | 说明 |
|------|------|
| ActiveChanged | 激活项改变时触发 |
| OpenChanged | 展开项改变时触发 |
| SelectedChanged | 选中项改变时触发 |
| OnInput | 输入时触发 |