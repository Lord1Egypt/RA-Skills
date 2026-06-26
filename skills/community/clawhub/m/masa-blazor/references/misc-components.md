# 其他常用组件

## MDivider 分割线

文档: https://docs.masastack.com/blazor/ui-components/dividers

```razor
<MDivider />
<MDivider Inset />
<MDivider Vertical />
<MDivider Class="my-4" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Inset | Boolean | 内嵌(不全宽) |
| Vertical | Boolean | 垂直分割线 |
| Light | Boolean | 亮色 |
| Dark | Boolean | 暗色 |

---

## MTooltip 工具提示

文档: https://docs.masastack.com/blazor/ui-components/tooltips

```razor
<MTooltip Top>
    <ActivatorContent>
        <MButton @attributes="context.Attrs">悬停提示</MButton>
    </ActivatorContent>
    <ChildContent>这是一个提示</ChildContent>
</MTooltip>

<MTooltip Bottom Color="primary">
    <ActivatorContent>
        <MIcon @attributes="context.Attrs">mdi-information</MIcon>
    </ActivatorContent>
    <ChildContent>更多信息</ChildContent>
</MTooltip>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Top/Bottom/Left/Right | Boolean | 位置 |
| Color | String | 颜色 |
| Dark | Boolean | 暗色主题 |
| Disabled | Boolean | 禁用 |
| OpenDelay | Int | 打开延迟(ms) |
| CloseDelay | Int | 关闭延迟(ms) |
| MaxWidth | Int/String | 最大宽度 |
| NudgeBottom | Int | 底部微调 |
| NudgeTop | Int | 顶部微调 |
| NudgeLeft | Int | 左侧微调 |
| NudgeRight | Int | 右侧微调 |
| Transition | String | 过渡动画 |
| ContentClass | String | 内容CSS类 |

---

## MFloatingActionButton 浮动操作按钮

文档: https://docs.masastack.com/blazor/ui-components/floating-action-buttons

```razor
<MFloatingActionButton App Fixed Bottom Right Color="primary">
    <MIcon>mdi-plus</MIcon>
</MFloatingActionButton>

<!-- 带菜单 -->
<MFloatingActionButton App Fixed Bottom Right Color="primary">
    <MIcon>mdi-plus</MIcon>
    <template #list>
        <MList>
            <MListItem><MIcon>mdi-email</MIcon></MListItem>
            <MListItem><MIcon>mdi-phone</MIcon></MListItem>
        </MList>
    </template>
</MFloatingActionButton>
```

---

## MFooter 页脚

文档: https://docs.masastack.com/blazor/ui-components/footers

```razor
<MFooter App Dark Color="primary" Padless>
    <MCol Class="text-center" Cols="12">
        <span>&copy; 2024 Company</span>
    </MCol>
</MFooter>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| App | Boolean | 布局模式 |
| Color | String | 颜色 |
| Dark | Boolean | 暗色主题 |
| Fixed | Boolean | 固定定位 |
| Padless | Boolean | 无内边距 |
| Absolute | Boolean | 绝对定位 |
| Inset | Boolean | 内嵌(避开 NavigationDrawer) |
| Height | Int/String | 高度 |
| MinHeight | Int/String | 最小高度 |

---

## MEmptyState 空状态

文档: https://docs.masastack.com/blazor/ui-components/empty-states

```razor
<MEmptyState Icon="mdi-folder-open" Label="暂无数据" Description="请添加数据后查看">
    <MButton Color="primary">添加数据</MButton>
</MEmptyState>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Icon | String | 图标 |
| IconSize | Int/String | 图标大小 |
| Label | String | 标签 |
| Description | String | 描述 |
| Size | Int/String | 尺寸 |
| Color | String | 颜色 |
| Dark | Boolean | 暗色主题 |
| Image | String | 图片URL |
| Text | String | 文本 |

---

## MSyntaxHighlight 代码高亮

文档: https://docs.masastack.com/blazor/ui-components/syntax-highlights

```razor
<MSyntaxHighlight Code="@_code" Language="csharp" />
<MSyntaxHighlight Code="@_html" Language="html" />
<MSyntaxHighlight Code="@_css" Language="css" />
```


## 事件
### MDivider
| 事件 | 说明 |
|------|------|
| (无常用事件) | 纯展示组件 |

### MTooltip
| 事件 | 说明 |
|------|------|
| OnShow | 显示时触发 |
| OnHide | 隐藏时触发 |

### MFloatingActionButton
| 事件 | 说明 |
|------|------|
| OnClick | 点击时触发 |

### MFooter
| 事件 | 说明 |
|------|------|
| (无常用事件) | 主要用于布局 |

### MEmptyState
| 事件 | 说明 |
|------|------|
| OnClickAction | 操作按钮点击时触发 |

### MSyntaxHighlight
| 事件 | 说明 |
|------|------|
| (无常用事件) | 纯展示组件 |