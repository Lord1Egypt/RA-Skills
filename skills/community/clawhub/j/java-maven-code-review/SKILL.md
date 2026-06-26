---
name: java-maven-code-review
description: Review a Java Maven project delivered as a ZIP archive or a GitLab repository URL for code规范, naming, module boundaries, maintainability problems, duplicated logic, structure issues, and整改建议. Use when the user asks for Java/Maven code review, 开发规范检查, 代码规范报告, or modification recommendations.
---

# Java Maven Code Review

Use this skill when the user wants a **代码规范检查报告** for a Java Maven project.

## Supported input
- Java Maven ZIP archive
- GitLab repository URL with user-authorized SSH access

## Goal
Inspect Java Maven projects for:
- 命名规范问题
- 模块边界不清
- 结构不合理
- 重复逻辑
- 可维护性问题
- 配置与资源文件中的规范风险

## Required output
Write a formal markdown report to `business/`.
Suggested filename:
`business/<project-name>-代码规范检查报告-YYYY-MM-DD.md`

## Minimum scan scope
- root `pom.xml`
- module `pom.xml`
- `src/main/java`
- `src/main/resources`
- optional `src/test/java`
- scripts / SQL / CI / Docker / deploy files

## Evidence rules
Each important finding should include file path, module, code/config evidence, impact, and modification advice when possible.

## Shared dependency

Use `java-maven-common` first when you need to normalize ZIP / GitLab input before review.

## Bundled resources
- `scripts/scan_code_review.py`
- `templates/report.md`
