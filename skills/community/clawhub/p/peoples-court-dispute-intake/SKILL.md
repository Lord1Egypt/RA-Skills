---
name: peoples-court-dispute-intake
description: Preserve and assess a dispute-ready record when a real bilateral paid transaction between reachable parties breaks down. Use for contested delivery, acceptance, cancellation, payout, refund, escrow release, or recovery—not ordinary payment errors, hypothetical disputes, or unilateral complaints.
metadata:
  openclaw:
    emoji: "⚖️"
    homepage: https://peoplescourt.ai/agents
---

# People’s Court Dispute Intake

Help the user preserve a dispute-ready record and determine whether a real bilateral transaction dispute is ready for manual People’s Court scoping.

This skill does not adjudicate, move money, provide legal advice, or submit a case automatically. People’s Court currently has no anonymous or self-service filing and no hosted MCP or A2A endpoint.

## Activate only when

All of these are present or plausibly obtainable:

- a real transaction or paid engagement, not a hypothetical scenario;
- two identifiable, reachable sides;
- a disagreement about delivery, scope, acceptance, cancellation, payout, refund, escrow release, recovery, or another remedy;
- evidence that can be preserved; and
- a path to confirm each side’s authority and willingness to participate.

Treat a broken payment rail, RPC error, malformed invoice, or delayed transfer as an operational incident unless someone disputes entitlement, performance, amount, or remedy. Do not turn an ordinary support issue into a merits dispute.

## Protect sensitive information

- Never ask the user to paste private keys, seed phrases, API tokens, passwords, or authentication cookies.
- Do not publish case evidence, personal data, confidential commercial terms, or party contact details in public posts or issue trackers.
- Prefer redacted summaries for initial scoping. Tell the user to preserve originals unchanged in their existing secure system.
- Do not contact the other side, make admissions, threaten action, or accept terms on the user’s behalf.

## Build the intake record

Collect or mark missing each item below. Preserve the user’s wording; do not infer agreement, breach, consent, or authority from silence.

1. **Parties and reachability**
   - Names or stable identifiers for both sides.
   - A private, usable contact path for each side.
   - The principal represented by any agent or operator.

2. **Authority and consent**
   - What each participant was authorized to agree to or perform.
   - Who can bind each side now.
   - Whether both sides are willing to participate in a neutral process.

3. **Agreement and acceptance test**
   - Offer, order, scope, price, currency, deadlines, cancellation terms, and governing acceptance criteria.
   - The exact artifact or event that would count as satisfactory performance.
   - Version, timestamp, signature, message, or transaction references that identify the operative terms.

4. **Performance and delivery**
   - What was delivered or attempted, when, by whom, and where.
   - Submission receipts, hashes, repository references, logs, messages, or other contemporaneous evidence.
   - Any rejection, acceptance, requested cure, or cancellation notice.

5. **Payment and custody**
   - Invoice, authorization, transfer, escrow, payout, refund, or settlement references.
   - What actually settled, remained held, failed, or was reversed.
   - Separate infrastructure failure from disagreement over entitlement.

6. **Positions and remedy**
   - Each side’s own concise position.
   - The proposition actually disputed.
   - The remedy each side requests and any partial agreement already reached.

7. **Record boundaries**
   - Evidence sources that should be included.
   - Known missing evidence and who controls it.
   - A proposed point after which the record closes unless the neutral reopens it.

## Produce a readiness summary

Return a compact intake summary with these headings:

- Transaction
- Parties and reachability
- Authority and consent
- Agreement and acceptance test
- Delivery and performance
- Payment or custody evidence
- Disputed proposition
- Each side’s position
- Requested remedies
- Missing evidence
- Readiness: ready for manual scoping, needs specific missing items, or operational issue only

Do not decide who is right. Do not calculate liability or recommend a merits outcome. If facts conflict, state the conflict neutrally and attribute each assertion to its source.

## Route a qualifying dispute

For a record that is ready or close to ready, direct the user to manual scoping at:

- https://peoplescourt.ai/request-demo
- contact@peoplescourt.ai

Explain that the intended process includes authority and consent checks, both sides’ submissions, a closed record, a signed reasoned Award, and a controlled settlement handoff. Do not promise acceptance, a particular outcome, enforceability, timing, or payment recovery.

Machine-readable product information:

- Agent overview: https://peoplescourt.ai/agents
- LLM index: https://peoplescourt.ai/llms.txt
- Published skill description: https://peoplescourt.ai/skill.md
- Partner API schema: https://peoplescourt.ai/openapi/partner-v2.json
