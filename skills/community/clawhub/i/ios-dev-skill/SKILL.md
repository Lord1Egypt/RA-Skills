---

name: ios-dev-skill
description: >
  iOS/macOS 开发技能（SwiftUI + UIKit）与 Swift 6.3 语言权威参考合集。覆盖 MVVM/Cocoa 架构、
  网络层（URLSession/async-await）、状态管理（@State/@Published/Combine）、依赖注入、
  Navigation、性能优化、单元测试/UI 测试、持久化、App 分发，以及 Swift 完整语法
  （类型系统/集合/闭包/协议/泛型/并发）。当用户询问 iOS 开发、SwiftUI、Swift 语法、
  Swift 语言任何相关内容时触发。
trigger: iOS 开发|SwiftUI|UIKit|Xcode|Swift 编程|MVVM|iOS 架构|iOS 网络|URLSession|Combine|@State|@Published|iOS 测试|XCTest|Swift 布局|SnapKit|Swift 语法|Swift 类型|Swift 闭包|Swift 泛型|Swift async|Swift await|Swift actor|Swift 代码解释|Swift optional|Swift protocol|Swift struct|Swift class|Swift enum|Swift guard|Swift if let|Swift ??|Swift @escaping|Swift 错误处理|Swift throws|Swift do-catch|Swift 访问控制|Swift extension|Swift 类型转换|Swift Sendable|Swift @propertyWrapper|Swift Property Wrapper|Swift tuple|Swift Optional 解包
tags:
  - ios
  - swiftui
  - uikit
  - xcode
  - swift
  - mvvm
  - ios-architecture
  - ios-network
hermes:
  tags: [ios, swiftui, uikit, xcode, swift, mvvm, ios-architecture, ios-network]
  related_skills: [apple-design, harmonyos-dev]
  version: "1.0.0"
  last_updated: "2026-04-23"
  source: |
    https://developer.apple.com/documentation/swiftui
    https://developer.apple.com/documentation/uikit
    https://developer.apple.com/documentation/xcode
    https://developer.apple.com/documentation/combine
license: MIT
---


# iOS 开发技能

iOS/macOS 应用开发技能，基于 SwiftUI + UIKit。

# 核心架构

## MVVM 架构（SwiftUI）

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│    View     │ ←── │  ViewModel  │ ←── │   Model    │
│  (SwiftUI)  │     │ (ObservableObject) │   │   (Struct) │
└─────────────┘     └──────────────┘     └─────────────┘
     @StateObject          @Published           @State
     @ObservedObject       @State               let
```

**数据流向**：
1. View 订阅 ViewModel 的 @Published 属性
2. ViewModel 处理业务逻辑，调用 Model
3. Model 定义数据结构
4. 状态变化自动触发 View 重新渲染

## UIKit 架构对比

| 模式 | 适用场景 | 复杂度 |
|------|---------|--------|
| MVC | 简单页面 | 低 |
| MVVM | 中等复杂度 | 中 |
| MVP | 需要解耦 View | 中 |
| VIPER | 大型模块化 | 高 |
| Coordinator | 导航复杂 | 高 |

---

## iOS 生命周期与状态管理

### App 生命周期

| 状态 | 触发时机 | 典型用途 |
|------|---------|---------|
| `didFinishLaunching` | App 启动完成 | 初始化配置 |
| `sceneWillEnterForeground` | 从后台恢复 | 刷新数据 |
| `sceneDidBecomeActive` | 获得焦点 | 恢复动画 |
| `sceneWillResignActive` | 失去焦点 | 暂停任务 |
| `sceneDidEnterBackground` | 进入后台 | 保存状态 |

### SwiftUI 状态修饰符

```swift
@State       // 值类型，值语义
@StateObject  // 引用类型，ObservableObject
@ObservedObject // 外部提供的 ObservableObject
@EnvironmentObject // 环境注入的共享状态
@Published   // 属性观察器，自动触发更新
```

### 状态管理对比

| 方式 | 适用场景 | 生命周期 |
|------|---------|---------|
| `@State` | 视图私有 | 随视图 |
| `@StateObject` | 模型对象 | 随视图 |
| `@EnvironmentObject` | 跨视图共享 | 随 App |
| `@AppStorage` | UserDefaults | 持久 |

---

## 数据持久化

### 方案对比

| 方案 | 适用数据量 | 类型 | 线程安全 |
|------|-----------|------|---------|
| `UserDefaults` | < 1MB | Key-Value | ✅ |
| FileManager | 任意 | 文件 | ❌ |
| `PropertyListEncoder` | 中等 | 结构化 | ❌ |
| `SQLite.swift` | 大型 | 关系型 | ✅ |
| Core Data | 超大型 | 对象图 | ✅ |
| Realm | 超大型 | 对象 | ✅ |

### UserDefaults

```swift
@AppStorage("username") var username = ""
@AppStorage("theme") var theme = "light"
```

### SQLite.swift

```swift
import SQLite

let db = try Connection("db.sqlite3")
let users = Table("users")
let id = Expression<Int64>("id")
let name = Expression<String>("name")

try db.run(users.insert(name <- "Alice"))
for user in try db.prepare(users) {
    print(user[name])
}
```

---

## 网络与 API

### URLSession 封装

```swift
enum APIError: Error {
    case invalidURL, noData, decodingError, networkError(Error)
}

func fetch<T: Decodable>(_ type: T.Type, from url: String) async throws -> T {
    guard let url = URL(string: url) else { throw APIError.invalidURL }
    let (data, _) = try await URLSession.shared.data(from: url)
    do {
        return try JSONDecoder().decode(T.self, from: data)
    } catch {
        throw APIError.decodingError
    }
}
```

### SwiftUI 网络图片

```swift
AsyncImage(url: URL(string: "https://...")) { phase in
    switch phase {
    case .empty: ProgressView()
    case .success(let image): image.resizable()
    case .failure: Image(systemName: "photo")
    @unknown default: EmptyView()
    }
}
```

---

## App 分发与发布

### 构建配置

| 配置 | 用途 | 代码签名 |
|------|------|---------|
| Debug | 开发调试 | Development |
| Release | App Store | Distribution |
| Ad Hoc | 测试分发 | Distribution |

### 发布检查清单

- [ ] App Icon 1024×1024
- [ ] 启动屏（Splash Screen）
- [ ] Info.plist 权限说明
- [ ] 隐私政策 URL
- [ ] TestFlight / App Store Connect 上传
- [ ] App Store 截图（6.7 / 6.5 / 5.5 英寸）

### 常用权限声明

| 权限 | Info.plist Key |
|------|---------------|
| 相机 | `NSCameraUsageDescription` |
| 照片 | `NSPhotoLibraryUsageDescription` |
| 位置 | `NSLocationWhenInUseUsageDescription` |
| 通知 | 推送证书配置 |

---

# SwiftUI 基础

### 页面结构
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
    }
}

struct ContentView: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 20) {
            Text("Count: \(count)")
                .font(.largeTitle)
            Button("Increment") { count += 1 }
                .buttonStyle(.borderedProminent)
        }
    }
}
```

