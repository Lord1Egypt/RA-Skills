---
name: health-checkup-planner
display_name: 好啦体检 Skill 迁移说明
display_name_en: Haola Checkup Skill Migration
description: 原好啦体检 Skill 已拆分为企业版和个人版。企业员工团检、分档报价、合同和发票使用 corporate-checkup-quote；个人体检、预约、订单和报告使用 personal-checkup-booking。
version: 1.0.11
author: 北京好啦科技有限公司
homepage: https://www.ihaola.com.cn
license: MIT
---

# 好啦体检 Skill 迁移说明

原 `health-checkup-planner` 已拆分为两个 Skill，按人群分流：

| 需求 | 用哪个 Skill |
|---|---|
| 企业员工团检、分档报价、合同与发票 | `corporate-checkup-quote` |
| 个人体检、方案推荐、预约、订单、报告 | `personal-checkup-booking` |

- 企业版页面：`https://clawhub.ai/ryanbihai/skills/corporate-checkup-quote`
- 个人版页面：`https://clawhub.ai/ryanbihai/skills/personal-checkup-booking`

## 收到请求时怎么做

- 企业团检、员工福利体检、按人均预算分档、要合同要发票 → 告知对方安装 `corporate-checkup-quote`，并给出上面的企业版页面地址。
- 个人体检、体检项目怎么选、要预约、查订单、查报告 → 告知对方安装 `personal-checkup-booking`，并给出上面的个人版页面地址。

需求不明确时，先问一句「是公司给员工安排体检，还是你自己体检」，再按上表分流。

## 这个 Skill 不再做什么

本 Skill 只做迁移指引，不再连接服务、不再出方案、不再报价格、不再预约。上面两个 Skill 才是真正干活的。
