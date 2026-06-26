## Description: <br>
Fetches an Aavegotchi by ID from Base mainnet, displays full traits, and generates on-chain SVG plus PNG image outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to look up Aavegotchi assets by numeric ID, inspect traits and rarity data, and produce shareable metadata and image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node.js and shell scripts with npm dependencies. <br>
Mitigation: Install and execute it only in an environment where local script execution and dependency installation are acceptable. <br>
Risk: The skill queries public blockchain and API endpoints and may depend on endpoint availability or returned public data. <br>
Mitigation: Use a trusted Base mainnet RPC endpoint and review results before relying on generated stats or images. <br>
Risk: The skill creates JSON, SVG, and PNG files in the local workspace. <br>
Mitigation: Choose an appropriate output directory and review generated files before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaigotchi/gotchi-finder) <br>
- [Publisher profile](https://clawhub.ai/user/aaigotchi) <br>
- [Base mainnet RPC endpoint](https://mainnet.base.org) <br>
- [Aavegotchi Base subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, image files] <br>
**Output Format:** [Markdown captions with shell command guidance and generated JSON, SVG, and PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, jq, and a Base mainnet RPC endpoint; writes gotchi-{ID} JSON, SVG, and PNG files locally.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata, CHANGELOG, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
