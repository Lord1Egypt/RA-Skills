---
name: advanced-prompt-engineering-template
version: 5.6.0
description: 基于原子化深度动态适配的提示词工程框架,lite骨架零成本直出加全量组合按需组装,DEPTH指纹可复现可调档,当用户需要生成各类结构化提示词、按任务复杂度定制提示词深度或迭代调优既有提示词时使用
---

# 高阶提示词工程模版 v5.6(原子化深度动态适配)

## 任务目标

- 将用户自然语言需求转换为"AI 拿到即可执行"的完整结构化提示词。
- 能力:深度基调判定、原子筛选组合、覆盖调档、指纹复现、契约门禁。
- 触发:用户要求生成/优化/分级提示词,或要求将模糊需求转为专业提示词。

## 路由速查(完整规则见 [references/routing-protocol.md](references/routing-protocol.md))

```
0. 能力边界预判:命中 C1-C5(需实时数据/需执行动作/需确定性计算/
   需运行时编排/超认知边界)→ 路由D:说明限制,给降级·转交·拆分三路径,
   不产出指纹;未命中才继续
1. 信息完整性检查:四要素(场景/受众/目标/形式)缺项先追问(最多2问)
2. 基调计分:复杂度信号(0-5分)+ 风险信号(0-3分)
   0-1分短小任务 → 路由A:用下方 LITE 骨架直出
   0-1分有结构  → 路由B:B1 指纹 [1×9]
   2-3分        → 路由B:B2 指纹 [2×9]
   4-5分        → 路由B:B3 指纹 [3×9]
   含风险信号或6分+ → 路由B:B4 指纹 [4×9]
   注:[n×9] 为简写,表示 9 个核心原子全部取该档位;核心原子位序见 depth-adaptation.md
3. 覆盖检查:存在 depth-adaptation.md 触发信号时单原子调档(≤3位)
4. 组装:按 composition-manifest.md 八步流程执行,产出头部写 DEPTH 指纹
5. 后缀适配(可选):指纹可加 @model=<id>(选 model-adapters/<id>.md 改写
   段落形态并尾部追加注入模块)、@lang=zh|en|bilingual、@tokens=<预算>;
   后缀只改表达形态与预算,不改任何一位档位;未指定则跳过
6. 迭代调档时先用 scripts/fingerprint.py diff 评估影响面,再决定重生成范围
```

## 七维质量速查表(组装产出前逐维核对,原子映射见 manifest 第 8 步(门禁自检))

| 维度 | 要求 | 权重 | 对应原子 |
|------|------|------|----------|
| 清晰度与明确性 | 零模糊词,量化到数字 | 20% | task-define, constraints |
| 结构化组织 | 五段式分层(角色/任务/上下文/格式/思考指令) | 15% | format-spec |
| 上下文与示例 | 数据标来源,示例贴合场景 | 15% | context-inject, example-shot |
| 约束与成功标准 | 正负面清单明确,标准可验证 | 15% | constraints, self-check |
| 深度推理引导 | 按指纹档位启用对应思考框架 | 15% | think-chain |
| 自校正机制 | 按指纹档位启用清单/评分/对抗验证 | 10% | self-check, iterate |
| 语气风格控制 | 风格显式定义且全程一致 | 10% | role-anchor, format-spec |

## LITE-1 骨架(路由A 直出用,零额外加载;豁免声明见 depth-adaptation.md)

### LITE 骨架(基调 B1:单一明确短任务)

```
你是[领域]专家。任务:[一句话目标+交付形式]。
要求:[3条核心约束]。
输出:[形式+字数]。如需调整请说明。
```

## 使用示例

- 示例1(路由A):输入"写一封50字的会议提醒" → 0分且短小 → LITE 骨架直出,零额外加载。
- 示例2(路由B+B3):输入"做一份国内新能源汽车市场调研报告" → 4分 → 组装:基调 B3 指纹 [3×9],域注入 consulting(行业调研咨询属性),输出注入 text-doc+chart-desc → 产出头部含 `DEPTH: [3,3,3,3,3,3,3,3,3]`。
- 示例3(调档迭代):对示例3 产出(B4 秒杀系统)反馈"约束再严格些" → constraints 已处 D4 顶档,按 depth-adaptation.md 覆盖触发表"顶档"行处理(位不变-内容增强或改调关联原子),优化日志记录变更。完整过程见 [references/complete-examples.md](references/complete-examples.md) 示例3。

## 资源索引

