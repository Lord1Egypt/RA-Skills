# Protected Document & Presentation PDF Exporter

<p align="center">
  <b>受限在线文档、课件与只读演示文稿的高清 PDF 自动化导出工具</b><br>
  <i>A privacy-first, cross-platform CLI tool & AI Agent skill to export protected, view-only online presentations and documents into crystal-clear vector PDFs.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT" />
  <img src="https://img.shields.io/badge/Platforms-Linux%20|%20macOS%20|%20Windows-blue" alt="Supported Platforms" />
  <img src="https://img.shields.io/badge/Privacy-100%25%20Local-success" alt="Privacy First" />
</p>

---

## 📖 简介 (Overview)

在日常办公与学术研究中，我们经常遇到分享者设置了“**仅允许在线查看、禁止直接下载/打印**”的文档（例如企业微信微盘、腾讯文档、飞书文档/幻灯片、百度文库等）。即使我们拥有合法的查看权限，也无法方便地离线备份或做研读批注。

**Protected Document PDF Exporter** 采用客户端浏览器无头自动化驱动技术（Chrome DevTools Protocol, CDP），在**用户已具备合法访问权限**的前提下：
- 自动穿透多层跨域沙箱与 Canvas 渲染核心；
- 自动提取底层的原生矢量渲染画布（Canvas Tiles），规避网页前端的下载限制；
- 动态拼合多块视网膜级（2x Retina）高分辨率画布，消除接缝；
- 自动滤除全屏半透明防泄密水印与网页浮动工具栏；
- 一键无损拼接编译为高质量的标准矢量 PDF 文件。

---

## 🔒 隐私保护与数据安全承诺 (Privacy & Security)

本项目在设计与实现上严格贯彻 **Privacy-First（隐私优先）** 与 **Local-Only（纯本地化）** 原则：

1. **零数据上传与外部遥测 (Zero Telemetry)**：
   - 本工具不包含任何埋点、数据统计、网络回传或第三方远程接口；
   - 所有的网络通信仅存在于本地无头浏览器与目标文档官方服务器之间。
2. **纯本地离线处理 (100% Local Execution)**：
   - 页面渲染、Canvas 拼接、水印过滤与 PDF 生成全部在您的本地 CPU/内存中运行，数据绝不离开您的设备。
3. **零凭据存储与安全沙箱 (Zero Credential Storage)**：
   - 本工具**绝不索取、存储或记录**任何账号密码、Cookie 或 Token；
   - 仅在运行时临时克隆系统默认浏览器的合法会话，任务完成后**立即彻底销毁**临时运行目录，不留存任何会话副本。

---

## ⚖️ 免责声明 (Legal Disclaimer)

> **⚠️ 请在开始使用本工具前仔细阅读以下条款：**

1. **合法使用前提**：
   - 本项目属于个人学习、技术研究与个人合法资产离线备份的辅助工具。
   - 使用者在运行本工具前，**必须对目标文档拥有合法的访问与阅读权限**。本工具不提供任何破解鉴权、绕过登录、暴力破解或越权访问的功能。
2. **版权与合理使用**：
   - 导出的文档所有权及知识产权仍归原作者或合法版权所有人所有。
   - 使用者使用本工具导出的内容仅供**个人学习、离线阅读、学术研讨或无障碍辅助**使用；**严禁**将导出内容用于任何商业分发、恶意传播、商业牟利或侵犯他人知识产权与企业商业秘密的行为。
3. **免责与责任界定**：
   - 本项目完全基于开源协议（MIT License）按“现状（AS IS）”提供，开发者不对因使用本工具引起的任何纠纷、争议、数据损坏或法律后果承担直接或连带责任。
   - 使用者应对其使用本工具的具体行为及合规性承担全部责任。如您不同意上述条款，请勿使用本项目。

---

## 🌟 核心特性 (Features)

- **多平台自适应支持**：
  - **企业微信微盘** (`drive.weixin.qq.com`)
  - **腾讯文档 & Weboffice** (`docs.qq.com`, `doc.weixin.qq.com`, `weboffice.work.weixin.qq.com`)
  - **飞书云文档 / 知识库 / 幻灯片** (`feishu.cn/docx/`, `feishu.cn/wiki/`, `feishu.cn/slides/`)
  - **通用网页课件与翻页阅读器** (SlideShare, SpeakerDeck, 百度文库等)
- **动态几何无损拼接**：
  - 自动识别每个 Canvas 瓦片的物理像素比例与 CSS 偏移量，支持纵横任意多 Tile 拼合；
  - 完美适配横版 PPT、竖版 A4 研报以及各类异形比例，**接缝零错位**。
- **纯净版面与反水印过滤**：
  - 直接从渲染图层中提取画面，天然避开上层叠加的用户姓名/手机号防泄密水印与网页控件。
- **全平台支持**：
  - 原生适配 **Linux、macOS、Windows** 三大操作系统；
  - 自动适配 **Google Chrome、Microsoft Edge、Chromium、Brave** 浏览器会话。
- **双形态交付**：
  - 既是独立的 **Python CLI 命令行工具**；
  - 也是标准规范的 **AI Agent 扩展技能 (Skill)**，即装即用。

