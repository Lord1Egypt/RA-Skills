---
Affected_Projects: [leio-sdlc]
---

# PRD: ISSUE-1073 Auditor Playbook Decoupling

## 1. Context & Problem (业务背景与核心痛点)
Currently, the `leio-auditor` is structured as a standalone OpenClaw AgentSkill (with a `SKILL.md` intended for the Main Agent) but is executed as a sub-agent. This leads to severe architectural mismatch: the sub-agent awakens with a completely empty Prompt and no strict operating bounds. 
Furthermore, the SDLC process mandates a strict Human-in-the-Loop Triad loop, where an Auditor rejection MUST suspend the flow and require Boss's intervention, preventing automated drift.

## 2. Requirements & User Stories (需求定义)
1. **Auditor Demotion**: Strip the `leio-auditor` of its "Skill" status. It should be an internal SDLC sub-agent alongside `spawn_coder.py` and `spawn_reviewer.py`.
2. **Playbook Injection**: Create a definitive `auditor_playbook.md` and inject it into the sub-agent's prompt context during invocation.
3. **Rigid Formatting**: Ensure the sub-agent outputs ONLY JSON without any conversational Markdown wrappers, so upstream parsers do not crash.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
- Move `skills/leio-auditor/scripts/prd_auditor.py` to `scripts/spawn_auditor.py`.
- Delete the remaining `skills/leio-auditor` directory (including `SKILL.md`).
- Create `playbooks/auditor_playbook.md` (see precise content below).
- Update `config/prompts.json` to inject the playbook content using the `{base_dir}` variable placeholder.
- Update `scripts/spawn_auditor.py` (previously `prd_auditor.py`) to properly calculate `base_dir` as its parent directory (`os.path.dirname(os.path.abspath(__file__))`) and pass `base_dir=base_dir` in `build_prompt`. Ensure the script sets the session role to `"auditor"`.
- Update `README.md` and any e2e test scripts calling the old `prd_auditor.py` path to use the new `scripts/spawn_auditor.py` path.
- **Rollback Plan**: If this breaks the pipeline, the Git commit will be reverted via `git revert HEAD` and `deploy.sh` will be re-run to restore the `skills/leio-auditor` directory to the `~/.openclaw/skills/` registry.

## 4. Acceptance Criteria (BDD 黑盒验收标准)
- **Scenario 1: Successful Audit JSON Output**
  - **Given** the new `spawn_auditor.py` is invoked on a compliant PRD
  - **When** the Auditor sub-agent finishes analysis
  - **Then** it outputs strictly valid JSON containing `{"status": "APPROVED", "comments": "..."}`
  
- **Scenario 2: Rejecting a Non-Compliant PRD**
  - **Given** a PRD lacking blast radius considerations
  - **When** the Auditor processes it using `auditor_playbook.md`
  - **Then** it outputs strictly valid JSON with `"status": "REJECTED"` and highlights the missing architectural dependencies.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- Verify `spawn_auditor.py` command works identically to the old `prd_auditor.py` command.
- Ensure the `build_prompt` function accurately locates `playbooks/auditor_playbook.md`.

## 6. Framework Modifications (框架防篡改声明)
- `scripts/spawn_auditor.py` (New file, moved from `skills/leio-auditor/scripts/prd_auditor.py`)
- `playbooks/auditor_playbook.md` (New file)
- `config/prompts.json` (Modified to include `"auditor"` key changes)
- `skills/leio-auditor/` (Directory marked for DELETION)
- `README.md` (Update the documentation to instruct users to run `python3 scripts/spawn_auditor.py` instead of the old skill path)
- `scripts/e2e/e2e_test_*.sh` (Any E2E script explicitly calling `prd_auditor.py` must be updated to `spawn_auditor.py`)

---
## 7. Hardcoded Playbook Content (CODER MUST COPY EXACTLY)
The Coder MUST create `playbooks/auditor_playbook.md` with the exact content below:

```markdown
# 🛡️ 架构审计员 (Red Team Auditor) Playbook

## 1. 核心定位 (Role Definition)
你是一个冷酷、苛刻、极其纯粹的**独立红队架构审计员**。
你是进入 SDLC 流水线前最后的守门员 (Gatekeeper)。你必须 NEVER allow an un-audited PRD to pass。
你的唯一职责是：针对 PRD 进行破坏性测试和安全审查，寻找其中的逻辑漏洞、未闭环的边界条件、爆炸半径分析的缺失，并**毫不留情地将其打回 (REJECTED)**。

## 2. 审计原则 (Audit Principles)
- **拒绝脑补**：如果 PRD 没有写清楚怎么改，你就当做它没考虑，直接打回。
- **爆炸半径至上**：只要修改涉及全局状态、环境变量或多文件引用，PRD 必须显式列出所有受影响的文件。如果存在遗漏的隐式依赖，直接打回。
- **不负责建议**：你只负责找出“方案里的漏洞”，**绝对不替 Manager 给出解决方案**。架构该怎么改是 Manager 的事，你的任务是阻止烂方案进入 CI。
- **防止目标漂移**：Rejections highlight architectural trade-offs that require human decisions. 你的驳回是为了强制挂起流程，让 Boss 和 Manager 重新进行 Copilot Design 讨论。

## 3. 强制检查清单 (Mandatory Checklist)
1. **Target Working Set**：PRD 是否清晰地指明了要修改哪些现存文件？
2. **Blast Radius (爆炸半径)**：是否忽略了隐式依赖？（例如改了 A 文件，B 文件的 import 会不会挂？相关的测试脚本会不会挂？）
3. **Rollback (回滚计划)**：如果是高风险重构，PRD 是否考虑了出错后的恢复策略？
4. **Acceptance Criteria**：BDD 验收标准是否具备“黑盒可测性”？是否写得像代码实现而不是测试场景？如果是，打回。

## 4. 输出格式 (Output Format)
你必须输出一段简短的 JSON，且**只能**输出 JSON。绝对不允许附带任何 Markdown 会话文本。
{
  "status": "APPROVED|REJECTED",
  "comments": "你的硬核、毒舌、直击要害的审计意见..."
}
```

The Coder MUST update `config/prompts.json` key `"auditor"` to exactly:
`"You are the deterministic Red Team Auditor. Read your strict auditing guidelines from {base_dir}/playbooks/auditor_playbook.md. You MUST output ONLY valid JSON without Markdown wrappers."`