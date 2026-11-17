# 使用指南(README 等价物)

## 目录

- 概览
- 六步路由速查(含第零步能力边界预判)
- 门禁命令
- 目录结构
- 扩展入口

## 概览

本 Skill 将自然语言需求转换为可执行的结构化提示词,核心机制是"深度动态适配":按任务复杂度判定基调 B1-B4,从 28 个原子注册库组装出定制模板,产出头部携带 DEPTH 指纹与 FP-HASH 保证可复现可审计。本文档是面向使用者的完整速查,与 SKILL.md 资源索引同源同步。

## 六步路由速查(含第零步,详见 routing-protocol.md R10 节)

0. 能力边界预判(R10):需求命中 C1 需实时/外部数据、C2 需执行副作用、C3 需确定性计算、C4 需运行时编排、C5 超出认知边界任一类 → 走**路由 D**(说明限制 + A 降级/B 转交/C 拆分),不产出 DEPTH 指纹;未命中才继续。
1. 信息检查:核心四要素(场景/受众/目标/输出)齐全?缺则按优先级追问,上限 2 问。
2. 特征计分:复杂度信号 0-5 分 + 风险信号 0-3 分(含高专业门槛、技术密集),完整信号表见 [routing-protocol.md](routing-protocol.md)。
3. 基调映射:0-1 分→B1(复杂短小需求走"产出短小"分流,见 LITE 骨架),2-3 分→B2,4-5 分→B3,6 分以上或有风险信号→B4。
4. 路由执行:0-1 分且短小(预计产出不超过 200 字、无章节结构)走 LITE-1 直出;其余按 composition-manifest.md **八步组装**。
5. 深度复核:产出头部必须带 DEPTH 指纹(建议附 FP-HASH,追溯规范见 depth-adaptation.md"指纹哈希");用户反馈时按 depth-adaptation.md 覆盖触发调档(含顶档分支)。
6. 迭代调档:先用 `python scripts/fingerprint.py diff "<旧指纹>" "<新指纹>"` 评估影响面,再仅重生成对应模块。

## 门禁命令

- 校验:`python scripts/validate_skill.py --skill-dir . --strict`(退出码 0 为通过;校验族覆盖 CR/DP/MF/FM/LT/TB/BN/FP/MA/QL/RB/IR/PK/RG/DH 等,详见脚本头注释)
- 门禁自测:`python scripts/test_validate_skill.py`(正反用例回归,含 RB007/RB003 双向、FP010 漂移、DH005 目录盲区、@lang 哈希等价)
- 产出评分:`python scripts/score_prompt.py --prompt-file out.md --depth 3,3,3,3,3,3,3,3,3`(七维可计算指标)

## 目录结构

```
SKILL.md                  # 入口:六步路由速查 + 七维表 + LITE-1 骨架 + 资源索引
scripts/validate_skill.py      # 契约门禁(多族校验,唯一校验真相源)
scripts/test_validate_skill.py # 门禁自测用例(9 例)
scripts/score_prompt.py        # 七维产出评分(R01)
scripts/fingerprint.py         # 指纹解析/哈希/diff(R02/R07)
scripts/gen_registry.py        # atom-registry.yaml 生成器(R08,实证生成)
references/routing-protocol.md # 第零步 + 六步判定 + 边界场景 + 能力边界预判(R10)
references/composition-manifest.md # 组装八步 + 域/输出判定信号表
references/depth-adaptation.md     # 深度语义锚 + 指纹/哈希/@lang + 覆盖触发(含顶档) + 依赖规则 R1-R5 + 扩展指南
references/quality-metrics.md      # 七维质量阈值表(R01)
references/prompt-ir.md            # PromptIR 中间层规范(R05 v0)
references/prompt-package.md       # 提示词包协议(R06 v0)
references/complete-examples.md    # 完整示例(含指纹与调档迭代)
references/usage-guide.md          # 本文档
references/changelog.md            # 变更记录
references/atoms/core/   # 9 个核心原子(各含 D1-D4 深度段,头部 deps 声明)
references/atoms/domains/ # 9 个域原子
references/atoms/outputs/ # 10 个输出原子
references/benchmark/cases.yaml     # 回归基线 12 条(R03,含 boundary_precheck 字段)
references/benchmark/snapshots/     # 产出快照(12 条,含 FP-HASH)
references/benchmark/model-samples/ # 5 组多模型产出样本(R05)
references/registry/atom-registry.yaml # 原子注册中心(28 原子,RG006 校验 deps)
references/model-adapters/ # 5 个模型适配器(claude/openai/gemini/deepseek/qwen)
assets/                    # 归档资产(历史 TODO 与外来方案文档,非运行时资源)
```

## 扩展入口(新增原子三步)

1. 创建原子文件至对应目录(core 需含 D1-D4 四段与质量清单,头部 deps 字段按参与规则声明;domain/output 单段正交),头部带 ATOM 声明与唯一真相源声明。
2. 在 composition-manifest.md 对应判定信号表登记原子名与判定信号(信号词以判定表为准)。
3. 运行门禁:DP007/CR010 校验位序一致,MF011 强制登记,RG006 校验 deps 与依赖规则反查一致;新增核心原子须同步 depth-adaptation.md 位序表与 CORE_ATOM_KEYS(唯一定义点,其余脚本引用该常量),并在质量清单标注指纹位号。
