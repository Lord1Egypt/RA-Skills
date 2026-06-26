## Description: <br>
Generates personalized learning content and short self-check quizzes for nodes in an input knowledge graph, adapting depth by L1/L2/L3 hierarchy and parent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzp2026](https://clawhub.ai/user/wzp2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and education-content authors use this skill to turn a knowledge graph node and its parent context into node-level learning material, quiz questions, and verification artifacts for learner review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curriculum may be inaccurate or misleading when it presents topic-specific content as authoritative. <br>
Mitigation: Treat output as a rough draft and manually verify every cited source before learner or production use. <br>
Risk: The RAG enhancer can query external Wikipedia and arXiv services with course, project, or learner topics. <br>
Mitigation: Avoid using the enhancer with confidential topics unless external lookups are acceptable; sanitize topics or disable enhancement when needed. <br>
Risk: The artifact behavior includes fixed blockchain-oriented defaults that may not fit arbitrary knowledge graph domains. <br>
Mitigation: Review generated content for topic fit and replace irrelevant defaults, examples, and citations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzp2026/learning-content-generator) <br>
- [Learning Content Generator README](references/README.md) <br>
- [Content generation configuration](references/content_config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown learning-content files, quiz Markdown, JSON content data, and verification summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Main content is described as 3000-5000 characters per node with 3-5 single-choice quiz questions; long text may be split.] <br>

## Skill Version(s): <br>
2.3.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
