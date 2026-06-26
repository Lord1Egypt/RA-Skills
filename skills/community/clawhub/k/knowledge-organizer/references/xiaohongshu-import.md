# Xiaohongshu Note Import

适用：小红书 / RedNote 笔记链接入库到 Obsidian 知识库。

## 标准流程

1. **小红书链接优先走 `xiaohongshu-mcp`**
   - 不要优先 `web_fetch`
   - 也不要默认把小红书 note 当普通网页抓

2. **先检查 MCP 状态**
   - 优先检查本地 `xiaohongshu-mcp` 服务与登录状态
   - 若状态异常（服务未启动 / 登录失效），先报告，不要直接硬跑 detail/search

3. **优先用 `detail` 获取结构化内容**
   - 如果已有 note 标识、`feed_id`、`xsec_token` 等可直接定位信息，优先 `detail`
   - 如果只有关键词或不完整标识，再走 `search` → `detail`

4. **先整理结构化抓取结果，再渲染**
   - 把小红书笔记先整理成中间 draft
   - 不要一开始就直接拼最终 Markdown

5. **重复检查先于最终写入**
   - 至少检查标题、`source_url`
   - 有条件时再做近似内容检查

6. **渲染与写入**
   - 优先复用 `scripts/obsidian_note.py`
   - 保持来源字段、作者、标签、图片、摘要尽量结构化

## 推荐的中间 draft 字段

最少包含：
- `title`
- `source_type: xiaohongshu_note`
- `source_url`
- `author`
- `published`
- `tags`
- `summary`
- `bullets`
- `images`
- `raw_content_markdown`

可选增强字段：
- `engagement`（likes / comments / collects）
- `comments_excerpt`
- `aliases`

## 偏离条件

只有在以下情况才允许退回普通 browser / web 路径：
- `xiaohongshu-mcp` 服务不可用
- 登录状态失效
- 无法解析 note 标识
- `detail` 失败且确认不是瞬时错误

偏离时必须说明：
- 为什么不能走 `xiaohongshu-mcp`
- 改用什么替代路径
- 哪一步失败了
