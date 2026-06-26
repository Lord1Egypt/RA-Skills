# Swift 6 Concurrency 权威参考

> 来源：The Swift Programming Language (6.3) - Concurrency Chapter
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/
> 抓取时间：2026-04-23

## 核心概念

Swift 并发 = 异步代码 + 并行代码。

| 概念 | 说明 |
|------|------|
| 异步代码 | 可暂停/恢复，同时只执行一段 |
| 并行代码 | 多段代码同时执行（如4核CPU同时运行4段） |
| 数据竞争 (data race) | 多段代码同时访问同一可变状态 |

Swift 在编译期检测并阻止大多数数据竞争。

## 异步函数 async/await

### 定义异步函数

```swift
// 基本异步函数
func listPhotos(inGallery name: String) async -> [String] {
    let result = await fetchPhotos(name: name)
    return result
}

// 异步 + throwing
func fetchPhoto(named name: String) async throws -> Photo {
    guard let photo = try await download(name: name) else {
        throw PhotoError.notFound
    }
    return photo
}
```

### 调用异步函数

```swift
// 普通调用
let photos = await listPhotos(inGallery: "Vacation")

// 异步 + throwing
let photo = try await fetchPhoto(named: "sunset")

// async-let 并行调用
async let first = fetchPhoto(named: photos[0])
async let second = fetchPhoto(named: photos[1])
async let third = fetchPhoto(named: photos[2])

let all = await [first, second, third]
```

### async-let vs await

| 方式 | 适用场景 |
|------|---------|
| `await` | 后续代码依赖结果 |
| `async let` | 结果只需在后面某处使用，可并行 |

## Task 和 TaskGroup

### Task 基础

```swift
// 创建任务
let handle = Task {
    return await fetchData()
}

// 等待结果
let data = await handle.value

// 取消
handle.cancel()
```

### TaskGroup（动态数量任务）

```swift
// 下载任意数量照片
let photos = await withTaskGroup(of: Data.self) { group in
    let names = await listPhotos()

    for name in names {
        group.addTask {
            return await downloadPhoto(named: name)
        }
    }

    var results: [Data] = []
    for await photo in group {
        results.append(photo)
    }
    return results
}

// Throwing 版本
let photos = await withThrowingTaskGroup(of: Data.self) { group in
    // 同上，但 addTask 可 throw
}
```

### Task 取消

```swift
// 方式1：checkCancellation（自动抛出）
func process() async throws {
    try Task.checkCancellation()
    // 继续处理
}

// 方式2：isCancelled（自定义清理）
func process() async {
    for item in items {
        guard !Task.isCancelled else {
            cleanup()
            return
        }
        await processItem(item)
    }
}

// 方式3：withTaskCancellationHandler
let task = await Task.withTaskCancellationHandler {
    await longRunningWork()
} onCancel: {
    cleanupResources()
}
task.cancel()

// addTaskUnlessCancelled
let added = group.addTaskUnlessCancelled {
    await download(name: name)
}
guard added else { break }
```

## 结构化并发 vs 非结构化并发

| 类型 | 说明 |
|------|------|
| 结构化 | TaskGroup/async-let，父子关系，自动取消/传播 |
| 非结构化 | `Task {}`，无父任务，需手动管理 |

```swift
// 结构化（TaskGroup）
await withTaskGroup { group in
    group.addTask { await work() }
}

// 非结构化
let handle = Task {
    await work()
}
await handle.value

// Detached（完全独立）
let detached = Task.detached {
    await work()
}
await detached.value
```

## MainActor

### 概念

MainActor = 保护 UI 数据的 actor，确保所有 UI 更新串行执行。

| 类比 | MainActor | Main Thread |
|------|-----------|-------------|
| 关系 | Swift 层面抽象 | 底层实现 |
| 保证 | 串行访问 UI 数据 | 实际执行代码 |

### @MainActor 用法

```swift
// 函数级别
@MainActor
func updateUI(with data: Data) {
    label.text = "\(data.count) bytes"
}

// 类型级别（struct/class/enum）
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []

    func load() async {
        let fetched = await api.fetch()
        self.items = fetched  // 安全，在 MainActor
    }
}

// 属性级别
struct Gallery {
    @MainActor var photoNames: [String]

    @MainActor
    func drawUI() { /* UI代码 */ }

    func cache() { /* 后台代码 */ }
}

// 闭包
Task { @MainActor in
    show(photo)
}
```

