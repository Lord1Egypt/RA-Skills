---
name: ICD-Coding
description: ICD疾病分类与手术操作编码技能。熟练掌握中国ICD-10、ICD-9-CM-3、ICD-O编码体系，精通主要诊断选择原则（含黄锋版规则），熟悉DRG/DIP分组规则，支持诊断/手术主导词双向查找（内置词条数据库）。
metadata:
  tags: [医疗, 病案, 编码, DRG, DIP, ICD-10, ICD-9, 医保]
  author: ICD-Coding Team
---

# ICD-Coding 疾病分类与手术操作编码技能

熟练掌握中国ICD-10、ICD-9-CM-3、ICD-O编码体系，精通主要诊断选择原则（含黄锋版规则），熟悉DRG/DIP分组规则，可进行疾病编码查询、诊断选择建议、编码审核等。

## 核心能力

1. **ICD-10 疾病编码查询** — 26,606条诊断主导词，支持精确+模糊双向查找
2. **ICD-9-CM-3 手术编码查询** — 4,620条手术主导词，含腹腔镜/开放入路区分
3. **主导词双向查找** — 词→码 / 码→词，含完整多级查找路径
4. **临床术语映射** — 🆕 **31,106条**《国家临床版ICD-10 2.0》对照，30个科室，含又称/曾称/英文名
5. **CHS-DRG2.0分组查询** — 🆕 **409个ADRG / 655个DRG** 含权重；ICD→MDC/ADRG/DRG三级映射
6. **主要诊断选择规则（黄锋版）** — 17个疾病类别的详细选择规范
7. **临床知识支持** — 诊断学基础知识、症状鉴别、辅助检查解读
8. **ICD-O肿瘤编码** — ICD-O-4最新动态行为编码
9. **ICD-11 最新知识** ← WHO 2022年发布，簇编码/扩展码/传统医学章节等新特性

## 查询指令

```
诊断主导词 <疾病名称>   → ICD-10编码（例：诊断主导词 肺炎）
ICD查码 <编码>          → 主导词路径（例：ICD查码 I10）
手术主导词 <手术名称>   → ICD-9-CM-3编码（例：手术主导词 胆囊切除）
手术查码 <编码>         → 主导词路径（例：手术查码 51.23）
临床术语 <医学名词>      → 国家临床版ICD-10 2.0编码（例：临床术语 原发性肺癌）
ICD临床查码 <编码>      → 临床术语名称（例：ICD临床查码 C34）
DRG查ICD <ICD编码>      → MDC/ADRG/DRG三级分组（例：DRG查ICD I21）
DRG查ADRG <ADRG>       → ADRG→DRG细分组（例：DRG查ADRG FF9）
DRG权重 <DRG代码>      → 查询DRG权重（例：DRG权重 FR21）
```

## 主要诊断三最原则

1. **患者住院的主要原因**
2. **消耗医疗资源最多**
3. **影响患者康复最大**

## 常用编码速查

| 编码 | 疾病 |
|------|------|
| I10 | 原发性高血压 |
| I21.0 | ST段抬高型心肌梗死 |
| I48.x | 心房颤动 |
| I63.x | 脑梗死 |
| J18.9 | 肺炎（未特指） |
| J44.1 | 慢阻肺急性加重 |
| K85.x | 急性胰腺炎 |
| E11.9 | 2型糖尿病（无并发症） |
| E11.1 | 2型糖尿病伴酮症酸中毒 |
| C34.x | 肺恶性肿瘤 |

## 常用网址

- 国家医保版ICD-10查询：https://code.nhsa.gov.cn/jbzd/public/dataWesterSearch.html
- WHO ICD-10 Browser：https://icd.who.int/browse10/2022/en
- **WHO ICD-11 Browser**（新增！）：https://icd.who.int/browse/11

## 详细文档

| 文档 | 内容 |
|------|------|
| `docs/Diagnosis_Lead_Words.md` | 诊断主导词速查表（15大类+完整路径） |
| `docs/Surgery_Lead_Words.md` | 手术主导词速查表（10大类+入路区分） |
| `docs/Diagnosis_Selection.md` | 黄锋版主要诊断选择规则（17类疾病） |
| `docs/Clinical_Term_Mapping.md` | 🆕 **临床术语映射速查**（31,106条，30个科室） |
| `docs/Clinical_Knowledge.md` | 诊断学临床知识（症状/检查/诊断标准） |
| `docs/Principal_Diagnosis_Procedure.md` | 编码操作规程 |
| `docs/DRG_Knowledge.md` | 🆕 **CHS-DRG2.0知识手册**（26MDC/409ADRG/655DRG/权重） |
| `docs/ICD_Updates_2025.md` | ICD编码2024-2025年最新更新 |
| `docs/ICD11_Reference.md` | ICD-11全面参考（簇编码/扩展码/中国实施进展） |
| `docs/ICD10_Chapters.md` | ICD-10 22章详细分类 |
| `docs/ICD9CM3_Chapters.md` | ICD-9-CM-3 17章详细分类 |
| `docs/ICDO_4.md` | ICD-O-4肿瘤形态学编码 |
| `docs/icd_lookup_tool.py` | Python诊断/手术/临床术语查询工具 |
| `docs/drg_lookup_tool.py` | 🆕 Python DRG分组+权重查询工具 |
| `data/clinical_terms.json` | 🆕 临床术语映射数据库（31,106条） |
| `data/drg_weight.json` | 🆕 DRG权重+ADRG/DRG映射（409+655条） |
| `data/drg_icd_map.json` | 🆕 ICD→MDC/ADRG映射（38,114条） |

## 参考资料

1. 《疾病和有关健康问题的国际分类第十次修订本（ICD-10）》
2. 《ICD-9-CM-3 手术操作分类代码》
3. 《ICD-O 第三版/第四版》
4. 《ICD-11 MMS 参考指南》（WHO 2022）
5. 《病案信息学》（第三版）
6. 《诊断学（第10版）》
7. 《主要诊断编码选择规则（黄锋版）》
8. CHS-DRG分组方案 + DIP技术规范
