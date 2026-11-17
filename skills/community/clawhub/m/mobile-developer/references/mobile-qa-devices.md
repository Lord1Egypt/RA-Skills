# 设备矩阵与真机测试（Mobile QA & Device Matrix）

> 模拟器通过了 ≠ 真机没问题。移动端的碎片化为质量埋雷：屏幕尺寸、系统版本、
> 芯片（含新旧架构）、权限弹窗时序都不同。本篇给一套设备覆盖决策 + 自动化测试
> 命令 + 真机必查清单，是子技能"能跑"之外必须补的 QA 方法论。

## 1. 设备覆盖决策树

```
Q1 目标市场在哪？
├─ 欧美 → iOS 权重高，但 Android 碎片大（覆盖 2019+ 主流机）
└─ 东南亚 / 印度 / 拉美 → Android 绝对主力，低端机必须测

Q2 最低支持系统版本？
├─ iOS：min 建议 iOS 15+（2024 起），旧版本份额<5% 可放
└─ Android：minSdk 建议 21（5.0）覆盖 98%+，低端机多在 API 21–24

Q3 必测设备集合（最小充分集）
├─ iOS：最新旗舰(17) + 一款旧芯片(A12/A13) + 一款小屏(SE)
└─ Android：旗舰(骁龙8系) + 一款低端(联发科/4GB内存) + 一款折叠/平板
```

**覆盖原则**：每平台至少 3 档（新旗舰 / 旧芯片 / 极端尺寸），比"覆盖面"更重要的是
覆盖**性能分位**与**系统分位**的两端，中间档出问题概率低。

## 2. 自动化测试命令（按栈）

### Flutter

```bash
flutter test                                 # 单元 + widget 测试
flutter test integration_test/app_test.dart # 集成（真机/E2E）
flutter drive --target=test_driver/app.dart # 旧 drive 方案
# 多设备并行（需要多台接入）
flutter test integration_test/ -d <deviceId1> -d <deviceId2>
```

### React Native

```bash
# Jest 单元
npm test
# Detox E2E（真机，需 build 出 test 包）
detox build --configuration ios.sim.debug
detox test --configuration ios.sim.debug
# Maestro 跨栈 UI 流（推荐，YAML 描述）
maestro test flows/login.yaml
```

### iOS / 原生

```bash
# XCTest
xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'
# UI 录制转 XCTest UI 测试
```

### 通用 UI 流（Maestro 跨 Flutter/RN/原生）

```yaml
# flows/smoke.yaml
appId: com.example.app
---
- launchApp
- tapOn: "登录"
- assertVisible: "欢迎"
```

各栈测试命令对应的子技能：[skills/flutter-builder/SKILL.md](../skills/flutter-builder/SKILL.md)、[skills/react-native-builder/SKILL.md](../skills/react-native-builder/SKILL.md)、[skills/ios-developer/SKILL.md](../skills/ios-developer/SKILL.md)；触控 / 无障碍真机核查另见 [skills/mobile-design-system/SKILL.md](../skills/mobile-design-system/SKILL.md)。

## 3. 真机必查清单（模拟器测不出）

| 检查项 | 为什么模拟器测不出 | 验证方式 |
|--------|--------------------|----------|
| 权限弹窗时序 | 模拟器常默认授权 | 真机首次启动逐个点权限，确认不卡流程 |
| 弱网 / 断网 | 模拟器网络太好 | 开飞行模式 + 开发者网络节流，看重试/降级 |
| 内存压力下被杀 | 模拟器内存大 | 低端机开多个 App 再回来，确认状态恢复 |
| 折叠 / 旋转 | 模拟器尺寸固定 | 真机旋转 + 折叠屏开合，看布局不崩 |
| 通知 / 深链 | 模拟器受限 | 点推送 / 通用链接拉起指定页 |
| 触控热区 | 鼠标点击精准 | 手指粗触点，确认 44pt 目标够大（见 skills/mobile-design-system） |
| 冷启动白屏 | 模拟器已热 | 清后台后首次打开，看首屏时机 |

## 4. 典型坑与规避

- **坑：只测主力机型，低端机首屏 8 秒被弃**。*规避*：低端机纳入必测，
  用 [references/mobile-performance.md](mobile-performance.md) 的降采样/虚拟化手段压首屏。
- **坑：权限被拒后功能永久不可用**。*规避*：所有权限请求配"被拒引导"，
  跳设置页的重试用文案；不静默失败。
- **坑：横竖屏状态丢失**。*规避*：ViewModel/State 持久化 + `onSaveInstanceState`，
  旋转后恢复输入与滚动位置。
- **坑：深浅色切换后图片/对比度失效**。*规避*：用语义色（systemBackground/
  onSurface）而非硬编码，切主题后重测可读性。
- **坑：E2E 只在 CI 模拟器过，真机 UI 时序不同失败**。*规避*：关键流至少 1 台真机跑 E2E。

