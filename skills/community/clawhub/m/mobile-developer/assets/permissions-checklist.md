# 移动端权限与隐私检查清单（Permissions & Privacy Checklist）

> 上线前逐条过。权限是商店审核高频拒因，也是用户信任的第一道门槛。
> 可配合 [scripts/check_permissions.py](../scripts/check_permissions.py) 自动校验声明文件（见下方「脚本自检」）。

## 一、通用原则

- [ ] **最小化**：只申请功能真正用到的权限，不用"将来可能用"的权限
- [ ] **用途透明**：每个权限在首次触发时，UI 内说明为什么需要（不只是系统弹窗文案）
- [ ] **被拒不卡死**：权限被拒后提供引导去设置的入口，不静默失败
- [ ] **隐私政策**：线上可访问的隐私政策 URL 已填（iOS 强制、Android 强烈建议）
- [ ] **数据最小化**：敏感数据本地优先，上传须加密、须告知用户

## 二、Android（Manifest）

- [ ] 所有 `<activity>`/`<service>`/`<receiver>` 显式 `android:exported`（targetSdk≥31 必须）
- [ ] 非必要组件 `exported="false"`，避免被其它应用拉起
- [ ] 危险权限（相机/定位/通讯录/麦克风/存储）确属必要，否则移除
- [ ] `READ_SMS`/`RECEIVE_SMS` 等敏感权限原则上不申请（除非是短信类应用）
- [ ] 后台定位用 `foregroundServiceType="location"`，前台可见通知
- [ ] 运行时权限在 `ContextCompat.checkSelfPermission` 后再请求，不假设已授权

## 三、iOS（Info.plist）

- [ ] 所有用到的 `NS*UsageDescription` 键已声明且文案非空、具体
- [ ] 文案写清「用途 + 用户收益」，避免 "We need access" 这类空话
- [ ] 用到相机/相册/定位/麦克风/通讯录/健康/运动每一项都对应声明
- [ ] 定位若仅前台用，用 `NSLocationWhenInUseUsageDescription`，不用 Always
- [ ] 相册若只写不读，用 `NSPhotoLibraryAddUsageDescription` 而非读权限
- [ ] 开启 `NSAppTransportSecurity` 例外前确认确有合规理由

## 四、脚本自检（确定性校验）

```bash
# 校验两份声明文件 + 规范，期望输出 0 error
python3 scripts/check_permissions.py \
  --android assets/android-manifest-template.xml \
  --ios assets/ios-info-plist-template.plist \
  --spec assets/permissions-spec.json
```

- [ ] 自检 0 error（模板已内置为 0 error 范例）
- [ ] 把 [assets/android-manifest-template.xml](android-manifest-template.xml) 换成你项目的 `AndroidManifest.xml` 重跑
- [ ] 把 [assets/ios-info-plist-template.plist](ios-info-plist-template.plist) 换成你项目的 `Info.plist` 重跑
- [ ] 按项目真实能力调整 [assets/permissions-spec.json](permissions-spec.json) 的 allow/deny/required 清单

## 五、发布前回顾

- [ ] 商店页权限说明与实机声明一致（见 references/mobile-release.md §3）
- [ ] 首启权限请求时序在真机验证，不卡流程（见 references/mobile-qa-devices.md §3）
- [ ] 隐私政策覆盖所申请的全部权限与数据用途
