---
templateId: T-pc-tauri
ifqMode: A-01
stack: tauri-2 + react + vite
artifact: dmg+exe+AppImage
locale: ['zh-CN', 'en']
---

# desktop-invoice-ledger — A-01 / T-pc-tauri

Mode A-01, template T-pc-tauri. A local desktop prompt bundle for a PDF invoice ledger tool.

## S1 — WHO + WHAT

财务同事每天把本地文件夹里的 PDF 发票整理成一份 Excel 台账。输入是一组本地 PDF，输出是一份 `.xlsx`，列含发票号、开票方、税额、合计金额、文件名与不确定标记。

## S2 — WHERE

macOS 13+ 与 Windows 10/11 桌面，本地运行，不联网，不上传文件。Distribution: 公司内网下载签名后的 `.dmg` 与 `.exe`。Locales: zh-CN 与 en。

## S3 — HOW SUCCESS LOOKS

拖入包含 20 张样例发票的文件夹后 30 秒内生成 Excel；无法确定的字段在 Excel 中标黄；产物为 `invoice-ledger.dmg` 与 `invoice-ledger-setup.exe`；非目标：不做手写 OCR、不做云同步、不做税局联网验真。

## Acceptance (binary, yes/no observable)

- [ ] macOS 构建生成 `invoice-ledger.dmg`，文件存在且签名检查通过。
- [ ] Windows 构建生成 `invoice-ledger-setup.exe`，文件存在且签名检查通过。
- [ ] 20 张样例 PDF 输入后 30 秒内输出 `.xlsx`，并包含发票号、开票方、税额、合计金额、文件名列。
- [ ] 关闭网络后主流程仍可完成，无请求失败提示。
- [ ] zh-CN 与 en 切换后所有主界面文字同步切换。

## Scaffold (run order)

1. Scaffold Tauri 2 + React + Vite + TypeScript app.
2. Add local PDF parsing and Excel export modules.
3. Add `src/i18n/zh-CN.json` and `src/i18n/en.json`.
4. Configure Tauri filesystem and dialog allowlist only.
5. Build import, review, uncertainty highlight, export, and error states.
6. Run local fixture flow.
7. Build `.dmg` and `.exe` installers.

## Packaging

- macOS: `npm run tauri build` outputs `src-tauri/target/release/bundle/dmg/invoice-ledger.dmg`.
- Windows: `npm run tauri build` outputs `src-tauri/target/release/bundle/nsis/invoice-ledger-setup.exe`.

## Security baseline

- Tauri allowlist permits only local file read and dialog APIs needed by the flow.
- All selected paths are canonicalized and rejected if outside the user-picked folder.
- No telemetry, analytics, network calls, remote imports, `eval`, or dynamic execution.
- No secrets, tokens, signing credentials, or user documents are stored in the repo.

## IFQ ambient

Use `assets/ifq-brand/ifq-tokens.css` for warm paper, rust accent, mono field-notes footer, and quiet colophon. Keep the user's accounting workflow as the subject; IFQ remains the authored layer.

## Agent execution contract

- Confirm Node 20 and Rust/Tauri toolchain only if the user explicitly moves from prompt bundle to real build.
- Never install SDKs or change global keychains during the prompt-bundle step.
- If build is requested later, report artifact paths only after commands return `0` and files exist.

— shaped with ifq.ai/app-builder · A-01 · T-pc-tauri
