## Description: <br>
Design, log, compare, and score prompt experiments so users can systematically improve outputs instead of guessing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and other agent users use this skill to plan prompt A/B experiments, compare outputs against explicit criteria, log scores, and decide the next prompt iteration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled helper script writes a CSV file to the selected output path and could overwrite an existing file. <br>
Mitigation: Choose an explicit, safe output path before running the script and avoid paths containing important existing files. <br>
Risk: Prompt experiment scores can be misleading if criteria, weights, or test cases are incomplete. <br>
Mitigation: Define success criteria, weights, and test cases before comparing prompts, and keep assumptions explicit in the result. <br>
Risk: User-provided local files may contain data outside the intended experiment scope. <br>
Mitigation: Provide only JSON files intended for the experiment and confirm the input scope before generating logs or summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/prompt-ab-lab) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Prompt Evaluation Rubric](artifact/resources/eval_rubric.md) <br>
- [Example prompt](artifact/examples/example-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional local CSV output from the bundled Python helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce an experiment plan, scored comparison table, rubric, next-iteration suggestions, and a CSV logging template.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
