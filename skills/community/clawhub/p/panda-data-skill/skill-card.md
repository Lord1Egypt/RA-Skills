## Description: <br>
Panda Data Skill wraps PandaAI financial data APIs as LLM-callable tools for market data, fundamentals, futures, indexes, calendars, and related financial datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pandaai-tech](https://clawhub.ai/user/pandaai-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent query PandaAI financial datasets through documented tool calls after installing the required Python packages and configuring PandaAI credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PandaAI account credentials could be exposed if users paste a real username or password into chat or public logs. <br>
Mitigation: Configure PANDA_DATA_USERNAME and PANDA_DATA_PASSWORD directly in a local environment, .env file, or secret manager instead of sharing credentials with the agent. <br>
Risk: Financial query parameters and research inputs may be sent to PandaAI's API when tools are called. <br>
Mitigation: Avoid confidential trading research inputs unless the user accepts that those parameters are sent to PandaAI. <br>
Risk: The skill depends on external PyPI packages for execution. <br>
Mitigation: Install only after reviewing and accepting the PandaAI and required PyPI package dependencies in the target environment. <br>


## Reference(s): <br>
- [Panda Data Skill on ClawHub](https://clawhub.ai/pandaai-tech/panda-data-skill) <br>
- [PandaAI-Tech publisher profile](https://clawhub.ai/user/pandaai-tech) <br>
- [panda-data-tools on PyPI](https://pypi.org/project/panda-data-tools/) <br>
- [PandaAI website](https://www.pandaai.online) <br>
- [Installation guide](artifact/INSTALL_GUIDE.md) <br>
- [API reference](artifact/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; tool calls return formatted table text or JSON error text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PandaAI credentials and the panda_data and panda-data-tools Python packages.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
