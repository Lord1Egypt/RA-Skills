# FHIR Server Check reference

## Role in this job

`powmcp-fhir-server-check:capability_check` checks the current declarations published by one named public FHIR R4 endpoint.
Run it immediately after receiving the public endpoint and before client code, registration, or credential provisioning begins.
The tool is read-only and fetches without authentication.

## What it measures

The check fetches the public CapabilityStatement and path-relative SMART configuration document.
From `baseUrl`, it appends `/metadata?_format=json` and `/.well-known/smart-configuration` to the full base path.
From `metadataUrl`, it drops the query and fragment, strips the trailing `/metadata`, and derives SMART discovery from the remaining origin and path.
It validates the CapabilityStatement structurally with the pinned official HL7 FHIR Validator 6.9.11.
The validator runs offline against app-local pre-fetched IG packages.
It inventories declared resource types and interactions at the server declaration level.
It reports US Core server resource-type coverage as covered and missing resource types.
It separately reports SMART discovery state, capabilities, authorization endpoint, and token endpoint.
It groups repeated structural errors into distinct findings and retains occurrence counts.
It also returns raw issue occurrences by severity, source, and location.

## Criterion and granularity

`conforms` and `capabilityState` concern the CapabilityStatement document’s structure alone.
US Core coverage means that the CapabilityStatement lists the resource types.
SMART discovery concerns the separately fetched well-known document.
For a server implementing SMART App Launch, `authorization_endpoint` and `token_endpoint` are required published fields.
One repeated rule violation is one distinct finding even when it occurs across many declared resources.
A repeated unresolvable vendor extension can therefore produce hundreds of raw occurrences but represent one distinct fix.

## Inputs requiring judgment

Supply exactly one of `baseUrl` or `metadataUrl`.
`baseUrl` is the public FHIR base and preserves its full path when deriving both document URLs.
`metadataUrl` is a direct public metadata URL. The tool adds `?_format=json` if it is missing.
Do not supply both URL inputs and do not omit both.
Set `maxIssues` only when the raw issue list needs a different cap.
`maxIssues` accepts integers from 1 to 1000.
Its default is 400.
The cap affects only the raw `issues` list. Distinct-finding counts still cover every issue produced.
Do not repeat URL query strings or credentials in narration.

## Duration

A large metadata document typically takes roughly 15 to 40 seconds because loading the app-local packages dominates latency.
State that duration before calling.

## Result fields to quote

Read and quote `conforms` first.
Read and quote `distinctFindings.errorTotal` next.
Quote distinct finding messages, cited locations, and occurrence counts without recalculation.
Record the returned validator version, pinned IG packages, and terminology mode.
Record declared resources and interactions.
Record the US Core covered and missing resource-type split.
Record SMART discovery state, capabilities, authorization endpoint, and token endpoint separately.
Record the combined missing list.
Record raw issue evidence when it is needed for repair.
Record whether the issue list was truncated.

## What a pass proves

A pass proves that the fetched CapabilityStatement passed the reported structural validation for that run.
It does not prove required search support, `_include` or `_revinclude` support, Must Support behavior, SMART conformance, certification, or conformant data from live endpoints.
A structurally valid CapabilityStatement can describe a server whose live endpoints behave differently.
Declared US Core resource types are not evidence that the required searches work.
Published SMART fields are declarations, not evidence of a successful authenticated OAuth launch.

## Structurally unassessable areas

Offline terminology validation cannot confirm membership in external LOINC, SNOMED CT, or RxNorm code systems.
Report that membership as unchecked rather than passed.
Missing or unreadable SMART discovery leaves SMART requirements unestablished without changing CapabilityStatement structural conformance.
A truncated raw issue list leaves omitted occurrences outside the displayed list even though distinct-finding counts cover every produced issue.

## Failure handling

The contract supplies no named failure-code enumeration. Do not invent failure codes.
For both URL inputs or neither URL input, tell the user: “The declaration check did not run because exactly one of `baseUrl` or `metadataUrl` is required.”
For an out-of-range issue cap, tell the user: “The declaration check did not run because `maxIssues` must be an integer from 1 to 1000.”
Correct the named field and call again. An invalid argument does not trigger unavailable-tool handling.
When the tool is absent from the session, use the exact two-path notice in `SKILL.md`.
When SMART discovery is missing or unreadable, quote the returned state and keep SMART discovery in the not-checked list with the returned reason.

## Non-PowMCP path

Fetch the public CapabilityStatement and path-relative SMART well-known document with a browser or HTTP client.
Preserve both complete responses.
Run the official HL7 FHIR Validator against the downloaded CapabilityStatement with the required IG packages.
Inspect FHIR version, per-resource interactions, search parameters, SMART capabilities, and OAuth endpoints as separate declarations.
This path does not establish live behavior and does not produce a `capability_check` result.
Use Inferno or another running-server suite for required searches, OAuth launch behavior, Must Support behavior, returned-resource conformance, or certification evidence.

## Source-of-truth links

- SMART App Launch v2.2.0 conformance requirements: http://www.hl7.org/fhir/smart-app-launch/conformance.html
- FHIR Server Check app page: https://powmcp.com/apps/fhir-server-check/
- Inferno ONC Certification test kit: https://inferno.healthit.gov/test-kits/onc-certification-g10/
- FHIR Conformance Check for individual resources: https://powmcp.com/apps/fhir-conformance-check/
