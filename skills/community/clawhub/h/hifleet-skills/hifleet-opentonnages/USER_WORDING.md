# User wording (mandatory)

## Say → Do not say

| Avoid (internal) | Use with user |
|------------------|---------------|
| unlock, decrypt, typeCode, dataId | **获取联系方式** / **查看联系人** / get contact details |
| POST /unlock | **向 HiFleet 查询该条的联系方式**（扣积分） |
| route V / G | **公开船盘** / **公开货盘** / **HiFleet 平台船货** |
| vessels/search, cargo/search | **在 HiFleet 公开市场上查询** |
| enrich-row | **补充船舶档案 / 标签 / 港距** |
| record id | **记录 id**（列表里每条旁的编号，用于指定要哪条） |

## List vs contacts

- **First reply**: ship/cargo facts only + **记录 id** on each row.
- **Guide** (example):  
  「如需某条船的联系方式，请告诉我 **记录 id**（如 `12345`）；若要本页全部船的联系方式，请说 **全部**。」
- **After fetch**: 「已获取联系方式」— show phone/email/company; **do not** say 「已解锁」.

## Redirects

| User wants | Skill |
|------------|--------|
| **Liner** schedule | **hifleet-schedule** |
| **Public** open tonnage/cargo | **hifleet-opentonnages** (this) |
