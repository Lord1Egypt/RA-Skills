---
name: project_analyzer
description: Analyze any project directory and produce a detailed report covering what the project does, its tech stack, folder structure, entry points, how to run it, and where to start reading.
homepage: https://clawhub.ai
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["python3"]},"install":[{"id":"brew","kind":"brew","formula":"python3","bins":["python3"],"label":"Install Python 3 (brew)","os":["darwin"]},{"id":"apt","kind":"download","url":"https://www.python.org/downloads/","label":"Install Python 3 from python.org","os":["linux","win32"]}]}}
---

# Project Scout

Use this skill whenever the user wants to understand, explore, or get oriented inside a codebase or project folder. Trigger phrases include:

- "analyze this project"
- "what does this project do"
- "I'm new to this codebase, where do I start"
- "give me an overview of [directory]"
- "explain the structure of my project"
- "scan the project"
- "project report"
- `/scout` (slash command)

## What you must do

When this skill is triggered:

1. **Identify the target directory.** Use the path the user mentions. If none is given, use the current working directory (run `pwd` to confirm it).

2. **Run the scout script** using the `exec` tool:

```
python3 {baseDir}/scout.py --path <DIRECTORY>
```

Replace `<DIRECTORY>` with the resolved absolute path. Always use `--path` explicitly.

3. **Present the output** as a clean, readable message to the user. Structure it with clear sections. Do not just dump raw text — format it nicely for the chat channel being used.

4. **Offer next steps.** After presenting the report, ask if the user wants to:
   - Dive deeper into any specific file or module
   - Get a dependency graph
   - Find the entry point and trace the execution flow
   - Generate a CLAUDE.md / README for the project

## Handling errors

- If `python3` is not found: tell the user to install Python 3 and point them to https://www.python.org/downloads/
- If the path doesn't exist: ask the user to double-check the path and try again
- If the directory is empty or has very few files: report what was found and note it may be a new/empty project
- If the output is very long: summarize the key sections and offer to elaborate on any part

## Slash command

This skill is available as `/scout [path]`. Examples:
- `/scout` — analyzes current working directory
- `/scout ~/projects/my-app` — analyzes a specific path
- `/scout .` — explicit current directory

## Output format

Structure your reply like this:

```
🔍 **Project Scout Report**
📁 *<project name> — <one-line summary>*

**What it does**
<plain English explanation>

**Tech stack**
<languages, frameworks, key libraries>

**Structure**
<brief tour of the important folders and files>

**Where to start**
<the 2-3 files a new dev should read first>

**How to run it**
<install/build/run commands if found>

**Notes**
<anything unusual, TODOs, missing docs, etc.>
```

Keep it conversational and useful. This is meant to orient a developer, not just dump data.
