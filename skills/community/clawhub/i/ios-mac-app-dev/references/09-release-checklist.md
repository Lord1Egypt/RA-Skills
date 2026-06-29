# App Store 上架发布就绪清单

> 完整发布检查清单，按阶段执行。

## 🟢 阶段 1：基础检查

- [ ] 应用图标符合 Apple 规范（1024×1024 px，无透明通道）
- [ ] 所有截图与最新 UI 一致
- [ ] 应用描述（≤4000 字符）已完成
- [ ] 关键词（≤100 字符）已优化
- [ ] 宣传文本（≤170 字符）已填写
- [ ] 支持网站 URL 已填写
- [ ] 营销 URL 已填写
- [ ] 隐私政策 URL 已填写

## 🟡 阶段 2：技术检查

- [ ] **出口合规**：Info.plist 包含 `ITSAppUsesNonExemptEncryption = false`
- [ ] 签名证书有效（3rd Party Mac Developer Application / Apple Distribution）
- [ ] Provisioning Profile 已下载到本地
- [ ] 推送证书有效（若有推送功能）
- [ ] 所有隐私权限已声明并填写「使用说明」
- [ ] 没有使用废弃 API
- [ ] `CFBundleVersion` 和 `CFBundleShortVersionString` 已更新
- [ ] 在模拟器/真机上运行通过
- [ ] Archive 构建成功

### 打包检查

**Xcode Archive：**
1. Product → Archive
2. 验证签名证书 = `3rd Party Mac Developer Application`（macOS App Store）
3. 验证 Distribution Method = App Store Connect

**macOS .pkg 打包自检：**
```bash
# 验证签名
codesign -dvvv /path/to/YourApp.app  # 应显示 TeamIdentifier

# 验证 entitlements
codesign -d --entitlements - /path/to/YourApp.app
# 必须包含: application-identifier, team-identifier, app-sandbox

# 验证 embedded.provisionprofile
ls /path/to/YourApp.app/Contents/embedded.provisionprofile
```

**常见错误：**
| 错误码 | 原因 | 修复 |
|--------|------|------|
| 90886 | 签名缺少 application-identifier | 合并 profile 中的 entitlements 后再签名 |
| 409 | 缺少 app-sandbox | 合并 entitlements 时确保 app-sandbox=true |
| 90889 | 缺少 provisioning profile | 验证 embedded.provisionprofile 存在 |

## 🔵 阶段 3：多语言检查

- [ ] 支持所有目标语言的本地化
- [ ] 每个语言的字符串完整翻译
- [ ] RTL 语言布局正确
- [ ] 日期/货币格式按地区适配
- [ ] 文化敏感性检查通过

## 🟣 阶段 4：UI/UX 检查

- [ ] 深色模式适配完成（见 `references/04-dark-mode.md`）
- [ ] Dynamic Type 支持（`.dynamicTypeSize(...DynamicTypeSize.xxxLarge)`）
- [ ] VoiceOver 支持完成（见 `references/07-accessibility.md`）
- [ ] 反 AI 流行模式检查通过（见 `references/02-ui-design.md`）
- [ ] iPad 横竖屏布局正确
- [ ] macOS 适配（菜单栏、窗口大小、Toolbar）

## 🔴 阶段 5：合规检查

- [ ] AI 功能符合条款 3.3.11 要求
- [ ] 未成年保护机制就绪（若面向儿童）
- [ ] 隐私标签和数据披露完成（PrivacyInfo.xcprivacy）
- [ ] 年龄分级正确设置
- [ ] 4.3 条款合规（应用差异化充分）

## ⚪ 阶段 6：发布策略

- [ ] 分阶段发布已配置（7 天逐步放量）
- [ ] App Analytics 已配置
- [ ] TestFlight Beta 测试已完成
- [ ] 崩溃监控已接入（Firebase Crashlytics / Sentry）
- [ ] 营销/发布文案准备就绪

## 一键打包脚本 (macOS .pkg)

```bash
# 用于 macOS App Store 发布的自动打包
# 确保以下路径和配置正确
VERSION="1.0.0"
APP_PATH="/path/to/YourApp.app"
PROVISION_PROFILE="/path/to/AppStore.provisionprofile"
SIGN_IDENTITY="3rd Party Mac Developer Application: Your Name (TEAMID)"
INSTALLER_IDENTITY="3rd Party Mac Developer Installer: Your Name (TEAMID)"

# 详见本 skill 的 TOOLS.md（若有自定义打包脚本）或 Xcode Archive 文档
```
