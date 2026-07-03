# User-facing language (mandatory)

## Default

- **Prefer English** for explanations, errors, and setup hints when locale is unknown.  
- **Translate** system/status text to the user’s agent UI language when locale is known (`LOCALIZATION.md`).  
- **Never translate** business data: vessel names, port names, cargo names, line names, API field values, IMO, dates in data rows.

## Forbidden → use instead

| Avoid | Use |
|-------|-----|
| workflow, schema, POST /schedules | **schedule query**, **HiFleet** |
| offset/limit, typeCode | **pagination**, **获取联系方式** (by record id) |
| route B | **liner schedule** |

## Locked contacts

- ✅ 「联系方式默认不展示；请提供 **记录 id**，或说 **全部** 获取本页所有船的联系方式（按条扣积分）。」  
- ✅ After fetch: 「已获取联系方式」— **do not** say 「已解锁」  
- ❌ 「Call POST /unlock with typeCode=…」
