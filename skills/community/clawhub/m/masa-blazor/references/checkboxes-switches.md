# 复选框与开关

## MCheckbox 复选框

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/checkboxes

### 基础用法
```razor
<MCheckbox @bind-Value="_checked" Label="同意协议" />
<MCheckbox @bind-Value="_checked" Label="记住我" Color="primary" />
```

### 多选组
```razor
<MCheckboxGroup @bind-Values="_selected" Label="选择爱好">
    <MCheckbox Label="阅读" Value="reading" />
    <MCheckbox Label="运动" Value="sports" />
    <MCheckbox Label="音乐" Value="music" />
</MCheckboxGroup>

@code {
    List<string> _selected = new();
}
```

### 禁用/只读
```razor
<MCheckbox Disabled Label="禁用" />
<MCheckbox Readonly Label="只读" Value="true" />
```

### 不确定状态
```razor
<MCheckbox Indeterminate Label="不确定" />
```

### 带图标
```razor
<MCheckbox OnIcon="mdi-heart" OffIcon="mdi-heart-outline" Color="red" Label="收藏" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Boolean | 选中状态(双向绑定) |
| Label | String | 标签 |
| Color | String | 颜色 |
| Disabled | Boolean | 禁用 |
| Readonly | Boolean | 只读 |
| Indeterminate | Boolean | 不确定状态 |
| IndeterminateIcon | String | 不确定图标 |
| OnIcon | String | 选中图标 |
| OffIcon | String | 未选中图标 |
| Dense | Boolean | 紧凑模式 |
| Dark | Boolean | 暗色主题 |
| HideDetails | String | 隐藏详情 |
| Ripple | Boolean | 水波纹 |
| TrueValue | Object | 自定义真值 |
| FalseValue | Object | 自定义假值 |
| ValueChanged | EventCallback | 值改变事件 |

---

## MSwitch 开关

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/switches

### 基础用法
```razor
<MSwitch @bind-Value="_enabled" Label="启用" />
<MSwitch @bind-Value="_darkMode" Label="暗色模式" Color="primary" />
```

### 带颜色
```razor
<MSwitch Color="primary" Label="Primary" />
<MSwitch Color="success" Label="Success" />
<MSwitch Color="error" Label="Error" />
<MSwitch Color="warning" Label="Warning" />
```

### 带图标
```razor
<MSwitch Label="消息通知">
    <CheckedContent>
        <MIcon Color="white" Style="font-size: 12px;">mdi-check</MIcon>
    </CheckedContent>
    <UncheckedContent>
        <MIcon Color="white" Style="font-size: 12px;">mdi-close</MIcon>
    </UncheckedContent>
</MSwitch>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Boolean | 开关状态(双向绑定) |
| Label | String | 标签 |
| Color | String | 颜色 |
| Disabled | Boolean | 禁用 |
| Readonly | Boolean | 只读 |
| Dense | Boolean | 紧凑模式 |
| Dark | Boolean | 暗色主题 |
| HideDetails | String | 隐藏详情 |
| Inset | Boolean | 内嵌样式 |
| Flat | Boolean | 无阴影 |
| TrueValue | Object | 自定义真值 |
| FalseValue | Object | 自定义假值 |
| Ripple | Boolean | 水波纹 |



## 事件
### MCheckbox
| 事件 | 说明 |
|------|------|
| ValueChanged | 选中状态改变时触发 |

### MSwitch
| 事件 | 说明 |
|------|------|
| ValueChanged | 开关状态改变时触发 |