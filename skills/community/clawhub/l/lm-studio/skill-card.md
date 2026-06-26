## Description: <br>
Run and integrate LM Studio with local model lifecycle control, OpenAI-compatible APIs, embeddings, and MCP-aware workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate LM Studio locally, verify server readiness, manage local model lifecycle choices, connect OpenAI-compatible clients, and troubleshoot API, embedding, and MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may keep local operational notes under ~/lm-studio/. <br>
Mitigation: Store only verified runtime facts and avoid tokens, passwords, or copied credentials in local notes. <br>
Risk: Guided commands may change which local models are loaded, affecting memory, GPU use, and runtime behavior. <br>
Mitigation: Verify server reachability and model readiness after each runtime change, and record only known-good combinations. <br>
Risk: MCP servers or remote endpoints can expand file, tool, or network access beyond the local LM Studio server. <br>
Mitigation: Enable only trusted MCP servers or remote endpoints with explicit user intent, and test model serving separately from tool access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/lm-studio) <br>
- [Skill homepage](https://clawic.com/skills/lm-studio) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local runtime checks, OpenAI-compatible API examples, model-loading guidance, MCP configuration guidance, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
