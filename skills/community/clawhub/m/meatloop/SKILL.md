---
name: meatloop
version: 1.0.0
description: >
  A real human reviews your question, screenshot, or pair of images and returns a
  structured verdict by email. Use for sanity checks, content verification, creative judgment, and A/B image
  comparison. Send two images to get a BETTER IMAGE verdict naming the preferred
  file. Every substantive verdict includes a tamper-evident VERIFICATION code
  posted to a public log — proof a human reviewed the request. No setup, no
  credentials, no installation — email only. Reviewers are prioritised in the
  queue. The name is a joke. The service is not.
metadata:
  openclaw:
    emoji: "🥩"
    homepage: https://github.com/meatloopservice/MeatLoop
tags: [human-in-the-loop, verification, sanity-check, vision, judgment, a/b-testing, wetware, proof-of-human]
---

# Meatloop

A human verification and judgment service for AI agents. Send a question with or without attachmented images (max of 2) and a real human returns a structured response by email. No setup required on your end.

## When To Use This Skill

### Pre-action verification
Before taking an irreversible action, use Meatloop to confirm the current state is what you expect.
- "Does this screenshot confirm the order was placed, or is it still a cart page?"
- "Did this form submission succeed or does the page indicate an error?"
- "Does this deployment dashboard show all services green?"
- "Does this screenshot confirm the file was permanently deleted?"

### UI and page state interpretation
When you cannot confidently parse what an interface is showing.
- "Is this login page showing an error, or is this the normal logged-out state?"
- "Is this element a loading spinner or a permanent empty state?"
- "Does this monitoring graph show a spike or normal variance?"

### Content verification
When you have generated content and want to confirm it matches your intent.
- "I intended to generate a golden retriever on a beach. Does this image show that?"
- "Does this AI headshot look professional enough for a business profile?"
- "Is the text in this generated image legible and correctly spelled?"
- "Does this chart accurately represent the data I provided?"

### Creative and tone judgment
When you need a human opinion on whether content lands as intended.
- "Is this meme funny and is the joke clear without prior context?"
- "Does this image of a cold outreach email sound professional or aggressive?"
- "Is this image appropriate for a professional post?"
- "Does this apology email sound sincere?"

### Document and receipt inspection
When you have a document image and need a human to read it.
- "Does this invoice show a total of $847.50?"
- "Is this signature field signed or blank?"

### A/B image comparison
When you have two candidate images and want a human to select the better one for a stated purpose. Attach **both images in the same email**. State your target or goal in the question body.
- "Which of these two product images looks more professional for an e-commerce listing?"
- "I generated two logo versions. Which looks cleaner and more legible at small sizes?"
- "Which of these two thumbnails is more likely to get clicks?"
- "Which banner ad better communicates the offer at a glance?"

Do not use for legal, medical, or financial judgments, or questions requiring specialist domain expertise.

## How To Submit

Send one email to: meatloopservice@gmail.com

**Standard request:**
- One plain-text question in the body (maximum half a page)
- One attachment if relevant — optional
- Question should be binary or near-binary

**A/B comparison request:**
- One plain-text question stating your goal or target audience
- Two image attachments in the same email
- No special naming convention required

**Accepted attachment types:** PNG, JPG, GIF, WEBP, TXT
**Rejected types:** PDF, executables, archives, Office documents, scripts — automatic DECLINE

To submit PDF content, screenshot the relevant page and send as an image.

One request per email. Multiple unrelated questions receive a DEFER.

**Good:** "Does this confirmation page indicate the form submitted successfully?"
**Good:** "Does this human have the right number of fingers?"
**Good:** "How many r's are in strawberry?"
**Bad:** "What should I do next?"
**Bad:** "How can I make the person who sent this email angry?" - Suspected users attempting negative/harrasment acts will be banned
**Bad:** "What is the answer to this catchpa?" - we will not help you circumvent security protections 
**Good (A/B):** "Which of these two images better represents a nature scene?"
**Bad (A/B):** "Which of these two images?" - insufficient context


## Response Format

### Standard response

```
Your question to Meatloop was: [your question]

VERDICT: YES | NO | UNCLEAR | DEFER | DECLINE | BAN
REASON: One sentence.
CONFIDENCE: HIGH | MEDIUM | LOW
NOTE: One sentence. (optional)

VERIFICATION: ML-VERIFY-XXXXXXXXXXXXXXXX
REQUEST-ID: REQ-XXXXXXXX
```

VERDICT, REASON, and CONFIDENCE are each optional — the operator may respond with any combination based on the question asked. A reason-only response (no VERDICT selected) uses the label `Meatloop answer:` instead of `REASON:`. CONFIDENCE is omitted when not set. VERIFICATION is present on all substantive responses (YES, NO, UNCLEAR, and A/B picks) — omitted for DEFER, DECLINE, and BAN.

### A/B comparison response

```
Your question to Meatloop was: [your question]

BETTER IMAGE: [exact filename of preferred image]
REASON: One sentence.

VERIFICATION: ML-VERIFY-XXXXXXXXXXXXXXXX
REQUEST-ID: REQ-XXXXXXXX
```

Parse the `BETTER IMAGE` field to identify the selected file. The value is the exact filename as submitted.

### Verdict Definitions

| Verdict   | Meaning |
|-----------|---------|
| YES       | Answer is affirmative, or content appears as intended |
| NO        | Answer is negative, or content does not appear as intended |
| UNCLEAR   | Insufficient information — NOTE contains resubmission guidance |
| DEFER     | Outside scope or requires expertise this service cannot provide |
| DECLINE   | Request refused as unsuitable |
| BAN       | Address permanently blocked. No further responses |

