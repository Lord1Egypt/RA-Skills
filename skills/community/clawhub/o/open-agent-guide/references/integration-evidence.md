# Integration evidence

Read this when adding documentation pointers, APIs, MCP servers, SDKs, CLIs, or
agent skills.

## Official llms.txt index

`llms_txt_url` links the product's official llms.txt documentation index. Submit
its observed URL, including docs subdomains, official hosted docs and scoped
paths such as `/docs/llms.txt`. The pointer itself supplies the evidence;
verification checks its content and product identity. HTML fallback pages and
guessed paths are insufficient. Omit unknown values or send an empty string to
clear a stored URL. A verified URL earns +1 raw Integration point within its
10-point cap and counts toward coverage. A whole-field `llms_txt_url` absence
attestation earns coverage without Integration points. For `page_silence`, cite
the official product documentation homepage/index or official marketing homepage
that is sufficiently complete to show or link the index across permitted docs
hosts and scoped paths. A scoped explicit vendor negative statement also
qualifies. A guessed-path 404, failed fetch, unrelated page or incomplete
silence excerpt is insufficient; a discovered official llms.txt document
contradicts absence. Use the existing `field_key`, `method`, `source_url`, and
optional `checked_at` shape with a blank label. For example:

```json
{"field_key":"llms_txt_url","method":"Inspected the complete official docs index and its linked documentation locations; no llms.txt index is shown or linked.","source_url":"https://vendor.example/docs/"}
```

The example describes the evidence to collect; substitute the page actually
inspected. Unknown values remain unknown, and clearing a URL requires no absence
evidence.

## Personal Agent Protocol (Poppy) support

`poppy_discovery_url` links the product's Personal Agent Protocol ("Poppy")
discovery document. The protocol serves that document at one authoritative
location, `/.well-known/poppy.json`, on the product's own origin. Submit that
well-known URL; verification checks that the document is a valid Poppy document
(a JSON document declaring a `protocol_version`) whose organization applies to
the product. A present value advertises Poppy support; it does not establish
end-to-end protocol conformance. A verified URL earns +1 raw Integration point
within its 10-point cap and counts toward coverage. Omit unknown values or send
an empty string to clear a stored URL.

Absence is simpler than the other pointers because the location is
authoritative. A whole-field `poppy_discovery_url` absence attestation needs
only an observed HTTP 404 at `/.well-known/poppy.json` on the product's own
origin; cite that URL and record the observed status and time in `method`. No
homepage silence or further discovery is required. A timeout, DNS or TLS
failure, access block, rate limit, server error, or non-Poppy document is
unresolved, not absence. A valid applicable Poppy document contradicts absence.
For example:

```json
{"field_key":"poppy_discovery_url","method":"GET https://vendor.example/.well-known/poppy.json returned HTTP 404 on 2026-11-21.","source_url":"https://vendor.example/.well-known/poppy.json"}
```

## Documentation resource labels and evidence

Use descriptive `name` and `verbose_name` labels for documentation resources.
They need no exact vendor-title match. Choose any valid synthetic `slug`; it
needs no vendor citation or URL-path match. Cite content establishing that the
URL documents the product and supports factual qualifiers in the labels, such as
capabilities, plan eligibility, or guarantees. A reachable unrelated page or a
plausible document name is insufficient. Repair missing evidence or remove the
unsupported assertion; cosmetic slug changes cannot fix it. This applies to both
nested `documentation_resources.create` and direct documentation entries.

## Typed pointer URLs must lead to the right kind of page

The `pointer_content` check fetches each **typed** pointer URL and verifies the
page actually is that kind of page: `trust_center_url`, `documentation_url`,
`terms_of_service_url`, `privacy_policy_url`, `status_page_url`, `pricing_url`,
`source_code_url`, and every `api_specs[].url`. API specifications also require
product attribution from parsed metadata. HTML pointers are judged semantically
(does the trust center give access to compliance evidence; does the page present
docs / pricing / … content?); `api_specs[].url` must parse as an OpenAPI/Swagger
document. The bare canonical `url` (the homepage) is **not** content-verified —
its reachability is covered by the `urls` check.

