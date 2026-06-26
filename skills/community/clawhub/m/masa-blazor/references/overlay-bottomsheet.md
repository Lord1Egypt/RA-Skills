# 遮罩与底部弹出

## MOverlay 遮罩

文档: https://docs.masastack.com/blazor/ui-components/overlays

### 基础用法
```razor
<MOverlay Value="_overlay">
    <MProgressCircular Indeterminate Size="64" />
</MOverlay>
```

### 全屏加载
```razor
<MOverlay Absolute Opacity="0.8" Color="white">
    <div class="d-flex flex-column align-center">
        <MProgressCircular Indeterminate Color="primary" />
        <span class="mt-4">加载中...</span>
    </div>
</MOverlay>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Boolean | 是否显示 |
| Absolute | Boolean | 绝对定位 |
| Color | String | 颜色 |
| Dark | Boolean | 暗色 |
| Light | Boolean | 亮色 |
| Opacity | Double | 透明度(0-1) |
| ZIndex | Int/String | z-index |
| Scrim | Boolean | 是否显示遮罩背景 |

---

## MBottomSheet 底部弹出面板

文档: https://docs.masastack.com/blazor/ui-components/bottom-sheets

### 基础用法
```razor
<MButton OnClick="() => _sheet = true">打开底部面板</MButton>

<MBottomSheet @bind-Value="_sheet">
    <MCard>
        <MCardTitle>底部面板</MCardTitle>
        <MCardText>面板内容</MCardText>
        <MCardActions>
            <MButton OnClick="() => _sheet = false">关闭</MButton>
        </MCardActions>
    </MCard>
</MBottomSheet>
```

### 可插入(内嵌)模式
```razor
<MBottomSheet @bind-Value="_sheet" Inset>
    <MCard>
        <MCardText>内嵌面板</MCardText>
    </MCard>
</MBottomSheet>
```

### 带列表
```razor
<MBottomSheet @bind-Value="_sheet">
    <MList>
        <MSubheader>选择操作</MSubheader>
        <MListItem OnClick="Share">
            <MListItemIcon><MIcon>mdi-share</MIcon></MListItemIcon>
            <MListItemContent>分享</MListItemContent>
        </MListItem>
        <MListItem OnClick="Copy">
            <MListItemIcon><MIcon>mdi-content-copy</MIcon></MListItemIcon>
            <MListItemContent>复制</MListItemContent>
        </MListItem>
    </MList>
</MBottomSheet>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Boolean | 是否显示 |
| Inset | Boolean | 内嵌模式 |
| MaxHeight | Int/String | 最大高度 |
| MaxWidth | Int/String | 最大宽度 |
| Persistent | Boolean | 持久化(点击遮罩不关闭) |
| Scrollable | Boolean | 可滚动 |
| OverlayColor | String | 遮罩颜色 |
| OverlayOpacity | Double | 遮罩透明度 |
| Transition | String | 过渡动画 |
| ContentClass | String | 内容CSS类 |
| Dark | Boolean | 暗色主题 |

---

## MModal 模态框

文档: https://docs.masastack.com/blazor/ui-components/modals

```razor
<MButton OnClick="() => _modal = true">打开模态框</MButton>

<MModal @bind-Value="_modal" Width="600">
    <MCard>
        <MCardTitle>模态框</MCardTitle>
        <MCardText>内容</MCardText>
    </MCard>
</MModal>
```

---

## MPopupService 弹出服务

文档: https://docs.masastack.com/blazor/ui-components/popup-service

### 通过服务弹出对话框
```razor
@inject IPopupService PopupService

<MButton OnClick="ShowConfirm">确认对话框</MButton>

@code {
    async Task ShowConfirm()
    {
        var result = await PopupService.PromptAsync(
            "确认删除",
            "确定要删除此记录吗?",
            AlertTypes.Warning);
        
        if (result)
        {
            // 执行删除
        }
    }
}
```

### Alert 弹窗
```razor
await PopupService.AlertAsync("操作成功", AlertTypes.Success);
await PopupService.AlertAsync("操作失败", AlertTypes.Error);
await PopupService.AlertAsync("请注意", AlertTypes.Warning);
```


## 事件
### MOverlay
| 事件 | 说明 |
|------|------|
| ValueChanged | 显示状态改变时触发 |

### MBottomSheet
| 事件 | 说明 |
|------|------|
| ValueChanged | 显示状态改变时触发 |

### MModal
| 事件 | 说明 |
|------|------|
| ValueChanged | 显示状态改变时触发 |