### 组件层级
```
Window → ViewController → View → Subviews
NavigationController → ViewController → TableView → Cell
TabBarController → ViewController × N → NavigationController
```

---

# 状态管理

| 状态类型 | SwiftUI | UIKit | 生命周期 |
|---------|---------|-------|---------|
| 本地临时 | @State | local var | 视图存在期间 |
| 页面级 | @State | view property | 页面存在期间 |
| 应用级 | @AppStorage | UserDefaults | 跨页面持久化 |
| 全局共享 | @StateObject | Singleton | 应用生命周期 |

### SwiftUI 状态装饰器

```swift
// @State — 值类型，组件私有
@State private var text = "Hello"

// @Binding — 双向绑定
@Binding var isPresented: Bool

// @StateObject — 引用类型，视图拥有
@StateObject private var viewModel = ViewModel()

// @ObservedObject — 引用类型，外部传入
@ObservedObject var viewModel: ViewModel

// @EnvironmentObject — 环境注入的全局状态
@EnvironmentObject var authService: AuthService

// @AppStorage — 持久化
@AppStorage("username") var username = ""
```

### UIKit 状态

```swift
// 局部变量
class ViewController: UIViewController {
    private var data: [String] = []

    override func viewDidLoad() {
        super.viewDidLoad()
        data = loadData()
    }
}

// 视图属性
class ViewController: UIViewController {
    var initialData: [String] = []
}

// UserDefaults
UserDefaults.standard.string(forKey: "username")

// Singleton
let shared = NetworkManager.shared
```

---

# Navigation 导航模式

### SwiftUI NavigationStack（推荐）

```swift
NavigationStack {
    List(users) { user in
        NavigationLink(destination: UserDetailView(user: user)) {
            Text(user.name)
        }
    }
}
```

### UIKit 导航

```swift
// 导航控制器
let nav = UINavigationController(rootViewController: HomeVC())
nav.pushViewController(detailVC, animated: true)
nav.popViewController(animated: true)

// TabBar 切换
UITabBarController()
  ├─ UINavigationController(首页)
  ├─ UINavigationController(发现)
  └─ UINavigationController(我的)
```

---

# 网络层

### SwiftUI + async/await

```swift
actor NetworkService {
    static let shared = NetworkService()

    func fetch<T: Decodable>(_ type: T.Type, from url: URL) async throws -> T {
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(T.self, from: data)
    }
}

// 使用
Task {
    let users = try await NetworkService.shared.fetch([User].self, from: url)
}
```

### UIKit + async/await

```swift
class NetworkManager {
    static let shared = NetworkManager()

    func request<T: Decodable>(_ type: T.Type, endpoint: String) async throws -> T {
        guard let url = URL(string: endpoint) else {
            throw NetworkError.invalidURL
        }
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(T.self, from: data)
    }
}
```

### URLSession 完整示例

```swift
import Foundation

struct User: Codable, Identifiable {
    let id: String
    let name: String
    let email: String
}

enum NetworkError: Error {
    case invalidURL
    case requestFailed
    case decodingFailed
    case noData
}

class APIClient {
    private let baseURL = "https://api.example.com"
    private let session: URLSession

    init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        self.session = URLSession(configuration: config)
    }

    func get<T: Codable>(_ type: T.Type, path: String) async throws -> T {
        guard let url = URL(string: baseURL + path) else {
            throw NetworkError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.requestFailed
        }

        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase

        do {
            return try decoder.decode(T.self, from: data)
        } catch {
            throw NetworkError.decodingFailed
        }
    }

    func post<T: Codable, B: Encodable>(_ type: T.Type, path: String, body: B) async throws -> T {
        guard let url = URL(string: baseURL + path) else {
            throw NetworkError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let encoder = JSONEncoder()
        encoder.keyEncodingStrategy = .convertToSnakeCase
        request.httpBody = try encoder.encode(body)

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.requestFailed
        }

        return try JSONDecoder().decode(T.self, from: data)
    }
}
```

---

# 依赖注入

### SwiftUI Environment 注入

```swift
struct ContentView: View {
    @EnvironmentObject var authService: AuthService
    var body: some View { ... }
}

// App 层级注入
ContentView()
    .environmentObject(AuthService())
```

### UIKit Protocol 注入

```swift
protocol NetworkServiceProtocol {
    func fetchUsers() async throws -> [User]
}

class ViewModel {
    let networkService: NetworkServiceProtocol
    init(networkService: NetworkServiceProtocol = NetworkService.shared) {
        self.networkService = networkService
    }
}
```

---

# Combine 响应式编程

### Publisher 与 Subscriber

```swift
import Combine

// Publisher
let publisher = PassthroughSubject<String, Never>()

// Subscriber
let cancellable = publisher
    .filter { $0.count > 3 }
    .map { $0.uppercased() }
    .sink { print($0) }

// Future + Promise
func fetchUser(id: Int) -> Future<User, Error> {
    Future { promise in
        // 异步操作
        promise(.success(user))
    }
}
```

### SwiftUI + Combine

```swift
@Published var searchText: String = ""

var searchResults: AnyPublisher<[User], Never> {
    $searchText
        .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
        .removeDuplicates()
        .flatMap { query in
            query.isEmpty ? Just([]).eraseToAnyPublisher()
                         : api.search(query: query)
        }
        .receive(on: DispatchQueue.main)
        .eraseToAnyPublisher()
}

### AnyCancellable 内存管理

```swift
import Combine

