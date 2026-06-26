## Description: <br>
帮助用户审计、共创、分阶段落地并持续优化基于 OpenClaw 的 GTD 个人知识管理（PKM）系统，适用于从零搭建、旧库重构、目录与标签策略、AGENTS.md/HEARTBEAT.md/TODO 自动化设计，以及后续迭代。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaor1995](https://clawhub.ai/user/zhaor1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to audit, design, phase in, and refine a GTD-based personal knowledge management system for Markdown, Obsidian, or OpenClaw workflows. It supports collaborative planning, directory and tag strategy, staged scaffolding, and ongoing workflow review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scaffolding in the wrong knowledge-root can add directories and Markdown templates to an unintended folder. <br>
Mitigation: Confirm the target knowledge-root before running bootstrap_knowledge.py and prefer an existing backup or Git snapshot for established note libraries. <br>
Risk: Using --force can overwrite existing template files created by earlier GTD/PKM work. <br>
Mitigation: Run the audit workflow first when unsure and use --force only after intentionally accepting template replacement. <br>
Risk: Directory, tag, or automation recommendations can disrupt a user's existing PKM habits if applied all at once. <br>
Mitigation: Apply the skill's staged rollout posture: audit first, align on a blueprint, implement one clear phase, then review friction before further changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaor1995/gtd-pkm) <br>
- [README](README.md) <br>
- [共创式设计流程](references/collaborative-design-playbook.md) <br>
- [GTD 个人知识库框架](references/gtd-knowledge-framework.md) <br>
- [OpenClaw 自动化配方](references/openclaw-automation-recipes.md) <br>
- [OpenClaw 可迁移模式](references/openclaw-portable-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands and generated Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local GTD directory scaffolds and audit reports when the user explicitly runs the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
