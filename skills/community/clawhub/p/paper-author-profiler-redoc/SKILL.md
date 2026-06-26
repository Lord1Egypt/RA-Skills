---
name: paper-author-profiler-redoc
description: 根据论文链接（arXiv / Google Scholar / Nature 等）自动抓取全部作者列表，并行搜集每位作者的公开信息（所在机构、研究方向、教育背景、Google Scholar / GitHub / LinkedIn / 个人主页），生成双 Sheet Redoc 在线文档：Sheet1 为作者个人信息表（含账号链接），Sheet2 为按学校背景分组汇总。适用于 DeepSeek / 大模型类大型合著论文（10人以上）。当用户说「帮我整理这篇论文的作者信息」「把作者都查一查」「生成作者档案文档」「做成表格」时使用。
---

# paper-author-profiler-redoc

## 工作流程

### Step 1：获取完整作者列表

优先从 Semantic Scholar API 获取：
https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=authors

### Step 2：并行搜集作者信息

超过 30 人时用 sessions_spawn 分批（每批 30-40 人，最多 5 个子代理）。
见 references/batch-task-template.md。

### Step 3：生成双 Sheet Redoc 文档

用 hi-redoc-curd skill 推送。见 references/output-template.md。

## 注意事项
- 不收录手机/微信等联系方式
- 默认在职，确认跳槽才标注
- 信息无法确认时写"待确认"
