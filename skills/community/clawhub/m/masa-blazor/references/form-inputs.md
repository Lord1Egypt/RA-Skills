# 表单输入组件

## MTextarea 多行文本

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/textareas

### 基础用法
```razor
<MTextarea @bind-Value="_text" Label="简介" />
<MTextarea @bind-Value="_text" Label="内容" Rows="5" />
```

### 自动增长
```razor
<MTextarea @bind-Value="_text" AutoGrow Label="自动增长" />
<MTextarea @bind-Value="_text" AutoGrow Rows="3" MaxRows="10" Label="最大10行" />
```

### 禁止调整大小
```razor
<MTextarea @bind-Value="_text" NoResize Label="禁止调整大小" />
```

### 字数统计
```razor
<MTextarea @bind-Value="_text" Counter="200" Label="最多200字" />
<MTextarea @bind-Value="_text" Counter Label="自动统计字数" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | String | 绑定值 |
| Label | String | 标签 |
| Placeholder | String | 占位文本 |
| Rows | Int | 行数 |
| MaxRows | Int | 最大行数(自动增长时) |
| AutoGrow | Boolean | 自动增长 |
| NoResize | Boolean | 禁止调整大小 |
| RowHeight | Int/String | 行高 |
| Counter | Int/String | 字数统计 |
| Outlined | Boolean | 描边样式 |
| Filled | Boolean | 填充样式 |
| Solo | Boolean | 单行样式 |
| Dense | Boolean | 紧凑模式 |
| Disabled | Boolean | 禁用 |
| Readonly | Boolean | 只读 |
| Clearable | Boolean | 可清除 |
| HideDetails | String | 隐藏详情 |
| Rules | List<Func> | 验证规则 |
| Required | Boolean | 必填 |

---

## MAutocomplete 自动完成

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/autocompletes

### 基础用法
```razor
<MAutocomplete @bind-Value="_selected"
               Items="@_items"
               ItemText="@(item => item)"
               ItemValue="@(item => item)"
               Label="搜索"
               Outlined />
```

### 自定义过滤
```razor
<MAutocomplete @bind-Value="_selected"
               Items="@_items"
               ItemText="@(item => item)"
               ItemValue="@(item => item)"
               Label="搜索"
               Filter="FilterFunc"
               Outlined />

@code {
    bool FilterFunc(string item, string queryText, string itemText)
    {
        return itemText.Contains(queryText, StringComparison.OrdinalIgnoreCase);
    }
}
```

### 带插槽
```razor
<MAutocomplete @bind-Value="_selected"
               Items="@_items"
               ItemText="@(item => item.Name)"
               ItemValue="@(item => item.Id)"
               Label="搜索">
    <ItemContent>
        <MListItemAvatar>
            <MImage Src="@context.Item.Avatar" />
        </MListItemAvatar>
        <MListItemContent>
            <MListItemTitle>@context.Item.Name</MListItemTitle>
            <MListItemSubtitle>@context.Item.Email</MListItemSubtitle>
        </MListItemContent>
    </ItemContent>
</MAutocomplete>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | T | 选中值 |
| Items | IEnumerable<T> | 选项列表 |
| ItemText | Func<T, string> | 选项文本映射 |
| ItemValue | Func<T, object> | 选项值映射 |
| Label | String | 标签 |
| Filter | Func | 自定义过滤函数 |
| Clearable | Boolean | 可清除 |
| Multiple | Boolean | 多选 |
| Chips | Boolean | Chip展示 |
| DeletableChips | Boolean | 可删除的Chips |
| NoFilter | Boolean | 禁用过滤 |
| SearchInput | String | 搜索输入值 |
| HideNoData | Boolean | 无数据时隐藏 |
| NoDataText | String | 无数据文本 |

---

## MCascader 级联选择

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/cascaders

### 基础用法
```razor
<MCascader @bind-Value="_selected"
           Items="@_items"
           ItemText="@(item => item.Name)"
           ItemValue="@(item => item.Value)"
           ItemChildren="@(item => item.Children)"
           Label="选择地区"
           Outlined />
```