class ViewModel {
    private var cancellables = Set<AnyCancellable>()

    func bind() {
        $searchText
            .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
            .sink { [weak self] text in
                self?.performSearch(text)
            }
            .store(in: &cancellables)
    }
}

// Store in property
class AnotherViewModel {
    @Published var data: [Item] = []

    private var cancellables = Set<AnyCancellable>()

    func subscribe(to api: APIService) {
        api.itemsPublisher
            .receive(on: DispatchQueue.main)
            .sink { [weak self] items in
                self?.data = items
            }
            .store(in: &cancellables)
    }
}

// 取消订阅
cancellables.removeAll()  // 手动取消所有
```

### 常用 Operators

| Operator | 用途 |
|----------|------|
| `map` | 转换值 |
| `filter` | 过滤值 |
| `flatMap` | 展平嵌套 Publisher |
| `debounce` | 防抖（搜索场景） |
| `throttle` | 节流（滚动场景） |
| `removeDuplicates` | 去重 |
| `combineLatest` | 合并多个 Publisher |
| `merge` | 合并同类型 Publisher |
| `catch` | 错误处理 |
| `retry` | 重试 |
| `zip` | 配对组合 |

---

# 性能优化

| 场景 | SwiftUI | UIKit |
|------|---------|-------|
| 列表滚动 | LazyVStack | UITableView/UICollectionView |
| 图片缓存 | AsyncImage + 第三方库 | SDWebImage/Kingfisher |
| 预取数据 | .task modifier | UITableViewDataSourcePrefetching |
| 后台任务 | Task.detached | async/await |

### SwiftUI 列表优化

```swift
// ✅ 推荐：LazyVStack
List {
    ForEach(items) { item in
        ItemView(item: item)
    }
}

// ❌ 避免：大列表不用 Lazy
VStack {
    ForEach(items) { item in  // 全部渲染
        ItemView(item: item)
    }
}
```

### UIKit 列表优化

```swift
// UICollectionView 预加载
func collectionView(_ collectionView: UICollectionView, prefetchItemsAt indexPaths: [IndexPath]) {
    for indexPath in indexPaths {
        let item = items[indexPath.item]
        imageLoader.prefetch(url: item.imageURL)
    }
}
```

---

# 测试策略

```
单元测试 → ViewModel / Service 逻辑
   ↓
UI 测试 → View 渲染 + 交互（XCUITest）
   ↓
集成测试 → 模块间交互
   ↓
快照测试 → UI 视觉回归（swift-snapshot-testing）
```

### Swift 单元测试示例

```swift
import XCTest

final class UserViewModelTests: XCTestCase {
    var viewModel: UserListViewModel!
    var mockService: MockNetworkService!

    override func setUp() {
        super.setUp()
        mockService = MockNetworkService()
        viewModel = UserListViewModel(networkService: mockService)
    }

    func testLoadUsersSuccess() async {
        // Given
        mockService.users = [User(id: "1", name: "John")]

        // When
        await viewModel.loadUsers()

        // Then
        XCTAssertEqual(viewModel.users.count, 1)
        XCTAssertFalse(viewModel.isLoading)
    }
}
```

---

# 完整页面示例

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
            users = try await api.fetch(User.self, path: "/users")
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

### UIKit + MVC

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

---

# Swift 语言权威参考

> 来源：The Swift Programming Language (6.3)
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/
> CC BY 4.0 License

## 类型系统

### 基本类型

| 类型 | 说明 | 示例 |
|------|------|------|
| Int | 整数 | `42`, `-7` |
| Double | 64位浮点 | `3.14159` |
| Float | 32位浮点 | `3.14` |
| Bool | 布尔 | `true` / `false` |
| String | 字符串 | `"Hello"` |
| Character | 单字符 | `"A"` |

### 类型推断与注解

```swift
let inferred = 42        // Int
let annotated: Int = 42  // 显式 Int
let pi: Double = 3.14   // Double
```

### 类型别名

```swift
typealias AudioSample = UInt16
typealias Callback = (Int, String) -> Void
```

## Optional 可选类型

### 定义与解包

```swift
// 定义
var serverResponse: String? = nil
var response: String! = nil  // 隐式解包

// 解包方式
if let value = optional {
    print(value)
}

// guard 解包
func process(_ value: String?) {
    guard let value = value else { return }
    print(value)
}

// ?? 操作符
let name = optional ?? "default"

// 链式调用
let upper = optional?.uppercased()
```

### Optional 模式

```swift
// switch 模式匹配
switch optional {
case .some(let value):
    print(value)
case .none:
    print("nil")
}

// 问号链式调用
person?.address?.city
```

##  Tuple 元组

```swift
// 定义
let httpError = (404, "Not Found")
let (code, message) = httpError
let onlyCode = httpError.0

// 命名
let success = (code: 200, message: "OK")
success.code
success.message

// 返回多值
func getUser() -> (name: String, age: Int) {
    return ("Alice", 30)
}
```

## 集合类型

### Array

```swift
// 创建
var arr = [Int]()           // 空
var arr2 = Array(repeating: 0, count: 5)  // [0,0,0,0,0]
let literals = [1, 2, 3]    // 字面量

// 操作
arr.append(4)
arr.insert(0, at: 0)
arr.remove(at: 0)
arr.removeLast()
arr.first
arr.last

// 遍历
for item in arr { }
for (i, v) in arr.enumerated() { }
```

### Set

```swift
// 创建
var set = Set<Int>()
let genres: Set<String> = ["Rock", "Jazz"]

// 操作
set.insert("Pop")
set.remove("Rock")
set.contains("Jazz")

// 集合运算
a.union(b)           // 并集
a.intersection(b)    // 交集
a.subtracting(b)     // 差集
a.symmetricDifference(b)  // 对称差集

// 关系
a.isSubset(of: b)
a.isSuperset(of: b)
a.isDisjoint(with: b)
```

### Dictionary

```swift
// 创建
var dict = [String: Int]()
let capitals = ["CN": "Beijing", "JP": "Tokyo"]

// 操作
dict["key"] = "value"
dict["key"] = nil      // 删除
dict.updateValue("v", forKey: "k")  // 返回旧值

