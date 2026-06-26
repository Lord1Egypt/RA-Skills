# MChip 标签

文档: https://docs.masastack.com/blazor/ui-components/chips

## 基础用法
```razor
<MChip>默认标签</MChip>
<MChip Color="primary">主色标签</MChip>
<MChip Color="success">成功标签</MChip>
<MChip Color="error">错误标签</MChip>
```

## 带关闭按钮
```razor
<MChip Closeable OnCloseClick="Remove">可关闭标签</MChip>
```

## 带图标
```razor
<MChip>
    <MIcon Left>mdi-account</MIcon>
    用户
</MChip>

<MChip Pill>
    <MAvatar Left>
        <MImage Src="avatar.jpg" />
    </MAvatar>
    用户名
</MChip>
```

## 可选中
```razor
<MChip @bind-Active="_active" Filter>可选中</MChip>
```

## Outlined 样式
```razor
<MChip Outlined Color="primary">描边标签</MChip>
<MChip Outlined Color="success">描边成功</MChip>
```

## 标签组
```razor
<MChipGroup @bind-Value="_selected" Multiple Column>
    <MChip Value="1" Filter>标签1</MChip>
    <MChip Value="2" Filter>标签2</MChip>
    <MChip Value="3" Filter>标签3</MChip>
    <MChip Value="4" Filter>标签4</MChip>
</MChipGroup>
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Active | Boolean | 激活状态 |
| Closeable | Boolean | 可关闭 |
| CloseIcon | String | 关闭图标 |
| Color | String | 颜色 |
| Dark | Boolean | 暗色主题 |
| Disabled | Boolean | 禁用 |
| Draggable | Boolean | 可拖拽 |
| Filter | Boolean | 可选中(显示勾选图标) |
| FilterIcon | String | 选中图标 |
| Label | Boolean | 标签样式(有背景) |
| Link | Boolean | 链接样式 |
| Outlined | Boolean | 描边样式 |
| Pill | Boolean | 胶囊样式(带头像时) |
| Ripple | Boolean | 水波纹 |
| Small | Boolean | 小尺寸 |
| Value | Object | 标签值 |
| Href | String | 链接 |

## MChipGroup 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Object | 选中值 |
| Values | IEnumerable | 多选值 |
| Multiple | Boolean | 多选 |
| Column | Boolean | 垂直排列 |
| ShowArrows | Boolean | 显示滚动箭头 |
| ActiveClass | String | 激活CSS类 |
| CenterActive | Boolean | 激活项居中 |
| Mandatory | Boolean | 必须选中一项 |
| Max | Int | 最大选中数 |



## 事件
### MChip
| 事件 | 说明 |
|------|------|
| OnClick | 点击时触发 |
| OnCloseClick | 关闭按钮点击时触发 |
| ActiveChanged | 激活状态改变时触发 |

### MChipGroup
| 事件 | 说明 |
|------|------|
| ValueChanged | 选中值改变时触发 |