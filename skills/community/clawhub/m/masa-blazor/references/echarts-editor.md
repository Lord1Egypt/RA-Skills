# 图表与编辑器

## MEcharts 图表

文档: https://docs.masastack.com/blazor/ui-components/echarts

### 基础用法
```razor
<MEcharts Option="@_option" Style="height: 400px;" />

@code {
    object _option = new
    {
        Title = new { Text = "销售数据" },
        XAxis = new { Type = "category", Data = new[] { "周一", "周二", "周三", "周四", "周五" } },
        YAxis = new { Type = "value" },
        Series = new[] { new { Type = "bar", Data = new[] { 120, 200, 150, 80, 70 } } }
    };
}
```

### 折线图
```razor
<MEcharts Option="@_lineOption" />

@code {
    object _lineOption = new
    {
        Title = new { Text = "趋势图" },
        XAxis = new { Type = "category", Data = new[] { "1月", "2月", "3月", "4月" } },
        YAxis = new { Type = "value" },
        Series = new[]
        {
            new { Type = "line", Name = "销量", Data = new[] { 820, 932, 901, 934 } },
            new { Type = "line", Name = "收入", Data = new[] { 620, 732, 801, 634 } }
        }
    };
}
```

### 饼图
```razor
<MEcharts Option="@_pieOption" />

@code {
    object _pieOption = new
    {
        Title = new { Text = "饼图" },
        Series = new[]
        {
            new
            {
                Type = "pie",
                Radius = "50%",
                Data = new[]
                {
                    new { Value = 335, Name = "直接访问" },
                    new { Value = 310, Name = "邮件营销" },
                    new { Value = 234, Name = "联盟广告" }
                }
            }
        }
    };
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Option | Object | ECharts 配置项 |
| Width | String | 宽度 |
| Height | String | 高度 |
| Theme | String | 主题(dark/light) |
| InitOptions | Object | 初始化选项 |
| AutoResize | Boolean | 自动调整大小 |
| Loading | Boolean | 加载状态 |
| LoadingOptions | Object | 加载配置 |
| Group | String | 图表分组联动 |

---

## MEditor 富文本编辑器

文档: https://docs.masastack.com/blazor/ui-components/editors

### 基础用法
```razor
<MEditor @bind-Value="_content" />

@code {
    string _content = "<p>初始内容</p>";
}
```

### 工具栏配置
```razor
<MEditor @bind-Value="_content" Toolbar="@_toolbar" />

@code {
    string[] _toolbar = new[]
    {
        "bold", "italic", "underline", "strike",
        "header", "list", "align",
        "link", "image", "code-block"
    };
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | String | 编辑器内容(HTML) |
| Placeholder | String | 占位文本 |
| ReadOnly | Boolean | 只读 |
| Theme | String | 主题(snow/bubble) |
| Toolbar | String[] | 工具栏配置 |
| Height | Int/String | 高度 |
| MinHeight | Int/String | 最小高度 |
| MaxHeight | Int/String | 最大高度 |

---

## MMonacoEditor 代码编辑器

文档: https://docs.masastack.com/blazor/ui-components/monaco-editor

```razor
<MMonacoEditor @bind-Value="_code" Language="csharp" Style="height: 400px;" />

@code {
    string _code = "using System;\n\nnamespace App\n{\n    class Program\n    {\n        static void Main() { }\n    }\n}";
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | String | 编辑器内容 |
| Language | String | 语言(csharp/javascript/html/css等) |
| Theme | String | 主题(vs/vs-dark/hc-black) |
| ReadOnly | Boolean | 只读 |
| Minimap | Boolean | 显示小地图 |
| AutomaticLayout | Boolean | 自动调整布局 |
| TabSize | Int | Tab大小 |
| WordWrap | String | 自动换行 |
| FontSize | Int | 字体大小 |
| LineNumbers | String | 行号显示 |

---

## MMarkdownParser Markdown 渲染

文档: https://docs.masastack.com/blazor/ui-components/markdown-parsers

```razor
<MMarkdownParser Source="@_markdown" />
<MMarkdownParser Source="# 标题\n\n**粗体** *斜体*" />
```

---

## MSyntaxHighlight 代码高亮

文档: https://docs.masastack.com/blazor/ui-components/syntax-highlights

```razor
<MSyntaxHighlight Code="@_code" Language="csharp" />
<MSyntaxHighlight Code="@_html" Language="html" Dark />
<MSyntaxHighlight Code="@_python" Language="python" />
```

### 支持的语言
csharp, javascript, typescript, html, css, python, java, sql, json, xml, markdown, bash 等


## 事件
### MEcharts
| 事件 | 说明 |
|------|------|
| OnClick | 图表点击时触发 |
| OnDataZoom | 数据缩放时触发 |
| OnLegendSelectChange | 图例选择改变时触发 |

### MEditor
| 事件 | 说明 |
|------|------|
| ValueChanged | 内容改变时触发 |
| OnTextChange | 文本改变时触发 |

### MMonacoEditor
| 事件 | 说明 |
|------|------|
| ValueChanged | 内容改变时触发 |
| OnDidChangeModelContent | 模型内容改变时触发 |