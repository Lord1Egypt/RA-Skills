# MDataTable 数据表格

文档: https://docs.masastack.com/blazor/ui-components/tables/data-tables

## 基础用法
```razor
<MDataTable Headers="@_headers" Items="@_items" />
```

## 带搜索/分页/排序
```razor
<MDataTable Headers="@_headers"
            Items="@_items"
            Search="@_search"
            ItemsPerPage="10"
            SortBy="@(new List<string> { "name" })"
            SortDesc="@(new List<bool> { false })">
    <TopContent>
        <MTextField @bind-Value="_search" Label="搜索" Clearable HideDetails="auto" />
    </TopContent>
</MDataTable>
```

## 自定义列
```razor
<MDataTable Headers="@_headers" Items="@_items">
    <ItemColContent>
        @if (context.Header.Value == "actions")
        {
            <MButton Icon Small><MIcon>mdi-pencil</MIcon></MButton>
            <MButton Icon Small Color="error"><MIcon>mdi-delete</MIcon></MButton>
        }
        else
        {
            @context.Value
        }
    </ItemColContent>
</MDataTable>
```

## 选择/多选
```razor
<MDataTable Headers="@_headers"
            Items="@_items"
            ShowSelect
            ItemKey="@(item => item.Id)"
            @bind-Selected="_selected">
</MDataTable>
```

## 服务端分页
```razor
<MDataTable Headers="@_headers"
            Items="@_items"
            ServerItemsLength="@_total"
            Options="@_options"
            Loading="@_loading"
            OnOptionsUpdate="OnOptionsChanged">
</MDataTable>
```

## Headers 定义
```razor
@code {
    List<DataTableHeader<YourModel>> _headers = new()
    {
        new() { Text = "姓名", Value = "name", Sortable = true },
        new() { Text = "年龄", Value = "age", Sortable = true, Align = DataTableHeaderAlign.Center },
        new() { Text = "邮箱", Value = "email", Sortable = false },
        new() { Text = "操作", Value = "actions", Sortable = false, Width = 120 }
    };
}
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Headers | List<DataTableHeader> | 列定义 |
| Items | IEnumerable<T> | 数据源 |
| ItemsPerPage | Int | 每页条数 |
| Page | Int | 当前页 |
| Search | String | 搜索关键字 |
| SortBy | List<String> | 排序字段 |
| SortDesc | List<Boolean> | 排序方向(true降序) |
| ShowSelect | Boolean | 显示选择框 |
| ItemKey | Func<T, object> | 行唯一键 |
| Selected | List<T> | 选中行(双向绑定) |
| Dense | Boolean | 紧凑模式 |
| Dark | Boolean | 暗色主题 |
| Loading | Boolean | 加载状态 |
| FixedHeader | Boolean | 固定表头 |
| Height | Int/String | 表格高度(固定表头时需要) |
| HideDefaultHeader | Boolean | 隐藏默认表头 |
| HideDefaultFooter | Boolean | 隐藏默认分页 |
| ServerItemsLength | Int | 服务端总数 |
| MultiSort | Boolean | 多列排序 |
| MustSort | Boolean | 必须排序 |
| DisableSort | Boolean | 禁用排序 |
| DisableFiltering | Boolean | 禁用过滤 |
| DisablePagination | Boolean | 禁用分页 |
| NoDataText | String | 无数据提示 |
| LoadingText | String | 加载提示 |
| FooterProps | Object | 分页属性 |



## 事件
| 事件 | 说明 |
|------|------|
| OnOptionsUpdate | 分页/排序/筛选选项改变时触发 |
| OnItemClick | 行点击时触发 |
| OnItemSelect | 行选中时触发 |
| OnPageChange | 页码改变时触发 |