# Keynote Video

> PPT/演示文稿转播报视频工具 —— LLM 管内容，脚本管技术

## 快速开始

```bash
node scripts/generate.js \
  --slides presentation.pptx \
  --scripts-dir scripts_rewritten/ \
  --output ./video/ \
  --project-dir ./project/
```

## 完整工作流

1. **Phase 0-2**（LLM 驱动）: 输入评估 → 内容理解 → 风格确定 → 讲稿生成 → 方案确认
2. **Phase 3-4**（脚本驱动）: PPT 截图 → TTS → 视频合成 → 质量验证

详见 `SKILL.md`。

## 支持的风格

| 风格 | 适用场景 | 音色 | 语速 |
|------|----------|------|------|
| 新闻播报 | 情报/资讯 | XiaoxiaoNeural | +30% |
| 资讯快报 | B站情报视频 | XiaoxiaoNeural | +15% |
| 技术汇报 | 方案/架构 | YunxiNeural | +20% |
| 技术培训 | 教程/入门 | YunxiNeural | +15% |
| 故事讲述 | 案例/产品 | YunxiNeural | +10% |
| 商业演讲 | BP/路演 | YunjianNeural | +25% |
| 轻松闲聊 | 团队分享 | XiaoyiNeural | +20% |

## 依赖

- Node.js v18+
- Python 3.8+ (`python-pptx`)
- ffmpeg 5.0+
- LibreOffice 7.0+
- edge-tts 7.0+
- poppler-utils (`pdftoppm`)

## 版本

v2.0 - 全新架构，LLM/脚本职责分离，项目隔离
