---
name: hyfceph
description: Run the HYFCeph cephalometric workflow through the HYFCeph portal with an API key by uploading one or two local lateral ceph images. The public user only sends images; the server reuses the owner's synced browser session behind the scenes. Save a local result JSON, write an annotated PNG, and return supported cephalometric metrics or overlap traces. Use when the user wants HYFCeph analysis, mentions HYFCeph, provides an API key, or sends ceph images.
---

# HYFCeph

Use the bundled Node service client.

In user-facing replies, use `HYFCeph` or `Ceph`.

Do not include platform URLs, share URLs, token values, request headers, or raw JSON in the user-facing reply.

## Publishing model

Do not try to protect a public skill by encrypting `SKILL.md` or local scripts. That only creates client-side obfuscation. Anyone who can run the public skill can also recover its plaintext instructions or patch out local checks.

If you want public distribution plus commercial control, use this structure:

1. Publish only a thin client skill.
2. Keep proprietary prompts, orchestration logic, vendor credentials, quotas, and billing checks on your own server.
3. Let users register on your website and get an API key.
4. Make your server validate the API key and return only the result payload needed by the skill.

This is the only reliable way to hide real business logic.

## Registration gate

Before measurement starts, prefer a locally saved API key from a previous successful run.

The bundled service client now persists the validated API key to:

`~/.codex/state/hyfceph-auth.json`

So in a new conversation, do not ask for the API key again by default. First try the saved key automatically.

Use this reply when the user has not yet provided an API key:

`你好，我是 HYFCeph。请先前往 https://hyfceph.52ortho.com/ 注册账号并获取 API Key。拿到后把 API Key 发我，我再开始测量。`

Do not continue into measurement until the user has either:

- provided an API key in the conversation, or
- already configured a valid local saved key.

## First reply rule

When the skill is triggered and the user has not yet给出 API key:

1. First prefer the saved local HYFCeph API key from a previous successful run.
2. Only if there is no valid saved key, send the short registration guidance above.
3. Do not send old metrics, old case data, old images, or cached results.

## Default workflow

After the user has either provided an API key, or a valid saved key is already present, and they explicitly asked to start measurement:

1. If the user has provided one local ceph image, upload it to the portal and run:

```bash
node scripts/hyfceph-service-client.mjs --image /path/to/ceph.png
```

If the user has just provided a new API key in this conversation, pass it once:

```bash
node scripts/hyfceph-service-client.mjs --api-key 'user-api-key' --image /path/to/ceph.png
```

2. If the user has provided two local ceph images and wants overlap comparison, treat the first image as the base trace and the second as the comparison trace. Default to `SN` alignment unless the user explicitly asks for `FH`:

```bash
node scripts/hyfceph-service-client.mjs \
  --image /path/to/base-ceph.png \
  --compare-image /path/to/compare-ceph.png \
  --align-mode SN
```

If they have just provided a new API key in this conversation, pass it once with `--api-key`.

This is the default public path. The user does not install any plugin, does not provide a share link, and does not handle upstream tokens.

3. Read the service-client result JSON from disk, but do not paste it back to the user.

4. Save the generated image artifacts for follow-up replies:
   - `annotatedPngPath`
   - `contourPngPath`
   - If PNG conversion is unavailable on that device, fall back to the corresponding SVG path.

5. Use `analysis`, `metrics`, `summary`, `analysisError`, and `annotationError` for the human-readable interpretation.

6. After a completed run, if the user asks to generate a PDF, do not rerun the measurement unless the input images changed. Prefer the latest local result and run:

```bash
node scripts/hyfceph-service-client.mjs --latest-pdf --patient-name '患者姓名'
```

If you already know the exact result JSON path, you may use:

```bash
node scripts/hyfceph-service-client.mjs --pdf-input /absolute/path/to/result.json --patient-name '患者姓名'
```

For measurement replies, prefer the server-side static HTML report link instead of generating a local PDF. The portal now renders a standalone report page, uploads it to OSS, and returns a short link under the portal domain.

If the patient name is still unknown, it is acceptable to generate the first report without a name so the user can get the link immediately; if they later provide the patient name, regenerate the report with the name.

## Outputs

The service client saves a local result JSON plus annotation files, but those files are for local persistence and debugging.

Prefer these reply-facing artifacts:

