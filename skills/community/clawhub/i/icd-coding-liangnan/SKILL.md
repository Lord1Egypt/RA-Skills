# ICD-Coding 疾病分类与手术操作编码技能

熟练掌握中国ICD-10、ICD-9-CM-3、ICD-O编码体系，精通主要诊断选择原则（含黄锋版规则），熟悉DRG/DIP分组规则，可进行疾病编码查询、诊断选择建议、编码审核等。

## 版本说明

- **v2.3.0** (2026-09-08) — **新增 CHS-DRG 3.0 分组知识**（医保发〔2026〕22号 附件1，492 ADRG / 825 DRG / 31 基层病组），与 2.0 双轨并行
- v2.2.0 (2026-06) — CHS-DRG 2.0 分组查询
- v2.1.0 — ICD-O-4 最新动态行为编码
- v2.0.0 — 31,106 条国家临床版 ICD-10 2.0 临床术语映射

## 核心能力

1. **ICD-10 疾病编码查询** — 26,606条诊断主导词，支持精确+模糊双向查找
2. **ICD-9-CM-3 手术编码查询** — 4,620条手术主导词，含腹腔镜/开放入路区分
3. **主导词双向查找** — 词→码 / 码→词，含完整多级查找路径
4. **临床术语映射** — 31,106 条《国家临床版ICD-10 2.0》对照，30个科室，含又称/曾称/英文名
5. **CHS-DRG 2.0 分组查询** — 409 ADRG / 655 DRG，含权重；ICD→MDC/ADRG/DRG三级映射
6. **CHS-DRG 3.0 分组查询** 🆕 — **492 ADRG / 825 DRG / 31 基层病组**（医保发〔2026〕22号），含 2.0↔3.0 对比、ADRG 分组明细（67,329 条入组规则）、MCC/CC/高危妊娠/机器人辅助/疾病排除/手术排除等完整数据
7. **主要诊断选择规则（黄锋版）** — 17个疾病类别的详细选择规范
8. **临床知识支持** — 诊断学基础知识、症状鉴别、辅助检查解读
9. **ICD-O 肿瘤编码** — ICD-O-4 最新动态行为编码
10. **ICD-11 最新知识** ← WHO 2022年发布，簇编码/扩展码/传统医学章节等新特性

## 查询指令

### 通用编码查询
```
诊断主导词 <疾病名称>   → ICD-10 编码（例：诊断主导词 肺炎）
ICD查码 <编码>          → 主导词路径（例：ICD查码 I10）
手术主导词 <手术名称>   → ICD-9-CM-3 编码（例：手术主导词 胆囊切除）
手术查码 <编码>         → 主导词路径（例：手术查码 51.23）
临床术语 <医学名词>      → 国家临床版 ICD-10 2.0 编码（例：临床术语 原发性肺癌）
ICD临床查码 <编码>      → 临床术语名称（例：ICD临床查码 C34）
```

### CHS-DRG 2.0 查询
```
DRG查ICD <ICD编码>      → MDC/ADRG/DRG 三级分组（例：DRG查ICD I21）
DRG查ADRG <ADRG>       → ADRG→DRG 细分组（例：DRG查ADRG FF9）
DRG权重 <DRG代码>      → 查询 DRG 权重（例：DRG权重 FR21）
```

### CHS-DRG 3.0 查询 🆕
```
DRG3.0查MDC <诊断编码>           → 所属 MDC（例：DRG3.0查MDC I63.401）
DRG3.0查ADRG <ICD编码>           → 可能的 ADRG 列表（例：DRG3.0查ADRG 33.5000）
DRG3.0查DRG <DRG编码>            → DRG 名称、CC/MCC 标识（例：DRG3.0查DRG BB21）
DRG3.0基层病组 <疾病名/编码>      → 是否为 31 基层病组之一
DRG3.0对比2.0 <ADRG编码>         → 2.0 ↔ 3.0 编码/名称变化
DRG3.0是MCC <诊断编码>            → 是否为严重合并症
DRG3.0是CC <诊断编码>             → 是否为一般合并症
DRG3.0高危妊娠 <诊断编码>         → 是否高危妊娠
DRG3.0查MDC列表 <MDC字母>         → 列出该 MDC 下所有 ADRG/DRG
```

