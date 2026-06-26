# Swift 高级特性

> 来源：The Swift Programming Language (6.3) - Advanced Features
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/
> 抓取时间：2026-04-23

## 内存安全

Swift 确保只使用有效内存：

| 特性 | 说明 |
|------|------|
| 栈安全 | 线程局部存储，先进后出 |
| 引用计数 | 类实例自动管理 |
| 无垂悬指针 | 编译器确保 |
| 无未初始化内存 | 必须初始化 |

## 自动引用计数 ARC

```swift
class Person {
    let name: String
    init(name: String) { self.name = name }
}

var ref1: Person?
var ref2: Person?
var ref3: Person?

ref1 = Person(name: "Alice")   // ref1 strong
ref2 = ref1                      // ref2 strong
ref3 = ref1                      // ref3 strong
// 现在有 3 个强引用

ref1 = nil   // 还有 ref2, ref3
ref2 = nil   // 还有 ref3
ref3 = nil   // 引用计数 = 0，deinit 调用
```

### 强引用循环

```swift
class Person {
    let name: String
    var apartment: Apartment?  // strong
    init(name: String) { self.name = name }
}

class Apartment {
    let unit: String
    var tenant: Person?  // strong — 循环引用！
    init(unit: String) { self.unit = unit }
}

var alice: Person?
var unit4A: Apartment?

alice = Person(name: "Alice")
unit4A = Apartment(unit: "4A")

alice!.apartment = unit4A
unit4A!.tenant = alice  // 循环引用！

alice = nil
unit4A = nil  // 内存泄漏！deinit 不会调用
```

### weak 和 unowned

```swift
class Person {
    let name: String
    var apartment: Apartment?  // weak
    init(name: String) { self.name = name }
}

class Apartment {
    let unit: String
    var tenant: Person?  // strong
    init(unit: String) { self.unit = unit }
}

// weak 不增加引用计数，可选
// unowned 不增加引用计数，非可选（假设永不为 nil）
```

### unowned 的使用场景

```swift
class Customer {
    let name: String
    var card: CreditCard?
    init(name: String) { self.name = name }
}

class CreditCard {
    let number: Int
    unowned let customer: Customer  // 非可选
    init(number: Int, customer: Customer) {
        self.number = number
        self.customer = customer
    }
}

// Customer 拥有 CreditCard，CreditCard 引用 Customer
// 假设卡永远属于某个客户
```

### unowned vs weak

| 修饰符 | 可选？ | 使用场景 |
|--------|--------|---------|
| weak | ✅ | 可能为 nil |
| unowned | ❌ | 永不为 nil |

## 类型擦除

### Any 和 AnyObject

```swift
var things: [Any] = []
things.append(42)
things.append("string")
things.append({ $0 > 0 })

// AnyObject（类实例）
var objects: [AnyObject] = []
objects.append(NSObject())
```

### 泛型类型擦除

```swift
// 类型擦除包装
struct AnySequence<Element>: Sequence {
    private var _makeIterator: () -> AnyIterator<Element>
    
    init<S: Sequence>(_ sequence: S) where S.Element == Element {
        _makeIterator = { AnyIterator(sequence.makeIterator()) }
    }
    
    func makeIterator() -> AnyIterator<Element> {
        return _makeIterator()
    }
}
```

## Opaque Types some

```swift
// some 修饰返回类型
protocol Shape {
    func area() -> Double
}

func makeShape() -> some Shape {
    return Circle()
}

// some 保证：
// 1. 返回具体类型一致
// 2. 编译器可优化
// 3. 隐藏实现细节
```

## 关键字速查

| 关键字 | 用途 |
|--------|------|
| `let` | 常量 |
| `var` | 变量 |
| `func` | 函数 |
| `class` | 类 |
| `struct` | 结构体 |
| `enum` | 枚举 |
| `protocol` | 协议 |
| `extension` | 扩展 |
| `init` | 构造器 |
| `deinit` | 析构器 |
| `guard` | 提前退出 |
| `defer` | 延迟执行 |
| `fallthrough` | switch 贯穿 |
| `break` | 跳出循环/switch |
| `continue` | 下一轮循环 |
| `return` | 返回值 |
| `throw` | 抛出错误 |
| `try` | 尝试可能出错 |
| `catch` | 捕获错误 |
| `async` | 异步函数 |
| `await` | 等待异步 |
| `actor` | 隔离类型 |
| `@escaping` | 逃逸闭包 |
| `@autoclosure` | 自动闭包 |
| `@available` | 版本检查 |
| `@main` | 程序入口 |
| `@discardableResult` | 可丢弃返回值 |
| `@inlinable` | 可内联 |
| `@testable` | 测试可见 |

## 声明属性速查

| 修饰符 | 适用 | 说明 |
|--------|------|------|
| `static` | 方法/属性 | 类型成员 |
| `class` | 方法 | 可被重写 |
| `final` | 类/方法 | 不可被继承/重写 |
| `override` | 方法/属性 | 重写父类 |
| `mutating` | 方法 | 修改 self |
| `nonisolated` | 函数/属性 | 跨 actor 访问 |
| `nonisolated(unsafe)` | 属性 | 显式跨域 |

## 访问控制速查

| 修饰符 | 模块内 | 模块外 | 继承 |
|--------|--------|--------|------|
| open | ✅ | ✅ 可继承/重写 | ✅ |
| public | ✅ | ✅ | ❌ |
| internal | ✅ | ❌ | ❌ |
| fileprivate | 当前文件 | ❌ | ❌ |
| private | 当前作用域 | ❌ | ❌ |

## 字符串插值

```swift
// 自定义插值
extension String.StringInterpolation {
    mutating func appendInterpolation(repeat count: Int, _ char: Character) {
        for _ in 0..<count {
            appendLiteral(String(char))
        }
    }
}

let s = "\(repeat: 5, "A")"  // "AAAAA"
```

## Mirror 反射

```swift
import Foundation

let m = Mirror(reflecting: someObject)
for child in m.children {
    if let label = child.label {
        print("\(label): \(child.value)")
    }
}
```

## 来源

> The Swift Programming Language (Swift 6.3)
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/
