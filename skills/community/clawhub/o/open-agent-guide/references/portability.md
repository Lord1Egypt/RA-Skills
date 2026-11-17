# Portability evidence and repairs

Portability classification uses semantic evidence, not literal vendor enum
wording. `data_import` and `data_export` accept only `full`, `partial`, `none`,
or the empty string for unknown. Never use booleans or explanatory prose as
their values. Judge import and export independently against the product's
material user data. Material user data means the user-owned records,
configuration, and produced artifacts needed to continue the product's
documented workflow elsewhere. Identify that scope from source evidence before
classifying transfer. For hosted workspaces, include documented material
records, configuration, and relationships. For APIs, include retained user
resources and configuration when present; a request/response interface alone
establishes neither migration nor its absence. For stateless/result-producing
tools, assess the actual result artifacts and any material reusable
configuration. Do not invent hosted workspaces, accounts, or history that the
tool does not maintain. Complete interoperable output of the material results
can support full export without a workspace archive, when the evidence also
accounts for any material reusable configuration. A reporter name or JSON/CSV
format alone does not establish complete fields or result coverage. Export
support does not imply an import capability.

For `data_export`, judge the exported output independently of import support in
this product or any destination. Do not require a destination importer,
round-trip restoration, or an end-to-end migration workflow. Complete documented
export can be `full` even when import is explicitly unavailable. Continue to
require evidence covering all material exported entities, fields, relationships,
and reusable configuration in open/interoperable formats. A promise to export a
complete set of records establishes record coverage; it does not by itself
establish preservation of their material fields, relationships, or reusable
configuration. A JSON endpoint alone does not fill those evidence gaps. Missing
import support is not an export limitation and cannot justify `partial` or
rejection of a complete export. Apply this rule to claim rationales, decision
summaries, and replacement advice. Review must correct a prior check that adds
an import or migration prerequisite; evaluate export coverage and fidelity from
the supplied source evidence. When that evidence leaves export scope unknown,
return `insufficient_evidence` and request the missing export evidence.
Recommend `partial` only when the sources establish an actual export limitation.

When no material data exists for a transfer direction, leave that scalar unset
and explain applicability; do not infer `full`, `none`, or an `n/a` enum value.
The existing dimension_applicability declaration is the only way to mark the
whole Portability dimension not applicable, and requires justification covering
integration/switching signals too. Stateless delivery alone does not justify it.

`full` requires evidence of complete transfer in open/interoperable formats
across material entity types, preserving material fields and relationships. Bulk
transfer is relative to the documented material data: a stateless tool can
transfer a complete run's artifacts as ordinary files. It need not aggregate
multiple runs or provide a separate export command. User-owned
input/configuration files that remain reusable unchanged need no additional
export facility. Require evidence that those files preserve the material
configuration; a file extension or download button alone is insufficient.
`partial` requires a documented transfer capability with limited entity
coverage, field fidelity, or proprietary-only formats. A lead-only CSV import
can be `partial` even when it supports every lead field; it does not establish
full migration of campaigns, messages, and other material product data. A full
workspace archive covering those entities and relationships in documented open
formats can support `full`. A CSV export omitting material custom fields or
relationships is `partial`. Absence of documentation is unknown, not `none`;
`none` requires evidence of no transfer capability. A generic import/export
mention without scope does not establish `full` or a specific limitation.

Assess entity coverage and preservation of material fields and relationships
separately. Creating destination projects or environment names is setup; it does
not prove migration of their configuration, metadata, or relationships. For
example, a secrets-upload script that creates project/environment names does not
by itself establish full workspace import. Missing fidelity documentation also
does not establish partial transfer: leave replacement advice unset when neither
classification has semantic support. Apply these same definitions to the
original claim and every proposed replacement. A list of transferred entities
without exclusive wording does not establish that other material entities are
excluded. For example, "imports secrets from JSON" and creation of
project/environment names establish a capability but no concrete limitation. Do
not turn that into "imports only secrets" or infer missing configuration
transfer from silence.

A successfully completed or atomic dump describes file creation. Wording such as
"never creates a partial dump file" does not establish transfer fidelity or
interoperability, and does not contradict `partial` by itself. Importing all
data contained in a dump only covers what the dump contains. Examine documented
omissions and their materiality to continuing the workflow, including whether
omitted credentials can be regenerated. A product-specific extension such as
`.dump` alone proves neither a proprietary-only format nor an open format.
Review must recheck prior claim rationales against these rules and the source
evidence; do not repeat invented workspace requirements or treat completion as
proof of full transfer. Name the actual missing scope, fidelity, or format
evidence when withholding a value.

