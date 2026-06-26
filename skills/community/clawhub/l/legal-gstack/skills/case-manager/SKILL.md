---
name: case-manager
description: 案件管理员。进度跟踪、期限提醒、结案归档、案件统计。
metadata: { "openclaw": { "requires": { "bins": [] }, "install": [] } }
---

# 案件管理员 `/case-manager`

## 功能
1. **进度跟踪** - 案件阶段、下一步行动
2. **期限提醒** - 举证期限、上诉期限、开庭时间
3. **结案归档** - 案件材料整理、归档
4. **案件统计** - 案件数量、类型分布、胜诉率

## 用法
```
/case-manager list                     # 案件列表
/case-manager deadline [案件名]        # 期限提醒
/case-manager status [案件名]          # 进度查看
/case-manager archive [案件名]         # 结案归档
/case-manager stats                    # 案件统计
```

## 文件位置
- 案件目录：`~/Documents/01_案件管理/`
- 归档：`~/Documents/01_案件管理/已结案/`

---

*优先级：P8 | 使用频率：中*
