# MAlert 警告提示

文档: https://docs.masastack.com/blazor/ui-components/alerts

## 基础用法
```razor
<MAlert Type="AlertTypes.Success">操作成功！</MAlert>
<MAlert Type="AlertTypes.Error">操作失败！</MAlert>
<MAlert Type="AlertTypes.Warning">请注意！</MAlert>
<MAlert Type="AlertTypes.Info">这是一条信息。</MAlert>
```

## 可关闭
```razor
<MAlert Type="AlertTypes.Success" Dismissible>
    可关闭的警告
    <OnCloseContent>
        <MButton Icon OnClick="() => _alert = false">
            <MIcon>mdi-close</MIcon>
        </MButton>
    </OnCloseContent>
</MAlert>
```

## 带图标
```razor
<MAlert Type="AlertTypes.Success" Icon="mdi-check-circle">
    带图标的警告
</MAlert>

<MAlert Type="AlertTypes.Error" Icon="mdi-alert-circle">
    错误警告
</MAlert>
```

## Outlined/Text 样式
```razor
<MAlert Type="AlertTypes.Success" Outlined>描边样式</MAlert>
<MAlert Type="AlertTypes.Success" Text>文本样式</MAlert>
<MAlert Type="AlertTypes.Success" Border="Borders.Left">左边框</MAlert>
<MAlert Type="AlertTypes.Success" Border="Borders.Top">上边框</MAlert>
<MAlert Type="AlertTypes.Success" Border="Borders.Right">右边框</MAlert>
<MAlert Type="AlertTypes.Success" Border="Borders.Bottom">下边框</MAlert>
```

## 密集模式
```razor
<MAlert Type="AlertTypes.Info" Dense>紧凑警告</MAlert>
<MAlert Type="AlertTypes.Info" Dense Outlined>紧凑描边</MAlert>
<MAlert Type="AlertTypes.Info" Dense Text>紧凑文本</MAlert>
```

## 自定义颜色
```razor
<MAlert Color="purple" Dark>自定义颜色</MAlert>
<MAlert Color="cyan" Dark Icon="mdi-information">自定义带图标</MAlert>
```

## Colored Border
```razor
<MAlert Type="AlertTypes.Success" Border="Borders.Left" ColoredBorder>
    彩色边框
</MAlert>
```

## Prominent 样式
```razor
<MAlert Type="AlertTypes.Info" Prominent>
    <MIcon Left>mdi-information</MIcon>
    突出显示的警告
</MAlert>
```

## Elevation 阴影
```razor
<MAlert Type="AlertTypes.Success" Elevation="2">带阴影的警告</MAlert>
```

## 组合使用
```razor
<MAlert Type="AlertTypes.Warning"
        Icon="mdi-alert"
        Dismissible
        Dense
        Border="Borders.Left"
        ColoredBorder
        Elevation="2">
    <MRow NoGutters Align="AlignTypes.Center">
        <MCol>
            <div class="text-body-2 font-weight-bold">警告标题</div>
            <div class="text-caption">详细的警告信息内容</div>
        </MCol>
        <MCol Cols="auto">
            <MButton Small Text>查看详情</MButton>
        </MCol>
    </MRow>
</MAlert>
```

## 条件渲染
```razor
@if (_showAlert)
{
    <MAlert Type="AlertTypes.Success"
            Dismissible
            OnCloseClick="() => _showAlert = false">
        操作成功！
    </MAlert>
}

@code {
    bool _showAlert = true;
}
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Type | AlertTypes | 类型(Success/Error/Warning/Info) |
| Color | String | 自定义颜色 |
| Icon | String | 图标 |
| Dismissible | Boolean | 可关闭 |
| Dense | Boolean | 紧凑模式 |
| Outlined | Boolean | 描边样式 |
| Text | Boolean | 文本样式 |
| Border | Borders | 边框位置(Left/Right/Top/Bottom) |
| ColoredBorder | Boolean | 彩色边框 |
| Dark | Boolean | 暗色主题 |
| Prominent | Boolean | 突出显示 |
| Shaped | Boolean | 形状样式 |
| Tile | Boolean | 直角 |
| Rounded | Boolean/String | 圆角 |
| Elevation | Int | 阴影层级(0-24) |
| Transition | String | 过渡动画 |
| Value | Boolean | 是否显示 |
| CloseIcon | String | 关闭图标 |
| CloseLabel | String | 关闭按钮标签 |
| Width | Int/String | 宽度 |

## 事件
| 事件 | 说明 |
|------|------|
| OnCloseClick | 关闭按钮点击时触发 |

## AlertTypes 枚举值
- `AlertTypes.Success` — 成功
- `AlertTypes.Error` — 错误
- `AlertTypes.Warning` — 警告
- `AlertTypes.Info` — 信息
