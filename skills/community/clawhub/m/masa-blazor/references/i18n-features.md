# 国际化与其他特性

## 国际化 (i18n)

文档: https://docs.masastack.com/blazor/features/internationalization

### 配置
```csharp
// Program.cs
builder.Services.AddMasaBlazor(options =>
{
    options.Locale = new CultureInfo("zh-CN");
});
```

### 切换语言
```razor
@inject MasaBlazor MasaBlazor

<MSelect @bind-Value="_culture" Items="@_cultures" ItemText="@(c => c.Name)" OnChange="ChangeCulture" />

@code {
    CultureInfo _culture = CultureInfo.CurrentCulture;
    List<CultureInfo> _cultures = new()
    {
        new CultureInfo("zh-CN"),
        new CultureInfo("en-US"),
        new CultureInfo("ja-JP")
    };
    
    void ChangeCulture(CultureInfo culture)
    {
        MasaBlazor.Locale = culture;
    }
}
```

---

## 断点 (Breakpoints)

文档: https://docs.masastack.com/blazor/features/breakpoints

### 断点值
| 名称 | 宽度 |
|------|------|
| xs | < 600px |
| sm | 600px - 959px |
| md | 960px - 1279px |
| lg | 1280px - 1919px |
| xl | ≥ 1920px |

### 使用断点
```razor
@inject MasaBlazor MasaBlazor

@if (MasaBlazor.Breakpoint.SmAndDown)
{
    <div>移动端布局</div>
}
else
{
    <div>桌面端布局</div>
}
```

### 断点属性
- `Xs` / `Sm` / `Md` / `Lg` / `Xl` - 单断点
- `SmAndDown` - sm 及以下
- `MdAndDown` - md 及以下
- `SmAndUp` - sm 及以上
- `MdAndUp` - md 及以上

---

## 图标字体 (Icon Fonts)

文档: https://docs.masastack.com/blazor/features/icon-fonts

### 默认图标库
MASA Blazor 默认使用 **Material Design Icons** (mdi)

### 使用
```razor
<MIcon>mdi-home</MIcon>
<MIcon>mdi-account</MIcon>
<MIcon>mdi-settings</MIcon>
```

### 自定义图标库
```csharp
// Program.cs
builder.Services.AddMasaBlazor(options =>
{
    options.ConfigureIcons(IconSet.MaterialDesignIcons);
});
```

---

## SSR (服务端渲染)

文档: https://docs.masastack.com/blazor/features/ssr

### .NET 8 SSR 支持
```csharp
// Program.cs
builder.Services.AddMasaBlazor();
```

---

## 双向文本 (Bidirectionality)

文档: https://docs.masastack.com/blazor/features/bidirectionality

```razor
<!-- RTL 支持 -->
<html dir="rtl">
```

---

## 主题自定义

文档: https://docs.masastack.com/blazor/features/theme

详见 `theme.md`

---

## 自动导航匹配

文档: https://docs.masastack.com/blazor/features/auto-match-nav

### 使用
```razor
<MNavigationDrawer App>
    <MList Nav>
        <MListItem Href="/" Match="NavLinkMatch.All">
            <MListItemIcon><MIcon>mdi-home</MIcon></MListItemIcon>
            <MListItemContent>首页</MListItemContent>
        </MListItem>
        <MListItem Href="/users" Match="NavLinkMatch.Prefix">
            <MListItemIcon><MIcon>mdi-account</MIcon></MListItemIcon>
            <MListItemContent>用户</MListItemContent>
        </MListItem>
    </MList>
</MNavigationDrawer>
```

---

## JS Modules

文档: https://docs.masastack.com/blazor/js-modules/

### Intersection Observer
```razor
@inject IJSRuntime JS

<div @ref="_element">观察目标</div>

@code {
    ElementReference _element;
    
    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            await JS.InvokeVoidAsync("observe", _element, DotNetObjectReference.Create(this));
        }
    }
    
    [JSInvokable]
    public void OnIntersection(IntersectionObserverEntry[] entries)
    {
        // 处理交叉状态
    }
}
```
