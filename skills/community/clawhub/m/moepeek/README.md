# MoePeek

轻量级 macOS 划词翻译工具，纯 Swift 6 开发。

## 概述

MoePeek 是一款 macOS 菜单栏翻译应用，支持划词翻译、OCR 截图翻译、剪贴板翻译和手动输入。安装体积仅 5MB，后台内存稳定约 50MB，支持 Apple 翻译（设备端运行，保护隐私）。

## 翻译模式

- **划词翻译**：选中任意应用中的文本，弹出浮动翻译面板
- **OCR 截图**：截取屏幕区域并翻译识别出的文字
- **剪贴板翻译**：翻译剪贴板内容
- **手动输入**：按需输入或粘贴文本进行翻译

## 支持的翻译服务

| 免费 | API | LLM | 系统 |
|------|-----|-----|------|
| Google Translate | DeepL | OpenAI | Apple Translation |
| Bing Translate | Baidu | Anthropic | |
| Youdao | NiuTrans | DeepSeek | |
| Caiyun | DeepLX | 智谱 GLM | |
| OpenRouter | Ollama (本地) | LM Studio (本地) | |

## 快速开始

```bash
# 下载最新版本
https://github.com/cosZone/MoePeek/releases/latest
```

## 相关资源

- GitHub: https://github.com/cosZone/MoePeek
- Release: https://github.com/cosZone/MoePeek/releases/latest
