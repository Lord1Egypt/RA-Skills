# Artifact Spec

Artifact generation is a downstream subsystem. It should only start after structured data already exists.

## Supported artifact kinds

### `.docx`

- 家访记录
- 班级通知
- 学生谈话记录

### `.xlsx`

- 座位表
- 值日表
- 班委表
- 扣分汇总表

### `.pptx`

- 家长会 PPT

These artifacts belong to two main generation families:

1. arrangement artifacts
   - seat plans
   - duty schedules
   - committee tables
2. presentation or communication artifacts
   - parent meeting slides
   - notices
   - visit records
   - student talk records

## Template policy

- Do not keep real `.docx`, `.xlsx`, or `.pptx` files inside the published skill directory.
- Existing Office files may be used only as temporary local references when extracting structure or outline.
- The skill should preserve reusable outlines, field mappings, and generation rules as text documentation, not as bundled Office assets.

## Artifact request contract

An artifact request should include:

- `artifact_type`
- `template_name` or template source
- `context_ref`
- `output_path`
- `sync_policy`

For arrangement artifacts, also include:

- `arrangement_constraints`
- `priority_attributes`

Examples of useful arrangement attributes:

- score
- gender
- height
- dorm or group
- conduct constraints

## Parent meeting PPT outline

When generating a 家长会 PPT in v1, prefer a text-defined outline instead of a bundled `.pptx` template.

Its data sources should come from both:

- score records
- daily performance or growth records

Suggested default outline:

1. 封面：时间、班级、家校协同主题
2. 教师与班级概况：任课教师、班级人数、班级基本面
3. 班级组织与文化：班委、科代表、班级文化建设
4. 班级运行现状：纪律、宿舍、作业、卫生、待改进点
5. 考试与成绩：阶段考试结果、学科表现、成绩表彰
6. 学习方法建议：学习兴趣、学习策略、考试观
7. 给家长的建议：家校协同、沟通方式、支持策略
8. 学科教师建议：可选附录部分

This outline may be adapted from prior local materials, but the Office source file itself should not be retained in the repository.

## Registry rules

Every generated artifact should be recorded with:

- title
- type
- related entity
- local path
- timestamp
- optional remote URL
- sync status
- parameter summary

## Guardrails

- refuse to fabricate structured data that does not exist
- call out missing templates explicitly
- do not sync externally unless the user asks for it
