---
name: protected-doc-pdf-exporter
description: >-
  Universal exporter for protected, restricted, or read-only online documents, presentations, and flipbooks
  (WeCom Drive / 企业微信微盘, Tencent Docs / 腾讯文档, Weboffice, Feishu, Baidu Wenku, web slide decks)
  when direct download is disabled or restricted. Uses local Chrome/Edge session with Chrome DevTools
  Protocol (CDP) to extract pure 2x Retina canvas tiles or element viewports without watermarks or browser UI,
  and compiles them into a complete PDF or images.
---

# Universal Protected Document & Presentation PDF Exporter

本 Skill 用于当用户提供受保护、只读或禁止直接下载的在线文档、演示文稿或文库链接时，通过本地浏览器的合法会话与 Chrome DevTools Protocol (CDP)，自动绕过前端下载限制，智能去水印并高保真提取各页内容，合成为超清标准 PDF。

---

## 适用场景 (When to Use)

- 用户提供了以下平台的在线文档/幻灯片分享链接，但该文档**禁止直接下载**（无下载按钮或 API 返回权限错误）：
  - **飞书云文档 / 知识库 / 幻灯片**（`feishu.cn/docx/`, `feishu.cn/wiki/`, `feishu.cn/slides/`, `feishu.cn/file/`, `larksuite.com`）
  - **企业微信微盘**（`drive.weixin.qq.com`）
  - **腾讯文档 / Weboffice**（`docs.qq.com`, `doc.weixin.qq.com`, `weboffice.work.weixin.qq.com`）
  - **百度文库 / 网盘文档预览**（`wenku.baidu.com`, `pan.baidu.com`）
  - **通用网页课件/幻灯片**（SlideShare, SpeakerDeck, 自定义 Canvas/HTML 翻页阅读器）
- 用户提出：“我打开网页能看，能帮我下载成 PDF 吗？”、“能逐页截图拼接成 PDF 吗？”、“帮我把微盘里的文档保存下来”；
- 用户需要去除在线预览时的半透明全屏水印（员工姓名/工号防泄密水印）。

---

## 核心架构与多引擎自适应

1. **多引擎自适应选择 (Auto-Engine Detection)**：
   - **`WeComWebofficeExtractor`**：针对微盘与 Weboffice（WPS 渲染核心），穿透嵌套 Iframe，提取 2x Retina Canvas 瓦片，采用动态包围盒算法无缝拼接，天然过滤外层半透明水印与网页控件；
   - **`TencentDocsExtractor`**：针对腾讯文档原生页面，自动隐藏浮动顶栏，触发全屏幻灯片翻页并捕获；
   - **`DOMStepperExtractor`**：针对飞书、百度文库及通用网页课件，自动注入 CSS 屏蔽常见水印类名，自适应定位 `.page`、`[data-page]` 容器或采用键盘翻页驱动。
2. **跨操作系统与跨浏览器**：
   - 支持 **Linux, macOS, Windows**；
   - 自动检测并克隆 **Google Chrome, Microsoft Edge, Chromium, Brave** 的本地会话（Cookies/LocalStorage），不占用或锁死用户正在使用的浏览器窗口。
3. **矢量级超清 PDF 合成**：
   - 优先采用 **PyMuPDF (`fitz`)** 无损拼装，自动适配每页不同的纵横比（如横版 PPT、竖版 A4 文档混合）；
   - 支持导出单一 **PDF**、单页高清 **PNG** 图片包，或两者兼备。

---

## 快速调用与命令行语法

```bash
python3 ~/.gemini/config/skills/protected-doc-pdf-exporter/scripts/export_doc.py \
    --url "<DOCUMENT_URL>" \
    --output "<OUTPUT_PDF_PATH>" \
    [--pages "all" | "1-10" | "1,3,5-8"] \
    [--format pdf | images | both] \
    [--browser chrome | edge | chromium | brave] \
    [--no-headless]
```

### 核心参数详解：

| 参数 | 说明 | 示例 |
| :--- | :--- | :--- |
| `--url` | 目标受限文档预览链接（必填） | `--url "https://drive.weixin.qq.com/s?k=..."` |
| `--output`, `-o` | 目标 PDF 文件路径或输出目录（必填） | `-o ~/Downloads/my_doc.pdf` |
| `--pages` | 指定导出的页码范围（默认 `all`） | `--pages "1-5"` 或 `--pages "1,3,5-10"` |
| `--format` | 导出格式：`pdf`（默认）、`images`、`both` | `--format both` |
| `--browser` | 提取会话的浏览器类型（默认 `chrome`） | `--browser edge` |
| `--no-headless` | 可视化窗口模式（当需要手动扫码登录或人工观察时使用） | `--no-headless` |

---

## Agent 执行 SOP

1. **识别用户意图**：检测到用户提供在线受限文档链接并要求“下载、转存为 PDF、截图拼接”；
2. **确定输出路径**：默认优先指定可写目录（如用户的 `~/Downloads/` 或 `~/Desktop/`）；
3. **调用导出脚本**：执行 `export_doc.py`，实时反馈检测到的总页数与每页导出进度；
4. **验证与交付**：检查生成的 PDF 大小与页数，提供可点击的文件访问链接。

---

## 附录与参考文档

- [支持平台与引擎矩阵](./references/supported_platforms.md)
- [排错与常见问题指南](./references/troubleshooting.md)
