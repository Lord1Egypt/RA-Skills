# MSnackbar 消息提示

文档: https://docs.masastack.com/blazor/ui-components/snackbars

## 基础用法
```razor
<MButton OnClick="() => _snackbar = true">显示消息</MButton>

<MSnackbar @bind-Value="_snackbar" Timeout="3000">
    操作成功！
</MSnackbar>
```

## 带操作按钮
```razor
<MSnackbar @bind-Value="_snackbar" MultiLine>
    文件已删除
    <ActionContent>
        <MButton Color="pink" Text OnClick="Undo">撤销</MButton>
    </ActionContent>
</MSnackbar>
```

## 不同位置
```razor
<!-- 顶部居中(默认) -->
<MSnackbar @bind-Value="_s1" Top Centered>顶部居中</MSnackbar>

<!-- 顶部左侧 -->
<MSnackbar @bind-Value="_s2" Top Left>顶部左侧</MSnackbar>

<!-- 底部居中 -->
<MSnackbar @bind-Value="_s3" Bottom Centered>底部居中</MSnackbar>

<!-- 底部右侧 -->
<MSnackbar @bind-Value="_s4" Bottom Right>底部右侧</MSnackbar>
```

## 不同颜色
```razor
<MSnackbar Color="success" @bind-Value="_s1">成功消息</MSnackbar>
<MSnackbar Color="error" @bind-Value="_s2">错误消息</MSnackbar>
<MSnackbar Color="warning" @bind-Value="_s3">警告消息</MSnackbar>
<MSnackbar Color="info" @bind-Value="_s4">信息消息</MSnackbar>
```

## 通过服务调用
```razor
@inject IPopupService PopupService

<MButton OnClick="ShowMessage">显示</MButton>

@code {
    async Task ShowMessage()
    {
        await PopupService.EnqueueSnackbarAsync("操作成功", AlertTypes.Success);
    }
}
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Boolean | 是否显示(双向绑定) |
| Timeout | Int | 自动关闭时间(ms), -1不关闭 |
| Color | String | 颜色 |
| Dark | Boolean | 暗色主题 |
| Top | Boolean | 显示在顶部 |
| Bottom | Boolean | 显示在底部 |
| Left | Boolean | 显示在左侧 |
| Right | Boolean | 显示在右侧 |
| Centered | Boolean | 水平居中 |
| MultiLine | Boolean | 多行模式 |
| Shaped | Boolean | 形状样式 |
| Outlined | Boolean | 描边样式 |
| Text | Boolean | 文本样式 |
| Rounded | Boolean/String | 圆角 |
| Tile | Boolean | 直角 |
| Vertical | Boolean | 垂直布局 |
| CloseButton | Boolean | 显示关闭按钮 |
| CloseIcon | String | 关闭图标 |
| Transition | String | 过渡动画 |
| ContentClass | String | 内容CSS类 |



## 事件
| 事件 | 说明 |
|------|------|
| ValueChanged | 显示状态改变时触发 |
| OnCloseClick | 关闭按钮点击时触发 |