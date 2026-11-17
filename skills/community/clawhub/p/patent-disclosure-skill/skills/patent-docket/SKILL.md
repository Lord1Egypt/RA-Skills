---
name: patent-docket
description: "按发明人/工程师给的材料一趟写出交底书和申请文件；申请问题清单上的缺口最多改三轮。缺技术事实就问人，不编。触发：交底申请一起做、从零出交底和申请、一条龙、帮写交底再出申请、按清单改、会稿、案卷、/patent-docket。"
user-invocable: false
---

# 案卷会稿

单 agent 协调者。**先 `Read` `prompts/guardrails.md`，再 `Read` `prompts/intake.md`。** 禁止跳过 intake 直接派工。

本包只调度与记案卷，不写交底正文、不出四件套。派工时 **`Read`** 对方 `SKILL.md` 并按该包执行；**禁止**调用其他子技能的 `tools/`。

## 加载顺序（每次进入都走）

1. `prompts/guardrails.md`
2. `prompts/intake.md`（判定 `from_zero` / `from_disclosure` / `from_application` / `resume`）
3. 按 intake 结果只加载下列之一，不要一次读完所有 prompt：
   - 新开或从零 → `prompts/bootstrap.md`
   - 已有 `docket.yaml` → `prompts/resume.md`
4. 之后按 `docket.yaml` 的 `phase` **只读**对应文件（见下表）。阶段表在 `references/phases.yaml`。

| `phase` | 再读 |
|---------|------|
| `bootstrap_disclosure` / `wait_disclosure` / `dispatch_disclosure` | `prompts/dispatch_disclosure.md` |
| `bootstrap_application` / `wait_application` / `dispatch_application` | `prompts/dispatch_application.md` |
| `triage` | `prompts/triage.md` → `references/issue_taxonomy.md` |
| `ask_human` | `prompts/ask_human.md` |
| `round_close` | `prompts/round_close.md` |
| `terminal_*` | `prompts/round_close.md`（只做收口陈述，不再派工） |

阶段合法跳转：`references/phases.yaml`。机器校验：`tools/validate_docket.py`。tracker 落盘：`tools/emit_tracker.py`。交接只传路径：`references/handoff_contract.md`。

## 轮次

- 上限 **`config.yaml` 的 `max_rounds`（默认 3）**，细则 `references/max_rounds.md`。
- 从零：首套交底 + 首套申请记为第 1 轮。
- 之后每「分诊 → 派工 → 再出申请并核清单」加 1 轮。
- 第 3 轮结束后必须停。

## 命令

```bash
python skills/patent-docket/tools/init_docket.py --case-id 案件slug --mode from_zero
python skills/patent-docket/tools/validate_docket.py --yaml outputs/docket/案件slug/docket.yaml
python skills/patent-docket/tools/emit_tracker.py --yaml outputs/docket/案件slug/docket.yaml
```

案卷目录默认 **`outputs/docket/{case_id}/`**（gitignore 的 `outputs/`）。机读前缀：`DOCKET_DIR:` / `DOCKET_YAML:` / `DOCKET_OK:` / `DOCKET_ERROR:`。

**不做**：审查答复、政策简报、著录检索当会稿引擎、多 agent 分发、把聊天摘要当成技术事实。
