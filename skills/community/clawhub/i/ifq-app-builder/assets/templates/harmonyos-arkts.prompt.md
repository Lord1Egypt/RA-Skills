---
templateId: T-harmonyos-arkts
ifqMode: A-06
stack: "ArkTS + ArkUI (Stage model) + DevEco Studio + API 12"
artifact: ".hap / .app (HarmonyOS Next)"
---

# T-harmonyos-arkts · HarmonyOS Next · ifq-app-builder

Fork, fill, verify, hand off.

## S1 — WHO + WHAT
<replace: who uses this 鸿蒙 app, what they do, what data flows in/out>

## S2 — WHERE
- Platform: HarmonyOS Next (API 12+), Stage model, phone + tablet form factors
- Stack (pinned): ArkTS, ArkUI declarative paradigm, DevEco Studio 5+, hvigor build system
- Runtime: <replace: 100% on-device · or 走华为帐号 · or 自有后端>
- Distribution: <replace: 华为应用市场 · 内测分发 · 企业内部>

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements describing a successful first run on a Mate 60 / P70 class device>

## Acceptance (binary, yes/no observable)
- [ ] First launch under 1.5s on a Mate 60 class device
- [ ] Primary workflow from S1 succeeds with <replace: real sample input>
- [ ] Adaptive layout: phone vertical, tablet horizontal, foldable expanded — all readable
- [ ] All strings in `entry/src/main/resources/{base,zh_CN}/element/string.json`
- [ ] No `appAttemptCrash` events during the happy path
- [ ] `hvigorw assembleHap --mode module -p product=default` succeeds

## Scaffold (run order)
1. Open DevEco Studio 5+ → New Project → `Application` → Stage model → API 12
2. Project name `<Slug>`, bundle name `ai.ifq.<slug>`
3. Create `common/src/main/ets/theme/IFQTheme.ets` exporting `@Provide` IFQ tokens
4. Pages under `entry/src/main/ets/pages/`; use `@Entry @Component struct`
5. State: `@State`, `@Prop`, `@Link`, `@Provide` / `@Consume`
6. Persistence: `@ohos.data.preferences` for small state; `@ohos.data.relationalStore` for tables
7. Network: `@ohos.net.http`; declare `ohos.permission.INTERNET` in `module.json5` only if S2 requires it

## Packaging
- Debug: `hvigorw assembleHap --mode module`
- Release: configure `signingConfigs` in `build-profile.json5`; output `.hap` under `entry/build/default/outputs/default/`
- App Gallery: bundle as `.app` for submission, signed with App Gallery Connect cert
- ARM64 only by default; add ARM32 split only if user targets older devices

## Security baseline
- App sandbox + permissions enforced via `module.json5`
- `crypto-js` or `@ohos.security.cert` for credentials; never plain `Preferences`
- HTTPS only via `@ohos.net.http`; no `http://` literals
- File access: use `context.filesDir`, never absolute paths

## IFQ ambient
- `theme/IFQTheme.ets` (paper / rust / spark / quiet / mono colors + font sizes)
- About page: a single `Text('— shaped with ifq.ai/app-builder')`

## Agent execution contract
- Print the three sentences back first
- If `hvigorw` / DevEco is missing, label packaging `(blocked: install DevEco Studio 5+)` and stop
- ArkTS is **not** TypeScript; do not paste DOM types or browser APIs

— shaped with ifq.ai/app-builder · A-06 · T-harmonyos-arkts
