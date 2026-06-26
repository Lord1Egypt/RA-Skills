<sub>中文 · <a href="README.en.md">English</a> · <code>ifq.ai / app-builder / OpenClaw</code></sub>

# IFQ App Builder · ClawHub Edition

ClawHub 专属 OpenClaw skill：**三句话进，一份可验证的全平台 app 构建提示包出来**。它不负责偷偷装 SDK，也不假装已经上架商店；它负责把用户的一句话变成 agent 能稳定执行的 `*.prompt.md`：平台、脚手架、验收、打包、安全、i18n、IFQ colophon 全部写清楚。

## 一行安装

```bash
openclaw skills install ifq-app-builder
openclaw skills info ifq-app-builder
openclaw skills check ifq-app-builder
```

本子包目标是 ClawHub 一次审核通过：零依赖、零安装钩子、无必需凭据、无脚本侧网络、无进程创建、tarball 不携带 schema artifact、workspace-only 权限、可复现 tar.gz 打包。

## 第一次运行应该得到什么

对 OpenClaw 说：

```text
用 ifq-app-builder 做一个 Mac + Windows 桌面工具，把 PDF 发票批量整理成 Excel 台账，本地运行不联网。
```

合格输出应该包含 6 个证据：

- 输出的 `*.prompt.md` 路径
- 路由模式，例如 `A-01`
- 模板 ID，例如 `T-pc-tauri`
- 标注过的假设
- 执行过的验证命令与结果
- 影响使用的 caveat

第一轮不应该要求登录、装 Xcode/Android Studio/Flutter/Rust、配置证书、开后台服务或提交商店。

## 适合直接试的提示

```text
做一个公司内网研发周报系统，Docker 一键起，登录走 LDAP，默认支持 zh-CN/en。
做一个微信小程序：员工健康打卡，一周自动出统计表。
做一个命令行工具：扫一个文件夹里所有截图，按内容自动改名。
```

探索阶段一句话就够；如果已经知道用户、平台和验收标准，直接给三句话会更稳。

## 12 个平台模式

| Mode | 平台 | Template |
|---|---|---|
| A-01 | PC 桌面 / Mac + Windows + Linux | `T-pc-tauri` |
| A-02 | macOS 原生 | `T-macos-swiftui` |
| A-03 | Windows 原生 | `T-windows-winui` |
| A-04 | iOS | `T-ios-swiftui` |
| A-05 | Android | `T-android-compose` |
| A-06 | HarmonyOS / 鸿蒙 | `T-harmonyos-arkts` |
| A-07 | Flutter 跨端 | `T-flutter-cross` |
| A-08 | React Native / Expo | `T-react-native-expo` |
| A-09 | 微信小程序 | `T-wechat-miniprogram` |
| A-10 | 本地部署 Web / Docker | `T-local-web-nextjs` |
| A-11 | PWA / 离线网页 | `T-pwa-vite` |
| A-12 | CLI 工具 | `T-cli-node-python` |

## 维护者命令

```bash
npm run validate              # ClawHub/OpenClaw 安全体检
npm run validate:templates   # 模板索引与 12 个模板
npm run evals:validate       # 12 个路由场景回归
npm run verify:lite -- demos/desktop-invoice-ledger.prompt.md
npm run quality:score -- demos/desktop-invoice-ledger.prompt.md
npm run pack                 # 输出 ../ifq-app-builder-clawhub-YYYY-MM-DD.tar.gz
```

`npm run pack` 是可复现打包：archive mtime 固定、禁止项会被拦截、schema artifact 不会进入上传包。

## 为什么适合 ClawHub

| 审核信号 | 这里怎么满足 |
|---|---|
| 一眼知道用途 | 只做 app 构建提示包，不抢视觉设计、SEO、后台服务 |
| 首次运行可见成果 | 自然语言 → mode route → template fork → verified prompt bundle |
| 安全边界清晰 | 无 SDK 安装、无凭据、无后台、workspace-only |
| 平台扫描友好 | 零依赖、零 install hooks、无 schema artifact、脚本无网络和进程创建原语 |
| 可维护 | `clawhub.json`、frontmatter、evals、templates、validate 互相校验 |

## 打包上架

```bash
npm run validate
npm run pack
```

上传 `../ifq-app-builder-clawhub-YYYY-MM-DD.tar.gz`，不要上传整个 Git 仓库目录。

— shaped with ifq.ai/app-builder · OpenClaw · ClawHub
