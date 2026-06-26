# MTextField 文本输入框

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/text-fields

## 基础用法
```razor
<MTextField @bind-Value="_name" Label="姓名" />
<MTextField @bind-Value="_email" Label="邮箱" Type="email" />
<MTextField @bind-Value="_password" Label="密码" Type="password" />
```

## 输入框样式
```razor
<!-- 标准样式(默认) -->
<MTextField Label="标准" Outlined />

<!-- 填充样式 -->
<MTextField Label="填充" Filled />

<!-- 单行下划线 -->
<MTextField Label="下划线" Solo />

<!-- 隐藏详情 -->
<MTextField Label="隐藏详情" HideDetails="auto" />
```

## 前缀/后缀/图标
```razor
<!-- 前缀 -->
<MTextField Prefix="$" Label="金额" />

<!-- 后缀 -->
<MTextField Suffix="@gmail.com" Label="邮箱" />

<!-- 前置图标 -->
<MTextField PrependIcon="mdi-account" Label="用户名" />

<!-- 后置图标 -->
<MTextField AppendIcon="mdi-lock" Label="密码" />

<!-- 前后图标 -->
<MTextField PrependIcon="mdi-map-marker" AppendIcon="mdi-crosshairs-gps" Label="位置" />
```

## 清除/计数/提示
```razor
<!-- 可清除 -->
<MTextField Clearable Label="可清除" />

<!-- 字符计数 -->
<MTextField Counter="20" Label="最多20字" />

<!-- CounterValue自定义计数 -->
<MTextField CounterValue="@(v => v?.Length ?? 0)" Label="自定义计数" />

<!-- 提示文本 -->
<MTextField Hint="请输入您的邮箱" PersistentHint Label="邮箱" />
```

## 禁用/只读
```razor
<MTextField Disabled Label="禁用" />
<MTextField Readonly Label="只读" Value="不可编辑的内容" />
```

## 验证规则
```razor
<MTextField Label="必填" Rules="@_rules" />
@code {
    List<Func<string, bool>> _rules = new()
    {
        v => !string.IsNullOrEmpty(v) || "此项为必填"
    };
}
```

## 数字输入
```razor
<MTextField @bind-Value="_number" Label="数字" Type="number" />
<MTextField @bind-Value="_age" Label="年龄" Type="number" Min="0" Max="150" />
```

## 多行文本
```razor
<!-- 使用 MTextarea 组件 -->
<MTextarea Label="简介" Rows="3" AutoGrow />
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Value | String | 绑定值 |
| Label | String | 标签 |
| Placeholder | String | 占位文本 |
| Type | String | 输入类型(text/password/email/number等) |
| Outlined | Boolean | 描边样式 |
| Filled | Boolean | 填充样式 |
| Solo | Boolean | 单行样式 |
| Dense | Boolean | 紧凑模式 |
| Disabled | Boolean | 禁用 |
| Readonly | Boolean | 只读 |
| Clearable | Boolean | 可清除 |
| Counter | Int/String | 字符计数限制 |
| CounterValue | Func | 自定义计数函数 |
| Hint | String | 提示文本 |
| PersistentHint | Boolean | 常驻显示提示 |
| PrependIcon | String | 前置图标 |
| AppendIcon | String | 后置图标 |
| Prefix | String | 前缀文本 |
| Suffix | String | 后缀文本 |
| HideDetails | String | 隐藏详情(auto/true/false) |
| Rules | List<Func> | 验证规则 |
| Required | Boolean | 必填 |
| Autofocus | Boolean | 自动聚焦 |
| Max | Number | 数字最大值 |
| Min | Number | 数字最小值 |
| Step | Number | 数字步长 |
| Color | String | 主题色 |
| BackgroundColor | String | 背景色 |



## 事件
| 事件 | 说明 |
|------|------|
| ValueChanged | 值改变时触发 |
| OnChange | 值确认改变时触发 |
| OnInput | 输入时触发 |
| OnBlur | 失去焦点时触发 |
| OnFocus | 获得焦点时触发 |
| OnKeyDown | 按键按下时触发 |
| OnKeyUp | 按键抬起时触发 |
| OnClickAppend | 后置图标点击时触发 |
| OnClickPrepend | 前置图标点击时触发 |