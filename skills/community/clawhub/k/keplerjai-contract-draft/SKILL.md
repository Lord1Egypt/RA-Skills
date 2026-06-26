---
name: keplerjai-contract-draft
description: 基于 Word 模板和结构化业务信息生成合同草稿。适用于 AI 总助根据现有 .docx 模板起草合同、填充甲乙方与合作信息、识别缺失字段并输出可审阅草稿的场景。
---

# KeplerJAI 合同起草

当目标是“基于现有 Word 模板 + 业务事实生成合同草稿”时使用这份 skill，而不是在没有模板的情况下凭空定稿法律文本。

## 核心分工

1. OpenClaw 负责理解需求、检查模板、起草正文改写方案，并生成结构化 JSON job spec。
2. `scripts/contract_runner.py` 负责稳定执行 `.docx` 修改、输出草稿和校验产物。

当稳定 runner 已能处理任务时，不要再临时生成 `_draft_v1.py`、`_draft_v2.py` 这类一次性脚本。

## 执行主线

默认按以下顺序执行：

1. 检查模板与用户输入
2. 判断需要联动修改的章节
3. 生成一份 UTF-8 编码的 JSON job spec
4. 执行 `python scripts\contract_runner.py --spec <job-spec.json>`
5. 检查生成的 `.docx`、`未决事项清单.md`、`run-summary.json`、`validation-report.json`

一旦 JSON job spec 成功写出：

1. 不要反复重写同一份 spec
2. 必须立刻执行 runner
3. 如果 runner 失败，要返回具体失败点，而不是重复状态文本

## OpenClaw 必须做的事

1. 检查源模板
2. 理解用户请求
3. 判断哪些章节需要联动修改
4. 搜集甲乙方公司介绍，并各自压缩为约 150 字的正式摘要
5. 根据合作主题起草合作内容正文
6. 生成符合 runner 要求的 JSON job spec
7. 检查输出结果并总结汇报

job spec 至少应包含：

- `template_path`
- `party_a` 或 `party_b`
- `cooperation_items`
- `unresolved_items`

如有需要，还应包含：

- `party_b_credit_code`
- `party_a_profile`
- `party_b_profile`
- `global_replacements`
- `paragraph_overrides`
- `leave_blank_fields`
- `agent_id`
- `agent_workspace`
- `output_dir`

如果用户只明确给出了甲方或乙方中的一方，另一方默认可补为 `成都景合开普勒科技有限公司`。  
如果双方都未提供，则不能继续起草。

如果用户没有提供甲乙方介绍，应先检查当前 agent 工作区中的 `MEMORY.md` 与 `memory/` 目录。  
若记忆中已存在准确版本，直接优先使用；仅在记忆中找不到或信息不足时，才通过可用的检索能力补齐。  
优先使用已安装的第三方检索 skill 或搜索工具，例如 Tavily；若无外部检索能力，再根据用户已给事实做审慎摘要，但不要编造履历、资质、融资、专利或政府背书。

如果用户在对话中明确表示“记住”“以后按这个版本用”“作为永久性记忆保存”等含义，应把对应公司介绍或规则写入当前 agent 工作区的永久记忆文件中，并保存到 `memory/` 目录或 `MEMORY.md` 中，供后续合同任务优先复用。

不要再使用旧版简化字段，例如只写 `content_sections` 却不写 `cooperation_items`。  
如果 job spec 未提供 `cooperation_items`，就不能把任务视为“已完成正文起草”。
runner 会自动归一化少数常见输错格式，例如：

- `global_replacements` 被写成单个对象
- `cooperation_items` 中误写成 `title/description`
- `paragraph_overrides` 被写成单个对象

但这只是兜底，不应依赖这种容错。OpenClaw 仍应优先产出标准 schema。  
如果 runner 报出 schema error，应按报错一次性修正后重试；同类 schema 错误不要连续盲改多轮。

## Runner 必须做的事

`scripts/contract_runner.py` 应负责：

1. 读取 `.docx` 模板
2. 更新标题和甲乙方信息
3. 写入甲乙方公司介绍相关段落
4. 做全局旧术语替换
5. 重写合作内容区
6. 应用段落级改写
7. 在目标 agent workspace 下保存新 `.docx`
8. 输出：
   - `未决事项清单.md`
   - `run-summary.json`
   - `validation-report.json`

对于当前示例模板这类“正文语义很重”的合同，runner 不应只做机械替换。

当 job spec 提供了新的合作内容，但未把所有兼容段显式写进 `paragraph_overrides` 时，runner 仍应对关键兼容段执行默认改写，至少覆盖：

1. 鉴于 / 背景
2. 合作原则
3. 甲方权利与义务
4. 乙方权利与义务
5. 合作机制
6. 主体承继或连续性相关段落
7. 知识产权前置归属段落

## 起草边界

1. 保留原有 Word 结构和格式
2. 更新封面及正文中的甲乙方；标题默认保留模板原题，不主动改写
3. 根据搜集到的公司介绍改写背景或鉴于段中的主体描述
4. 根据用户给定主题重写合作内容区
5. 当合作主题变化导致语义不再匹配时，同步修改相关联动段落
6. 保证改写后全文逻辑一致

不要为了让文档“看起来完整”而虚构关键法律事实或商业事实。

敏感或未明确字段默认处理：

1. 身份证号默认留空
2. 签署信息默认留空，除非用户明确提供
3. 未确定日期使用空白或待确认标记
4. 如果主体是机构，不要强行沿用自然人身份证语义

## 强约束

1. 不要把模板改造成新的“第X章 / 第X条”结构，除非模板本来就是这种结构
2. 不要只改合作内容区就停止
3. 不要把旧行业、旧地域、旧主体、旧产品的明显残留原样留在正文里
4. 不要把内部规则抛回给用户重复描述
5. 不要在同一个错误点无限重试

如果一致性检查发现明显残留问题，默认行为应是继续修正并重新生成，而不是先问用户“要不要继续修”。

## 插件与环境

如果任务需要直接调用 Word 插件能力：

1. 先自检 `word-docx` 是否可用
2. 如未安装，优先尝试通过 `clawhub` 自动安装
3. 如未登录 ClawHub，先补齐登录态
4. 只有自动准备明确失败后，才退回纯文本兜底方案

## 路径规则

1. 输出目录应写入 `<agent_workspace>/keplerjai-contract-draft`
2. 优先自动推导 `agent_workspace`
3. 优先使用相对路径、自动推导路径或由配置读取的路径
4. 不要把某台机器上的用户目录、盘符或绝对路径当成默认值
5. skill 安装目录只作为说明和脚本来源，不作为输出目录

## 校验重点

在宣布成功前，至少验证：

1. 确实生成了新的 `.docx`
2. 向用户汇报时给出完整输出文件路径
3. 原模板没有被覆盖
4. 关键输入已经写入草稿
5. 签署页仍然存在
6. 标题保持模板原样，除非用户明确要求改标题
7. 当合作语义发生变化时，关键联动段落也已经同步更新
8. 甲乙方介绍已写入或已在未决事项中明确说明缺失原因

## 参考文件

需要补充上下文时，按需阅读：

- `README.md`
- `scripts/contract_runner.py`
- `references/input-contracting-rules.md`
- `references/runtime-output-contract.md`
- `references/template-analysis.md`
- `references/word-plugin-setup.md`
- `references/iteration-notes.md`