### 带搜索
```razor
<MCascader @bind-Value="_selected"
           Items="@_items"
           ItemText="@(item => item.Name)"
           ItemValue="@(item => item.Value)"
           ItemChildren="@(item => item.Children)"
           Label="搜索选择"
           Searchable
           Clearable
           Outlined />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | String/Object | 选中值 |
| Items | IEnumerable | 数据源 |
| ItemText | Func | 文本映射 |
| ItemValue | Func | 值映射 |
| ItemChildren | Func | 子节点映射 |
| Label | String | 标签 |
| Searchable | Boolean | 可搜索 |
| Clearable | Boolean | 可清除 |
| ChangeOnSelect | Boolean | 选择即改变 |
| ShowAllLevels | Boolean | 显示完整路径 |

---

## MFileInput 文件上传

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/file-inputs

### 基础用法
```razor
<MFileInput @bind-Value="_file" Label="选择文件" />
<MFileInput @bind-Value="_file" Label="选择文件" Outlined />
```

### 多文件
```razor
<MFileInput @bind-Value="_files" Multiple Label="多文件上传" />
```

### 限制文件类型
```razor
<MFileInput @bind-Value="_file" Accept=".jpg,.png,.gif" Label="图片上传" />
<MFileInput @bind-Value="_file" Accept=".pdf" Label="PDF文件" />
<MFileInput @bind-Value="_file" Accept=".doc,.docx" Label="Word文件" />
```

### 显示文件大小
```razor
<MFileInput @bind-Value="_file" ShowSize Label="显示大小" />
```

### 带图标
```razor
<MFileInput @bind-Value="_file" PrependIcon="mdi-camera" Label="拍照上传" />
<MFileInput @bind-Value="_file" PrependIcon="mdi-file-upload" Label="上传文件" />
```

### Chip 展示
```razor
<MFileInput @bind-Value="_files" Multiple Chips DeletableChips Label="文件列表" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | IBrowserFile/List<IBrowserFile> | 文件对象 |
| Multiple | Boolean | 多文件 |
| Accept | String | 接受的文件类型(.jpg,.png等) |
| ShowSize | Boolean | 显示文件大小 |
| PrependIcon | String | 前置图标 |
| Chips | Boolean | Chip展示 |
| DeletableChips | Boolean | 可删除的Chips |
| Counter | Boolean | 显示计数 |
| TruncateLength | Int | 文件名截断长度 |
| Label | String | 标签 |
| Disabled | Boolean | 禁用 |
| HideDetails | String | 隐藏详情 |

---

## MSlider 滑块

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/sliders

### 基础用法
```razor
<MSlider @bind-Value="_value" Label="音量" Color="primary" />
```

### 带范围
```razor
<MSlider @bind-Value="_value" Min="0" Max="100" Step="10" Label="步长10" />
```

### 带标签
```razor
<MSlider @bind-Value="_value" ThumbLabel="always" Label="始终显示标签" />
<MSlider @bind-Value="_value" ThumbLabel="on-hover" Label="悬停显示标签" />
```

### 垂直滑块
```razor
<MSlider @bind-Value="_value" Vertical Style="height: 200px;" />
```

### 带刻度
```razor
<MSlider @bind-Value="_value" Ticks TickLabels="@_labels" Max="5" />

@code {
    Dictionary<string, string> _labels = new()
    {
        { "0", "很低" }, { "1", "低" }, { "2", "中" }, { "3", "高" }, { "4", "很高" }, { "5", "极高" }
    };
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Double | 滑块值 |
| Min | Double | 最小值 |
| Max | Double | 最大值 |
| Step | Double | 步长 |
| ThumbLabel | String | 滑块标签(always/on-hover) |
| ThumbSize | Int/String | 滑块大小 |
| Vertical | Boolean | 垂直模式 |
| InverseLabel | Boolean | 标签在上方 |
| Disabled | Boolean | 禁用 |
| Readonly | Boolean | 只读 |
| Dense | Boolean | 紧凑模式 |
| TickLabels | Dictionary | 刻度标签 |
| Ticks | Boolean/String | 显示刻度 |
| TrackColor | String | 轨道颜色 |
| TrackFillColor | String | 轨道填充色 |

---

## MRangeSlider 范围滑块

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/range-sliders

```razor
<MRangeSlider @bind-Value="_range" Label="价格范围" Min="0" Max="1000" />

