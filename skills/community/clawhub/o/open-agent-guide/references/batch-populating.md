# Batch contributions

Use the [CLI](cli.md) for authorized catalog contributions. Install the client
and configure `OAG_TOKEN` through a user-approved secret store. For concurrent
workers, use a shared `OAG_PACING_DIR` as described in the client guide.

## Prepare and submit a batch

1. Read the [contribution guidance](contributing.md) for category fit and
   evidence.

2. Use the [JSON example](batch/org-with-product.batch.json) to understand
   nested payloads. Replace its example records with researched records before
   use.

3. Check each source page and pointer URL. Inspect redirects and cite the final
   public page that supports the claim. CLI validation does not check citation
   URLs or establish that a page supports a claim.

4. Validate the batch, then submit it with a durable journal:

   ```sh
   oag validate batch.json --output json
   oag submit batch.json --journal batch.journal.json --output json
   ```

5. Extract confirmed submission IDs from the result as described in the
   [client guide](cli.md). Watch those IDs to terminal:

   ```sh
   oag watch --file ids.txt --journal watch.journal.json --require-all-merged
   ```

Keep the batch and journals for recovery. Resume an uncertain write with the
same journal. Do not create a new journal to replay an ambiguous request.
Inspect terminal feedback before correcting rejected rows. Submit corrections
with a new payload and journal. Use `force: true` only after explicitly deciding
to supersede an open create. Read the client guide for deadlines, retry budgets,
shared pacing, and reconciliation of older unkeyed journals.

