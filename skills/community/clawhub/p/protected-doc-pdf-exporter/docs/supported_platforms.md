# 支持的平台与在线文档阅读器 (Supported Platforms)

`protected-doc-pdf-exporter` 采用多引擎自适应抓取架构，支持以下国内外主流受限文档与只读演示平台：

---

## 1. 腾讯生态平台 (Tencent Platforms)

| 平台 | 域名特征 | 默认提取引擎 | 说明 |
| :--- | :--- | :--- | :--- |
| **企业微信微盘** | `drive.weixin.qq.com` | `WeComWebofficeExtractor` | 穿透嵌套沙箱，提取 2x Retina Canvas 瓦片，自然滤除用户水印 |
| **腾讯 Weboffice** | `weboffice.work.weixin.qq.com` | `WeComWebofficeExtractor` | WPS 核心在线渲染引擎，动态计算瓦片几何坐标 |
| **腾讯文档** | `docs.qq.com`, `doc.weixin.qq.com` | `TencentDocsExtractor` | 自动隐藏浮动顶栏，触发全屏翻页捕获 |

---

## 2. 飞书生态平台 (Feishu / Lark Suite)

| 平台 / 文档类型 | 域名特征 | 默认提取引擎 | 说明 |
| :--- | :--- | :--- | :--- |
| **飞书新版文档 (DocX)** | `feishu.cn/docx/...` | `FeishuExtractor` | 预滚屏预热懒加载块，屏蔽侧边导航与水印，自动分屏捕获 |
| **飞书知识库 (Wiki)** | `feishu.cn/wiki/...` | `FeishuExtractor` | 自动隐藏左侧目录树与评论浮条，全宽渲染抓取 |
| **飞书幻灯片 (Slides)** | `feishu.cn/slides/...` | `FeishuExtractor` | 逐页点击左侧缩略图自动切换，捕获高清演示画面 |
| **飞书云空间文件预览** | `feishu.cn/file/...` | `FeishuExtractor` | 适配内嵌 PDF/PPT 预览器，按页精准捕获 |

---

## 3. 其它主流在线协作与文库平台 (Other Platforms)

| 平台 | 域名特征 | 默认提取引擎 | 说明 |
| :--- | :--- | :--- | :--- |
| **飞书文档 / 妙记** | `feishu.cn`, `larksuite.com` | `DOMStepperExtractor` | 元素级视口精确定位，自动注入去水印 CSS |
| **百度文库 / 网盘** | `wenku.baidu.com`, `pan.baidu.com` | `DOMStepperExtractor` | 逐页视口滚入，去除固定遮罩与浮窗 |
| **钉钉文档** | `alidocs.dingtalk.com` | `DOMStepperExtractor` | 视口区域捕获与自适应拼装 |
| **通用网页幻灯片** | SlideShare, SpeakerDeck, 网页 PPT | `DOMStepperExtractor` | 键盘 PageDown / Arrow 翻页与视口捕获 |

---

## 3. 操作系统与浏览器兼容性 (Compatibility)

- **操作系统**：
  - Linux (Ubuntu / Debian / Arch / Fedora 等)
  - macOS (Intel & Apple Silicon)
  - Windows 10 / 11
- **支持浏览器**：
  - Google Chrome
  - Microsoft Edge
  - Chromium
  - Brave
