# keplerjai-contract-draft

这份 skill 现在采用清晰的两段式工作流：

1. OpenClaw 负责理解业务需求，并整理出结构化的 job spec。
2. `scripts\contract_runner.py` 负责稳定地修改 Word 模板，并把草稿写入当前 agent 工作区。

## 这个目录的作用

这个 skill 目录主要存放：

- 工作流规则
- 可复用参考说明
- 稳定的 Word 执行脚本
- 便于排障和迭代的操作说明

它不应该被当作主要的运行输出目录。

## 运行输出原则

运行产物应写入目标 agent 工作区下的同名目录：

`<agent_workspace>/keplerjai-contract-draft`

实际执行时，runner 应优先从 OpenClaw 本机配置中的 agent workspace 自动推导输出目录，而不是依赖某台机器上的固定用户目录、盘符或绝对路径。

常见输出包括：

- 生成后的合同草稿 `.docx`
- `未决事项清单.md`
- `run-summary.json`
- `validation-report.json`

生成文件名应统一遵循同一套规则：

- 默认：`<模板标题>_草稿.docx`
- 如果同名文件已存在：`<模板标题>_草稿_v2.docx`、`<模板标题>_草稿_v3.docx`，依次递增

## 职责分工

### OpenClaw / Skill

OpenClaw 负责做判断型工作：

- 理解用户的合同起草需求
- 在需要时检查模板结构
- 判断哪些章节需要联动修改
- 起草合作内容正文
- 为 runner 准备结构化 JSON job spec

### Python Runner

`scripts\contract_runner.py` 负责做确定性执行：

- 打开 `.docx` 模板
- 更新标题和甲乙方信息
- 做全局旧术语替换
- 重写合作内容区
- 对受影响的其他段落执行定向改写
- 另存为新草稿，不覆盖原模板
- 输出校验和未决事项产物

## 主要文件

- `SKILL.md`
  这份 skill 的核心规则说明
- `scripts\contract_runner.py`
  稳定的 Word 草稿执行器
- `references\input-contracting-rules.md`
  输入约束和起草边界
- `references\runtime-output-contract.md`
  输出目录约束
- `references\iteration-notes.md`
  真实运行中总结出的失败模式与经验

## 插件准备

如果当前任务需要直接调用 Word 插件能力，OpenClaw 应先自行检查 `word-docx` 是否已安装。

默认顺序应是：

1. 检查 `word-docx` 是否已可用
2. 如未安装，尝试通过 `clawhub` 自动安装
3. 如未登录 ClawHub，先补齐登录态
4. 只有在自动准备失败时，才退回到纯文本草稿和待填项清单

不要在可以自动补环境时，直接把插件安装步骤推回给用户。

## 提示词原则

面向用户的提示词应该保持口语化、业务化、简洁。

通常只需要包含：

- 模板路径
- 甲方
- 乙方
- 合同标题
- 合作主题或合作方向
- 是否有特殊条款增删

像默认留空规则、输出目录规则、校验规则这类内部要求，应放在 skill 和 runner 中，而不是要求用户每次重复。

## Job Spec 结构

runner 接收一份 UTF-8 编码的 JSON 文件。典型结构如下：

```json
{
  "template_path": "./战略合作框架协议模板.docx",
  "party_a": "西藏高原数智产业研究院",
  "party_b": "成都景合开普勒科技有限公司",
  "party_a_profile": "甲方是一家围绕高原特色产业数字化、产业研究与项目协同开展工作的机构，具备区域资源整合、场景组织与项目推进能力。",
  "party_b_profile": "乙方是一家聚焦人工智能产品研发、行业解决方案交付和应用落地服务的科技公司，能够提供模型能力、平台产品与项目实施支持。",
  "party_b_credit_code": "91510100MADRXTX633",
  "party_a_identity_line": "地址：【待确认】    联系人：【待确认】",
  "party_a_aliases_to_replace": [
    "扎西院士"
  ],
  "global_replacements": [
    {
      "old": "纳金实验室",
      "new": "人工智能联合创新中心"
    }
  ],
  "cooperation_items": [
    {
      "heading": "共建高原特色产业数字化与人工智能联合创新中心",
      "body": "双方联合筹建相关平台并推进示范场景建设。"
    },
    {
      "heading": "推进面向政府和国企的AI数据治理与知识库建设",
      "body": "双方围绕政企客户开展数据治理、知识库建设和智能问答应用落地。"
    }
  ],
  "paragraph_overrides": [
    {
      "index": 46,
      "text": "甲方负责协调高原地区产业资源、政策对接和应用场景需求，为合作项目提供组织协调与本地资源支持。"
    },
    {
      "index": 57,
      "text": "合作双方共同设立联合工作组，围绕合作内容中的各项任务制定年度计划、推进项目实施并定期复盘执行进展。"
    }
  ],
  "leave_blank_fields": [
    "身份证号",
    "签署日期",
    "联系人"
  ],
  "unresolved_items": [
    "合作起止日期",
    "签署页签字人"
  ]
}
```

如确需覆盖模板标题，可额外显式传入：

```json
{
  "contract_title": "人工智能产业合作框架协议",
  "preserve_template_title": false
}
```

## 手动调试方式

在 skill 根目录下执行：

```powershell
pip install -r requirements.txt
python scripts\contract_runner.py --spec <path-to-job-spec.json>
```

正常学习后的工作流不应该再临时生成 `_draft_v1.py`、`_draft_v2.py` 这类一次性脚本。

推荐路径应始终是：

1. OpenClaw 写出一份结构化 JSON spec
2. OpenClaw 调用 `scripts\contract_runner.py`
3. OpenClaw 读取校验结果并向用户汇报

## 联动改写提醒

如果合作范围发生了实质变化，OpenClaw 不应只改合作内容区。

通常还需要一起检查或改写的段落包括：

- 鉴于 / 背景段落
- 权利与义务
- 合作机制
- 合作期限或承继逻辑
- 知识产权相关段落

如果新的合作主题、行业方向、地域背景或合作对象已经和模板原文明显不一致，应默认执行全文适配改写，而不是只做局部替换。

只有在确认模板原段落语义仍然兼容的情况下，才可以保留未改。

## 可迁移性

这份 skill 的设计目标，是让 OpenClaw 在另一台机器上也能直接学习并使用，尽量减少人工改路径步骤。

正常情况下，应由 OpenClaw 自动推导：

- 当前已安装的 skill 目录
- 目标 agent workspace
- 最终输出目录

手工改本地绝对路径只能作为兜底方案，不应成为标准使用方式。相对路径、自动推导路径和由配置读取的 workspace 路径应优先于写死的绝对路径。