---

## 🛠️ 安装与前置要求 (Prerequisites)

### 1. 软件环境
- Python 3.9+
- 现代 Chromium 系浏览器：Google Chrome、Microsoft Edge 或 Chromium（日常登录使用的浏览器）

### 2. 方式一：一键快速安装（推荐）
在终端中执行以下一键安装命令，将自动克隆仓库、安装依赖并配置全局 CLI 与 AI Agent Skill：

```bash
curl -fsSL https://raw.githubusercontent.com/Nelson-zhou/protected-doc-pdf-exporter/main/install.sh | bash
```

### 3. 方式二：手动克隆与安装
```bash
git clone https://github.com/Nelson-zhou/protected-doc-pdf-exporter.git
cd protected-doc-pdf-exporter

pip install -r requirements.txt
```

---

## 🚀 命令行快速上手 (Usage)

### 1. 导出受限文档为高清 PDF（最简用法）
确保您已在桌面的 Chrome 或 Edge 中打开过该文档并处于登录状态：

```bash
python3 export_doc.py \
    --url "https://drive.weixin.qq.com/s?k=xxxxxx" \
    -o ~/Downloads/我的文档.pdf
```

### 2. 按需导出指定页码（如只要第 1 至 5 页）
```bash
python3 export_doc.py \
    --url "https://your-company.feishu.cn/slides/xxxxxx" \
    -o ~/Downloads/飞书幻灯片.pdf \
    --pages "1-5"
```

### 3. 同时输出 PDF 与单页超清 PNG 截图切片
```bash
python3 export_doc.py \
    --url "https://docs.qq.com/xxxxxx" \
    -o ~/Desktop/tencent_doc.pdf \
    --format both
```

### 4. 指定浏览器类型或开启可见窗口（便于手动扫码）
```bash
python3 export_doc.py \
    --url "https://..." \
    -o output.pdf \
    --browser edge \
    --no-headless
```

### 参数详解

| 参数 | 默认值 | 作用与说明 |
| :--- | :---: | :--- |
| `--url` | *必填* | 目标只读文档、幻灯片或文库预览链接 |
| `--output`, `-o` | *必填* | 目标 PDF 文件保存路径或输出目录 |
| `--pages` | `all` | 导出的页码范围，例如 `all`, `1-5`, `1,3,5-10` |
| `--format` | `pdf` | 输出格式：`pdf`、`images`（仅图片切片）、`both`（两者皆要） |
| `--browser` | `chrome` | 会话来源浏览器：`chrome`、`edge`、`chromium`、`brave` |
| `--quality` | `95` | PDF 合成图片质量压缩比率 (1-100) |
| `--no-headless` | `False` | 是否以可见窗口启动浏览器（用于手动观察或扫码） |
| `--keep-images` | `False` | 任务结束后是否保留临时生成的每页 PNG 切片 |

---

## 🤖 作为 AI Agent Skill 使用

本项目完全遵循 Antigravity / Claude Code / Cursor / Codex 技能体系标准，天然就是一个标准的 **AI Agent Skill**！

### 1. 全局安装到 AI 技能库
```bash
# 克隆到 Antigravity 全局技能库（跨所有工作区永久生效）
git clone https://github.com/Nelson-zhou/protected-doc-pdf-exporter.git ~/.gemini/config/skills/protected-doc-pdf-exporter

# 安装依赖
pip install -r ~/.gemini/config/skills/protected-doc-pdf-exporter/requirements.txt
```

### 2. 项目工作区安装（供团队协作与代码仓库共享）
将本仓库克隆或软链接到项目的 `.agents/skills/` 目录：
```bash
mkdir -p .agents/skills/
git clone https://github.com/Nelson-zhou/protected-doc-pdf-exporter.git .agents/skills/protected-doc-pdf-exporter
```

### 3. AI 对话交互体验
安装后无需任何额外配置，当您向 AI 发送受限文档链接时：
> **您**：“*帮我把这个微盘链接导出成 PDF：https://drive.weixin.qq.com/s?k=...*”  
> **AI**：自动触发 `protected-doc-pdf-exporter` 技能，完成后台静默无水印抓取并交付高清 PDF 文件。

---

## 🏗️ 架构与工作流 (Architecture)

```text
[用户输入文档 URL]
        │
        ▼
[BrowserManager] ──> 检测系统环境 (Linux/macOS/Windows) ──> 克隆会话 Cookies
        │
        ▼
[CDP 无头自动化会话] ──> 穿透多层 Iframe & DOM 结构
        │
        ├──> [WeComWebofficeExtractor] (Canvas 瓦片动态几何包围盒重组)
        ├──> [FeishuExtractor] (DocX 预滚屏预热 + 视口无水印截屏)
        ├──> [TencentDocsExtractor] (原生翻页捕获)
        └──> [DOMStepperExtractor] (通用网页课件/幻灯片视口捕获)
        │
        ▼
[PDFBuilder] ──> 动态根据各页尺寸与 DPI 组装 ──> [高质量矢量级 PDF 交付]
```

---

## 📄 开源许可证 (License)

本项目遵循 [MIT License](LICENSE) 开源协议。
