## Description: <br>
Plutus Lite is a free expense tracker that categorises up to 15 transactions and shows a basic spend breakdown as a preview of Plutus Pro. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to paste a small set of expenses and receive a quick category and spend summary. It is intended for lightweight personal expense review rather than full budget, tax, trend, or export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense details are supplied through an environment variable. <br>
Mitigation: Use only expense details you are comfortable pasting into EXPENSES_TEXT, and avoid including unnecessary sensitive account or merchant data. <br>
Risk: The install command uses --break-system-packages and can modify the Python environment. <br>
Mitigation: Prefer installing and running the dependency in a virtual environment. <br>
Risk: The Lite skill displays upgrade links for a paid Pro version. <br>
Mitigation: Review paid upgrade links and purchasing terms separately before following them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/plutus-lite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks, plus terminal-formatted expense tables when run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts optional EXPENSES_TEXT and CURRENCY environment variables; limits summaries to 15 transactions.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
