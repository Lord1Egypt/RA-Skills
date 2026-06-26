# Defense Report Contract

The main defense report is `generated/defense/<paper-slug>/defense_qa_bank_cn.md`.

It must be a derivative artifact grounded in the authoritative deep-read report, paper, code, logs, and review materials. It must not silently invent evidence.

## Mandatory sections

```markdown
# <Paper Title>：答辩问答与代码/训练审计包

## 1. 答辩范围与证据状态
## 2. 论文一句话主张与最安全表述
## 3. 核心贡献的可防守版本
## 4. 高风险问题总览
## 5. 论文层面问题与回答
## 6. 方法 / 公式 / 理论问题与回答
## 7. 实验 / 消融 / 基线问题与回答
## 8. 代码与训练过程问题与回答
## 9. 可复现性与工程实现问题与回答
## 10. 局限性 / 失败模式 / 伦理风险问题与回答
## 11. 未来工作与研究边界问题与回答
## 12. 最不该说的话
## 13. 备份页与证据材料清单
## 14. 模拟答辩脚本
## 15. 最后 10 分钟速记卡
## 16. 图文答辩卡片与生图提示词
```

## Evidence labels

Every answer must include one or more labels:

- `paper_grounded`
- `code_grounded`
- `experiment_log_grounded`
- `review_grounded`
- `inferred`
- `missing_evidence`
- `external_context`

## Required Q&A item format

```markdown
### Qxx. <question>

- **对象**：advisor / reviewer / peer / beginner / practitioner
- **攻击轴**：novelty / method / experiment / code / training / reproducibility / limitation
- **优先级**：P0 / P1 / P2 / P3 / P4
- **为什么会问**：...
- **短回答**：...
- **长回答**：...
- **证据**：paper section / table / figure / code path / log path / review note
- **证据标签**：...
- **不能过度声称**：...
- **追问后的回应**：...
- **备份页 / 材料**：...
```

## P0/P1 requirement

Every P0/P1 item must have:

- a short answer;
- a long answer;
- evidence references or explicit missing-evidence warning;
- what not to overclaim;
- backup slide or artifact;
- follow-up experiment / code check.

## Visual Q&A addendum

When visual mode is enabled, the main report section `## 16. 图文答辩卡片与生图提示词` must summarize:

- which P0/P1 or hard-to-explain questions were converted to visual cards;
- the card sequence and audience purpose;
- whether each card is `text_ready`, `image_pending`, or `image_generated`;
- the reminder that text answers and image generation are separate steps;
- the exact follow-up request the user can send to generate the series with the Codex `imagegen` skill, ChatGPT Create image mode, or an approved API.

Each visual card must link back to one or more Q_IDs from `defense_qa_bank_cn.json`.
