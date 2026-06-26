# Swift 泛型参考

> 来源：The Swift Programming Language (6.3) - Generics
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/generics/
> 抓取时间：2026-04-23

## 泛型函数

```swift
func swapTwoValues<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

var i = 3, j = 5
swapTwoValues(&i, &j)  // T = Int
swapTwoValues(&i, &j)  // T = Double
```

## 类型约束

```swift
// Equatable 约束
func findIndex<T: Equatable>(of valueToFind: T, in array: [T]) -> Int? {
    for (index, value) in array.enumerated() {
        if value == valueToFind { return index }
    }
    return nil
}

// Comparable 约束
func maximum<T: Comparable>(_ array: [T]) -> T? {
    return array.max()
}
```

## 协议约束

```swift
// 继承约束
func send<Request: APIRequest>(_ request: Request) { }

// 类约束
class SomeClass { }
protocol SomeProtocol { }
func someFunction<T: SomeClass, U: SomeProtocol>(some: T, item: U) { }
```

## 泛型类型

```swift
struct Stack<Element> {
    var items: [Element] = []
    mutating func push(_ item: Element) { items.append(item) }
    mutating func pop() -> Element { items.removeLast() }
    var top: Element? { items.last }
}

var stack = Stack<Int>()
stack.push(10)
stack.push(20)
print(stack.pop())  // 20
```

## 泛型扩展

```swift
extension Stack {
    var topItem: Element? {
        return items.isEmpty ? nil : items[items.count - 1]
    }
}

if let top = stack.topItem {
    print(top)
}
```

## 关联类型

```swift
protocol Container {
    associatedtype Item
    mutating func append(_ item: Item)
    var count: Int { get }
    subscript(i: Int) -> Item { get }
}

struct IntStack: Container {
    var items = [Int]()
    mutating func push(_ item: Int) { items.append(item) }
    mutating func pop() -> Int { items.removeLast() }
    
    // 关联类型实现
    typealias Item = Int
    mutating func append(_ item: Int) { push(item) }
    var count: Int { items.count }
    subscript(i: Int) -> Int { items[i] }
}

// 泛型版本
struct GenericStack<Element>: Container {
    var items = [Element]()
    mutating func push(_ item: Element) { items.append(item) }
    mutating func pop() -> Element { items.removeLast() }
    
    mutating func append(_ item: Element) { items.append(item) }
    var count: Int { items.count }
    subscript(i: Int) -> Element { items[i] }
}
```

## where 子句

```swift
// 函数约束
func allItemsMatch<C1: Container, C2: Container>
    (_ someContainer: C1, _ anotherContainer: C2) -> Bool
    where C1.Item == C2.Item, C1.Item: Equatable
{
    if someContainer.count != anotherContainer.count { return false }
    for i in 0..<someContainer.count {
        if someContainer[i] != anotherContainer[i] { return false }
    }
    return true
}

// 扩展约束
extension Container where Item: Comparable {
    func sorted() -> [Item] {
        return items.sorted()
    }
}

// 关联类型约束
protocol ComparableContainer: Container where Item: Comparable {
    // ...
}
```

## 泛型下标

```swift
extension Container {
    subscript<Indices: Sequence>(indices: Indices) -> [Item]
        where Indices.Iterator.Element == Int
    {
        var result: [Item] = []
        for index in indices {
            result.append(self[index])
        }
        return result
    }
}
```

## 泛型 Builder

```swift
// Result Builder
@resultBuilder
struct StringBuilder {
    static func buildBlock(_ parts: String...) -> String {
        parts.joined()
    }
    static func buildIf(_ part: String?) -> String {
        part ?? ""
    }
}

func build(@StringBuilder _ strings: () -> String) -> String {
    strings()
}

let result = build {
    "Hello"
    " "
    "World"
}
```

## 不透明类型 some

```swift
// some 修饰符
func makeProtocol() -> some Equatable {
    return 42  // 返回类型隐藏为 some Equatable
}

// 不透明类型保证具体类型一致
func makeIntStack() -> some Stack {
    var stack = IntStack()
    stack.push(1)
    return stack
}
```

## 泛型约束

| 约束类型 | 语法 | 说明 |
|---------|------|------|
| 类型约束 | `T: Comparable` | T 必须实现 Comparable |
| 协议约束 | `T: SomeProtocol` | T 必须遵循协议 |
| 类约束 | `T: UIView` | T 必须是 UIView 子类 |
| 关联类型 | `T.Iterator` | 使用关联类型 |

## 泛型与 OOP

| 模式 | 泛型实现 | 协议实现 |
|------|---------|---------|
| 通用容器 | `Stack<T>` | `Container` 协议 |
| 通用算法 | `sort<T: Comparable>` | `Comparable` |
| 类型擦除 | `AnyCollection<T>` | `Collection` |

## 来源

> The Swift Programming Language (Swift 6.3)
> Generics Chapter
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/generics/
