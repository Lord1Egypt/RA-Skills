## Description: <br>
Delegate web and API data fetching to local LLMs for research tasks, saving tokens and keeping data private while using your local machine for analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solsuk](https://clawhub.ai/user/solsuk) <br>

### License/Terms of Use: <br>
Single-user license <br>


## Use Case: <br>
Developers and OpenClaw users use Grago to delegate web, API, RSS, log, and local file research tasks to a local LLM. It is intended for trusted, single-user environments where the user controls the agent and accepts local command execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad unsandboxed shell and file access on the user's machine. <br>
Mitigation: Install only on a trusted personal machine, VM, or container where you are comfortable letting the agent run shell commands as your user. <br>
Risk: Using the skill on shared systems, public agent endpoints, or machines with sensitive files can expose data or allow unwanted command execution. <br>
Mitigation: Do not use it in those environments unless you add sandboxing and review sources.yaml files before use. <br>
Risk: Command strings and configuration can expose long-lived secrets or send data to untrusted model endpoints. <br>
Mitigation: Keep model endpoints local or otherwise trusted, and avoid putting long-lived secrets in configs or command strings. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/solsuk/grago) <br>
- [Ollama](https://ollama.ai) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, or text returned from local model analysis and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Input sent to the local model is truncated according to the configured max_input_chars value.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