// 安全访问
if let value = dict["key"] { }

// 遍历
for (k, v) in dict { }
for key in dict.keys { }
for value in dict.values { }
```

## 函数

### 定义与调用

```swift
func greet(name: String) -> String {
    return "Hello, \(name)"
}
greet(name: "World")

// 参数标签
func greet(to name: String) -> String {
    return "Hello, \(name)"
}
greet(to: "World")

// 默认参数
func greet(_ name: String = "World") -> String {
    return "Hello, \(name)"
}

// 可变参数
func sum(_ numbers: Int...) -> Int {
    return numbers.reduce(0, +)
}
sum(1, 2, 3, 4, 5)

// inout 参数
func swap(_ a: inout Int, _ b: inout Int) {
    let temp = a
    a = b
    b = temp
}
```

### 函数类型

```swift
var mathFunc: (Int, Int) -> Int = { $0 + $1 }

// 作为参数
func apply(_ op: (Int, Int) -> Int, _ a: Int, _ b: Int) -> Int {
    return op(a, b)
}
apply(mathFunc, 3, 4)

// 作为返回值
func choose(_ op: Bool) -> (Int, Int) -> Int {
    return op ? { $0 + $1 } : { $0 - $1 }
}
```

### 嵌套函数

```swift
func outer() -> () -> Int {
    var count = 0
    func inner() -> Int {
        count += 1
        return count
    }
    return inner
}
```

## 闭包

### 基本语法

```swift
// 完整语法
{ (params) -> ReturnType in
    statements
}

// 类型推断
{ a, b in a + b }

// 无参数
{ () -> Int in 42 }

// 返回类型推断
{ $0 + $1 }
```

### 尾随闭包

```swift
// 不用尾随
arr.map({ (x: Int) -> Int in x * 2 })

// 尾随闭包
arr.map { $0 * 2 }

// 最后一个参数是闭包
arr.map { x in x * 2 }
```

### @escaping

```swift
var handlers: [() -> Void] = []

func withEscaping(_ handler: @escaping () -> Void) {
    handlers.append(handler)
}

func withoutEscaping(_ handler: () -> Void) {
    handler()
}

// 逃逸闭包需要显式 self
class MyClass {
    var x = 10
    func test() {
        withEscaping { self.x = 20 }  // 必须显式
        withoutEscaping { x = 30 }      // 可省略
    }
}
```

### 捕获

```swift
func makeCounter() -> () -> Int {
    var count = 0
    return {
        count += 1
        return count
    }
}
let counter = makeCounter()
counter()  // 1
counter()  // 2
```

## 枚举

```swift
enum Direction {
    case north, south, east, west
}

let dir: Direction = .north

// 关联值
enum Result {
    case success(Data)
    case failure(Error)
}

// 方法
enum Device {
    case phone, tablet
    func description() -> String {
        switch self {
        case .phone: return "iPhone"
        case .tablet: return "iPad"
        }
    }
}

// 原始值
enum ASCIIControl: Character {
    case tab = "\t"
    case newline = "\n"
}
```

## 结构体与类

### 对比

| 特性 | struct | class |
|------|--------|-------|
| 类型 | 值类型 | 引用类型 |
| 继承 | ❌ | ✅ |
| 初始化 | 自动生成 | 手动 |
| 析构 | — | ✅ |
| 引用计数 | — | ✅ |

```swift
struct Point {
    var x: Double
    var y: Double
    // 自动生成 memberwise init
}

class Person {
    var name: String
    var age: Int
    init(name: String, age: Int) {
        self.name = name
        self.age = age
    }
}
```

## 属性

### 存储属性

```swift
struct FixedRange {
    var start: Int
    let end: Int  // 常量
}
```

### 计算属性

```swift
struct Rect {
    var origin: Point
    var size: Size
    var center: Point {
        get {
            Point(x: origin.x + size.width/2,
                  y: origin.y + size.height/2)
        }
        set {
            origin.x = newValue.x - size.width/2
            origin.y = newValue.y - size.height/2
        }
    }
}
```

### 属性包装器

```swift
@propertyWrapper
struct SmallNumber {
    private var number: Int
    var value: Int {
        get { min(number, 12) }
        set { number = newValue }
    }
    init() { number = 0 }
    init(wrappedValue: Int) { number = min(wrappedValue, 12) }
}

@SmallNumber var value: Int  // 使用
```

### 属性观察者

```swift
class StepCounter {
    var totalSteps: Int = 0 {
        willSet { print("will set to \(newValue)") }
        didSet { print("did set from \(oldValue)") }
    }
}
```

### 懒加载

```swift
class DataManager {
    lazy var importer = DataImporter()  // 首次访问时才创建
}
```

## 方法

### 实例方法

```swift
class Counter {
    var count = 0
    func increment() { count += 1 }
    func increment(by amount: Int) { count += amount }
    func reset() { count = 0 }
}
```

### 静态/类方法

```swift
struct MathUtils {
    static func sqrt(_ n: Double) -> Double { ... }
}
MathUtils.sqrt(16)

// 类方法（可被重写）
class Animal {
    class func info() { print("Animal") }
}
```

## 下标

```swift
struct TimesTable {
    subscript(index: Int) -> Int {
        return index * multiplier
    }
}
let table = TimesTable(multiplier: 3)
table[6]  // 18

// 多维下标
struct Matrix {
    subscript(row: Int, col: Int) -> Double {
        get { return grid[row * 3 + col] }
        set { grid[row * 3 + col] = newValue }
    }
}
```

## 继承

```swift
class Vehicle {
    var speed = 0
    func describe() -> String { "speed: \(speed)" }
}

class Bicycle: Vehicle {
    var hasBasket = false
    override func describe() -> String {
        // 调用父类
        return super.describe() + ", basket: \(hasBasket)"
    }
}

// final 类不可被继承
final class FinalClass { }
```

## 初始化与析构

### 初始化

```swift
class ShoppingListItem {
    var name: String
    var quantity: Int = 1
    var completed: Bool = false

    init(name: String, quantity: Int = 1) {
        self.name = name
        self.quantity = quantity
    }
}