Separate coverage and fidelity from access conditions. A paid-plan restriction,
row cap with repeatable batches, or rate limit alone does not make transfer
`partial`; record the condition in explanatory prose with evidence. A hard cap
that prevents transferring material data can support `partial`. Retention limits
define which data still exists; a 30-day retention window alone does not make
export of all retained data partial. Export limited to 7 days while 30 days
remain stored does. Do not assume batching, fidelity, or wider entity coverage
when the source does not establish it.

Regression examples from the category pilot: Snov.io prospect CSV/XLS imports
with field mapping, 100,000 rows, and 30 custom fields support
`data_import=partial` when the documented transfer scope is prospects. Hunter
CSV/TXT lead imports with field mapping and a 100,000-row limit likewise support
`data_import=partial` for the documented lead-only scope. The entity scope
supports these classifications; the row limits alone do not. Neither vendor must
call its feature "partial". These examples illustrate classification; new
submissions still need their own supplied evidence for the submitted product and
transfer scope.

Evaluate standard_protocol_access, no_proprietary_sdk, open_standards, and
documented_provider_swap independently using each field's definition. Each
assertion needs evidence for the submitted product. Missing evidence remains
unknown; it does not establish false. Use insufficient_evidence when sources do
not establish or contradict an assertion, and unsupported only when they
contradict it. Never recommend a false value from missing evidence. Evaluate
each field separately even when another field is explicitly contradicted.
`standard_protocol_access`: Direct access over HTTP/OpenAPI, gRPC, or GraphQL
qualifies. Documented HTTP requests are sufficient even with product-specific
JSON payloads or authentication; no additional named interchange standard is
required. An SDK's internal HTTP transport alone does not establish supported
direct access. `documented_provider_swap`: A documented way to replace the
cataloged product. Provider means the product being left. Identify that product
and an outbound migration guide or interchangeable interface with replacement
steps, destination and limitations. For interface replacement, document
endpoint, credentials and supported operations. Preserve operation, parameter,
model and plan limits; full parity is unnecessary. MCP setup, client connection,
backend model selection and protocol branding alone do not establish
replacement. An inbound competitor guide can support leaving its source product
when applicable, but not leaving its destination. Export, including private
account data, belongs in data_export; it alone establishes no replacement route.
Competitor imports belong in data_import, format interoperability in
open_standards, protocol access in standard_protocol_access, and SDK
independence in no_proprietary_sdk. JSON alone establishes no meaningful
interoperability. Record contract exit penalties, commitments, migration effort
and limits in switching_cost_notes; missing terms do not imply penalty-free
cancellation. A fixed vendor backend does not contradict a customer replacement
route. A sibling's route cannot support this product. Missing replacement
evidence is insufficient_evidence. A statement that one page lacks migration
instructions is page-local missing evidence, not proof that no route exists
elsewhere. Do not infer false; negative values require normal scoped absence
attestations. `no_proprietary_sdk`: The product is usable without a mandatory
single-vendor SDK. Documented direct requests without a required vendor SDK
qualify. Optional SDKs may exist; this field concerns mandatory SDK use. An
open-source vendor SDK alone does not establish SDK independence. Third-party
integration documentation can establish this route for the target product;
vendor-hosted documentation is not a prerequisite. Inspect the documented
installation, imports, authentication and operation, including required
dependencies. A third-party package with a complete usable setup and no required
target-vendor SDK can qualify. For example, a Haystack integration that
documents its package installation, Serper API key and search operation can
establish Serper API use without a Serper SDK. Do not infer a hidden vendor SDK
requirement merely because the example uses a third-party package. Conversely,
third-party authorship alone proves nothing: a wrapper that requires the target
vendor's SDK still requires that SDK. A complete documented client setup also
qualifies: identify the client, required configuration/authentication and a
usable product operation. For example, enabling MCP in a named client,
configuring the server URL, and issuing a documented in-client operation
establishes this route when no vendor SDK dependency is required by the setup. A
required hosted client application is not a vendor SDK. Do not demand raw
HTTP/curl examples, a generic API, or an additional SDK disclaimer for that
complete configuration-and-use workflow. An end-user connection is a complete
client route too: connecting a published connector or app from a named client's
directory and running a documented in-client operation establishes this route
even when the user configures no server URL. For example, opening a client's app
catalog, connecting the listed product, and issuing a documented in-client
request qualifies. End-user setup documentation suffices; developer or API
documentation is not a prerequisite, and a complete connect-and-use workflow
needs no further product-level evidence. Do not require an explicit
no-SDK-required sentence when these steps establish a route without a vendor
SDK. Preserve required components, the named client, supported-client list,
logged-in or regional eligibility, plan eligibility and other restrictions. A
bare MCP endpoint, protocol name, connector listing, app name, a connector for a
different product, or an incomplete example alone is insufficient. Name the
missing dependency or setup step when the route is incomplete. If neither a
usable SDK-free route nor mandatory SDK use is established, return
insufficient_evidence even when it rules out direct API access. Keep SDK
requirements and SDK-free routes attached to the product they describe through
extraction, assessment, and review. For a publisher policy covering multiple
services, identify the service covered by each passage. A sibling product's SDK
requirement cannot contradict this claim for the target product. Shared
ownership, a shared policy URL, or an SDK installation example alone does not
establish mandatory SDK use for the target. Conversely, direct HTTP or another
SDK-free route supports this claim only when documented as usable for the target
product. A sibling's route cannot support it. Explicit target-product
requirements with no SDK-free alternative contradict the claim. When target
applicability or the documented access route is unclear, return
insufficient_evidence. Explain the target product, the passage's service scope,
and whether evidence contradicts the claim or merely leaves target-product
SDK-free access unproven. Review must preserve this distinction even when a
prior check's rationale attributes SDK language to the wrong product.
`open_standards`: The product implements a named open, interoperable format or
protocol for actual data exchange or integration, such as CSV with field
mapping, iCalendar, OAuth 2.0, or MCP. Cite the product's implementation. HTTP
transport or a JSON response alone does not establish this field. A required
vendor SDK can still exchange standard formats; mandatory SDK use does not
establish absence of open standards. If the source only describes transport, SDK
requirements, or a planned API, return insufficient_evidence for this assertion.
To return unsupported, cite evidence ruling out standardized exchange itself.

