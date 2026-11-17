# 课堂包 JSON 格式

`lesson.json` 使用 UTF-8 编码，顶层结构如下。额外字段可以保留，但以下字段为必填：

```json
{
  "title": "课程名称",
  "audience": "教学对象及先修知识",
  "duration_minutes": 45,
  "assumptions": ["本次采用的默认假设"],
  "objectives": ["学生能够……"],
  "agenda": [
    {
      "title": "环节名称",
      "minutes": 5,
      "teacher_action": "教师/Agent 的动作",
      "learner_action": "学生的动作",
      "check": "观察到什么算理解"
    }
  ],
  "slides": [
    {"title": "页面标题", "key_point": "核心信息", "teacher_notes": "讲解提示"}
  ],
  "activities": [
    {
      "title": "活动名称",
      "mode": "simulation",
      "instructions": "学生操作指令",
      "expected_observation": "预期观察",
      "discussion_questions": ["讨论问题"],
      "fallback": "没有工具时的替代方式"
    }
  ],
  "quiz": [
    {"question": "题干", "answer": "答案", "explanation": "解析", "next_step": "答错时的提示"}
  ],
  "homework": ["课后任务"]
}
```

`agenda[].minutes` 合计应等于 `duration_minutes`。`activities[].mode` 建议使用 `discussion`、`simulation`、`diagram`、`code`、`game` 或 `project`；未知类型也可以用清晰的自然语言描述。
