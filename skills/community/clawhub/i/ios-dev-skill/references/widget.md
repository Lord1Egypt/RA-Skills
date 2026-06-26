# Widget 开发参考

> 来源：Apple WidgetKit Documentation（2026-04-23）
> https://developer.apple.com/documentation/widgetkit

## Widget 概述

Widget 在锁屏、主屏幕、通知中心展示应用的实时信息。

### 支持尺寸

| 尺寸 | 平台 | 尺寸 (pt) |
|------|------|-----------|
| systemSmall | iOS/macOS | 155×155 |
| systemMedium | iOS/macOS | 329×155 |
| systemLarge | iOS/macOS | 329×345 |
| accessoryCircular | watchOS | 圆形 |
| accessoryRectangular | watchOS | 矩形 |
| accessoryInline | watchOS | 单行 |
| accessoryCorner | iOS 16+ | 角落 |

### 锁屏 Widget

| 类型 | 形状 | 用途 |
|------|------|------|
| accessoryCircular | 圆形 | 进度环、数据指标 |
| accessoryRectangular | 矩形 | 标题+副标题 |
| accessoryInline | 单行文字 | 简短信息 |

## 基础 Widget

### 项目结构

```
MyWidget/
├── MyWidget.swift           # Widget 配置
├── MyWidgetBundle.swift    # App Entry
├── MyWidgetEntryView.swift  # 视图
└── Assets.xcassets/         # 图片资源
```

### WidgetBundle

```swift
import WidgetKit
import SwiftUI

@main
struct MyWidgetBundle: WidgetBundle {
    var body: some Widget {
        MyWidget()
        if #available(iOS 17.0, *) {
            MyWidget_Interactive()  // iOS 17+ 交互
        }
    }
}
```

### Widget 配置

```swift
struct MyWidget: Widget {
    let kind: String = "MyWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            MyWidgetEntryView(entry: entry)
        }
        .configurationDisplayName("我的 Widget")
        .description("显示实时信息")
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}
```

### TimelineProvider

```swift
struct Provider: TimelineProvider {
    typealias Entry = MyWidgetEntry

    func placeholder(in context: Context) -> MyWidgetEntry {
        MyWidgetEntry(date: Date(), data: .placeholder)
    }

    func getSnapshot(in context: Context, completion: @escaping (MyWidgetEntry) -> Void) {
        let entry = MyWidgetEntry(date: Date(), data: fetchData())
        completion(entry)
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<MyWidgetEntry>) -> Void) {
        var entries: [MyWidgetEntry] = []
        let currentDate = Date()

        for offset in 0..<5 {
            let entryDate = Calendar.current.date(byAdding: .minute, value: offset * 15, to: currentDate)!
            let entry = MyWidgetEntry(date: entryDate, data: fetchData())
            entries.append(entry)
        }

        let timeline = Timeline(entries: entries, policy: .atEnd)
        completion(timeline)
    }

    private func fetchData() -> WidgetData {
        // 从 App Group 获取数据
        return WidgetData()
    }
}
```

### Entry 模型

```swift
struct MyWidgetEntry: TimelineEntry {
    let date: Date
    let data: WidgetData
}

struct WidgetData {
    let title: String
    let value: String
    let trend: Double  // 变化趋势

    static let placeholder = WidgetData(
        title: "加载中",
        value: "...",
        trend: 0
    )
}
```

### Widget 视图

```swift
struct MyWidgetEntryView: View {
    var entry: Provider.Entry
    @Environment(\.widgetFamily) var family

    var body: some View {
        switch family {
        case .systemSmall:
            SmallView(data: entry.data)
        case .systemMedium:
            MediumView(data: entry.data)
        case .systemLarge:
            LargeView(data: entry.data)
        default:
            SmallView(data: entry.data)
        }
    }
}

struct SmallView: View {
    let data: WidgetData

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(data.title)
                .font(.caption)
                .foregroundStyle(.secondary)
            Text(data.value)
                .font(.title2)
                .fontWeight(.bold)
            TrendView(trend: data.trend)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
        .containerBackground(.fill.tertiary, for: .widget)
    }
}
```

