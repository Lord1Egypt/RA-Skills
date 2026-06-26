## Description: <br>
A persistent autonomous engineering harness runtime that transforms repositories into self-improving software systems for agentic software development workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louis-szeto](https://clawhub.ai/user/louis-szeto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run a structured autonomous coding harness that coordinates research, planning, implementation, review, testing, recovery, and continuous improvement across a repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad autonomous agent, scheduling, repository-writing, and optional external-vault command authority. <br>
Mitigation: Install only in a sandboxed repository or throwaway branch, verify the platform controls in PLATFORM_REQUIREMENTS.md, and keep the default single-pass mode before enabling broader automation. <br>
Risk: Continuous mode, scheduler jobs, broad subagent spawning, and garbage-collection refactors can expand the operational scope of changes. <br>
Mitigation: Require explicit review and cleanup controls before enabling continuous operation or high-parallelism workflows. <br>
Risk: Optional Obsidian export can write outside normal repository documentation paths if the vault path is not trusted. <br>
Mitigation: Disable Obsidian export unless the vault path is trusted and validated. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/louis-szeto/harness-engineer) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Platform requirements](artifact/PLATFORM_REQUIREMENTS.md) <br>
- [Runtime loop](artifact/runtime/loop.md) <br>
- [Tool router](artifact/tools/tool-router.md) <br>
- [Security and performance](artifact/references/security-performance.md) <br>
- [Testing standards](artifact/references/testing-standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown instructions, repository documentation, code changes, and configuration guidance produced through the host agent platform.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; safe operation depends on host platform controls, sandboxed execution, scoped credentials, and human approval gates.] <br>

## Skill Version(s): <br>
5.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
