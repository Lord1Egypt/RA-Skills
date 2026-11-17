# Motivation Letter Reference

Actionable guidelines for drafting a motivation/cover letter. Every rule tells you *what to do*, not just *what to aim for*. This file is read by an AI agent (Claude) when drafting or reviewing a letter from a `letter.yaml` file.

**Cross-references used throughout this document:**
- `job-posting-extraction.md` — provides the extracted schema, especially `company_values_tone`, `must_haves`, `nice_to_haves`, `keywords`
- `gap-analysis.md` — provides the tailoring plan (AMPLIFY, REFRAME, HONEST-GAPS)
- `cv-craft.md` — governs the honesty standard that applies equally here

---

## 0. When to Write vs. Skip

Write a motivation letter by default. Skip it only when one of the following clearly applies:

| Skip condition | Explanation |
|---|---|
| The portal has no field for it | If the ATS provides nowhere to attach or paste a letter, omitting it is correct — don't force it into the "additional documents" field as a workaround unless you are confident it will be read. |
| The posting explicitly says not to include one | Respect it; ignoring the instruction signals poor reading comprehension. |
| High-volume / quick-apply role where letters are not standard | Mass-application postings (e.g. LinkedIn Easy Apply with 500+ applicants, junior roles where the process is clearly volume-driven) rarely have letters read. |
| A strong referral has effectively replaced it | If the referring contact has briefed the hiring manager, a formal letter may be redundant — confirm with your referral. |

**Why write even when unsure it will be read:** ~45% of hiring managers read the cover letter *before* the CV — it can set the frame for everything that follows. Write it as if it will be read first, by someone who hasn't seen your CV yet.

**Earning attention:** ~65% of recruiters don't read every cover letter. A letter that looks generic at a glance (boilerplate opener, vague claims, no company-specific anchors) will not be read. The test is: would this letter make an overloaded recruiter slow down in the first two sentences? If not, revise the opening.

---

## 1. Structure: the Paragraphs in Order

A motivation letter has exactly four logical parts, written as 3–4 short paragraphs. Do not deviate from this order.

### 1.1 Opening Hook (Paragraph 1)

**Purpose:** Establish why *this* company and *this* role, not any job that fits your profile.

**How to write it:**
1. Open with a specific, concrete anchor — a product the company ships, a mission statement you can quote, a technology bet they've publicly made, or something from the `company_values_tone` field extracted per `job-posting-extraction.md`.
2. Connect that anchor to a genuine professional interest or experience of your own in one sentence.
3. State the role you're applying for. Do not bury it; the reader should know within the first two sentences.

**What to avoid:**
- "I am writing to apply for the position of…" — generic and reads as filler.
- Praise that could apply to any company ("a fast-growing company with an exciting culture").
- Opening with "I" if it can be avoided — restructure the sentence to lead with the company's work.

**Strong example:**
> Meridian's bet on real-time anomaly detection for payment fraud — described in detail in your 2025 engineering blog post — sits squarely at the intersection of my PhD work on streaming change-point detection and my two years shipping production ML pipelines at DataFlow. I'd like to join your ML Platform team as a Senior Machine Learning Engineer.

**Weak example:**
> I am writing to apply for the Senior Machine Learning Engineer role at Meridian. I am a passionate machine learning engineer with experience in several areas relevant to your business.

---

### 1.2 Fit Narrative (Paragraphs 2–3, or one longer paragraph)

**Purpose:** Demonstrate that you can do the job, with evidence — not claims.

**How to write it:**
1. Select the **2–3 strongest matched requirements** from the AMPLIFY list in `gap-analysis.md`. Do not try to cover every requirement — depth beats breadth.
2. For each selected requirement, write one to two sentences that:
   - Name the real experience or achievement from your CV (the specific role, project, or outcome).
   - Connect it explicitly to the company's need: "…which is exactly the pattern your job description describes as…" or more naturally woven.
3. Do not restate the CV verbatim. The letter should add context and connection, not just repeat bullet points.
4. If gap analysis identified an `HONEST-GAP` with a "cover letter" mitigation, this is where to include it — honest framing of transferable strength or learning trajectory. See §5 (Honest-only Rule) and `gap-analysis.md §4`.

**How many requirements to cover:**

