# US Property Tax Appeal Routes

## Purpose

Use this reference after identifying the subject state and local assessing authority. It covers valuation appeals for owner-occupied or residential real property. Classification, exemption, special-assessment, omitted-property, agricultural-use, and tax-bill collection disputes may use different forms and standards.

The names below are route families, not substitutes for current local instructions. Run `scripts/lookup_jurisdiction.py --state <code>` and then verify the exact route, deadline, valuation date, evidence window, form revision, filing fee, signature requirement, and submission method on official sources.

## Route Decision

1. Read the assessment notice and identify what decision is being challenged.
2. Reconcile every notice value label as a sourced node. Explicitly designate the sales-comparable market value and preserve each ratio, cap, equalization, classification, exemption, and authority-specific taxable-value transformation.
3. Determine whether an informal assessor review is available and whether using it preserves the formal filing deadline.
4. Identify the first formal body and exact form. Common bodies include a board of review, board of equalization, assessment appeals board, board of revision, value adjustment board, appraisal review board, county tax board, or state assessment appeal board.
5. Identify the controlling valuation date and the legally or administratively accepted sale window. Never import California's January 1 or 90-day rule into another jurisdiction.
6. Determine whether the argument is market value, unequal/non-uniform appraisal, classification, exemption, factual correction, or another issue. Use this skill's comparable-sale workflow only when market value is material. For every other ground, stop packet generation after identifying the verified authority, form, and deadline; do not substitute neighboring assessments for sales.
7. Calendar every formal deadline even when pursuing an informal review. State in the work record whether the informal request tolls or preserves that deadline.

## Main Route Families

### `assessor_then_local_board`

Typical sequence: optional or required assessor conference, then a local board, followed by a state tribunal or court. This is the most common general pattern.

Prepare an informal-review attachment for the assessor or a formal evidence statement for the board. For a formal filing, the attachment supplements rather than replaces the official petition.

### `local_equalization_board`

Typical sequence: assessor contact, county or local board of equalization, then a state board, tax tribunal, or court. Verify whether the initial assessor conference is mandatory and whether the board filing is based on a fixed calendar date or days after notice.

### `abatement`

Common in Maine, Massachusetts, and New Hampshire. The owner applies to the assessors or municipality for an abatement, then may appeal to a tax board, commissioners, or court. Use the jurisdiction's term `abatement` throughout the cover narrative and official form.

### `grievance`

Common in New York and Vermont. The owner files a grievance or appears before a local review body. Verify tentative-roll dates, grievance-day rules, required complaint forms, and later small-claims or court options.

### `appraisal_review_board`

Texas uses a notice of protest to the local appraisal review board. Verify the current Comptroller form, appraisal-district filing portal, protest reasons, hearing election, evidence-exchange rules, and the owner's available post-ARB remedies. Do not treat a capped homestead appraised value as the sales-comparison market value merely because both appear on the notice. Equal-and-uniform protests use a separate median-level evidence model and are outside this packet builder.

### `value_adjustment_board`

Florida uses a petition to the county value adjustment board. Verify the current Department of Revenue petition form, county clerk portal, filing fee, good-cause rules, evidence exchange, and whether the owner also requested an informal conference with the property appraiser. Preserve separate just, assessed, and taxing-authority taxable values instead of collapsing them into one notice amount.

### `board_of_revision`

Ohio generally uses a complaint to the county board of revision. Verify the current complaint form, filing window, countercomplaint rules, and appeal route.

### `county_tax_board`

New Jersey generally routes assessment petitions to the county board of taxation, with Tax Court review available under current law and procedure. Verify the applicable county board form, filing threshold rules, filing fee, service requirements, and whether a direct Tax Court route applies.

### `bopta`

Oregon uses the county Board of Property Tax Appeals. Verify the current petition type, filing date, evidence requirements, and Magistrate Division route.

### `state_assessment_ladder`

Maryland uses an assessment appeal sequence administered through the State Department of Assessments and Taxation before later review bodies. Follow the current notice instructions and identify the exact appeal level being requested.

## Document Modes

Set `case.document_mode` to one of:

- `informal_review_attachment`: concise evidence packet for an assessor conference or online review.
- `formal_board_evidence`: attachment to a board petition, complaint, or hearing submission.
- `protest_statement`: support for an appraisal review board or similar protest.
- `grievance_support`: support for a grievance application.
- `abatement_support`: support for an abatement application.
- `tribunal_exhibit`: organized evidence statement for later administrative or judicial review; recommend professional advice when procedure is complex.

The generated document must name the route actually used. Do not label every case an `appeal`, `Proposition 8`, or `informal review` when the official jurisdiction uses another term.

## Official Forms

- Download forms only from the current official state, county, municipal, appraisal-district, clerk, or tribunal source.
- Record the form title, revision date when shown, URL, access date, filing authority, and deadline in the case JSON.
- Treat the Markdown/PDF generated by this skill as a supporting attachment unless the official authority expressly accepts a narrative in place of its form.
- Do not invent form fields, owner signatures, representative authority, service certifications, or hearing elections.
- If the user asks to fill an official PDF, inspect whether it is an AcroForm, preserve interactivity by default, populate only verified fields, and visually and logically validate the result.
- If a form requires a filing fee, notarization, original signature, copies, service on another party, or a separate authorization, call that out before delivery.

## Deadline and Payment Guardrails

- Never state a deadline from memory. Cite the current official rule or the owner's notice.
- Distinguish a calendar deadline from a deadline measured in days after notice, mailing, publication, or roll completion.
- Do not assume an informal review extends a formal deadline.
- Tell the owner that an appeal ordinarily does not suspend tax-payment obligations unless the official authority says otherwise.
- If the formal deadline is close or unclear, prioritize preserving the formal filing while continuing evidence research.

## Nationwide Research Queries

Start with the router's official URL and search query, then narrow to the exact locality. Useful query patterns include:

```text
site:<official-domain> <county-or-city> property assessment appeal form
site:<official-domain> <county-or-city> board of review deadline residential
site:<official-domain> <county-or-city> valuation date comparable sales appeal
site:<official-domain> <form-name-or-number> PDF
```

Prefer the notice, official assessor, official appeals body, official tax authority, recorder, and official form instructions over summaries from law firms, real-estate portals, or search snippets.
