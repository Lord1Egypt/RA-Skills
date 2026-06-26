# 拖拽与分割

## MSortable 拖拽排序

文档: https://docs.masastack.com/blazor/ui-components/sortable

### 基础用法
```razor
<MSortable @bind-Items="_items" OnSort="OnSort">
    @foreach (var item in _items)
    {
        <div class="pa-2 ma-1" style="background: #eee; cursor: move;">
            @item
        </div>
    }
</MSortable>

@code {
    List<string> _items = new() { "项目1", "项目2", "项目3", "项目4" };
    
    void OnSort()
    {
        // 排序完成回调
    }
}
```

### 卡片排序
```razor
<MSortable @bind-Items="_cards" Group="cards">
    @foreach (var card in _cards)
    {
        <MCard Class="ma-2" Style="cursor: move;">
            <MCardTitle>@card.Title</MCardTitle>
        </MCard>
    }
</MSortable>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Items | IEnumerable | 数据源 |
| Group | String | 分组(跨列表拖拽) |
| Animation | Int | 动画时长(ms) |
| GhostClass | String | 拖拽占位样式 |
| ChosenClass | String | 选中样式 |
| DragClass | String | 拖拽样式 |
| Disabled | Boolean | 禁用 |
| Handle | String | 拖拽手柄选择器 |
| Filter | String | 不可拖拽元素选择器 |
| Delay | Int | 拖拽延迟(ms) |
| SwapThreshold | Double | 交换阈值 |
| MultiDrag | Boolean | 多选拖拽 |

---

## MSplitter 分割面板

文档: https://docs.masastack.com/blazor/ui-components/splitters

### 基础用法
```razor
<MSplitter>
    <MSplitterPane>
        <MCard>
            <MCardText>左侧面板</MCardText>
        </MCard>
    </MSplitterPane>
    <MSplitterPane>
        <MCard>
            <MCardText>右侧面板</MCardText>
        </MCard>
    </MSplitterPane>
</MSplitter>
```

### 垂直分割
```razor
<MSplitter Vertical Style="height: 400px;">
    <MSplitterPane>上方面板</MSplitterPane>
    <MSplitterPane>下方面板</MSplitterPane>
</MSplitter>
```

### 三栏布局
```razor
<MSplitter>
    <MSplitterPane Size="200">左栏</MSplitterPane>
    <MSplitterPane>中间(自动填充)</MSplitterPane>
    <MSplitterPane Size="300">右栏</MSplitterPane>
</MSplitter>
```

### 常用参数

#### MSplitter
| 参数 | 类型 | 说明 |
|------|------|------|
| Vertical | Boolean | 垂直分割 |
| RTL | Boolean | 从右到左 |
| GutterSize | Int | 分割条大小 |
| GutterStyle | Object | 分割条样式 |
| OnDrag | EventCallback | 拖拽事件 |

#### MSplitterPane
| 参数 | 类型 | 说明 |
|------|------|------|
| Size | Int/String | 面板大小 |
| MinSize | Int/String | 最小大小 |
| MaxSize | Int/String | 最大大小 |
| Collapsible | Boolean | 可折叠 |
| Collapsed | Boolean | 折叠状态 |
| Resizable | Boolean | 可调整大小 |

---

## MDescription 描述列表

文档: https://docs.masastack.com/blazor/ui-components/descriptions

### 基础用法
```razor
<MDescriptions Title="用户信息">
    <MDescriptionsItem Label="姓名">张三</MDescriptionsItem>
    <MDescriptionsItem Label="年龄">28</MDescriptionsItem>
    <MDescriptionsItem Label="邮箱">zhangsan@example.com</MDescriptionsItem>
</MDescriptions>
```

### 带边框
```razor
<MDescriptions Title="用户信息" Bordered>
    <MDescriptionsItem Label="姓名">张三</MDescriptionsItem>
    <MDescriptionsItem Label="年龄">28</MDescriptionsItem>
    <MDescriptionsItem Label="邮箱" Span="2">zhangsan@example.com</MDescriptionsItem>
    <MDescriptionsItem Label="地址" Span="3">北京市朝阳区</MDescriptionsItem>
</MDescriptions>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Title | String | 标题 |
| Bordered | Boolean | 带边框 |
| Column | Int | 列数 |
| Colon | Boolean | 显示冒号 |
| Dense | Boolean | 紧凑模式 |
| LabelWidth | Int/String | 标签宽度 |
| Size | String | 尺寸 |

---

## MBlockText 块文本

文档: https://docs.masastack.com/blazor/ui-components/block-text

```razor
<MBlockText>
    这是一段较长的文本内容，会自动换行和分段显示。
</MBlockText>
```

---

## MCopyableText 可复制文本

文档: https://docs.masastack.com/blazor/ui-components/copyable-text

```razor
<MCopyableText Text="要复制的内容" />
<MCopyableText Text="https://example.com" ShowCopyIcon />
```


## 事件
### MSortable
| 事件 | 说明 |
|------|------|
| OnSort | 排序完成时触发 |
| OnStart | 开始拖拽时触发 |
| OnEnd | 结束拖拽时触发 |
| OnChange | 顺序改变时触发 |

### MSplitter
| 事件 | 说明 |
|------|------|
| OnDrag | 拖拽分割条时触发 |
| OnDragStart | 开始拖拽时触发 |
| OnDragEnd | 结束拖拽时触发 |

### MDescriptions
| 事件 | 说明 |
|------|------|
| (无常用事件) | 主要用于展示 |