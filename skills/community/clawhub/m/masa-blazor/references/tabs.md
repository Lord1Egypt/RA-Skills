# MTabs 标签页

文档: https://docs.masastack.com/blazor/ui-components/tabs

## 基础用法
```razor
<MTabs @bind-Value="_tab">
    <MTab Value="1">标签1</MTab>
    <MTab Value="2">标签2</MTab>
    <MTab Value="3">标签3</MTab>
</MTabs>

<MTabsItems Value="_tab">
    <MTabItem Value="1">内容1</MTabItem>
    <MTabItem Value="2">内容2</MTabItem>
    <MTabItem Value="3">内容3</MTabItem>
</MTabsItems>

@code {
    StringNumber _tab = "1";
}
```

## 带图标
```razor
<MTabs>
    <MTab>
        <MIcon Left>mdi-phone</MIcon>
        电话
    </MTab>
    <MTab>
        <MIcon Left>mdi-heart</MIcon>
        收藏
    </MTab>
</MTabs>
```

## 垂直标签
```razor
<MTabs Vertical>
    <MTab>标签1</MTab>
    <MTab>标签2</MTab>
    <MTab>标签3</MTab>
</MTabs>
```

## 样式变体
```razor
<!-- 固定标签 -->
<MTabs FixedTabs>
    <MTab>固定</MTab>
</MTabs>

<!-- 居中 -->
<MTabs Centered>
    <MTab>居中</Tab>
</MTabs>

<!-- 右对齐 -->
<MTabs Right>
    <MTab>右对齐</MTab>
</MTabs>

<!-- 描边 -->
<MTabs BackgroundColor="transparent" Color="primary">
    <MTab>描边</MTab>
</MTabs>

<!-- 填充 -->
<MTabs BackgroundColor="primary" Dark>
    <MTab>填充</MTab>
</MTabs>
```

## 常用参数

### MTabs
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | StringNumber | 当前选中值 |
| Centered | Boolean | 居中 |
| FixedTabs | Boolean | 固定标签宽度 |
| Right | Boolean | 右对齐 |
| Vertical | Boolean | 垂直排列 |
| Dark | Boolean | 暗色主题 |
| Color | String | 激活颜色 |
| BackgroundColor | String | 背景色 |
| SliderColor | String | 滑块颜色 |
| HideSlider | Boolean | 隐藏滑块 |
| Grow | Boolean | 填充可用空间 |
| ShowArrows | Boolean | 显示滚动箭头 |
| IconsAndText | Boolean | 图标和文本 |

### MTab
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | StringNumber | 标签值 |
| Disabled | Boolean | 禁用 |
| Href | String | 链接 |
| Ripple | Boolean | 水波纹效果 |



## 事件
### MTabs
| 事件 | 说明 |
|------|------|
| ValueChanged | 当前标签改变时触发 |

### MTab
| 事件 | 说明 |
|------|------|
| OnClick | 点击时触发 |