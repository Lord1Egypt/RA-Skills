---
name: Media_Processor
description: "OpenClaw 核心素材加工工具。支持对图片和视频（含 URL、m3u8、mp4）进行自动化处理，包括下载、压缩、添加水印和格式转换。"
version: 1.2.0
metadata:
  openclaw:
    type: command
    command: "python3"
    args: ["run.py", "--type", "{type}", "--action", "{action}", "--input", "{input}", "--output", "{output}", "--text", "{text}"]
    parameters:
      - name: type
        type: string
        description: "素材类型 (image, video)"
        required: true
      - name: action
        type: string
        description: "动作类型 (compress, watermark, convert)"
        required: true
      - name: input
        type: string
        description: "原始素材的绝对路径或远程 URL (支持 http/https, mp4, m3u8 等)"
        required: true
      - name: output
        type: string
        description: "处理后的保存路径"
      - name: text
        type: string
        description: "水印文字内容"
---

# Media_Processor (媒体处理专家)

## 描述
OpenClaw 核心素材加工工具。支持对本地或在线图片及视频进行自动化处理。
- **自动下载**：支持传入 HTTP/HTTPS 链接。
- **流媒体支持**：支持 m3u8 等流媒体协议。
- **编码转换**：默认支持将 H.265 (HEVC) 编码转换为 H.264 (AVC)。
- **图像处理**：支持压缩大小及添加文字水印。

## 适用场景
- 传入在线视频 URL 直接进行压缩并转码。
- 在发帖前，自动为下载的图片添加品牌水印。
- 针对有文件大小限制的平台，自动处理在线素材。


## 输入参数
- `type` (string): **必需**。可选值：`image`, `video`。
- `action` (string): **必需**。动作类型：
  - `compress`: 压缩文件大小.
  - `watermark`: 添加文字水印.
  - `convert`: 格式转换（图片转 JPEG，视频默认转为 H.264）。
- `input` (string): **必需**。原始素材的绝对路径。
- `output` (string): **可选**。处理后的保存路径。如果不传，会自动在同级目录生成带前缀的文件。
- `text` (string): **可选**。水印文字内容，默认为 `OpenClaw`。

## 返回结果
返回处理成功后的文件路径及状态信息。
