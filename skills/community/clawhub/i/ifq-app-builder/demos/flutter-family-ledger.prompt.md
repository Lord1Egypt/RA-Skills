---
templateId: T-flutter-cross
ifqMode: A-07
stack: flutter-3 + dart-3 + riverpod
artifact: ipa+aab
locale: ['zh-CN', 'en']
---

# flutter-family-ledger — A-07 / T-flutter-cross

Mode A-07, template T-flutter-cross. A cross-platform family ledger prompt bundle.

## S1 — WHO + WHAT

家庭共同记账的两位成员记录日常消费、收入、预算和月末结余。输入是手动账目、分类、金额、日期、备注与可选照片；输出是月度预算进度、分类统计、可导出的 `.csv` 和共享同步状态。

## S2 — WHERE

iOS 17+ 与 Android 10+，一份 Flutter 代码库，离线优先，网络恢复后加密同步。Distribution: TestFlight 与 Google Play internal testing。Locales: zh-CN 与 en。

## S3 — HOW SUCCESS LOOKS

新建账本、添加两笔支出、一笔收入后首页余额立即更新；离线新增记录会进入待同步队列；产物为 `family-ledger.ipa` 与 `family-ledger.aab`；非目标：不做股票投资、不做银行 OpenAPI、不做多人社交动态。

## Acceptance (binary, yes/no observable)

- [ ] `flutter test` 通过核心账本计算与离线队列测试。
- [ ] iOS 构建生成 `family-ledger.ipa`，Android 构建生成 `family-ledger.aab`。
- [ ] 飞行模式下能新增记录，恢复网络后同步状态从 pending 变为 synced。
- [ ] 月预算进度与分类统计在样例数据下计算正确。
- [ ] zh-CN 与 en 均存在，金额、日期和空状态文案按 locale 显示。

## Scaffold (run order)

1. Scaffold Flutter 3 app with Riverpod and go_router.
2. Add local database layer and ledger domain tests.
3. Add encrypted sync abstraction and pending queue states.
4. Add `lib/l10n/intl_zh_CN.arb` and `lib/l10n/intl_en.arb`.
5. Build home, add-entry, budget, stats, sync status, settings screens.
6. Run `flutter test`.
7. Build `flutter build ipa` and `flutter build appbundle --release` when SDKs are available.

## Packaging

- iOS: `flutter build ipa` outputs `build/ios/ipa/family-ledger.ipa`.
- Android: `flutter build appbundle --release` outputs `build/app/outputs/bundle/release/family-ledger.aab`.

## Security baseline

- Sync tokens are stored only in Keychain/Keystore via a secure storage plugin.
- Local ledger cache is encrypted at rest.
- Network sync uses HTTPS only and validates response schemas before applying mutations.
- No financial credentials, bank passwords, or card numbers are collected.
- Release builds enable obfuscation and split debug symbols.

## IFQ ambient

Use IFQ warm paper for overview surfaces, restrained rust for destructive confirmation, and mono field-notes for sync ledger captions. Keep the family ledger brand user-owned; IFQ appears only as colophon.

## Agent execution contract

- Do not install Flutter or mobile SDKs unless the user explicitly enters Tier 1.
- If SDKs are missing, deliver the verified bundle and list exact next commands without claiming build success.
- Never ask for App Store or Play Console credentials during Tier 0.

— shaped with ifq.ai/app-builder · A-07 · T-flutter-cross
