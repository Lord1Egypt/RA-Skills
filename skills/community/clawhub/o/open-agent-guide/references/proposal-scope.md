# Proposal scope and claim grouping

Read this when dividing a create or update into independently verifiable
proposals.

## Keep narrow updates focused

For a repair or a single-topic update, read the current record and submit only
fields needed for that change. Omit unchanged product descriptions and unrelated
SDK, capability, license, or pricing claims. Omission preserves stored fields;
it does not retract them. If an unchanged field must remain in the payload,
explicitly cite every affirmative claim it contains, including qualifiers. A
claim already stored in the catalog still needs evidence when resubmitted. Keep
dependent values and qualifiers together, and follow the replacement rules for
collections such as `prices`.

For example, a trust-only update can target the existing Product ID and supply
`trust_center_url` with a citation to the official trust page establishing its
applicability to that product. Omit the unchanged Product `description` and SDK
claims. If also adding a certification, cite its coverage and retain any plan or
deployment restriction; a trust-center link alone does not prove every cert.

The [field evidence workflow](field-evidence.md) still calls for researching all
decision fields. Reach that coverage through focused submissions without
repeating unrelated claims in each repair. Every submitted claim still passes
the same checks.

## Establish category fit and preserve evidence

Before research, state the actor, task and usable product boundary that make the
entry fit the intended category. For personal-assistant shopping, an assistant
must be able to use the product to shop directly. A merchant platform or SDK for
building shopping applications does not qualify on commerce support alone.

Before submission, map each field to its product/component scope, source,
authoritative page class and supported, attested-absent or unknown disposition.
Read validation guidance for the required page class. Keep unknown fields
omitted. Fetch the sources; a URL alone does not establish support. During
repairs, preserve every retained claim's citations, including publisher
attribution, and flag disappearing evidence. Put justification in the
submission-level description; public catalog copy describes the product.

When disputed independent enrichment blocks a new record, publish a supported
base first. Resolve and reuse its publisher, retain identity citations, wait for
merge and read back the product identity. Submit independent claim groups as
updates to that identity. Keep dependent values, qualifiers, contradictions,
absence attestations and associations together. Do not split to evade rejection
or create duplicate publishers. Revalidate every group.

## Keep cited pages within the size budget, and shell-first for new records

Cite at most five distinct pages of claim evidence in one submission: the
pricing, trust, offer, and absence-source pages, plus any page you cite in the
free-text note to back a claim. The fact-check verifies each world-claim against
the evidence page behind it, so a submission citing more evidence than that is
rejected at `validate/` and create before any verification runs. Typed pointers
— the entity `url`, `documentation_url`, `source_code_url`, `llms_txt_url`, API
specs, SDKs, CLIs, MCP servers, and agent-skill URLs — do not count toward the
limit; they are verified by the `urls` and `pointer_content` checks, so a rich
create carrying many pointers is fine. The count collapses fragment-only
variants and exact duplicates of a page. Split a change needing more evidence
into smaller submissions grouped by topic and source, and check the evidence
count with `validate/` before you submit.

Separately, before any model runs, a resource-size gate fetches the admitted
pages and rejects the submission when that evidence is too large to fact-check
and review within budget. The rejection reports the token count of each page it
fetched, so you can see which one is too large. Because the repair pushes you
toward fewer, more specific citations, drafting a claim from memory and leaning
on one broad page to carry it is doubly unsafe (see
[source evidence](source-evidence.md)).

For a new product or organization, submit a minimal cited core first: name,
category, description, and `url`. Let it merge, then add capabilities, pricing,
documentation, and other affordances in follow-up `update` submissions. A create
that bundles several large pages is the shape that trips the gate.