| Seniority | Requirements to highlight |
|---|---|
| Intern / Junior | 2 (depth over breadth; pick the strongest and the most differentiating) |
| Mid | 2–3 |
| Senior / Lead | 3 (include at least one that speaks to scope/impact, not just technical skill) |

**What to avoid:**
- Listing skills as assertions without evidence: "I am highly proficient in Python and have strong communication skills."
- Starting every sentence with "I" — vary the syntax.
- Restating your CV word for word — the letter adds narrative, not a second CV.

---

### 1.3 Company-Specific Paragraph (Paragraph 3 or 4)

**Purpose:** Show genuine knowledge of this company and explain why you want *them*, not just any employer who needs your skills.

**How to write it:**
1. Draw from `company_values_tone` (extracted per `job-posting-extraction.md`). Use the company's own framing when quoting their mission or values — paraphrase accurately rather than copying verbatim.
2. Name something specific: a product, a market position, a strategic direction, a team culture detail, or a public statement. Generics ("innovative company", "great culture") are worthless. **If the posting alone doesn't give you a concrete anchor, fetch one** — `WebFetch`/`WebSearch` the company's careers page, product page, engineering blog, or a recent announcement, and cite something real and specific from it. (Same fetch-don't-guess principle as enriching the CV from the candidate's papers/repos.) Never invent a detail about the company; if you genuinely can't find one, keep the paragraph honest and lean rather than fabricating specifics.
3. Connect your motivation honestly. If you are attracted to the problem domain, say so and explain the connection to your own interests. If you are motivated by the team's technical approach, be concrete about what in their stack or methodology appeals to you.
4. This paragraph need not be long — two to three sentences is enough. Its job is to make the letter unmistakably *not* a template.