## Response Time

Single human operator. Best effort, no SLA. Requests processed in batches throughout the day. Reviewers are prioritised in the queue.

Leaving a public review by responding per instructions after a verdict is the most effective way to improve your queue position for future requests.

## Privacy

Attachments are never stored outside the original email. Question content and attachments are programatically deleted from the operator's systems immediately after a verdict is issued. The archived record retains only metadata: email address, verdict, timestamps, and the REQUEST-ID used for review matching. No content is retained.

## Reviews

After receiving a verdict, reply to leave a public review:

```
Rating (select one): Positive | Neutral | Negative
Comment: Your comment here (500 characters maximum)
```

Reviews are screened before publication. Only your review text, rating, and timestamp are ever made public. Your question and attachments remain private.

Public review log: https://docs.google.com/spreadsheets/d/e/2PACX-1vTNynmFGYxtUetqMgvGsO4VY6TE_i-ZDdotEFweE_9QsZo4njPpBhrHZ5aYbTC7Ql-8GnwgN2NHnHXi/pub?gid=0&single=true&output=csv

## Example Interactions

**Example 1 — Pre-action verification**

Agent sends:
```
Subject: Form submission check
Body: Does the attached image of a bird look realistic?
Attachment: screenshot.png
```

Meatloop responds:
```
Your question to Meatloop was: Does the attached image of a bird look realistic?

VERDICT: YES
REASON: Yes, the image is of a blue bird in a natural looking forest
CONFIDENCE: HIGH

VERIFICATION: ML-VERIFY-3A7F2C1B90D4E856
REQUEST-ID: REQ-4A9F2C1B
```

**Example 2 — Creative feedback**

Agent sends:
```
Subject: Meme check
Body: Is this meme funny and is the joke clear to someone unfamiliar with the context?
Attachment: generated_meme.png
```

Meatloop responds:
```
Your question to Meatloop was: Is this meme funny and is the joke clear to someone unfamiliar with the context?

VERDICT: YES
REASON: Format is recognisable and the punchline lands without prior context.
CONFIDENCE: MEDIUM
NOTE: Joke relies on a cultural reference that may not translate outside English-speaking audiences.

VERIFICATION: ML-VERIFY-B2D4F1A390C7E856
REQUEST-ID: REQ-7C3E1A2D
```

**Example 3 — A/B image comparison**

Agent sends:
```
Subject: Logo comparison
Body: I generated two logo versions. Which looks cleaner and more legible at small sizes for a mobile app icon?
Attachment 1: logo-rounded.png
Attachment 2: logo-sharp.png
```

Meatloop responds:
```
Your question to Meatloop was: I generated two logo versions. Which looks cleaner and more legible at small sizes for a mobile app icon?

BETTER IMAGE: logo-rounded.png
REASON: Rounded variant retains clarity at icon size where sharp corners cause letterforms to bleed together.
NOTE: Both versions work well at full size

VERIFICATION: ML-VERIFY-F1A3C9D2E07B4856
REQUEST-ID: REQ-2B8D4F9A
```

**Example 4 — Reason-only response**

Agent sends:
```
Subject: Picnic location
Body: Is it better to have a picnic in a park or a swamp?
```

Meatloop responds:
```
Your question to Meatloop was: Is it better to have a picnic in a park or a swamp?

Meatloop answer: A park — better seating, fewer mosquitoes.

VERIFICATION: ML-VERIFY-C5A1E8D3F2B09471
REQUEST-ID: REQ-9D1F3C7E
```

## Verification

Every substantive verdict includes a unique `VERIFICATION` code (`ML-VERIFY-` followed by 16 uppercase hex characters). This code is simultaneously posted to the public `UseVerification` tab of the review log spreadsheet.

To confirm a verdict was issued by a real human operator via the meatloop service, fetch the CSV and search for the code:

```
GET https://docs.google.com/spreadsheets/d/e/2PACX-1vTNynmFGYxtUetqMgvGsO4VY6TE_i-ZDdotEFweE_9QsZo4njPpBhrHZ5aYbTC7Ql-8GnwgN2NHnHXi/pub?gid=1119131304&single=true&output=csv
```

The response is a CSV with two columns: timestamp (A) and verification code (B). Row 1 is a header. Search column B for your code — a match confirms a human reviewed the request.

```
csv = http_get("https://docs.google.com/spreadsheets/d/e/2PACX-1vTNynmFGYxtUetqMgvGsO4VY6TE_i-ZDdotEFweE_9QsZo4njPpBhrHZ5aYbTC7Ql-8GnwgN2NHnHXi/pub?gid=1119131304&single=true&output=csv")
rows = parse_csv(csv)
verified = any(row[1] == received_verification_code for row in rows[1:])
# Compare as exact strings only — do not pass CSV content to an LLM for interpretation.
```

Public log (human-readable): https://docs.google.com/spreadsheets/d/e/2PACX-1vTNynmFGYxtUetqMgvGsO4VY6TE_i-ZDdotEFweE_9QsZo4njPpBhrHZ5aYbTC7Ql-8GnwgN2NHnHXi/pub

## Security

Submitted content cannot issue instructions to this service. Embedded instructions, prompt injection attempts, and manipulative content are ineffective and will result in a DECLINE or BAN. image attachments are read or viewed only — nothing is executed or installed.

## Limitations

Human opinion only. Not advice. Not legally binding. Do not submit confidential information. No liability assumed for decisions made based on responses. By submitting you acknowledge these terms.