## 5. 收口清单

- [ ] 已用 §1 决策树定出最小设备矩阵（每平台 ≥3 档）
- [ ] 单元/widget 测试通过（flutter test / npm test / XCTest）
- [ ] 至少 1 条关键 E2E 流（Detox / Maestro / integration_test）通过
- [ ] 真机权限弹窗时序验证，被拒有引导
- [ ] 弱网/断网降级路径验证
- [ ] 旋转/折叠/深链/通知拉起验证
- [ ] 低端机冷启动与内存压测达标（指标见 references/mobile-performance.md）
- [ ] 深浅色主题切后可读性与对比度复核
- [ ] 崩溃监控（Sentry/Firebase）已接，发布后看崩溃率曲线

## 6. 设备云与本地矩阵的成本权衡

| 方案 | 覆盖 | 成本 | 适合 |
|------|------|------|------|
| 本地 3–5 台真机 | 中（自有矩阵） | 买机 + 维护 | 独立开发者 / 小团队 |
| Firebase Test Lab / AWS Device Farm | 极大（数百款） | 按分钟计费 | 发布前全量兼容性扫 |
| BrowserStack / Sauce Labs | 大（含 iOS 真机） | 订阅 | 跨端 E2E 常态化 |
| 模拟器 + 少量真机 | 低 | 几乎 0 | 仅原型期 |

**务实组合**：日常用模拟器 + 1 台 iOS + 1 台 Android 低端机快速迭代；
发布前跑一次 Device Farm 的兼容矩阵（重点查崩溃与首屏）。

## 7. 无障碍 QA（常被漏掉）

移动端无障碍是合规与体验双底线，真机才测得准：

- **动态字体**：iOS 开 "更大字体"、Android 开 "字体大小最大"，确认布局不溢出/不截断
- **VoiceOver / TalkBack**：开启后走核心流程，确认焦点顺序合理、标签非空
- **对比度**：正文 ≥4.5:1，大文本 ≥3:1（用对比度工具核）
- **触控目标**：所有可点元素 ≥44×44pt（iOS）/ 48×48dp（Android），见 skills/mobile-design-system
- **减少动态**：开启 "减少动态效果" 后，动画降级但不影响功能（见 animation 类技能）

## 8. 一条完整 Maestro 冒烟流（示例）

```yaml
# flows/release-smoke.yaml
appId: com.example.app
---
- launchApp
- assertVisible: "欢迎"
- tapOn: "登录"
- inputText: "test@example.com"
- inputText: "password123"
- tapOn: "提交"
- assertVisible: "首页"
- doubleTapOn: "刷新"
- assertVisible: "最新数据"
- stopApp
- launchApp
- assertVisible: "首页"        # 验证状态恢复，不死在登录页
```
这条流同时覆盖：启动、登录、核心操作、冷重启状态恢复——发布前必跑。

## 9. 质量门禁收口（CI 里固化）

- [ ] `flutter test` / `npm test` / XCTest 全绿才允许打 release 包
- [ ] 至少 1 条 Maestro/Detox E2E 在合并前跑（可用模拟器，省成本）
- [ ] 真机冒烟（§8 流程）在提审前跑一次
- [ ] 弱网/断网/旋转/权限被拒 四类边界用例有对应测试或手动清单
- [ ] 无障碍四项（§7）在真机过一遍
- [ ] 发布后崩溃率看板有基线对比，异常即回滚（见 references/mobile-release.md §9）

## 10. 碎片化专项（最易漏的兼容性点）

| 维度 | 差异点 | 必查 |
|------|--------|------|
| 屏幕 | 刘海 / 灵动岛 / 挖孔 / 瀑布屏 | 安全区 `SafeArea` / `WindowInsets` 适配，内容不被遮挡 |
| 字体 | 系统默认字号各厂商不同 | 动态字体开到最大不溢出（§7） |
| 时区/ locale | 12/24 小时、日期格式、RTL | 阿拉伯语 RTL 布局不镜像错乱 |
| 键盘 | 第三方输入法高度不一 | 输入框不被键盘顶出屏幕（监听键盘高度） |
| 深色模式 | 各厂商色值解释不同 | 语义色而非硬编码，切主题后重测 |
| 权限默认 | 厂商预授权策略不同 | 真机点权限，不假设已授权 |
| 后台限制 | 国产 ROM 杀进程更激进 | 小米/华为/OPPO 后台保活策略验证 |

**安全区适配**（两端通用）：
- iOS：`SafeAreaView` / `safeAreaInsets` 包住全屏内容
- Android：`WindowCompat.setDecorFitsSystemWindows` + `WindowInsetsCompat` 处理刘海
- Flutter：`SafeArea` widget 包裹 `Scaffold` body
- RN：`react-native-safe-area-context` 的 `SafeAreaView`

漏掉安全区 = 刘海挡住顶部按钮，是商店差评高频来源，必须真机逐项确认。


