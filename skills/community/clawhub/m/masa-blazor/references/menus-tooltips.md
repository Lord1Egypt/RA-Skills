# MMenu 菜单

文档: https://docs.masastack.com/blazor/ui-components/menus

## 基础用法
```razor
<MMenu @bind-Value="_menu">
    <ActivatorContent>
        <MButton @attributes="context.Attrs">打开菜单</MButton>
    </ActivatorContent>
    <ChildContent>
        <MList>
            <MListItem OnClick="() => {}">选项1</MListItem>
            <MListItem OnClick="() => {}">选项2</MListItem>
            <MListItem OnClick="() => {}">选项3</MListItem>
        </MList>
    </ChildContent>
</MMenu>
```

## 下拉菜单
```razor
<MMenu Bottom OffsetY>
    <ActivatorContent>
        <MButton @attributes="context.Attrs">
            下拉菜单
            <MIcon Right>mdi-menu-down</MIcon>
        </MButton>
    </ActivatorContent>
    <ChildContent>
        <MList Dense>
            <MListItem><MListItemTitle>编辑</MListItemTitle></MListItem>
            <MListItem><MListItemTitle>删除</MListItemTitle></MListItem>
            <MDivider />
            <MListItem><MListItemTitle>详情</MListItemTitle></MListItem>
        </MList>
    </ChildContent>
</MMenu>
```

## 上下文菜单(右键)
```razor
<MMenu @bind-Value="_menu" Absolute OffsetX OffsetY>
    <ActivatorContent>
        <div @attributes="context.Attrs" Style="height: 200px; background: #eee;">
            右键点击此区域
        </div>
    </ActivatorContent>
    <ChildContent>
        <MList Dense>
            <MListItem>复制</MListItem>
            <MListItem>粘贴</MListItem>
            <MListItem>删除</MListItem>
        </MList>
    </ChildContent>
</MMenu>
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Boolean | 是否打开 |
| CloseOnClick | Boolean | 点击内容关闭 |
| CloseOnContentClick | Boolean | 点击菜单内容关闭 |
| OffsetX | Boolean | X轴偏移 |
| OffsetY | Boolean | Y轴偏移 |
| Top | Boolean | 在上方打开 |
| Bottom | Boolean | 在下方打开 |
| Left | Boolean | 在左侧打开 |
| Right | Boolean | 在右侧打开 |
| Absolute | Boolean | 绝对定位 |
| MaxHeight | Int/String | 最大高度 |
| MaxWidth | Int/String | 最大宽度 |
| MinWidth | Int/String | 最小宽度 |
| NudgeBottom | Int | 底部微调 |
| NudgeTop | Int | 顶部微调 |
| NudgeLeft | Int | 左侧微调 |
| NudgeRight | Int | 右侧微调 |
| Transition | String | 过渡动画 |
| Dark | Boolean | 暗色主题 |
| Disabled | Boolean | 禁用 |
| Rounded | Boolean/String | 圆角 |
| Tile | Boolean | 直角 |
| AllowOverflow | Boolean | 允许溢出 |


## 事件
### MMenu
| 事件 | 说明 |
|------|------|
| ValueChanged | 显示状态改变时触发 |
| OnOutsideClick | 点击外部时触发 |

### MTooltip
| 事件 | 说明 |
|------|------|
| OnShow | 显示时触发 |
| OnHide | 隐藏时触发 |