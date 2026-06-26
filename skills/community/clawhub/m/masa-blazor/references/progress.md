# 进度指示器

文档: https://docs.masastack.com/blazor/ui-components/progress

## MProgressLinear 线性进度条

文档: https://docs.masastack.com/blazor/ui-components/progress/progress-linear

### 基础用法
```razor
<MProgressLinear Value="33" Color="primary" />
<MProgressLinear Value="66" Color="success" />
<MProgressLinear Value="100" Color="info" />
```

### 不确定进度(加载)
```razor
<MProgressLinear Indeterminate Color="primary" />
```

### 缓冲进度
```razor
<MProgressLinear Value="33" BufferValue="66" Color="primary" />
```

### 条纹样式
```razor
<MProgressLinear Value="33" Striped Color="primary" />
<MProgressLinear Value="66" Striped Color="success" />
```

### 带插槽
```razor
<MProgressLinear Value="33" Color="primary">
    <strong>33%</strong>
</MProgressLinear>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Double | 进度值(0-100) |
| BufferValue | Double | 缓冲值 |
| Indeterminate | Boolean | 不确定模式(循环动画) |
| Striped | Boolean | 条纹样式 |
| Rounded | Boolean | 圆角 |
| Height | Int/String | 高度 |
| Color | String | 颜色 |
| BackgroundColor | String | 背景色 |
| Dark | Boolean | 暗色主题 |
| Stream | Boolean | 流样式 |
| Active | Boolean | 激活状态 |
| BackgroundOpacity | Double | 背景透明度 |
| Query | Boolean | 查询模式(顶部细条) |

---

## MProgressCircular 圆形进度条

文档: https://docs.masastack.com/blazor/ui-components/progress/progress-circular

### 基础用法
```razor
<MProgressCircular Value="33" Color="primary" />
<MProgressCircular Value="66" Color="success" />
<MProgressCircular Value="100" Color="info" />
```

### 不确定进度(加载)
```razor
<MProgressCircular Indeterminate Color="primary" />
```

### 带尺寸
```razor
<MProgressCircular Indeterminate Size="20" Width="2" Color="primary" />
<MProgressCircular Indeterminate Size="40" Width="3" Color="primary" />
<MProgressCircular Indeterminate Size="60" Width="4" Color="primary" />
<MProgressCircular Indeterminate Size="80" Width="5" Color="primary" />
```

### 带插槽
```razor
<MProgressCircular Value="33" Color="primary">
    33%
</MProgressCircular>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Double | 进度值(0-100) |
| Indeterminate | Boolean | 不确定模式 |
| Size | Int/String | 尺寸 |
| Width | Int/String | 线条宽度 |
| Rotate | Int | 旋转角度 |
| Color | String | 颜色 |
| Dark | Boolean | 暗色主题 |
| Active | Boolean | 激活状态 |


## 事件
MProgressCircular 和 MProgressLinear 是纯展示组件，无常用事件。用于显示加载状态或进度百分比。