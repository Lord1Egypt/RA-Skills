# SwiftUI 进阶参考

> 来源：Apple SwiftUI Documentation（2026-04-23）
> https://developer.apple.com/documentation/swiftui

## 环境值 @Environment

访问系统级上下文。

```swift
struct DetailView: View {
    @Environment(\.dismiss) var dismiss      // 关闭视图
    @Environment(\.horizontalSizeClass) var hSize  // 水平尺寸类
    @Environment(\.colorScheme) var colorScheme   // 深色/浅色模式
    @Environment(\.managedObjectContext) var context // Core Data
    @Environment(\.scenePhase) var scenePhase     // App 状态

    var body: some View {
        Button("关闭") { dismiss() }
    }
}
```

### 常用 Environment Key

| Key | 类型 | 说明 |
|-----|------|------|
| `.dismiss` | DismissAction | 关闭 Sheet/Navigation |
| `.colorScheme` | ColorScheme | light/dark |
| `.horizontalSizeClass` | UserInterfaceSizeClass? | regular/compact |
| `.managedObjectContext` | NSManagedObjectContext | Core Data |
| `.scenePhase` | ScenePhase | active/inactive/background |

---

## @AppStorage 和 @SceneStorage

```swift
struct SettingsView: View {
    @AppStorage("username") var username = ""
    @AppStorage("notificationsEnabled") var notificationsEnabled = true
    @AppStorage("selectedColor") var selectedColor = "blue"

    var body: some View {
        Form {
            TextField("用户名", text: $username)
            Toggle("启用通知", isOn: $notificationsEnabled)
        }
    }
}

struct FormView: View {
    @SceneStorage("draftText") private var draftText = ""
    @SceneStorage("selectedTab") private var selectedTab = 0

    var body: some View {
        // 数据在同一个 Scene 内持久化
        // 切换 App 会恢复状态
    }
}
```

### 区别

| 修饰器 | 持久化 | 作用域 |
|--------|--------|--------|
| @AppStorage | UserDefaults | 全局 |
| @SceneStorage | UserDefaults | 同一 Scene |
| @State | 内存 | 视图生命周期 |

---

## @FocusState 焦点管理

```swift
struct LoginView: View {
    @State private var email = ""
    @State private var password = ""
    @FocusState private var focusedField: Field?

    enum Field {
        case email, password
    }

    var body: some View {
        VStack {
            TextField("Email", text: $email)
                .focused($focusedField, equals: .email)
                .textContentType(.emailAddress)
                .submitLabel(.next)
                .onSubmit { focusedField = .password }

            SecureField("Password", text: $password)
                .focused($focusedField, equals: .password)
                .textContentType(.password)
                .submitLabel(.go)
                .onSubmit { login() }

            Button("登录") { login() }
                .focused($focusedField, equals: nil)  // 失去焦点
        }
        .toolbar {
            ToolbarItemGroup(placement: .keyboard) {
                Button("完成") { focusedField = nil }
            }
        }
    }
}
```

---

## 高级动画

### animation(_:value:) 绑定动画

```swift
struct AnimatedCard: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Image(systemName: isExpanded ? "star.fill" : "star")
            Text(isExpanded ? "已收藏" : "收藏")
        }
        .padding()
        .background(isExpanded ? Color.yellow : Color.gray.opacity(0.2))
        .cornerRadius(12)
        .animation(.easeInOut(duration: 0.3), value: isExpanded)
        // isExpanded 变化时自动触发动画
    }
}
```

### 过渡 Transitions

```swift
struct TransitionView: View {
    @State private var showDetail = false

    var body: some View {
        ZStack {
            if showDetail {
                DetailView()
                    .transition(.asymmetric(
                        insertion: .scale(scale: 0.8).combined(with: .opacity),
                        removal: .move(edge: .bottom).combined(with: .opacity)
                    ))
            }
        }
        .animation(.spring(response: 0.4, dampingFraction: 0.7), value: showDetail)
    }
}
```

### 手势动画

```swift
struct DraggableView: View {
    @State private var offset = CGSize.zero
    @State private var scale: CGFloat = 1.0

    var body: some View {
        Circle()
            .fill(Color.blue)
            .frame(width: 100, height: 100)
            .offset(offset)
            .scaleEffect(scale)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        offset = value.translation
                        scale = 1.1  // 拖动时放大
                    }
                    .onEnded { _ in
                        offset = .zero
                        scale = 1.0
                    }
            )
    }
}
```

