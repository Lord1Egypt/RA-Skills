---
name: legal-draft
description: 文书起草员。起诉状、答辩状、代理词、律师函、合同审查/起草。
metadata: { "openclaw": { "requires": { "bins": [] }, "install": [] } }
---

# 文书起草员 `/legal-draft`

## 功能
1. **诉讼文书** - 起诉状、答辩状、上诉状、代理词
2. **非诉文书** - 律师函、法律意见书
3. **合同** - 审查、起草、修改
4. **程序文书** - 申请书、授权委托书

## 用法
```
/legal-draft [文书类型] --case [案件名]
/legal-draft 起诉状 --case 张三离婚案
/legal-draft 律师函 --recipient [对方名称]
```

## 模板位置
- `~/Documents/01_案件管理/模板/`
- `~/Documents/02_法律文书/`

## 输出位置
- `~/Documents/02_法律文书/诉讼文书/[文书名].docx`
- `~/Documents/01_案件管理/进行中/[案件名]/[文书名].docx`

## 命名规范
`YYYYMMDD_案件名_文书类型_版本.docx`

---

*优先级：P2 | 使用频率：高*
