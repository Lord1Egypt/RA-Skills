# SwiftUI 基础参考

> 来源：Apple SwiftUI Documentation（2026-04-23）
> https://developer.apple.com/documentation/swiftui

## 视图基础

### 最简单的 App

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### View Protocol

```swift
struct MyView: View {
    var body: some View {
        // 返回单个 View
        Text("Hello")
    }
}
```

### 常用视图

| 视图 | 用途 |
|------|------|
| Text | 文本 |
| Image | 图片 |
| VStack | 垂直布局 |
| HStack | 水平布局 |
| ZStack | 层叠布局 |
| Spacer | 空白填充 |

### 修饰器

```swift
Text("Hello")
    .font(.largeTitle)
    .foregroundColor(.blue)
    .padding()
    .background(Color.yellow)
    .cornerRadius(10)
```

## 状态管理

### @State

```swift
struct Counter: View {
    @State private var count = 0

    var body: some View {
        Button("Count: \(count)") {
            count += 1
        }
    }
}
```

### @Binding

```swift
struct ParentView: View {
    @State private var value = true

    var body: some View {
        ChildView(isOn: $value)
    }
}

struct ChildView: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("", isOn: $isOn)
    }
}
```

### @StateObject

```swift
class ViewModel: ObservableObject {
    @Published var count = 0
}

struct MyView: View {
    @StateObject private var vm = ViewModel()

    var body: some View {
        Text("\(vm.count)")
    }
}
```

### @EnvironmentObject

```swift
// App 层级注入
ContentView()
    .environmentObject(AuthService())

// 视图中使用
@EnvironmentObject var auth: AuthService
```

## 列表

### ForEach

```swift
List {
    ForEach(items) { item in
        ItemRow(item: item)
    }
}
```

### 动态列表

```swift
List(items, id: \.id) { item in
    Text(item.name)
}
```

### 分组

```swift
List {
    Section("Header 1") {
        Text("Item 1")
        Text("Item 2")
    }
    Section("Header 2") {
        Text("Item 3")
    }
}
```

## 导航

### NavigationStack

```swift
NavigationStack {
    List(items) { item in
        NavigationLink(item.name, value: item)
    }
    .navigationDestination(for: Item.self) { item in
        DetailView(item: item)
    }
}
```

### Sheet

```swift
struct ContentView: View {
    @State private var showingSheet = false

    Button("Show Sheet") {
        showingSheet = true
    }
    .sheet(isPresented: $showingSheet) {
        SheetView()
    }
}
```

## 表单

### TextField

```swift
@State private var name = ""
@State private var email = ""

Form {
    TextField("Name", text: $name)
    TextField("Email", text: $email)
        .keyboardType(.emailAddress)
        .textContentType(.emailAddress)
}
```

### Picker

```swift
@State private var selectedColor = 0

Picker("Color", selection: $selectedColor) {
    Text("Red").tag(0)
    Text("Blue").tag(1)
    Text("Green").tag(2)
}
```

## 动画

### 隐式动画

```swift
withAnimation(.easeInOut(duration: 0.3)) {
    isExpanded.toggle()
}
```

### 显式动画

```swift
Button("Animate") {
    withSpring {
        offset = CGSize(width: 100, height: 0)
    }
}
```

### 过渡

```swift
Text("Hello")
    .transition(.opacity.combined(with: .scale))
```
