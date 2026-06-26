# 工具栏与应用栏

## MToolbar 工具栏

文档: https://docs.masastack.com/blazor/ui-components/bars/toolbars

### 基础用法
```razor
<MToolbar Dark Color="primary">
    <MToolbarTitle>应用标题</MToolbarTitle>
    <MSpacer />
    <MButton Icon><MIcon>mdi-magnify</MIcon></MButton>
    <MButton Icon><MIcon>mdi-dots-vertical</MIcon></MButton>
</MToolbar>
```

### 带导航图标
```razor
<MToolbar>
    <MAppBarNavIcon OnClick="ToggleDrawer" />
    <MToolbarTitle>标题</MToolbarTitle>
    <MSpacer />
    <MButton Icon><MIcon>mdi-bell</MIcon></MButton>
</MToolbar>
```

### Dense 模式
```razor
<MToolbar Dense>
    <MToolbarTitle>Dense 工具栏</MToolbarTitle>
</MToolbar>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Color | String | 颜色 |
| Dark | Boolean | 暗色主题 |
| Dense | Boolean | 紧凑模式 |
| Flat | Boolean | 无阴影 |
| Floating | Boolean | 浮动 |
| Prominent | Boolean | 突出显示(双倍高度) |
| Short | Boolean | 短工具栏 |
| Collapse | Boolean | 折叠模式 |
| Elevation | Int | 阴影层级 |
| ExtensionHeight | Int | 扩展区域高度 |
| Fixed | Boolean | 固定定位 |
| ClippedLeft | Boolean | 左侧裁剪 |
| ClippedRight | Boolean | 右侧裁剪 |
| ShrinkOnScroll | Boolean | 滚动缩小 |
| HideOnScroll | Boolean | 滚动隐藏 |
| InvertedScroll | Boolean | 反向滚动 |
| ScrollTarget | String | 滚动目标 |
| ScrollThreshold | Int | 滚动阈值 |
| Img | String | 背景图片 |
| MaxHeight | Int/String | 最大高度 |

---

## MAppBar 应用栏

文档: https://docs.masastack.com/blazor/ui-components/bars/app-bars

### 基础用法
```razor
<MAppBar App Dark Color="primary">
    <MAppBarNavIcon />
    <MAppBarTitle>应用名称</MAppBarTitle>
    <MSpacer />
    <MButton Icon><MIcon>mdi-magnify</MIcon></MButton>
</MAppBar>

<MMain>
    <!-- 页面内容 -->
</MMain>
```

### 可折叠
```razor
<MAppBar App ShrinkOnScroll>
    <MAppBarNavIcon />
    <MAppBarTitle>标题</MAppBarTitle>
    <MSpacer />
    <template #extension>
        <MTabs>
            <MTab>标签1</MTab>
            <MTab>标签2</MTab>
        </MTabs>
    </template>
</MAppBar>
```

### 带图片背景
```razor
<MAppBar App Color="primary" Dark>
    <template #img="{ props }">
        <MImage Src="bg.jpg" Bind="props" Cover />
    </template>
    <MAppBarTitle>带背景的应用栏</MAppBarTitle>
</MAppBar>
```

### 常用参数
与 MToolbar 类似，额外参数：
| 参数 | 类型 | 说明 |
|------|------|------|
| App | Boolean | 布局模式 |
| ClippedLeft | Boolean | 左侧裁剪(配合 NavigationDrawer) |
| ClippedRight | Boolean | 右侧裁剪 |
| ElevateOnScroll | Boolean | 滚动时增加阴影 |
| FadeImgOnScroll | Boolean | 滚动时图片渐隐 |
| HideOnScroll | Boolean | 滚动隐藏 |
| InvertedScroll | Boolean | 向下滚动显示 |
| ScrollOffScreen | Boolean | 滚动时离开屏幕 |
| Value | Boolean | 是否显示 |

---

## MSystemBar 系统栏

文档: https://docs.masastack.com/blazor/ui-components/bars/system-bars

```razor
<MSystemBar App Dark Color="primary">
    <MIcon>mdi-wifi-strength-4</MIcon>
    <MIcon>mdi-signal-cellular</MIcon>
    <MIcon>mdi-battery</MIcon>
    <span>12:30</span>
</MSystemBar>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| App | Boolean | 布局模式 |
| Color | String | 颜色 |
| Dark | Boolean | 暗色主题 |
| Fixed | Boolean | 固定定位 |
| Height | Int/String | 高度 |
| LightsOut | Boolean | 关灯模式 |
| Window | Boolean | 窗口模式 |


## 事件
### MToolbar/MAppBar
| 事件 | 说明 |
|------|------|
| OnScroll | 滚动时触发 |