A typed pointer hard-fails the submission when its page is the wrong kind, is a
dead link, or is blocked by a bot wall the fetcher can't get past — and the
close reason **names which links were anti-bot-blocked** distinctly from the
wrong-kind ones. So:

- Emit a typed `*_url` only when the page plainly presents that kind of content
  (a privacy page whose text reads as a privacy policy, a pricing page that
  shows plans). A marketing homepage dropped into `documentation_url` now fails
  as `wrong_content`.
- The fetcher renders JavaScript and, when a page blocks the primary fetch,
  escalates once to an anti-bot tier (ZenRows: JS render + residential proxy),
  so a JS-heavy or lightly bot-gated page can now pass. A page that blocks even
  that tier is `anti_bot_blocked` and hard-fails — be ready to drop it and
  resubmit without it (or point at the static page that renders the content),
  exactly as you would for a bot-gated cert page.
- For `api_specs[].url`, point at the raw spec document (the `.json`/`.yaml`
  OpenAPI file), not an HTML API-reference portal that merely *renders* a spec —
  the check parses the body as a spec.

## Resolve an unverified pointer

A successful source preview confirms retrievable evidence only. It does not
confirm the pointer's kind or product attribution. Read the final pointer check.

The verifier checks complete bounded OpenAPI/Swagger documents, then judges
product identity from title, description, contact and server metadata. GraphQL
and gRPC artifacts currently remain unverified. Supply a supported raw
specification or omit the optional pointer. Do not substitute an HTML API page.

For `llms_txt_url`, supply an official Markdown documentation index with
documentation links. Headings are optional. The verifier sends the complete
index to a large-context model. It does not follow every link. Archives and
executables cannot supply text evidence.

For `resource_limit`, read `details.pointer_verification[].limit_stage` to
distinguish transport, parser, request allocation and model context limits. Read
`details.pointer_verification[].next_action` for replacement evidence guidance.
No content verdict was made. Keep accurate claims unchanged. Use a smaller
complete authoritative resource or report the verifier limitation to
`support@openagentguide.com`. A URL fragment does not reduce fetched content. An
inconclusive MCP probe or insufficient identity evidence remains unverified and
blocks publication.

## Add `api_specs` for a machine-readable spec — the body is parse-checked, exempt from the citation bar

An `api_specs` entry's identity — `name`, `slug`, `spec_type`, and the spec
`url` — is **record structure**, not a fact-checked world-claim, so it is not
held to the citation bar a vendor page must corroborate. Almost no vendor page
states "product X documents an OpenAPI spec named Y at Z" in a citeable form, so
holding it to that bar used to sink otherwise-clean submissions — that is scoped
out.

But the `pointer_content` check still fetches the spec `url` **raw** and parses
the body as an OpenAPI/Swagger document, so a reachable `200` is not enough on
its own: point the `url` at the raw spec file (the `.json`/`.yaml` OpenAPI
document), **not** an HTML API-reference or introduction page that merely
renders a spec. A reference or introduction page is not a spec and hard-fails
`wrong_content`, exactly as in "Typed pointer URLs must lead to the right kind
of page" above. When the vendor publishes no machine-readable spec, keep the
human API docs under `documentation_url` and omit the `api_specs` entry rather
than pointing it at a reference page.

This exemption from the *citation* bar is specific to `api_specs` and
`developer_kits`, whose URLs are self-describing: `mcp_servers` and
`command_line_interfaces` are **not** exempt — they are held to the citation bar
(see below), because a protected MCP endpoint or a CLI page tells the pipeline
nothing it can verify without a citation.

## Add an MCP server — but cite the docs page that documents it