## App Group 数据共享

### 配置

1. Xcode: Signing & Capabilities → App Groups → 添加 group.xxx
2. 主 App 和 Widget Extension 都启用同一 App Group

### 共享数据

```swift
// 主 App 写入
let sharedDefaults = UserDefaults(suiteName: "group.xxx")
sharedDefaults?.set(value, forKey: "widgetData")

// Widget 读取
let sharedDefaults = UserDefaults(suiteName: "group.xxx")
let value = sharedDefaults?.string(forKey: "widgetData")

// 通知 Widget 刷新
WidgetCenter.shared.reloadTimelines(ofKind: "MyWidget")
```

## Widget 交互（iOS 17+）

### Link 跳转

```swift
struct MyWidgetEntryView: View {
    var entry: Provider.Entry

    var body: some View {
        Link(destination: URL(string: "myapp://detail/\(entry.data.id)")!) {
            VStack {
                Text(entry.data.title)
            }
        }
    }
}
```

### Interactive Widget（iOS 17+）

```swift
// iOS 17+ Button
struct InteractiveWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "Interactive", provider: Provider()) { entry in
            InteractiveWidgetView(entry: entry)
        }
        .configurationDisplayName("交互 Widget")
    }
}

struct InteractiveWidgetView: View {
    var entry: MyWidgetEntry

    var body: some View {
        Button(intent: IncrementIntent()) {
            VStack {
                Text("\(entry.data.value)")
                    .font(.largeTitle)
                Text("点击 +1")
                    .font(.caption)
            }
        }
        .buttonStyle(.plain)
    }
}

// AppIntent
import AppIntents

struct IncrementIntent: AppIntent {
    static var title: LocalizedStringResource = "增加计数"

    func perform() async throws -> some IntentResult {
        // 更新数据
        return .result()
    }
}
```

## Widget 刷新策略

| 策略 | 说明 | 使用场景 |
|------|------|---------|
| `.atEnd` | Timeline 末尾刷新 | 定期更新 |
| `.after(date)` | 指定时间刷新 | 定时任务 |
| `.never` | 不自动刷新 | 依赖外部触发 |

```swift
let timeline = Timeline(entries: entries, policy: .after(nextUpdateDate))
```

### 背景刷新

```swift
// WidgetCenter 触发刷新
WidgetCenter.shared.reloadTimelines(ofKind: "MyWidget")
WidgetCenter.shared.reloadAllTimelines()

// 主 App 生命周期
class AppDelegate: NSObject, UIApplicationDelegate {
    func applicationDidBecomeActive(_ application: UIApplication) {
        WidgetCenter.shared.reloadTimelines(ofKind: "MyWidget")
    }
}
```

## Lock Screen Widget（iOS 16+）

```swift
struct LockScreenWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "LockScreen", provider: Provider()) { entry in
            LockScreenView(entry: entry)
        }
        .configurationDisplayName("锁屏 Widget")
        .supportedFamilies([.accessoryCircular, .accessoryRectangular, .accessoryInline])
    }
}

struct LockScreenView: View {
    @Environment(\.widgetFamily) var family

    var body: some View {
        switch family {
        case .accessoryCircular:
            Gauge(value: 0.7) {
                Text("%")
            } currentValueLabel: {
                Text("70")
            }
            .gaugeStyle(.accessoryCircularCapacity)

        case .accessoryRectangular:
            VStack(alignment: .leading) {
                Text("今日步数")
                    .font(.headline)
                Text("8,542")
                    .font(.title)
            }

        case .accessoryInline:
            Text("步数: 8,542")

        default:
            EmptyView()
        }
    }
}
```

## 避坑指南

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 复杂布局 | ✅ 简洁信息展示 |
| ❌ 频繁网络请求 | ✅ 读取 App Group 数据 |
| ❌ 耗时操作 | ✅ Timeline 预计算 |
| ❌ 直接更新 UI | ✅ 触发 reloadTimelines |
| ❌ 大图资源 | ✅ SF Symbols / 小图 |

## 来源

> Apple WidgetKit Documentation
> https://developer.apple.com/documentation/widgetkit
