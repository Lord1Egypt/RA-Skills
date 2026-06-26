# MNavigationDrawer 侧边导航抽屉

文档: https://docs.masastack.com/blazor/ui-components/navigation-drawers

## 基础用法
```razor
<MApp>
    <MNavigationDrawer App @bind-Value="_drawer">
        <MList>
            <MListItem Href="/">
                <MListItemIcon><MIcon>mdi-home</MIcon></MListItemIcon>
                <MListItemContent>
                    <MListItemTitle>首页</MListItemTitle>
                </MListItemContent>
            </MListItem>
            <MListItem Href="/settings">
                <MListItemIcon><MIcon>mdi-cog</MIcon></MListItemIcon>
                <MListItemContent>
                    <MListItemTitle>设置</MListItemTitle>
                </MListItemContent>
            </MListItem>
        </MList>
    </MNavigationDrawer>
    
    <MMain>
        <MButton OnClick="() => _drawer = !_drawer">切换抽屉</MButton>
    </MMain>
</MApp>
```

## 带迷你模式
```razor
<MNavigationDrawer App MiniVariant="@_mini" MiniVariantWidth="56">
    <MList Dense Nav>
        <MListItem Href="/">
            <MListItemIcon><MIcon>mdi-home</MIcon></MListItemIcon>
            <MListItemContent>
                <MListItemTitle>首页</MListItemTitle>
            </MListItemContent>
        </MListItem>
    </MList>
</MNavigationDrawer>
```

## 带分组菜单
```razor
<MNavigationDrawer App>
    <MList>
        <MListGroup PrependIcon="mdi-account-circle" Value="true">
            <ActivatorContent>
                <MListItemContent>
                    <MListItemTitle>用户管理</MListItemTitle>
                </MListItemContent>
            </ActivatorContent>
            <ChildContent>
                <MListItem Href="/users/list">
                    <MListItemContent>
                        <MListItemTitle>用户列表</MListItemTitle>
                    </MListItemContent>
                </MListItem>
                <MListItem Href="/users/roles">
                    <MListItemContent>
                        <MListItemTitle>角色管理</MListItemTitle>
                    </MListItemContent>
                </MListItem>
            </ChildContent>
        </MListGroup>
    </MList>
</MNavigationDrawer>
```

## 右侧抽屉
```razor
<MNavigationDrawer App Right Temporary @bind-Value="_rightDrawer">
    <MList>
        <MListItem>通知</MListItem>
    </MList>
</MNavigationDrawer>
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Boolean | 是否显示(双向绑定) |
| App | Boolean | 布局模式(与MMain配合) |
| MiniVariant | Boolean | 迷你模式 |
| MiniVariantWidth | Int | 迷你模式宽度 |
| Width | Int | 完整宽度 |
| Permanent | Boolean | 常驻显示 |
| Temporary | Boolean | 临时模式(覆盖内容) |
| Right | Boolean | 显示在右侧 |
| Clipped | Boolean | 在Toolbar下方 |
| Dark | Boolean | 暗色主题 |
| Color | String | 背景色 |
| Fixed | Boolean | 固定定位 |
| Floating | Boolean | 无边框 |
| ExpandOnHover | Boolean | 悬停展开(迷你模式) |
| HideOverlay | Boolean | 隐藏遮罩 |
| OverlayColor | String | 遮罩颜色 |
| State | Boolean | 控制状态 |


## 事件
| 事件 | 说明 |
|------|------|
| ValueChanged | 显示状态改变时触发 |
| OnExpandTransitionEnd | 展开动画结束时触发 |
| OnInput | 状态输入时触发 |