// 可失败初始化
struct Animal {
    let species: String
    init?(species: String) {
        if species.isEmpty { return nil }
        self.species = species
    }
}
```

### 析构

```swift
class FileHandler {
    var file: FileHandle
    init() { file = open(...) }
    deinit {
        file.close()
    }
}
```

# 错误处理

## 错误处理

```swift
// 定义错误
enum NetworkError: Error {
    case badURL
    case noData
    case decodingFailed
}

// 抛出
func fetch() throws -> Data {
    guard let url = URL(string: "...") else {
        throw NetworkError.badURL
    }
    return try Data(contentsOf: url)
}

// 处理
do {
    let data = try fetch()
} catch NetworkError.badURL {
    print("Bad URL")
} catch {
    print("Error: \(error)")
}

// try? 转换 Optional
let data = try? fetch()

// try! 强制解包（危险）
let data = try! fetch()
```

# 协议与泛型

## 协议

### 定义与遵循

```swift
protocol ExampleProtocol {
    var simpleDescription: String { get }
    mutating func adjust()
}

// 遵循
struct SimpleStructure: ExampleProtocol {
    var simpleDescription: String = "A simple structure"
    mutating func adjust() { }
}

// 类遵循
class SimpleClass: ExampleProtocol {
    var simpleDescription: String = "A simple class"
    func adjust() { }
}
```

### 协议扩展

```swift
extension Collection {
    func allEven() -> [Element] where Element: Numeric {
        return self.filter { ($0 as? Int ?? 0) % 2 == 0 }
    }
}
```

## 泛型

### 函数泛型

```swift
func swapTwoValues<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}
swapTwoValues(&x, &y)
```

### 类型约束

```swift
func findIndex<T: Equatable>(of valueToFind: T, in array: [T]) -> Int? {
    for (index, value) in array.enumerated() {
        if value == valueToFind { return index }
    }
    return nil
}
```

### 泛型类型

```swift
struct Stack<Element> {
    var items: [Element] = []
    mutating func push(_ item: Element) { items.append(item) }
    mutating func pop() -> Element { items.removeLast() }
}
```

### where 子句

```swift
func allItemsMatch<C1: Container, C2: Container>
    (_ someContainer: C1, _ anotherContainer: C2) -> Bool
    where C1.Element == C2.Element, C1.Element: Equatable
{
    // ...
}
```

## 访问控制

| 修饰符 | 范围 |
|--------|------|
| open | 任意模块，可被继承 |
| public | 任意模块 |
| internal | 模块内（默认） |
| fileprivate | 当前文件 |
| private | 当前作用域 |

```swift
public class PublicClass {
    private var privateVar = 0
    fileprivate var fileVar = 0
}
```

## 扩展

```swift
extension Int {
    var isEven: Bool { return self % 2 == 0 }
    func repetitions(_ task: () -> Void) {
        for _ in 0..<self { task() }
    }
}

5.isEven           // true
3.repetitions { print("Hello") }
```

## 类型转换

```swift
// 类型检查
if item is String {
    print("String")
}

// 向下转型
if let str = item as? String {
    print(str)
}

// 强制转型（危险）
let str = item as! String

// Any 和 AnyObject
var things: [Any] = []
things.append(42)
things.append("string")
```

## 嵌套类型

```swift
struct ChessBoard {
    enum Piece {
        case king, queen, rook, bishop, knight, pawn
    }
    var board: [[Piece?]]
}

let piece: ChessBoard.Piece = .king
```

# Swift 6 并发

## Swift 6 Concurrency

### async/await

```swift
func fetchData() async throws -> Data { ... }

Task {
    do {
        let data = try await fetchData()
    } catch {
        print(error)
    }
}

// async let 并行
async let first = fetchData()
async let second = anotherFetch()
let results = await [first, second]
```

### Task

```swift
// 创建
let task = Task { await doWork() }
let result = await task.value
task.cancel()

// TaskGroup
await withTaskGroup(of: Data.self) { group in
    for url in urls {
        group.addTask { await fetch(url) }
    }
    var results: [Data] = []
    for await data in group {
        results.append(data)
    }
}
```

### Actor

```swift
actor SafeCounter {
    private var count = 0
    func increment() { count += 1 }
    func getCount() -> Int { count }
}

// MainActor
@MainActor
func updateUI() {
    // UI 更新
}
```

### Sendable

```swift
struct User: Sendable { let id: String }

actor SafeLogger: Sendable {
    // actor 自动 Sendable
}
```
---

## 避坑指南

### 常见错误

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 在主线程执行网络请求 | ✅ async/await 自动后台执行 |
| ❌ 不处理网络错误 | ✅ always try-catch + user feedback |
| ❌ @State 用于引用类型 | ✅ @StateObject 用于 class |
| ❌ 不用 LazyVStack 处理大列表 | ✅ 懒加载避免性能问题 |
| ❌ 硬编码 URL | ✅ Configuration/Environment |

### SwiftUI 陷阱

- ⚠️ **@State 复制语义** — @State 修饰的 struct 是值语义，修改会触发重渲染
- ⚠️ **@StateObject 只初始化一次** — 不能在 body 中创建
- ⚠️ **onAppear vs task** — task 可取消，onAppear 不行

### UIKit 陷阱

- ⚠️ **循环引用** — delegate/closure 记得用 [weak self]
- ⚠️ **主线程 UI** — UI 更新必须在主线程
- ⚠️ **Memory Leak** — 及时清理 NotificationCenter 观察者

---

## 来源

> 来源：Apple Developer Documentation（2026-04-23 访问）
> - SwiftUI: https://developer.apple.com/documentation/swiftui
> - UIKit: https://developer.apple.com/documentation/uikit
> - Xcode: https://developer.apple.com/documentation/xcode
> - Combine: https://developer.apple.com/documentation/combine
>
> 更新频率：随 Xcode/iOS 版本迭代

---

# 持久化

### UserDefaults

适用于：小量配置、用户偏好、简单状态

```swift
// SwiftUI
@AppStorage("username") var username = ""
@AppStorage("isDarkMode") var isDarkMode = false

// 代码直接访问
UserDefaults.standard.string(forKey: "username")
UserDefaults.standard.set("value", forKey: "key")
```

### SQLite（生产推荐）

适用于：结构化数据、离线存储、查询性能

```swift
import SQLite

