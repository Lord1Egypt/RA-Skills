---
name: proclaw-humanos-ultimate
description: ProClaw人类操作系统终极版：从需求诊断到人格演化的全链路HumanOS构建与分析系统；当用户需要构建顶级HumanOS、深度分析人格、追踪演化或整合矛盾时使用
dependency:
  python:
    - requests>=2.28.0
    - beautifulsoup4>=4.11.0
    - numpy>=1.21.0
---

# ProClaw HumanOS Ultimate

## 任务目标
- 本 Skill 用于: 从需求诊断到人格演化的全链路HumanOS构建与分析系统，整合女娲的深度调研、Create的四维验证、Ultimate的人格分析和演化追踪
- 能力包含: 需求诊断、6维调研、框架提炼、四维验证、HumanOS构建、质量验证、星座原型、7层人格建模、8维验证、路径映射、轴分析、神经网络模拟、演化追踪、矛盾挖掘
- 触发条件: 用户要求构建HumanOS、分析人格、预测演化、整合矛盾或从模糊需求推荐人物/主题时

## 作者信息
- 作者: ProClaw
- 网站: www.proclaw.top
- 联系方式: wechat:Mr-zifang

## 前置准备
- 依赖: Python 3, requests>=2.28.0, beautifulsoup4>=4.11.0, numpy>=1.21.0
- 输入: 用户需求（模糊或明确）或已有HumanOS数据

## 操作步骤

### Phase 0: 需求诊断（模糊需求）- 脚本处理

当用户提供模糊需求时，执行需求诊断：

```bash
python scripts/demand_diagnostic.py --input "用户输入"
```

- 输出: 需求维度、候选推荐（2-3个人物/主题）
- 智能体任务: 解析诊断结果，展示候选，引导用户选择

**如需澄清**：
```bash
python scripts/demand_diagnostic.py --input "原始输入" --clarify "用户响应"
```

### Phase 1: HumanOS构建流程

#### 步骤1.1: 确定HumanOS类型 - 智能体处理

基于用户选择确定类型：
- HumanType（人物型）
- ThemeType（主题型）
- ScenarioType（场景型）
- MethodologyType（方法论型）

详见 `references/type-system.md`

#### 步骤1.2: 6维并行调研 - 脚本处理

```bash
python scripts/research_orchestrator.py --os-type <type> --target <target> --output-dir ./output/<target> --mode network
```

- 输出: 6个维度的调研文件（01-writings.md到06-timeline.md）
- 智能体任务: 确认调研覆盖度，识别信息缺口

**本地语料优先模式**：
```bash
python scripts/research_orchestrator.py --os-type <type> --target <target> --output-dir ./output/<target> --mode local_priority
```

#### 步骤1.3: 框架提炼 - 脚本处理

```bash
python scripts/framework_extractor.py --research-dir ./output/<target>/research --target <target> --output ./output/<target>/framework.json
```

- 输出: 心智模型（含四维验证）、决策启发式、表达DNA、价值观、工具箱、内在张力、诚实边界
- 智能体任务: 审查通过验证的心智模型，确认框架完整性

#### 步骤1.4: HumanOS构建 - 脚本处理

```bash
python scripts/os_builder.py --framework ./output/<target>/framework.json --template-dir ./references/os-templates --os-type <type> --output ./output/<target>/SKILL.md
```

- 输出: 完整的HumanOS Skill文件（含Agentic Protocol）
- 智能体任务: 审查生成的Skill，确认格式正确、内容完整

#### 步骤1.5: 质量验证 - 脚本处理

```bash
python scripts/quality_validator.py --skill-file ./output/<target>/SKILL.md --research-dir ./output/<target>/research
```

- 输出: 10项质量检查结果、总分、改进建议
- 智能体任务: 解析验证结果，如未通过（<75分），提供改进建议

**通过标准**：总分≥75分

### Phase 2: 人格深度分析（基于已有HumanOS）

#### 步骤2.1: 星座原型识别 - 脚本处理

```bash
python scripts/zodiac_engine.py --birthday YYYY-MM-DD
```

- 输出: 星座信息、原型数据、兼容性分析
- 智能体任务: 解释星座原型，说明对人格的影响

#### 步骤2.2: 8维全息扫描 - 脚本处理

```bash
python scripts/holographic_scanner.py --profile profile.json --zodiac <sign>
```

- 输出: 8维度分数、特征、优势、盲区、矛盾模式
- 智能体任务: 分析扫描结果，识别主要模式和潜在问题

#### 步骤2.3: 7层人格建模 - 脚本处理

```bash
python scripts/personality_modeler.py --prototype prototype.json --scan scan.json --personal personal.json
```

