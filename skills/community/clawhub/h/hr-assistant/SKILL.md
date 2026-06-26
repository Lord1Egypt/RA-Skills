---
name: hr-assistant
version: 1.2.5
author: ai-lab-hr
description: |
  Smart HR Assistant for Chinese small and medium businesses. Handles employee roster management,
  organizational structure, monthly payroll calculation (individual income tax, social insurance,
  housing fund, special deductions), year-end bonus tax optimization, attendance tracking with
  automatic deductions, and HR report generation. All data is stored locally in Excel and JSON files.
  Suitable for HR topics such as employee onboarding, resignation, promotion, transfer, salary adjustment,
  department management, attendance records, and payroll reports.
description_zh: |
  智能HR助手 — 专为中国中小企业设计。支持员工花名册管理、组织架构维护、考勤管理与自动扣减、
  月度薪资自动计算（个税累计预扣法/社保/公积金/专项附加扣除）、年终奖个税优化、
  HR报表生成与导出。数据全部本地存储，不上云，Excel一键绑定，5分钟完成初始化。
keywords:
  - hr
  - 人力资源
  - HR管理
  - 员工管理
  - 花名册
  - 薪资计算
  - 工资计算
  - 个税计算
  - 累计预扣法
  - 社保计算
  - 公积金计算
  - 五险一金
  - 年终奖
  - 年终奖个税
  - 薪酬
  - 考勤管理
  - 考勤扣款
  - 组织架构
  - 部门管理
  - 入职
  - 离职
  - 转正
  - 调岗
  - 调薪
  - 人力报表
  - 合同到期
  - Excel
  - 中小企业
  - payroll
  - employee management
  - attendance
  - salary
  - tax
  - social insurance
  - housing fund
description_en: "Smart HR Assistant for Chinese SMEs — Employee management, attendance, payroll & tax optimization"
license: MIT
runtime: python:3.8
permissions:
  - filesystem:read
  - filesystem:write
tags:
  - hr
  - payroll
  - employee-management
  - attendance
  - tax
  - business
  - chinese
  - 人力资源
  - 薪资
  - 工资
  - 个税
  - 社保
  - 公积金
  - 五险一金
  - 年终奖
  - 考勤
  - 花名册
  - 中小企业
  - Excel
  - 组织架构
metadata:
  category: business
  emoji: 👔
  requires:
    bins: [python3]
    packages:
      - openpyxl>=3.0
      - xlrd>=2.0
---

# 👔 HR助手

智能 HR 助手，支持员工花名册管理、组织架构维护、薪资自动计算（个税/社保/公积金）、年终奖优化与报表生成。

## 重要说明

**所有数据存储在用户本地，不上云。** 用户上传 Excel 文件后，系统会自动分析表格结构并识别列映射。

## 核心调用方式

### 自然语言模式（推荐）

```bash
python3 {{baseDir}}/tools/main.py "<用户自然语言指令>"
```

脚本内部会自动完成：意图识别 → 参数提取 → 工具执行 → 响应格式化。

```bash
# 查看帮助
python3 {{baseDir}}/tools/main.py "帮助"

# 查看当前配置状态
python3 {{baseDir}}/tools/main.py "查看配置"

# 查询员工
python3 {{baseDir}}/tools/main.py "查一下张三的信息"
python3 {{baseDir}}/tools/main.py "技术部有哪些员工"

# 员工统计
python3 {{baseDir}}/tools/main.py "员工统计"

# 薪资计算
python3 {{baseDir}}/tools/main.py "计算本月薪资"
python3 {{baseDir}}/tools/main.py "年终奖36000"

# 社保公积金计算（不需要绑定表格）
python3 {{baseDir}}/tools/main.py "北京社保10000"
python3 {{baseDir}}/tools/main.py "上海五险一金15000"
```

### 子命令模式（精确操作）

```bash
# 查看配置状态
python3 {{baseDir}}/tools/main.py status

# 绑定表格（分析 + 自动映射 + 绑定 一步完成）
python3 {{baseDir}}/tools/main.py bind organization /path/to/org.xlsx
python3 {{baseDir}}/tools/main.py bind employee /path/to/employee.xlsx
python3 {{baseDir}}/tools/main.py bind salary /path/to/salary.xlsx

# 仅分析表格结构（不绑定）
python3 {{baseDir}}/tools/main.py analyze /path/to/file.xlsx [sheet_name]
```

---

## 初始化流程（核心）

### ⚡ 关键设计：直接读取用户上传的文件

**当用户说「开始初始化」或上传了 Excel 文件时：**

1. 先运行 `python3 {{baseDir}}/tools/main.py status` 查看当前状态
2. 如果未选择存储方式，引导用户使用 Excel 本地存储（默认）
3. 然后引导用户依次上传三张表：
   - 「请上传你的**组织架构** Excel 文件」
   - 「请上传你的**员工花名册** Excel 文件」
   - 「请上传你的**薪资表** Excel 文件」

