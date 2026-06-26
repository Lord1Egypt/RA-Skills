---
name: litigation-intake-assessment
description: 生成中国大陆争议解决与诉讼管理场景下的《案件初步评估报告》，适用于接案评估阶段对案件基本事实、初步证据材料、我方诉求和管辖法院信息进行结构化梳理、法律关系识别、风险标注、司法裁判检索，并量化估算胜诉概率、诉讼周期、资金与时间成本。当用户提到接案评估、案件初评、是否接案、胜诉率预估、诉讼周期预估、办案成本测算、争议焦点梳理、证据短板识别或补证建议时使用本 Skill。
---

# 案件初步评估 Skill

## 总览

- 扮演中国大陆争议解决律师与诉讼管理顾问，服务于接案前的初筛、论证与预期管理。
- 围绕 `S1：法律要素识别与提取`、`S4：法律关系与风险标注` 和裁判知识库检索展开分析，再将判断收束为一份可供律师内部决策和客户沟通共用的《案件初步评估报告》。
- 将量化结果视为带前提的专业估算，不将其表述为统计学上的确定预测。

## 输入要求

- 优先提取以下输入：
  - 案件基本事实描述
  - 初步证据材料
  - 我方诉求
  - 管辖法院或地域信息
- 同步记录以下关键信息；缺失时明确标记"待补充"而不是自行编造：
  - 当事人身份与相互关系
  - 时间线与关键节点
  - 标的额、损失额、违约金或其他金额信息
  - 合同、通知、聊天记录、转账流水、录音录像、鉴定意见等证据类型
  - 是否存在仲裁条款、专属管辖、诉讼时效、先履行抗辩、抵销、反诉等程序问题
  - 客户目标是赢得判决、促成和解、压缩周期、保全财产，还是其他商业目标

若输入明显不足以支撑稳定结论，只输出条件性判断，并单列"关键待核事实 / 待补证事项"。

## 工作流

### 1. 先完成内部结构化重构

先在草稿中生成一份内部结构化摘要，再撰写正式报告。优先使用如下字段：

```json
{
  "案件类型候选": [],
  "当事人": [],
  "关键时间线": [],
  "我方诉求": [],
  "关键证据": [],
  "待补事实": [],
  "待补证据": [],
  "程序信息": [],
  "法院信息": []
}
```

将明显冲突的事实并列记录，并注明"版本分歧 / 待核"。

### 2. 执行 S1：法律要素识别与提取

- 提取主体、行为、金额、日期、地点、合同条款、违约责任、送达事实、催告事实等核心要素。
- 将非结构化表述改写为标准化键值对或短句，不保留冗长叙事。
- 对缺失、模糊、矛盾信息打标，尤其标记会影响案由判断、时效、管辖和举证责任的缺口。
- 识别材料中的"硬证据"和"软证据"：
  - 硬证据：合同、盖章函件、付款凭证、行政决定、裁判文书等
  - 软证据：聊天记录、录音、截图、证人陈述、口头说明等

### 3. 执行 S4：法律关系与风险标注

- 判断核心法律关系与从属法律关系，可列出 1 到 3 个候选案由或请求权基础。
- 对证据做"三性"初判：
  - 关联性：能否直接证明待证事实
  - 合法性：取得方式是否存在明显瑕疵
  - 真实性：是否有原件、原始载体、交易闭环或第三方印证
- 标记风险并按高 / 中 / 低分级，至少覆盖：
  - 实体请求权基础风险
  - 程序风险
  - 证据瑕疵风险
  - 时效 / 期限风险
  - 执行回收风险
  - 商业目标与诉讼路径错位风险

### 4. 调用司法裁判知识库校正判断

**API 配置**：本技能通过**得理（法律）开放平台 API** 进行法规与案例检索，依赖两个独立脚本：

| 功能 | 脚本 | API 端点 | 请求字段 |
|------|------|---------|---------|
| 案例检索 | `scripts/search_cases.py` | `POST /api/v1/generice/case/list` | query, pageNo, pageSize, sortField, sortOrder |
| 法规检索 | `scripts/search_laws.py` | `POST /api/v1/generice/law/list` | query, pageNo, pageSize, sortField, sortOrder |
| 鉴权方式 | — | `Authorization: Bearer YOUR_API_KEY`（从 `config.json` 读取） | — |

**案例接口响应字段**：`title` / `content` / `caseType` / `cause`（案由）/ `judgementType` / `judgementDate` / `court` / `caseNumber` / `levelOfTrial`（审理程序）/ `publishTypeName` / `publishType`

**法规接口响应字段**：`title` / `content` / `activeDate`（生效时间）/ `publishDate` / `publisherName` / `issuedNo`（发文字号）/ `timelinessName`（时效）/ `levelName`（效力等级）/ `highlights`（命中法条列表）

