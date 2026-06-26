# 考勤管理 (attendance_*)

## 打卡记录

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `attendance_queryMyTodayRecords` | — | — | 今日打卡 |
| `attendance_queryMyRecords` | — | `startDate` `endDate` `status`(normal/late/early/absent/overtime) | 历史打卡记录 |
| `attendance_queryAllRecords` | — | `employeeName` `startDate` `endDate` `page` `limit` | 全员考勤（管理员） |

## 考勤统计

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `attendance_queryMyMonthlyStat` | — | `month`(yyyyMM,默认当月) | 月度统计 |
| `attendance_queryMyYearlyStat` | — | `year`(yyyy,默认当年) | 年度统计（全年12个月） |
| `attendance_queryDeptMonthlyStat` | — | `deptName`(模糊) `deptId` `year` `month`(1-12) | 部门月度统计；deptName与deptId二选一 |

## 请假查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `attendance_queryMyLeaveRecords` | — | `startDate` `endDate` `page` `limit` | 请假记录 |
| `attendance_queryMyLeaveBalance` | — | — | 假期余额 |

## 请假申请

`attendance_applyLeave(leaveData: JSON)`

**必填**：`type` `startTime`(yyyy-MM-dd HH:mm:ss) `endTime`(yyyy-MM-dd HH:mm:ss) `reason`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `type` | 请假类型ID | 1年假 / 2事假 / 3病假 / 4婚假 / 5产假 / 6丧假（以系统配置为准） |
| `duration` | 请假时长 | 不填则系统自动计算 |

> `employeeId`、`companyId` 由系统自动注入，无需传入

## 加班管理

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `attendance_queryMyOvertimeRecords` | — | `startDate` `endDate` `page` `limit` | 加班记录 |
