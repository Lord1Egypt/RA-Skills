## Description: <br>
Blind multi-model comparison with architecturally guaranteed de-anonymization. Trigger with "mdls" or "modelshow" for double-blind evaluation of AI model responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[schbz](https://clawhub.ai/user/schbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI users use ModelShow to send one prompt to multiple configured models, compare their responses with blind judging, and review a scored ranking with judge commentary. It supports fact checking, creative tasks, technical decisions, code review, and brainstorming where comparing model behavior is useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced context are sent to all configured models and to a judge model. <br>
Mitigation: Review config.json before use and include only models approved for the data being evaluated. <br>
Risk: Full prompts, model responses, rankings, and judge analysis are saved locally after each run. <br>
Mitigation: Do not use the skill with secrets, regulated data, private code, or confidential documents unless local full-result storage is acceptable; keep the output directory private. <br>
Risk: The optional web indexer can copy saved result files into a public-facing location. <br>
Mitigation: Use update_modelshow_index.py only when publication is intentional and the saved outputs have been reviewed. <br>
Risk: Blind judging reduces label bias but should not be treated as a privacy control. <br>
Mitigation: Treat anonymization as an evaluation aid and review final rankings before using them for consequential decisions. <br>


## Reference(s): <br>
- [ModelShow repository](https://github.com/schbz/modelshow) <br>
- [ModelShow ClawHub listing](https://clawhub.ai/schbz/modelshow) <br>
- [schbz ClawHub publisher profile](https://clawhub.ai/user/schbz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown comparison output with saved JSON and Markdown result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs configured models in parallel, judges anonymized responses, returns ranked results with scores and commentary, and saves full outputs to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
