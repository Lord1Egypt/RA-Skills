# MDatePicker 日期选择器

文档: https://docs.masastack.com/blazor/ui-components/pickers/date-pickers

## 基础用法
```razor
<MDatePicker @bind-Value="_date" />
<MDatePicker @bind-Value="_date" NoTitle />
```

## 与输入框配合
```razor
<MMenu @bind-Value="_menu" CloseOnContentClick="false">
    <ActivatorContent>
        <MTextField @bind-Value="_date"
                    Label="选择日期"
                    Readonly
                    @attributes="context.Attrs"
                    AppendIcon="mdi-calendar" />
    </ActivatorContent>
    <ChildContent>
        <MDatePicker @bind-Value="_date" OnClickDate="() => _menu = false" />
    </ChildContent>
</MMenu>
```

## 范围选择
```razor
<MDatePicker @bind-Value="_dates" Range />
```

## 多选日期
```razor
<MDatePicker @bind-Value="_multiple" Multiple />
```

## 月份选择
```razor
<MDatePicker @bind-Value="_date" Type="DatePickerType.Month" />
```

## 限制日期范围
```razor
<MDatePicker @bind-Value="_date" Min="2024-01-01" Max="2024-12-31" />
```

## 禁用特定日期
```razor
<MDatePicker @bind-Value="_date" AllowedDates="AllowedDates" />

@code {
    DateTime? _date;
    Func<DateTime, bool> AllowedDates = date => date.Day != 15;
}
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | DateTime/String | 选中值 |
| Type | DatePickerType | 类型(Date/Month) |
| Multiple | Boolean | 多选 |
| Range | Boolean | 范围选择 |
| NoTitle | Boolean | 隐藏标题 |
| ShowCurrent | Boolean | 显示当前日期 |
| ShowWeek | Boolean | 显示周数 |
| FirstDayOfWeek | Int | 首日(0-6) |
| Min | String/DateTime | 最小日期 |
| Max | String/DateTime | 最大日期 |
| AllowedDates | Func | 允许的日期 |
| Disabled | Boolean | 禁用 |
| Readonly | Boolean | 只读 |
| Locale | String | 本地化 |
| WeekdayFormat | String | 星期格式 |
| TitleDateFormat | String | 标题日期格式 |
| HeaderDateFormat | String | 头部日期格式 |
| DayFormat | Func | 日期格式化 |
| MonthFormat | Func | 月份格式化 |
| WeekdayFormat | Func | 星期格式化 |
| Color | String | 颜色 |
| Dark | Boolean | 暗色主题 |
| Elevation | Int | 阴影 |
| Flat | Boolean | 无阴影 |
| FullWidth | Boolean | 全宽 |
| Width | Int/String | 宽度 |
| Scrollable | Boolean | 可滚动 |
| Events | Func | 事件日期标记 |
| EventColor | Func/String | 事件颜色 |

## MDateTimePicker 日期时间选择器

文档: https://docs.masastack.com/blazor/ui-components/pickers/date-time-pickers

```razor
<MDateTimePicker @bind-Value="_datetime" DateTitle="选择日期" TimeTitle="选择时间" />
```



## 事件
### MDatePicker
| 事件 | 说明 |
|------|------|
| ValueChanged | 日期改变时触发 |
| OnInput | 输入日期时触发 |
| OnChange | 日期确认时触发 |
| OnClickDate | 点击日期时触发 |