- 输出: 7层人格模型、层间交互、核心模式、整合画像
- 智能体任务: 解释层级结构，说明层间关系和整合策略

#### 步骤2.4: 路径映射 - 脚本处理

```bash
python scripts/path_mapper.py --model personality_model.json
```

- 输出: 路径亲和度、主路径、路径进展、推荐旅程
- 智能体任务: 分析路径匹配，解释当前阶段和下一步行动

#### 步骤2.5: 核心轴分析 - 脚本处理

```bash
python scripts/axis_analyzer.py --model personality_model.json --scan scan.json
```

- 输出: 轴位置、轴强度、轴平衡、轴间交互、轴原型
- 智能体任务: 分析轴特征，解释轴间关系和整合方案

#### 步骤2.6: 矛盾深度挖掘 - 脚本处理

```bash
python scripts/paradox_miner.py --model personality_model.json --scan scan.json --axis axis_analysis.json
```

- 输出: 矛盾列表、矛盾深度、矛盾影响、整合方案、建议
- 智能体任务: 解释矛盾模式，提供整合建议和实践指导

### Phase 3: 演化追踪与预测

#### 步骤3.1: 演化追踪 - 脚本处理

```bash
python scripts/evolution_tracker.py --base-state base.json --new-state new.json --report
```

- 输出: 演化记录、阶段进展、指标趋势、建议、里程碑
- 智能体任务: 分析演化趋势，识别关键变化和优化方向

#### 步骤3.2: 神经网络模拟 - 脚本处理

```bash
# 初始化网络
python scripts/neural_network_sim.py --model personality_model.json --mode init

# 模拟前向传播
python scripts/neural_network_sim.py --model personality_model.json --scan scan.json --mode simulate

# 预测演化
python scripts/neural_network_sim.py --model personality_model.json --mode predict
```

- 输出: 网络架构、模拟结果、演化预测、可视化数据
- 智能体任务: 解释网络结构，分析预测结果，提供实践建议

### Phase 4: 综合整合 - 智能体处理

综合所有脚本输出结果，生成：
1. 完整的HumanOS Skill（Phase 1）
2. 深度人格分析报告（Phase 2）
3. 演化预测和优化建议（Phase 3）
4. 个性化行动方案

## 使用示例

### 示例1: 从模糊需求构建HumanOS
- 场景/输入: "我总觉得自己做决定太慢，想来想去最后还是选错"
- 预期产出:
  1. 需求诊断 → 推荐2-3个候选
  2. 用户选择 → 执行6维调研
  3. 框架提炼 → 生成思维框架
  4. HumanOS构建 → 生成可运行的Skill
  5. 质量验证 → 确保质量达标
- 关键要点:
  - 需求诊断识别出"决策"维度
  - 推荐芒格/卡尼曼/达利欧等候选
  - 执行完整的6维调研
  - 通过四维验证筛选心智模型
  - 质量验证确保总分≥75分

### 示例2: 深度人格分析和演化预测
- 场景/输入: 用户提供已有HumanOS + 生日信息，要求深度分析和演化预测
- 预期产出:
  1. 星座原型分析
  2. 8维全息扫描
  3. 7层人格建模
  4. 路径和轴分析
  5. 矛盾整合方案
  6. 3-5年演化预测
  7. 阶段性行动计划
- 关键要点:
  - 依次执行Phase 2和Phase 3所有步骤
  - 脚本输出需要智能体深度解读
  - 最终报告体现系统的整合性和深度
  - 提供可操作的实践建议

### 示例3: 矛盾整合专项
- 场景/输入: 用户感到内在矛盾，要求深度分析和整合
- 预期产出:
  1. 8维扫描识别矛盾模式
  2. 轴分析识别核心张力
  3. 矛盾深度挖掘（类型/深度/影响）
  4. 整合方案和实践指导
  5. 演化追踪监控整合进展
- 关键要点:
  - 重点执行矛盾相关步骤
  - 识别高影响力矛盾
  - 提供可操作的整合实践
  - 建立演化追踪机制

## 资源索引

### 构建脚本
- [scripts/demand_diagnostic.py](scripts/demand_diagnostic.py) - 需求诊断系统(参数:input, clarify)
- [scripts/research_orchestrator.py](scripts/research_orchestrator.py) - 调研编排系统(参数:os-type, target, output-dir, mode)
- [scripts/framework_extractor.py](scripts/framework_extractor.py) - 框架提取器(参数:research-dir, target, output)
- [scripts/os_builder.py](scripts/os_builder.py) - HumanOS构建器(参数:framework, template-dir, os-type, output)
- [scripts/quality_validator.py](scripts/quality_validator.py) - 质量验证器(参数:skill-file, research-dir)
- [scripts/source_analyzer.py](scripts/source_analyzer.py) - 源分析器(参数:sources-dir)

