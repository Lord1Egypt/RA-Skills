# 营销助手数字员工

> 版本：2026-05-26  
> 部署建议：电脑3，飞书入口“小宣”，Hermes Agent 员工 ID：`marketing_assistant`

## 1. 员工定位

通过飞书接收主题、素材和传播需求，调用 Hermes Agent skills 完成选题策划、海报文案、公众号初稿、短视频脚本、活动方案、发布包和营销复盘。

## 2. 场景包与子角色

| 场景包 | 子角色/责任位 | 目标 | 关键 skills |
| --- | --- | --- | --- |
| 选题策划 | 内容策划员 | 根据产品、活动、热点和目标人群生成选题、标题和传播角度。 | M01_topic_planning, M07_material_tagging |
| 海报物料 | 视觉文案员 | 生成海报主标题、副标题、卖点、行动号召和设计提示。 | M02_poster_copy_generate, M07_material_tagging |
| 公众号内容 | 图文编辑员 | 生成公众号标题、结构、正文初稿、摘要和配图建议。 | M03_wechat_article_draft, M01_topic_planning |
| 短视频脚本 | 视频编导员 | 生成口播稿、分镜、字幕、镜头建议和拍摄清单。 | M04_short_video_script, M07_material_tagging |
| 活动策划 | 活动策划员 | 生成活动目标、流程、物料、节奏、分工和预算提示。 | M05_campaign_plan_generate, M06_multi_platform_publish_pack |
| 发布包生成 | 新媒体运营员 | 生成公众号、朋友圈、视频号等平台发布文案和标签。 | M06_multi_platform_publish_pack, M02_poster_copy_generate |
| 运营复盘 | 数据复盘员 | 根据阅读、转发、线索和互动数据生成复盘结论。 | M08_marketing_data_review, M01_topic_planning |

## 3. 领域 skills

| Skill ID | 名称 | 用途 | 主要输出 |
| --- | --- | --- | --- |
| M01_topic_planning | 选题策划 | 根据主题、产品、活动、热点和目标人群生成选题、传播角度、标题和内容矩阵。 | topic_list, angle_matrix, title_options, content_calendar |
| M02_poster_copy_generate | 海报文案生成 | 生成海报主标题、副标题、核心卖点、行动号召和设计提示。 | poster_headlines, poster_copy, cta, design_notes |
| M03_wechat_article_draft | 公众号初稿生成 | 生成公众号标题、文章结构、正文初稿、摘要和配图建议。 | article_titles, article_outline, article_draft, summary, image_suggestions |
| M04_short_video_script | 短视频脚本生成 | 生成短视频口播、分镜、字幕、镜头建议和拍摄物料清单。 | script, storyboard, subtitles, shot_list, material_list |
| M05_campaign_plan_generate | 活动方案生成 | 生成活动目标、流程、执行节奏、物料清单、预算提示和分工建议。 | campaign_plan, task_table, material_list, risk_notes |
| M06_multi_platform_publish_pack | 多平台发布包生成 | 按平台生成标题、正文、标签、封面建议、发布时间和差异化口径。 | publish_pack, platform_variants, tag_list, schedule_suggestion |
| M07_material_tagging | 素材整理与标签 | 对图片、案例、视频和产品资料进行分类、标签化和可复用摘要。 | tagged_materials, reusable_summary, missing_materials |
| M08_marketing_data_review | 营销数据复盘 | 根据阅读、转发、互动、线索等数据输出复盘、归因和优化建议。 | review_report, insight_list, next_actions |

## 4. 关键边界

- 可以生成草稿、建议、清单、摘要、风险提示和归档记录。
- 涉及对外发布、品牌承诺、客户案例引用、数据口径、引用第三方材料时必须人工确认。
- 演示样例必须使用脱敏或虚拟数据，不使用真实客户、员工、财务、合同或技术敏感信息。
- 所有 Hermes Agent skill 调用需要记录输入、输出、确认人和归档位置。

## 5. 文件结构

```text
marketing-assistant/
  README.md
  employee.yaml
  system_prompt.md
  workflows.md
  runbook.md
  skills/
  knowledge/
  templates/
  test_cases/
  demo/
```
