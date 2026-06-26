# 领星目标管理接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

> 注意：这两个接口的成功状态码为 `code=1`（而非通常的 0），消息字段为 `msg`。

---

## StoreBatchSelect - 店铺维度批量查询目标

**路径**: `/bd/goal/management/open/store/batchSelect`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| assessYear | 是 | string | 目标年份，如 "2024" |

**关键返回字段**: goalName, sid, name(店铺名), currencyCode, icon, assessYear, goalAmount1~12(各月目标值), realAmount1~12(各月完成值), completeRateAmount1~12(各月完成率), totalGoalAmount, totalRealAmount, totalCompleteRate, createUserName, gmtCreate

---

## UserBatchSelect - 组织维度批量查询目标

**路径**: `/bd/goal/management/open/user/batchSelect`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| assessYear | 是 | int | 目标年份，如 2024 |
| assessType | 是 | int | 考核指标：1=销售额，2=销量 |

**关键返回字段**: realName, uid, defaultOrg, orgs[orgId/orgName], currencyCode, assessType, goalValue1~12(各月目标值), realValue1~12(各月完成值), completeRate1~12(各月完成率), yearGoalValue, yearRealValue, completeProcess, createUser, gmtCreate

---
