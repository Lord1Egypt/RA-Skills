## Description: <br>
Multi-stage multi-agent reasoning middleware that reduces LLM hallucination by 70%+. 9 specialized emergence engines for invention, creative, pharma, genomics, chemistry, ecology, law, recipe, and document generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cutechicken99](https://clawhub.ai/user/Cutechicken99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to route OpenAI-compatible model calls through MARL's multi-stage reasoning middleware for more thoroughly checked responses. It supports domain modes for invention, creative work, pharma, genomics, chemistry, ecology, law, recipes, and document generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model prompts and responses are routed through third-party middleware. <br>
Mitigation: Review the VIDRAFT Docker or PyPI package before use, pin the version, and deploy only in environments where that dependency is trusted. <br>
Risk: Prompts may be sent to the configured LLM provider unless the backend is fully local. <br>
Mitigation: Avoid sensitive data until data handling is clear, and use a local model backend when data must remain inside controlled infrastructure. <br>
Risk: The artifact makes a broad claim that data never leaves local infrastructure. <br>
Mitigation: Confirm the configured model endpoint and network path before relying on local-only privacy behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Cutechicken99/marl-middleware) <br>
- [PyPI package](https://pypi.org/project/marl-middleware/) <br>
- [GitHub repository](https://github.com/Vidraft/MARL) <br>
- [Hugging Face demo](https://huggingface.co/spaces/VIDraft/MARL) <br>
- [FINAL Bench leaderboard](https://huggingface.co/spaces/FINAL-Bench/Leaderboard) <br>
- [VIDRAFT website](https://vidraft.net) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [OpenAI-compatible text responses with YAML or JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mode suffixes such as ::create or ::pharma select specialized reasoning engines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
