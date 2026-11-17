# 移动端发布与 CI 工作流（Mobile Release & CI）

> 子技能各自负责"开发态"，但把代码变成商店里能装的包，是另一条独立链路：
> 签名、构建变体、商店元数据、审核避坑。本篇是跨栈的发布 playbook，
> 把一次"从 commit 到上架"的可重复流程固化下来。
>
> 本篇的构建 / 签名命令对应三个栈子技能的开发产出：
> [skills/flutter-builder/SKILL.md](../skills/flutter-builder/SKILL.md)、[skills/react-native-builder/SKILL.md](../skills/react-native-builder/SKILL.md)、[skills/ios-developer/SKILL.md](../skills/ios-developer/SKILL.md)。

## 1. 发布流水线总览

```
代码冻结 ──▶ 构建(签名) ──▶ 自动化冒烟 ──▶ 商店元数据 ──▶ 提审
   │                                                     │
   └──▶ 版本号 + changelog ──▶ 灰度(TestFlight/内部测试) ─┘
                                         │
                                    全量发布 + 监控
```

三平台入口对照：

| 平台 | 构建产物 | 内部测试通道 | 提审入口 | 签名体系 |
|------|----------|--------------|----------|----------|
| iOS | `.ipa` | TestFlight | App Store Connect | 证书 + Provisioning Profile (自动签名优先) |
| Android | `.aab` | Play 内部测试轨道 | Google Play Console | 上传密钥 + Play 签名 |
| RN/Flutter | 同上（封装原生） | 同上 | 同上 | 同上 |

**铁律**：CI 出包，**人不在本地手动出包**。本地环境差异是"我机器上能跑"的根源。

## 2. 构建与签名命令

### iOS（自动签名，Flutter/RN 同理）

```bash
# Flutter
flutter build ipa --release --export-options-plist ios/ExportOptions.plist
# 纯 RN
xcodebuild -workspace ios/App.xcworkspace -scheme App -configuration Release \
  -archivePath build/App.xcarchive archive
xcodebuild -exportArchive -archivePath build/App.xcarchive \
  -exportOptionsPlist ios/ExportOptions.plist -exportPath build/ipa

# 校验签名与 entitlements
codesign -dvvv build/App.ipa
```

### Android（Play 签名，aab 必交）

```bash
# Flutter
flutter build appbundle --release
# RN
cd android && ./gradlew bundleRelease
# 校验 aab 已用上传密钥签名
jarsigner -verify -verbose -certs build/app/outputs/bundle/release/app-release.aab
```

签名避坑：
- **绝不把上传密钥/发布证书提交进 Git**。用 CI Secret / Keystore 服务托管
- iOS 自动签名（`automaticallyManageSigning`）优先，避免 Profile 过期类审核延期
- `versionCode`/`CFBundleVersion` 单调递增，回退旧版本会卡在"版本号低于线上"

## 3. 商店元数据清单

上架前必须齐备（缺一项多数会被拒或打回）：

- [ ] 应用名称 + 副标题（≤30 字符关键词策略）
- [ ] 短描述（前 1–2 句决定转化）+ 长描述
- [ ] 截图：每尺寸至少 1–3 张（含 6.5" / 平板），含关键流程
- [ ] 预览视频（可选但显著提升转化）
- [ ] 关键词 / 标签（iOS 100 字符；Android 靠描述自然覆盖）
- [ ] 隐私政策 URL（**强制**，否则 iOS 直接拒）
- [ ] 年龄分级问卷填完
- [ ] 权限用途文案与 Info.plist / Manifest 声明一致（见 references/mobile-privacy-permissions 概念，脚本见 scripts/check_permissions.py）

## 4. 审核避坑（高频拒因）

| 拒因 | 信号 | 规避 |
|------|------|------|
| 崩溃 / 启动黑屏 | 审核设备上一打开就崩 | 内部测试先过一遍真实设备，别只模拟器 |
| 缺失隐私政策链接 | "We noticed your app is missing a privacy policy" | 上线前必填 URL，且页面可访问 |
| 权限用途不符 | 申请了定位但功能里没用到 | 最小化权限，用途文案写清场景 |
| 占位内容 / 未完成 | 有 "Lorem"/TODO/死按钮 | 提审前跑一遍全功能走查 |
| 登录后空白无游客态 | "we couldn't review the app" | 提供 demo 账号或游客可进 |
| 支付走非官方渠道 | 虚拟商品用微信/支付宝 | 数字商品必须用 Apple IAP / Play Billing |
| 侵权素材 | 用了未授权 IP | 素材来源留证 |

