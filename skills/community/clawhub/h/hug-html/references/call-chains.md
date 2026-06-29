# call-chains.md — hug-html 调用链定义

本文件定义 `hug-html` 技能的调用链，供 `skill-sub` 读取和执行。

---

## 调用链 1：generate-html（完整生成流程）

**描述**：从需求分析到输出最终 HTML 的完整流程

**触发方式**：`/hug-html generate --type <type> --output <path>`

**步骤**：

| 步骤 | 动作 | 调用脚本 | 输出 |
|------|-------|------|------|
| 1 | 解析需求 | （AI 理解用户意图） | 确定 `type`, `preset`, `modules` |
| 2 | 生成模板 | `template_generator.py --type <t> --output <o>` | `template.html` |
| 3 | 填充内容（可选） | `content_filler.py --auto --template <t> --output <o>` | `filled.html` |
| 4 | 应用样式预设（可选） | `content_filler.py --preset <p> --template <t> --output <o>` | `styled.html` |
| 5 | 生成编辑界面（可选） | `visual_editor.py --template <t> --output <o>` | `editor.html` |
| 6 | 组装模块（可选） | `module_assembler.py --modules <m> --output <o>` | `assembled.html` |
| 7 | 输出最终文件 | （复制到 `data/output/final.html`） | `final.html` |

**调用链 JSON**（`skill-sub` 格式）：

```json
{
  "name": "generate-html",
  "description": "从需求到最终 HTML 的完整生成流程",
  "steps": [
    {"step": 1, "action": "parse-requirement", "tool": "AI", "output": "type,preset,modules"},
    {"step": 2, "action": "generate-template", "script": "template_generator.py", "args": "--type {type} --output data/output/template.html"},
    {"step": 3, "action": "fill-content", "script": "content_filler.py", "args": "--auto --template data/output/template.html --output data/output/filled.html", "optional": true},
    {"step": 4, "action": "apply-preset", "script": "content_filler.py", "args": "--preset {preset} --template data/output/template.html --output data/output/styled.html", "optional": true},
    {"step": 5, "action": "generate-editor", "script": "visual_editor.py", "args": "--template data/output/template.html --output data/output/editor.html", "optional": true},
    {"step": 6, "action": "assemble-modules", "script": "module_assembler.py", "args": "--modules {modules} --output data/output/assembled.html", "optional": true},
    {"step": 7, "action": "finalize", "tool": "AI", "output": "data/output/final.html"}
  ]
}
```

---

## 调用链 2：edit-html（编辑流程）

**描述**：生成模板 → 生成编辑界面 → 用户编辑 → 导出最终 HTML

**触发方式**：`/hug-html edit --template <path>`

**步骤**：

| 步骤 | 动作 | 调用脚本 | 输出 |
|------|-------|------|------|
| 1 | 检查模板是否存在 | （AI 验证） | 模板路径 |
| 2 | 生成可视化编辑界面 | `visual_editor.py --template <t> --output <o>` | `editor.html` |
| 3 | 提示用户在浏览器中编辑 | （AI 输出提示） | 编辑说明 |
| 4 | 用户导出最终 HTML | （用户点击「生成最终 HTML」按钮） | `final.html` |
| 5 | 提取编辑后内容（可选） | `content_filler.py --extract <html> --output <json>` | `content.json` |

**调用链 JSON**：

```json
{
  "name": "edit-html",
  "description": "生成可视化编辑界面并导出最终 HTML",
  "steps": [
    {"step": 1, "action": "validate-template", "tool": "AI", "output": "template-path"},
    {"step": 2, "action": "generate-editor", "script": "visual_editor.py", "args": "--template {template} --output data/output/editor.html"},
    {"step": 3, "action": "prompt-user", "tool": "AI", "output": "edit-instructions"},
    {"step": 4, "action": "export-final", "tool": "user", "output": "final.html"},
    {"step": 5, "action": "extract-content", "script": "content_filler.py", "args": "--extract data/output/editor-output.html --output data/config/content.json", "optional": true}
  ]
}
```

---

## 调用链 3：assemble-with-modules（模块组装流程）

**描述**：选择模块 → 组装 → 填充内容 → 输出

**触发方式**：`/hug-html assemble --modules <csv>`

**步骤**：

| 步骤 | 动作 | 调用脚本 | 输出 |
|------|-------|------|------|
| 1 | 列出可用模块 | `module_assembler.py --list` | 模块列表 |
| 2 | 组装选定模块 | `module_assembler.py --modules <m> --output <o>` | `assembled.html` |
| 3 | 填充内容（可选） | `content_filler.py --template <t> --content <c> --output <o>` | `filled.html` |
| 4 | 生成编辑界面（可选） | `visual_editor.py --template <t> --output <o>` | `editor.html` |

**调用链 JSON**：

```json
{
  "name": "assemble-with-modules",
  "description": "选择模块并组装成完整 HTML",
  "steps": [
    {"step": 1, "action": "list-modules", "script": "module_assembler.py", "args": "--list"},
    {"step": 2, "action": "assemble", "script": "module_assembler.py", "args": "--modules {modules} --output data/output/assembled.html"},
    {"step": 3, "action": "fill-content", "script": "content_filler.py", "args": "--template data/output/assembled.html --content data/config/content.json --output data/output/filled.html", "optional": true},
    {"step": 4, "action": "generate-editor", "script": "visual_editor.py", "args": "--template data/output/assembled.html --output data/output/editor.html", "optional": true}
  ]
}
```

---

## 注册方式（skill-sub）

将以上 JSON 保存到 `data/config/call-chains.json`，或在 `skill-sub` 中注册：

```bash
python "$(SKILL_DIR)/../skill-sub/scripts/chain_manager.py" register --file "C:/Users/sm001/.workbuddy/skills/hug-html/data/config/call-chains.json"
```

---

## 调用示例

```bash
# 使用 generate-html 调用链
python "$(SKILL_DIR)/../skill-sub/scripts/chain_executor.py" run --chain generate-html --type promo --preset business

# 使用 edit-html 调用链
python "$(SKILL_DIR)/../skill-sub/scripts/chain_executor.py" run --chain edit-html --template "data/output/template.html"

# 使用 assemble-with-modules 调用链
python "$(SKILL_DIR)/../skill-sub/scripts/chain_executor.py" run --chain assemble-with-modules --modules "color:gradient-purple,font:title-large,image:img-cover"
```
