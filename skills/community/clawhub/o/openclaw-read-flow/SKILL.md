---
name: openclaw-read-flow
description: "基于 FreshRSS 的漏斗式阅读流总技能：从未读抓取、昨天窗口切片、Digest 构建，到固定 6 栏 Daily Review 和后续知识沉淀。用于需要把聚合信息流加工成可读日报与可复用知识资产的场景。"
---

# OpenClaw Read Flow

以简体中文工作。把整个阅读工作流当成一条连续流水线处理，而不是把抓取、Digest、日报、知识沉淀割裂为孤立动作。

## 适用场景

- 已经搭建 FreshRSS，想把未读列表加工成结构化 Digest
- 需要把 Digest 进一步整理成固定栏目 Daily Review
- 需要在 OpenClaw / ClawHub 中复用整套漏斗式阅读流，而不是只调用单个局部技能
- 需要把阅读流与知识库、笔记、后续自动化对接

## 总体目标

工作流默认分为 5 层：

1. FreshRSS 聚合池
2. Digest 预处理
3. Daily Review 精选
4. 人工精读与知识沉淀
5. 反馈与轻量排序优化

原则：

- 先全量抓取未读池，再按昨天窗口处理
- Digest 必须严格去重
- Daily Review 必须落入固定 6 个栏目
- 默认不回写 FreshRSS 已读
- 默认不把未确认内容直接写入长期知识库

## 默认处理顺序

1. 从 FreshRSS Google Reader API 拉取未读列表
2. 默认切出“昨天”这个自然日窗口
3. 构建 Digest：
   - URL 精确去重
   - 相似内容去重
   - 正文抓取
   - 质量检查
   - 噪音过滤
   - 摘要生成
   - 初步排序
4. 生成 Daily Review
5. 视需要再接知识库、笔记或人工沉淀

## FreshRSS 约束

- 优先读取配置文件，其次读取环境变量
- 关键配置：
  - `base_url`
  - `username`
  - `api_password`
- 默认处理的是未读列表，而不是全部文章
- 默认不限制原始未读总数
- 默认不把处理过的内容自动回写为已读

## Digest 硬约束

- 必须严格去重：
  - URL 层去重
  - 事件层去重
  - 摘要层去重
- 所有英文文章都必须提供中文摘要
- 链接统一使用 Markdown：`[标题文本](链接)`
- 摘要不能只是改写标题，必须包含正文关键信息

## Daily Review 固定栏目

Daily Review 必须固定使用以下 6 个 `##` 栏目，顺序不变：

1. `今日大事`
2. `变更与实践`
3. `安全与风险`
4. `开源与工具`
5. `洞察与数据点`
6. `主题深挖`

要求：

- 不再使用“产业与公司动态”“云与基础设施”“研究与治理”“今日观察”这类题材栏目替代固定栏目体系
- 所有内容都要先判断认知任务，再落到对应栏目
- 若当天某栏目无高价值内容，也保留栏目，并用 `### 暂无关键更新` 说明

## LLM 在这条工作流中的职责

适合由 LLM 完成的中间层任务：

- 合并同一事件的多个信息来源
- 提炼核心主题
- 为内容分配到固定栏目
- 识别值得进入“主题深挖”的话题
- 将零散候选重组成可快速扫描的日报结构

不适合直接越权完成的任务：

- 擅自把内容判定为长期知识
- 用个人偏好覆盖公共重要性事件
- 在未确认结果质量前自动回写 FreshRSS 已读

## 本地目录约定

```text
openclaw-read-flow/
  execution-plan.md
  digests/
  reviews/
  skills/
```

关键目录：

- `digests/`：Digest 阶段产物
- `reviews/`：Daily Review 产物
- `skills/`：本地技能定义

## 推荐脚本入口

- 抓取未读：`../digest-builder/scripts/fetch_freshrss_unread.py`
- 昨天切片：`../digest-builder/scripts/slice_freshrss_by_date.py`
- 构建 Digest：`../digest-builder/scripts/build_digest.py`

## 输出要求

- 每次都明确当前阶段、输入、处理方式、产物
- 若上游产物缺失，优先补最小缺口，不强行继续下游
- 若涉及英文内容，必须输出中文摘要
- 若正文不可访问，必须显式标记，不假装完整阅读过

## 反例禁区

- 把原始标题列表直接包装成日报
- Digest 没去重就进入 Review
- Daily Review 不按 6 个固定栏目组织
- 自动把 FreshRSS 标记为已读
- 还没人工确认就直接写入长期知识库

## 参考文件

- 执行计划：`references/workflow.md`