class DatabaseManager {
    static let shared = DatabaseManager()
    private var db: Connection?

    // 表定义
    private let users = Table("users")
    private let id = SQLite.Expression<Int64>("id")
    private let name = SQLite.Expression<String>("name")
    private let email = SQLite.Expression<String>("email")

    init() {
        do {
            let path = NSSearchPathForDirectoriesInDomains(
                .documentDirectory, .userDomainMask, true
            ).first!
            db = try Connection("\(path)/sqlite.db")
            try createTables()
        } catch {
            print("Database error: \(error)")
        }
    }

    private func createTables() throws {
        try db?.run(users.create(ifNotExists: true) { t in
            t.column(id, primaryKey: .autoincrement)
            t.column(name)
            t.column(email)
        })
    }

    // CRUD
    func insertUser(_ user: User) throws {
        let insert = users.insert(
            name <- user.name,
            email <- user.email
        )
        try db?.run(insert)
    }

    func fetchUsers() throws -> [User] {
        guard let db = db else { return [] }
        return try db.prepare(users).map { row in
            User(
                id: row[id],
                name: row[name],
                email: row[email]
            )
        }
    }

    func deleteUser(_ userId: Int64) throws {
        let user = users.filter(id == userId)
        try db?.run(user.delete())
    }
}
```

### Core Data（苹果官方）

适用于：复杂对象图、大量关系数据、Apple 生态深度集成

```swift
// Core Data Stack
class CoreDataManager {
    static let shared = CoreDataManager()

    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "Model")
        container.loadPersistentStores { _, error in
            if let error = error {
                fatalError("Core Data failed: \(error)")
            }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
        return container
    }()

    var viewContext: NSManagedObjectContext {
        persistentContainer.viewContext
    }

    func save() {
        let context = viewContext
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                print("Save error: \(error)")
            }
        }
    }
}

// SwiftUI 集成
struct ContentView: View {
    @Environment(\.managedObjectContext) var viewContext

    @FetchRequest(
        sortDescriptors: [NSSortDescriptor(keyPath: \User.name, ascending: true)],
        animation: .default
    )
    var users: FetchedResults<User>

    var body: some View {
        List(users, id: \.self) { user in
            Text(user.name ?? "Unknown")
        }
    }
}
```

---

# Swift Concurrency 深度

### Sendable 协议

确保数据可以安全跨并发域传递。

```swift
// ✅ 可Sendable的类型
struct User: Sendable {
    let id: String
    let name: String
    // 值类型默认 Sendable
}

// ⚠️ Class 需要手动实现
final class SafeClass: @unchecked Sendable {
    // 不做线程安全假设，仅用于已知安全的场景
}

// ❌ 不可Sendable
class UnsafeClass {
    var cache = [String: Any]()  // 包含可变状态
}
```

### MainActor

确保代码在主线程执行，用于 UI 更新。

```swift
// 方法级别
@MainActor
func updateUI() {
    // 自动在主线程执行
    self.username = "New Name"
}

// 类级别（所有方法默认主线程）
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []

    // 隐式 @MainActor
    func loadItems() async {
        let fetched = await network.fetchItems()
        self.items = fetched  // 安全
    }
}

// 非隔离函数访问主线程数据
nonisolated func describe(_ vm: ViewModel) {
    // ❌ 不能访问 @Published
    // ✅ 可以访问 Sendable 属性
    print("Description")
}
```

### TaskGroup

并发执行多个任务。

```swift
// 并发下载
func fetchAllImages(urls: [URL]) async throws -> [Data] {
    try await withThrowingTaskGroup(of: Data.self) { group in
        for url in urls {
            group.addTask {
                let (data, _) = try await URLSession.shared.data(from: url)
                return data
            }
        }

        var results: [Data] = []
        for try await data in group {
            results.append(data)
        }
        return results
    }
}

// 带取消
func fetchWithCancel(urls: [URL]) async {
    await withTaskGroup(of: Data?.self) { group in
        for url in urls {
            group.addTask {
                try? await Task.sleep(nanoseconds: 1_000_000_000)
                guard !Task.isCancelled else { return nil }
                let (data, _) = try await URLSession.shared.data(from: url)
                return data
            }
        }
    }
}
```

### Task 取消

```swift
// 检查取消
func performWork() async throws {
    for item in items {
        try Task.checkCancellation()  // 抛出 CancellationError
        // 处理 item
    }
}

// withTaskCancellationHandler
try await withTaskCancellationHandler {
    try await longRunningWork()
} onCancel: {
    cleanup()
}

// 传递取消
struct DetailView: View {
    @State private var data: Data?
    @Environment(\.dismiss) var dismiss

    var body: some View {
        Button("加载") {
            Task {
                data = await fetchData()
            }
        }
        .onDisappear {
            // 视图消失时自动取消
        }
    }
}
```

---

# UIKit 进阶

### UICollectionView

生产级列表/网格首选。

```swift
class CollectionViewController: UIViewController {
    private var collectionView: UICollectionView!
    private var dataSource: UICollectionViewDiffableDataSource<Section, Item>!

    enum Section: Hashable {
        case main
        case featured
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        setupCollectionView()
        configureDataSource()
        applySnapshot()
    }

    private func setupCollectionView() {
        // Compositional Layout
        let config = UICollectionLayoutConfiguration(
           -interSectionSpacing: 16
        )
        let layout = UICollectionViewCompositionalLayout(
            sectionProvider: { sectionIndex, environment in
                let itemSize = NSCollectionLayoutSize(
                    widthDimension: .fractionalWidth(0.5),
                    heightDimension: .fractionalHeight(1.0)
                )
                let item = NSCollectionLayoutItem(layoutSize: itemSize)
                item.contentInsets = NSDirectionalEdgeInsets(
                    top: 8, leading: 8, bottom: 8, trailing: 8
                )

                let groupSize = NSCollectionLayoutSize(
                    widthDimension: .fractionalWidth(1.0),
                    heightDimension: .absolute(180)
                )
                let group = NSCollectionLayoutGroup.horizontal(
                    layoutSize: groupSize, subitems: [item]
                )

                let section = NSCollectionLayoutSection(group: group)
                section.contentInsets = NSDirectionalEdgeInsets(
                    top: 0, leading: 16, bottom: 16, trailing: 16
                )

                return NSCollectionLayoutSection(section: section)
            },
            configuration: config
        )

        collectionView = UICollectionView(
            frame: view.bounds,
            collectionViewLayout: layout
        )
        collectionView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        collectionView.delegate = self
        view.addSubview(collectionView)
    }

