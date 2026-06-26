# MList 列表

文档: https://docs.masastack.com/blazor/ui-components/lists

## 基础用法
```razor
<MList>
    <MListItem>
        <MListItemContent>
            <MListItemTitle>列表项1</MListItemTitle>
        </MListItemContent>
    </MListItem>
    <MListItem>
        <MListItemContent>
            <MListItemTitle>列表项2</MListItemTitle>
        </MListItemContent>
    </MListItem>
</MList>
```

## 带图标
```razor
<MList>
    <MListItem>
        <MListItemIcon><MIcon>mdi-home</MIcon></MListItemIcon>
        <MListItemContent>
            <MListItemTitle>首页</MListItemTitle>
        </MListItemContent>
    </MListItem>
    <MListItem>
        <MListItemIcon><MIcon>mdi-account</MIcon></MListItemIcon>
        <MListItemContent>
            <MListItemTitle>个人中心</MListItemTitle>
            <MListItemSubtitle>查看个人信息</MListItemSubtitle>
        </MListItemContent>
    </MListItem>
</MList>
```

## 带头像
```razor
<MList>
    <MListItem>
        <MListItemAvatar>
            <MAvatar>
                <MImage Src="avatar.jpg" />
            </MAvatar>
        </MListItemAvatar>
        <MListItemContent>
            <MListItemTitle>用户名</MListItemTitle>
            <MListItemSubtitle>在线</MListItemSubtitle>
        </MListItemContent>
        <MListItemAction>
            <MIcon Color="green">mdi-circle</MIcon>
        </MListItemAction>
    </MListItem>
</MList>
```

## 分组列表
```razor
<MList>
    <MListGroup PrependIcon="mdi-account-circle" Value="true">
        <ActivatorContent>
            <MListItemContent>
                <MListItemTitle>用户管理</MListItemTitle>
            </MListItemContent>
        </ActivatorContent>
        <ChildContent>
            <MListItem Href="/users/list" Dense>
                <MListItemContent>
                    <MListItemTitle>用户列表</MListItemTitle>
                </MListItemContent>
            </MListItem>
            <MListItem Href="/users/roles" Dense>
                <MListItemContent>
                    <MListItemTitle>角色管理</MListItemTitle>
                </MListItemContent>
            </MListItem>
        </ChildContent>
    </MListGroup>
</MList>
```

## 可选列表
```razor
<MListItemGroup @bind-Value="_selected" Color="primary">
    <MListItem Value="1">
        <MListItemContent>选项1</MListItemContent>
    </MListItem>
    <MListItem Value="2">
        <MListItemContent>选项2</MListItemContent>
    </MListItem>
    <MListItem Value="3">
        <MListItemContent>选项3</MListItemContent>
    </MListItem>
</MListItemGroup>
```

## 常用参数

### MList
| 参数 | 类型 | 说明 |
|------|------|------|
| Dense | Boolean | 紧凑模式 |
| Dark | Boolean | 暗色主题 |
| Shaped | Boolean | 形状样式 |
| Rounded | Boolean/String | 圆角 |
| Flat | Boolean | 无阴影 |
| Nav | Boolean | 导航模式 |
| TwoLine | Boolean | 双行模式 |
| ThreeLine | Boolean | 三行模式 |
| Subheader | Boolean | 子标题样式 |
| Color | String | 激活颜色 |
| BackgroundColor | String | 背景色 |

### MListItem
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Object | 项目值 |
| Href | String | 链接地址 |
| Target | String | 链接目标 |
| Active | Boolean | 激活状态 |
| Inactive | Boolean | 不激活 |
| Disabled | Boolean | 禁用 |
| Dense | Boolean | 紧凑 |
| Link | Boolean | 链接样式 |
| Ripple | Boolean | 水波纹 |
| Selectable | Boolean | 可选中 |
| TwoLine | Boolean | 双行 |
| ThreeLine | Boolean | 三行 |


## 事件
### MListItem
| 事件 | 说明 |
|------|------|
| OnClick | 点击时触发 |
| OnContext | 右键点击时触发 |

### MListItemGroup
| 事件 | 说明 |
|------|------|
| ValueChanged | 选中项改变时触发 |