## Description: <br>
Pelatih OSNK - Bank soal OSK/OSNK/SNK/Bebras (2006-2025) dengan latihan cerdas, speed run, performance tracking, dan mentoring lengkap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrrqd](https://clawhub.ai/user/jrrqd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and coaches use this skill to practice Indonesian informatics olympiad questions, run timed drills, review topic explanations, and track local performance over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Bash helper may contact GitHub for missing question text when bundled or local question files are unavailable. <br>
Mitigation: Keep the bundled question bank available for offline use, or block outbound network access in stricter environments. <br>
Risk: The artifact warns that answer keys may not be fully accurate. <br>
Mitigation: Verify important answers against official TLX TOKI keys, forum explanations, or other trusted references before relying on them. <br>
Risk: Practice progress and statistics are written to local workspace JSON files. <br>
Mitigation: Review workspace data retention expectations and clear the local memory files when shared environments require it. <br>


## Reference(s): <br>
- [OSNK Trainer skill page](https://clawhub.ai/jrrqd/osnk-trainer) <br>
- [Security documentation](artifact/SECURITY.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain text responses with question excerpts, answer prompts, stats, and topic explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local JSON progress and stats; may use an optional GitHub fallback for missing question text.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
