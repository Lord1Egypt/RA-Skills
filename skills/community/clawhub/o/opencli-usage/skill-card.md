## Description: <br>
Use at the start of any OpenCLI session - this is the top-level map of what `opencli` can do, how to discover adapters, what flags and output formats are universal, and which specialized skill to load next. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill as an orientation guide for OpenCLI sessions: discovering installed adapters, choosing command output formats, understanding browser bridge prerequisites, and finding the next specialized OpenCLI skill to load. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents toward OpenCLI flows that can use logged-in browser or desktop app sessions, external CLI passthrough, plugin installs, and cached browser or network state. <br>
Mitigation: Install only from trusted OpenCLI sources, use a separate low-privilege browser profile, begin with read-only discovery commands, manually approve plugins, packages, external CLIs, and state-changing actions, and clear or isolate the OpenCLI cache after sensitive work. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides operational guidance for command discovery, adapter usage, browser bridge setup, plugin management, and external CLI passthrough.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
