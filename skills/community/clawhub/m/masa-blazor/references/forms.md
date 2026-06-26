# MForm 表单

文档: https://docs.masastack.com/blazor/ui-components/form-inputs-and-controls/forms

## 基础用法
```razor
<MForm @ref="_form" Model="@_model" OnValidSubmit="Submit">
    <MTextField @bind-Value="_model.Name" Label="姓名" Rules="@_nameRules" />
    <MTextField @bind-Value="_model.Email" Label="邮箱" Rules="@_emailRules" />
    <MButton Type="submit" Color="primary">提交</MButton>
</MForm>

@code {
    MForm _form;
    UserModel _model = new();
    
    List<Func<string, bool>> _nameRules = new()
    {
        v => !string.IsNullOrEmpty(v) || "姓名为必填项"
    };
    
    List<Func<string, bool>> _emailRules = new()
    {
        v => !string.IsNullOrEmpty(v) || "邮箱为必填项",
        v => v.Contains("@") || "邮箱格式不正确"
    };
    
    void Submit()
    {
        // 提交逻辑
    }
}
```

## 手动验证
```razor
<MForm @ref="_form" Model="@_model">
    <MTextField @bind-Value="_model.Name" Label="姓名" />
    <MButton OnClick="Validate">验证</MButton>
    <MButton OnClick="Reset">重置</MButton>
</MForm>

@code {
    async Task Validate()
    {
        var valid = await _form.ValidateAsync();
        if (valid)
        {
            // 验证通过
        }
    }
    
    void Reset()
    {
        _form.Reset();
    }
}
```

## EnableValidation 模式
```razor
<MForm EnableValidation>
    <MTextField @bind-Value="_model.Name" Label="姓名" Required />
    <MTextField @bind-Value="_model.Age" Label="年龄" Type="number" Min="0" Max="150" />
</MForm>
```

## 常用参数
| 参数 | 类型 | 说明 |
|------|------|------|
| Model | Object | 表单模型 |
| EnableValidation | Boolean | 启用验证 |
| Value | Boolean | 表单是否有效 |
| OnValidSubmit | EventCallback | 验证通过后提交 |
| OnInvalidSubmit | EventCallback | 验证失败时触发 |

## 常用方法
| 方法 | 返回类型 | 说明 |
|------|----------|------|
| ValidateAsync() | Task<bool> | 异步验证 |
| Reset() | void | 重置表单 |
| ResetValidation() | void | 重置验证状态 |


## 事件
| 事件 | 说明 |
|------|------|
| OnValidSubmit | 验证通过后提交时触发 |
| OnInvalidSubmit | 验证失败时触发 |