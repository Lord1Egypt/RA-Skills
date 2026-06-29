## Description: <br>
Make Html directs agents to create self-contained, validated HTML artifacts for substantial human-facing deliverables, with optional hosted sharing when explicitly requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuller-stack-dev](https://clawhub.ai/user/fuller-stack-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, reviewers, and other ClawHub users use this skill to turn substantial reports, plans, reviews, dashboards, diagrams, decks, prototypes, and editors into self-contained HTML deliverables that are easier to inspect, present, and share. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive content could be exposed if a generated HTML artifact is shared through the hosted preview path. <br>
Mitigation: Use hosted sharing only after explicit user request or confirmation, and do not upload credentials, secrets, personal data, private customer data, or internal-only material. <br>
Risk: Password-protected hosted links may still be inappropriate for sensitive material. <br>
Mitigation: Treat password protection as defense in depth, use a dedicated password environment variable, and keep the local HTML file as the canonical artifact. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fuller-stack-dev/make-html) <br>
- [Recognition](references/recognition.md) <br>
- [Artifact Patterns](references/artifact-patterns.md) <br>
- [Interaction Patterns](references/interaction-patterns.md) <br>
- [Visual Quality](references/visual-quality.md) <br>
- [Validation](references/validation.md) <br>
- [Source Style](references/source-style.md) <br>
- [Custom Themes](references/custom-themes.md) <br>
- [Sharing HTML Artifacts](references/sharing.md) <br>
- [PageDrop About](https://pagedrop.io/about) <br>
- [PageDrop FAQ](https://pagedrop.io/faq) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Self-contained HTML files with inline CSS and JavaScript, Markdown fallback when files cannot be created, and optional shell commands for hosted sharing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline-first HTML by default; optional PageDrop upload is used only after the user requests or confirms hosted sharing.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
