# iOS 开发技能

iOS/macOS 应用开发与 Swift 6.3 语言权威参考合集，基于 SwiftUI + UIKit。

## 概述

本 skill 覆盖 iOS/macOS 完整开发知识体系，包括：

- **SwiftUI** — 声明式 UI、状态管理、Navigation、数据绑定
- **UIKit** — 视图控制器、Auto Layout、SnapKit、生命周期
- **Swift 语言** — 类型系统、集合、闭包、协议、泛型、并发（async/await/actor）
- **架构模式** — MVVM、依赖注入、Combine 响应式编程
- **网络层** — URLSession、async-await、REST API
- **性能优化** — LazyVStack、图片缓存、预取
- **测试** — XCTest 单元测试、XCUITest UI 测试
- **Widget** — WidgetKit、Live Activities
- **持久化** — UserDefaults、SQLite、FileManager
- **App 分发** — TestFlight、App Store、签名

## 核心章节

### 架构与基础

| 章节 | 内容 |
|------|------|
| [核心架构](SKILL.md#核心架构) | MVVM 架构（SwiftUI）、UIKit 架构对比、iOS 生命周期 |
| [SwiftUI 基础](SKILL.md#SwiftUI-基础) | 页面结构、组件层级、状态装饰器 |
| [状态管理](SKILL.md#状态管理) | @State/@Binding/@StateObject/@ObservedObject/@EnvironmentObject |
| [Navigation 导航模式](SKILL.md#Navigation-导航模式) | NavigationStack、TabBar、Sheet、路由 |
| [网络层](SKILL.md#网络层) | URLSession、async-await、APIClient、错误处理 |
| [依赖注入](SKILL.md#依赖注入) | SwiftUI Environment、UIKit Protocol 注入 |

### Swift 语言权威参考

| 章节 | 内容 |
|------|------|
| [类型系统](SKILL.md#类型系统) | 基本类型、类型推断、类型别名 |
| [Optional 可选类型](SKILL.md#Optional-可选类型) | 解包方式、?? 操作符、guard let |
| [Tuple 元组](SKILL.md#Tuple-元组) | 多元组、命名、解构 |
| [集合类型](SKILL.md#集合类型) | Array、Set、Dictionary |
| [函数](SKILL.md#函数) | 参数标签、默认参数、可变参数、inout |
| [闭包](SKILL.md#闭包) | @escaping、尾随闭包、捕获列表 |
| [枚举](SKILL.md#枚举) | 关联值、原始值、Switch 匹配 |
| [结构体与类](SKILL.md#结构体与类) | 值类型 vs 引用类型、方法、构造器 |
| [属性](SKILL.md#属性) | 存储属性、计算属性、属性包装器 |
| [协议与泛型](SKILL.md#协议与泛型) | 协议扩展、泛型约束、关联类型 |
| [访问控制](SKILL.md#访问控制) | public/private/internal/fileprivate/open |
| [错误处理](SKILL.md#错误处理) | throws/do-catch/try/Result |

### Swift 6 并发

| 章节 | 内容 |
|------|------|
| [Swift 6 Concurrency](SKILL.md#Swift-6-Concurrency) | async/await、actor、Task、Sendable |
| [Swift Concurrency 深度](SKILL.md#Swift-Concurrency-深度) | Structured Concurrency、TaskGroup、MainActor |
| [Swift Concurrency 避坑](SKILL.md#Swift-Concurrency-避坑) | 常见错误与正确做法 |

### UIKit 进阶

| 章节 | 内容 |
|------|------|
| [UIKit 进阶](SKILL.md#UIKit-进阶) | Auto Layout（NSLayoutConstraint + SnapKit）、手势识别、动画 |
| [Widget 开发](SKILL.md#Widget-开发) | WidgetKit、Timeline Provider、Intent |
| [国际化与本地化](SKILL.md#国际化与本地化) | String Catalog、多语言支持 |

### 工程与质量

| 章节 | 内容 |
|------|------|
| [性能优化](SKILL.md#性能优化) | LazyVStack、图片缓存、预取、后台任务 |
| [测试策略](SKILL.md#测试策略) | XCTest 单元测试、XCUITest UI 测试、快照测试 |
| [数据持久化](SKILL.md#数据持久化) | UserDefaults、SQLite、FileManager、AppStorage |
| [App 分发与发布](SKILL.md#App-分发与发布) | TestFlight、App Store Connect、签名配置 |
| [避坑指南](SKILL.md#避坑指南) | 常见错误、SwiftUI/UIKit 陷阱 |

## 快速参考

### SwiftUI 状态装饰器

| 装饰器 | 作用域 | 父传子 | 创建者 |
|--------|--------|--------|--------|
| @State | 局部 | ❌ | 视图 |
| @Binding | 局部 | ✅ | 视图 |
| @StateObject | 局部 | ❌ | 视图 |
| @ObservedObject | 局部 | ✅ | 父视图 |
| @EnvironmentObject | 全局 | ✅ | 任意 |
| @AppStorage | 全局 | ✅ | UserDefaults |
| @SceneStorage | 全局 | ✅ | Scene |

### iOS 版本支持

| API | 最低版本 |
|-----|---------|
| NavigationStack | iOS 16+ |
| @MainActor | iOS 16+ / Swift 5.5+ |
| SwiftUI Charts | iOS 16+ |
| AsyncSequence | Swift 5.5+ |
| WidgetKit | iOS 14+ |
| Live Activities | iOS 16.1+ |
| Interactive Widget | iOS 17+ |

### 最小触摸目标

**44 × 44 pt**（Apple HIG 规定）

## 完整示例

### SwiftUI + MVVM

```swift
// Model
struct User: Identifiable, Codable {
    let id: String
    let name: String
    let email: String
}

// ViewModel
@MainActor
class UserListViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var error: String?

    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }
        do {
            users = try await api.fetchUsers()
        } catch {
            self.error = error.localizedDescription
        }
    }
}

// View
struct UserListView: View {
    @StateObject private var vm = UserListViewModel()

    var body: some View {
        NavigationStack {
            Group {
                if vm.isLoading {
                    ProgressView()
                } else if let error = vm.error {
                    Text("Error: \(error)")
                        .foregroundColor(.red)
                } else {
                    List(vm.users) { user in
                        NavigationLink(destination: UserDetailView(user: user)) {
                            HStack {
                                Text(user.name)
                                Spacer()
                                Text(user.email)
                                    .foregroundColor(.secondary)
                            }
                        }
                    }
                }
            }
            .navigationTitle("用户")
            .task { await vm.loadUsers() }
        }
    }
}
```

### UIKit + Auto Layout（SnapKit）

```swift
import UIKit
import SnapKit

class UserListViewController: UIViewController {
    private let tableView = UITableView(frame: .zero, style: .insetGrouped)
    private var users: [User] = []

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        loadData()
    }

    private func setupUI() {
        title = "用户"
        view.backgroundColor = .systemGroupedBackground

        tableView.delegate = self
        tableView.dataSource = self
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "Cell")
        view.addSubview(tableView)

        tableView.snp.makeConstraints { make in
            make.edges.equalToSuperview()
        }
    }

    private func loadData() {
        Task {
            do {
                users = try await APIClient.shared.get([User].self, path: "/users")
                tableView.reloadData()
            } catch {
                showError(error)
            }
        }
    }
}

extension UserListViewController: UITableViewDataSource, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return users.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath)
        let user = users[indexPath.row]
        var config = cell.defaultContentConfiguration()
        config.text = user.name
        config.secondaryText = user.email
        cell.contentConfiguration = config
        return cell
    }

    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        let user = users[indexPath.row]
        let detailVC = UserDetailViewController(user: user)
        navigationController?.pushViewController(detailVC, animated: true)
    }
}
```

### Swift async/await 网络请求

```swift
actor NetworkService {
    static let shared = NetworkService()

    func fetch<T: Decodable>(_ type: T.Type, from url: URL) async throws -> T {
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(T.self, from: data)
    }
}

struct User: Codable, Identifiable {
    let id: String
    let name: String
    let email: String
}

// 使用
Task {
    let users = try await NetworkService.shared.fetch([User].self, from: url)
}
```

### Swift Concurrency（async/await/actor）

```swift
// actor 线程安全类
actor UserStore {
    private var users: [User] = []

    func add(_ user: User) {
        users.append(user)
    }

    func all() -> [User] {
        return users
    }
}

// Task 和 async/await
func fetchUser(id: String) async throws -> User {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// MainActor 确保 UI 更新在主线程
@MainActor
class ViewModel: ObservableObject {
    @Published var user: User?

    func load() async {
        user = try? await fetchUser(id: "1")
    }
}
```

## 参考文档

| 文件 | 行数 | 内容 |
|------|------|------|
| swift-concurrency.md | 408 | async/await/actor/Task/Sendable/TaskGroup |
| uikit-advanced.md | 504 | Auto Layout/SnapKit/手势/动画/TableView/CollectionView |
| swiftui-advanced.md | 400 | 高级组件、GeometryReader、偏好设置 |
| widget.md | 339 | WidgetKit/Timeline/Live Activities |
| uikit-basics.md | 212 | UIViewController/UIView/生命周期 |
| swiftui-basics.md | 234 | 基础组件、@State、@Binding、Navigation |
| localization.md | 279 | String Catalog/多语言/日期格式化 |
| app-store-distribution.md | 197 | TestFlight/App Store/签名 |
| standard-library.md | 411 | Swift 标准库 API |
| protocols.md | 206 | 协议进阶、Equatable/Hashable/Codable |
| generics.md | 203 | 泛型约束、关联类型、泛型上下文 |
| closures.md | 130 | 闭包逃逸、尾随闭包、捕获语义 |
| collection-types.md | 191 | Array/Set/Dictionary 深度用法 |
| advanced-features.md | 253 | 高级特性、内存管理、反射 |

## 避坑指南

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 在主线程执行网络请求 | ✅ async/await 自动后台执行 |
| ❌ 不处理网络错误 | ✅ always try-catch + user feedback |
| ❌ @State 用于引用类型 | ✅ @StateObject 用于 class |
| ❌ 不用 LazyVStack 处理大列表 | ✅ 懒加载避免性能问题 |
| ❌ 硬编码 URL | ✅ Configuration/Environment |
| ❌ @StateObject 在 body 中创建 | ✅ @StateObject 在视图外初始化 |
| ❌ 循环引用（delegate/closure） | ✅ 记得用 `[weak self]` |

## 来源

> Apple Developer Documentation
> - SwiftUI: https://developer.apple.com/documentation/swiftui
> - UIKit: https://developer.apple.com/documentation/uikit
> - Xcode: https://developer.apple.com/documentation/xcode
> - Combine: https://developer.apple.com/documentation/combine
>
> 版本：Swift 6.3 / iOS 18+
> 更新日期：2026-04-23
