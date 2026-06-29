# 性能优化

> 启动速度、内存管理、渲染性能优化指南。

## 启动优化

### 冷启动优化策略

```swift
// 1. 懒加载非关键服务
class AppDelegate {
    lazy var analyticsService = AnalyticsService()
    lazy var syncService = CloudSyncService()
    
    func application(_ application: UIApplication,
                    didFinishLaunchingWithOptions options: ...) -> Bool {
        // 仅初始化关键路径
        configureCrashReporting()
        return true
    }
}
```

**检查清单：**
- [ ] 启动时间 < 400ms
- [ ] 不使用 `DispatchQueue.main.sync`
- [ ] 避免在 `application:didFinishLaunching` 中执行网络请求
- [ ] Storyboard 改用纯代码/SwiftUI
- [ ] 使用 `static` 避免动态库链接开销

## 内存管理

```swift
// 1. 弱引用避免循环引用
class NetworkManager {
    private var tasks: [UUID: URLSessionTask] = [:]
    
    func fetch<T>(_ endpoint: APIEndpoint) async throws -> T {
        // async/await 自动管理引用
    }
}

// 2. 图片缓存
let cache = URLCache(
    memoryCapacity: 50 * 1024 * 1024,  // 50MB
    diskCapacity: 200 * 1024 * 1024    // 200MB
)

// 3. 大文件处理用流式读取
let stream = InputStream(url: largeFileURL)
stream?.open()
```

**检查清单：**
- [ ] 无循环引用（使用 Instruments Leaks 检测）
- [ ] 图片缓存策略已配置
- [ ] 大列表使用 `LazyVStack` / `UICollectionView` 复用
- [ ] Notification 观察者在 deinit 中移除
- [ ] KVO 正确移除

## 渲染性能

```swift
// 1. 使用 LazyVStack/LazyHStack 替代 VStack 大量数据
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
}

// 2. 图片异步解码
Image(uiImage: image)
    .resizable()
    .aspectRatio(contentMode: .fit)
    .frame(height: 200)

// 3. EquatableView 减少不必要的重渲染
EquatableView(content: ComplexView(data: data))
    .equatable()

// 4. 使用 AnyLayout 自适应布局
let layout = sizeClass == .compact ? AnyLayout(VStackLayout()) : AnyLayout(HStackLayout())
```

**检查清单：**
- [ ] 列表使用 `LazyVStack` / `UICollectionView`
- [ ] View 实现 `Equatable` 或使用 `.equatable()`
- [ ] 无昂贵的计算属性在 `body` 中
- [ ] 动画帧率 >= 60fps

## 监控工具

```bash
# Instruments 命令行
xcrun xctrace record --template "Time Profiler" --device <device-id> --output profile.trace

# 内存调试
leaks <app-pid>

# Core Animation 帧率检查
# 模拟器：Debug → Show Render 选项 → Color Blended Layers
```
