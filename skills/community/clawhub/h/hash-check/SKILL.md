---
name: hash-check
description: 文件哈希校验 — 生成/校验目录 SHA-256 清单：下载验 integrity、传输前后比对、防篡改留证（零依赖） 适用场景：当需要文件哈希校验能力时使用本技能；触发词：hash-check。
slug: hash-check
version: 1.0.1
display_name: 文件哈希校验
display_name_en: File Hash Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
description_zh: "文件哈希校验 — 生成/校验目录 SHA-256 清单：下载验 integrity、传输前后比对、防篡改留证（零依赖）"
description_en: "Generate and verify SHA-256 manifests for directories: download integrity, before/after transfer comparison and tamper-evident records (zero-dependency)."
classification:
  skillhub: ["productivity"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [hash-check, 效率工具, SHA-256, 完整性校验]
read_when:
  - 下载/传输/上传完成后要校验数据是否比特翻转、损坏或被篡改
  - 要生成独立完整性清单（Manifest）作分发凭证供客户端二次比对
  - 版本控制/备份恢复/多方协作要记录文件指纹确保持续一致
  - 用户说「这个文件有没有被改」「验一下下载完整性」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/hash_check.py
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
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
1. After a file download, transfer or upload, to verify that no bit-rot, corruption or tampering occurred.
2. When an independent integrity manifest must be generated as a distribution credential for later client-side re-verification.
3. In version control, backup/restore or multi-party collaboration, when file fingerprints must be recorded to ensure ongoing consistency and keep audit evidence.

### Usage
1. Run the Python script from the command line: `python hash_check.py` — zero-dependency.
2. Core parameters: `--input` (file or directory path) and `--action` (mode: check / generate / compare).
3. To batch-check a directory, pass the full path and set the output to JSON to fit automated pipelines.

### Workflow
1. Initialize the script runtime; confirm the Python environment and stdlib (e.g. hashlib) are healthy.
2. Upload or point at the local target file/directory; ensure read/write permissions and correct paths.
3. Start the compute module: walk the directory or read the single file, hashing block by block and aggregating into a SHA-256 value.
4. The script auto-compares against the provided hashes (if expected values are configured) and returns a pass/fail status code to the console.
5. Save the verification result to a log file or the designated JSON output location, forming a tamper-evident credential record.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 在文件下载、传输或上传完成后，用于校验数据是否发生比特翻转、损坏或被人为篡改。
2. 当需要生成一份独立的完整性清单（Manifest）作为分发凭证时，用于后续客户端二次比对验证。
3. 在进行版本控制、系统备份恢复或多方协作场景下，需记录文件指纹以确保持续一致性并保留审计证据。

### 用法
1. 直接通过命令行执行 Python 脚本，主要命令格式为 `python hash_check.py`，支持无依赖运行。
2. 核心参数包括 `--input`（指定输入文件或目录路径）和 `--action`（校验模式：check/generate/compare）。
3. 若需要批量校验目录结构，需传入完整路径并配置输出格式为 JSON 以适配自动化流程。

### 流程
1. 初始化脚本环境，确认当前 Python 运行环境与依赖库（如 hashlib）状态正常。
2. 上传或指定本地目标文件/目录，确保输入源权限可读写且路径无误。
3. 启动计算模块，遍历目录结构或读取单个文件并逐块哈希聚合生成 SHA-256 值。
4. 脚本自动比对双方提供的哈希值（如配置了预期值），并在控制台返回通过或失败状态码。
5. 将验证结果保存至日志文件或指定 JSON 输出位置，形成不可篡改的凭证留存记录。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
