# Quickstart

Three one-liners.

## 1. "Mac + Win 桌面工具，把 PDF 发票变成 Excel"

```
用 $ifq-app-builder 把这句话变成构建包，平台默认 Mac + Win，本地运行不联网。
```

Expected: agent routes A-01, forks `pc-tauri.prompt.md`, writes `pdf-invoice-ledger.prompt.md`, runs `verify:lite`, reports path.

## 2. "iOS + Android 一份代码的家庭账本"

```
用 $ifq-app-builder 做一个 iOS + Android 家庭账本，跨端单代码库，端到端加密同步。
```

Expected: A-07 Flutter, `flutter-cross.prompt.md` forked as `family-ledger.prompt.md`.

## 3. "公司内网部署的研发周报系统"

```
用 $ifq-app-builder 做一个公司内网周报系统，Docker 一键起，登录走 LDAP。
```

Expected: A-10, `local-web-nextjs.prompt.md` forked as `eng-weekly.prompt.md`.

## What you do next

Hand the bundle to the same agent (or a different one) with:

> "按这个 prompt 包把 app 真正搭出来，跑通验收里的每一条。"

The agent will run the scaffold steps, build, and report.
