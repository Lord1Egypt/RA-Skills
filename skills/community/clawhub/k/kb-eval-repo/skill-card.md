## Description: <br>
Evaluate whether a GitHub/open-source repository is useful for the user's selected Research KB context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research knowledge-base users use this skill to assess whether a named GitHub or open-source repository is worth studying, reproducing, or adapting for the selected knowledge-base context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Gitea admin token for knowledge-base access. <br>
Mitigation: Install only where that access level is acceptable, and prefer a narrowly scoped bot token when possible. <br>
Risk: The skill can create or update review pages in selected knowledge-base repositories by default. <br>
Mitigation: Set writeReview to false unless persistence is intended, and review generated pages before relying on them. <br>
Risk: Repository reproducibility findings are based on fetched repository materials rather than actual installation or execution. <br>
Mitigation: Treat the result as an initial assessment and perform a minimal reproduction before making engineering decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/skills/kb-eval-repo) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Sample task input](artifact/tests/sample_eval_repo_task.json) <br>


## Skill Output: <br>
**Output Type(s):** [json, markdown, guidance] <br>
**Output Format:** [JSON result object with citations and an optional Markdown review page] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a single query-compatible result for the provided research_kb_agent_task JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
