# 移动端组件

文档: https://docs.masastack.com/blazor/mobiles/

## MPullRefresh 下拉刷新

文档: https://docs.masastack.com/blazor/mobiles/pull-refresh

### 基础用法
```razor
<div class="overflow-auto" style="height: 300px;">
    <MPullRefresh OnRefresh="OnRefresh">
        <div class="text-center rounded pt-6"
             style="height: 500px; border: 1px dashed grey;">
            Pull down to refresh @_counter
        </div>
    </MPullRefresh>
</div>

@code {
    private int _counter;

    private async Task OnRefresh()
    {
        await Task.Delay(1000);
        _counter++;
    }
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Refreshing | Boolean | 是否正在刷新 |
| Disabled | Boolean | 禁用下拉刷新 |
| PullDistance | Int | 触发刷新的距离 |
| HeadHeight | Int | 头部高度 |
| SuccessText | String | 刷新成功文本 |
| SuccessDuration | Int | 成功提示显示时长(ms) |
| AnimationDuration | Int | 动画时长(ms) |
| LoosingText | String | 释放刷新文本 |
| PullingText | String | 下拉刷新文本 |
| LoadingText | String | 加载中文本 |

### 事件
| 事件 | 说明 |
|------|------|
| OnRefresh | 触发刷新时调用 |
| OnError | 刷新出错时调用 |

---

## MSwiper 轮播滑动

文档: https://docs.masastack.com/blazor/mobiles/swiper

### 基础用法
```razor
<MSwiper Height="300">
    <MSwiperSlide Class="d-flex align-center justify-center surface-container-highest">
        <h3> Slide 1 </h3>
    </MSwiperSlide>
    <MSwiperSlide Class="d-flex align-center justify-center surface-container-highest">
        <h3> Slide 2 </h3>
    </MSwiperSlide>
    <MSwiperSlide Class="d-flex align-center justify-center surface-container-highest">
        <h3> Slide 3 </h3>
    </MSwiperSlide>
</MSwiper>
```

### 带分页指示器
```razor
<MSwiper Height="300">
    <MSwiperPagination />
    <MSwiperSlide Class="d-flex align-center justify-center surface-container-highest">
        <h3> Slide 1 </h3>
    </MSwiperSlide>
    <MSwiperSlide Class="d-flex align-center justify-center surface-container-highest">
        <h3> Slide 2 </h3>
    </MSwiperSlide>
    <MSwiperSlide Class="d-flex align-center justify-center surface-container-highest">
        <h3> Slide 3 </h3>
    </MSwiperSlide>
</MSwiper>
```

### 自动播放
```razor
<MSwiper Height="300" Autoplay>
    <MSwiperSlide>Slide 1</MSwiperSlide>
    <MSwiperSlide>Slide 2</MSwiperSlide>
    <MSwiperSlide>Slide 3</MSwiperSlide>
</MSwiper>
```

### 循环模式
```razor
<MSwiper Height="300" Loop>
    <MSwiperSlide>Slide 1</MSwiperSlide>
    <MSwiperSlide>Slide 2</MSwiperSlide>
    <MSwiperSlide>Slide 3</MSwiperSlide>
</MSwiper>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Height | Int/String | 高度 |
| Direction | String | 方向(horizontal/vertical) |
| Autoplay | Boolean | 自动播放 |
| Loop | Boolean | 循环模式 |
| AutoHeight | Boolean | 自适应高度 |
| Navigation | Boolean | 显示导航按钮 |
| Pagination | Boolean | 显示分页指示器 |
| SpaceBetween | Int | 间距(px) |
| SlidesPerView | Int/String | 每屏显示数量 |
| InitialSlide | Int | 初始幻灯片索引 |
| Speed | Int | 切换速度(ms) |
| Effect | String | 切换效果(slide/fade/cube/coverflow/flip) |

---

## MPageStack 页面栈

文档: https://docs.masastack.com/blazor/mobiles/page-stack

```razor
<MPageStack @ref="_pageStack">
    <MPage Name="home">
        <Home OnNavigateToDetail="() => _pageStack.Push(\"detail\")" />
    </MPage>
    <MPage Name="detail">
        <Detail />
    </MPage>
</MPageStack>

@code {
    MPageStack _pageStack;
}
```

### 方法
| 方法 | 说明 |
|------|------|
| Push(string name) | 压入新页面 |
| Pop() | 返回上一页 |
| Replace(string name) | 替换当前页面 |
| PopToRoot() | 返回到根页面 |

---

## PMobileDatePicker 移动端日期选择

文档: https://docs.masastack.com/blazor/mobiles/mobile-date-pickers

### 基础用法
```razor
<div class="text-center">
    <PMobileDatePicker @bind-Value="_date">
        <ActivatorContent>
            <MButton Color="primary" Class="text-capitalize" Text @attributes="context.Attrs">
                @(_date == default ? "Please select" : _date)
            </MButton>
        </ActivatorContent>
    </PMobileDatePicker>
</div>

@code {
    private DateOnly _date;
}
```