4. **当用户上传文件后**，使用上传后的文件路径执行绑定：

```bash
# 绑定组织架构表
python3 {{baseDir}}/tools/main.py bind organization "<上传文件路径>"

# 绑定员工花名册
python3 {{baseDir}}/tools/main.py bind employee "<上传文件路径>"

# 绑定薪资表
python3 {{baseDir}}/tools/main.py bind salary "<上传文件路径>"
```

> **安全提示**：仅接受用户主动上传的文件路径，不要读取或处理非 Excel 文件。

5. 脚本会自动完成：读取 Excel → 分析列名 → 匹配标准字段 → 完成绑定
6. 三张表全部绑定后，初始化完成，可以直接使用

### 用户可能一次上传多个文件

如果用户一次上传了多个 Excel 文件：
- 先读取每个文件的内容，根据列名判断是组织架构/花名册/薪资表
- 按 `bind <type> <path>` 依次绑定
- 如果无法自动判断，询问用户哪个文件对应什么

### 列映射说明

`bind` 命令会自动识别常见列名别名，包括：

| 标准字段 | 常见列名 |
|---------|---------|
| 工号 (empNo) | 工号、员工编号、员工ID、编号 |
| 姓名 (name) | 姓名、员工姓名、名字 |
| 部门 (deptCode) | 部门编码、部门ID、所属部门 |
| 基本工资 (baseSalary) | 基本工资、底薪、基础工资 |
| 入职日期 (hireDate) | 入职日期、入职时间、到岗日期 |
| 在职状态 (status) | 在职状态、状态、员工状态 |

如果自动匹配有误，系统会提示用户确认。

---

## 功能清单

### 员工管理

| 操作 | 示例指令 |
|------|----------|
| 查询员工 | 「查一下张三的信息」「E001的信息」 |
| 员工列表 | 「所有员工」「花名册」「在职多少人」 |
| 搜索筛选 | 「技术部员工」「试用期员工」「姓李的」 |
| 添加员工 | 「添加员工 E020 王五 技术部 工程师」 |
| 修改员工 | 「张三转正」「李四调到市场部」「E003调薪到20000」 |
| 删除员工 | 「E010离职」「删除E020」 |
| 批量操作 | 「E001到E010批量转正」 |

### 组织架构

| 操作 | 示例指令 |
|------|----------|
| 查看部门 | 「组织架构」「有哪些部门」「技术部信息」 |
| 部门树 | 「部门树」「组织架构图」 |
| 汇报关系 | 「张三的汇报链」「张三向谁汇报」 |

### 薪资计算

| 操作 | 示例指令 |
|------|----------|
| 批量薪资 | 「计算本月薪资」「跑工资」「算2月工资」 |
| 单人薪资 | 「算一下张三的工资」 |
| 年终奖 | 「年终奖36000」「年终奖50000月薪2万」 |
| 社保公积金 | 「北京社保10000」「上海五险一金15000」 |
| 个税税率 | 「个税税率」「税率表」 |

### 报表与校验

| 操作 | 示例指令 |
|------|----------|
| 员工统计 | 「员工统计」「人数统计」「合同到期提醒」 |
| 数据校验 | 「校验花名册」「检查数据质量」 |
| 导出报表 | 「导出报表」「生成Excel」 |
| 审计日志 | 「查看操作日志」「最近操作记录」 |

## 数据存储

所有数据存储在用户本地，不上云：

| 文件 | 说明 |
|------|------|
| `.hr-data/config.json` | 绑定状态、列映射、初始化配置 |
| `.hr-data/audit.log.jsonl` | 操作审计日志（append-only） |
| `.hr-data/payroll/YYYY-MM.json` | 月度薪资计算结果（按月归档） |
| `.hr-data/conversations/` | 对话历史记录 |

## 交互规范

1. **首次使用**：如果用户提到员工/薪资等操作但未初始化，先引导完成初始化
2. **文件上传**：初始化时引导用户直接上传 Excel 文件，不要让用户手动填写路径
3. **参数缺失**：当用户提供的信息不完整时，主动追问缺失参数
4. **中文回复**：所有响应使用中文
5. **操作确认**：增删改操作执行前，向用户确认
6. **错误处理**：遇到错误时给出清晰的错误原因和建议
7. **文件路径**：仅处理用户上传的 Excel 文件（.xlsx/.xls），使用上传后的文件路径调用 `bind` 子命令

## 注意事项

- 不需要绑定表格即可使用：社保计算、公积金计算、年终奖计算、个税税率查询
- 批量薪资计算结果会自动持久化到 `.hr-data/payroll/` 目录
- 所有写操作（增/删/改/薪资计算）自动记录审计日志
- Python 脚本路径为 `{{baseDir}}/tools/main.py`，所有 `.py` 文件在 `tools/` 目录下
- 本 Skill 仅处理 Excel 文件（.xlsx/.xls），不会访问其他类型的系统文件
