<!-- wm:坤图_GIS:V5.0 -->

# GeoEvolve 子模块: 反馈采集层

> 全局唯一知识ID: GIS-EVO-001
> 隶属: 顶层GeoEvolve自进化闭环

## 功能

自动解析用户反馈日志，识别：
- 报错信息 → 提取错误码+触发条件
- 知识缺口 → 标记为缺失知识点
- 精度不足 → 触发改进流程
- 新需求 → 生成新模块创建任务

## 输入源

| 来源 | 格式 | 触发频率 |
|------|------|----------|
| feedback/feedback_log.md | Markdown | 每次会话结束 |
| knowledge_gaps.md | Markdown | 实时 |
| 任务执行日志 | JSON | 每次任务 |
| 原子Skill报错 | Exception | 实时 |

## 输出

- 分类归因后的知识缺口报告
- 推送至 knowledge_fixer 子模块
