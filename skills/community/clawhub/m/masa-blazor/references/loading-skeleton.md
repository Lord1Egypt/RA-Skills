# 加载与骨架屏

## MProgressCircular 环形加载

文档: https://docs.masastack.com/blazor/ui-components/progress/progress-circular

```razor
<!-- 不确定进度(加载中) -->
<MProgressCircular Indeterminate Color="primary" />

<!-- 带文字 -->
<MProgressCircular Indeterminate Color="primary" Size="60" Width="4">
    <span>加载中...</span>
</MProgressCircular>

<!-- 居中加载 -->
<MContainer Fluid Class="d-flex justify-center align-center" Style="height: 200px;">
    <MProgressCircular Indeterminate Color="primary" Size="50" />
</MContainer>
```

## MProgressLinear 线性加载

文档: https://docs.masastack.com/blazor/ui-components/progress/progress-linear

```razor
<!-- 全宽线性加载 -->
<MProgressLinear Indeterminate Color="primary" />

<!-- 卡片内加载 -->
<MCard>
    <MProgressLinear Indeterminate Color="primary" />
    <MCardTitle>加载中</MCardTitle>
    <MCardText>内容区域</MCardText>
</MCard>

<!-- 顶部查询模式 -->
<MProgressLinear Query Indeterminate Color="primary" />
```

## MSkeletonLoader 骨架屏

文档: https://docs.masastack.com/blazor/ui-components/skeleton-loaders

### 基础用法
```razor
<MSkeletonLoader Type="card" Loading="@_loading">
    <MCard>
        <MCardTitle>实际内容</MCardTitle>
        <MCardText>加载完成的内容</MCardText>
    </MCard>
</MSkeletonLoader>
```

### 骨架类型
```razor
<!-- 卡片骨架 -->
<MSkeletonLoader Type="card" />

<!-- 文章骨架 -->
<MSkeletonLoader Type="article" />

<!-- 表格骨架 -->
<MSkeletonLoader Type="table" />

<!-- 表单骨架 -->
<MSkeletonLoader Type="form" />

<!-- 列表骨架 -->
<MSkeletonLoader Type="list-item" />
<MSkeletonLoader Type="list-item-avatar" />
<MSkeletonLoader Type="list-item-two-line" />
<MSkeletonLoader Type="list-item-avatar-two-line" />
<MSkeletonLoader Type="list-item-three-line" />
<MSkeletonLoader Type="list-item-avatar-three-line" />

<!-- 头像骨架 -->
<MSkeletonLoader Type="avatar" />

<!-- 按钮骨架 -->
<MSkeletonLoader Type="button" />

<!-- 图片骨架 -->
<MSkeletonLoader Type="image" />

<!-- 芯片骨架 -->
<MSkeletonLoader Type="chip" />

<!-- 表头骨架 -->
<MSkeletonLoader Type="heading" />

<!-- 文本骨架 -->
<MSkeletonLoader Type="text" />
```

### 组合使用
```razor
<MSkeletonLoader Type="card-heading, list-item-avatar-three-line, actions" Loading="@_loading">
    <MCard>
        <MCardTitle>标题</MCardTitle>
        <MCardText>内容</MCardText>
        <MCardActions>
            <MButton>操作</MButton>
        </MCardActions>
    </MCard>
</MSkeletonLoader>
```

### 自定义样式
```razor
<MSkeletonLoader Type="card" Boilerplate />
<MSkeletonLoader Type="card" Loading="@_loading" Dark />
<MSkeletonLoader Type="card" Elevation="2" />
<MSkeletonLoader Type="card" Tile />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Type | String | 骨架类型 |
| Loading | Boolean | 加载状态 |
| Boilerplate | Boolean | 无动画模式 |
| Dark | Boolean | 暗色主题 |
| Elevation | Int | 阴影层级 |
| Tile | Boolean | 直角 |
| Transition | String | 过渡动画 |
| Types | Dictionary | 自定义骨架类型配置 |
| Light | Boolean | 亮色主题 |
| BoneColor | String | 骨架颜色 |
| Color | String | 颜色 |

---

## MLazy 懒加载

文档: https://docs.masastack.com/blazor/ui-components/lazy

```razor
<!-- 进入视口时加载 -->
<MLazy MinHeight="200" Options="@_options">
    <MCard>
        <MCardTitle>懒加载内容</MCardTitle>
        <MCardText>进入视口时才会渲染</MCardText>
    </MCard>
</MLazy>

@code {
    IntersectionObserverOptions _options = new() { Threshold = 0.5 };
}
```


## 事件
### MSkeletonLoader
| 事件 | 说明 |
|------|------|
| (无常用事件) | 主要用于展示加载状态 |

### MLazy
| 事件 | 说明 |
|------|------|
| OnIntersect | 进入视口时触发 |