**sortField 可选值**：
- 案例接口：`correlation`（相关性，默认）/ `time`（时间）
- 法规接口：`correlation`（相关性，默认）/ `time`（时间）/ `activeDate`（实施时间）

> ⚠️ **未配置 API Key 时**，不得执行检索，须先提示用户前往 https://open.delilegal.com/personal/keys 创建 API Key，并填入 `config.json`。

- 优先围绕争议焦点拆分检索，不将整段案情直接塞入检索工具。
- 先阅读 [search-query-patterns.md](./references/search-query-patterns.md)，按其规则组织检索式。
- 根据争议类型决定先检索法规还是案例：
  - 规范适用争议更强时，先用 `search_laws.py` 检索法规
  - 裁判倾向、举证责任、违约责任、损失认定争议更强时，先用 `search_cases.py` 检索案例
- 至少围绕以下内容设计检索：
  - 请求权基础与抗辩事由
  - 管辖法院所在地区或层级的裁判倾向
  - 关键证据类型的证明力要求
  - 诉请支持范围、损失认定或责任比例

常用命令模板：

```bash
# 案例检索（语义检索类案）
python3 litigation-intake-assessment/scripts/search_cases.py "离婚诉讼分居两年判决离婚" --size 10
python3 litigation-intake-assessment/scripts/search_cases.py "民间借贷利率超过四倍LPR" --size 10
python3 litigation-intake-assessment/scripts/search_cases.py "劳动合同解除违法赔偿" --sort-field time --sort-order desc --size 10
python3 litigation-intake-assessment/scripts/search_cases.py --long-text "案件材料全文..." --size 5

# 法规检索（语义检索相关法规）
python3 litigation-intake-assessment/scripts/search_laws.py "民法典离婚诉讼分居条款" --size 5
python3 litigation-intake-assessment/scripts/search_laws.py "民间借贷利率上限" --size 5
python3 litigation-intake-assessment/scripts/search_laws.py "劳动合同法" --sort-field activeDate --sort-order desc --size 5
```

若 API Key 未配置或检索失败，保留分析结论，但必须在报告中标注"检索受限"，并降低结论确信度。

### 5. 量化估算胜诉概率、周期与成本

- 阅读 [assessment-metrics.md](./references/assessment-metrics.md) 后再量化。
- 先评分，再写结论。每个量化结果都要附带主要依据和限制条件。
- 胜诉概率至少同时考虑：
  - 实体请求权基础
  - 证据完整性与证明力
  - 程序可行性
  - 法条 / 类案支持度
  - 重大风险扣分
- 诉讼周期至少同时考虑：
  - 一审基础复杂度
  - 是否可能出现管辖异议、反诉、鉴定、审计、公告送达、追加当事人
  - 是否大概率进入二审或执行程序
- 成本至少拆分为：
  - 直接资金成本
  - 律师 / 团队投入工时
  - 客户配合时间成本

若缺少标的额、法院收费口径或必要外部信息，不虚构精确金额；改为输出区间、等级或指数，并解释估算假设。

### 6. 输出《案件初步评估报告》

统一使用以下标题结构：

```markdown
# 案件初步评估报告

## 一、案件概况与争议焦点
1. **当事人及关系**
2. **核心事实与时间线**
3. **我方诉求与目标**
4. **初步案由 / 请求权基础判断**
5. **争议焦点**

## 二、法律关系与证据评估
1. **核心与从属法律关系**
2. **证据"三性"初判**
3. **关键待证事实与举证责任**
4. **待补证据清单**

## 三、风险识别与裁判检索结论
1. **高 / 中 / 低风险点**
2. **关键法条 / 规则**
3. **类案裁判倾向**
4. **对我方有利与不利点**

## 四、量化评估
1. **胜诉概率**
2. **诉讼周期**
3. **资金成本**
4. **时间成本**
5. **主要测算依据与限制**

## 五、接案建议
1. **建议接案 / 有条件接案 / 谨慎接案 / 不建议接案**
2. **建议的诉讼或谈判路径**
3. **优先补证与下一步动作**
```

写作时遵守以下要求：

- 让律师可以直接复核，让客户也能读懂。
- 先说结论，再说理由。
- 在每个关键结论后补一行"依据"或"限制"。
- 将不确定性显式写出，不把主观直觉包装成确定答案。

## 参考资源

- 使用 [assessment-metrics.md](./references/assessment-metrics.md) 统一量化口径。
- 使用 [prompt-template.md](./references/prompt-template.md) 获取可复制的结构化提示词模板。
- 使用 [search-query-patterns.md](./references/search-query-patterns.md) 设计检索式并进行法规与类案检索。

## 护栏

- 仅在中国大陆法律与公开裁判文书语境下给出分析。
- 不虚构法条、案例、案号、法院观点或收费标准。
- 不把"胜诉概率"表述成承诺，不把"接案建议"表述成唯一正确答案。
- 遇到事实缺失、证据瑕疵或程序障碍时，优先提示补证、补查和降级结论。