- `annotatedPngPath`: PNG landmark overlay for direct display when the user asks for 标点图
- `contourPngPath`: white-background PNG contour trace with tooth fill and no points, for direct display when the user asks for 轮廓图
- `reportShareUrl`: standard online static report link
- `prettyReportShareUrl`: beautified online static report link
- `feishuDocShareUrl`: backup Feishu document link
- `reportUpload`: standard report upload metadata
- `prettyReportUpload`: beautified report upload metadata
- `feishuDocUpload`: backup Feishu document metadata
- `metrics`: supported measurements
- `analysis.riskLabel`: short classification summary
- `analysis.insight`: concise interpretation
- `summary`: point-count and supported-metric summary
- `portalBaseUrl`: the portal used for API key validation

## Reply style

When the run succeeds:

1. Give a short clinical summary in plain Chinese.
2. Do not show the 标点图 or 轮廓图 automatically in the first result reply.
3. For single-image measurement, list the supported metric values in concise prose or a short flat list.
4. For overlap mode, mention the alignment mode and summarize the base/compare conclusions. Do not dump both raw metric arrays unless the user asks.
5. Do not mention JSON files unless the user explicitly asks for raw data.
6. End by asking which analysis framework they want next.
7. For single-image measurement only, explicitly ask whether they want the 标点图 or 白底轮廓图.
8. If the user asks for 标点图, show `annotatedPngPath` directly with Markdown image syntax using the absolute local path.
9. If the user asks for 轮廓图, show `contourPngPath` directly with Markdown image syntax using the absolute local path.
10. Keep the existing data-and-analysis reply shape unchanged. The static report link and image artifacts are additional additions, not replacements for the normal measurement reply.
11. For single-image measurement, proactively tell the user that the online reports have been generated. Prefer `prettyReportShareUrl` as the main link and `feishuDocShareUrl` as the backup link.
12. If `prettyReportShareUrl` exists, output it on its own line using this exact prefix:

`美化报告链接：<url>`

13. If `feishuDocShareUrl` exists, output it on its own line using this exact prefix:

`飞书文档版：<url>`

14. If `reportShareUrl` exists, you may additionally output it on its own line using this exact prefix:

`在线报告链接：<url>`

15. If `reportQrPngPath` exists, tell the user this QR can be scanned in WeChat to open the standard report, then show `reportQrPngPath` directly with Markdown image syntax using the absolute local path.

16. If `prettyReportQrPngPath` exists, tell the user this QR can be scanned in WeChat to open the beautified report, then show `prettyReportQrPngPath` directly with Markdown image syntax using the absolute local path.

17. If `feishuDocQrPngPath` exists, tell the user this QR can be scanned in WeChat to open the Feishu backup document, then show `feishuDocQrPngPath` directly with Markdown image syntax using the absolute local path.

Use this exact style for the closing choice line:

`可继续按以下分析法整理：Downs、Steiner、北大分析法、ABO、Ricketts、Tweed、McNamara、Jarabak。你选一个，我按那个口径继续解读。`

For single-image measurement, add this exact report follow-up line before the image follow-up line:

`这次的静态报告我也已经整理好了；我会把标准版和美化版链接一起发你。`

If QR codes exist, add this exact line after the two report links:

`如果你在微信里打不开链接，可以直接扫下面的二维码进入报告。`

For single-image measurement, add this exact image follow-up line after it:

`如果你要，我也可以把这次的标点图和白底轮廓图发你。`

If the user says they want把患者姓名写进报告 and the patient name is still unknown, ask this exact line first:

`可以。我先补一下患者姓名，报告开头会带上这个名字。`

## Constraints

- Require Node.js 18 or newer because the script uses native `fetch`, `Blob`, and `FormData`.
- PNG conversion tries `sips`, then `magick`, then `rsvg-convert`. If none exist, use the SVG output instead.
- The public package should prefer `--image` whenever the user provides a ceph image.
- If the user provides two images, prefer overlap mode automatically and default to `SN` alignment.
- Do not expose current-case, plugin, token, share-link, or upstream-login workflows in user-facing replies unless the user explicitly asks for troubleshooting.
- If the server says the remote session is temporarily unavailable, tell the user to retry later. Do not expose internal bridge details.
- Do not expose credentials in the final response.
