## Description: <br>
Humanizer-DE analyzes German text for AI-like writing patterns, scores the likelihood of AI-generated prose, and provides concrete rewriting suggestions or humanized revisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tikitackr](https://clawhub.ai/user/tikitackr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and German-speaking teams use this skill to review German drafts for AI-sounding wording, repetitive structure, and statistical signals, then improve the text with targeted suggestions or rewrites. It also includes an optional local CLI for quick file-based scoring, suggestions, and auto-fix output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may activate the skill when the user only intended to discuss similar wording. <br>
Mitigation: Invoke it with explicit German text-review or humanizing requests and confirm the desired mode before relying on the result. <br>
Risk: Rewrites or auto-fix output can change meaning or add personal-sounding claims that were not in the source text. <br>
Mitigation: Review rewritten text and any CLI-generated fixed output before publishing, committing, or sharing it. <br>
Risk: The optional CLI can modify intended file outputs during auto-fix workflows. <br>
Mitigation: Run the CLI only on intended files and inspect the generated output before replacing the original text. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tikitackr/humanizer-de) <br>
- [README](artifact/README.md) <br>
- [KI-Schreibmuster](artifact/references/ki-muster.md) <br>
- [Deutsche KI-Vokabel-Datenbank](artifact/references/vokabeln.md) <br>
- [Statistische Signale](artifact/references/statistische-signale.md) <br>
- [Personality Injection](artifact/references/personality-injection.md) <br>
- [Humanisierungs-Beispiele](artifact/references/examples.md) <br>
- [Stil-Layer: Basis](artifact/references/stil-layer/basis.md) <br>
- [Stil-Layer: Lesch](artifact/references/stil-layer/lesch.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis reports, rewritten German text, replacement suggestions, and optional CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores German text from 0 to 100 and may produce file-based CLI outputs that users should review before use.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
