## Description: <br>
Wraps HLE benchmark questions in a structured Chain-of-Thought (CoT) reasoning process. Use when answering HLE questions to ensure strict step-by-step logic and format compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and benchmark evaluators use this skill to format HLE questions with required reasoning and final-answer sections, then check whether model responses follow that structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cached answers can be written to a local cache.json file in the skill directory. <br>
Mitigation: Avoid caching private benchmark content or sensitive answers unless local persistence is acceptable, and delete the cache file when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanng-ide/hle-reasoning-wrapper) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Structured prompt text and boolean validation result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional local cache storage for answers] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
