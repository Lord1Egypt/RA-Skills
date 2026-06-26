## Description: <br>
Manage multi-tier AI inference clusters for homelabs, including health monitoring, expert MoE routing, automatic node recovery, model deployment across Ollama and llama.cpp nodes, GPU memory planning, Docker volume strategies, sequential startup patterns, and LiteLLM gateway configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlesnews](https://clawhub.ai/user/mlesnews) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and homelab operators use this skill to manage distributed AI inference infrastructure, route requests across heterogeneous model endpoints, recover unavailable nodes, and plan model deployments across local, remote, and CPU fallback tiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward remote host access, Docker Desktop restarts, container restarts, and recovery workflows. <br>
Mitigation: Require manual approval before SSH, RDP, Docker Desktop, or container restart actions, and restrict automation to named hosts and containers. <br>
Risk: Recovery and deployment workflows may involve infrastructure credentials. <br>
Mitigation: Use least-privilege credentials from a vault and avoid plaintext secrets or command-line secret arguments. <br>
Risk: Operational commands can disrupt running inference services if applied without environment-specific checks. <br>
Mitigation: Test commands manually in the target homelab environment before allowing an agent to automate them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mlesnews/homelab-cluster) <br>
- [Lumina Homelab](https://luminahomelab.ai) <br>
- [GitHub Profile](https://github.com/mlesnews) <br>
- [X Profile](https://x.com/HK47LUMINA) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational recommendations for remote hosts, Docker containers, model endpoints, and LiteLLM gateway settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
