## Description: <br>
Nutrition Claw is a local-first CLI skill for tracking meals, foods, nutrition goals, history, and semantic searches with YAML output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pita](https://clawhub.ai/user/Pita) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and end users use this skill to configure nutrition goals, manage a local food library, log meals and ingredients, review daily or multi-day nutrition totals, and search nutrition history without cloud services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Malformed date inputs may cause the CLI to read or write log files outside its intended nutrition folder. <br>
Mitigation: Use normal YYYY-MM-DD dates only and review date-handling behavior before deploying the skill in shared or automated environments. <br>
Risk: Nutrition history is stored locally in plaintext under ~/.nutrition-claw/. <br>
Mitigation: Avoid running the skill with elevated privileges and protect or delete the local data directory according to the user's privacy requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Pita/nutrition-claw) <br>
- [GitHub Packages listing](https://github.com/Pita/nutrition-claw/pkgs/npm/nutrition-claw) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Bun](https://bun.sh) <br>


## Skill Output: <br>
**Output Type(s):** [YAML, Shell commands, Guidance] <br>
**Output Format:** [YAML CLI responses with stderr errors and human-facing nutrition guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores goals, foods, meal logs, vectors, and education history locally under ~/.nutrition-claw/.] <br>

## Skill Version(s): <br>
1.0.9 (source: evidence.release.version, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
