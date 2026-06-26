# Obsidian 知识库底层逻辑参考

## 核心概念

### Vault（知识库）
Obsidian 以本地文件夹（Vault）为单位管理笔记。所有文件均为纯文本 Markdown，可在任何编辑器打开。知识库的结构直接反映用户的思维组织方式。

### 文件与文件夹
- 文件夹用于**物理归档**：按项目、时间、主题分层
- 典型目录结构（参考，具体以用户实际为准）：
  - `0-Inbox/`：收件箱，待处理未分类内容
  - `1-Projects/`：进行中的项目笔记
  - `2-Areas/`：持续关注的领域（健康、财务、工作）
  - `3-Resources/`：参考资料、知识储备
  - `4-Archive/`：已完结内容
  - `Daily Notes/`：每日笔记

### Links（双向链接）
- `[[Note Name]]` 语法建立笔记间连接
- 双向链接是 Obsidian 知识图谱的核心
- Backlinks 面板显示所有引用当前笔记的来源
- 孤立笔记（无链接）通常意味着知识孤岛

### Tags（标签）
- `#tag` 语法打标签，支持嵌套：`#tag/subtag`
- 标签用于**跨目录的横向聚合**，与文件夹的纵向层级互补
- 常见标签体系：
  - 状态标签：`#status/inbox` `#status/done` `#status/wip`
  - 类型标签：`#type/log` `#type/reference` `#type/project`
  - 主题标签：`#topic/ai` `#topic/finance` `#topic/health`

### Frontmatter（元数据）
```yaml
---
title: 笔记标题
date: 2026-04-21
tags: [tag1, tag2]
status: active
aliases: [别名]
---
```
- YAML 格式，位于文件开头
- 支持 Dataview 查询（类 SQL 语法检索笔记）
- 常见字段：`title`、`date`、`tags`、`status`、`type`、`source`

### Dataview 插件
- 用 `dataview` 代码块执行数据库式查询
- 示例：
  ```dataview
  TABLE date, status FROM "1-Projects" WHERE status = "active"
  ```
- 支持 TABLE / LIST / TASK / CALENDAR 四种视图

### Templates 模板
- 模板文件夹中存放可复用笔记结构
- 常见模板：每日笔记模板、会议记录模板、项目模板、读书笔记模板

### Canvas（画布）
- 无限画布，用于非线性思维整理
- 可嵌入笔记卡片、图片、网页

## 用户操作模式分类

### 1. 信息捕获（Capture）
- 快速录入想法到 Inbox
- 剪藏网页（Clipper 插件）
- 每日笔记记录日志
- 触发词：新建、快速录入、收件箱、剪藏

### 2. 整理归档（Organize）
- 将 Inbox 内容分类到对应目录
- 打标签、建立链接
- 整理 frontmatter 元数据
- 触发词：整理、归档、分类、打标签

### 3. 知识连接（Connect）
- 建立双向链接
- 发现相关笔记（Backlinks / Graph View）
- MOC（Map of Content）笔记汇聚主题
- 触发词：链接、关联、图谱、MOC

### 4. 检索回顾（Retrieve）
- 全文搜索
- Dataview 查询
- 标签过滤
- 触发词：搜索、查找、查询、回顾

### 5. 输出创作（Output）
- 从笔记中提炼成文章/报告
- 利用 Canvas 整合多篇笔记
- 触发词：写作、输出、整理成、导出

## 常用插件生态
| 插件 | 功能 |
|------|------|
| Dataview | SQL 式查询笔记 |
| Templater | 高级模板（支持 JS 脚本） |
| Calendar | 日历式导航每日笔记 |
| Obsidian Git | 自动 Git 同步 |
| QuickAdd | 快速捕获/命令宏 |
| Tasks | 任务管理（跨笔记） |
| Excalidraw | 手绘白板 |
| Periodic Notes | 周/月/季/年总结笔记 |
