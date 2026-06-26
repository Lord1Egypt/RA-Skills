# Swift 闭包

> 来源：The Swift Programming Language (Swift 6.3) — Closures
> URL: https://docs.swift.org/swift-book/documentation/the-swift-programming-language/closures/
> 整理时间：2026-04-23

## 三种闭包形式

| 类型 | 有名字 | 捕获值 |
|------|--------|--------|
| 全局函数 | ✅ | ❌ |
| 嵌套函数 | ✅ | ✅ |
| 闭包表达式 | ❌ | ✅ |

## 闭包表达式语法

```swift
{ (params) -> ReturnType in
    statements
}
```

### 类型推断

```swift
// 完整形式
reversedNames = names.sorted(by: { (s1: String, s2: String) -> Bool in
    return s1 > s2
})

// 推断后
reversedNames = names.sorted(by: { s1, s2 in return s1 > s2 })

// 单表达式隐式返回
reversedNames = names.sorted(by: { s1, s2 in s1 > s2 })

// 缩写参数名
reversedNames = names.sorted(by: { $0 > $1 })

// 操作符方法
reversedNames = names.sorted(by: >)
```

## 尾随闭包

```swift
// 普通写法
arr.map({ (x: Int) -> Int in x * 2 })

// 尾随闭包
arr.map { $0 * 2 }

// 最后一个参数是闭包
loadPicture(from: server) { picture in
    someView.currentPicture = picture
} onFailure: {
    print("Error")
}
```

## 逃逸闭包 @escaping

```swift
var completionHandlers: [() -> Void] = []

func someFunctionWithEscapingClosure(completionHandler: @escaping () -> Void) {
    completionHandlers.append(completionHandler)
}

// 逃逸闭包需要显式 self
class SomeClass {
    var x = 10
    func doSomething() {
        someFunctionWithEscapingClosure { self.x = 100 }
    }
}

// capture list 打破循环引用
someFunctionWithEscapingClosure { [weak self] in
    self?.x = 100
}
```

## 捕获值

```swift
func makeIncrementer(forIncrement amount: Int) -> () -> Int {
    var runningTotal = 0
    func incrementer() -> Int {
        runningTotal += amount
        return runningTotal
    }
    return incrementer
}

let incrementByTen = makeIncrementer(forIncrement: 10)
incrementByTen()  // 10
incrementByTen()  // 20
```

## @autoclosure

```swift
var customersInLine = ["Chris", "Alex", "Ewa"]

// 普通闭包
func serve(customer provider: () -> String) {
    print("Now serving \(provider())!")
}
serve(customer: { customersInLine.remove(at: 0) })

// @autoclosure（自动包装表达式）
func serve(customer provider: @autoclosure () -> String) {
    print("Now serving \(provider())!")
}
serve(customer: customersInLine.remove(at: 0))  // 无需 {}
```

### @autoclosure 注意事项

| 注意事项 | 说明 |
|---------|------|
| 仅适合无参数闭包 | 参数为 `() -> T` |
| 慎用 | 隐藏闭包执行时机 |
| 调试困难 | 调用栈不直观 |
| 仅用于 API 设计 | Swift 标准库内部使用 |

## 闭包是引用类型

```swift
let alsoIncrementByTen = incrementByTen
alsoIncrementByTen()  // 30
incrementByTen()       // 40
// 两个引用指向同一个闭包实例
```

## 使用场景

| 场景 | 示例 |
|------|------|
| 数组排序 | `arr.sorted { $0 > $1 }` |
| 异步回调 | `fetch { data in ... }` |
| 事件处理 | `button.onTap { ... }` |
| 延迟执行 | `DispatchQueue.main.asyncAfter { ... }` |
| 条件判断 | `arr.filter { $0 > 0 }` |

### 常见高阶函数

```swift
// map：转换每个元素
[1, 2, 3].map { $0 * 2 }        // [2, 4, 6]

// filter：过滤元素
[1, 2, 3].filter { $0 > 1 }    // [2, 3]

// reduce：聚合
[1, 2, 3].reduce(0) { $0 + $1 } // 6

// flatMap：扁平化
[[1, 2], [3]].flatMap { $0 }   // [1, 2, 3]

// compactMap：去除 nil
[1, nil, 3].compactMap { $0 }  // [1, 3]
```

## 闭包与函数

### 闭包作为返回值

```swift
func makeAdder(n: Int) -> (Int) -> Int {
    return { $0 + n }
}

let addFive = makeAdder(n: 5)
addFive(3)  // 8
```

### 闭包作为参数

```swift
func transform(_ array: [Int], using fn: (Int) -> Int) -> [Int] {
    return array.map(fn)
}

transform([1, 2, 3]) { $0 * 2 }  // [2, 4, 6]
```

## 性能注意事项

1. **避免循环引用**：始终使用 `[weak self]` 或 `[unowned self]`
2. **避免过长的闭包**：超过 20 行考虑提取为独立函数
3. **尾随闭包优先**：可读性更好
4. **@escaping 谨慎使用**：仅在必要时标记