> 命令前缀 `DRG3.0` 用于与 2.0 命令 `DRG` 区分。  
> 过渡期（2026-9 ~ 2027-3）建议同时支持两套命令。

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

- 国家医保版 ICD-10 查询：https://code.nhsa.gov.cn/jbzd/public/dataWesterSearch.html
- WHO ICD-10 Browser：https://icd.who.int/browse10/2022/en
- **WHO ICD-11 Browser**（新增！）：https://icd.who.int/browse/11
- 国家医保局 DRG/DIP 3.0 通知：https://www.nhsa.gov.cn/art/2026/9/2/art_104_21975.html

## 详细文档

| 文档内容 | 说明 |
|----------|------|
| `docs/Diagnosis_Lead_Words.md` | 诊断主导词速查表（15大类+完整路径） |
| `docs/Surgery_Lead_Words.md` | 手术主导词速查表（10大类+入路区分） |
| `docs/Diagnosis_Selection.md` | 黄锋版主要诊断选择规则（17类疾病） |
| `docs/Clinical_Term_Mapping.md` | 临床术语映射速查（31,106 条，30 个科室） |
| `docs/Clinical_Knowledge.md` | 诊断学临床知识（症状/检查/诊断标准） |
| `docs/Principal_Diagnosis_Procedure.md` | 编码操作规程 |
| `docs/DRG_Knowledge.md` | CHS-DRG 2.0 知识手册（26 MDC / 409 ADRG / 655 DRG） |
| **`docs/DRG3.0_Knowledge.md`** 🆕 | **CHS-DRG 3.0 知识手册**（26 MDC / 492 ADRG / 825 DRG / 31 基层病组） |
| **`docs/DRG3.0_Changes.md`** 🆕 | **CHS-DRG 2.0 → 3.0 关键变更对照**（83 个新增 ADRG、47 个删除/合并、命名口径变化） |
| `docs/ICD_Updates_2025.md` | ICD 编码 2024-2025 年最新更新 |
| `docs/ICD11_Reference.md` | ICD-11 全面参考（簇编码/扩展码/中国实施进展） |
| `docs/ICD10_Chapters.md` | ICD-10 22 章详细分类 |
| `docs/ICD9CM3_Chapters.md` | ICD-9-CM-3 17 章详细分类 |
| `docs/ICDO_4.md` | ICD-O-4 肿瘤形态学编码 |
| `docs/icd_lookup_tool.py` | Python 诊断/手术/临床术语查询工具 |
| `docs/drg_lookup_tool.py` | Python DRG 2.0 分组+权重查询工具 |
| **`docs/drg3.0_lookup_tool.py`** 🆕 | **Python DRG 3.0 分组+权重+对比+基层病组+MCC/CC/高危妊娠查询工具** |

## 数据文件

