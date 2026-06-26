## Description: <br>
Repairs malformed JSON by handling common issues such as trailing commas, unquoted keys, comments, and single-quoted strings, with support for direct text repair and user-selected file repair. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to recover usable JSON from malformed strings, LLM responses, and local JSON files. It is suited for repair workflows where the corrected output is reviewed before replacing important configuration or project data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File repair mode can overwrite user-selected files without a backup by default. <br>
Mitigation: Use the skill on copies when possible, pass the backup option for file repairs, and review repaired output before replacing important files. <br>
Risk: Broad trigger wording may cause the skill to run in contexts where JSON repair is not the intended action. <br>
Mitigation: Invoke it only for clear malformed JSON inputs or JSON parsing failures, and confirm the repaired structure matches the intended data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muguozi1/muguozi1-openclaw-json-repair) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/muguozi1) <br>
- [EvoMap asset](https://evomap.ai/a2a/assets/sha256:acce5be22676155e3ca07ff2c5060acdd1de5529aded8ed5edcc946b03f20eae) <br>
- [npm json-repair package](https://www.npmjs.com/package/json-repair) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON objects, formatted JSON files, and Markdown guidance with inline code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [File repair can rewrite user-selected files; use backups and review repaired output before replacement.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
