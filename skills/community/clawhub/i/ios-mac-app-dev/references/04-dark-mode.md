# 深色模式适配

> iOS 13+ / macOS 10.15+ 深色模式完整适配方案。

## 自适应颜色系统

### 推荐方案：Asset Catalog 命名颜色

```
Assets.xcassets/
├── AccentColor.colorset/          # Light: #007AFF   Dark: #0A84FF
│   ├── Contents.json
│   ├── 1x.png (light)
│   └── 1x-dark.png (dark)
├── Background.colorset/           # Light: #FFFFFF   Dark: #1C1C1E
├── TextPrimary.colorset/          # Light: #000000   Dark: #FFFFFF
├── Surface.colorset/              # Light: #F2F2F7   Dark: #2C2C2E
└── ...
```

### 程序化颜色（后备方案）

```swift
static func adaptiveColor(light: Color, dark: Color) -> Color {
    Color(UIColor { traitCollection in
        traitCollection.userInterfaceStyle == .dark 
            ? UIColor(light) 
            : UIColor(dark)
    })
}
```

## 深色模式色彩规范

| 色值 | Light Mode | Dark Mode |
|------|-----------|-----------|
| 背景色 | #FFFFFF | #1C1C1E |
| 次级背景 | #F2F2F7 | #2C2C2E |
| 三级背景 | #FFFFFF | #3A3A3C |
| 主文字 | #000000 | #FFFFFF |
| 次级文字 | #3C3C43 (60%) | #EBEBF5 (60%) |
| 分割线 | #C6C6C8 (30%) | #545458 (60%) |

**关键原则：** 深色模式下饱和度限制在 **200-500**之间，避免高饱和度颜色刺眼。

## 检查清单

| # | 检查项 | 自动检查 |
|---|--------|----------|
| ✅ | 所有硬编码颜色替换为 Asset Catalog 命名颜色 | ✅ |
| ✅ | 所有图片提供深色模式变体 | ✅ |
| ✅ | 毛玻璃效果使用 `.ultraThinMaterial` | ✅ |
| ✅ | 深色模式下阴影增加亮度 | ⚠️ 需手动 |
| ✅ | 对比度满足 WCAG AA 标准 (≥4.5:1) | ✅ |
| ✅ | 自定义绘图使用 `traitCollection.userInterfaceStyle` | ✅ |

## SwiftUI 深色模式检查代码

```swift
struct DarkModePreview: PreviewModifier {
    static func makeValue() -> ColorScheme {
        .dark
    }
    
    func body(content: Content, _ value: ColorScheme) -> some View {
        content.preferredColorScheme(value)
    }
}

// 为每个 View 写深色模式 Preview
#Preview {
    ContentView()
        .previewDisplayName("深色模式")
}
```