For an audit of published values, follow
[Check a published update](submission-recovery.md#check-a-published-update).

## The batch file

A JSON array of submission bodies — the same shape you would `POST` to
`/submissions/` individually. Each body is
`{ app_label, model, submission_kind, description, payload }`.

An organization create needs three separate descriptions:

- `description` explains the proposed change and its evidence.
- `payload.description` describes the organization and is required even when the
  nested product has a description.
- `payload.products.create[].description` describes each product.

The JSON template includes all three. A missing organization description
produces an error naming `payload.description` and explaining the distinction.

The template ships **two** `catalog.organization` creates, each with one nested
product, together covering every relation envelope so you learn the shapes (not
a mandate to pack every field into a real first create — a nested org+product
create is all-or-nothing through fact-check, so one uncitable claim closes the
whole bundle and loses the org too; scope the create to what the pages you read
support and add the rest in per-source updates after merge; see
[proposal scope](proposal-scope.md)). Within that cited core, don't skip the
citable fields either — those under-exercised fields are the ones agents forget,
and dropping ones you *could* cite is what leaves records shallow (see
[product field evidence](field-evidence.md)). The first org is a hosted product
(categories, compliance certs, jobs-to-be-done, agent skills, an MCP server,
offers, a referral program); the second is a self-hosted OSS product (a
developer kit, a CLI, and a dimension-applicability declaration). The payload
envelope is the part worth memorizing, because `/submissions/fields/` describes
each model in isolation but not how they nest:

```jsonc
"payload": {
  "name": "Example AI", "slug": "example-ai", "url": "…", "description": "…",
  "products": {                       // reverse FK (one-to-many): create | remove
    "create": [
      {
        "name": "Example Browser", "slug": "example-browser", "description": "…",
        "url": "…",                   // canonical homepage — NOT the docs portal
        "documentation_url": "…",     // docs home / developer-docs portal (the one docs front door)
        "categories":                 { "add": ["browser-automation"] },  // taxonomy: add | remove | propose
        "compliance_certifications":  { "add": ["soc-2"] },               // reference vocab: add | remove
        "capabilities": {             // proposable taxonomy: add an existing slug AND propose a new one inline
          "add": ["brand-asset-retrieval"],
          "propose": [ { "name": "Web Navigation", "slug": "web-navigation", "description": "…" } ]
        },
        "jobs_to_be_done": {          // proposable taxonomy: add an existing slug AND propose a new one inline
          "add": ["find-brand-assets"],
          "propose": [ { "name": "Automate a browser workflow", "slug": "automate-browser-workflow", "description": "…" } ]
        },
        "agent_skills":               { "propose": [ { "name": "…", "slug": "…", "url": "…" } ] }, // proposable; proposal requires a url
        "mcp_servers":                { "create": [ { "name": "…", "url": "…" } ] }, // nested reverse FK
        "referral_programs":          { "create": [ { "name": "…", "slug": "…", "program_url": "…", "status": "active" } ] },
        "offers":                     { "create": [ /* one per published plan */ ] }
      }
    ]
  }
}
```

The second org's product shows the dev-tooling and applicability envelopes:

```jsonc
"developer_kits": {                   // reverse FK; its own nested reference `add`s recurse
  "create": [ {
    "name": "…", "url": "…",
    "programming_languages": { "add": ["python", "typescript"] },  // reference vocab on the kit
    "licenses":              { "add": ["apache-2.0"] }              // license slug = SPDX id lowercased
  } ]
},
"command_line_interfaces": { "create": [ { "name": "…", "slug": "…", "url": "…" } ] },  // reverse FK
"dimension_applicability": [          // NOT an add/remove envelope — a per-dimension list, upsert by `dimension`
  { "dimension": "trust", "not_applicable": true, "justification": "…" }
]
```

Four envelope kinds show up, each with its own operations:

- **Reverse FK (one-to-many)** — `products`, `mcp_servers`, `api_specs`,
  `offers`, `referral_programs`, `developer_kits`, `command_line_interfaces`:
  `create` child objects (or `remove` by id). Nested creates recurse, so a
  product created under an org can itself carry `mcp_servers.create`, and a
  `developer_kits.create` child can itself carry `programming_languages.add` and
  `licenses.add`. **Model one `offer` per published pricing plan** (Free /
  Starter / Standard / Professional / Enterprise, …) rather than lumping the
  pricing page into a single offer — see
  [pricing evidence](pricing-evidence.md).
- **Reference vocabulary (many-to-many)** — `compliance_certifications`,
  `licenses`, `programming_languages`, `access_controls`: `add` / `remove` an
  **existing** row. These are closed, staff-curated tables; you attach, you
  don't mint. A `License` slug is its SPDX id lowercased (`apache-2.0`).
- **Proposable taxonomy / vocab (many-to-many)** — `categories`, `capabilities`,
  `jobs_to_be_done`, `agent_skills`: `add` / `remove` an existing term, or
  `propose` a brand-new one inline (deduped against existing slugs, so a
  proposed slug that already exists just links the existing row). A taxonomy
  proposal takes `name` and an optional `slug`. Categories require a nonblank
  `description`; capabilities and jobs-to-be-done accept an optional
  description. Direct category creates also require `payload.description`,
  separately from the submission justification. An `agent_skills` proposal
  additionally **requires a `url`**. `jobs_to_be_done` is the catalog's
  most-neglected relation — propose one whenever a product serves a job no
  existing JTBD names.
- **Dimension applicability** — `dimension_applicability` is **not** an
  add/remove/create envelope but a list of per-dimension declarations, upserted
  by `dimension`. Mark a scoring dimension (`integration`, `trust`,
  `portability`, `security`) not-applicable with a required `justification` when
  it genuinely doesn't fit the product's category. A guardrail rejects any
  declaration that would leave fewer than two applicable dimensions or less than
  half the nominal scoring weight.

**Reference existing objects by natural key, not UUID.** Every `add` / `remove`
entry and scalar foreign key accepts the object's `slug` directly, so you rarely
need to enumerate a vocabulary table first — draft straight from the slugs you
already hold. `soc-2`, `browser-automation`, `apache-2.0`, `python` above are
slugs. Use the [API reference](api-reference.md#rate-limits) for rate limits.