**What to avoid:**
- Empty flattery: "Meridian is an industry leader that I have long admired."
- Reusing the company's About page verbatim.
- Making claims you cannot defend in conversation ("I've followed Meridian for years" — if you haven't).

---

### 1.4 Forward-Looking Close and Call to Action (Final Paragraph)

**Purpose:** Signal enthusiasm for next steps, project briefly what you'd bring, and make it easy to respond.

**How to write it:**
1. State one forward-looking value you'd bring — connect your background to their trajectory, not just their current state.
2. Express genuine availability: "I'd welcome a conversation at your convenience" or similar. Keep it professional and confident, not desperate.
3. If there is a concrete timeline detail (e.g. you are available from a certain date), include it here. If not, omit.
4. Close with a simple, professional sign-off. The `closing` field in `letter.yaml` handles the formal closing line (e.g. "Sincerely,") — the paragraph itself ends before that.

**What to avoid:**
- "I look forward to hopefully hearing from you" — hedging weakens the close.
- Restating everything you already said.
- Overly long closings that dilute the call to action.

---

## 2. Length and Format

| Constraint | Rule |
|---|---|
| **Word count** | 250–350 words optimal for the body (the `body` paragraphs in `letter.yaml`). **400 words is the hard ceiling** — do not cut genuine value just to hit 350, but nothing beyond 400. Stays comfortably on one page when rendered. |
| **Paragraphs** | 3–4 paragraphs total. Never a single monolithic block. Never more than 4 unless a specific structure requires it (rare). |
| **Sentence length** | Vary it. Short sentences punch. Longer sentences can carry nuance. Aim for an average under 22 words. |
| **Page limit** | One page, always. If the rendered output overflows, cut — starting with adjectives, filler transitions, and any sentence that is not carrying its weight. |
| **Format** | Professional but human. Not a legal brief, not a casual email. Match the tone to the company (see §3). |
| **File format** | The `letter.yaml` `body` field is a list of paragraph strings. Each list item is one paragraph. Render to PDF for submission. |

---

## 3. Tone Matching

The cover letter's register must match the company's voice. Use `company_values_tone` from the extraction to calibrate.

### How to calibrate

| Signal in `company_values_tone` | Register to use |
|---|---|
| "formal", "corporate", "enterprise", "regulated industry" | Formal: full sentences, no contractions, passive voice acceptable, "the candidate" → "I" used sparingly and carefully structured |
| "casual", "startup", "autonomous", "you'll", "we believe", "fast-moving" | Natural, direct, first-person throughout, contractions acceptable ("I've", "we're"), shorter sentences |
| "purposeful but informal", "mission-driven" | Warm professional: contractions sparingly, active voice throughout, personal but not chatty |
| No clear tone signal | Default to warm-professional |

### Same content, two registers

**Scenario:** Candidate improved data pipeline latency by 40%.

**Formal (enterprise/corporate):**
> During my tenure at DataFlow Ltd, I led the re-architecture of the primary ingestion pipeline, achieving a 40% reduction in end-to-end latency and eliminating recurrent SLA breaches that had affected downstream analytical teams.

**Casual (startup):**
> At DataFlow I rebuilt the ingestion pipeline from scratch — cut latency 40%, killed the SLA fires that kept the analytics team up at night. That's the kind of ownership I'd bring to Meridian's platform work.

Both are accurate and professional. The content is identical; the rhythm and vocabulary differ. Match the register to the signal in `company_values_tone`.

---

## 4. The `letter.yaml` Field Mapping

The file consumed by `scripts/render_letter.py` has this exact schema:

```yaml
meta:
  language: "en"        # ISO 639-1, the letter's language: en | nl | de | fr | es | it | zh | ja | ko | …
  target_market: "us"   # same value as the CV's meta.target_market; us/ca → Letter paper, others → A4

sender:
  name: "Jane Smith"
  email: "jane.smith@email.com"
  location: "Amsterdam, NL"

recipient:
  name: "Hiring Team"          # see below for unknown-recipient rules
  company: "Meridian BV"
  location: "Amsterdam, NL"

date: "YYYY-MM-DD"             # ISO 8601; fill with today's date

salutation: "Dear Hiring Team,"  # see salutation rules below

body:
  - "Opening hook paragraph text."
  - "Fit narrative paragraph 1 text."
  - "Fit narrative paragraph 2 text (or company-specific paragraph if fit is one paragraph)."
  - "Company-specific paragraph text (if fit narrative is two paragraphs, this is paragraph 4)."
  - "Forward-looking close paragraph text."

closing: "Sincerely,"
```

### Field-by-field rules

**`meta`** — copy `language` and `target_market` from `tailored-profile.yaml`'s `meta`, so the letter is in the
CV's language and on the CV's paper. Optional: `paper: "a4" | "letter"` to force the size, `main_font`, `cjk_font`.
When it is omitted, `render_letter.py` infers each value and says so on a `NOTICE:` line: language from the body,
then the workspace's `tailored-profile.yaml`, then `en`; paper from that profile (or `profile.yaml`), then a US/Canada
`posting.yaml` location → Letter, else A4. A salutation or closing in a different language from the body is
`SALUTATION_LANGUAGE_MISMATCH` / `CLOSING_LANGUAGE_MISMATCH` in `check_letter.py`.

**`sender`** — Fill from the candidate's profile. All three sub-fields are rendered on the letter header.

**`recipient.name`** — The contact person's name if known (e.g. "Dr. A. de Vries"). If unknown, use the team or department as the display name:
- Preferred (in order): the hiring team's name ("Data Engineering Hiring Team"), the department ("Engineering Team"), the generic "Hiring Team".
- Avoid "To Whom It May Concern" — it reads as 1990s boilerplate and signals you did not look for a name.
- If the posting names a contact, use their name here and in the salutation.

**`recipient.company`** — The exact company name as written publicly. Spelling the company name wrong is a disqualifying error.

**`date`** — ISO 8601 format (`YYYY-MM-DD`). Use the date of final preparation, not the date of the initial draft.

**`salutation`** — Follows `recipient.name`:

| Situation | Salutation |
|---|---|
| Named contact (person's name confirmed) | `Dear [First name] [Last name],` or `Dear [First name],` (use first name if the company tone is casual; full name if formal) |
| Name only guessed / inferred (uncertain) | Use `Dear Hiring Team,` — a generic but professional salutation is not penalised; a wrong name is worse than a generic one |
| Team/department, no named contact | `Dear [Team Name] Hiring Team,` or `Dear Hiring Team,` |
| Academic / highly formal context | `Dear Dr. [Last name],` |
| Do not use | `To Whom It May Concern,` — outdated; `Dear Sir/Madam,` — outdated and gendered; never fabricate a name |

**Localized salutations (non-English letters):** when the letter is written in the market's local language, use that language's standard salutation — not a literal translation of "Dear". For an unnamed recipient: German `Sehr geehrte Damen und Herren,`; French/Belgian `Madame, Monsieur,`; Spanish `Estimados señores:`; Italian `Gentile Responsabile delle Assunzioni,`; Dutch `Geachte heer/mevrouw,`. For a named recipient, use the formal gendered form (e.g. German `Sehr geehrte Frau [Last],` / `Sehr geehrter Herr [Last],`). Match the salutation's language to the letter's language; never mix.

**`body`** — A YAML list. Each element is one paragraph as a single string. No Markdown formatting inside the strings (no `**bold**`, no bullet points) — render_letter.py outputs plain text per paragraph. Keep each paragraph to 4–7 sentences maximum.

**`closing`** — Choose from: `"Sincerely,"` (universal, formal), `"Kind regards,"` (warm professional), `"Best regards,"` (slightly more casual). Match the register. The sender's name is appended automatically by render_letter.py.

**Localized closings (non-English letters):** the standard formal sign-off in that language, matching the salutation above and never an English one appended to a non-English letter. German `Mit freundlichen Grüßen`; Dutch `Met vriendelijke groet,`; French `Cordialement,`; Spanish `Atentamente,`; Italian `Cordiali saluti,`. This table exists because the renderer needs one: leaving it out meant a Dutch letter with a correctly localized opener still had to be given an English sign-off or none at all. For a language not listed — Chinese, Japanese, Korean and every other — the skill has no sign-off to offer and `check_letter` says so (`NO_CLOSING`) rather than inventing one; write it yourself in the letter's own language.

---

## 5. Honest-Only Rule

The same honesty standard that governs the CV governs the cover letter, without exception. Cross-reference `gap-analysis.md §2` (Honest-Reframing Decision Rules) and `cv-craft.md §7` (Honest Reframing Only).

### What is allowed

- **Framing and contextualising real experience** — connecting what you did to what they need, in your own words.
- **Projecting genuine interest forward** — explaining why the company's direction aligns with what you want to work on next, if it genuinely does.
- **Addressing an honest gap positively** — when `gap-analysis.md` specifies "address in cover letter" as a mitigation, use the transferable-strength framing it proposes. The framing must be true.
  - Example: "My analytical work has been in e-commerce at scale rather than fintech directly, but working with 10M+ monthly transactions has given me hands-on experience with the same data quality and funnel analysis challenges a payments team faces."
- **Expressing enthusiasm for aspects of the role that genuinely appeal to you** — if you care about the problem domain or the team's technical approach, say so and say why.

### What is not allowed

- Inventing passion: "I have always been passionate about fintech" — if you haven't, don't write it. It reads hollow in the letter and unravels in conversation.
- Claiming familiarity with a company's product you have not actually used: "I use Meridian's dashboard daily" — if untrue.
- Fabricating or exaggerating experiences to fill a gap — this is the same prohibition as in `cv-craft.md §7`. An honest gap framed with real transferable strength is stronger than a fabricated claim that unravels at interview.
- Softening a genuine gap by implying it isn't one: if you lack fintech experience and the role requires it as a hard must-have, honest framing of transferable skills is appropriate; implying the gap doesn't exist is not.

### The honest-gap close

When a material gap exists and the gap analysis says "address in cover letter", follow this pattern in the fit narrative paragraph:

1. Acknowledge the gap briefly and honestly — do not lead with it, but do not hide it.
2. State the adjacent strength that partially covers it — with evidence.
3. If relevant, state genuine learning trajectory: courses underway, projects in progress. Only if real.

> "My background has been in e-commerce data rather than payments directly. The analytical patterns — funnel integrity, transaction anomaly detection, high-volume data quality — transfer directly, and I've spent the past month building a side project with open fintech datasets to close the domain gap."

---

## 6. AI-Authenticity: When AI Help Hurts and When It Doesn't

~67% of hiring managers report they can spot AI-generated cover letters; ~54% view them negatively. However, **personalized AI-assisted letters are viewed favorably** — the problem is *generic* output, not AI involvement.

### Tell-tale markers to eliminate

| Marker | Example | Fix |
|---|---|---|
| Buzzword overload | "results-driven professional leveraging synergy to deliver proven track records" | Name a real outcome instead: "cut latency 40%" |
| Flawless-but-voiceless prose | Grammatically perfect sentences with no personality, no concrete detail | Add one specific product, number, or moment that only you could write |
| Generic enthusiasm | "I am passionate about innovation and excited to contribute to your mission" | State *which* aspect of the company's work and *why it connects to your work* |
| Formulaic structure that matches every template | Hook → "my experience includes" → generic company praise → generic close | Lead with something that would only appear in a letter for this specific company |
| Abstract claims, no concrete detail | "I have strong communication skills and a track record of success" | Evidence or remove: "presented quarterly findings to a 12-person exec team" |
| The 2026 vocabulary | spearheaded · pivotal · intricate · showcasing · delve · realm · robust · cutting-edge · seamless · "valuable asset" · "thrive in a fast-paced environment" | Say what the candidate did. The word is doing no work the specific fact would not do better |
| "Not just X, but Y" | "This is not just a role — it is a chance to…" | The single most recognisable construction in model prose. State the thing you mean without the contrast |
| Em dashes at model rate | three or more in a 300-word letter | Models use them at two to three times the human rate. Keep one at most; a comma or a full stop does the same work without the signature |
| The rule of three, applied to everything | "efficient, effective, and reliable" three times in one letter | One tricolon is good writing. Three is a template. Keep the one that carries the most weight |

**These five are checked mechanically.** `scripts/check_letter.py` reports them as
`AI_VOCABULARY`, `NOT_JUST_PIVOT`, `EM_DASH_DENSITY` and `TRICOLON_DENSITY`, and
`scripts/lint_cv.py` reports the vocabulary on the CV — over the whole document,
because the summary is the line a recruiter reads first. The thresholds are
densities calibrated against real letters (including this skill's own), not
absolutes: a single em dash and a single tricolon are ordinary writing and are
never reported. `scripts/prose_tells.py` carries the calibration table and, just
as importantly, what is deliberately NOT checked and why. The rest of this
section is the half no gate can measure — a gate can see the word `pivotal`; it
cannot see that the letter could have been sent to any employer.

### The 80/20 rule for AI-assisted letters

- **80% authentic specific content:** Real quantified achievements, company-specific references you researched, genuine reasons for interest. This content can only come from you.
- **20% AI polish:** Structure, transitions, register consistency, grammar. AI earns its place here.

A letter that passes this test: could any other candidate have written exactly this letter? If yes, it is too generic.

---

## 6b. Market & language calibration

**Language rule (all markets):** write the letter in the **same language as the CV / posting** (see `cv-craft.md §2` clusters). Never mix languages in one letter. Use the market's standard salutation (see the localized-salutation note above).

Calibrate tone and expectation to the market:

- **US & Canada / UK & Ireland / Australia & NZ:** cover letters are common but often skimmed; lead with the strongest hook fast. US tone tolerates more direct self-promotion than Europe; UK/Commonwealth is a touch more reserved.
- **EU / EEA:** formal and specific. For non-tech, public-sector, or local-company roles, write in the **local language**; English is fine for tech/international employers. Avoid American-style self-promotion — it reads as overclaiming across most of continental Europe.
- **East & SE Asia:** for international/foreign-capital firms, a Western-style letter in English (or the local language) works. **Japan caveat:** for a traditional rirekisho application the motivation lives in the form's **志望の動機** box, so a separate Western cover letter is usually redundant — a Japanese enclosure is a brief 添え状 (cover note), not a persuasive Western letter. Apply the §0 skip gate before drafting one.

**NL specifics (motivatiebrief):** in the Netherlands the letter is **universally expected** and read closely. Tone: direct and understated — American-style self-promotion creates a poor impression. Keep the opener concise (Dutch culture values getting to the point). Dutch-language postings expect a Dutch letter; English postings (especially tech) expect English. 250–350 words; a shorter, sharper letter is well-received, padding is not.

---

## 7. Common Mistakes to Avoid

| Mistake | Why it fails | Fix |
|---|---|---|
| Restating the whole CV | The reader has your CV. The letter should add narrative and connection, not duplicate. | Pick 2–3 points and go deep; leave the rest to the CV. |
| Generic templated opening ("I am writing to apply for…") | Signals effort was not spent on this letter. | Open with something specific to the company or role — see §1.1. |
| "I" overload | Reading "I did… I have… I believe… I would…" in every sentence shifts focus from their needs to your story. | Every second or third sentence should be about them: their challenge, their product, what you'd bring *to them*. |
| Misspelling the company or role name | Disqualifying; signals carelessness or a copy-paste template. | Check `recipient.company` against the exact public name. Check `role_title` from the extracted schema. |
| Exceeding one page | Hiring managers read many letters. Over one page implies you cannot edit. | Stay in the 250–350 word range for `body`. If rendered output overflows, cut the weakest sentences first. |
| Empty flattery | "Meridian is an industry leader and the most innovative company in the space" — provides zero information and reads as filler. | Replace with a specific observation: name the product, the feature, the blog post, the market position. |
| Writing to impress rather than to connect | Dense, jargon-heavy prose that performs intelligence instead of communicating it. | Write as if explaining to a sharp colleague, not performing for a committee. |
| Forgetting the call to action | A letter that ends without inviting next steps leaves the hiring manager with nothing to do. | Close with a clear, confident invitation for a conversation. |

---

## 8. Worked Example

### Input

**Posting (abbreviated):**
> **Data Analyst — London, UK (Hybrid)**  
> Fast-growing fintech. Join the Growth team. Work with marketing and product to turn raw event data into decisions.  
> Must-haves: 2+ years analytical experience; strong SQL; Python or R; stakeholder communication.  
> Nice-to-haves: dbt; Looker or Tableau; fintech background.  
> Tone: casual, ownership-driven, self-directed.

**Candidate (abbreviated):**
> 3 years as data analyst in e-commerce. Strong SQL, Python. Built ETL pipelines; cut analyst prep time 3 hrs/sprint. Presented quarterly board reports. No fintech experience. Uses Tableau; knows dbt from a side project.
>
> Gap analysis HONEST-GAP: fintech — mitigation: address in cover letter with e-commerce transaction volume as transferable.

### Strong letter body (as it would appear in `body:`)

```yaml
body:
  - "FinCo's Growth team sits exactly at the intersection I find most energising: raw event data that is messy, high-volume, and consequential — where a sharp SQL query and a well-framed chart can shift how a product team bets its next quarter. That is the kind of work I want more of, which is why the Data Analyst role caught my attention."
  - "For the past three years at ShopMetrics I've been the analyst bridging engineering and non-technical stakeholders — owning the SQL data models, writing the Python ETL pipelines, and presenting findings to the board each quarter. The most tangible result: a pipeline rebuild that cut analyst pre-processing time by three hours per sprint, giving the team room to actually think rather than wrangle. That same pattern — find the bottleneck, build the infrastructure, free up the human judgment — is what I'd bring to FinCo's Growth analytics."
  - "My direct fintech experience is limited; my background is e-commerce. That said, the analytical challenges are closely related: high-volume transactional data, funnel integrity, cohort analysis, and anomaly detection at scale. I've worked with datasets exceeding 10 million monthly transactions and built the stakeholder trust that comes from consistently accurate, timely reporting. I'd be on the fintech learning curve on domain-specific regulation and product language, and I'm already investing time there."
  - "I'd welcome the chance to talk through how my background maps to what the Growth team is building. I'm available from mid-July and happy to fit your timeline."
```

### Why this example works

- **Paragraph 1 (hook):** Opens with a specific description of the work, not a generic company compliment. States the role at the end.
- **Paragraph 2 (fit narrative):** Names the actual role, the real outcome (3 hrs/sprint), and a specific deliverable (board presentation). Connects it to their need without restating the CV bullet.
- **Paragraph 3 (honest gap + company-specific):** Directly acknowledges the fintech gap per the gap analysis HONEST-GAP mitigation, pairs it with the real transferable strength (transaction volume, funnel analysis), and adds a genuine learning signal. Does not pretend the gap doesn't exist.
- **Paragraph 4 (close):** Short, confident, concrete availability, clear call to action.
- **Tone:** Casual and direct — matches the startup/ownership-driven `company_values_tone` signal.
- **Word count (body only):** ~290 words.
