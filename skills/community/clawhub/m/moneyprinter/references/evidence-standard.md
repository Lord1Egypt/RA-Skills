# Evidence standard

Every economic result uses exactly one label below. The label describes the
current evidence, not the hoped-for outcome. Artifact-backed labels require an
inspected source record; a narrative statement or explicit user attestation
alone is not a substitute. Keep original supporting records private and share
only privacy-safe redacted details when personal, confidential, or regulated
information is involved.

1. **Cash collected** — settled payment received, supported by a settlement
   artifact.
   - Valid: A redacted processor or bank settlement record shows $250 arrived;
     label the result **Cash collected**.
   - Invalid: An issued $250 invoice or user attestation without settlement
     evidence is labeled **Cash collected**.

2. **Revenue contracted** — signed obligation, not yet collected, supported by
   a signed-obligation artifact.
   - Valid: A redacted executed $1,000 service agreement records both parties'
     signatures and no payment has settled; label it **Revenue contracted**.
   - Invalid: Verbal interest or user attestation without a signed-obligation
     artifact is labeled **Revenue contracted**.

3. **Revenue booked** — invoice or order created, not yet settled.
   - Valid: An approved $300 order exists in the order system but no settlement
     has occurred; label it **Revenue booked**.
   - Invalid: A signed contract is labeled **Revenue booked** when no order or
     invoice was created.

4. **Pipeline signal** — reply, meeting, proposal, waitlist, or intent.
   - Valid: A qualified buyer accepted a discovery meeting; label it **Pipeline
     signal**.
   - Invalid: An unsolicited page view is labeled **Pipeline signal**.

5. **Estimated economic value** — modeled value with explicit assumptions.
   - Valid: A manual workflow saves 10 hours at $30/hour, assuming all saved
     time is redeployed; show sensitivity at 5 and 15 hours and label it
     **Estimated economic value**.
   - Invalid: "This automation saves $10,000" is labeled **Estimated economic
     value** without a formula, assumptions, or sensitivity.

6. **Simulation** — benchmark or hypothetical result.
   - Valid: A test harness predicts a 12% conversion lift; present **Simulation**
     beside the number.
   - Invalid: A benchmark result is called **Cash collected**.

7. **Unverified anecdote** — reported but not supported by the artifact required
   for a stronger label.
   - Valid: A user reports a payment, contract, or sale without the appropriate
     supporting artifact; label it **Unverified anecdote**.
   - Invalid: A reported result without supporting records is labeled **Revenue
     contracted**.

For a public field report, include the time window, starting assets, cash spend,
model and harness, human work, method, result label, and redacted evidence where
safe. Never infer settlement, a contract, or a buyer's intent from a benchmark,
dashboard estimate, invoice draft, page view, anecdote, or attestation. If
settlement evidence or a signed-obligation artifact is unavailable, use
**Unverified anecdote**, not **Cash collected** or **Revenue contracted**.