## 5. CI 配置要点（GitHub Actions 示例骨架）

```yaml
# .github/workflows/release.yml（骨架，非完整）
on:
  push:
    tags: ['v*']
jobs:
  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - run: flutter build ipa --release   # 或 xcodebuild
        env:
          APPLE_CERT: ${{ secrets.APPLE_CERT }}
      - uses: actions/upload-artifact@v4
        with: { name: ios-ipa, path: build/ipa/*.ipa }
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: flutter build appbundle --release
        env:
          UPLOAD_KEY: ${{ secrets.ANDROID_KEYSTORE }}
```

要点：标签触发、密钥走 Secret、产物上传 Artifact 而非直接发布、构建缓存降时。

## 6. 收口清单

- [ ] 版本号 / versionCode 已递增且大于线上
- [ ] changelog 用用户语言写"改了什么"而非技术提交
- [ ] CI 出包成功，签名校验通过（codesign / jarsigner）
- [ ] 内部测试通道（TestFlight / Play 内部轨道）已过一轮真机冒烟
- [ ] 商店元数据七项齐备（见 §3）
- [ ] 隐私政策 URL 可访问，权限文案与声明一致（脚本校验见 scripts/check_permissions.py）
- [ ] 高频拒因（§4）逐条排除，提供 demo 账号或游客态
- [ ] 灰度 → 全量 节奏已定，发布后监控崩溃率（Firebase / Sentry）

## 7. 自动化发布工具（fastlane 骨架）

手动走商店后台是出错温床。用 fastlane 固化：

```ruby
# ios/fastfile（骨架）
lane :beta do
  build_app(export_options: "ios/ExportOptions.plist")
  upload_to_testflight(skip_waiting_for_build_processing: true)
end
lane :release do
  build_app
  upload_to_app_store(submit_for_review: false)
end
```
```ruby
# android/fastfile
lane :beta do
  gradle(task: "bundle", build_type: "Release")
  upload_to_play_store(track: "internal")
end
```
要点：lane 固化步骤、凭证走 `fastlane match`（加密证书仓库）、`changelog` 从 git tag 生成。

## 8. 分阶段发布与回滚

不要一次性全量：

| 阶段 | 比例 | 观察指标 | 晋级条件 |
|------|------|----------|----------|
| 内部 / TestFlight | 100% 内部 | 崩溃率 | 0 崩溃过一轮 |
| 灰度 1% | 1% | 崩溃率、ANR、好评 | 崩溃率 <0.1% |
| 灰度 10–25% | 10–25% | 留存、转化 | 无劣化 |
| 全量 | 100% | 全指标 | 稳定 24–48h |

回滚手段：
- iOS：App Store Connect "Phased Release" 暂停；或撤审
- Android：Play Console 暂停轨道 / 回退上一版本
- 紧急热修：RN 用 CodePush / Expo OTA 推 JS 层修复，免重新过审

## 9. 发布后监控必装

- 崩溃：Sentry / Firebase Crashlytics（按版本、按设备聚合）
- 性能：Firebase Performance Monitoring（冷启动、网络时延）
- 可用性：商店评分与评论关键词告警（"崩溃""卡"出现即查）
- 指标基线：发布前记一份指标快照，发布后 diff，异常波动即回滚

## 10. 常见发布事故清单（复盘用）

- [ ] 密钥过期 / Profile 失效导致 CI 红（设到期提醒）
- [ ] versionCode 没递增，Google Play 拒收
- [ ] 隐私政策 URL 404，iOS 拒
- [ ] 灰度期间崩溃率飙升但没暂停，扩散到全量
- [ ] OTA 热修引入新 bug，且无灰度直接全量
- [ ] 商店元数据与实机权限不一致（脚本校验见 scripts/check_permissions.py）

