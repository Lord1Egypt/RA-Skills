---
name: ip-full-detection
description: 全方位知识产权检测流程（带 AIGC 预筛）：输入一个亚马逊 ASIN，自动拉取产品详情后，先用 AIGC 多模态大模型对 6 项 IP 风险做零积分预筛（明确有风险→直接标记、明确无风险→直接放行），仅对模棱两可的项调用睿观专业检测消耗积分，最终汇总风险评级并生成 HTML 报告。当用户说"IP 全检测"、"知识产权排查"、"查侵权"、"商标专利版权全面检查"、"product IP check"、"full IP screening"、" infringement scan"、"查一下这个产品有没有侵权风险"、"上架前合规检测"、"全方位知识产权查询"、"IP risk assessment"时触发。即使用户只说"帮我查查这个 ASIN 能不能卖"或"这个产品有没有知识产权风险"，也应触发。
---

## 适用场景

输入一个亚马逊 ASIN，先用 AIGC 多模态大模型零积分预筛 6 项 IP 风险，仅对模糊项调用专业工具检测，输出风险评级报告。适用于上架前合规排查、选品阶段侵权风险评估、竞品 IP 分析。

| 场景 | 说明 |
|------|------|
| 上架前 IP 排查 | 新品上架前全面检查商标/专利/版权/政策合规风险 |
| 选品阶段风险评估 | 候选产品知识产权风险快速筛查，辅助选品决策 |
| 竞品 IP 分析 | 对竞品 ASIN 做 IP 检测，了解竞品知识产权布局 |

## 核心策略：AIGC 预筛 → 按需专业检测

利用多模态大模型的接地搜索与推理能力 + 世界级知识库，最大化前置过滤，最小化积分消耗：

| AIGC 预筛结论 | 处理方式 | 积分消耗 |
|---------------|---------|---------|
| 明确有风险 | 直接标记风险，跳过专业工具 | 零 |
| 明确无风险 | 直接放行，跳过专业工具 | 零 |
| 模棱两可 | 进入第二层专业工具检测 | 消耗 |

## 不适用

- 只想查单项 IP（如只查商标）——直接调对应睿关 skill 即可
- 非亚马逊平台产品——本流程依赖 amazon-product-detail 拉取信息
- 已知专利号需查专利详情——用智慧芽系列 skill

## 输入参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| asin | string | 必填 | 亚马逊 ASIN（如 B0GQBDQF5R） |
| region | string | US | 检测区域代码，影响商标/专利检测范围 |

## 已挂载能力约束

| skill | 用途 | 调用位置 | 状态 |
|-------|------|----------|------|
| linkfox-amazon-product-detail | 拉 ASIN 产品详情（标题、主图、五点描述） | S1 | 已挂载 |
| linkfox-aigc-textgen | AIGC 多模态预筛（图片理解 + 文本推理） | S2 | 已挂载 |
| linkfox-ruiguan-text-trademark-detection | 文字商标检测（仅 S3 模糊项触发） | S3 | 已挂载 |
| linkfox-ruiguan-trademark-graphic-detection | 图形商标检测（仅 S3 模糊项触发） | S3 | 已挂载 |
| linkfox-ruiguan-utility-patent-detection | 实用新型/发明专利检测（仅 S3 模糊项触发） | S3 | 已挂载 |
| linkfox-ruiguan-detection-patent-design | 外观设计专利检测（仅 S3 模糊项触发） | S3 | 已挂载 |
| linkfox-ruiguan-copyright-detection | 版权检测（仅 S3 模糊项触发） | S3 | 已挂载 |
| linkfox-ruiguan-gun-parts-search | 政策合规检测（仅 S3 模糊项触发） | S3 | 已挂载 |
| linkfox-report-generator | 报告样式、排版、HTML 导出 | S5 | 已挂载 |

## 执行编排

- **第 1 层**：S1 拉取产品详情 —— 后续所有检测依赖此步输出的标题和图片 URL。
- **第 2 层（并行）**：S2 用 AIGC 多模态大模型同时对 6 项 IP 风险做预筛 —— 零积分成本，6 项并行调用 `linkfox-aigc-textgen`，每项返回 `RISK` / `CLEAN` / `AMBIGUOUS` 三态判定。
- **第 3 层（条件并行）**：S3 仅对 S2 判定为 `AMBIGUOUS` 的项发起专业睿观检测 —— 只有模糊项消耗积分，明确项直接采用 AIGC 结论。
- **第 4 层**：S4 合并 AIGC 预筛结论 + 专业检测结果，统一计算每项风险等级与总体风险。
- **第 5 层**：S5 生成 HTML 报告 —— 包含 AIGC 预筛概览 + 专业检测详情。

