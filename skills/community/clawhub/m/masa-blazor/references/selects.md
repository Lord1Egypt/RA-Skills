# MSelect 下拉选择器

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/selects

## 基础用法
```razor
<MSelect @bind-Value="_selected"
         Items="@_items"
         ItemText="@(item => item.Name)"
         ItemValue="@(item => item.Id)"
         Label="选择项目"
         Outlined />
```

## 多选
```razor
<MSelect @bind-Values="_selectedList"
         Items="@_items"
         ItemText="@(item => item.Name)"
         ItemValue="@(item => item.Id)"
         Label="多选"
         Multiple
         Outlined />
```

## 带图标的选项
```razor
<MSelect @bind-Value="_selected"
         Items="@_items"
         ItemText="@(item => item.Name)"
         ItemValue="@(item => item.Id)"
         Label="选择"
         Outlined>
    <SelectionContent>
        <MIcon Left>@context.Item.Icon</MIcon>
        @context.Item.Name
    </SelectionContent>
</MSelect>
```

## 可清除/搜索
```razor
<!-- 可清除 -->
<MSelect Clearable Label="可清除" />

<!-- 可搜索 -->
<MSelect @bind-Value="_selected" 
         Items="@_cities"
         Label="搜索城市"
         Outlined
         Clearable />
```

## Chips 模式
```razor
<MSelect @bind-Values="_selected"
         Items="@_items"
         ItemText="@(item => item)"
         ItemValue="@(item => item)"
         Label="标签选择"
         Multiple
         Chips
         DeletableChips
         Outlined />
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | T | 选中值 |
| Values | IEnumerable<T> | 多选值 |
| Items | IEnumerable<T> | 选项列表 |
| ItemText | Func<T, string> | 选项文本映射 |
| ItemValue | Func<T, object> | 选项值映射 |
| Label | String | 标签 |
| Placeholder | String | 占位文本 |
| Multiple | Boolean | 多选模式 |
| Clearable | Boolean | 可清除 |
| Disabled | Boolean | 禁用 |
| Readonly | Boolean | 只读 |
| Outlined | Boolean | 描边样式 |
| Filled | Boolean | 填充样式 |
| Solo | Boolean | 单行样式 |
| Dense | Boolean | 紧凑模式 |
| Chips | Boolean | Chip展示模式 |
| DeletableChips | Boolean | 可删除的Chips |
| SmallChips | Boolean | 小型Chips |
| MenuProps | Object | 下拉菜单属性 |
| HideDetails | String | 隐藏详情 |
| Rules | List<Func> | 验证规则 |
| Required | Boolean | 必填 |
| Color | String | 主题色 |
| AppendIcon | String | 后置图标 |
| PrependIcon | String | 前置图标 |



## 事件
| 事件 | 说明 |
|------|------|
| ValueChanged | 选中值改变时触发 |
| OnChange | 值确认改变时触发 |
| OnBlur | 失去焦点时触发 |
| OnFocus | 获得焦点时触发 |
| OnSearchUpdate | 搜索值更新时触发 |