# Swift 标准库参考

> 来源：The Swift Programming Language (6.3) - Language Guide 补充
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/
> 抓取时间：2026-04-23

## 字符串 String

### 创建与访问

```swift
let greeting = "Hello, World!"
greeting[greeting.startIndex]           // "H"
greeting[greeting.index(before: greeting.endIndex)]  // "!"
greeting[greeting.index(greeting.startIndex, offsetBy: 7)]  // "W"

// 安全访问
if let idx = greeting.firstIndex(of: ",") {
    let sub = greeting[..<idx]  // "Hello"
}
```

### 常用方法

```swift
let str = "  Hello, Swift!  "

str.hasPrefix("  H")    // true
str.hasSuffix("!  ")    // true
str.lowercased()        // "  hello, swift!  "
str.uppercased()        // "  HELLO, SWIFT!  "
str.trimmingCharacters(in: .whitespaces)  // "  Hello, Swift!"
str.trimmingCharacters(in: .whitespacesAndNewlines)  // "Hello, Swift!"

str.replacingOccurrences(of: "Hello", with: "Hi")  // "  Hi, Swift!  "
str.split(separator: ",")  // ["  Hello", " Swift!  "]
str.count                  // 17
str.isEmpty               // false
```

### 字符串插值

```swift
let name = "Alice"
let age = 30
let bio = "Name: \(name), Age: \(age)"  // "Name: Alice, Age: 30"

// 多行
let multi = """
    Line 1
    Line 2
    """
```

### 正则表达式（Swift 5.7+）

```swift
import Foundation

let text = "Call 123-456-7890 or 987-654-3210"
let pattern = #"\d{3}-\d{3}-\d{4}"#

if let regex = try? Regex(pattern) {
    let matches = text.matches(of: regex)
    for match in matches {
        print(match.output)  // "123-456-7890", "987-654-3210"
    }
    
    // 替换
    let masked = text.replacing(regex, with: "XXX-XXX-XXXX")
    print(masked)
}
```

## 数字 Number

### 常用类型

| 类型 | 说明 | 范围 |
|------|------|------|
| Int | 有符号整数 | 平台相关 |
| Int8/16/32/64 | 指定位宽 | -128~127 等 |
| UInt | 无符号整数 | 平台相关 |
| Double | 64位浮点 | ±10^308 |
| Float | 32位浮点 | ±10^38 |
| Decimal | 高精度十进制 | — |

### 数值转换

```swift
let int: Int = 42
let double = Double(int)  // 42.0
let intFromDouble = Int(3.14)  // 3（截断）

// 安全转换
let big: Int64 = 1000
let small = Int(exactly: big)  // Optional(1000)
let overflow = Int32(exactly: Int64.max)  // nil
```

### 数值方法

```swift
let n = 255

n.isMultiple(of: 3)      // false
n.isEven                  // false
n.isOdd                   // true

let abs = (-42).abs      // 42
let max = Swift.max(10, 20)  // 20
let min = Swift.min(10, 20)  // 10

// 位运算
let shifted = 1 << 3      // 8
let masked = 0b1010 & 0b1100  // 0b1000 = 8
```

### 格式化

```swift
import Foundation

let price = 1234.567

let nf = NumberFormatter()
nf.numberStyle = .decimal
nf.maximumFractionDigits = 2
nf.string(from: NSNumber(value: price))  // "1,234.57"

let cf = NumberFormatter()
cf.numberStyle = .currency
cf.currencyCode = "CNY"
cf.string(from: NSNumber(value: price))  // "¥1,234.57"

// CGFloat 格式化
let width: CGFloat = 100.5
String(format: "%.1f", width)  // "100.5"
```

## 日期 Date

```swift
import Foundation

let now = Date()
let formatter = DateFormatter()

formatter.dateStyle = .medium
formatter.timeStyle = .short
formatter.string(from: now)  // "2024年4月23日 14:30"

formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
formatter.string(from: now)  // "2024-04-23 14:30:00"

// ISO8601
let iso = ISO8601DateFormatter()
iso.string(from: now)  // "2024-04-23T06:30:00Z"

// 加减
let tomorrow = Calendar.current.date(byAdding: .day, value: 1, to: now)!
let yesterday = Calendar.current.date(byAdding: .day, value: -1, to: now)!

// 比较
now > yesterday        // true
now == now            // true

// 组件
let components = Calendar.current.dateComponents([.year, .month, .day], from: now)
components.year        // 2024
components.month       // 4
components.day         // 23
```

## URL

```swift
var url = URL(string: "https://example.com/path?query=value")!

url.scheme             // "https"
url.host               // "example.com"
url.path               // "/path"
url.query              // "query=value"
url.fragment           // nil

// 追加
var base = URL(string: "https://example.com/")!
base.appendPathComponent("api")
base.appendPathComponent("users")
base.appendPathComponent("123")
// "https://example.com/api/users/123"

// 查询参数
var components = URLComponents(url: url, resolvingAgainstBaseURL: true)!
components.queryItems  // [URLQueryItem(name: "query", value: "value")]
components.path         // "/path"

// 构建查询
var build = URLComponents()
build.scheme = "https"
build.host = "api.example.com"
build.path = "/search"
build.queryItems = [
    URLQueryItem(name: "q", value: "swift"),
    URLQueryItem(name: "page", value: "1")
]
build.url?.absoluteString  // "https://api.example.com/search?q=swift&page=1"
```

