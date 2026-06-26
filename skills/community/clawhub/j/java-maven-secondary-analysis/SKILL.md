---
name: java-maven-secondary-analysis
description: Analyze a Java Maven project delivered as a ZIP archive or a GitLab repository URL for secondary-development scope, class counts, module distribution, product customization traces, invasive modifications, and upgrade pollution risks. Use when the user asks for 二开分析, 二开范围识别, 模块分布统计, 产品二开信息, or a structured secondary-development report.
---

# Java Maven Secondary Analysis

Use this skill when the user wants a **二开分析报告** for a Java Maven project.

## Supported input
- Java Maven ZIP archive
- GitLab repository URL with user-authorized SSH access

## Goal
Inspect Java Maven projects for:
- 二开涉及多少类
- 模块分布
- controller/service/mapper/config 等层次分布
- 产品化 / 客户化 / 品牌化痕迹
- 侵入式改造和升级污染风险

## Required output
Write a formal markdown report to `business/`.
Suggested filename:
`business/<project-name>-二开分析报告-YYYY-MM-DD.md`

## Minimum scan scope
- root `pom.xml`
- module `pom.xml`
- `src/main/java`
- `src/main/resources`
- optional `src/test/java`
- scripts / SQL / CI / Docker / deploy files

## Evidence rules
Each important finding should include file path, module, layer/category, keyword/snippet evidence, and risk explanation when possible.

## Shared dependency

Use `java-maven-common` first when you need to normalize ZIP / GitLab input before analysis.

## Bundled resources
- `scripts/scan_secondary_analysis.py`
- `templates/report.md`
