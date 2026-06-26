# 网格布局系统

文档: https://docs.masastack.com/blazor/ui-components/grids

## 概述
MASA Blazor 使用 12 列响应式网格系统，基于 Flexbox 实现。

## 断点
| 名称 | 宽度 | 后缀 |
|------|------|------|
| xs | < 600px | (无) |
| sm | 600px - 959px | sm |
| md | 960px - 1279px | md |
| lg | 1280px - 1919px | lg |
| xl | ≥ 1920px | xl |

## 基础用法
```razor
<MRow>
    <MCol>1</MCol>
    <MCol>2</MCol>
    <MCol>3</MCol>
</MRow>
```

## 指定列宽
```razor
<MRow>
    <MCol Cols="6">6列</MCol>
    <MCol Cols="6">6列</MCol>
</MRow>

<MRow>
    <MCol Cols="4">4列</MCol>
    <MCol Cols="4">4列</MCol>
    <MCol Cols="4">4列</MCol>
</MRow>

<MRow>
    <MCol Cols="3">3列</MCol>
    <MCol Cols="9">9列</MCol>
</MRow>
```

## 响应式列宽
```razor
<!-- 小屏幕12列，中等屏幕6列，大屏幕4列 -->
<MRow>
    <MCol Cols="12" Md="6" Lg="4">响应式</MCol>
    <MCol Cols="12" Md="6" Lg="4">响应式</MCol>
    <MCol Cols="12" Md="12" Lg="4">响应式</MCol>
</MRow>
```

## 列偏移
```razor
<MRow>
    <MCol Cols="4">4列</MCol>
    <MCol Cols="4" Offset="4">4列 偏移4</MCol>
</MRow>

<MRow>
    <MCol Cols="3" OffsetMd="3">偏移响应式</MCol>
    <MCol Cols="3" OffsetMd="3">偏移响应式</MCol>
</MRow>
```

## 自动宽度
```razor
<MRow>
    <MCol>自动</MCol>
    <MCol>自动</MCol>
    <MCol>自动</MCol>
</MRow>
```

## 对齐方式
```razor
<!-- 垂直对齐 -->
<MRow Align="AlignTypes.Center" Style="height: 200px;">
    <MCol>垂直居中</MCol>
</MRow>

<MRow Align="AlignTypes.End" Style="height: 200px;">
    <MCol>底部对齐</MCol>
</MRow>

<!-- 水平对齐 -->
<MRow Justify="JustifyTypes.Center">
    <MCol Cols="4">水平居中</MCol>
</MRow>

<MRow Justify="JustifyTypes.End">
    <MCol Cols="4">右对齐</MCol>
</MRow>

<MRow Justify="JustifyTypes.SpaceBetween">
    <MCol Cols="4">两端</MCol>
    <MCol Cols="4">两端</MCol>
</MRow>
```

## 间距
```razor
<!-- Row 间距 -->
<MRow Dense>
    <MCol Cols="4">紧凑</MCol>
    <MCol Cols="4">紧凑</MCol>
    <MCol Cols="4">紧凑</MCol>
</MRow>

<!-- Gutter 间距 -->
<MRow>
    <MCol>默认间距</MCol>
    <MCol>默认间距</MCol>
</MRow>
```

## 嵌套网格
```razor
<MRow>
    <MCol Cols="6">
        <MRow>
            <MCol Cols="6">嵌套1</MCol>
            <MCol Cols="6">嵌套2</MCol>
        </MRow>
    </MCol>
    <MCol Cols="6">另一列</MCol>
</MRow>
```

## MContainer
```razor
<MContainer Fluid>全宽容器</MContainer>
<MContainer>固定宽度居中容器</MContainer>
```

## 常用参数

### MRow
| 参数 | 类型 | 说明 |
|------|------|------|
| Dense | Boolean | 紧凑模式(减少间距) |
| NoGutters | Boolean | 无间距 |
| Align | AlignTypes | 垂直对齐(Start/Center/End) |
| Justify | JustifyTypes | 水平对齐 |
| AlignContent | AlignContentTypes | 多行对齐 |

### MCol
| 参数 | 类型 | 说明 |
|------|------|------|
| Cols | Int/String | 列宽(1-12/auto) |
| Sm | Int/String | sm断点列宽 |
| Md | Int/String | md断点列宽 |
| Lg | Int/String | lg断点列宽 |
| Xl | Int/String | xl断点列宽 |
| Offset | Int/String | 偏移量 |
| OffsetSm/Md/Lg/Xl | Int/String | 响应式偏移 |
| Order | Int/String | 排序 |
| AlignSelf | AlignTypes | 自身对齐 |


## 事件
MRow 和 MCol 是纯布局组件，无常用事件。用于构建响应式网格系统。