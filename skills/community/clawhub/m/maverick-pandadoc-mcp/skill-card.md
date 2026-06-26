## Description: <br>
Use PandaDoc integration context for documents, templates, recipients, proposals, and document status after Maverick connects PandaDoc and provisions runtime OAuth credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work with PandaDoc documents, templates, recipients, proposals, and document status through Maverick-provisioned runtime OAuth credentials. It is intended for PandaDoc-related workflows where the agent first inspects available runtime tools and confirms user intent before write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access PandaDoc business data through OAuth-backed runtime tools. <br>
Mitigation: Install only when Maverick-provisioned PandaDoc OAuth credentials are expected, use a dedicated account where possible, and avoid passing unrelated sensitive content through the tools. <br>
Risk: Write-capable PandaDoc operations can affect customer-visible document and signing workflows. <br>
Mitigation: Confirm clear user intent before create, send, update, complete, delete, or status-changing actions, and read current document or template state before making changes. <br>
Risk: The local mcporter credential vault may contain OAuth material on shared machines. <br>
Mitigation: Keep the ~/.mcporter credential vault protected and re-authorize the integration if OAuth grants are revoked. <br>
Risk: The artifact notes that no provider-owned PandaDoc MCP manifest is registered yet. <br>
Mitigation: Inspect available PandaDoc runtime tools before use and do not invoke the bundled wrapper until a provider MCP manifest is added. <br>
Risk: The install metadata uses the unpinned mcporter package. <br>
Mitigation: Operators with strict supply-chain controls should override the install to pin a reviewed mcporter version. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-pandadoc-mcp) <br>
- [mcporter MCP CLI](https://github.com/steipete/mcporter) <br>
- [jq](https://stedolan.github.io/jq/) <br>
- [util-linux flock](https://github.com/util-linux/util-linux) <br>
- [Perl Digest::SHA](https://metacpan.org/pod/Digest::SHA) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command snippets and YAML metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Maverick-provisioned PandaDoc OAuth environment variables and local command dependencies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
