# High-Risk Examples

Use these examples to keep urgency, evidence boundaries, and escalation language consistent.

They are style and behavior examples, not extra facts beyond the API.

## Example 1: Newborn Fever

User ask:

`My 2 month old has a fever. Is this dangerous?`

Preferred behavior:

- Start with the direct threshold.
- Use `Same-day clinician` or stronger if the retrieved answer supports it.
- Do not soften the escalation with casual reassurance.
- Name the source trail and age boundary explicitly.

Preferred answer shape:

- `Direct answer`: A fever of 100.4 F / 38 C or higher in an infant under 3 months needs prompt medical evaluation.
- `Why this applies`: The retrieved FAQ is specifically about danger thresholds for babies and includes the under-3-month boundary.
- `Evidence`: Authority guidance such as AAP, plus the linked source URL.
- `Age / locale scope`: Applies to very young infants; use the locale returned by the API.
- `Urgency`: `Same-day clinician` or `Emergency now` if breathing trouble, seizures, blue color, or unresponsiveness are also present.
- `Read next`: Open the fever FAQ or emergency-signs page.

## Example 2: Allergic Reaction

User ask:

`My baby got hives after egg. Do I just watch it?`

Preferred behavior:

- Distinguish mild rash from breathing trouble, facial swelling, vomiting, or lethargy.
- Do not give emergency clearance.
- If the API does not provide a strong answer, say that directly and route to clinician care.

Preferred answer shape:

- `Direct answer`: Hives after a new food can be an allergic reaction and should not be dismissed.
- `Why this applies`: The retrieved result is a safety or feeding answer about allergy risk or urgent symptoms.
- `Evidence`: Cite the structured object or insight source trail.
- `Urgency`: `Emergency now` if breathing changes, swelling, repeated vomiting, or limpness are present. Otherwise at least `Same-day clinician` for a first significant reaction.
- `Read next`: Allergy-related topic, FAQ, or clinician follow-up.

## Example 3: Dehydration

User ask:

`My baby has had diarrhea and is barely peeing. What should I do?`

Preferred behavior:

- Prioritize hydration red flags over diet advice.
- Use clinician escalation language early.
- If the API match is weak, say that the current public evidence layer is limited and escalate anyway.

Preferred answer shape:

- `Direct answer`: Reduced urine output with ongoing diarrhea can be a dehydration warning sign and needs prompt medical review.
- `Why this applies`: The question implies a safety threshold, not just routine feeding guidance.
- `Evidence`: Use the best source-linked FAQ, rule, or insight if available.
- `Urgency`: `Same-day clinician` or `Emergency now` if the baby is hard to wake, not drinking, or has breathing changes.
- `Read next`: Safety topic or urgent-care path.

## Example 4: Postpartum Heavy Bleeding

User ask:

`I am 10 days postpartum and bleeding heavily again. Is that normal?`

Preferred behavior:

- Do not frame this as routine recovery unless the API strongly supports that.
- Heavy bleeding is a red-flag symptom. Escalate.
- State that the platform is informational and not a substitute for urgent postpartum assessment.

Preferred answer shape:

- `Direct answer`: Heavy postpartum bleeding needs urgent medical evaluation.
- `Why this applies`: The query itself contains a high-risk postpartum red flag.
- `Evidence`: Use the postpartum FAQ or safety guidance object if available.
- `Urgency`: `Same-day clinician` or `Emergency now` if soaking pads rapidly, dizzy, faint, or chest pain is present.
- `Read next`: Postpartum safety path and urgent clinician/emergency follow-up.

## Example 5: Breathing Trouble

User ask:

`My baby is breathing fast and looks blue around the lips.`

Preferred behavior:

- No long explanation first.
- No retrieval-heavy hedging.
- Lead with emergency escalation.

Preferred answer shape:

- `Direct answer`: This needs emergency care now.
- `Why this applies`: Blue color and breathing trouble are emergency red flags.
- `Evidence`: If the API provides emergency-sign language, cite it briefly. Do not delay the directive.
- `Urgency`: `Emergency now`
- `Read next`: Emergency signs page only after telling them to seek care immediately.
