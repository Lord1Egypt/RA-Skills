# 补充组件

## MSheet 面板

文档: https://docs.masastack.com/blazor/ui-components/sheets

```razor
<MSheet Class="pa-4" Color="grey lighten-3">
    面板内容
</MSheet>

<MSheet Class="pa-4" Elevation="2" Rounded>
    带阴影的面板
</MSheet>

<MSheet Outlined Class="pa-4">
    描边面板
</MSheet>

<MSheet Tile Elevation="1" Class="pa-4" Width="300" Height="200">
    直角面板(固定尺寸)
</MSheet>
```

### 常用参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| ChildContent | RenderFragment | — | 子内容 |
| Tag | String | "div" | HTML 标签 |
| Show | Boolean? | null | 是否显示 |
| Outlined | Boolean | false | 描边样式 |
| Shaped | Boolean | false | 形状样式(右侧保留圆角) |
| Elevation | StringNumber | — | 阴影层级(0-24) |
| Rounded | StringBoolean | — | 圆角(true/false/"pill"/"circle"等) |
| Tile | Boolean | false | 直角(无圆角) |
| Color | String | — | 颜色 |
| Width | StringNumber | — | 宽度 |
| MaxWidth | StringNumber | — | 最大宽度 |
| MinWidth | StringNumber | — | 最小宽度 |
| Height | StringNumber | — | 高度 |
| MaxHeight | StringNumber | — | 最大高度 |
| MinHeight | StringNumber | — | 最小高度 |

### 事件
无特有事件（通用容器组件，无回调事件）。

---

## MBanner 横幅

文档: https://docs.masastack.com/blazor/ui-components/banners

```razor
<MBanner Icon="mdi-wifi-strength-alert-outline" Color="warning">
    <ChildContent>
        网络连接不稳定
    </ChildContent>
    <ActionsContent>
        <MButton Text Color="primary">重试</MButton>
    </ActionsContent>
</MBanner>

<MBanner SingleLine Sticky>
    <ChildContent>单行横幅</ChildContent>
    <ActionsContent>
        <MButton Text>关闭</MButton>
    </ActionsContent>
</MBanner>

<!-- 可关闭横幅 -->
<MBanner @bind-Value="_show" Icon="mdi-information">
    <ChildContent>可关闭横幅</ChildContent>
</MBanner>
```

### 常用参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| Value | Boolean | true | 是否显示（双向绑定） |
| Icon | String | — | 图标 |
| IconColor | String | — | 图标颜色 |
| Color | String | — | 背景颜色 |
| Elevation | StringNumber | 0 | 阴影层级 |
| SingleLine | Boolean | false | 单行模式 |
| Sticky | Boolean | false | 吸顶粘性定位 |
| App | Boolean | false | 应用模式(与 App Bar 联动) |
| IconContent | RenderFragment | — | 自定义图标插槽 |
| ActionsContent | RenderFragment<Action> | — | 操作按钮插槽(回调可关闭横幅) |
| ChildContent | RenderFragment | — | 主内容插槽 |

### 事件
| 事件 | 说明 |
|------|------|
| ValueChanged | 显示状态改变时触发 |
| OnIconClick | 图标点击时触发 |

---

## MBorders 边框

文档: https://docs.masastack.com/blazor/ui-components/borders

MBorders 是 CSS 工具类，不是 Blazor 组件，直接在元素上使用 class。

```razor
<!-- 边框颜色 -->
<div class="border border-primary">主色边框</div>
<div class="border border-error">错误边框</div>

<!-- 边框位置 -->
<div class="border-s">左边框</div>
<div class="border-e">右边框</div>
<div class="border-t">上边框</div>
<div class="border-b">下边框</div>

<!-- 边框样式 -->
<div class="border-dashed">虚线边框</div>
<div class="border-dotted">点状边框</div>

<!-- 宽度 -->
<div class="border-lg">粗边框</div>
<div class="border-sm">细边框</div>
<div class="border-0">无边框</div>
```

### 常用 CSS 类
| 类名 | 说明 |
|------|------|
| border | 四边边框 |
| border-s / border-e | 左/右边框 |
| border-t / border-b | 上/下边框 |
| border-0 | 移除边框 |
| border-sm / border-lg | 边框粗细 |
| border-{color} | 边框颜色(primary/error/success等) |
| border-dashed | 虚线边框 |
| border-dotted | 点状边框 |

### 事件
不适用（CSS 工具类，非组件）。

