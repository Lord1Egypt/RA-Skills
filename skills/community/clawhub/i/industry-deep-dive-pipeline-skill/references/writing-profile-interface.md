# Writing Profile Interface

## Purpose

把个人或品牌写作规则留在私有 profile，通用 Skill 只读取标准字段。不得把历史文章、真实身份、公司资料或完整语料复制进公开包。

## Supported fields

```yaml
profile_version: "1.0"
language: zh-CN
scene: wechat_article | industry_report | linkedin_article | generic
thinking_model:
  - judgment_first
  - evidence_chain
  - boundary_conditions
language_tone:
  - calm
  - professional
  - non_marketing
negative_rules:
  literal_patterns: []
  semantic_rules: []
  max_em_dash: null
  forbid_meta_commentary: true
content_boundaries:
  private_materials: []
  forbidden_entities: []
  external_publication_requires_confirmation: true
output_preferences:
  target_length: null
  tables_preferred: true
  conclusion_style: restrained
```

## Runtime loading

1. 只读取与当前 scene 匹配的 `thinking_model`、`language_tone`、`negative_rules`、`content_boundaries` 和 `output_preferences`。
2. 不预加载完整语料、历史会话和全部个人画像。
3. profile 缺失时使用 generic：判断清楚、来源可追溯、禁止营销黑话和元信息。
4. profile 中的文字规则由 LLM 通读检查；可机械识别的 literal patterns 传给扫描脚本。

## WorkBuddy private profile example

运行个人/团队内容任务时，可按需读取由环境变量 `WRITING_PROFILE_PATH` 指向的私有画像文件（未设置则使用 generic 规则，不读取任何本机绝对路径）。示例结构参见私有画像 JSON。

从画像中只提取：

- `thinking_model`
- `language_tone`
- `task_specific_preferences`
- `negative_rules`
- `expression_style_profile` 中与正式内容有关的规则

不得复制到 Skill 目录、模板或回放报告。

## Public example profile

```yaml
profile_version: "1.0"
language: zh-CN
scene: industry_report
thinking_model:
  - judgment_first
  - evidence_chain
language_tone:
  - calm
  - professional
negative_rules:
  literal_patterns:
    - "本文将"
    - "颠覆性"
  semantic_rules:
    - "Do not instruct readers unless the task explicitly asks for advice."
  forbid_meta_commentary: true
content_boundaries:
  private_materials: []
  forbidden_entities: []
  external_publication_requires_confirmation: true
output_preferences:
  tables_preferred: true
  conclusion_style: restrained
```

## Security rules

- profile 文件保持在用户或项目私有目录。
- 公开 Skill 只包含字段说明和虚构示例。
- 扫描报告显示规则命中位置，不输出私有 profile 的完整内容。
- 外部发布前重新执行凭据、路径、身份和公司信息扫描。
