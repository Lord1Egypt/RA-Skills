# 知识资产转化巧匠｜统一知识结构参考

## 1. 来源登记

```yaml
source_id: SRC-YYYYMMDD-序号
source_name: 原始文件或内容名称
source_type: qa | transcript | long_doc | unknown_source
source_path: 原始文件路径或外部来源标识
source_author: 作者或说话人
source_date: 来源时间
source_version: 来源版本
source_hash: 可取得时填写
processing_batch: 处理批次
status: draft | pending_review | published | superseded | rolled_back
```

## 2. 知识条目

```yaml
id: KA-模块-序号
source_id: SRC-YYYYMMDD-序号
source_type: qa | transcript | long_doc | unknown_source
source_span: 页码、段落、时间段、问答编号或章节路径
module: 业务模块
intent: 用户要解决的意图
question: 用户可能提出的问题
retrieval_text: 面向召回的短文本，默认不超过80字
answer_text: 面向下游回答的完整文本
aliases: [口语说法, 同义词]
tags:
  stage: 问题或流程阶段
  content_type: 内容类型
  symptom: 用户现象
  action: 建议动作
  scope: 适用范围
evidence: 原文依据和证据说明
negative_scope: 不能套用的情况
status: confirmed | transferable | ask_teacher | conflict | pending_review
priority: high | normal | pending
version: v1
related_ids: []
conflict_ids: []
```

## 3. 状态使用规则

- `confirmed`：原文有明确依据，适用范围清楚，可发布。
- `transferable`：与目标问题相近但不是完全对应，允许有限参考，回答时需说明边界。
- `ask_teacher`：资料不足或需要领域负责人判断，不能当作确认答案。
- `conflict`：与其他条目冲突，保留双方证据，等待审核。
- `pending_review`：已抽取但来源、术语、范围或事实仍需审核。

## 4. 关系记录

```yaml
relation:
  from_id: KA-模块-序号
  relation_type: related | refines | derived_from | contradicts | supersedes | duplicate_of
  to_id: KA-模块-序号
  reason: 建立关系的依据
  source_span: 关系依据所在位置
```

## 5. 双视图交付规范

### 5.1 单一事实源

JSONL 是知识资产的机器主数据；Markdown 是由 JSONL 自动生成的人工审核视图。两者不得独立维护。

```text
结构化知识主数据
  └── knowledge_assets.jsonl  ← 权威来源
        └── knowledge_assets.md ← 自动生成、供人审核
```

每个批次必须绑定同一组：

```yaml
batch_id: BATCH-YYYYMMDD-序号
version: v1.0
source_manifest: source_manifest.json
primary_data: knowledge_assets.jsonl
human_view: knowledge_assets.md
generated_from: knowledge_assets.jsonl
generator_version: 知识资产化巧匠-vX.Y
```

### 5.2 Markdown 派生视图固定结构

```markdown
# 知识资产审核视图｜批次与版本

## 1. 批次概览
来源、处理日期、版本、条目数、发布状态

## 2. 模块目录
模块、条目数、待审核数

## 3. 知识条目
每条按以下顺序展示：
ID → 问题 → 检索文本 → 回答 → 标签 → 适用范围 → 不能外推 → 来源 → 状态 → 关系

## 4. 冲突与待审核
conflict / pending_review / ask_teacher 条目不能隐藏

## 5. 质量检查与变更记录
字段检查、来源抽样、检索评测、相对上一版的变更
```

### 5.3 生成、审核、回写

1. 先写入或更新 JSONL 主数据，再从 JSONL 生成 Markdown；
2. 人工在 Markdown 中发现问题时，记录条目 ID 和问题类型；
3. 回写 JSONL 后重新生成 Markdown，不允许直接手改 Markdown 作为最终版本；
4. 重新生成后做双向一致性检查：JSONL 的每个 ID 在 Markdown 中出现一次，Markdown 不得出现 JSONL 没有的 ID；
5. 条目数、ID、版本、状态、问题、检索文本、回答文本、模块必须一致；
6. 失败时输出差异报告，暂停发布，不能用旧 Markdown 冒充新版本。

### 5.4 双视图质量规则

- JSONL 负责机器质量：可解析、每行一条、字段完整、ID 唯一、状态可过滤、检索字段可用于召回；
- Markdown 负责人类质量：结构清楚、可读、来源和边界可见、冲突和待审核内容不被折叠隐藏；
- Markdown 的格式美化不得改变 JSONL 的事实内容；
- 任一视图发生变化，都必须在版本记录中标注变更原因、操作者、时间和影响条目；
- 只有 JSONL 通过校验且 Markdown 同步通过一致性检查，才可交付完整批次。

## 6. 批次交付清单

```text
[ ] 来源清单及读取范围
[ ] 处理批次与版本号
[ ] 统一知识索引
[ ] 标签字典与关系字典
[ ] 新增/补充/修正/冲突/待确认统计
[ ] 来源追溯抽样结果
[ ] 去重与冲突检查结果
[ ] 检索评测集与 top-1/top-3 结果
[ ] 无答案误答检查
[ ] 旧问题回归结果
[ ] 未解决问题与问老师清单
[ ] 回滚点和下游接入说明
```
