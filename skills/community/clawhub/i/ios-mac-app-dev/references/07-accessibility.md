# 无障碍支持

> VoiceOver、Dynamic Type、WCAG 标准完整指南。

## Dynamic Type

```swift
struct ContentView: View {
    @Environment(\.dynamicTypeSize) var dynamicTypeSize
    @ScaledMetric var padding: CGFloat = 16
    
    var body: some View {
        Text("自适应文字大小")
            .font(.body)  // 自动跟随系统设置
            .dynamicTypeSize(...DynamicTypeSize.xxxLarge)
        
        // 自定义视图约束
        CustomView()
            .frame(height: padding * 4)
    }
}
```

## VoiceOver

```swift
// 1. 基本标签
Button(action: sendMessage) {
    Image(systemName: "paperplane.fill")
}
.accessibilityLabel("发送消息")
.accessibilityHint("点击发送当前编辑的消息")

// 2. 自定义手势
Rectangle()
    .accessibilityAction(.magicTap) { handleMagicTap() }
    .accessibilityAction(.escape) { dismiss() }

// 3. 合并/分组
VStack {
    Text("¥\(price)")
    Text("含税")
}
.accessibilityElement(children: .combine)
.accessibilityLabel("价格 \(price) 元，含税")

// 4. 忽略装饰元素
Image("background")
    .accessibilityHidden(true)
```

## WCAG 对比度标准

| 级别 | 标准文本对比度 | 大文本对比度 |
|------|---------------|--------------|
| AA | ≥ 4.5:1 | ≥ 3:1 |
| AAA | ≥ 7:1 | ≥ 4.5:1 |

## 检查清单

- [ ] 所有图片控件有 `accessibilityLabel`
- [ ] Dynamic Type 支持 (`.dynamicTypeSize(...DynamicTypeSize.xxxLarge)`)
- [ ] 对比度 ≥ 4.5:1
- [ ] 装饰性元素标记 `accessibilityHidden(true)`
- [ ] 用户界面元素可聚焦 (VoiceOver)
- [ ] 支持「辅助触控」
- [ ] 视频支持隐藏式字幕
- [ ] 减少动态效果时禁用动画 (`@Environment(\.accessibilityReduceMotion)`)
- [ ] 减少透明度时移除毛玻璃 (`@Environment(\.accessibilityReduceTransparency)`)