    private func configureDataSource() {
        let cellRegistration = UICollectionView.CellRegistration<
            UICollectionViewCell, Item
        > { cell, indexPath, item in
            var config = UIListContentConfiguration.cell()
            config.text = item.title
            config.secondaryText = item.subtitle
            config.image = UIImage(systemName: item.icon)
            cell.contentConfiguration = config
        }

        dataSource = UICollectionViewDiffableDataSource<Section, Item>(
            collectionView: collectionView
        ) { collectionView, indexPath, item in
            collectionView.dequeueConfiguredReusableCell(
                using: cellRegistration, for: indexPath, item: item
            )
        }
    }

    private func applySnapshot() {
        var snapshot = NSDiffableDataSourceSnapshot<Section, Item>()
        snapshot.appendSections([.main])
        snapshot.appendItems(items)
        dataSource.apply(snapshot, animatingDifferences: true)
    }
}

extension CollectionViewController: UICollectionViewDelegate {
    func collectionView(
        _ collectionView: UICollectionView,
        didSelectItemAt indexPath: IndexPath
    ) {
        guard let item = dataSource.itemIdentifier(for: indexPath) else { return }
        // 处理选择
    }
}
```

### Auto Layout 完整约束

```swift
// NSLayoutConstraint 语法
label.translatesAutoresizingMaskIntoConstraints = false
NSLayoutConstraint.activate([
    label.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
    label.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -16),
    label.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 16),
    label.heightAnchor.constraint(greaterThanOrEqualToConstant: 44)
])

// 优先级
let highPriority = label.widthAnchor.constraint(equalToConstant: 100)
highPriority.priority = .defaultHigh  // 750

let lowPriority = label.widthAnchor.constraint(equalToConstant: 50)
lowPriority.priority = .defaultLow  // 250

// 比例约束
label.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.5)

// 尺寸约束
label.heightAnchor.constraint(equalTo: label.widthAnchor, multiplier: 1.5)
```

### 键盘处理

```swift
class KeyboardViewController: UIViewController {
    @IBOutlet weak var scrollView: UIScrollView!
    @IBOutlet weak var textField: UITextField!

    override func viewDidLoad() {
        super.viewDidLoad()
        setupKeyboardObservers()
    }

    private func setupKeyboardObservers() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(keyboardWillShow),
            name: UIResponder.keyboardWillShowNotification,
            object: nil
        )
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(keyboardWillHide),
            name: UIResponder.keyboardWillHideNotification,
            object: nil
        )
    }

    @objc func keyboardWillShow(_ notification: Notification) {
        guard let keyboardFrame = notification.userInfo?[
            UIResponder.keyboardFrameEndUserInfoKey
        ] as? CGRect else { return }

        let contentInsets = UIEdgeInsets(
            top: 0, left: 0,
            bottom: keyboardFrame.height, right: 0
        )
        scrollView.contentInset = contentInsets
        scrollView.scrollIndicatorInsets = contentInsets
    }

    @objc func keyboardWillHide(_ notification: Notification) {
        scrollView.contentInset = .zero
        scrollView.scrollIndicatorInsets = .zero
    }

    @objc func dismissKeyboard() {
        view.endEditing(true)
    }
}

// SwiftUI 版本
struct KeyboardAvoidingView: View {
    @State private var text = ""
    @FocusState private var isFocused: Bool

    var body: some View {
        ScrollView {
            TextField("输入", text: $text)
                .focused($isFocused)
                .padding()
                .background(Color.gray.opacity(0.2))
        }
        .onTapGesture {
            isFocused = false
        }
    }
}
```

---

## Swift Concurrency 避坑

### 常见错误

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ nonisolated 函数访问 @Published | ✅ 用 @MainActor 包装 |
| ❌ 跨线程传递 UIView | ✅ 始终在主线程操作 |
| ❌ Task 不保存引用 | ✅ 存储 Task 以支持取消 |
| ❌ 忘记 CancellationError | ✅ 调用 Task.checkCancellation() |
| ❌ actor 内部用锁 | ✅ actor 天然线程安全 |
| ❌ 传递非 Sendable 闭包 | ✅ 确保闭包捕获值是 Sendable |

### @MainActor 传递规则

```swift
@MainActor
class ViewModel {
    func update() { /* 主线程 */ }
}

// ✅ 正确：await 后自动回到主线程
let vm = ViewModel()
Task { @MainActor in
    await someAsyncMethod()
    vm.update()  // 安全
}

// ❌ 错误：非隔离上下文访问
Task {
    await someAsyncMethod()
    // vm.update() // ❌ 编译错误
}
```

---

# Widget 开发

- [widget.md](references/widget.md) — TimelineProvider / App Group / Interactive Widget / Lock Screen Widget

# 国际化与本地化

- [localization.md](references/localization.md) — NSLocalizedString / String Catalog / 格式化 / RTL / App Store 本地化

# Swift Concurrency 权威参考

- [swift-concurrency.md](references/swift-concurrency.md) — async/await / TaskGroup / MainActor / Actor / Sendable / Swift 6

## 快速参考

### SwiftUI 状态装饰器速查

| 装饰器 | 作用域 | 父传子 | 创建者 |
|--------|--------|--------|--------|
| @State | 局部 | ❌ | 视图 |
| @Binding | 局部 | ✅ | 视图 |
| @StateObject | 局部 | ❌ | 视图 |
| @ObservedObject | 局部 | ✅ | 父视图 |
| @EnvironmentObject | 全局 | ✅ | 任意 |
| @AppStorage | 全局 | ✅ | UserDefaults |
| @SceneStorage | 全局 | ✅ | Scene |
| @FocusState | 局部 | ✅ | 视图 |
| @ScaledMetric | 局部 | ✅ | 视图 |

### UIKit vs SwiftUI 生命周期

| 阶段 | UIKit | SwiftUI |
|------|-------|---------|
| 创建 | `init` | `@State init` |
| 加载视图 | `loadView` | body |
| 视图加载 | `viewDidLoad` | `.task` |
| 即将显示 | `viewWillAppear` | `.onAppear` |
| 已显示 | `viewDidAppear` | — |
| 即将消失 | `viewWillDisappear` | `.onDisappear` |
| 已消失 | `viewDidDisappear` | — |
| 内存警告 | `didReceiveMemoryWarning` | `.onChange` |

### iOS 版本支持速查

| API | 最低版本 |
|-----|---------|
| NavigationStack | iOS 16+ |
| @MainActor | iOS 16+ / Swift 5.5+ |
| SwiftUI Charts | iOS 16+ |
| AnyCancellable store | iOS 13+ |
| AsyncSequence | Swift 5.5+ |
| WidgetKit | iOS 14+ |
| Live Activities | iOS 16.1+ |
| Interactive Widget | iOS 17+ |

### Auto Layout 速查

```swift
// 核心约束
label.translatesAutoresizingMaskIntoConstraints = false
NSLayoutConstraint.activate([
    label.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
    label.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -16),
    label.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
    label.heightAnchor.constraint(greaterThanOrEqualToConstant: 44)
])