**A nested org+product create is all-or-nothing through fact-check.** The
organization, its nested product, and every claim in the bundle rise or fall
together: one unsupported claim closes the *whole* submission, so you lose the
org and the product too, not just the weak field. This is the size gate's repair
guidance applied **proactively** — don't wait for a reject to learn it. Scope
the first create to the claims a small set of pages you actually read support,
then add the rest in focused per-source `update` submissions after merge (see
[claim grouping](#group-claims-by-source-and-dependency)). In the 2026-10-28
populator run, atomic nested creates for FAL, Cartesia, and LanceDB each closed
whole on a single failed claim, while the depth arms' per-source updates merged
partially — ntfy and airbyte landed real coverage even though several of their
updates closed, because an update that fails takes one focused claim group down
with it instead of the whole entity.

A lean core is **not** a thin record (see
[product field evidence](field-evidence.md)): the depth target is the same,
reached across submissions. "Lean" means *only what you can cite* — which can be
anything from a bare name/category/description/`url` shell up to a citable-rich
create. The one breadth create in that run that merged with real depth (Vespa,
coverage 19) was lean in that richer sense: it carried only the open-source,
self-hosting, open-standards, and CLI fields it could cite from the pages it
read, and deferred the rest to updates. What sinks a create is a claim you
*could not* cite riding along with the ones you could, not the number of fields.

For any shape, cite a specific page for each claim rather than one broad landing
or pricing page, and split a wide update into smaller submissions grouped by
topic and source. Citing a narrower page that still supports the claim is the
fix; dropping evidence or truncating a page is not.

Before submitting, call `POST /api/v1/submissions/validate/` and inspect
`mcp_endpoint_guidance`. Each entry identifies a submitted URL by payload path;
`hint` flags likely documentation URLs using their hostname or path. A hint is
advisory, and a null hint does not verify the endpoint. Confirm the connection
address in authoritative documentation and retain evidence linking that exact
address to the product and its functionality.

For product enrichment, also inspect `product_update_preview` in the validation
response. `current` and `projected` show coverage, score components and display
tier. `newly_known_fields` identifies coverage gains;
`refreshed_evidence_fields` identifies repeated absence evidence, and
`unchanged_fields` lists submitted decision values that stay the same. A useful
evidence refresh can have zero coverage and score delta. Creates and non-product
targets return `unsupported`. Non-empty trust-center URL updates return
`partial`, with `pending_fields` identifying `trust_center_url`. `projected` and
its deltas assume no pointer verification credit; `projected_if_verified` shows
coverage, score and display tier if the pointer is corroborated. Field-change
lists exclude the pending pointer. Clearing the URL supports a complete preview.
Partial and unsupported previews include a reason. Every projection assumes
accepted claims and provides no citation approval or guarantee against
concurrent catalog changes.

## Group a broad update

For broad updates, start with at most four material claims per submission,
grouped by topic and source, such as licensing and hosting, or retention and
interface absences. Count each association label, confirmed absence, and prose
assertion separately. Keep values with citations, qualifiers, required absence
attestations, and dependent or contradictory claims. Create the minimum valid
new product first, then update it after merge. Revalidate every group.
`review_budget_guidance` in a successful validation response explains this
starting point. Shape validation cannot predict future model-generated evidence;
even one claim can exceed the hard review cap. If review rejects a group for its
evidence size, separate any independent claim groups without dropping
substantive evidence. Keep an indivisible Offer complete even when it exceeds
the cap.

### Group claims by source and dependency

Group by independent verifiability as well as size. Verification is
all-or-nothing: one unsupported claim can prevent the entire proposal from
publishing. Separate proposals help only when each claim group can be assessed
without the other group's values or evidence. Sharing a source URL alone does
not make claims dependent, and separate URLs do not prove independence. Each
proposal still needs factual corroboration and curator approval.

Keep dependent values, qualifiers, contradictions, absence attestations, and
associations together when they are needed to interpret a claim. Preserve each
complete Offer's prices, units, billing cadence, restrictions, qualifiers, and
citations together, including all required `prices`. Never split an indivisible
Offer or remove a restriction to fit a review budget. A scalar and its scope
condition, an absence and its attestation, or a claim and contradictory evidence
each require joint review.

Before drafting an absence claim, inspect the live field-specific evidence and
page-class guidance. Check `absence_attestation_guidance`, including
`expected_page_class` and `hint`, from validation and read the actual source.
Structural validation checks payload shape; it does not fetch sources or
establish factual corroboration. A missing hint does not establish absence. Omit
unresolved absence claims from the proposal and research them separately. Only
submit a later absence proposal once its evidence supports it and its claims are
genuinely independent of the earlier proposal.

Never split to evade a substantive rejection. Repair the rejected claim's
evidence or leave it unsubmitted. Preserve every retained claim's citations,
scope, qualifiers, contradictions, and required dependencies, then revalidate
each proposal against the current catalog. Splitting changes no evidence gate
and provides no partial acceptance within a proposal.

### Worked example: pricing and an unresolved hosting absence

Suppose an update for an existing search API combines a credit-top-up Offer, a
pricing pointer, a budget-cap claim, a capability association, and
`self_hostable=false`. The draft cites a pricing page that says "Our
infrastructure" and says nothing about self-hosting. Structural validation
passes. That result establishes neither the hosting absence nor the pricing
claims. Pricing-page silence and that phrase do not establish that self-hosting
is unavailable.

1. Read the pricing evidence and prepare the complete Offer with its prices,
   units, billing cadence, restrictions, qualifiers, and citations. Keep any
   budget cap or capability restriction needed to interpret that Offer with it.
   Include a pricing pointer or a separate capability association only with
   evidence supporting its own scope. Omit unsupported additions.
2. If those pricing claims stand independently of hosting availability, submit
   the pricing proposal without `self_hostable=false` or its unresolved absence
   attestation. Validate it, then wait for factual verification and curator
   review. The original validation result does not predict its approval.
3. Research self-hosting separately using the live field-specific page-class
   guidance. Leave the absence unsubmitted while evidence is unresolved. If
   adequate evidence later establishes the absence, submit a separate update
   containing `self_hostable=false`, its required attestation, citations, and
   any relevant qualifiers or contradictory evidence.
4. If deployment availability determines the price, plan eligibility, or
   capability scope, keep those claims together and resolve the evidence gap
   before submission. Splitting would remove information needed to assess them.
