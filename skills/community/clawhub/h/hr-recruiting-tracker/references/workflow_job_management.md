# 岗位信息管理工作流 (job-management)

将岗位信息维护到固定的腾讯文档智能表格，供后续候选人-岗位匹配、进度查询和面试流程判断使用。

## 目录

- 统一数据模型
- 岗位表字段
- 前置条件
- 初始化和维护岗位表
- 岗位记录 JSON 格式
- 测试数据规则
- 实测限制
- 预期回复

## 统一数据模型

所有招聘表模型统一维护在：

```text
assets/schemas/recruiting_tables.json
```

当前包含：

- `candidates`：候选人核心信息表，固定智能表格名 `HR候选人库`
- `jobs`：岗位信息表，固定智能表格名 `HR岗位信息库`

脚本必须从该文件读取字段定义，不要在 workflow 中临时拼字段。

## 岗位表字段

岗位表固定表名：`HR岗位信息库`

| 字段 | 说明 |
|------|------|
| job_id | 岗位唯一标识 |
| job_title | 岗位名称 |
| department | 部门 |
| hiring_manager | 用人经理 |
| must_have | 必须条件 |
| nice_to_have | 加分条件 |
| responsibilities | 工作职责 |
| level | 职级 |
| location | 地点 |
| salary_range | 薪资范围 |
| interview_process | 面试流程 |
| status | 开放/暂停/关闭 |
| updated_at | 岗位记录更新时间 |

`job_id` 和 `updated_at` 是系统管理字段。其余字段来自业务岗位信息。

## 前置条件

与 `candidate-upload` 相同：

1. 已安装 `tencent-docs` skill
2. 已安装 `mcporter`
3. 已完成腾讯文档授权

检查：

```bash
python3 {baseDir}/scripts/dependency_check.py --workflow job-management
python3 {baseDir}/scripts/dependency_check.py --workflow job-management --probe-remote
```

如需授权排障，且已安装并审阅 `tencent-docs` skill，使用：

```bash
export TENCENT_DOCS_SKILL_DIR="${TENCENT_DOCS_SKILL_DIR:-$HOME/.openclaw/workspace/skills/tencent-docs}"
bash "$TENCENT_DOCS_SKILL_DIR/setup.sh" tdoc_check_and_start_auth
```

## 初始化和维护岗位表

默认行为：

1. 按固定表名 `HR岗位信息库` 搜索已有智能表格。
2. 若找到同名表，则复用。
3. 若未找到，则创建新智能表格。
4. 确保岗位字段存在。
5. 清理新建表的默认空行和默认列。
6. 未显式传入岗位记录文件时，不写入任何岗位数据。

命令：

```bash
python3 {baseDir}/scripts/manage_jobs.py
```

导入真实岗位记录：

```bash
python3 {baseDir}/scripts/manage_jobs.py --records-json "/path/to/jobs.json"
```

导入时按 `job_id` 去重，重复运行不会重复追加相同岗位。

指定已有岗位表：

```bash
python3 {baseDir}/scripts/manage_jobs.py --file-id "your_file_id"
```

在知识库空间内创建：

```bash
python3 {baseDir}/scripts/manage_jobs.py --space-id "your_space_id"
```

预览模式：

```bash
python3 {baseDir}/scripts/manage_jobs.py --dry-run
```

预览真实岗位记录导入：

```bash
python3 {baseDir}/scripts/manage_jobs.py --records-json "/path/to/jobs.json" --dry-run
```

## 岗位记录 JSON 格式

岗位记录文件必须是数组，或包含 `jobs` 数组的对象。

```json
[
  {
    "job_id": "JOB-001",
    "job_title": "Agent 开发工程师",
    "department": "AI平台部",
    "hiring_manager": "王经理",
    "must_have": "Python；LLM 应用开发；工具调用经验",
    "nice_to_have": "MCP、RAG、OpenClaw 经验",
    "responsibilities": "开发和维护企业内部 Agent 工作流",
    "level": "P5-P6",
    "location": "深圳",
    "salary_range": "20k-35k * 14",
    "interview_process": "HR初筛 -> 技术一面 -> 主管面",
    "status": "开放"
  }
]
```

## 测试数据规则

本 skill 不内置测试岗位数据，也不会默认写入测试岗位。

如需测试，请在测试用临时 JSON 文件中构造样例岗位，并通过 `--records-json` 显式导入；测试完成后自行清理测试文档或测试记录。

## 实测限制

- `tencent-docs` 1.0.33 新建 `singleSelect/select` 字段可能返回 `22020: Smartsheet invalid select field`，所以 `status` 暂用文本字段保存。
- 如果 HR 后续手动把 `status` 转成单选字段，脚本会检测字段类型冲突并停止，避免误写。

## 预期回复

成功后回复：

- 固定岗位表名
- 腾讯文档链接
- `file_id`
- `sheet_id`
- 新写入的岗位记录数，如果传入了 `--records-json`
- 跳过的重复 `job_id`