MCP endpoint evidence must link the exact endpoint to the cataloged product and
its functionality through an applicable documentation passage or equivalent
authoritative evidence. Record the source URL and supporting passage for
verification and curation. Evaluate availability, HTTP status, ownership, and
product applicability separately. HTTP 200, 401, or 405 alone establishes
neither ownership nor applicability. Authenticated endpoints are valid when
documented; no unauthenticated success or MCP handshake is required. Hunter's
setup docs naming its endpoint, Hunter tools, and authorization are supporting
evidence; a bare unauthorized response is not. Reject or repair missing product
linkage even when automated checks passed.

An `mcp_servers` entry is a **world-claim held to the citation bar**, unlike
`api_specs`. It has no writable `slug`; the server's `name` and endpoint `url`
are a claim about the world — *"operates an MCP server at `<endpoint>`"* — that
the vendor's own docs must support. The `urls` check verifies the endpoint is
reachable (a bare GET answering `401` / `403` / `405` / `429` counts as
reachable — the "protected" set), but reachability alone is **not** enough: an
endpoint that 401s is not self-describing, so a reachable-but-uncited MCP server
is indistinguishable from a fabricated one and the review agent rejects the
whole submission. (We deliberately verify MCP servers by citation rather than by
querying the endpoint for its tool manifest — keeping the one rule, "cite the
docs," is preferred over maintaining MCP metadata-retrieval code.) So **add an
MCP server only when a vendor page documents one, and cite that page**; the
fact-check evaluates whether the cited passage supports that endpoint and its
product scope. Do not add an MCP server off the bare endpoint URL alone. Put the
actual MCP connection endpoint in the `url` field and the documenting page in
your cited evidence. A documentation URL submitted as the endpoint is rejected,
because each submitted `url` is assessed as the claim that that exact URL is the
product's MCP connection endpoint.

For `mcp_servers.url`, use the documented remote connection endpoint, for
example `https://mcp.example.ai/mcp`. Put its setup guide in `documentation_url`
and cite the evidence linking the server to the product and its functionality.
Authenticated endpoints qualify without an unauthenticated successful handshake.
A published endpoint must be concrete, safe to share, and free of credentials.

Accept a documentation-only MCP server entry when authoritative setup
instructions establish a remote MCP server for the cataloged product, but no
single publishable endpoint exists because users must supply their tenant
hostname or obtain a personal connection URL inside their account. Set `url` to
null and `documentation_url` to that setup guide. This preserves a verified path
to connect without publishing a placeholder, credentials, or a docs page as a
connection endpoint. Explain the account-specific setup in the submission
justification and retain evidence for the product relationship and
functionality. At least one pointer is required.

A generic MCP mention, client-only integration, server-building framework, or
unrelated server guide does not establish a remote server for this product.
Missing evidence or a failed probe alone does not justify replacing an endpoint
with documentation. If a supported public endpoint exists, include it. Local
stdio installs belong in `local_mcp_servers` with their package or repository
URL. Documentation-only presence means users can find setup instructions; it
does not promise an immediately dialable public endpoint.

## Agent skills, CLIs, and referral programs

These three affordances split on the citation bar, so draft them differently:

- **`agent_skills`** is a **world-claim** — the fact-check synthesizes *"the
  product supports the `<label>` agent skill"* and holds it to the citation bar.
  Like [taxonomy fields](taxonomy-evidence.md), it needs a corroborating page.
  In addition, an `agent_skills` `propose` entry additionally **requires a
  reachable `url`** pointing at the skill's doc/spec. `add`/`propose` one only
  when a vendor page documents the skill, and cite that page.
- **`command_line_interfaces`** is held to the citation bar like `mcp_servers`,
  **not** exempt like `api_specs`: only its `slug` is record structure, while
  the fact-check synthesizes the CLI's `name`/`url` as a claim the vendor's docs
  must support. Add a CLI when a vendor page documents one and cite that page,
  with a `url` that also resolves (the `urls` check covers reachability
  separately). The `url` must point at the page that specifically documents,
  installs, or distributes *that* CLI (its install guide, command reference, or
  release/changelog page), not a general developer portal that does not document
  that CLI specifically. Paddle's CLI update first closed on
  `developer.paddle.com/` (the general portal) and merged once it cited
  `developer.paddle.com/changelog/2026/paddle-cli` (the CLI-specific page).
- **`referral_programs`** is a reverse-FK `create` (`name`, `slug`, a reachable
  `program_url` / `affiliate_url`, and `status`: `active` / `pending` /
  `inactive`). Add one when the vendor documents a referral or affiliate
  program.

## Create MCP servers and SDKs

For MCP and SDK nested creates, inspect
`/api/v1/submissions/fields/?app_label=catalog&model=product&include_nested=true`.
Use only the child fields it advertises. MCP servers accept `name` and `url`;
developer kits also accept `programming_languages` and `licenses`. The server
binds `product` and assigns `id`. Neither child model accepts `slug`. Other
models, such as products and offers, do accept slugs; check each model
separately.

This product-update payload shows both nested-create shapes. Replace the example
URLs and names with documented facts, bind the existing product's `object_id`,
and supply evidence in the submission `description` before calling
`POST /api/v1/submissions/validate/`. Validation checks payload structure;
submission checks and review still require evidence for MCP endpoint identity
and each asserted SDK language or license.

```json
{
  "mcp_servers": {
    "create": [
      {
        "name": "Example MCP",
        "url": "https://mcp.example.ai/mcp"
      }
    ]
  },
  "developer_kits": {
    "create": [
      {
        "name": "Example Python SDK",
        "url": "https://github.com/example/sdk-python",
        "programming_languages": {
          "add": [
            "python"
          ]
        }
      }
    ]
  }
}
```

Resolve SDK languages from every page of
`/api/v1/catalog/programming-languages/?page_size=100` before using their slugs
or UUIDs. If a verified language is missing, report its canonical name, official
language URL, and SDK evidence to `support@openagentguide.com`. A maintainer can
submit the vocabulary entry for review. `programming_languages` accepts
`add`/`remove`, with no inline `propose`. While waiting, omit the unavailable
reference and explain the gap in the submission description; after it appears in
the catalog, update the existing kit with the verified language. Do not invent a
reference, choose a different language, or create a duplicate kit.

## Capture verified SDK languages

For each developer kit, check its official SDK documentation, package page, or
README for supported programming languages. Include verified languages in
`programming_languages: {"add": ["typescript"]}` using existing vocabulary
slugs. A name such as "Linear TypeScript SDK" is a cue to verify TypeScript and
populate the relation, not a substitute for it or evidence by itself. If the
kit's own documentation explicitly supports JavaScript too, include both. Do not
infer JavaScript from TypeScript, or a language from a runtime such as Node.js.

`licenses` and `programming_languages` remain optional when evidence is missing.
Do not omit an already verified language merely to minimize the payload. Cite
the exact kit's official documentation, README, or package page for languages;
use its license text for licenses. Product or sibling-kit facts do not establish
this kit's attributes. Presence is checked through URL reachability.

For a published kit missing languages, submit an `update` targeting
`catalog.developerkit` with its ID and `programming_languages: {"add": [...]}`.
Cite the evidence in the submission description and leave unchanged fields out.
Do not create a duplicate kit to fill its metadata.

## auth.md

Submit `auth_md_url` only after inspecting the product's own published auth.md
Markdown document at its official service root. API/auth subdomains and official
vendor-controlled service hosts can qualify; confirm product identity through
redirects. Generic authentication docs, HTML fallbacks and adopter badges do not
establish the document. WorkOS's [Adopted by badges](https://workos.com/auth-md)
are discovery leads only. Read documentation without executing registration.

The field is unscored and does not imply headless signup. Omit to preserve or
send `"auth_md_url": ""` to clear. Whole-field absence uses the normal
attestation metadata, for example `"field_key": "auth_md_url"`, with no label.
Cite complete official registration/authentication documentation that would
publish or link the file, or a scoped explicit vendor negative. A guessed 404 or
failed fetch alone is insufficient. Absence is recorded for completion only,
without score, research-coverage or field-density credit.