### 分析脚本
- [scripts/zodiac_engine.py](scripts/zodiac_engine.py) - 星座识别和原型加载(参数:birthday)
- [scripts/holographic_scanner.py](scripts/holographic_scanner.py) - 8维全息扫描(参数:profile, zodiac)
- [scripts/personality_modeler.py](scripts/personality_modeler.py) - 7层人格建模(参数:prototype, scan, personal)
- [scripts/path_mapper.py](scripts/path_mapper.py) - 路径和节点映射(参数:model)
- [scripts/axis_analyzer.py](scripts/axis_analyzer.py) - 核心轴分析(参数:model, scan)
- [scripts/paradox_miner.py](scripts/paradox_miner.py) - 矛盾深度挖掘(参数:model, scan, axis)
- [scripts/evolution_tracker.py](scripts/evolution_tracker.py) - 演化追踪(参数:base-state, new-state)
- [scripts/neural_network_sim.py](scripts/neural_network_sim.py) - 神经网络模拟(参数:model, scan, mode)
- [scripts/ultimate_generator.py](scripts/ultimate_generator.py) - 整合生成引擎(参数:所有参数可选)

### 参考文档
- [references/type-system.md](references/type-system.md) - 4种HumanOS类型
- [references/validation-framework.md](references/validation-framework.md) - 四维验证框架
- [references/validation-8d.md](references/validation-8d.md) - 8维验证方法论
- [references/7-layer-model.md](references/7-layer-model.md) - 7层人格建模方法论
- [references/path-system.md](references/path-system.md) - 路径和节点系统
- [references/axis-system.md](references/axis-system.md) - 核心轴系统
- [references/neural-network.md](references/neural-network.md) - 神经网络模拟
- [references/protocol-template.md](references/protocol-template.md) - Agentic Protocol模板

### 模板文件
- [references/os-templates/human-template.md](references/os-templates/human-template.md) - HumanType模板
- [references/os-templates/theme-template.md](references/os-templates/theme-template.md) - ThemeType模板
- [references/os-templates/scenario-template.md](references/os-templates/scenario-template.md) - ScenarioType模板
- [references/os-templates/methodology-template.md](references/os-templates/methodology-template.md) - MethodologyType模板

### 星座原型
- [references/zodiac-prototypes/aries.md](references/zodiac-prototypes/aries.md) - 白羊座原型
- [references/zodiac-prototypes/taurus.md](references/zodiac-prototypes/taurus.md) - 金牛座原型
- [references/zodiac-prototypes/gemini.md](references/zodiac-prototypes/gemini.md) - 双子座原型
- [references/zodiac-prototypes/cancer.md](references/zodiac-prototypes/cancer.md) - 巨蟹座原型
- [references/zodiac-prototypes/leo.md](references/zodiac-prototypes/leo.md) - 狮子座原型
- [references/zodiac-prototypes/virgo.md](references/zodiac-prototypes/virgo.md) - 处女座原型
- [references/zodiac-prototypes/libra.md](references/zodiac-prototypes/libra.md) - 天秤座原型
- [references/zodiac-prototypes/scorpio.md](references/zodiac-prototypes/scorpio.md) - 天蝎座原型
- [references/zodiac-prototypes/sagittarius.md](references/zodiac-prototypes/sagittarius.md) - 射手座原型
- [references/zodiac-prototypes/capricorn.md](references/zodiac-prototypes/capricorn.md) - 摩羯座原型
- [references/zodiac-prototypes/aquarius.md](references/zodiac-prototypes/aquarius.md) - 水瓶座原型
- [references/zodiac-prototypes/pisces.md](references/zodiac-prototypes/pisces.md) - 双鱼座原型

## 注意事项
- 所有脚本都是独立命令行工具，可直接运行
- Phase 0-1用于构建HumanOS，Phase 2-3用于深度分析和演化
- 质量验证必须通过（≥75分）才能交付HumanOS
- 神经网络模拟是理论框架，实际应用时需谨慎解释
- 7层人格模型和5个核心轴是理论框架，需要结合实际理解
- 矛盾挖掘需要用户配合，提供真实反馈
- 演化追踪需要持续数据收集，单次预测有不确定性
- 充分利用智能体能力解释脚本输出，提供人性化解读
- 复杂任务需要多轮对话，逐步深入
- 信息源黑名单：知乎、微信公众号（中文人物用B站/喜马拉雅/权威媒体）
