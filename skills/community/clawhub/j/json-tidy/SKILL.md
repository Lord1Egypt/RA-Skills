---
name: json-tidy
description: JSON 整形器 — JSON 格式化/压缩/键排序，解析错误精确定位行列，管道可用（零依赖） 适用场景：当需要JSON 整形器能力时使用本技能；触发词：json-tidy。
slug: json-tidy
version: 1.0.5
display_name: JSON 整形器
display_name_en: JSON Tidy
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "JSON 整形器 — JSON 格式化/压缩/键排序，解析错误精确定位行列，管道可用（零依赖）"
description_en: "JSON formatter, minifier and key-sorter with precise line-column error locating; pipe-friendly (zero-dependency)."
classification:
  skillhub: ["productivity"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [json-tidy, 效率工具, JSON, 格式化]
read_when:
  - 输入 JSON 格式混乱/多余空白/键名无序要标准化整理
  - 数据管道里要零依赖处理 JSON（无法装外部工具）
  - JSON 解析报错要精确定位行列而非笼统 invalid 提示
  - 用户说「把这段 JSON 排一下版」「压缩成一行」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/json_tidy.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见各包 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=PASS/完成；1=FAIL/有警告或待补强；2=用法或参数错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.5: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
- When input JSON is messy, padded with stray whitespace or has unsorted keys, and needs standardizing for readability.
- When JSON content moves through a data pipeline with a restricted environment where external tools cannot be installed (zero-dependency runtime).
- When a JSON parse error occurs and you need the exact line and column of the error instead of a vague "invalid" message.

### Usage
- **Command**: run `python json_tidy.py [options]` to start the main script.
- **Input**: read directly from stdin, or specify a file path as the data source.
- **Parameters**: `--format` picks compact or pretty mode, `--sort-keys` enables key sorting, `--loc-error` prints detailed line/column location.

### Workflow
1. Confirm the input file format; ensure the content is a valid JSON fragment or a full document.
2. Invoke the appropriate python interpreter to load `json_tidy.py` and set the format options.
3. Pipe the data in, or point at the file path, and run the conversion.
4. The system parses and formats the data, also flagging the line/column of any syntax error.
5. Take the standardized JSON output and verify it meets the expected formatting or minification goal.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.5
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
- 当输入 JSON 数据格式混乱、包含多余空白或键名无序，需要标准化整理以提升可读性时。
- 在数据处理管道中处理 JSON 内容，且环境受限无法安装外部依赖工具以保证零依赖运行时时。
- 遇到 JSON 解析异常，需要通过精确的行号与列号定位错误位置而非笼统报错信息时。

### 用法
- **调用命令**：执行 `python json_tidy.py [选项]` 启动主脚本处理逻辑。
- **输入方式**：支持从标准输入（stdin）直接读取或指定文件路径作为数据源。
- **参数配置**：主要包含 `--format` 指定压缩或美观模式、`--sort-keys` 开启键名排序及 `--loc-error` 输出详细行列定位。

### 流程
1. 确认待处理的数据文件格式，确保其内容为有效的 JSON 结构片段或完整文档。
2. 根据实际需求在命令行中调用对应版本的 python 解释器加载 `json_tidy.py` 并配置格式选项参数。
3. 将数据输入标准管道或直接指定文件路径启动脚本执行命令转换。
4. 系统自动解析并格式化数据，同时检查潜在的语法错误行号与列号。
5. 获取处理后的标准化 JSON 输出并验证其是否符合预期规范或压缩目标。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.5
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
