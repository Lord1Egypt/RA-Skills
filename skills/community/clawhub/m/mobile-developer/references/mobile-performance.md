# 移动端性能与电池优化（Mobile Performance & Battery）

> 子技能讲了"怎么布局/怎么写组件"，但性能是跨栈的横向课题，且直接决定应用商店
> 评分与留存。本篇给一套可执行的性能与电池优化 playbook：先量化再优化，附命令、
> 阈值与清单。任何栈（Flutter/RN/iOS）都通用。

## 1. 性能基线指标与阈值

| 指标 | 优秀 | 可接受 | 危险（必须修） | 测量方式 |
|------|------|--------|----------------|----------|
| 冷启动（iOS） | <400ms | <800ms | >2s | Instruments App Launch |
| 冷启动（Android） | <500ms | <1s | >2.5s | `adb shell am start -W` |
| 列表滚动帧率 | 稳定 60fps | ≥55fps | <50fps 掉帧 | Perf Monitor / Profile GPU |
| 内存峰值 | <150MB | <300MB | >512MB（OOM 风险） | Xcode Memory Graph |
| 包体积（iOS IPA） | <50MB | <100MB | >150MB | App Store Connect |
| 主线程阻塞 | <16ms/帧 | <50ms | >100ms | Trace / Systrace |
| 单帧电量 | 看趋势 | 平稳 | 滚动时骤升 | Energy Log |

**黄金法则**：先量后改。没有基线的优化是玄学。每次改动后重新量，确认数字下降。

## 2. 各栈性能命令清单

### Flutter

```bash
# 发布模式下测帧率（关键：必须 --release，debug 永远慢）
flutter run --release
flutter build apk --analyze-size          # 包体积拆解
flutter analyze                            # 静态检查（含 const 缺失提示）
# DevTools 打开：flutter pub global activate devtools && devtools
# 查 rebuild 次数：DevTools → Performance → 勾选 "Track widget rebuilds"
```

Flutter 性能要点：
- 列表用 `ListView.builder` + `const` 构造函数，避免整列表重建
- 大图用 `cached_network_image` 并指定 `memCacheWidth` 降采样
- 避免 `Opacity` 包裹大子树（触发离屏渲染），改用 `Visibility` 或 `AnimatedOpacity` 仅对小元素
- `ShaderMask` / `Clip` 代价高，能用 `BoxDecoration` 解决的别用 clip

### React Native

```bash
# 包体积
npx react-native bundle --platform android --dev false --entry-file index.js \
  --bundle-output /tmp/main.jsbundle --sourcemap-output /tmp/main.jsbundle.map
# 启动 Flipper / Hermes 采样（Hermes 必开，显著降冷启动与内存）
```

RN 性能要点：
- 长列表**必须**用 `FlatList`，并设 `getItemLayout`（已知高度时跳过测量）、
  `windowSize`（默认 21 太大，调到 5–7）、`initialNumToRender`（首屏够用即可）
- 图片用 `react-native-fast-image` 做缓存与降采样
- 开 Hermes（`enableHermes: true`）——Bytecode 预编译，冷启动降 30%+
- JS 线程卡顿定位：`__DEV__` 下开会看到桥调用栈；用 `InteractionManager.runAfterInteractions` 延后非紧急渲染

### iOS (SwiftUI)

```bash
#  Instruments 命令行采样卡顿
xcrun xctrace record --template "Time Profiler" --launch -- /path/to/app
# 滚动掉帧定位：Instruments → Animation Hitches
```

SwiftUI 要点：
- 列表用 `LazyVStack`/`LazyVGrid`（见 ios-developer），**不要**在 `ScrollView` 里放非 lazy 栈
- 用 `.id()` 触发刷新要谨慎，会重建整个子树
- `@State`/ `@ObservedObject` 粒度过粗导致全视图重绘；拆小 `View` 让 SwiftUI 做差异比对
- 图片解码放后台：`UIImage(contentsOfFile:)` + 预解码，避免主线程解码大图

## 3. 电池友好的硬性规则

1. **暗色模式适配**：OLED 上纯黑像素不耗电，提供并默认跟随 `prefers-color-scheme`
2. **减少轮询**：用 `Push` / 长连接替代 30s 轮询；定位用 `significant-location-change` 替代持续 GPS
3. **降频动画**：后台或低电量时停掉非必要动画（见 mobile-design-system）
4. **网络合并**：批量上报，避免每秒小请求；用 `URLSession` 后台传输大文件
5. **避免唤醒锁**：`WakeLock` / `beginBackgroundTask` 必须配对 `endBackgroundTask`，泄漏会持续耗电
6. **定位精度按需降级**：导航时用 `best`，仅记录轨迹时用 `reduced`

