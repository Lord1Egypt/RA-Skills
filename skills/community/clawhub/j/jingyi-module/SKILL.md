---
name: jingyi-module
description: Help users use 精易模块 in 易语言. Search command names, fetch official docs, and generate directly runnable 易语言 code that the user can copy.
homepage: https://ec.ijingyi.com/sub.htm
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python"]},"homepage":"https://ec.ijingyi.com/sub.htm"}}
---

# Jingyi Module Skill

Use this skill when the user asks for:

- 精易模块应该用哪个命令
- 某个精易模块命令的参数、返回值、备注
- 一段可以直接复制运行的易语言代码

This skill is designed for retrieval first, then code generation.

## Goals

- Quickly find the most relevant 精易模块命令
- Pull the official command content by id or name
- Generate directly runnable 易语言 code
- Avoid inventing commands or parameters

## Workflow

1. Search candidate commands first
2. Fetch the full command doc for the best candidates
3. Write code only after confirming the signature and behavior
4. Prefer concise explanation plus one runnable code block

## Search commands

Run:

```powershell
python "{baseDir}/scripts/search_jingyi.py" "随机汉字" --top 8
```

Examples:

```powershell
python "{baseDir}/scripts/search_jingyi.py" "随机汉字" --top 8
python "{baseDir}/scripts/search_jingyi.py" "选择字体" --top 8
python "{baseDir}/scripts/search_jingyi.py" "取月末" --top 8
```

The result includes:

- `id`
- `name`
- `canonical_path`
- `cmdtype`
- `score`
- `summary`

## Fetch full command docs

Run:

```powershell
python "{baseDir}/scripts/fetch_jingyi_doc.py" --id 1109
```

or:

```powershell
python "{baseDir}/scripts/fetch_jingyi_doc.py" --name "文本_取随机汉字"
```

This returns the official document JSON. For three known official empty-response nodes, the script includes built-in补录 content:

- `时间_取月末`
- `文本_取随机汉字`
- `选择字体`

## Output rules

- Output runnable 易语言 code with `.版本 2` when code is requested
- Do not mention IDE automation
- Do not invent missing parameters or return types
- If there are multiple candidate commands, name the chosen command before the code
- When uncertain, keep the explanation to one short sentence

## Good response shape

One short paragraph:

- what command is being used
- why it matches the request

Then one code block:

```text
.版本 2
...
```

## Notes

- The local index is a compact retrieval index, not the full manual
- The fetch script uses the official endpoint:
  - `https://ec.ijingyi.com/plugin.php?id=plugin1&`