### 限制日期范围
```razor
<PMobileDatePicker @bind-Value="_date"
                   Max="DateOnly.FromDateTime(DateTime.Now)"
                   Min="new DateOnly(2000, 1, 1)">
    <ActivatorContent>
        <MButton Color="primary" Class="text-capitalize" Text @attributes="context.Attrs">
            @(_date == default ? "Please select" : _date)
        </MButton>
    </ActivatorContent>
</PMobileDatePicker>
```

### 精度控制
```razor
<PMobileDatePicker @bind-Value="_date" Precision="DatePickerPrecision.Date" />
<PMobileDatePicker @bind-Value="_date" Precision="DatePickerPrecision.Month" />
<PMobileDatePicker @bind-Value="_date" Precision="DatePickerPrecision.Year" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | DateOnly | 选中值 |
| Title | String | 标题 |
| Min | DateOnly | 最小日期 |
| Max | DateOnly | 最大日期 |
| Precision | DatePickerPrecision | 精度(Year/Month/Date) |
| Formatter | Func | 自定义格式化 |
| Readonly | Boolean | 只读 |

---

## PMobileTimePicker 移动端时间选择

文档: https://docs.masastack.com/blazor/mobiles/mobile-time-pickers

### 基础用法
```razor
<div class="text-center">
    <PMobileTimePicker @bind-Value="_time">
        <ActivatorContent>
            <MButton Color="primary" Class="text-capitalize" Text @attributes="context.Attrs">
                @_time.ToString("HH:mm:ss")
            </MButton>
        </ActivatorContent>
    </PMobileTimePicker>
</div>

@code {
    private TimeOnly _time = new TimeOnly(10, 30, 0);
}
```

### 限制时间范围
```razor
<PMobileTimePicker @bind-Value="_time"
                   Min="new TimeOnly(9, 30, 0)"
                   Max="new TimeOnly(14, 59, 59)">
    <ActivatorContent>
        <MButton Color="primary" Class="text-capitalize" Text @attributes="context.Attrs">
            @_time.ToString("HH:mm:ss")
        </MButton>
    </ActivatorContent>
</PMobileTimePicker>
```

### 精度控制
```razor
<PMobileTimePicker @bind-Value="_time" Precision="TimePickerPrecision.Hour" />
<PMobileTimePicker @bind-Value="_time" Precision="TimePickerPrecision.Minute" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | TimeOnly | 选中值 |
| Title | String | 标题 |
| Min | TimeOnly | 最小时间 |
| Max | TimeOnly | 最大时间 |
| Precision | TimePickerPrecision | 精度(Hour/Minute) |
| Formatter | Func | 自定义格式化 |
| Readonly | Boolean | 只读 |

---

## PMobileDateTimePicker 移动端日期时间选择

文档: https://docs.masastack.com/blazor/mobiles/mobile-date-time-pickers

```razor
<PMobileDateTimePicker @bind-Value="_datetime" />
<PMobileDateTimePicker @bind-Value="_datetime" Title="选择日期时间" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | DateTime | 选中值 |
| Title | String | 标题 |
| Min | DateTime | 最小日期时间 |
| Max | DateTime | 最大日期时间 |
| Precision | DateTimePickerPrecision | 精度 |
| Formatter | Func | 自定义格式化 |

---

## PMobilePicker 移动端选择器

文档: https://docs.masastack.com/blazor/mobiles/mobile-pickers

### 基础用法
```razor
<div class="text-center">
    <PMobilePicker @bind-Value="_value"
                   Columns="@Columns"
                   TColumn="Data"
                   TColumnItem="string"
                   ItemValue="item => item.Code"
                   ItemText="item => item.Name"
                   ItemChildren="item => item.Children"
                   ItemDisabled="item => item.Disabled">
        <ActivatorContent>
            <MButton Color="primary" Class="text-capitalize" Text @attributes="context.Attrs">
                @(_value.Count == 0 ? "Please select" : string.Join(" ", GetNames()))
            </MButton>
        </ActivatorContent>
    </PMobilePicker>
</div>
```

### 级联选择
```razor
<PMobilePicker @bind-Value="_value"
               Columns="@Columns"
               TColumn="Data"
               TColumnItem="string"
               ItemValue="item => item.Code"
               ItemText="item => item.Name"
               ItemChildren="item => item.Children"
               ItemDisabled="item => item.Disabled">
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | List<string> | 选中值列表 |
| Columns | IEnumerable | 选项数据源 |
| TColumn | Type | 列类型 |
| TColumnItem | Type | 列项类型 |
| ItemValue | Func | 值映射 |
| ItemText | Func | 文本映射 |
| ItemChildren | Func | 子节点映射 |
| ItemDisabled | Func | 禁用状态映射 |
| Title | String | 标题 |
| ItemHeight | Int | 选项高度 |
| VisibleItemCount | Int | 可见选项数量 |

---

## PMobileCascader 移动端级联选择

文档: https://docs.masastack.com/blazor/mobiles/mobile-cascader