## 流水线

| 步骤 | 做什么（一句话） | 依赖 | 用途 | 详情 |
|------|----------------|------|------|------|
| S1 拉取产品详情 | 调 amazon-product-detail 获取标题、主图 URL、五点描述 | 无 | 为 S2/S3 提供输入参数 | `references/steps/S1.md` |
| S2 AIGC 多模态预筛 | 并行调 linkfox-aigc-textgen 对 6 项 IP 风险做零积分预筛 | S1 | 三态判定（RISK/CLEAN/AMBIGUOUS），过滤出需专业检测的模糊项 | `references/steps/S2.md` |
| S3 条件专业检测 | 仅对 S2 判定 AMBIGUOUS 的项并行发起睿观 IP 检测 | S2 | 精准兜底，仅模糊项消耗积分 | `references/steps/S3.md` |
| S4 汇总风险评估 | 合并 AIGC 预筛 + 专业检测结果，统一计算风险评级 | S3 | 结构化数据供 S5 报告生成 | `references/steps/S4.md` |
| S5 生成报告 | 调 linkfox-report-generator 生成 HTML 报告 | S4 | 最终交付物 | `references/steps/S5.md` |

## 报告产物

每次执行后生成一份 HTML 报告，包含：

- **AIGC 预筛概览**：6 项预筛结论一览表（RISK/CLEAN/AMBIGUOUS），标注哪些项跳过了专业检测
- **总体风险评级与风险矩阵概览**：以表格展示 6 项检测的最终风险等级
- **每项检测详细结果**：独立章节，含风险等级标签（LOW/MODERATE/HIGH/CLEAN）
- **高风险项重点标注**：radar same=true 的专利、sim>=0.7 的专利、TRO flagged 项、blacklist 匹配项
- **积分节省统计**：展示因 AIGC 预筛而跳过的专业检测数量
- **综合行动建议**：按优先级排序

报告数据来源：
- 产品信息：S1 输出
- AIGC 预筛结论：S2 输出
- 专业检测结果：S3 输出（仅模糊项）
- 风险评级：S4 计算结果

> **如果需要生成报告 / 精美报告，必须去阅读 SKILL `linkfox-report-generator`，根据它的规范来。**
> 本 skill 只准备业务数据；样式、排版、md/html 导出、元信息块统统由 `linkfox-report-generator` 负责。
> 不要在此处复制报告样式或 html 模板。

## 执行自检

每次跑完流程，agent 在收尾时确认：

- [ ] AIGC 预筛 6 项全部返回有效判定（RISK/CLEAN/AMBIGUOUS），否则该项默认 AMBIGUOUS 进入专业检测
- [ ] S3 仅对 AMBIGUOUS 项发起专业检测，未对 RISK/CLEAN 项浪费积分
- [ ] 被 AIGC 判定为 RISK 的项已在报告中标注"AIGC 预筛风险"
- [ ] 被 AIGC 判定为 CLEAN 的项已在报告中标注"AIGC 预筛放行"
- [ ] 专业检测项全部返回非空数据（errcode=200），否则在报告局限性章节注明失败项
- [ ] 外观设计专利的 radar same=true 结果已重点标注
- [ ] 实用新型专利 sim>=0.7 的有效专利已列出
- [ ] 总体风险等级取最高单项风险等级
- [ ] 报告路径和数据文件路径已完整输出给用户

## 已知局限

- AIGC 预筛基于大模型推理，不访问实时专利/商标数据库；对冷门产品或复杂结构可能判断为 AMBIGUOUS
- 实用新型专利检测目前仅支持 US 区域
- 各专业检测 skill 有积分消耗成本，同一会话同一参数组合只调用一次（24h 本地缓存）
- 检测结果基于算法相似度匹配，不构成法律意见；建议咨询专业 IP 律师做最终判断
- 产品图片质量影响 AIGC 预筛和专业检测的准确度
