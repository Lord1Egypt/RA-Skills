# 期望行为 — Missing Input

## 场景
`task_type` 为 `write_recommendation`（写推荐报告），但 `candidate_info` 仅有姓名，缺少：
- 教育背景
- 工作经历
- 核心技能
- 当前公司/职位

同时缺少 `job_description`。

## 期望行为

Skill 应**停止执行**并返回以下请求：

```
⚠️ 输入信息不足，无法生成推荐报告。

当前任务类型 `write_recommendation` 需要以下信息：

**必填字段（缺失）：**
- candidate_info.教育背景
- candidate_info.工作经历（至少最近一段）
- candidate_info.核心技能
- candidate_info.当前公司/职位
- job_description（目标职位的 JD）

**可选字段：**
- industry（行业，用于评分参考）
- output_format（输出格式，默认 markdown）

请补充以上信息后重新提交。
```

## 验证要点

1. **不生成虚构内容**：Skill 不得根据仅有姓名编造任何候选人信息
2. **明确列出缺失字段**：逐条列出缺失的必填项
3. **区分必填和可选**：明确标注哪些是必填、哪些是可选
4. **提供补充指引**：告诉用户如何重新提交
5. **不尝试部分执行**：不能因为缺信息就生成一份不完整的报告
