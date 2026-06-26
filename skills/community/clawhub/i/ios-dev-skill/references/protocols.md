# Swift 协议参考

> 来源：The Swift Programming Language (6.3) - Protocols
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/
> 抓取时间：2026-04-23

## 协议基础

```swift
protocol ExampleProtocol {
    var simpleDescription: String { get }
    mutating func adjust()
}
```

### 遵循协议

```swift
// 结构体
struct SimpleStructure: ExampleProtocol {
    var simpleDescription: String = "A simple structure"
    mutating func adjust() {
        simpleDescription += " (adjusted)"
    }
}

// 类
class SimpleClass: ExampleProtocol {
    var simpleDescription: String = "A simple class"
    func adjust() {
        simpleDescription += " (adjusted)"
    }
}
```

## 属性要求

```swift
protocol FullyNamed {
    var fullName: String { get }  // 必须可读
    var displayName: String { get set }  // 可读可写
}

struct Person: FullyNamed {
    var fullName: String
    var displayName: String
}
```

## 方法要求

```swift
protocol RandomNumberGenerator {
    func random() -> Double
}

class LinearCongruentialGenerator: RandomNumberGenerator {
    var lastRandom = 42.0
    func random() -> Double {
        lastRandom = (lastRandom * 3039177861 + 1) % 6075
        return lastRandom / 6075
    }
}
```

## 突变方法要求

```swift
protocol Togglable {
    mutating func toggle()
}

enum OnOffSwitch: Togglable {
    case off, on
    mutating func toggle() {
        switch self {
        case .off: self = .on
        case .on: self = .off
        }
    }
}
```

## 构造器要求

```swift
protocol SomeProtocol {
    init()
    init(name: String)
}

class SomeClass: SomeProtocol {
    var name: String
    required init() {
        self.name = "default"
    }
    required init(name: String) {
        self.name = name
    }
}
```

## 协议作为类型

```swift
protocol DiceGame {
    var dice: Dice { get }
    func play()
}

// 当作类型使用
var game: DiceGame = SnakesAndLadders()
game.play()
```

## 委托模式

```swift
protocol DiceGameDelegate {
    func gameDidStart(_ game: DiceGame)
    func game(_ game: DiceGame, didStartNewTurnWithDiceRoll diceRoll: Int)
    func gameDidEnd(_ game: DiceGame)
}

class Tracker: DiceGameDelegate {
    func gameDidStart(_ game: DiceGame) { }
    func game(_ game: DiceGame, didStartNewTurnWithDiceRoll: Int) { }
    func gameDidEnd(_ game: DiceGame) { }
}
```

## 协议扩展

```swift
extension Collection {
    func allEven() -> [Element] where Element: Numeric {
        return self.filter { ($0 as? Int ?? 0) % 2 == 0 }
    }
}

extension RandomNumberGenerator {
    func randomBool() -> Bool {
        return random() > 0.5
    }
}
```

## 协议约束

```swift
func someFunction<T: SomeProtocol>(thing: T) { }

// where 子句
func allItemsMatch<C1: Container, C2: Container>
    (_ someContainer: C1, _ anotherContainer: C2) -> Bool
    where C1.Element == C2.Element, C1.Element: Equatable
{
    // ...
}
```

## 合成协议

```swift
protocol InEqual: Equatable, Comparable { }

// 自动 Equatable + Comparable
struct Point: InEqual {
    var x: Int, y: Int
}
```

## Class-Only 协议

```swift
protocol ClassOnlyProtocol: AnyObject {
    // 只有类可以遵循
}

// 错误：结构体无法遵循
// struct S: ClassOnlyProtocol { }  // ❌
```

## 协议继承

```swift
protocol PrettyTextRepresentable: TextRepresentable {
    var prettyDescription: String { get }
}
```

## Optional 协议要求（Objective-C）

```swift
@objc
protocol CounterDataSource {
    @objc optional func increment(for counter: Counter) -> Int
    @objc optional var fixedIncrement: Int { get }
}
```

## 来源

> The Swift Programming Language (Swift 6.3)
> Protocols Chapter
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/
