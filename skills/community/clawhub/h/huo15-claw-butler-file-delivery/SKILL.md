---
name: huo15-claw-butler-file-delivery
description: Deliver a file to the user's 龙虾管家 (Claw Butler) desktop/mobile client. Use whenever you produced a file (report, PDF, image, spreadsheet, export, archive, code bundle) and the user wants to receive, open, download, or save it — and especially the moment a normal send fails with "Message failed" or the file shows up only as a clickable link that 404s. Delivers via the client's `file.push` node capability (works), never via WebChat outbound (which cannot carry files). Triggers: 发我文件 / 把文件发过来 / 下载 / 导出给我 / send me the file / why is it just a link.
---

# 给龙虾管家客户端发文件（file.push）

龙虾管家（Claw Butler）客户端**通过 WebChat 通道连接**。WebChat 是 OpenClaw 的内部通道，**不支持出站文件投递** —— 你若想用普通消息附带文件，会得到 `Delivering to WebChat is not supported` / 客户端只看到 `Message failed`，或文件退化成一个打不开的链接。

**正确做法：用客户端的 `file.push` node 能力把文件推过去。** 客户端收到后会自动内联预览（图片 / PDF / Markdown / 代码 / 音视频），并让用户一键保存到设备。

## 何时用

- 用户要任何文件：报告、PDF、图片、Excel、导出、压缩包、代码包。
- 你已经在工作目录产出了文件，需要交付给用户。
- 你刚试着“发文件”失败了（Message failed / 只显示成链接）→ 立刻改用本能力重发。

## 怎么调用

用 **`nodes`** 工具，`action: "invoke"`，命令 `file.push`：

```
nodes(
  action="invoke",
  node="<目标客户端，单设备可用 auto>",
  invokeCommand="file.push",
  invokeParamsJson="{...见下...}"
)
```

`invokeParamsJson` 是一段 JSON 字符串，字段：

| 字段 | 说明 |
|---|---|
| `fileName` | 文件名（带扩展名，决定预览类型）。必填。 |
| `mimeType` | MIME 类型，如 `application/pdf`、`image/png`、`text/markdown`。建议填。 |
| `contentBase64` | **小文件（≤ ~48MB）**：文件字节的 base64。 |
| `url` | **大文件**：先把文件传到可访问地址（公司 OSS 等），再推 HTTP(S) URL，客户端自取。 |

`contentBase64` 与 `url` **二选一**：小文件走 base64（不依赖外网），大文件走 url（避免一次性塞爆连接）。

## 例子

小文件（内联 base64）：
```
nodes(action="invoke", node="auto", invokeCommand="file.push",
  invokeParamsJson="{\"fileName\":\"周报.pdf\",\"mimeType\":\"application/pdf\",\"contentBase64\":\"JVBERi0xLjQ...\"}")
```

大文件（OSS 中转）：
```
nodes(action="invoke", node="auto", invokeCommand="file.push",
  invokeParamsJson="{\"fileName\":\"数据集.zip\",\"mimeType\":\"application/zip\",\"url\":\"https://huo15-odoo.oss-cn-qingdao.aliyuncs.com/exports/数据集.zip\"}")
```

成功返回 `{ ok: true, payload: { received: true, fileName } }`，用户端会弹出预览。

## 红线

- ❌ 不要用普通消息 / WebChat 出站投递文件（必失败）。
- ❌ 不要把远程机器上的本地路径（`/home/...`、`media://...`）直接当链接发给用户 —— 客户端拿不到，必死链。改用 `file.push`：小文件 base64、大文件先传 OSS 再推 url。
- ✅ 大文件优先 `url` 模式；`contentBase64` 仅用于小文件。
- 前提：客户端已配对，且未在权限里关闭“接收文件 / Receive Files”（默认开启）。
