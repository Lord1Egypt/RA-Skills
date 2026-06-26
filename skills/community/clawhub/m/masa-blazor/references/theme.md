# 主题系统

文档: https://docs.masastack.com/blazor/features/theme

## 概述
MASA Blazor 基于 Material Design 3 颜色系统，支持亮色/暗色主题切换。

## 主题配置 (Program.cs)
```csharp
builder.Services.AddMasaBlazor(options =>
{
    options.ConfigureTheme(theme =>
    {
        // 亮色主题
        theme.Themes.Light.Primary = "#1976D2";
        theme.Themes.Light.Secondary = "#424242";
        theme.Themes.Light.Accent = "#82B1FF";
        theme.Themes.Light.Error = "#FF5252";
        theme.Themes.Light.Info = "#2196F3";
        theme.Themes.Light.Success = "#4CAF50";
        theme.Themes.Light.Warning = "#FB8C00";
        theme.Themes.Light.Background = "#FFFFFF";
        theme.Themes.Light.Surface = "#FFFFFF";
        
        // 暗色主题
        theme.Themes.Dark.Primary = "#2196F3";
        theme.Themes.Dark.Secondary = "#424242";
        theme.Themes.Dark.Accent = "#FF4081";
        theme.Themes.Dark.Error = "#FF5252";
        theme.Themes.Dark.Info = "#2196F3";
        theme.Themes.Dark.Success = "#4CAF50";
        theme.Themes.Dark.Warning = "#FB8C00";
        theme.Themes.Dark.Background = "#121212";
        theme.Themes.Dark.Surface = "#1E1E1E";
        
        // 全局设置
        theme.Dark = false; // 默认亮色
        theme.DefaultFontFamily = "Roboto, sans-serif";
    });
});
```

## 主题切换
```razor
@inject MasaBlazor MasaBlazor

<MButton OnClick="ToggleDark">
    @(_isDark ? "亮色模式" : "暗色模式")
</MButton>

@code {
    bool _isDark => MasaBlazor.Theme.Dark;
    
    void ToggleDark()
    {
        MasaBlazor.ToggleTheme();
    }
}
```

## CSS 变量
MASA Blazor 使用 CSS 变量管理主题：

```css
:root {
    /* 亮色主题变量 */
    --m-theme-light-primary: #1976D2;
    --m-theme-light-secondary: #424242;
    --m-theme-light-accent: #82B1FF;
    --m-theme-light-error: #FF5252;
    --m-theme-light-info: #2196F3;
    --m-theme-light-success: #4CAF50;
    --m-theme-light-warning: #FB8C00;
    --m-theme-light-background: #FFFFFF;
    --m-theme-light-surface: #FFFFFF;
    --m-theme-light-on-primary: #FFFFFF;
    --m-theme-light-on-secondary: #FFFFFF;
    --m-theme-light-on-background: rgba(0, 0, 0, 0.87);
    --m-theme-light-on-surface: rgba(0, 0, 0, 0.87);
}

.m-theme--dark {
    /* 暗色主题变量 */
    --m-theme-dark-primary: #2196F3;
    --m-theme-dark-background: #121212;
    --m-theme-dark-surface: #1E1E1E;
    --m-theme-dark-on-background: #FFFFFF;
    --m-theme-dark-on-surface: #FFFFFF;
}
```

## 自定义 CSS 变量
```css
/* 在全局样式文件中覆盖 */
:root {
    --m-theme-light-primary: #6200EA;
    --m-theme-light-secondary: #03DAC6;
}
```

## MThemeProvider 局部主题
```razor
<!-- 局部使用暗色主题 -->
<MThemeProvider Dark>
    <MCard>
        <MCardTitle>暗色卡片</MCardTitle>
    </MCard>
</MThemeProvider>

<!-- 局部覆盖主色 -->
<MThemeProvider RootTheme="customTheme">
    <MButton Color="primary">自定义主色</MButton>
</MThemeProvider>
```

## 颜色工具类
```razor
<!-- 背景色 -->
<div class="red">红色背景</div>
<div class="blue lighten-2">浅蓝色背景</div>
<div class="green darken-3">深绿色背景</div>

<!-- 文本色 -->
<p class="red--text">红色文本</p>
<p class="blue--text text--lighten-2">浅蓝色文本</p>
<p class="green--text text--darken-3">深绿色文本</p>
```

## 常用颜色
- **red, pink, purple, deep-purple, indigo, blue, light-blue, cyan, teal, green, light-green, lime, yellow, amber, orange, deep-orange**
- **brown, blue-grey, grey**
- **shade**: lighten-1~5, darken-1~4, accent-1~4
