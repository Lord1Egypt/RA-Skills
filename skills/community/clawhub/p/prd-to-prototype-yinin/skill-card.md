## Description: <br>
Turns a product idea into a complete PRD, then generates a high-fidelity HTML/Tailwind prototype for mobile or desktop after platform confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinin2005](https://clawhub.ai/user/yinin2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, founders, designers, and developers use this skill to convert early product ideas into a Chinese PRD with user flows, then into a browser-previewable prototype for mobile or desktop review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad auto-activation can turn vague product ideas into files without first asking clarifying questions. <br>
Mitigation: Use it only in workspaces where automatic PRD creation is expected, and review the generated PRD before proceeding to prototype generation. <br>
Risk: The skill writes to /workspace/docs and /workspace/prototype during normal execution. <br>
Mitigation: Run it in a clean or disposable workspace, or review existing files before execution to avoid overwriting important work. <br>
Risk: Prototype deployment may expose generated product concepts if deploy tooling is available. <br>
Mitigation: Require explicit publish confirmation or disable deployment tools, and avoid entering confidential product details unless preview publication is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinin2005/prd-to-prototype-yinin) <br>
- [Tailwind CSS CDN](https://cdn.tailwindcss.com) <br>
- [Font Awesome 6 stylesheet](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css) <br>
- [Unsplash image example](https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Chinese Markdown plus HTML, Tailwind CSS, and Vanilla JavaScript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a PRD to /workspace/docs/prd.md and prototype files under /workspace/prototype/ when executed by an agent with filesystem access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
