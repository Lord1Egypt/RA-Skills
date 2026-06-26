# MDialog 对话框

文档: https://docs.masastack.com/blazor/ui-components/dialogs

## 基础用法
```razor
<MButton Color="primary" OnClick="() => _dialog = true">打开对话框</MButton>

<MDialog @bind-Value="_dialog" Width="500">
    <MCard>
        <MCardTitle>对话框标题</MCardTitle>
        <MCardText>这是对话框内容</MCardText>
        <MCardActions>
            <MSpacer />
            <MButton Text OnClick="() => _dialog = false">取消</MButton>
            <MButton Color="primary" OnClick="() => _dialog = false">确定</MButton>
        </MCardActions>
    </MCard>
</MDialog>

@code {
    bool _dialog = false;
}
```

## 全屏对话框
```razor
<MDialog @bind-Value="_dialog" Fullscreen>
    <MCard>
        <MToolbar Dark Color="primary">
            <MButton Icon OnClick="() => _dialog = false">
                <MIcon>mdi-close</MIcon>
            </MButton>
            <MToolbarTitle>全屏对话框</MToolbarTitle>
            <MSpacer />
        </MToolbar>
        <MCardText>全屏内容区域</MCardText>
    </MCard>
</MDialog>
```

## 持久化对话框(不可点击遮罩关闭)
```razor
<MDialog @bind-Value="_dialog" Persistent Width="400">
    <MCard>
        <MCardTitle>请确认</MCardTitle>
        <MCardText>确定要删除此记录吗?</MCardText>
        <MCardActions>
            <MSpacer />
            <MButton Text OnClick="() => _dialog = false">取消</MButton>
            <MButton Color="error" OnClick="Confirm">确认删除</MButton>
        </MCardActions>
    </MCard>
</MDialog>
```

## 可滚动内容
```razor
<MDialog @bind-Value="_dialog" Scrollable Width="500">
    <MCard>
        <MCardTitle>长内容</MCardTitle>
        <MCardText Style="max-height: 300px;">
            @for (int i = 0; i < 50; i++)
            {
                <p>内容行 @i</p>
            }
        </MCardText>
        <MCardActions>
            <MSpacer />
            <MButton Color="primary" OnClick="() => _dialog = false">关闭</MButton>
        </MCardActions>
    </MCard>
</MDialog>
```

## 带加载器
```razor
<MDialog @bind-Value="_dialog" Width="400" ContentClass="pa-0">
    <MCard>
        <MCardTitle>加载中...</MCardTitle>
        <MProgressLinear Indeterminate Color="primary" />
        <MCardText>请稍候</MCardText>
    </MCard>
</MDialog>
```

## 嵌套对话框
```razor
<MDialog @bind-Value="_dialog1" Width="500">
    <MCard>
        <MCardTitle>外层对话框</MCardTitle>
        <MCardActions>
            <MButton OnClick="() => _dialog2 = true">打开内层</MButton>
        </MCardActions>
    </MCard>
</MDialog>

<MDialog @bind-Value="_dialog2" Width="300">
    <MCard>
        <MCardTitle>内层对话框</MCardTitle>
        <MCardActions>
            <MButton OnClick="() => _dialog2 = false">关闭</MButton>
        </MCardActions>
    </MCard>
</MDialog>
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Boolean | 是否显示(双向绑定) |
| Width | Int/String | 宽度 |
| MaxWidth | Int/String | 最大宽度 |
| MinWidth | Int/String | 最小宽度 |
| Height | Int/String | 高度 |
| MaxHeight | Int/String | 最大高度 |
| Fullscreen | Boolean | 全屏 |
| Persistent | Boolean | 持久化(点击遮罩不关闭) |
| Scrollable | Boolean | 可滚动 |
| Transition | String | 过渡动画(dialog-transition等) |
| OverlayColor | String | 遮罩颜色 |
| OverlayOpacity | Double | 遮罩透明度 |
| ContentClass | String | 内容区CSS类 |
| NoClickAnimation | Boolean | 禁用点击动画 |
| Attach | String | 挂载位置 |
| Origin | String | 动画原点 |
| Dark | Boolean | 暗色主题 |

## 事件
| 事件 | 说明 |
|------|------|
| ValueChanged | 值改变时触发 |
| OnOutsideClick | 点击遮罩时触发 |
