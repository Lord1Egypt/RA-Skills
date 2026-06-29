## Description: <br>
Lanhu To Code helps agents convert Lanhu design drafts, specs, screenshots, exported assets, annotations, or design links into frontend code while following the target project's conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sucriss](https://clawhub.ai/user/sucriss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement frontend screens or components from Lanhu design material, including HTML, CSS, React, Vue, and Tailwind outputs. It is most useful when a coding agent needs to inspect a target codebase, extract design-system details, implement the UI, and verify visual fidelity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Design inputs may contain private product or interface information. <br>
Mitigation: Provide only Lanhu links, screenshots, specs, or exported assets that are appropriate for the coding task and review generated files before use. <br>
Risk: Incomplete Lanhu data can lead to visual or implementation assumptions. <br>
Mitigation: Compare the generated UI against available design material and document missing assets, inaccessible links, and intentional deviations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sucriss/skills/lanhu-to-code) <br>
- [Server-resolved source repository](https://github.com/SuCriss/lanhu-to-code) <br>
- [Source commit](https://github.com/SuCriss/lanhu-to-code/tree/8d75c5f498f1326fdbed469cd67032e38405565d) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, file-change summaries, verification commands, and screenshot or browser-check notes when applicable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve project conventions, document assumptions or missing Lanhu assets, and avoid hotlinking private Lanhu material.] <br>

## Skill Version(s): <br>
0.1.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
