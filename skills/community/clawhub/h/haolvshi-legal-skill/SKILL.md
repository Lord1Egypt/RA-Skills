---
name: haolvshi-legal-skill
display_name: 好律狮法律技能包
display_name_en: HaoLvShi Legal Skill
description: "好律狮法律技能包。只要用户提出具体法律问题，或要求计算赔偿、费用、社会保险待遇或养老保险待遇（包括企业职工养老保险、基础养老金、个人账户养老金、过渡性养老金和退休待遇），审核合同、生成起诉状或生成答辩状，就应使用本技能调用好律狮专业法律服务接口完成流程；典型表达包括“离婚财产如何分割”“帮我算养老保险”“退休后每月能领多少养老金”“帮我审核这份合同”“生成离婚起诉状”。支持多轮问答、结构化表单、附件上传、多个当事人、在线报告查看和法律文书直接下载。"
version: "1.17"
description_zh: "基于好律狮法律服务接口的专业法律技能，支持法律咨询报告、赔偿与费用计算、社会保险和养老保险待遇测算、智能合同审核、起诉状生成与答辩状生成。一句话提出问题，技能会引导补充关键事实，并交付在线报告或 Word 文书。"
description_en: "Professional legal workflows via HaoLvShi APIs for consultation reports, compensation calculators, contract review, complaints and answers. One sentence starts a guided flow that delivers an online report or a Word document."
compatibility: "需要网络访问、临时文件读写和 shell 或 PowerShell 执行能力；技能会自动检查并准备 Node.js 运行环境。"
license: MIT-0
metadata:
  version: "1.17"
  homepage: https://skills.ai.lvpin100.com
  display_name: 好律狮法律技能包
  description_zh: "基于好律狮法律服务接口的专业法律技能，支持法律咨询报告、赔偿与费用计算、社会保险和养老保险待遇测算、智能合同审核、起诉状生成与答辩状生成。一句话提出问题，技能会引导补充关键事实，并交付在线报告或 Word 文书。"
---

# 好律狮法律技能包

## 默认快速路径

按顺序直接执行，不要先规划整套流程、复述规则或推演后端节点；脚本会保存状态并返回下一步。

1. 每次进入本技能先清空上一次的技能记忆：丢弃此前的 `sessionId`、项目选择、题目答案、接口用法和报告链接，一切从当前对话重新开始。历史会话里的接口方法、参数和结论一律不得沿用。
2. 运行环境准备只需首次执行，它会补齐脚本执行位并建好状态目录；之后只用 `run.sh` 或 `run.ps1` 调用命令。
3. 每次只运行一项能力；目的不明时只问要哪一种。需多个独立产物时按 `references/multi-capability.md` 串行；每项交付后须询问是否继续下一项，明确同意前不得启动。
4. 只使用当前任务/线程的信息、当前上传材料、同一 `sessionId` 的保存答案和较新的明确更正。不得读取或使用全局记忆、其他任务、旧案例或猜测；缺少事实就提问。
5. 每次只处理脚本返回的 `stage`、`prompt` 和当前 `interaction`；命令默认只返回下一步所需的精简载荷。保存 `sessionId`，“继续”只能恢复用户明确对应的同一任务。
6. 先用语义判断当前题能否由案情直接得出：把选项与案情逐一比对，**含义一致即可，不要求字面相同**（"老板"对应"用人单位"，"拖欠5年"对应"超过三年"）。置信度不低于 `0.85` 且明显优于其他选项时直接作答，多选题提交全部成立的选项；没有依据或多项都可能成立才呈现 `interaction.native.batches[0]`，不猜测，不默认选"其他""不清楚"。契约见 `interaction.answerPolicy`。
7. 脚本处理建议选项、追加题、多填题、非必填敏感字段和明确排除的条件字段，并按契约转换日期、地区；不适用字段保留空值，不能填零或默认数量，单纯未提到仍需询问。地区题问到 `areaLevel`；每轮只处理当前字段，地区与重复记录姓名仍需确认。
8. 最终摘要只能依据本次生成的报告或文书，不再搜索或补充外部法律信息。同一轮回复必须原样输出 `data.delivery.markdown`；`autoOpen=true` 时立即用宿主内置浏览器打开 `data.delivery.url`，不得调起外部浏览器。禁止自行生成 HTML、Markdown、PDF 等任何报告或文书文件。

默认不读取参考文档，只有命中下表情形时才按需读取，避免每轮重复加载长规则。

| 情形 | 读取 |
| --- | --- |
| 上传或无法读取材料 | `references/case-materials.md` |
| 同一请求涉及多个独立产物或能力 | `references/multi-capability.md` |
| 原生控件不可用、选项过多、追加题或多当事人 | `references/interaction.md`；需要兼容载荷时在原命令输入中加 `"verbose": true` |
| 材料、控件之外的能力异常 | 对应能力参考或 `references/errors.md` |