电池验证（Android）：
```bash
adb shell dumpsys batterystats --reset          # 重置基线
# 跑一轮典型用例
adb shell dumpsys batterystats > /tmp/battery.txt
# 查 UID 的 wakeup/mobile 次数，异常高即定位元凶
```

## 4. 典型坑与规避

- **坑：只在 debug 模式测性能**。debug 有 JIT、断言、检查，数字毫无意义。
  *规避*：所有性能结论必须来自 `--release` / Hermes / 真机。
- **坑：列表首屏一次性渲染上千项**导致白屏 + 卡死。
  *规避*：`FlatList`/`ListView.builder` 虚拟化；首屏 `initialNumToRender` 限制。
- **坑：把图片原图塞进内存**。一张 4000px 图占 ~64MB。
  *规避*：解码时 `memCacheWidth` / `inSampleSize` 降采样到显示尺寸。
- **坑：过度使用 `Opacity`/`blur` 触发离屏渲染**。滚动掉帧。
  *规避*：仅对小元素用；大背景模糊用缓存图。
- **坑：后台任务不收尾**。电池一夜掉光，被系统杀进程。
  *规避*：`endBackgroundTask` 配对；后台定位用完即停。

## 5. 优化收口清单

- [ ] 已用 --release / Hermes / 真机测得**基线**数字（启动/帧率/内存/体积）
- [ ] 列表全部虚拟化（FlatList / ListView.builder / LazyVStack），无全量渲染
- [ ] 图片做了缓存 + 降采样，无原图进内存
- [ ] 主线程无 >16ms 阻塞（耗时操作进 isolate / 异步 / 后台）
- [ ] 已开 Hermes（RN）/ 已用 const（Flutter）/ 已拆小 View（SwiftUI）
- [ ] 电池：无 30s 轮询、无定位泄漏、暗色模式已适配
- [ ] 包体积在阈值内，超标的依赖已做拆分或动态下发
- [ ] 改动后重测，数字确认下降（不是"感觉快了"）
- [ ] 详细命令见 [skills/flutter-builder/SKILL.md](../skills/flutter-builder/SKILL.md)、[skills/react-native-builder/SKILL.md](../skills/react-native-builder/SKILL.md)、[skills/ios-developer/SKILL.md](../skills/ios-developer/SKILL.md)、[skills/mobile-design-system/SKILL.md](../skills/mobile-design-system/SKILL.md)（电池友好见 §3）

## 6. 内存分析实操（排查 OOM）

OOM 是最隐蔽的崩溃——只在低端机、长会话后出现。定位手法：

**Android（LeakCanary + MAT）**：
```bash
# 接 LeakCanary，复现后看 heap dump，定位 retained 对象链
adb shell am dumpheap <pid> /data/local/tmp/h.hprof
# 拉到本地用 Android Studio Profiler / MAT 打开，看 Dominator Tree
```
常见元凶：未反注册的监听器、`static` 持有 Activity、大图未回收、`RxJava` 订阅未 dispose。

**iOS（Memory Graph + Instruments）**：
```bash
# Xcode → Debug Memory Graph，看循环引用（两个对象互指无根）
# 或命令行抓堆：
heap <pid> -addresses all | head
```
常见元凶：闭包捕获 `self` 形成循环（`[weak self]`）、`NotificationCenter` 未移除、
`Timer` 未 invalidate、`UIImage` 大图缓存未设上限。

**Flutter**：用 `dart:developer` 的 `Service.getMemoryUsage()` 或 DevTools Memory 页，
看 Dart 堆与 GPU 内存；`Image` 缓存上限用 `painting.imageCache.maximumSizeBytes` 调。

## 7. 帧率掉帧定位（Hitch 分析）

掉帧不是"动画慢"，是单帧超过 16.6ms（60fps）或 8.3ms（120fps）：
- **主线程忙**：把耗时逻辑移到 `compute()`（Flutter）/ Worker（Web）/ 后台线程（原生）
- **布局爆炸**：避免深层嵌套 `Column`/`Row` 在滚动中重算；Flutter 用 `RepaintBoundary` 隔离
- **过度绘制**：Android 开发者选项开 "Show overdraw"，红色区域即重复绘制，合并背景
- **大列表**：见 §2 虚拟化规则，非懒列表是滚动掉帧第一元凶

## 8. 包体积拆解与瘦身

```bash
# Flutter
flutter build apk --analyze-size --target-platform android-arm64
# 打开 size 报告，定位大依赖（字体 / 图片 / 大库）
```
瘦身手段（按性价比）：
1. 删无用国际化（`synthetic-package` 裁剪）、只留用的 locale
2. 字体子集化（只打用到的字形，`fontTools` 子集）
3. 大图转 WebP / AVIF，矢量图优先
4. 拆 `dynamic feature`（Android）按需下发非首屏模块
5. 依赖审计：一个 `lodash` 全量引入 vs 按需，差出百 KB