Repair advice must keep proposed scalar values schema-valid and put reasons,
conditions, and missing evidence in separate explanatory text. If evidence
cannot support a replacement, recommend omitting the disputed assertion rather
than inventing a value. When useful, submit unrelated supported integration
updates separately from disputed portability claims. Every resulting submission
still needs all required checks and review approval; splitting never bypasses a
gate.

Before returning a portability verdict, check the proposed value against these
minimum evidence requirements. For `full`, identify the material data scope and
source evidence preserving that scope's fields/configuration in interoperable
form. For `partial`, identify the source's concrete excluded material data,
fidelity loss, or proprietary-only format. A capability with unknown
completeness meets neither requirement: return insufficient_evidence for the
original claim and supported=false for either proposed replacement. Review must
reject that unsupported assertion and leave replacement advice empty.

Examples with deliberately insufficient evidence:

- "Imports secrets from .env, JSON and YAML; a script creates
  project/environment names and uploads key/value pairs": neither full nor
  partial is established. Creation does not prove configuration fidelity;
  listing secrets does not prove other material entities are excluded.
- "Its CSV and JSON reporters output test results": neither full nor partial is
  established. Reporter names prove no field coverage and identify no omissions.
- "All indexes are saved to a .dump file; never creates a partial dump file":
  neither full nor partial is established without fidelity and format evidence.
  Use these examples only for their stated evidence. Additional evidence of
  actual complete transfer or concrete limitations can establish a value.

Automated reviews expose suggested portability replacements in
`metadata.portability_repairs`, each with `path`, `field`, `value`, and
`explanation`. Read the explanation and evidence before using the value in a new
draft. These are advisory suggestions, not patches or permission to merge.

## Portability enums clear a review-side grounding bar

Like a confirmed absence, a portability enum passing fact-check is not enough:
review independently rejects a `full` / `partial` / `none` value as "not
grounded" when the cited page does not establish a documented transfer
capability at that level for this product. The failure mode is choosing an enum
from the product's *shape* rather than from documented transfer — guessing
`none` for a product that looks closed, or `partial` for one with a download
button, without a page that documents the actual import or export. Two OpenTable
portability values were `review:rejected` this way in the 2026-10-28 run. The
grounding rule is the one above: cite a page that documents the transfer at the
level you chose; use `partial` only when the page shows the import or export
capability exists; and when no page documents transfer for a direction (or no
material user data exists to transfer), leave that scalar unset and explain
applicability rather than asserting an enum its silence cannot ground.