## 运行环境准备

macOS 或 Linux 首次使用时执行：

```bash
sh scripts/bootstrap.sh --ensure
```

Windows 首次使用时执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1 -Ensure
```

脚本优先复用系统中的 Node.js；缺少或低于 20 时自动下载并校验技能专用的 Node.js 22，无需管理员权限。之后统一用 `run.sh` 或 `run.ps1` 调用。

## 运行脚本

在本技能目录中执行。macOS 或 Linux：

```bash
sh scripts/run.sh <命令>
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run.ps1 <命令>
```

用标准输入传 JSON，避免把案情和身份信息写进命令行参数：

```bash
printf '%s' '{"capability":"calculator","query":"交通事故赔偿"}' \
  | sh scripts/run.sh catalog
```

脚本始终返回 JSON：`ok=true` 表示成功，`stage` 是当前阶段；`ok=false` 时按 `error.retryable` 和 `references/errors.md` 处理。

## 能力路由

### 项目语义选择

咨询和计算器的 `catalog` 返回完整目录，由大模型结合用户原话和候选的父级领域、具体项目名称打分，不得按分词、关键词命中数或目录顺序选择。第一名置信度不低于 `0.85` 且领先第二名 `0.15` 时，用该候选的 `id` 作为 `projectId`；否则请用户在 2 至 4 个真实候选中确认，或只问一个能区分它们的问题，不得默认“不清楚”“其他”。

### 法律咨询报告

调用 `catalog`（`capability: consultation`）并按上节选定 `projectId` 后调用 `question-start`；`stage=ready_for_report` 时调用 `question-report`。目录和问答异常才读 `references/consultation.md`。

### 法律计算器

用于赔偿、费用及社会保险待遇测算（含企业职工养老保险、基础养老金、个人账户养老金、过渡性养老金和退休待遇）。调用 `catalog`（`capability: calculator`）并按上节选定 `projectId` 后调用 `question-start`；`stage=ready_for_report` 时调用 `question-report`。目录和问答异常才读 `references/calculator.md`。

### 智能合同审核

先确认用户代表甲方或乙方，未知时直接呈现脚本返回的原生单选。确认立场和合同文件后调用 `contract-review`。仅在连接中断且脚本给出本任务 `sessionId` 时调用一次 `resume`，不轮询。异常才读 `references/contract-review.md`。

### 起诉状、答辩状

调用 `catalog`（起诉状 `complaint`，答辩状 `defense`），选模板后调用 `pleading-start`，再把当前任务案情和材料传给 `pleading-extract`。按当前字段页或当事人卡片调用 `pleading-update`，只问没有唯一依据的字段。确认摘要后以 `confirmed: true` 调用 `pleading-generate`。异常才读 `references/pleading.md`。

## 会话恢复和清理

- 用户要求继续当前任务时，只使用与当前任务明确对应的原 `sessionId`；不得从全局记忆或其他任务猜测、搜索或加载任务编号。
- `resume` 不会重复提交答案、审核或文书生成。
- 完成后可以调用 `cleanup` 删除任务材料；技能也会自动清理超过二十四小时的临时任务。

## 输出要求

- 咨询报告：核心结论、法律分析、行动建议和 `[法律咨询报告](链接地址)`。
- 计算结果：总金额、分项金额、计算依据、关键输入和 `[法律计算报告](链接地址)`。
- 合同审核：风险数量、风险等级、重点条款、修改建议和 `[合同审核报告](链接地址)`。
- 起诉状和答辩状：当事人、请求或答辩意见、事实理由摘要和 `[起诉状（Word）](链接地址)` 或 `[答辩状（Word）](链接地址)`。
- 上述摘要、结论、金额、风险、建议和法律依据只能取自脚本返回的报告或文书正文及其内嵌法规、案例；生成后不再搜索、查询或添加外部内容，报告未写明的不作补充。
- 最终链接统一使用 `data.delivery.markdown`，必须在生成当轮的用户可见回复中原样出现，不得等用户再次索取。`autoOpen=true`（在线报告）时立即用宿主的浏览器或导航能力打开 `data.delivery.url`；宿主没有该能力时仍要发链接。文书下载链接不自动打开，也不用本地文件路径替代用户入口。

## 隐私与安全

- 只把完成当前流程所需的信息发送到好律狮服务接口。
- 不在回复和日志中输出身份证号、合同全文、服务端配置或密钥。
- 用户要求删除本地任务材料时立即调用 `cleanup`。
- 接口返回登录、验证码、付费或配置错误时，直接说明实际限制，不绕过服务端校验。
