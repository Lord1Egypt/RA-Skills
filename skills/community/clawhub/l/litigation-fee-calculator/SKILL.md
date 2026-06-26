---
name: litigation-fee-calculator
description: >
  用于计算中国法院诉讼费、案件受理费和申请费，依据《诉讼费用交纳办法》（国务院令第481号）第十三条、第十四条。用户询问或比较财产案件、离婚案件、人格权案件、知识产权民事案件、劳动争议、行政案件、管辖权异议、申请执行、财产保全、支付令、公示催告、撤销仲裁裁决、认定仲裁协议效力、破产申请、海事申请费等费用时使用。典型触发词包括：“计算诉讼费”“诉讼费怎么算”“起诉要交多少钱”“案件受理费”“申请执行费”“保全费”“支付令费用”“公示催告费”“破产申请费”“海事申请费”。兼容英文检索词：litigation fee、court filing fee。
---

# 诉讼费用计算 Skill

## 定位

计算中国法院案件受理费与各类申请费，依据《诉讼费用交纳办法》（国务院令第481号）第十三条、第十四条。优先使用脚本给出确定金额；对法定幅度收费，默认按下限输出，并明确提示“以当地法院或地方标准为准”。

---

## 触发场景

- 用户询问起诉某一金额需缴多少诉讼费
- 用户询问离婚、人格权、知识产权、劳动争议、行政案件的收费标准
- 用户询问申请执行、财产保全、申请支付令、破产申请的费用
- 用户需要对多种方案的诉讼成本进行对比

---

## 工作流程

### 第一步：判断案件类型与必要参数

询问或从上下文确认以下信息：

| 信息项 | 说明 |
|--------|------|
| 案件类型 | 财产、离婚、人格权、知识产权、劳动争议、行政、执行、保全、支付令、破产、公示催告、仲裁撤销/仲裁协议效力、海事申请等 |
| 金额参数 | 财产、执行、保全、支付令、破产、知识产权有争议金额时必须提供 |
| 特殊参数 | 离婚案件需财产分割金额；人格权案件需赔偿金额 |
| 二级分类 | 知识产权需区分有无争议金额；行政需区分商标/专利/海事行政与其他行政；执行需区分有无执行金额；海事申请需区分具体申请类型 |

### 第二步：调用计算脚本

使用 `scripts/calc_litigation_fee.py` 计算费用，统一使用 `python3`：

```bash
# 财产案件（诉讼请求金额150万元）
python3 scripts/calc_litigation_fee.py --type property --amount 1500000

# 离婚案件（涉及财产分割250万元）
python3 scripts/calc_litigation_fee.py --type divorce --property 2500000

# 人格权案件（赔偿金额12万元）
python3 scripts/calc_litigation_fee.py --type personality --damages 120000

# 申请执行（执行金额80万元）
python3 scripts/calc_litigation_fee.py --type enforcement --amount 800000

# 财产保全（保全金额120万元）
python3 scripts/calc_litigation_fee.py --type preservation --amount 1200000

# 申请支付令（金额30万元）
python3 scripts/calc_litigation_fee.py --type payment_order --amount 300000

# 破产案件（破产财产总额500万元）
python3 scripts/calc_litigation_fee.py --type bankruptcy --amount 5000000

# 公示催告
python3 scripts/calc_litigation_fee.py --type public_notice

# 申请撤销仲裁裁决或认定仲裁协议效力
python3 scripts/calc_litigation_fee.py --type arbitration_set_aside
```

完整 `--type` 参数列表：

| 参数值 | 对应案件类型 |
|--------|------------|
| `property` | 财产案件受理费 |
| `divorce` | 离婚案件受理费 |
| `personality` | 侵害人格权案件受理费 |
| `other_non` | 其他非财产案件受理费 |
| `ip_no_amount` | 知识产权案件（无争议金额） |
| `ip_with_amount` | 知识产权案件（有争议金额） |
| `labor` | 劳动争议案件受理费 |
| `admin_ip` | 商标/专利/海事行政案件受理费 |
| `admin_other` | 其他行政案件受理费 |
| `jurisdiction` | 管辖权异议费 |
| `enforcement` | 申请执行费（有金额） |
| `enforcement_no` | 申请执行费（无金额） |
| `preservation` | 申请保全措施费 |
| `payment_order` | 申请支付令费用 |
| `public_notice` | 申请公示催告费 |
| `arbitration_set_aside` | 申请撤销仲裁裁决/认定仲裁协议效力费 |
| `bankruptcy` | 破产案件申请费 |
| `maritime_fund` | 申请设立海事赔偿责任限制基金 |
| `maritime_injunction` | 申请海事强制令 |
| `maritime_priority` | 申请船舶优先权催告 |
| `maritime_claim` | 申请海事债权登记 |
| `maritime_average` | 申请共同海损理算 |

### 第三步：呈现结果

以结构化表格或列表输出，包含：
1. 案件类型和计算依据（条款引用）
2. 分段计算明细
财产案件、知识产权有争议金额案件、支付令、执行申请、破产申请应展示各段；区间收费案件至少说明“默认按下限取值”
3. 合计金额
4. 必要的注意事项（幅度费用说明、地方标准提示、减免情形提示）

---

## 注意事项

1. **幅度费用**：离婚、人格权、其他非财产、无争议金额知识产权、管辖权异议、无金额执行申请、部分海事申请等存在上下限。脚本默认取**下限**，输出时必须明确说明不是全国统一固定额。
2. **地方差异**：法定幅度内可能存在地方标准差异；对区间收费，应表述为“按当前默认口径为下限参考值”。
3. **减免情形**：《诉讼费用交纳办法》第十五条规定了减、免、缓的情形（如困难当事人），不纳入自动计算，需提示用户可向法院申请。
4. **精度要求**：输入金额直接按字符串解析为 Python `Decimal`，四舍五入到分（0.01元）。
5. **法律依据引用**：输出结果须标注具体条款与项次。

---

## 参考资料

- `references/litigation-fee-rules.md`：完整条文表格、幅度费用口径和使用提示；需要核对法条范围或提示语时加载。
- `scripts/calc_litigation_fee.py`：核心计算脚本；优先用它计算，不要手写重复公式。