### 调用 @MainActor 函数

```swift
// 从 MainActor 调用：同步
@MainActor
func show(_ photo: Photo) { }

struct MyView: View {
    @StateObject var vm = ViewModel()
    var body: some View {
        Button("Show") {
            show(photo)  // 同步调用
        }
    }
}

// 从非 MainActor 调用：需要 await
func downloadAndShow(name: String) async {
    let photo = await download(name: name)
    await show(photo)  // 需要 await
}
```

## 自定义 Actor

### 定义和用法

```swift
actor TemperatureLogger {
    let label: String
    var measurements: [Int]
    private(set) var max: Int

    init(label: String, measurement: Int) {
        self.label = label
        self.measurements = [measurement]
        self.max = measurement
    }

    func update(with measurement: Int) {
        measurements.append(measurement)
        if measurement > max {
            max = measurement
        }
    }
}

// 访问 actor
let logger = TemperatureLogger(label: "Indoor", measurement: 22)
print(await logger.max)  // 需要 await

// actor 内部访问：不需要 await
extension TemperatureLogger {
    func convertFahrenheitToCelsius() {
        for i in measurements.indices {
            measurements[i] = (measurements[i] - 32) * 5 / 9
        }
    }
}
```

### GlobalActor

```swift
@globalActor
struct DatabaseActor {
    static let shared = DatabaseActor()
}

@DatabaseActor
func saveToDatabase(_ data: Data) async {
    // 在 DatabaseActor 上执行
}
```

## Sendable 协议

### Sendable 条件

| 类型 | Sendable? | 说明 |
|------|-----------|------|
| 值类型（只含 Sendable 属性） | ✅ 自动 | struct/enum |
| 无可变状态的不可变类型 | ✅ 自动 | let 属性 |
| @MainActor 类 | ✅ | UI 框架类 |
| 序列化访问的类 | ✅ | 自行保证线程安全 |
| 普通类 | ❌ | 含可变状态 |

### 显式标记

```swift
// 显式实现
struct Reading: Sendable {
    var value: Int
}

// 显式不可 Sendable
struct UnsafeWrapper {
    let rawPointer: UnsafePointer<Void>
}

@available(*, unavailable)
extension UnsafeWrapper: Sendable {}
```

### 闭包的 Sendable

```swift
// @Sendable 闭包
let task = Task { @Sendable in
    await work()  // 自动 Sendable
}

// actor init 中的 sendable 要求
actor MyActor {
    init(sendable closure: @Sendable @escaping () async -> Void) {
        Task { await closure() }
    }
}
```

## 异步序列 AsyncSequence

```swift
// 基本用法
let handle = FileHandle.standardInput
for try await line in handle.bytes.lines {
    print(line)
}

// 自定义 AsyncSequence
struct Counter: AsyncSequence {
    typealias Element = Int

    struct AsyncIterator: AsyncIteratorProtocol {
        var count = 0
        mutating func next() async -> Int? {
            guard count < 5 else { return nil }
            count += 1
            return count
        }
    }

    func makeAsyncIterator() -> AsyncIterator {
        AsyncIterator()
    }
}

for await i in Counter() {
    print(i)  // 1, 2, 3, 4, 5
}
```

## Swift 6 数据竞争安全

### 编译期检测

Swift 6 默认开启 Complete Concurrency Checking：

```swift
// Swift 6 模式下，以下代码编译错误：
class UnsafeCounter {
    var count = 0
    func increment() { count += 1 }
}

// 正确方式：使用 actor
actor SafeCounter {
    private var count = 0
    func increment() { count += 1 }
    var value: Int { count }
}
```

### 迁移策略（Top-Down）

```
1. 入口点（@main、AppDelegate）标记为 async
2. 逐层向下转换调用方
3. 不能从下往上迁移
```

## 性能考虑

| 操作 | 成本 |
|------|------|
| Task 创建 | 低 |
| await 暂停 | 极低 |
| actor 切换 | 极低 |
| Thread 创建 | 高 |

## 来源

> The Swift Programming Language (Swift 6.3)
> Concurrency Chapter
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/
