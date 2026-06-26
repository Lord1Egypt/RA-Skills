# Swift 集合类型

> 来源：The Swift Programming Language (6.3) - Collection Types
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/collectiontypes/
> 抓取时间：2026-04-23

## 三大集合类型

| 类型 | 有序 | 可重复 | 用途 |
|------|------|--------|------|
| Array | ✅ | ✅ | 顺序列表 |
| Set | ❌ | ❌ | 无序唯一值 |
| Dictionary | ❌ | — | 键值对 |

## Array

### 创建

```swift
// 空数组
var empty: [Int] = []
var anotherEmpty = [Int]()

// 默认值
var threeDoubles = Array(repeating: 0.0, count: 3)  // [0.0, 0.0, 0.0]

// 字面量
var shoppingList = ["Eggs", "Milk"]  // 类型推断 [String]

// 合并
var combined = array1 + array2
```

### 操作

```swift
// 增
shoppingList.append("Flour")
shoppingList += ["Baking Powder"]

// 插入
shoppingList.insert("Maple Syrup", at: 0)

// 删除
let first = shoppingList.removeFirst()
let last = shoppingList.removeLast()
shoppingList.remove(at: 0)
shoppingList.removeAll()

// 访问
let first = shoppingList[0]
let range = shoppingList[1...3]

// 修改
shoppingList[0] = "Six eggs"
shoppingList[1...3] = ["A", "B"]  // 可变长

// 属性
shoppingList.count
shoppingList.isEmpty

// 遍历
for item in shoppingList { }
for (index, value) in shoppingList.enumerated() { }
```

## Set

### 创建

```swift
var letters = Set<Character>()
var favoriteGenres: Set<String> = ["Rock", "Classical", "Hip hop"]
```

### 操作

```swift
// 增删
favoriteGenres.insert("Jazz")
if let removed = favoriteGenres.remove("Rock") { }

// 查询
favoriteGenres.contains("Rock")
favoriteGenres.count
favoriteGenres.isEmpty

// 遍历
for genre in favoriteGenres { }
for genre in favoriteGenres.sorted() { }  // 排序遍历
```

### 集合运算

```swift
let oddDigits: Set = [1, 3, 5, 7, 9]
let evenDigits: Set = [0, 2, 4, 6, 8]

oddDigits.union(evenDigits)           // 并集
oddDigits.intersection(evenDigits)    // 交集
oddDigits.subtracting(singleDigitPrimeNumbers)  // 差集
oddDigits.symmetricDifference(evenDigits)        // 对称差集
```

### 集合关系

```swift
houseAnimals.isSubset(of: farmAnimals)      // 子集
farmAnimals.isSuperset(of: houseAnimals)   // 超集
farmAnimals.isDisjoint(with: cityAnimals)   // 不相交
houseAnimals.isStrictSubset(of: farmAnimals)  // 真子集
```

## Dictionary

### 创建

```swift
var emptyDict: [String: Int] = [:]
var airports = ["YYZ": "Toronto", "DUB": "Dublin"]
```

### 操作

```swift
// 增改
airports["LHR"] = "London"
airports["LHR"] = "London Heathrow"  // 修改

// 安全更新
if let old = airports.updateValue("Dublin Airport", forKey: "DUB") {
    print("旧值: \(old)")
}

// 访问（返回 Optional）
if let name = airports["DUB"] {
    print(name)
}

// 删除
airports["APL"] = nil
if let removed = airports.removeValue(forKey: "DUB") { }

// 遍历
for (code, name) in airports { }
for code in airports.keys { }
for name in airports.values { }

// 转换
let codes = [String](airports.keys)
let names = [String](airports.values)
```

## 性能特性

| 操作 | Array | Set | Dictionary |
|------|-------|-----|------------|
| 读取 | O(1) | O(1) | O(1) |
| 插入(尾) | O(1) amortized | — | — |
| 插入(随机) | O(n) | O(n) | O(n) |
| 删除(随机) | O(n) | O(n) | O(n) |

## 常用扩展

```swift
// 过滤
let filtered = array.filter { $0 > 0 }

// 映射
let doubled = array.map { $0 * 2 }

// 展平
let flat = nestedArray.flatMap { $0 }

// 排序
let sorted = array.sorted()
let sortedDesc = array.sorted(by: >)

// 查找
if let first = array.first(where: { $0 > 5 }) { }

// reduce
let sum = array.reduce(0) { $0 + $1 }
let sum2 = array.reduce(0, +)

// contains
array.contains(where: { $0 > 5 })

// allSatisfy
array.allSatisfy { $0 > 0 }
```

## 性能注意事项

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| `append` | O(1) 均摊 | Array 末尾追加 |
| `insert` | O(n) | 中间插入 |
| `remove(at:)` | O(n) | 删除元素 |
| `contains` | O(n) | 线性搜索 |
| `Dictionary` 查找 | O(1) | 哈希表 |

## 来源

> The Swift Programming Language (Swift 6.3) — Collection Types
> https://docs.swift.org/swift-book/documentation/the-swift-programming-language/collectiontypes/
