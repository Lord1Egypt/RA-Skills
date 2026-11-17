## Description:

Jobs-System is a community demonstration skill that guides product, strategy, opportunity, and positioning decisions through a three-layer decision-analysis workflow with evidence requirements, certainty labels, domain routing, and Jobs-inspired voice constraints.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[sabre232](https://clawhub.ai/user/sabre232)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and product or strategy practitioners use this skill to draft structured decision memos for startup opportunities, product definition, strategic tradeoffs, competitive positioning, market research, feature reduction, and technology timing. Outputs are drafts that require human validation, especially for sensitive business decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill strongly shapes response style and transparency, which can make normal assistant behavior less neutral.

Mitigation: Install and enable it only for the intended Chinese Jobs-style decision workflow; keep unrelated chat, search, and coding tasks outside its trigger scope.

Risk: The artifact can save local plaintext decision, actor, and reasoning records.

Mitigation: Avoid entering sensitive personal or business strategy data unless the workspace and generated memory files are managed, reviewed, and deleted as needed.

Risk: Strategic recommendations may be incorrect or misleading if treated as final decisions.

Mitigation: Treat outputs as drafts, verify cited evidence independently, and require human review before acting on high-stakes product or business advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sabre232/skills/jobs-system-community)
- [README.md](artifact/README.md)
- [Jobs voice layer](artifact/jobs-voice.md)
- [Installation instructions](artifact/安装说明.md)
- [Product shell and structure checks](artifact/references/product_shell.py)
- [Self-test decision record](artifact/references/_selftest_record.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown decision memos with evidence markers, certainty labels, domain-routing notes, and optional Python CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled product shell may write local JSON and JSONL decision, actor, and reasoning records when its render CLI is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
