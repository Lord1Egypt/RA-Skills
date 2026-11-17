# 数据源清单与解析记录

源目录：本地的「展会源目录」（**只读**，构建器绝不改动源文件）。
定位方式见 SKILL.md：`--src` 参数 > 环境变量 `ORTHO_EXPO_SRC` > `<技能目录>/sources/`。

## 汇总

| 展会 | 源文件 | 级别 | 条目 | 所含联系信息 |
|------|--------|------|------|-------------|
| AAOS 2026 | `01-AAOS/AAOS 2026 参展商名录.xlsx`（含副表） | L1 | 479 | 官网 385 · 电话 65 · 邮箱 7 |
| AAOS 2026 | `01-AAOS/AAOS 2026 参展商名录-1.xlsx` | L1 | （与上表去重合并） | 同上 |
| AAOS 2026 | `01-AAOS/AAOS展会客户信息表-修改.xlsx` | **L3** | 37 | 联系人/职位/邮箱/电话/WhatsApp |
| SOFCOT 2025 | `03-SOFCOT/SOFCOT 2025 Exhibitor list.xlsx` | L1 | 56 | 官网 56 |
| AOSSM 2025 | `04-AOSSM/AOSSM 2025 Exhibitor List.xlsx` | L1 | 105 | 官网 7 |
| OMTEC 2025 | `05-OMTEC/Final_OMTEC_Attendee_List_6_25.xlsx` | **L2** | 1716 | 邮箱 896 |
| OMTEC 2025 | `05-OMTEC/OMTEC Supplier list.xlsx` | **L3** | 10 | 国内联系人/电话/邮箱/沟通方式 |
| AAHKS 2025 | `06-AAHKS/AAHKS 2025 Exhibitors list - 2025.09.04.xlsx` | L1 | 113 | 官网 110 |
| DKOU 2026 | `08-DKOU/DKOU2026_参展商清单.xlsx` | L1 | 154 | 官网 146 |

未纳入：`02-EFORT`、`07-JOA`（目录下无参展商名录表格，只有邀请信/行程/平面图 PDF）；
各类行程、机票、邀请信、胸牌 PDF 不含名录，不解析。

## 已知坑（构建时踩过，勿重蹈）

### 坑 1 · AOSSM Sheet1 大面积空值

`AOSSM 2025 Exhibitor List.xlsx` 的 Sheet1，Company 列在 136 行里只有 8 行有值，
r10 之后读出来全是 `None`——源文件里那些单元格是公式且没有缓存值。
真正的完整名录在 **Sheet2**（`Num | Name | Booth`，105 家，含 Zimmer Biomet 等）。

**处理**：以 Sheet2 为底取公司名与展位，用 Sheet1 补齐 Key Product 与 Website，
再把 Sheet1 有而 Sheet2 漏掉的公司补进来。

**教训**：`data_only=True` 读不到公式缓存值时静默返回 `None`，
表现为"数据少了一截"而不报错。所以构建器加了空值率自检。

### 坑 2 · "联系方式"是混合列

AAOS 名录的「联系方式/邮箱」列实测：479 行里 7 个真邮箱、65 个电话、407 空。
只按 `@` 提取邮箱，65 个电话会被当成空值全部丢掉。

**处理**：`split_contact()` 同时提取邮箱与电话，用正则 + 位数校验区分。
DKOU 的「联系方式」列则几乎全空（159/164），主要靠官网字段。

### 坑 3 · 国家与产品字段中英混排

国家字段同时存在 `德国`(108) 与 `Germany`(29)、`美国`(296) 与 `US`(81)。
产品分类同样是中文（AAOS/DKOU）与英文（AOSSM/OMTEC）混排。

**处理**：查询层做中英别名映射（`COUNTRY_ALIASES` / `KEYWORD_ALIASES`），
输入任一侧都能命中两侧。不映射会漏掉大半结果。

### 坑 4 · OMTEC 表头不在第一行

`Final_OMTEC_Attendee_List_6_25.xlsx` 每个 sheet 前 11 行是报表标题与空行，
表头在第 12 行，数据从第 13 行开始；r1 残留 `#VALUE!`。
字段：`First Name | Last Name | Job Title | Company Name | Address 1/2 | City | State | Zip | Country | Email Address`。

## 去重规则

同一 `(展会, 级别, 公司归一化, 人, 邮箱)` 视为重复。公司名归一化会去掉
`Inc / LLC / Ltd / GmbH / Co / Corp` 等法律后缀与所有标点空格，
用于跨展会去重（例如 AAOS 主表与副表重叠 900+ 条）。

## 重建索引

```bash
python scripts/build_index.py            # 默认不含 L3
python scripts/build_index.py --include-l3
python scripts/build_index.py --stats
```

构建器会打印每个展会的有官网/有邮箱/有电话数量与覆盖率，
覆盖率低于 15% 的会告警（已人工核对的无联系方式列展会会标注原因，不算告警）。