---

## Sheet 和 FullScreenCover

```swift
struct SheetExamples: View {
    @State private var showSheet = false
    @State private var selectedItem: Item?
    @State private var itemToEdit: Item?

    var body: some View {
        // 基本用法
        Button("显示 Sheet") { showSheet = true }
            .sheet(isPresented: $showSheet) {
                BasicSheet()
            }

        // 基于 item 的 Sheet
        Button("编辑项目") { selectedItem = items.first }
            .sheet(item: $selectedItem) { item in
                EditView(item: item)
            }

        // 全屏覆盖
        Button("全屏") { showSheet = true }
            .fullScreenCover(isPresented: $showSheet) {
                FullScreenView()
            }
    }
}

// Dismisser
struct DismissibleSheet: View {
    @Environment(\.dismiss) var dismiss

    var body: some View {
        VStack {
            Text("可滑出关闭")
            Button("手动关闭") { dismiss() }
        }
        .interactiveDismissDisabled()  // 禁用滑出关闭
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
    }
}
```

### Presentation 修饰器

```swift
.sheet(isPresented: $show) { }           // Sheet 弹出
.fullScreenCover(isPresented: $show) { }  // 全屏覆盖
.confirmationDialog("标题", isPresented: $show) { }  // 确认对话框
        .confirmationDialog("选择", isPresented: $show, titleVisibility: .visible) {
            Button("选项1") { }
            Button("选项2", role: .destructive) { }
            Button("取消", role: .cancel) { }
        } message: {
            Text("选择一项操作")
        }
```

---

## Navigation 进阶

### NavigationStack 深度导航

```swift
struct AppNavigation: View {
    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationDestination(for: Item.self) { item in
                DetailView(item: item)
            }
            .navigationDestination(for: String.self) { path in
                // 字符串路径
                RouteView(path: path)
            }
            .navigationDestination(for: Route.self) { route in
                // 枚举路由
                RouteView(route: route)
            }
        }
        .navigationDestination(for: Item.self, destination: { item in
            DetailView(item: item)
        })
    }
}

// Programmatic Navigation
struct ProgrammaticNav: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List {
                ForEach(items) { item in
                    Button(item.name) {
                        path.append(item)
                    }
                }
            }
            .navigationDestination(for: Item.self) { item in
                DetailView(item: item)
            }
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("返回") {
                        path.removeLast()
                    }
                    Button("回首页") {
                        path.removeLast(path.count)  // 回到根
                    }
                }
            }
        }
    }
}
```

### 深度链接 Deep Linking

```swift
struct DeepLinkView: View {
    @Environment(\.navigationDestinationKind) var navKind

    var body: some View {
        if navKind == .push {
            Text("通过导航链进入")
        } else if navKind == .sheet {
            Text("通过 Sheet 进入")
        }
    }
}
```

---

## 列表进阶

### 展开/折叠

```swift
struct ExpandableList: View {
    @State private var expandedSections: Set<String> = []

    var body: some View {
        List {
            ForEach(sections) { section in
                Section {
                    if expandedSections.contains(section.id) {
                        ForEach(section.items) { item in
                            ItemRow(item: item)
                        }
                    }
                } header: {
                    Button {
                        withAnimation {
                            expandedSections.toggle(section.id)
                        }
                    } label: {
                        HStack {
                            Text(section.title)
                            Spacer()
                            Image(systemName: expandedSections.contains(section.id)
                                ? "chevron.up" : "chevron.down")
                        }
                    }
                }
            }
        }
    }
}
```

### Swipe Actions

```swift
struct SwipeList: View {
    @State private var items = ["A", "B", "C"]

    var body: some View {
        List {
            ForEach(items, id: \.self) { item in
                Text(item)
                    .swipeActions(edge: .trailing) {
                        Button(role: .destructive) {
                            items.removeAll { $0 == item }
                        } label: {
                            Label("删除", systemImage: "trash")
                        }
                        Button {
                            // 收藏
                        } label: {
                            Label("收藏", systemImage: "heart")
                        }
                        .tint(.orange)
                    }
                    .swipeActions(edge: .leading) {
                        Button {
                            // 分享
                        } label: {
                            Label("分享", systemImage: "square.and.arrow.up")
                        }
                        .tint(.blue)
                    }
            }
        }
    }
}
```
