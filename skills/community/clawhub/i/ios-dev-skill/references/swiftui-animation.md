# SwiftUI 动画与过渡

> 来源：Apple Developer Documentation — SwiftUI
> URL: https://developer.apple.com/documentation/swiftui/view-transitions
> 整理时间：2026-04-23
> 版本：iOS 17+

## 动画基础

### 动画修饰符

SwiftUI 提供三种主要动画方式：

```swift
// 隐式动画：任何状态变化都自动应用
withAnimation(.easeInOut(duration: 0.3)) {
    isExpanded.toggle()
}

// 显式动画：指定具体属性变化
withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
    scale += 0.1
}

// 绑定动画：直接绑定到 Animation
@State private var amount: Double = 0
Slider(value: $amount.animation(.easeInOut))
```

### 常用动画曲线

| 曲线 | 特点 | 适用场景 |
|------|------|---------|
| `.default` | easeInOut | 通用 |
| `.easeIn` | 缓入 | 进入动画 |
| `.easeOut` | 缓出 | 退出动画 |
| `.easeInOut` | 缓入缓出 | 标准过渡 |
| `.linear` | 匀速 | 进度条 |
| `.spring()` | 弹性 | 弹跳效果 |
| `.interactiveSpring()` | 交互弹性 | 拖拽跟随 |
| `.snappy()` | 快速响应 | 轻快切换 |

### 动画参数

| 参数 | 说明 | 典型值 |
|------|------|-------|
| `duration` | 动画时长（秒） | 0.25 - 0.5 |
| `response` | 弹簧响应 | 0.3 - 0.5 |
| `dampingFraction` | 阻尼系数 | 0.5 - 0.8 |
| `blendDuration` | 混合时长 | 0.0 - 0.3 |

---

## 视图过渡（Transitions）

### transition 修饰符

```swift
// 单边滑入
Rectangle()
    .transition(.move(edge: .trailing))

// 组合过渡
Rectangle()
    .transition(.asymmetric(
        insertion: .scale.combined(with: .opacity),
        removal: .slide
    ))

// 渐变过渡
Rectangle()
    .transition(.opacity)
```

### 常用过渡效果

| 过渡 | 效果 |
|------|------|
| `.opacity` | 透明度 0→1 |
| `.scale` | 缩放 0→1 |
| `.slide` | 滑入滑出 |
| `.move(edge:)` | 指定边滑入 |
| `.combined(with:)` | 组合多个 |
| `.asymmetric(insertion:removal:)` | 不同进出 |
| `.push(from:)` | 推入方向 |
| `.offset(x:y:)` | 平移 |

---

## 显式动画 withAnimation

### 状态驱动动画

```swift
struct ContentView: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Button("Toggle") {
                withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                    isExpanded.toggle()
                }
            }

            if isExpanded {
                DetailView()
                    .transition(.scale.combined(with: .opacity))
            }
        }
    }
}
```

### 动画优先级

| 优先级 | 说明 |
|--------|------|
| Transaction | 最高，覆盖 withAnimation |
| Implicit | 隐式动画（animation 修饰符）|
| Environment | 环境默认动画 |

---

## 动画Modifiers（动画专用修饰符）

### animation 修饰符

```swift
// 应用到所有子视图
Text("Hello")
    .animation(.easeInOut, value: isActive)

// 旋转动画
Image(systemName: "arrow.right")
    .rotationEffect(.degrees(isRotated ? 90 : 0))
    .animation(.easeInOut, value: isRotated)

// 位置动画
circle
    .position(x: x, y: y)
    .animation(.spring(response: 0.3), value: x)
```

### 关键帧动画（Keyframes）

```swift
Text("Bounce")
    .keyframes(
        in: 0...1,
        data: \.scale,
        tracking: 0.1
    ) { value in
        switch value {
        case 0:    return 1.0
        case 0.25: return 1.2
        case 0.5:  return 0.9
        case 0.75: return 1.05
        case 1:    return 1.0
        }
    }
```

---

## 匹配几何过渡（Matched Geometry）

### 跨视图的连续过渡

```swift
@Namespace private var namespace

var body: some View {
    if showDetail {
        DetailView()
            .matchedGeometryEffect(in: namespace, properties: .frame)
            .transition(.opacity)
    } else {
        GridItemView()
            .matchedGeometryEffect(in: namespace, properties: .frame)
            .transition(.opacity)
    }
}
```

### matchedGeometryEffect 属性

| 属性 | 说明 |
|------|------|
| `.frame` | 位置和大小 |
| `.position` | 仅位置 |
| `.size` | 仅大小 |
| `.opacity` | 透明度 |

---

## 手势与动画结合

### 拖拽动画

```swift
struct DraggableView: View {
    @State private var offset = CGSize.zero

    var body: some View {
        Circle()
            .fill(.blue)
            .frame(width: 100, height: 100)
            .offset(offset)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        offset = value.translation
                    }
                    .onEnded { _ in
                        withAnimation(.spring()) {
                            offset = .zero
                        }
                    }
            )
    }
}
```

### 弹性效果

```swift
// 弹簧动画参数
struct SpringPreset {
    static let snappy = Animation.spring(response: 0.3, dampingFraction: 0.7)
    static let bouncy = Animation.spring(response: 0.5, dampingFraction: 0.5)
    static let smooth = Animation.spring(response: 0.5, dampingFraction: 0.8)
}
```

---

## 动画控制

### 暂停 / 恢复

```swift
@State private var isAnimating = false

// 通过绑定控制
ProgressView()
    .animation(isAnimating ? .easeInOut : nil, value: isAnimating)
```

### 动画状态机

| 状态 | 动画 |
|------|------|
| `loading` | `.easeInOut` 循环 |
| `success` | `.spring` 弹跳 |
| `error` | `.shake` 左右抖动 |

---

## 性能注意事项

1. **避免过度动画**：每个动画都消耗 GPU，复杂场景限制在 3 个以内
2. **使用 `drawingGroup()`**：将视图合成位图再渲染，提升性能
3. **优先使用 `opacity`**：比 `scale` / `offset` 性能更好
4. **避免在动画中计算**：提前计算，不要在每帧中计算

---

## 来源

> Apple Developer Documentation — SwiftUI View Transitions
> https://developer.apple.com/documentation/swiftui/view-transitions
> Apple Developer Documentation — Animation
> https://developer.apple.com/documentation/swiftui/animation
