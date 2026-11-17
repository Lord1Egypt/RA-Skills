# WPS AI API 调研记录

> 调研时间：2026-07-17
> 调研目标：确认 WPS AI 能力（写作/分析/PPT/阅读）是否有开放 API 可供 kingdoc 调用

---

## 1. 调研结论

**WPS AI 没有公开的免费开发者 API 接口。**

WPS 开放平台（open.wps.cn）主要提供：
- 云文档 API（文件列表/上传/下载/权限）
- 协作 API（通讯录/消息/群组）
- WebOffice（在线预览/编辑）
- AI PPT 开放能力（企业付费，需企业认证）

WPS AI 的写作/分析/阅读能力是 **WPS 客户端内置功能**，通过 UI 唤起（如连按两次 Ctrl），无对外 REST API。

## 2. 具体能力调研

| 能力 | 开放 API？ | 调用方式 |
|------|-----------|---------|
| AI 写作（续写/改写/润色/翻译） | ❌ 无 | 仅 WPS 客户端 UI |
| AI 数据分析（公式/图表/洞察） | ❌ 无 | 仅 WPS 客户端 UI |
| AI PPT 生成 | ⚠️ 企业付费 | open.wps.cn AIPPT API |
| AI 阅读（总结/问答/划词） | ❌ 无 | 仅 WPS 客户端 UI |
| 会议纪要 | ✅ 有 API | open.wps.cn/v7/minutes/create |

## 3. 实现策略

**本地降级优先，自研逻辑实现**：
- 写作辅助：本地 NLP（分词/句法分析/同义词替换）+ 模板匹配
- 数据分析：本地统计（均值/趋势/异常检测）+ 公式生成
- PPT 生成：本地 python-pptx 生成（已有 generators.py）
- 阅读助手：本地文本摘要（TextRank）+ 关键信息提取

**未来扩展**：如 WPS AI 开放 API，只需新增 `backends/open_api.py`，无需改动上层逻辑。

## 4. 参考资源

- WPS 开放平台：https://open.wps.cn
- AI PPT API：https://open.wps.cn/documents/app-integration-dev/docs-center/aippt/Document
- 会议纪要 API：https://open.wps.cn/documents/app-integration-dev/wps365/server/meeting/minutes/create_minute
