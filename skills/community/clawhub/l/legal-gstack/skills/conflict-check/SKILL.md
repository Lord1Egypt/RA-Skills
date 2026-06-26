---
name: conflict-check
description: 利益冲突审查员。利益冲突检索、委托评估、回避审查。
metadata: { "openclaw": { "requires": { "bins": [] }, "install": [] } }
---

# 利益冲突审查员 `/conflict-check`

## 功能
1. **利益冲突检索** - 检索历史案件、对方当事人
2. **委托评估** - 是否存在利益冲突
3. **回避审查** - 是否需要回避

## 用法
```
/conflict-check [对方当事人名称]
/conflict-check --case [案件名]
```

## 输出位置
- `~/Documents/01_案件管理/利益冲突审查/[日期]_[对象名称].md`

---

*优先级：P7 | 使用频率：低*