- 路由协议:见 [references/routing-protocol.md](references/routing-protocol.md)(何时读取:判定基调与边界场景处理时)
- 全局架构:见 [references/architecture.md](references/architecture.md)(何时读取:新增/修改原子·步骤·校验族之前,排查跨文件脱节时;含唯一真相源对照表与升级同步检查单)
- 组合清单:见 [references/composition-manifest.md](references/composition-manifest.md)(何时读取:路由B组装前必读,含组装八步与判定信号表)
- 深度适配协议:见 [references/depth-adaptation.md](references/depth-adaptation.md)(何时读取:处理覆盖调档、依赖规则、新增原子扩展时)
- 组合示例:见 [references/complete-examples.md](references/complete-examples.md)(何时读取:需要组装参照时)
- 质量指标:见 [references/quality-metrics.md](references/quality-metrics.md)(何时读取:产出后需自动核验七维可计算子集时)
- 回归基线:见 [references/benchmark/cases.yaml](references/benchmark/cases.yaml)(何时读取:改原子后需比对产出快照时)
- 使用指南:见 [references/usage-guide.md](references/usage-guide.md)(何时读取:首次接入本 Skill 或需要完整操作速查时)
- 变更记录:见 [references/changelog.md](references/changelog.md)(何时读取:版本升级、追溯修复历史时)
- PromptIR 规范:见 [references/prompt-ir.md](references/prompt-ir.md)(何时读取:同一提示词需适配多模型形态、或做结构化解析改写时)
- 提示词包协议:见 [references/prompt-package.md](references/prompt-package.md)(何时读取:复杂任务需拆解为主提示词+子任务编排时)
- 原子注册中心:见 [references/registry/atom-registry.yaml](references/registry/atom-registry.yaml)(何时读取:跨 Skill 复用原子、新增或重命名原子时)
- 模型适配:见 [references/model-adapters/](references/model-adapters/)(5个适配器;何时读取:用户指定目标模型时,按 @model=<id> 取用)
- 核心原子:见 [references/atoms/core/](references/atoms/core/)(9个,每个含 D1-D4 四段;组装时按指纹取对应段)
- 域原子:见 [references/atoms/domains/](references/atoms/domains/)(9个领域,按判定信号表匹配注入)
- 输出原子:见 [references/atoms/outputs/](references/atoms/outputs/)(10种输出类型,按判定表匹配注入)
- 契约门禁:见 [scripts/validate_skill.py](scripts/validate_skill.py)(用途:校验原子契约/深度段/指纹/依赖规则/信号表;运行:`python scripts/validate_skill.py --skill-dir . --strict`)
- 门禁测试:见 [scripts/test_validate_skill.py](scripts/test_validate_skill.py)(用途:门禁自身正反用例回归;运行:`python scripts/test_validate_skill.py`)
- 产出评分:见 [scripts/score_prompt.py](scripts/score_prompt.py)(用途:产出提示词的七维可计算指标评分;运行:`python scripts/score_prompt.py --prompt-file out.md --depth 3,3,3,3,3,3,3,3,3`)
- 指纹工具:见 [scripts/fingerprint.py](scripts/fingerprint.py)(用途:指纹解析/哈希/差异比对;运行:`python scripts/fingerprint.py diff "<旧指纹>" "<新指纹>"`)
- 注册生成:见 [scripts/gen_registry.py](scripts/gen_registry.py)(用途:从 atoms/ 目录实证生成 atom-registry.yaml;运行:`python scripts/gen_registry.py`)
- 归档资产:见 [assets/](assets/)(用途:历史跟踪表 TODO.md、外来方案文档 api-docs 与内部审计归档 .workbuddy 的收纳目录,非运行时资源;仅追溯历史时读取)

## 注意事项

- 原子文件是唯一真相源:任何文档不得复制原子内容,分歧时以 atoms/ 目录为准。
- DEPTH 指纹必须写入产出头部;迭代调档后同步更新指纹与优化日志。
- 依赖规则 R1-R5 违反时修正指纹后再组装,禁止产出非法组合。
- 产出提示词内部标点统一使用中文标点,禁止中英混排(代码块与公式除外);指纹带 `@lang=en/bilingual` 时改按 depth-adaptation.md"@lang 处理规则"执行。
- 新增原子/领域/输出/深度档时,严格按 depth-adaptation.md 扩展指南执行并运行门禁。
- 仅在需要时读取参考与原子文件,保持上下文简洁;路由A 场景零额外加载。
