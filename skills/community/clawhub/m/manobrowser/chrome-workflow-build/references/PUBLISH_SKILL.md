# Skill发布到服务端指南

## 概述

本文档说明如何使用 `mcp__skills__create_workflow` tool 将生成的 Skill 发布到服务端。

**使用时机**：在 CREATOR.md 步骤7.2，检测到该 tool 可用时调用。

**前提条件**：
- Skill已成功生成在本地目录 `workflow-skills/[skill-name]/`
- 用户已确认Skill满意
- 已有 `workflow.json` 和 `SKILL.md` 文件

## Tool调用说明

### Tool名称
`mcp__skills__create_workflow`

### 必需参数

| 参数名 | 类型 | 说明 | 数据来源 |
|--------|------|------|---------|
| `name` | string | Skill标识名 | workflow.json的`name`字段 |
| `display_title` | string | 显示名称 | SKILL.md第一个`#`标题文本 |
| `description` | string | 功能描述 | workflow.json的`description`字段 |
| `skill_files` | array | 文件列表 | 读取SKILL.md、scripts/、references/下的所有文件 |
| `type` | string | Skill类型 | 从workflow最终步骤推断（见下文） |

### 可选参数

| 参数名 | 类型 | 说明 | 数据来源 |
|--------|------|------|---------|
| `icon` | string | emoji图标 | 可以根据生成 Skill 的意义自由发挥 |
| `metadata` | object | 元数据 | 可包含platform、version、参数数量、步骤数量等统计信息 |

## 参数构造要点

### 1. skill_files 数组构造

读取Skill目录下的所有文件，构造为数组：

```json
[
  {
    "filename": "SKILL.md",
    "content": "文件完整内容",
    "mime_type": "text/markdown"
  },
  {
    "filename": "scripts/validate_params.py",
    "content": "文件完整内容",
    "mime_type": "text/x-python"
  }
]
```

**关键点**：
- `filename`：相对于Skill根目录的路径（不包含`workflow-skills/[skill-name]/`前缀）
- `content`：使用Read工具读取的文件完整内容
- `mime_type`：根据文件扩展名映射（.md→text/markdown，.py→text/x-python）

**读取顺序**：

1. SKILL.md（必须）
2. scripts/*.py（如果存在）
3. references/*.md（如果存在）

### 2. type 字段推断

根据 Skill 的功能分析定位为以下三种之一

- data_acquisition: 数据获取
- operation_execution: 操作执行
- data_processing: 数据处理

## 调用示例

```python
# 1. 读取workflow.json
workflow = read_json(f"workflow-workflows/{skill_name}-workflow.json")

# 2. 读取SKILL.md并提取display_title（第一个# xxx）
skill_md_content = read_file(f"workflow-skills/{skill_name}/SKILL.md")
# 从SKILL.md中提取第一个以"# "开头的行，去掉"# "前缀即为display_title

# 3. 构造skill_files数组
skill_files = [
    {
        "filename": "SKILL.md",
        "content": skill_md_content,
        "mime_type": "text/markdown"
    }
]
# 使用Glob查找并读取scripts/*.py和references/*.md文件追加到数组

# 4. 推断type（分析workflow最终步骤）
type_value = "operation_execution"  # 或根据最终步骤推断

# 5. 调用tool
result = mcp__skills__create_workflow(
    name=workflow["name"],
    display_title=display_title,
    description=workflow["description"],
    skill_files=skill_files,
    type=type_value,
    icon="📕",  # 可选
    metadata={  # 可选
        "platform": workflow["platform"],
        "version": "1.0.0"
    }
)
```

## 成功/失败处理

### 发布成功

展示信息：
```
✅ Skill已发布到服务端！

📊 发布信息：
- Skill ID：{result["skill_id"]}
- 名称：{result["name"]}
- 显示名称：{result["display_title"]}
```

### 发布失败

展示信息：
```
⚠️ Skill发布到服务端失败

错误信息：{error_message}

Skill已成功保存在文件：
workflow-skills/{skill_name}/
```

## 重要提示

1. **非阻断性**：发布失败不应影响Skill的文件的生成使用
2. **文件保留**：发布成功后，本地文件仍然保留
3. **参数推断**：大部分参数可以从现有文件中分析提取
