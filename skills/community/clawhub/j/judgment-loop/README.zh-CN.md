<p align="center">
  <img src="assets/judgment-loop-hero.png" alt="判断闭环——证据、反证、验证与行动" width="100%">
</p>

<p align="center">
  <strong>简体中文</strong> · <a href="README.md">English</a>
</p>

<h1 align="center">Judgment Loop · 判断闭环</h1>

<p align="center"><strong>补上从“想明白”到“现实行动”之间缺失的一步。</strong></p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT-0" src="https://img.shields.io/badge/license-MIT--0-F2C94C.svg"></a>
  <a href="https://skills.sh/sirsws/judgment-loop"><img alt="skills.sh installs" src="https://skills.sh/b/sirsws/judgment-loop"></a>
  <img alt="Version 1.1.2" src="https://img.shields.io/badge/version-1.1.2-2563EB.svg">
</p>

Judgment Loop 是一个面向重要选择、不确定结论、反复失败、深度学习和证据复盘的开放 Agent Skill。它把模糊的确信转成暂定判断、区分性验证，以及仍由用户承担的现实行动。

它不是让 AI 显得更深刻的提示词，而是防止 AI 把错误问题回答得无比漂亮。

## 30 秒看出区别

**向 Agent 提问**

> 一次志愿者工作坊获得了很高的满意度。现在应该推广到整个公司吗？

**流畅的回答可能只会优化代理指标**

> 试点很受欢迎，开始准备全公司推广。

这把参与者满意度直接当成了工作坊改善目标结果的证据。

**Judgment Loop 会改变任务本身**

- **暂定判断：**暂不全面推广，先在一个有代表性的团队做后续试点。
- **真实目标：**改善跨团队交接，而不是提高出席率或满意度。
- **已验证事实：**志愿参加者对第一次工作坊评价很高。
- **待验证假设：**普通团队参加后会改变实际行为。
- **最强失败理由：**自愿参加者可能不能代表推广人群。
- **最低成本验证：**为第二个团队预先规定一个交接结果和停止条件。
- **停止或扩大：**只有目标结果改善且代价可接受时才扩大。

安装后可以直接测试同一个问题：

```text
$judgment-loop 一次志愿者工作坊获得了很高的满意度。现在应该推广到整个公司吗？
```
## 为什么需要它

AI 往往能在人尚未辨认真实目标时，就给出完整、流畅、自洽的答案。这会产生四种常见失败：

- 代理指标增长了，现实目标没有改善；
- 人迷恋一个方案，并把它与自我认同绑定；
- 漂亮解释跑在证据前面；
- AI 完成了全部认知工作，用户没有留下自己的判断和行动。

判断闭环会在必要时打断这个过程，同时避免把每件小事都变成一套沉重仪式。

## 五种模式

| 模式 | 适用场景 | 核心动作 |
|---|---|---|
| **快速** | 问题模糊或已经迷恋某个方案 | 真实目标 → 最强失败理由 → 最便宜动作 |
| **决策** | 有代价或难撤回的选择 | 下行、可逆性、关键假设、护栏 |
| **研究** | 论文、报告、数据和因果结论 | 主张、证据、边界、最强替代解释 |
| **学习** | 希望真正理解并迁移 | 重建、边界、迁移、回忆 |
| **复盘** | 行动已经产生现实结果 | 原目标、实际结果、预期差异、更新 |

## 安装

### skills.sh / 通用 Skills CLI

```bash
npx skills add sirsws/judgment-loop
```

只为 Codex 全局安装：

```bash
npx skills add sirsws/judgment-loop --skill judgment-loop -g -a codex -y
```

### ClawHub / OpenClaw

```bash
clawhub install judgment-loop
```

### 手动安装

把仓库目录复制到 Agent 的 Skill 目录。Codex 的全局目录是 `~/.codex/skills/judgment-loop/`。

## 使用

显式调用：

```text
$judgment-loop 我应该现在发布，还是继续完善？
```

当“后果明显＋结论不确定”同时出现时，Skill 也允许自动调用。简单事实、明确执行、低风险可逆小事、自由创作和单纯情绪陪伴不会触发完整闭环。

## 一次好的闭环会产生什么

```text
暂定判断
    ↓
真实目标与主权
    ↓
承重假设
    ↓
最强失败理由
    ↓
最低成本区分性验证
    ↓
用户承担的行动与复审触发条件
```

只使用会改变判断的动作。闭环保持开放：行动可以闭合，认知必须允许更新。

## 示例与评测

[使用案例](examples/README.md)展示行为差异，并与单一来源的[跨领域评测清单](evals/cases.json)明确分离。

[人工复核评测协议](evals/trigger-cases.md)分别统计触发深度、模式选择、证据更新、缺失案例和错误严重度。当前版本在完成保留原始输出且经独立复核的运行前，不宣称已有行为基线。

## 设计原则

1. **用户主权**：模型不替用户作价值选择。
2. **证据先于漂亮表达**：明确区分事实、推断和假设。
3. **先找最强失败理由**：寻找承重弱点，而不是制造形式平衡。
4. **最低成本证伪**：增加流程前，先区分竞争解释。
5. **行动闭合，认知开放**：必要时作出选择，同时保留更新能力。
6. **轻重相称**：低风险可逆小事就应该保持简单。

## 语言版本

公开运行版使用英文，以兼容更多 Agent，并要求 Agent 使用用户的语言回答。完整中文参考译本位于 [`translations/zh-CN`](translations/zh-CN/)。

## 许可证

[MIT-0](LICENSE)：允许使用、修改、再分发和商业使用，无署名要求。