---

## MImageCaptcha 图片验证码

文档: https://docs.masastack.com/blazor/ui-components/image-captcha

```razor
<MImageCaptcha @bind-Value="_captcha" />

<!-- 带刷新回调 -->
<MImageCaptcha @bind-Value="_captcha" OnRefresh="RefreshCaptcha" />

@code {
    string _captcha;
    void RefreshCaptcha() { /* 重新生成验证码 */ }
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | String | 验证码值（双向绑定） |
| Width | Int/String | 验证码图片宽度 |
| Height | Int/String | 验证码图片高度 |

### 事件
| 事件 | 说明 |
|------|------|
| ValueChanged | 验证码值改变时触发 |
| OnRefresh | 刷新验证码时触发 |

---

## MCron Cron 表达式

文档: https://docs.masastack.com/blazor/ui-components/cron

```razor
<MCron @bind-Value="_cron" />

@code {
    string _cron = "0 0 * * *";
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | String | Cron 表达式值（双向绑定） |
| Locale | String | 语言(zh/en) |

### 事件
| 事件 | 说明 |
|------|------|
| ValueChanged | Cron 表达式改变时触发 |

---

## MDrawflow 流程图

文档: https://docs.masastack.com/blazor/ui-components/drawflow

```razor
<MDrawflow @ref="_drawflow" Style="height: 500px;"
           OnNodeCreated="OnCreated"
           OnNodeRemoved="OnRemoved" />

@code {
    MDrawflow _drawflow;

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            await _drawflow.AddNodeAsync("start", 1, 1, 100, 100, 0, 0,
                "start-node", new { label = "开始" }, "<div>开始节点</div>");
        }
    }

    void OnCreated(string nodeId) { /* 节点创建 */ }
    void OnRemoved(string nodeId) { /* 节点删除 */ }
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Mode | DrawflowEditorMode | 编辑模式(Edit/Fixed/View) |
| DataInitializer | Func<ValueTask<string>> | 初始化数据加载回调 |

### 事件
| 事件 | 说明 |
|------|------|
| OnNodeCreated | 节点创建时触发 |
| OnNodeRemoved | 节点删除时触发 |
| OnNodeSelected | 节点选中时触发 |
| OnNodeUnselected | 节点取消选中时触发 |
| OnNodeDataChanged | 节点数据变更时触发 |
| OnContextmenu | 右键菜单时触发 |
| OnConnectionStart | 连线开始时触发 |
| OnConnectionCancel | 连线取消时触发 |
| OnMouseUp | 鼠标抬起时触发 |
| OnImport | 数据导入完成时触发 |

### 方法
| 方法 | 说明 |
|------|------|
| AddNodeAsync(name, inputs, outputs, x, y, ...) | 添加节点 |
| RemoveNodeAsync(nodeId) | 删除节点 |
| GetNodeFromIdAsync<T>(nodeId) | 获取节点数据 |
| UpdateNodeDataAsync(nodeId, data) | 更新节点数据 |
| UpdateNodeHTMLAsync(nodeId, html) | 更新节点 HTML |
| ClearAsync() | 清空画布 |
| ImportAsync(json) | 导入数据 |
| ExportAsync(indented) | 导出数据 |
| AddInputAsync(nodeId) | 添加输入端口 |
| AddOutputAsync(nodeId) | 添加输出端口 |
| RemoveInputAsync(nodeId, inputClass) | 删除输入端口 |
| RemoveOutputAsync(nodeId, outputClass) | 删除输出端口 |
| FocusNodeAsync(nodeId) | 聚焦节点 |
| CenterNodeAsync(nodeId, animate) | 居中节点 |
| AddConnectionAsync(outputId, inputId, ...) | 添加连线 |

---

## MGridStack 网格堆叠

文档: https://docs.masastack.com/blazor/ui-components/gridstack

```razor
<MGridStack @bind-Items="_items" ColumnCount="12" CellHeight="80">
    @foreach (var item in _items)
    {
        <MGridStackItem X="@item.X" Y="@item.Y" W="@item.W" H="@item.H">
            <MCard Class="pa-2">@item.Content</MCard>
        </MGridStackItem>
    }
</MGridStack>

@code {
    List<GridStackItem> _items = new()
    {
        new() { X = 0, Y = 0, W = 4, H = 2, Content = "项目1" },
        new() { X = 4, Y = 0, W = 4, H = 2, Content = "项目2" }
    };
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Items | IEnumerable | 网格项目集合 |
| ColumnCount | Int | 列数(默认12) |
| CellHeight | Int/String | 单元格高度 |
| Margin | Int/String | 间距 |
| Draggable | Boolean/String | 是否可拖拽 |
| Resizable | Boolean/String | 是否可调整大小 |
| Readonly | Boolean | 只读模式 |

### MGridStackItem 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| X | Int | X 坐标(列位置) |
| Y | Int | Y 坐标(行位置) |
| W | Int | 宽度(占列数) |
| H | Int | 高度(占行数) |
| MinW | Int | 最小宽度 |
| MinH | Int | 最小高度 |
| MaxW | Int | 最大宽度 |
| MaxH | Int | 最大高度 |
| NoResize | Boolean | 禁止调整大小 |
| NoMove | Boolean | 禁止移动 |
| Id | String | 项目 ID |
| Locked | Boolean | 锁定位置 |

### 事件
| 事件 | 说明 |
|------|------|
| ItemsChanged | 项目集合改变时触发 |
| OnDragStart | 拖拽开始时触发 |
| OnDragStop | 拖拽结束时触发 |
| OnResizeStart | 调整大小开始时触发 |
| OnResizeStop | 调整大小结束时触发 |

---

## MBaiduMap 百度地图

文档: https://docs.masastack.com/blazor/ui-components/baidumaps

```razor
<MBaiduMap Center="@_center" Zoom="15" Style="height: 400px;"
           OnClick="HandleMapClick" />

@code {
    BaiduMapPoint _center = new(116.404, 39.915);
    void HandleMapClick(BaiduMapPoint point) { /* 处理点击 */ }
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Center | BaiduMapPoint | 地图中心点坐标 |
| Zoom | Int | 缩放级别(3-19) |
| MinZoom | Int | 最小缩放级别 |
| MaxZoom | Int | 最大缩放级别 |
| EnableScrollWheelZoom | Boolean | 启用滚轮缩放 |
| EnableDragging | Boolean | 启用拖拽 |
| EnableDoubleClickZoom | Boolean | 启用双击缩放 |
| MapType | BaiduMapType | 地图类型(普通/卫星/混合) |
| Style | String | 地图容器样式 |

### 事件
| 事件 | 说明 |
|------|------|
| OnClick | 地图点击时触发 |
| OnDoubleClick | 地图双击时触发 |
| OnZoomChange | 缩放级别改变时触发 |
| OnMoveEnd | 地图移动结束时触发 |
| OnLoad | 地图加载完成时触发 |

---

## MInteractiveTrigger 交互触发

文档: https://docs.masastack.com/blazor/ui-components/interactive-trigger

```razor
<MInteractiveTrigger TValue="string" InteractiveValue="target"
                     @bind-Value="_current">
    <MButton>点击触发</MButton>
</MInteractiveTrigger>

<!-- 带弹出菜单 -->
<MInteractivePopup>
    <ActivatorContent>
        <MButton @attributes="context.Attrs">打开菜单</MButton>
    </ActivatorContent>
    <ChildContent>
        <MList>
            <MListItem>选项1</MListItem>
            <MListItem>选项2</MListItem>
        </MList>
    </ChildContent>
</MInteractivePopup>
```

### 常用参数（MInteractiveTrigger）
| 参数 | 类型 | 说明 |
|------|------|------|
| TValue | Type | 值类型 |
| Value | TValue | 当前值（双向绑定） |
| InteractiveValue | TValue | 触发交互的目标值 |

### 常用参数（MInteractivePopup）
| 参数 | 类型 | 说明 |
|------|------|------|
| ActivatorContent | RenderFragment<ActivatorProps> | 激活器内容插槽 |
| ChildContent | RenderFragment | 弹出内容插槽 |

### 事件
| 事件 | 说明 |
|------|------|
| ValueChanged | 值改变时触发 |

---

## MVirtualScroll 虚拟滚动

文档: https://docs.masastack.com/blazor/ui-components/virtual-scroll

```razor
<MVirtualScroll Items="@_items" ItemSize="50" Height="400">
    <ItemContent>
        <MListItem>@context</MListItem>
        <MDivider />
    </ItemContent>
</MVirtualScroll>

<!-- 自定义尺寸 -->
<MVirtualScroll Items="@_items" ItemSize="80" Height="600" OverscanCount="5">
    <ItemContent>
        <MListItem TwoLine>
            <MListItemContent>
                <MListItemTitle>@context.Name</MListItemTitle>
                <MListItemSubtitle>@context.Desc</MListItemSubtitle>
            </MListItemContent>
        </MListItem>
    </ItemContent>
</MVirtualScroll>
```

### 常用参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| Items | ICollection<TItem> | — | 数据源 |
| ItemContent | RenderFragment<TItem> | — | 每项内容模板 |
| FooterContent | RenderFragment | — | 底部内容插槽 |
| ItemSize | Float | 50 | 每项高度(px) |
| OverscanCount | Int | 3 | 视口外预渲染项数 |
| Height | StringNumber | — | 容器高度 |
| MaxHeight | StringNumber | — | 最大高度 |
| MinHeight | StringNumber | — | 最小高度 |
| Width | StringNumber | — | 容器宽度 |
| MaxWidth | StringNumber | — | 最大宽度 |
| MinWidth | StringNumber | — | 最小宽度 |

### 事件
无特有事件（纯展示型虚拟滚动组件）。

---

## MXgplayer 西瓜播放器

文档: https://docs.masastack.com/blazor/ui-components/xgplayer

```razor
<!-- 基础视频 -->
<MXgplayer Src="video.mp4" Style="height: 400px;" />

<!-- HLS 直播流 -->
<MXgplayer Src="https://example.com/live/stream.m3u8"
           IsLive="true"
           Style="height: 400px;" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Src | String | 视频源地址 |
| Poster | String | 封面图地址 |
| Autoplay | Boolean | 自动播放 |
| Loop | Boolean | 循环播放 |
| Muted | Boolean | 静音 |
| Volume | Double | 音量(0-1) |
| PlaybackRate | Double | 播放速率 |
| IsLive | Boolean | 直播模式 |
| Fluid | Boolean | 流式布局(自适应宽度) |
| Style | String | 容器样式 |
| Class | String | CSS 类 |

### 事件
| 事件 | 说明 |
|------|------|
| OnPlay | 播放时触发 |
| OnPause | 暂停时触发 |
| OnEnded | 播放结束时触发 |
| OnTimeUpdate | 播放进度更新时触发 |
| OnError | 播放出错时触发 |

---

## MVideoFeeder 视频播放

文档: https://docs.masastack.com/blazor/ui-components/video-feeder

```razor
<MVideoFeeder Src="video.mp4" Style="height: 400px;" />

<MVideoFeeder Src="video.mp4" Autoplay Loop Muted Style="height: 300px;" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Src | String | 视频源地址 |
| Autoplay | Boolean | 自动播放 |
| Loop | Boolean | 循环播放 |
| Muted | Boolean | 静音 |
| Controls | Boolean | 显示控制条 |
| Poster | String | 封面图地址 |
| Style | String | 容器样式 |

### 事件
| 事件 | 说明 |
|------|------|
| OnPlay | 播放时触发 |
| OnPause | 暂停时触发 |
| OnEnded | 播放结束时触发 |

---

## MPageTabs 页面标签页

文档: https://docs.masastack.com/blazor/ui-components/page-tabs

```razor
<MPageTabs @bind-Value="_currentTab">
    <MPageTab Value="tab1" Title="页面1">
        <Page1 />
    </MPageTab>
    <MPageTab Value="tab2" Title="页面2">
        <Page2 />
    </MPageTab>
    <MPageTab Value="tab3" Title="页面3" Closable>
        <Page3 />
    </MPageTab>
</MPageTabs>

@code {
    string _currentTab = "tab1";
}
```

### 常用参数（MPageTabs）
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | String | 当前激活的标签页值（双向绑定） |
| Dark | Boolean | 暗色主题 |
| Color | String | 标签栏颜色 |
| Dense | Boolean | 紧凑模式 |
| FixedTabs | Boolean | 固定标签宽度 |
| Centered | Boolean | 标签居中 |
| HideSlider | Boolean | 隐藏滑动指示条 |

### MPageTab 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | String | 标签页唯一标识 |
| Title | String | 标签标题 |
| Icon | String | 标签图标 |
| Closable | Boolean | 可关闭 |
| Disabled | Boolean | 禁用 |
| Href | String | 链接地址 |
| ChildContent | RenderFragment | 标签页内容 |

### 事件
| 事件 | 说明 |
|------|------|
| ValueChanged | 当前标签页改变时触发 |
| OnClose | 标签页关闭时触发 |
