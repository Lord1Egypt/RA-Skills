# Look Decision Policy

## Why these risk tiers

- **Low risk** (pricing comparisons, candidate lists) — user can delete or ignore these with no consequence. No confirmation needed.
- **Medium risk** (calendar creation, maps writes) — user may need to undo these. Reversible actions, confirmation recommended but not required.
- **High risk** (purchases, 311 submission, health writes, drive writes) — difficult or impossible to reverse. Explicit confirmation token required per draft.

The confirmation-token requirement exists because high-risk actions (like purchasing a product or filing a civic report) have real-world consequences the agent cannot undo. The token ensures the user intentionally selected this specific draft.

## No-Hallucination Policy

Why: Hallucinated OCR text would propagate into calendar events, expense entries, or civic reports — corrupting the user's records and potentially causing real harm (wrong event date, incorrect expense amount). When the agent fills gaps with guesses instead of flagging uncertainty, downstream actions compound the error.
Never invent: OCR text, barcodes, prices, ticket inventory, license plates. If uncertain, flag uncertainty in the draft.
