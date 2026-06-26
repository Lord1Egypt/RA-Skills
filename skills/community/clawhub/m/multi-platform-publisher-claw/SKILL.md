---
name: multi-platform-publisher-claw
description: |
  全平台内容自动分发与搜索排名优化专家。将内容（视频/图文）一键同步发布到抖音、小红书、视频号、B站、微博等多个平台，自动进行平台差异化适配（标题长度/话题标签/封面尺寸）、SEO关键词优化、最佳时间计算，并监控发布状态。
  触发场景：用户说"发布内容"、"多平台发布"、"一键分发"、"自动发布"、"定时发布"、"SEO优化"、"话题标签"、"跨平台"、"内容分发"、"同步发布"时使用。
---

# 全平台自动分发虾 (multi-platform-publisher-claw)

## 工作流程

**步骤 1：收集内容包**
确认以下信息（缺失时向用户询问）：
- 内容文件：视频（MP4/MOV）或图文（Markdown/HTML）
- 封面图片（JPG/PNG）
- 标题和描述
- 目标平台列表（默认全平台）
- 发布时间（默认立即发布）

**步骤 2：平台差异化适配**
参考 `references/platform-rules.md` 对各平台进行内容适配。

**步骤 3：SEO优化**
参考 `references/seo-optimization.md` 优化关键词和话题标签。

**步骤 4：确定发布时间**
参考 `references/best-posting-time.md`，若用户未指定时间则推荐最佳时段。

**步骤 5：执行发布**
调用 `scripts/publish-content.py` 发布内容：

```bash
# 发布到所有平台（立即）
python3 scripts/publish-content.py --all --video video.mp4 --title "标题" --desc "描述"

# 定时发布
python3 scripts/publish-content.py --all --video video.mp4 --title "标题" --desc "描述" --schedule "2026-04-02 09:00"

# 发布到指定平台
python3 scripts/publish-content.py --platform douyin,bilibili --video video.mp4 --title "标题" --desc "描述"
```

**步骤 6：汇总报告**
发布完成后输出各平台发布状态（成功/失败/审核中）及内容链接。

## 注意事项
- 小红书无官方API，通过自动化脚本发布，稳定性较低
- 定时发布依赖服务持续运行
- 失败自动重试最多3次
- 需提前配置各平台账号（`.env` 文件）
