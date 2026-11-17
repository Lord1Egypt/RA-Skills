# Trending 总览输出模板

各仓库详情文件（格式见 `repo-output_template.md`）全部保存后，再按本模板生成总览文件。总览负责回答三件事：这期榜单有哪些仓库、每个仓库是做什么的、怎么跳转到详情。

## 一、保存位置

（1）周榜：`assets/weekly/YYYY-Wnn/Overview.md`（ISO 周数，如 `2026-W45/Overview.md`）；月榜：`assets/monthly/YYYY-Mnn/Overview.md`（如 `2026-M11/Overview.md`）。与各仓库详情文件在同一目录。

（2）具体路径以脚本输出为准。

（3）同一周（月）内重复运行时，脚本会先清理周期目录中上一次的详情与总览，再重新写入。

## 二、文件格式

（1）中英文、数字之间加空格；中文语境用全角标点。

（2）符合 markdownlint 规范：一个一级标题，其下为二级标题，各级内容之间用空白行隔开。

（3）月榜时，标题中的“周榜”替换为“月榜”，表头“本周新增”替换为“本月新增”。

（4）“来源”链接原样取脚本输出，不得手改：走第三方接口时为 `https://gitstock.org/api/v1/github/trending?period=weekly|monthly`，回退到页面（或使用 `--html`）时为 `https://github.com/trending?since=weekly|monthly`。

```markdown
# GitHub Trending 周榜

> 数据日期：YYYY-MM-DD，来源：<https://gitstock.org/api/v1/github/trending?period=weekly>，共 N 个仓库

## 一、榜单总览

| 排名 | 仓库 | 总 Stars | 本周新增 | Forks | 简介 | 详情 |
| ---- | ---- | -------- | -------- | ----- | ---- | ---- |
| 1 | [owner/repo](https://github.com/owner/repo) | 111,291 | +1,138 | 9,697 | 中文一句话简介 | [查看详情](Rank-01_owner_repo.md) |
| 2 | [owner/repo](https://github.com/owner/repo) | 11,524 | +3,792 | 781 | 中文一句话简介（信息有限） | [查看详情](Rank-02_owner_repo.md) |
```

## 三、总览表要求

（1）表头固定为：排名、仓库、总 Stars、本周新增、Forks、简介、详情，榜单内每个仓库一行，顺序与榜单排名一致。

（2）数据列（排名、仓库、总 Stars、新增、Forks）直接取脚本输出，不得改动。

（3）“简介”列是唯一允许改写的列：

- 用中文一句话概括，不超过 40 字，从该仓库详情“项目是什么”中提炼，说清“是什么 + 给谁用”。
- 信息有限的仓库在简介后加“（信息有限）”。
- 简介中的 `|` 须转义为 `\|`，不得换行。

（4）“详情”列是脚本生成的相对链接 `[查看详情](Rank-NN_owner_repo.md)`（与总览同目录），不得改动；每个链接都必须有对应的详情文件。

## 四、回答中的汇报

（1）保存完成后，在回答中给出总览文件路径和仓库数量。

（2）不重复贴整张表，不做额外总结。