## FileManager

```swift
import Foundation

let fm = FileManager.default
let docs = fm.urls(for: .documentDirectory, in: .userDomainMask)[0]

// 路径操作
fm.currentDirectoryPath
docs.path

// 文件存在
fm.fileExists(atPath: "test.txt")
fm.fileExists(atPath: docs.path)

// 目录操作
fm.createDirectory(at: docs.appendingPathComponent("cache"), withIntermediateDirectories: true)
fm.removeItem(at: docs.appendingPathComponent("cache"))

// 文件操作
fm.copyItem(at: source, to: dest)
fm.moveItem(at: source, to: dest)

// 属性
let attrs = try fm.attributesOfItem(atPath: "test.txt")
attrs[.size]       // 文件大小
attrs[.creationDate]
attrs[.modificationDate]

// 遍历目录
let contents = try fm.contentsOfDirectory(at: docs, includingPropertiesForKeys: nil)
for file in contents where file.pathExtension == "txt" { }
```

## UserDefaults

```swift
let defaults = UserDefaults.standard

// 存储
defaults.set("Alice", forKey: "username")
defaults.set(42, forKey: "age")
defaults.set([1, 2, 3], forKey: "scores")
defaults.set(true, forKey: "isOnboarded")

// 读取
defaults.string(forKey: "username")    // "Alice"
defaults.integer(forKey: "age")        // 42
defaults.array(forKey: "scores")       // [1, 2, 3]
defaults.bool(forKey: "isOnboarded")   // true

// 监听变化
NotificationCenter.default.addObserver(
    forName: UserDefaults.didChangeNotification,
    object: nil,
    queue: .main
) { _ in
    // 重新读取
}
```

## JSON 编码解码

```swift
import Foundation

struct User: Codable {
    let id: Int
    let name: String
    let email: String?
}

let user = User(id: 1, name: "Alice", email: "alice@example.com")

// 编码
let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
let data = try encoder.encode(user)
let json = String(data: data, encoding: .utf8)!

// 解码
let decoder = JSONDecoder()
decoder.keyDecodingStrategy = .convertFromSnakeCase  // snake_case
let decoded = try decoder.decode(User.self, from: data)

// 通用 Any 解码
let anyDecoder = JSONDecoder()
let anyData = try anyDecoder.decode([String: Any].self, from: data)  // 需 Codable 扩展
```

## 常用宏

| 宏 | 用途 |
|----|------|
| `@main` | 程序入口 |
| `@State` | SwiftUI 状态 |
| `@Binding` | 绑定 |
| `@Published` | Observable 属性 |
| `@ObservedObject` | 观察对象 |
| `@EnvironmentObject` | 环境注入 |
| `@propertyWrapper` | 自定义包装器 |
| `@resultBuilder` | 结果构建器 |
| `@dynamicMemberLookup` | 动态成员查找 |
| `@dynamicCallable` | 动态调用 |

## Result

```swift
enum NetworkError: Error {
    case badURL
    case noData
    case decodingFailed(Error)
}

func fetch() -> Result<Data, NetworkError> {
    guard let url = URL(string: "...") else {
        return .failure(.badURL)
    }
    guard let data = try? Data(contentsOf: url) else {
        return .failure(.noData)
    }
    return .success(data)
}

// 使用
let result = fetch()
switch result {
case .success(let data):
    print(data.count)
case .failure(let error):
    print(error)
}

// map / flatMap
let stringResult = result.map { String(data: $0, encoding: .utf8) }
```

## 常用协议

| 协议 | 用途 |
|------|------|
| Codable | JSON 编解码 |
| Equatable | 相等比较 |
| Hashable | 可哈希/Set/Dict key |
| Comparable | 排序 |
| CustomStringConvertible | print 描述 |
| Identifiable | ID 标识 |
| Sequence | 迭代 |
| Collection | 下标访问 |
| LazySequenceProtocol | 惰性序列 |

### CustomStringConvertible

```swift
struct Point: CustomStringConvertible {
    let x: Int, y: Int
    var description: String { "(\(x), \(y))" }
}

print(Point(x: 1, y: 2))  // "(1, 2)"
```

### Identifiable

```swift
struct User: Identifiable {
    let id: Int
    let name: String
}

// ForEach 无需 id 参数
ForEach(users) { user in
    Text(user.name)
}
```

## 常用扩展

```swift
// String 扩展
extension String {
    var isBlank: Bool { trimmingCharacters(in: .whitespaces).isEmpty }
    func toInt() -> Int? { Int(self) }
}

// Array 扩展
extension Array {
    func chunked(into size: Int) -> [[Element]] {
        stride(from: 0, to: count, by: size).map {
            Array(self[$0..<Swift.min($0 + size, count)])
        }
    }
}

[1, 2, 3, 4, 5].chunked(into: 2)  // [[1,2], [3,4], [5]]
```

## 来源

> The Swift Programming Language (Swift 6.3)
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/