// SnapKit
view.snp.makeConstraints { make in
    make.edges.equalToSuperview().inset(16)
    make.height.greaterThanOrEqualTo(100)
    make.width.equalToSuperview().multipliedBy(0.5)
}

// 优先级
.widthAnchor.constraint(equalToConstant: 100).priority = .defaultHigh  // 750
.widthAnchor.constraint(equalToConstant: 50).priority = .defaultLow   // 250
.widthAnchor.constraint(equalToConstant: 0).priority = .required      // 1000
```

### 网络状态速查

| 状态 | SwiftUI | UIKit |
|------|---------|-------|
| 空闲 | `isLoading = false` | `state = .idle` |
| 加载中 | `isLoading = true` | `state = .loading` |
| 成功 | `@Published var items` | `delegate?.didFinish` |
| 错误 | `@Published var error` | `delegate?.didFail` |

### Combine 操作符速查

| 操作符 | 用途 | 示例 |
|--------|------|------|
| `map` | 转换值 | `.map { $0 * 2 }` |
| `filter` | 过滤 | `.filter { $0 > 0 }` |
| `flatMap` | 展平 | `.flatMap { $0.publisher }` |
| `debounce` | 防抖 | `.debounce(for: .milliseconds(300), scheduler: RunLoop.main)` |
| `throttle` | 节流 | `.throttle(for: .seconds(1), scheduler: RunLoop.main, latest: true)` |
| `combineLatest` | 合并 | `Publishers.CombineLatest(a, b)` |
| `merge` | 合并同类型 | `a.merge(with: b)` |
| `catch` | 错误处理 | `.catch { Just(default) }` |
| `retry` | 重试 | `.retry(3)` |
| `zip` | 配对 | `a.zip(b)` |

### Auto Layout 速查

```swift
// 核心约束
label.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16)
label.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -16)
label.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor)
label.heightAnchor.constraint(greaterThanOrEqualToConstant: 44)

// SnapKit
view.snp.makeConstraints { make in
    make.edges.equalToSuperview().inset(16)
    make.height.greaterThanOrEqualTo(100)
}

// 优先级
.widthAnchor.constraint(equalToConstant: 100).priority = .defaultHigh
.widthAnchor.constraint(equalToConstant: 50).priority = .defaultLow
```

### Widget 尺寸速查

| 尺寸 | 宽度 | 高度 | 用途 |
|------|------|------|------|
| systemSmall | 155pt | 155pt | 单指标 |
| systemMedium | 329pt | 155pt | 双指标 |
| systemLarge | 329pt | 345pt | 列表卡片 |
| accessoryCircular | — | — | 锁屏圆形 |
| accessoryRectangular | — | — | 锁屏矩形 |

### 常用尺寸速查

| 场景 | 尺寸 |
|------|------|
| 最小点击区域 | 44pt |
| 标准间距 | 16pt |
| 大间距 | 24pt |
| 安全区留边 | 16pt |
| TabBar 高度 | 49pt |
| NavigationBar 高度 | 44pt |
| Widget 圆角 | 20pt |
| 按钮圆角 | 8pt |
| 图片圆角 | 12pt |

### Swift Concurrency 速查

```swift
// async/await
func fetch() async throws -> Data

// Task
Task { await fetch() }
Task.detached { await fetch() }

// TaskGroup
await withTaskGroup(of: Data.self) { group in
    group.addTask { await fetch() }
}

// MainActor
@MainActor func update() { }
Task { @MainActor in update() }

// Sendable
struct User: Sendable { let id: String }
actor SafeCounter { }

// 取消
Task.checkCancellation()
Task.isCancelled
task.cancel()
```

### 生命周期速查

| 事件 | SwiftUI | UIKit |
|------|---------|-------|
| 视图出现 | `.onAppear` | `viewDidAppear` |
| 视图消失 | `.onDisappear` | `viewDidDisappear` |
| 应用激活 | `.onReceive` | `applicationDidBecomeActive` |
| 应用休眠 | — | `applicationWillResignActive` |



## 输出格式规范

当使用本技能回答用户问题时，遵循以下格式：

### 回复结构
1. **直接回答** — 一段简洁的话给出核心答案
2. **代码示例** — 提供完整的 SwiftUI/UIKit 代码（如需）
3. **实现要点** — 关键步骤和注意事项
4. **避坑提醒** — 常见错误+正确做法

### 示例回复（网络请求）

> SwiftUI 推荐使用 async/await 处理网络请求。定义一个 `NetworkService` actor 封装 `URLSession`，在 ViewModel 中用 `@Published` 管理状态。示例：定义 `fetch<T: Decodable>` 泛型方法，用 `Task` 调用并更新 `@Published` 属性。错误处理用 `do-catch`，始终给用户反馈。

### 禁用格式
- ❌ 不要显式分层（避免"第一层/第二层/框架分析"等字眼）
- ❌ 不要长篇解释概念，要直接给出实现
- ❌ 不要只给代码片段，要给完整可运行的示例
- ✅ 输出应是一段干净的话 + 完整代码
