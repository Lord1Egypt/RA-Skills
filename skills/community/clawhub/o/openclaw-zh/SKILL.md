---
name: openclaw-zh
slug: openclaw-zh
version: "1.0.0"
description: OpenClaw 界面汉化技能。用于将 OpenClaw 的 Web Control UI 和 Chrome 扩展界面翻译为中文。触发条件：用户提到"汉化"、"中文界面"、"翻译 OpenClaw 界面"、"openclaw-zh" 或需要汉化 OpenClaw 组件。
---

# OpenClaw 界面汉化

将 OpenClaw 用户界面组件翻译为中文。

## 支持的组件

| 组件 | 路径 | 状态 |
|------|------|------|
| Web Control UI | `/usr/lib/node_modules/openclaw/dist/control-ui/` | ✅ 支持 |
| Chrome 扩展 | `/usr/lib/node_modules/openclaw/assets/chrome-extension/` | ✅ 支持 |
| 文档 | `/usr/lib/node_modules/openclaw/docs/zh-CN/` | ✅ 已有 |

## 快速使用

### 汉化 Control UI

```bash
# 应用中文翻译
python3 ~/.openclaw/workspace/skills/openclaw-zh/scripts/apply_translation.py

# 恢复英文（重新安装）
npm install -g openclaw@latest
```

### 汉化 Chrome 扩展

直接编辑 `options.html`，将英文替换为中文。

## 翻译文件

- `translations/control-ui-zh.json` - Control UI 中文翻译映射
- `translations/chrome-extension-zh.json` - Chrome 扩展中文翻译映射

## 注意事项

1. **版本更新会覆盖翻译** - OpenClaw 更新后需重新应用翻译
2. **备份原文件** - 翻译前会自动备份原始文件
3. **贡献翻译** - 可向官方 GitHub 提交 PR 添加 i18n 支持

## 扩展翻译

如需添加或修改翻译：

1. 编辑 `translations/control-ui-zh.json`
2. 运行 `apply_translation.py` 应用更改

## 相关资源

- OpenClaw 中文文档: `/usr/lib/node_modules/openclaw/docs/zh-CN/`
- OpenClaw GitHub: https://github.com/openclaw/openclaw