### 基础用法
```razor
<PMobileCascader TItem="Data"
                 TItemValue="string"
                 Title="选择地区"
                 Items="@Datas"
                 ItemText="d => d.Name"
                 ItemValue="d => d.Code"
                 ItemChildren="d => d.Children"
                 ItemDisabled="d => d.Disabled"
                 OnConfirm="HandleOnConfirm">
    <ActivatorContent>
        <MButton @attributes="context.Attrs">Select</MButton>
    </ActivatorContent>
</PMobileCascader>

@code {
    List<Data> selectedItems = new();

    void HandleOnConfirm(List<Data> selected)
    {
        selectedItems = selected;
    }

    record Data(string Code, string Name, List<Data> Children = null, bool Disabled = false);
}
```

### 异步加载子节点
```razor
<PMobileCascader TItem="Data"
                 TItemValue="string"
                 Items="@Datas"
                 ItemText="d => d.Name"
                 ItemValue="d => d.Code"
                 ItemChildren="d => d.Children"
                 LoadChildren="LoadChildrenAsync">
    <ActivatorContent>
        <MButton @attributes="context.Attrs">Select</MButton>
    </ActivatorContent>
</PMobileCascader>

@code {
    async Task<List<Data>> LoadChildrenAsync(Data parent)
    {
        // 异步加载子节点
        return await GetDataAsync(parent.Code);
    }
}
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| TItem | Type | 数据项类型 |
| TItemValue | Type | 值类型 |
| Title | String | 标题 |
| Items | IEnumerable | 数据源 |
| ItemText | Func | 文本映射 |
| ItemValue | Func | 值映射 |
| ItemChildren | Func | 子节点映射 |
| ItemDisabled | Func | 禁用状态映射 |
| LoadChildren | Func | 异步加载子节点 |

### 事件
| 事件 | 说明 |
|------|------|
| OnConfirm | 确认选择时触发 |

---

## PMobilePickerView 移动端选择视图

文档: https://docs.masastack.com/blazor/mobiles/mobile-picker-views

```razor
<PMobilePickerView @bind-Value="_value"
                   Columns="@Columns"
                   TColumn="Data"
                   TColumnItem="string"
                   ItemValue="item => item.Code"
                   ItemText="item => item.Name"
                   ItemChildren="item => item.Children" />
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | List<string> | 选中值 |
| Columns | IEnumerable | 数据源 |
| ItemHeight | Int | 选项高度 |
| ItemDisabled | Func | 禁用映射 |

---

## MPdfMobileViewer PDF 阅读器

文档: https://docs.masastack.com/blazor/mobiles/pdf-mobile-viewer

```razor
<MPdfMobileViewer Source="document.pdf" />
<MPdfMobileViewer Source="https://example.com/document.pdf" />
```

---

## MSwipeActions 滑动操作

文档: https://docs.masastack.com/blazor/mobiles/swipe-actions

### 基础用法
```razor
<MSwipeActions>
    <LeftContent>
        <MButton Color="primary">Left</MButton>
    </LeftContent>
    <ChildContent>
        <MListItem Style="background-color: white; height: 54px;">
            <MListItemContent>Swipe Me</MListItemContent>
        </MListItem>
    </ChildContent>
</MSwipeActions>
```

### 左右滑动
```razor
<MSwipeActions CloseOnClick>
    <LeftContent>
        <MButton Color="error" Tile Style="height: 100%;">删除</MButton>
    </LeftContent>
    <RightContent>
        <MButton Color="primary" Tile Style="height: 100%;">编辑</MButton>
    </RightContent>
    <ChildContent>
        <MListItem Style="background-color: white; height: 54px;">
            <MListItemContent>向左或向右滑动</MListItemContent>
        </MListItem>
    </ChildContent>
</MSwipeActions>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| CloseOnClick | Boolean | 点击内容后关闭滑动 |
| Disabled | Boolean | 禁用滑动 |

---

## MCell 单元格 (Labs)

文档: https://docs.masastack.com/blazor/mobiles/cell

### 基础用法
```razor
<MCellGroup>
    <MCell Title="单元格标题" Value="内容" />
    <MCell Title="单元格标题" Value="内容" IsLink />
</MCellGroup>
```

### 描边样式
```razor
<MCellGroup Outlined>
    <MCell Title="单元格标题" Value="内容" />
    <MCell Title="单元格标题" Value="内容" IsLink />
</MCellGroup>
```

### 微信风格
```razor
<MCellGroup>
    <MCell Title="我的订单" Icon="mdi-order-numeric-descending" IsLink />
    <MCell Title="收货地址" Icon="mdi-map-marker" IsLink />
    <MCell Title="帮助中心" Icon="mdi-help-circle" IsLink />
</MCellGroup>
```

### 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Title | String | 标题 |
| Value | String | 内容 |
| Label | String | 描述 |
| Icon | String | 图标 |
| IsLink | Boolean | 显示箭头(链接样式) |
| OnClick | EventCallback | 点击事件 |
| Outlined | Boolean | 描边样式(MCellGroup) |
| Inset | Boolean | 内嵌样式(MCellGroup) |