## 内存管理

### 内存管理原则

1. **闭包默认捕获变量引用**（强引用）
2. **逃逸闭包必须显式处理 self 引用**
3. **使用 `[weak self]` 打破强引用环**
4. **避免在闭包内直接使用 `self`**

### weak vs unowned

| 场景 | 选择 | 原因 |
|------|------|------|
| ViewController → Closure | `weak self` | ViewController 可能被释放 |
| Self 生命周期确定 | `unowned self` | 避免 Optional 解包 |
| 值类型 | 无需捕获列表 | 不存在引用语义 |
| 闭包内多次使用 | `weak self` + guard | 避免多次判断 |

### 循环引用检测

```swift
// ❌ 循环引用
class MyClass {
    var handler: (() -> Void)!
    func setup() {
        handler = { self.doSomething() }  // self → 闭包 → self
    }
}

// ✅ 正确
class MyClass {
    var handler: (() -> Void)!
    func setup() {
        handler = { [weak self] in self?.doSomething() }
    }
}

// ✅ unowned（确定不会 nil 时）
class MyClass {
    var handler: (() -> Void)!
    func setup() {
        handler = { [unowned self] in self.doSomething() }
    }
}
```

### 内存泄漏场景

| 场景 | 原因 | 解决方案 |
|------|------|---------|
| 网络请求回调 | ViewController 持有闭包，闭包持有 VC | `[weak self]` |
| Timer 回调 | Timer 持有闭包 | `invalidate()` |
| 动画完成回调 | View 持有闭包 | 使用 `nil` 检查 |
| Notification 回调 | 持有闭包 | `removeObserver` |

### 闭包常见错误

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 忘记 `[weak self]` | 内存泄漏 | `[weak self]` |
| `[weak self]` 后不判断 | 运行时崩溃 | `guard let self else { return }` |
| `@escaping` 漏标 | 编译错误 | 添加 `@escaping` |
| 闭包内递归调用 | 栈溢出 | 确保终止条件 |

## 来源

> The Swift Programming Language (Swift 6.3) — Closures
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/closures/

## 附录速查

### 语法速查

| 语法 | 示例 |
|------|------|
| 标准闭包 | `{ x, y in x + y }` |
| 省略参数 | `{ $0 + $1 }` |
| 省略返回 | `arr.sorted { $0 > $1 }` |
| 尾随闭包 | `arr.map { $0 * 2 }` |
| @escaping | 闭包存储后执行 |
| @autoclosure | 表达式自动包装 |
| 捕获列表 | `[weak self], [unowned self]` |

### Swift 标准库常用闭包参数

| 方法 | 闭包签名 | 说明 |
|------|---------|------|
| `map` | `(Element) -> T` | 转换 |
| `filter` | `(Element) -> Bool` | 过滤 |
| `reduce` | `(Result, Element) -> Result` | 聚合 |
| `forEach` | `(Element) -> Void` | 遍历 |
| `compactMap` | `(Element) -> T?` | 去除 nil |
| `flatMap` | `(Element) -> [T]` | 扁平化 |
| `first(where:)` | `(Element) -> Bool` | 查找首个 |
| `contains` | `(Element) -> Bool` | 是否包含 |
| `allSatisfy` | `(Element) -> Bool` | 全部满足 |
| `firstIndex` | `(Element) -> Int?` | 查找下标 |
| `lastIndex` | `(Element) -> Int?` | 查找末尾下标 |
| `last(where:)` | `(Element) -> Element?` | 查找末尾元素 |
| `partition` | `(Element) -> Bool` | 分区重排 |
| `split` | `(Element) -> Bool` | 按条件分割 |
| `min()` | `() -> Element?` | 最小值 |
| `max()` | `() -> Element?` | 最大值 |
| `sorted()` | `() -> [Element]` | 排序副本 |
| `shuffled()` | `() -> [Element]` | 随机打乱 |
| `reversed()` | `() -> [Element]` | 反向副本 |
| `prefix` | `(Int) -> [Element]` | 前缀切片 |
| `suffix` | `(Int) -> [Element]` | 后缀切片 |
| `dropFirst` | `(Int) -> [Element]` | 去除前缀 |
| `dropLast` | `(Int) -> [Element]` | 去除后缀 |
| `chunked` | `(Int) -> [[Element]]` | 分块 |
| `chunked(into:)` | `([Element]) -> [[Element]]` | 按大小分块 |
| `unique` | `() -> [Element]` | 去重（需自定义）|
| `count` | `() -> Int` | 元素个数 |
| `isEmpty` | `() -> Bool` | 是否为空 |
| `randomElement` | `() -> Element?` | 随机元素 |
| `reduce(into:)` | `((inout Result, Element) -> ()) -> Result` | 聚合 |
| `enumerated()` | `() -> [(offset: Int, element: Element)]` | 带索引 |
| `zip` | `(Sequence) -> [(A, B)]` | 合并序列 |
| `product` | `() -> Int` | 元素乘积 |
