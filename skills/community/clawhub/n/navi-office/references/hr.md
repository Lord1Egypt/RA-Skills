# 人力资源管理 (hr_*)

## 员工查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `hr_queryMyInfo` | — | — | 当前用户基本信息 |
| `hr_queryEmployeeList` | — | `employeeName`(模糊) `employeeNo`(模糊) `employeeStatus`(1在职/2离职/3试用) `deptName`(模糊,自动转deptId) `entryDateStart` `entryDateEnd` `page` `limit` | 员工列表 |
| `hr_queryEmployeeInfo` | `employeeId`或`employeeName` | — | 员工详情；姓名可能重名需确认 |
| `hr_queryBirthdayEmployees` | — | `month`(1-12,默认当月) `page` `limit` | 生日员工（仅在职） |
| `hr_queryContractExpiring` | — | `days`(默认30) `page` `limit` | 合同即将到期员工 |
| `hr_queryProbationExpiring` | — | `days`(默认30) `page` `limit` | 试用期即将结束员工 |

## 员工创建

`hr_createEmployee(employeeData: JSON)`

**必填**：`employeeName` `mobile`

**强烈建议同时提供**：`entryDate`(yyyy-MM-dd) `firstWorkDate`(yyyy-MM-dd，首次参加工作日期)

**未填时的系统默认值**：`employeeType`=1(全职)、`employeeStatus`=0(试用)、`firstWorkDate`=entryDate或今日

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `employeeNo` | 工号 | — |
| `gender` | 性别 | 0男 / 1女 / 2未知 |
| `orgId` | 部门ID | 先调 `system_queryDeptTree` 获取 |
| `employeeType` | 员工类型 | 0无/1全职/2兼职/3实习/4劳务派遣/5退休返聘/6劳务外包 |
| `employeeStatus` | 员工状态 | 0试用/1正式/2离职 |
| `probationPeriod` | 试用期月数 | 0无/1-6月/7其他 |
| `idNumber` | 身份证号 | — |
| `birthDate` | 出生日期 | yyyy-MM-dd |
| `nationality` | 民族 | — |
| `education` | 学历 | 0小学/1初中/2高中/3中专/4大专/5本科/6硕士/7博士/8其他 |
| `graduationSchool` | 毕业院校 | — |
| `major` | 专业 | — |
| `bankCardNumber` | 银行卡号 | — |
| `bankName` | 开户行 | — |

> 部门名称→ID：先调 `system_queryDeptTree` 获取 `orgId`

## 员工修改

`hr_updateEmployee(employeeId, employeeData: JSON字符串)`

**必填**：`employeeId`（员工ID）

**employeeData**：JSON **字符串**只传需要修改的字段，未传字段保持原值。可修改字段与「员工创建」可选字段相同（`employeeName` `mobile` `gender` `orgId` `employeeType` `employeeStatus` `entryDate` `firstWorkDate` `probationPeriod` `idNumber` `birthDate` `nationality` `education` `graduationSchool` `major` `bankCardNumber` `bankName` 等）。

> `jobLevelId`、`baseSalary`、`sysUserId` 受保护，此工具无法修改。

> 修改前建议先调 `hr_queryEmployeeInfo` 确认员工ID及当前信息。

## 薪资查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `hr_queryMySalary` | — | `month`(yyyyMM) | 个人工资（不填查最新） |
| `hr_queryMySalaryList` | — | `year`(yyyy,默认当年) | 全年12个月工资列表 |
| `hr_queryEmployeeSalary` | `employeeId` | `month`(yyyyMM) | 查他人工资（需权限）；先查employeeId |
