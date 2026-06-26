# Query types

## `course_schedule`
- 用途：查询课程表
- 状态：已支持按教师进入课表页查询；调用时应根据用户问题灵活组织返回，不要写死成固定模板

## `invigilation`
- 用途：考务安排查询 / 监考安排
- 菜单：考务成绩 → 考试事务 → 考务安排查询
- 结果页：内层 `fcenter` iframe

## `exam_course_arrangement`
- 用途：课程考试安排查询
- 菜单：考务成绩 → 考试事务 → 课程考试安排查询
- 结果页：内层 `fcenter` iframe

## `exam_info`
- 用途：考试信息查询
- 菜单：考务成绩 → 考试事务 → 考试信息查询
- 结果页：内层 `fcenter` iframe

## `exam_all`
- 用途：统一考试总查询
- 行为：顺序执行 `invigilation`、`exam_course_arrangement`、`exam_info`
- 输出：合并后的 `rows`，每行附带 `_query_type`

## Output conventions
- 标准输出：JSON
- 顶层字段：`query_type`, `teacher`, `term`, `count`, `rows`
- `exam_all` 额外带 `details`
- 无结果时返回 `count: 0` 与空数组，或结果表中的“未查询到数据”被解析为空数组
