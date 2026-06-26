## Description: <br>
Poi Clean plans nearby dining, cafe, dessert, mall, cinema, and date-spot recommendations from a local origin using POI recall, web evidence, scoring, and fallback area guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccmxigua](https://clawhub.ai/user/ccmxigua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to answer nearby-place requests with constraints such as origin, metro access, seating, category, budget, and avoid rules. It is most useful when an agent needs ranked recommendations, backups, weak-evidence notes, and next steps. <br>

### Deployment Geography for Use: <br>
Global, with strongest coverage for China local POI workflows and locations supported by the configured map and search providers. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically derive a user's location and share location-derived data with external map or search services. <br>
Mitigation: Use an explicit origin when location privacy matters, and review nearby queries before allowing device or IP-based location fallback. <br>
Risk: The skill requires a sensitive AMAP_KEY credential for map and routing calls. <br>
Mitigation: Keep AMAP_KEY scoped, rotate it as needed, and do not store it in shared files or published artifacts. <br>
Risk: Optional CoreLocationCLI use depends on a locally installed location utility and macOS permission prompts. <br>
Mitigation: Install CoreLocationCLI only from a trusted source and approve location access only when current-position lookup is intended. <br>


## Reference(s): <br>
- [Poi Clean on ClawHub](https://clawhub.ai/ccmxigua/local-poi-planner) <br>
- [Unified Search Suite dependency](https://clawhub.ai/ccmxigua/unified-search-suite) <br>
- [Output template](references/output-template.md) <br>
- [Planner lessons, 2026-05-31](references/lessons-2026-05-31.md) <br>
- [Planner lessons, 2026-06-01](references/lessons-2026-06-01.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown recommendations, JSON intermediate planner output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write /tmp/local-poi-planner-*.json and /tmp/local-poi-planner-*.md; reports include a top pick, backups, weak-evidence notes, and next steps.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
