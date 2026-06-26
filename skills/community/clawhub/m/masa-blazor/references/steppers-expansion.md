# MStepper 步骤条

文档: https://docs.masastack.com/blazor/ui-components/steppers

## 基础用法
```razor
<MStepper Value="_step">
    <MStepperHeader>
        <MStepperStep Complete="_step > 1" Step="1">第一步</MStepperStep>
        <MDivider />
        <MStepperStep Complete="_step > 2" Step="2">第二步</MStepperStep>
        <MDivider />
        <MStepperStep Step="3">第三步</MStepperStep>
    </MStepperHeader>
    
    <MStepperItems>
        <MStepperContent Step="1">
            <MCardText>第一步内容</MCardText>
            <MButton Color="primary" OnClick="() => _step = 2">下一步</MButton>
        </MStepperContent>
        
        <MStepperContent Step="2">
            <MCardText>第二步内容</MCardText>
            <MButton Text OnClick="() => _step = 1">上一步</MButton>
            <MButton Color="primary" OnClick="() => _step = 3">下一步</MButton>
        </MStepperContent>
        
        <MStepperContent Step="3">
            <MCardText>第三步内容</MCardText>
            <MButton Text OnClick="() => _step = 2">上一步</MButton>
            <MButton Color="primary" OnClick="Submit">提交</MButton>
        </MStepperContent>
    </MStepperItems>
</MStepper>

@code {
    int _step = 1;
}
```

## 垂直步骤条
```razor
<MStepper Value="_step" Vertical>
    <MStepperStep Step="1">步骤1</MStepperStep>
    <MStepperContent Step="1">
        <MCardText>步骤1内容</MCardText>
        <MButton Color="primary" OnClick="() => _step = 2">下一步</MButton>
    </MStepperContent>
    
    <MStepperStep Step="2">步骤2</MStepperStep>
    <MStepperContent Step="2">
        <MCardText>步骤2内容</MCardText>
    </MStepperContent>
</MStepper>
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Int/StringNumber | 当前步骤 |
| Vertical | Boolean | 垂直模式 |
| AltLabels | Boolean | 标签在下方 |
| NonLinear | Boolean | 非线性(可跳步) |
| Flat | Boolean | 无阴影 |
| Dark | Boolean | 暗色主题 |
| Elevation | Int | 阴影层级 |

---

# MExpansionPanel 折叠面板

文档: https://docs.masastack.com/blazor/ui-components/expansion-panels

## 基础用法
```razor
<MExpansionPanels>
    <MExpansionPanel>
        <MExpansionPanelHeader>面板1</MExpansionPanelHeader>
        <MExpansionPanelContent>面板1内容</MExpansionPanelContent>
    </MExpansionPanel>
    <MExpansionPanel>
        <MExpansionPanelHeader>面板2</MExpansionPanelHeader>
        <MExpansionPanelContent>面板2内容</MExpansionPanelContent>
    </MExpansionPanel>
</MExpansionPanels>
```

## 手风琴模式
```razor
<MExpansionPanels Accordion>
    <MExpansionPanel>
        <MExpansionPanelHeader>面板1</MExpansionPanelHeader>
        <MExpansionPanelContent>内容1</MExpansionPanelContent>
    </MExpansionPanel>
    <MExpansionPanel>
        <MExpansionPanelHeader>面板2</MExpansionPanelHeader>
        <MExpansionPanelContent>内容2</MExpansionPanelContent>
    </MExpansionPanel>
</MExpansionPanels>
```

## 带图标
```razor
<MExpansionPanel>
    <MExpansionPanelHeader>
        面板标题
        <template #actions>
            <MIcon>mdi-chevron-down</MIcon>
        </template>
    </MExpansionPanelHeader>
    <MExpansionPanelContent>内容</MExpansionPanelContent>
</MExpansionPanel>
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | Int/StringNumber | 当前展开面板 |
| Accordion | Boolean | 手风琴模式(只展开一个) |
| Flat | Boolean | 无阴影 |
| Popout | Boolean | 弹出样式 |
| Inset | Boolean | 内嵌样式 |
| Focusable | Boolean | 可聚焦 |
| Dark | Boolean | 暗色主题 |
| Readonly | Boolean | 只读 |
| Disabled | Boolean | 禁用 |


## 事件
### MStepper
| 事件 | 说明 |
|------|------|
| ValueChanged | 当前步骤改变时触发 |

### MExpansionPanels
| 事件 | 说明 |
|------|------|
| ValueChanged | 当前展开面板改变时触发 |