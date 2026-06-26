## Description: <br>
Reviews frontend UI code for visual consistency, design-system compliance, component structure, responsive behavior, and UI performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend reviewers use this skill to inspect UI code for design-system compliance, responsive layout issues, visual consistency, component structure, and UI performance concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent needs access to the UI files being reviewed, which may expose private source code during review. <br>
Mitigation: Limit review scope to the required files and follow the user's or organization's data-handling requirements for private code. <br>
Risk: The generated UI review may contain incorrect or context-insensitive recommendations. <br>
Mitigation: Have a developer or designer validate findings before applying changes to production code. <br>
Risk: The default report format is Chinese, which may not match the user's preferred review language. <br>
Mitigation: Ask the agent or host environment to use the desired language when a different report language is needed. <br>


## Reference(s): <br>
- [Canlah AI](https://canlah.ai) <br>
- [Front-End Checklist](https://github.com/thedaviddias/Front-End-Checklist) <br>
- [React Code Review Best Practices](https://pagepro.co/blog/18-tips-for-a-better-react-code-review-ts-js/) <br>
- [Vue Style Guide](https://v2.vuejs.org/v2/style-guide/) <br>
- [USWDS Design Tokens](https://designsystem.digital.gov/design-tokens/) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown UI review report with issue severity, file references, suggested fixes, and checklist summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports follow the skill's Chinese-language template unless the user or host requests another language.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
