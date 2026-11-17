## Description:

Provides AI agents with workflows and references for machine learning, PyTorch deep learning, computer vision, reproducible experiments, model evaluation, and related agent engineering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT

## Use Case:

Developers and ML engineers can use this skill collection to plan and implement machine learning workflows, from data preparation and evaluation to PyTorch training and computer vision. It also provides guidance for reproducibility, agent development, and agent evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation may involve private documents or production logs, which could be sent to a model provider or tracking service.

Mitigation: Before use, approve the provider, tracking destination, access controls, and retention settings; consider local logging.

Risk: The bundled CSV checker’s class-distribution calculation can be flawed, and helper scripts referenced by evaluation guidance may not be included.

Mitigation: Independently verify class distribution and confirm that required helper scripts are available before relying on evaluation results.

Risk: Future remote dependency versions are outside the current security review.

Mitigation: Use reviewed, pinned dependency sources and install only the components needed for the task.

## Reference(s):

- [ClawHub release](https://clawhub.ai/skills-repo/skills/machine-learning-engineer)
- [Experiment reproducibility playbook](artifact/references/experiment-reproducibility.md)
- [Model evaluation playbook](artifact/references/model-evaluation.md)
- [ML pipeline design playbook](artifact/references/ml-pipeline-design.md)
- [Agent evaluation playbook](artifact/references/agent-evaluation.md)
- [MCP server generation playbook](artifact/references/mcp-server-generation.md)
- [Claude API playbook](artifact/references/claude-api-playbook.md)
- [Machine learning skill source](https://skills.sh/mindrally/skills/machine-learning)
- [Deep learning with PyTorch skill source](https://skills.sh/mindrally/skills/deep-learning-pytorch)
- [Computer vision skill source](https://skills.sh/mindrally/skills/computer-vision-opencv)
- [PyTorch patterns skill source](https://skills.sh/affaan-m/everything-claude-code/pytorch-patterns)
- [Claude Agent SDK skill source](https://skills.sh/bobmatnyc/claude-mpm-skills/anthropic-sdk)
- [MCP server generation skill source](https://skills.sh/github/awesome-copilot/python-mcp-server-generator)
- [Agent evaluation skill source](https://skills.sh/mlflow/skills/agent-evaluation)
- [Anthropic API documentation](https://docs.anthropic.com)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown guidance with code examples, shell commands, and reusable templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scripts or configuration examples tailored to the user's project.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