@code {
    IList<double> _range = new List<double> { 100, 500 };
}
```

---

## MRadioGroup 单选组

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/radios

### 基础用法
```razor
<MRadioGroup @bind-Value="_selected" Label="性别">
    <MRadio Label="男" Value="male" />
    <MRadio Label="女" Value="female" />
    <MRadio Label="其他" Value="other" />
</MRadioGroup>
```

### 横向排列
```razor
<MRadioGroup @bind-Value="_selected" Row>
    <MRadio Label="选项A" Value="a" />
    <MRadio Label="选项B" Value="b" />
    <MRadio Label="选项C" Value="c" />
</MRadioGroup>
```

### 带颜色
```razor
<MRadioGroup @bind-Value="_selected" Color="primary">
    <MRadio Label="Primary" Value="1" />
    <MRadio Label="Success" Value="2" Color="success" />
</MRadioGroup>
```

### 常用参数

#### MRadioGroup
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | T | 选中值 |
| Label | String | 标签 |
| Row | Boolean | 横向排列 |
| Column | Boolean | 纵向排列 |
| Mandatory | Boolean | 必须选择 |
| Color | String | 颜色 |
| Dense | Boolean | 紧凑模式 |
| Disabled | Boolean | 禁用 |

#### MRadio
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | T | 选项值 |
| Label | String | 标签 |
| Color | String | 颜色 |
| Disabled | Boolean | 禁用 |
| Readonly | Boolean | 只读 |
| OnIcon | String | 选中图标 |
| OffIcon | String | 未选中图标 |

---

## MOTPInput 验证码输入

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/otp-input

### 基础用法
```razor
<MOTPInput @bind-Value="_otp" Length="6" />
```

### 数字输入
```razor
<MOTPInput @bind-Value="_otp" Length="6" Type="OTPInputType.Number" />
```

### 密码输入
```razor
<MOTPInput @bind-Value="_otp" Length="4" Type="OTPInputType.Password" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | String | 验证码值 |
| Length | Int | 长度 |
| Type | OTPInputType | 类型(Number/Password/Text) |
| Disabled | Boolean | 禁用 |
| Dark | Boolean | 暗色主题 |
| Color | String | 颜色 |
| Plain | Boolean | 朴素样式 |

---

## MImageCaptcha 图片验证码

文档: https://docs.masastack.com/blazor/ui-components/image-captcha

```razor
<MImageCaptcha @bind-Value="_captcha" />
<MImageCaptcha @bind-Value="_captcha" OnRefresh="RefreshCaptcha" />
```


## 事件
### MTextarea
| 事件 | 说明 |
|------|------|
| ValueChanged | 值改变时触发 |
| OnInput | 输入时触发 |
| OnBlur | 失去焦点时触发 |
| OnFocus | 获得焦点时触发 |

### MAutocomplete
| 事件 | 说明 |
|------|------|
| ValueChanged | 选中值改变时触发 |
| OnSearchUpdate | 搜索值更新时触发 |
| OnItemClick | 选项点击时触发 |

### MCascader
| 事件 | 说明 |
|------|------|
| ValueChanged | 选中值改变时触发 |
| OnChange | 值改变时触发 |

### MFileInput
| 事件 | 说明 |
|------|------|
| ValueChanged | 文件改变时触发 |
| OnChange | 文件改变时触发 |

### MSlider
| 事件 | 说明 |
|------|------|
| ValueChanged | 值改变时触发 |
| OnStart | 开始拖拽时触发 |
| OnEnd | 结束拖拽时触发 |

### MRangeSlider
| 事件 | 说明 |
|------|------|
| ValueChanged | 值改变时触发 |

### MRadioGroup
| 事件 | 说明 |
|------|------|
| ValueChanged | 选中值改变时触发 |

### MOTPInput
| 事件 | 说明 |
|------|------|
| ValueChanged | 验证码值改变时触发 |