## Description:

Verifies a client's newly supplied public FHIR endpoint's declared conformance surface before integration work begins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powmcp](https://clawhub.ai/user/powmcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to preflight a client's public FHIR base URL or metadata URL before onboarding. It helps separate CapabilityStatement structure, declared US Core coverage, and SMART discovery fields from live server behavior that still requires follow-up testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint details are sent to the PowMCP FHIR Server Check service.

Mitigation: Use only public FHIR endpoints and avoid credential-bearing, private, or patient-data URLs.

Risk: The setup command is not pinned to an immutable source in the artifact.

Mitigation: Prefer pinned or otherwise verified install sources where the execution environment supports them.

Risk: A clean declaration preflight can be mistaken for proof of live server behavior.

Mitigation: Treat the result as declaration evidence only and run separate live tests for required searches, OAuth launch behavior, Must Support behavior, returned-resource conformance, and certification evidence.

## Reference(s):

- [FHIR Server Check reference](references/fhir-server-check.md)
- [FHIR Server Check app page](https://powmcp.com/apps/fhir-server-check/)
- [SMART App Launch conformance requirements](http://www.hl7.org/fhir/smart-app-launch/conformance.html)
- [Inferno ONC Certification test kit](https://inferno.healthit.gov/test-kits/onc-certification-g10/)
- [FHIR Conformance Check for individual resources](https://powmcp.com/apps/fhir-conformance-check/)
- [ClawHub skill release page](https://clawhub.ai/powmcp/skills/preflight-client-endpoint-before-integration)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline commands and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports tool-produced declaration evidence and preserves unassessed areas without recalculating returned figures.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
