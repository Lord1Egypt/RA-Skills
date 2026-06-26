# 国际化与本地化参考

> 来源：Apple Localization Documentation（2026-04-23）
> https://developer.apple.com/documentation/localization

## 本地化基础

### 支持语言

| 平台 | 语言代码 | 示例 |
|------|---------|------|
| iOS/macOS | zh-Hans | 简体中文 |
| iOS/macOS | zh-Hant | 繁体中文 |
| iOS/macOS | en | 英语 |
| iOS/macOS | ja | 日语 |
| iOS/macOS | ko | 韩语 |

### 本地化目录结构

```
项目/
├── en.lproj/           # 英语
│   └── Localizable.strings
├── zh-Hans.lproj/      # 简体中文
│   └── Localizable.strings
├── ja.lproj/           # 日语
│   └── Localizable.strings
└── Base.lproj/         # 默认语言
    └── Localizable.strings
```

## NSLocalizedString

### 基本用法

```swift
// 代码中
let title = NSLocalizedString("welcome_title", comment: "欢迎标题")
let message = NSLocalizedString("welcome_message", comment: "欢迎消息")

// 带参数
let greeting = String(format: NSLocalizedString("greeting_format", comment: ""), name, count)
```

### String Catalog（Xcode 15+ 推荐）

```swift
// 新方式：String Catalog (.xcstrings)
struct Strings {
    static func welcome(name: String) -> String {
        String(localized: "Welcome, \(name)")
    }

    static func itemCount(_ count: Int) -> String {
        String(localized: "\(count) items", defaultValue: "\(count) 个项目")
    }
}
```

### .xcstrings 文件格式

```json
{
  "sourceLanguage": "en",
  "strings": {
    "welcome_title": {
      "localizations": {
        "zh-Hans": {
          "stringUnit": {
            "state": "translated",
            "value": "欢迎"
          }
        }
      }
    },
    "greeting_format": {
      "localizations": {
        "zh-Hans": {
          "stringUnit": {
            "state": "translated",
            "value": "你好，%@！"
          }
        }
      }
    }
  }
}
```

## 格式化

### 数字格式化

```swift
let formatter = NumberFormatter()
formatter.numberStyle = .decimal
formatter.maximumFractionDigits = 2

let price = formatter.string(from: 1234.567)  // "1,234.57"
```

### 货币格式化

```swift
let formatter = NumberFormatter()
formatter.numberStyle = .currency
formatter.currencyCode = "CNY"
formatter.locale = Locale(identifier: "zh-Hans")

let price = formatter.string(from: 99.9)  // "¥99.90"
```

### 日期格式化

```swift
let formatter = DateFormatter()
formatter.dateStyle = .medium
formatter.timeStyle = .short
formatter.locale = Locale(identifier: "zh-Hans")

let dateString = formatter.string(from: Date())  // "2024年4月23日 14:30"
```

### 相对日期

```swift
let formatter = RelativeDateTimeFormatter()
formatter.unitsStyle = .full
formatter.locale = Locale(identifier: "zh-Hans")

let relative = formatter.localizedString(for: Date().addingTimeInterval(-3600), relativeTo: Date())
// "1小时前"
```

### 复数格式化

```swift
// Localizable.stringsdict
/*
 %d items = {
    one = "%d 个项目";
    other = "%d 个项目";
 };
 */

// 代码
let format = NSLocalizedString("%d items", comment: "")
let result = String(format: format, count)
```

## SwiftUI 本地化

### Text 本地化

```swift
Text("Hello, World!")
Text("items_count", comment: "项目数量")
Text("\(count) items", comment: "")

// 动态值
Text("greeting", value: name, format: .name(style: .firstName))
```

### 复数

```swift
Text(
    "\(count) items",
    table: "Plurals",
    comment: ""
)

// Plurals.xcstrings
{
    "items_count": {
        "localizations": {
            "zh-Hans": {
                "stringUnit": {
                    "value": "\(count) 个项目"
                }
            }
        }
    }
}
```

## App Store 本地化

### 可本地化内容

| 内容 | 说明 |
|------|------|
| App 名称 | App Store Connect |
| 副标题 | App Store Connect |
| 描述 | 每个语言版本 |
| 关键词 | 每个语言版本 |
| 更新日志 | 每个语言版本 |
| 截图 | 按设备/语言 |

### 本地化截图尺寸

| 设备 | 尺寸 (pt) | 比例 |
|------|----------|------|
| iPhone 6.5" | 1284×2778 | 2.165 |
| iPhone 6.7" | 1290×2796 | 2.165 |
| iPad 12.9" | 2048×2732 | 1.333 |

## RTL 语言支持

### 布局方向

```swift
// SwiftUI
Text("Hello")
    .environment(\.layoutDirection, .rightToLeft)

// UIKit
label.semanticContentAttribute = .forceRightToLeft
view.transform = CGAffineTransform(scaleX: -1, y: 1)
```

### 检测 RTL

```swift
func isRTL() -> Bool {
    let direction = UIApplication.shared.userInterfaceLayoutDirection
    return direction == .rightToLeft
}
```

## 测量单位

| 类型 | 中国 | 美国 |
|------|------|------|
| 距离 | 公里/米 | 英里/英尺 |
| 温度 | 摄氏度 | 华氏度 |
| 重量 | 公斤 | 磅 |
| 体积 | 升 | 加仑 |

```swift
let formatter = MeasurementFormatter()
formatter.unitStyle = .medium
formatter.unitOptions = .providedUnit

let distance = Measurement(value: 10, unit: UnitLength.kilometers)
formatter.string(from: distance)  // "10 km" 或 "6.2 mi"
```

## 字符长度注意

| 语言 | vs 英语 | 示例 |
|------|--------|------|
| 德语 | +20~30% | "Einstellungen" vs "Settings" |
| 俄语 | +10~15% | "Настройки" vs "Settings" |
| 中文 | -50% | "设置" vs "Settings" |
| 日语 | -40% | "設定" vs "Settings" |

## App Icon 本地化

### 本地化 Icon

```
AppIcon/
├── AppIcon.appiconset/
│   ├── Contents.json
│   ├── Icon-60@2x.png      # 英文
│   ├── Icon-60@3x.png      # 英文
│   ├── zh-Hans/
│   │   ├── Icon-60@2x.png  # 中文
│   │   └── Icon-60@3x.png  # 中文
│   └── ja/
│       ├── Icon-60@2x.png  # 日语
│       └── Icon-60@3x.png  # 日语
```

## 来源

> Apple Localization Documentation
> https://developer.apple.com/documentation/localization
