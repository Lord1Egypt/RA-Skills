## Description: <br>
OpenClaw Workflow Architect helps developers design, review, and generate OpenClaw workflows using Lobster and OpenProse, including approval gates, layered architecture decisions, and .prose/.lobster files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thanh01pmt](https://clawhub.ai/user/thanh01pmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow engineers use this skill to choose the right OpenClaw layer, review existing .lobster/.prose designs, and generate workflow file structures with approval and compatibility guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .lobster and .prose workflows can automate file writes, CLI calls, and other side effects. <br>
Mitigation: Review generated workflow files before running them, confirm output paths, and keep approval gates before side effects. <br>
Risk: Remote .prose URLs or untrusted workflow sources can introduce unsafe automation. <br>
Mitigation: Avoid running remote .prose URLs from untrusted sources and inspect imported workflow content before use. <br>
Risk: OpenProse workflows may not run correctly on systems that are not Prose Complete. <br>
Mitigation: Use the skill's compatibility checks, test .prose workflows before relying on them, and prefer Lobster-only or mixed fallback modes when compatibility is uncertain. <br>


## Reference(s): <br>
- [OpenClaw Workflow Architect ClawHub page](https://clawhub.ai/thanh01pmt/openclaw-workflow-architect) <br>
- [Layering Guide](references/layering-guide.md) <br>
- [Lobster Technical Specification](references/lobster-spec.md) <br>
- [OpenProse Technical Specification](references/openprose-spec.md) <br>
- [OpenClaw Lobster documentation](https://docs.openclaw.ai/tools/lobster) <br>
- [OpenClaw Prose documentation](https://docs.openclaw.ai/prose) <br>
- [Prose documentation](https://www.prose.md) <br>
- [Curriculum Pipeline Example](references/examples/curriculum-pipeline.md) <br>
- [Gate Approval Example](references/examples/gate-approval.md) <br>
- [Lesson Worker Example](references/examples/lesson-worker.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with .prose/.lobster code and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workflow folder structures, compatibility notes, approval checklists, and recommended commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