| 数据文件 | 说明 |
|----------|------|
| `data/clinical_terms.json` | 临床术语映射数据库（31,106 条） |
| `data/drg_weight.json` | DRG 2.0 权重+ADRG/DRG 映射（409+655 条） |
| `data/drg_icd_map.json` | DRG 2.0 ICD→MDC/ADRG 映射（38,114 条） |
| **`data/drg3.0_mdc.json`** 🆕 | **DRG 3.0 26 MDC 目录** |
| **`data/drg3.0_mdc_summary.json`** 🆕 | **DRG 3.0 MDC 概览（ADRG/DRG 数）** |
| **`data/drg3.0_adrg.json`** 🆕 | **DRG 3.0 492 ADRG 目录** |
| **`data/drg3.0_drg.json`** 🆕 | **DRG 3.0 825 DRG 目录（含 MCC/CC 标识）** |
| **`data/drg3.0_basal.json`** 🆕 | **DRG 3.0 31 基层病组（27 内科+4 手术）** |
| **`data/drg3.0_adrg_compare.json`** 🆕 | **DRG 2.0 ↔ 3.0 ADRG 对比（409→492，含统计）** |
| **`data/drg3.0_mdc_dx.json`** 🆕 | **DRG 3.0 MDC 主诊表（29,174 条）** |
| **`data/drg3.0_adrg_to_icd.json`** 🆕 | **DRG 3.0 ADRG→入组 ICD 明细（含 67,329 条入组规则）** |
| **`data/drg3.0_icd_to_adrg.json`** 🆕 | **DRG 3.0 ICD→ADRG 反向索引（38,427 个编码）** |
| **`data/drg3.0_ops.json`** 🆕 | **DRG 3.0 9,629 条手术或操作目录** |
| **`data/drg3.0_mcc.json`** 🆕 | **DRG 3.0 1,581 条 MCC 严重合并症** |
| **`data/drg3.0_cc.json`** 🆕 | **DRG 3.0 6,337 条 CC 合并症** |
| **`data/drg3.0_excl_dx.json`** 🆕 | **DRG 3.0 1,859 条不作为分组的疾病** |
| **`data/drg3.0_high_risk_preg.json`** 🆕 | **DRG 3.0 811 条高危妊娠诊断** |
| **`data/drg3.0_robot_ops.json`** 🆕 | **DRG 3.0 机器人辅助手术（5 条）** |

## CHS-DRG 3.0 关键变化（详见 `docs/DRG3.0_Changes.md`）

- ADRG: 409 → **492** (+83)
- DRG: 655 → **825** (+170)
- 31 个基层病组（同病同付）：27 内科 + 4 手术
- 重大重构：肿瘤治疗（拆为 21 个 ADRG）、神经系统（神经刺激器/疼痛治疗/康复/免疫治疗）、眼科、呼吸支持、新生儿（按入院体重分 5 档）、糖尿病（3 类）、血小板/凝血（5 类）等
- 执行时间：**2027-01-01 起执行**，2026-12-31 前完成准备，2027-3 月底前全面落地

## 参考资料

1. 《疾病和有关健康问题的国际分类第十次修订本（ICD-10）》
2. 《ICD-9-CM-3 手术操作分类代码》
3. 《ICD-O 第三版/第四版》
4. 《ICD-11 MMS 参考指南》（WHO 2022）
5. 《病案信息学》（第三版）
6. 《诊断学（第10版）》
7. 《主要诊断编码选择规则（黄锋版）》
8. CHS-DRG 2.0 分组方案 + DIP 技术规范
9. 🆕 **医保发〔2026〕22号《关于印发按病组（DRG）和病种分值（DIP）付费 3.0 版分组方案的通知》**
10. 🆕 **CHS-DRG 3.0 分组方案（附件 1，1829 页）+ DIP 3.0 病种库（附件 2，311 页）**

---

## 如何更新此 Skill 到 ClawHub

将本目录打包后到 https://clawhub.ai 上传更新即可。文件结构：
```
icd-coding/
├── SKILL.md                              # 本文件
├── docs/
│   ├── ... (原有文档)
│   ├── DRG3.0_Knowledge.md               # 新增
│   ├── DRG3.0_Changes.md                 # 新增
│   └── drg3.0_lookup_tool.py             # 新增
└── data/
    ├── ... (原有数据)
    ├── drg3.0_mdc.json                   # 新增
    ├── drg3.0_adrg.json                  # 新增
    └── ... (其他 drg3.0_*.json)
```

**当前版本**：v2.3.0  
**最后更新**：2026-09-08  
**许可证**：MIT-0
