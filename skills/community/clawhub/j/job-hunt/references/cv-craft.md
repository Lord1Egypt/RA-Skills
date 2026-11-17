# CV Craft Reference

Actionable guidelines for building and tailoring CVs. Every rule here tells you *what to do*, not just *what to aim for*.

---

## 1. Section Ordering by Career Stage

### Early-career / Student (0–3 years experience, or still in education)

```
1. Contact header
2. Summary (optional — omit if no clear target; include if career-changing or injecting keywords)
3. Education  ← near top; it is your primary credential
4. Relevant Projects / Research
5. Work Experience  (internships, part-time, student jobs)
6. Skills (technical stack, languages, tools)
7. Awards / Honors / Certifications (if relevant)
8. Volunteer / Activities (only if it adds signal)
```

**Why:** A 2019 CS grad with a Google internship has more to show from coursework + projects than from 18 months of work history. Education and projects anchor the story.

### Experienced / Mid-to-Senior (3+ years)

```
1. Contact header
2. Summary / Professional Profile  ← 2–4 sentences; see §6
3. Work Experience  ← chronological, most recent first; takes the lion's share
4. Skills
5. Education  ← condensed: degree, school, year — no GPA unless <5 years ago and ≥3.7
6. Certifications / Courses (if relevant)
7. Publications / Patents / Talks (for technical/academic roles)
```

**Why:** Recruiters spend 6–10 seconds on first pass. Years of relevant impact must be front and centre.

### Academic / Research (PhD candidate, postdoc, research scientist, applying to research roles)

```
1. Contact header
2. Summary / Research profile  (2–4 sentences; the research you do and your angle)
3. Education  ← leads; for a researcher the degree/programme IS the headline credential
4. Research Experience  (the PhD/postdoc role and its contributions)
5. Publications  ← surfaced early; it is the currency of research hiring
6. Skills  (methods, software, modalities)
7. Projects (only genuinely standalone work — see §9)
8. Awards / Grants
```

**Why:** Penn Career Services, Wordvice, and Paperpile all converge here — academic and research CVs lead with Education and bring Publications up near the top, because that is what a research hiring committee scans for first. A 2nd-year PhD has more signal in their programme + papers than in a job-title timeline. For an industry role that happens to value research (e.g. an ML-research engineer position), this order still reads well; for a pure software role, fall back to the experienced/industry order above and let work impact lead.

### Senior leader / Executive (15+ years, P&L / org leadership, director and above)

```
1. Contact header
2. Executive Summary  ← 3–5 lines; scope owned (revenue/P&L, headcount, geographies), leader type, signature outcomes
3. Selected Achievements  ← 3–5 career-defining results above the timeline (turnarounds, exits, scale-ups)
4. Work Experience  ← scope-and-outcome framed; compress the oldest roles to one line each
5. Board / Advisory roles (if any)
6. Education + Executive education
7. Awards / Speaking / Affiliations (if they add signal)
```

**Why:** at this level the reader (a CEO, board, or search partner) scans for altitude — scope, P&L, transformation — not a keyword list, and exec hiring routes more through search/referral than ATS filters. A 1-page IC template buries exactly what gets someone shortlisted. 2 pages is normal and **3 is legitimate** when senior roles are genuinely distinct (see §5). The renderer has native `achievements` ("Selected Achievements") and `board` ("Board & Advisory") sections for exactly this — promote them via `meta.section_order`. Full playbook: `candidate-situations.md §6`.

### Credential-led and non-technical roles

For regulated and non-software professions — clinical/nursing, legal, finance, skilled trades, teaching, and others — the first thing the reader (or a credentialing screen) checks is often a **licence, registration, ticket, or portfolio**, not work history. Surface it accordingly: relabel the `certifications` section to the field's header and push it high. E.g. a nurse: `meta.section_order: [summary, certifications, experience, education, skills]` with `meta.headings: {certifications: "Licenses & Certifications"}`. The full per-family recipes (what to lead with and how each field evidences competence) are in **`role-families.md`** — read it whenever the target is not a software/research/engineering role. Some public-sector roles aren't a free CV at all but a criterion-scored form — see `structured-applications.md`.

### Controlling order in practice: `meta.section_order`

This is the escape hatch for **every** case the two auto-picked defaults don't fit — exec, credential-led, career-changer, a publication-heavy candidate, or any target-specific preference — so reach for it freely; it's not an edge case.

The renderer auto-picks only two defaults: a **current** PhD/researcher role, or a current student with no work history, triggers the academic order (Education first); everyone else gets the industry order (Experience first). That binary doesn't know about executives or credential-led professions — so for those, **set `meta.section_order` explicitly** (and `meta.headings` to relabel a section). An explicit list wins outright. Listing a subset only reorders those sections; every section that has real content still renders (the field sequences sections, it does not hide them). Use it, for example, to lead with an Executive Summary + Selected Achievements, to surface Licenses for a nurse, to push Publications above Experience for a researcher, or to force Experience-first for a PhD applying to an industry engineering role.

---


### Deciding between the templates

The three above overlap, and the overlap is the common case rather than the edge
one: a PhD candidate is *still in education* AND may be applying to industry, so
the early-career template and the mid-senior template both fire. Pick with these
two questions, in this order — **not** by whether the employer is academic or
industrial, which is the wrong axis and the one that gets reached for first.

**1. Is the degree in the target role's own domain?**

A doctorate in the field the job is about is a **credential the reader is
looking for**, and it belongs where they will look — near the top, whoever the
employer is. An MRI-reconstruction PhD applying to medical-imaging AI is not
"academic background"; it is the strongest single line on the page. The same
doctorate applied to an unrelated role — insurance-process automation, say — is
background, and Experience should lead instead.

Check it against the posting, not against the employer's sector: if the degree
or its field appears in `must_haves`, it is relevant by the posting's own words.

**2. How much formal post-degree experience is there?**

At **3+ years** of formal industry experience, Education moves below Experience
and condenses to degree / school / year regardless of relevance — by then the
track record is the stronger evidence and the degree is corroboration. Below
that, or while still in education, relevance decides.

| | degree IS in the role's domain | degree is NOT in the role's domain |
|---|---|---|
| still studying, or <3 yrs formal experience | **Education near the top** | Experience leads; Education after it, still on page one if the posting names a degree requirement |
| 3+ yrs formal experience | Experience leads; Education below it, condensed | Experience leads; Education last, condensed |

**Watch the must-have you are burying.** If the posting's first requirement is a
degree and Education sits on page two, the one hard credential the screener is
checking for is where a ten-second skim will not reach it. Naming it in the
summary mitigates that; it does not replace it.

This is a judgement the candidate is entitled to make. State which template you
applied and why, and offer the alternative — a late-stage PhD generally has a
clearer view of how their doctorate reads to their own field than a rule table
does.

## 2. Regional Conventions & Language

Target markets fall into three clusters that share CV conventions. The user picks a cluster; you then pin down the **specific country** (it refines the details below) and the **CV language**. Set `meta.target_market` (country/market) and `meta.language` accordingly. The conventions that vary across clusters: length, photo, personal data, "CV" vs "Resume" terminology, references, and language.

### Cluster 1 — Anglophone developed (US, Canada, UK, Ireland, Australia, New Zealand)

Language: **English** (Canada: also French for Québec / bilingual federal roles). This cluster contains two convention sub-styles — do **not** blur them:

- **US & Canada — *résumé* style.** The document is a "Resume". **1 page** (US strict; a 2nd page only at 10+ years / senior). **Never** a photo, DOB, marital status, or nationality. No references section ("available on request" is filler — omit). Reverse-chronological, single column. Contact: name, phone, email, city + state/province (no street address), LinkedIn, GitHub/portfolio if relevant.
- **UK, Ireland, Australia & New Zealand — *CV* style.** The document is a "CV". **Up to 2 pages** (1 fine for junior). No photo; no DOB/marital status (discrimination grounds). "References available on request" is acceptable, or omit. Otherwise the same clean reverse-chronological single column.

### Cluster 2 — EU / EEA (continental developed)

Representative, not exhaustive: Netherlands, Germany, France, Belgium, Spain, Italy, Austria, Portugal, Poland, and the Nordics (Sweden, Denmark, Norway, Finland). Use the nearest-neighbour conventions for an unlisted EU country.

- **Language — English *or* the official local language.** English is standard and expected in **tech and at international/multinational employers** across the EU. The **local language** is preferred for non-tech, public-sector, government, healthcare, and traditional-industry roles. When unsure, match the posting's language; offer both if it adds value. Built-in localized headings exist for `nl`, `de`, `fr`, `es`, `it`; for any other language set `meta.headings` (the renderer applies it). Write the CV *content* in the chosen language, not just the headings.
- **Length:** 2 pages (academic CVs longer). **Format:** clean custom reverse-chronological single column. **Personal data:** nationality / work-authorization is commonly included (helpful for non-EU candidates); DOB optional and country-dependent — omit unless the local norm expects it.
- **Photo:** optional; **common in DE, FR, and traditional NL sectors**, less so for tech/international. Omit by default for tech/international employers; include where the sector expects it.
- **Europass:** recognised by EU institutions and some public-sector roles, but private recruiters often find it verbose and dated. Use a clean custom CV by default; switch to Europass only if the posting explicitly asks.
- **NL specifics:** English CVs are standard at Dutch tech and international firms; write in Dutch (or offer both) for Dutch-language postings (overheid, onderwijs, traditional industries). Photo: omit by default for tech/international; traditional Dutch-speaking sectors (retail, hospitality) may still expect one — match the sector.

### Cluster 3 — East & Southeast Asia (China, Japan, South Korea, Singapore, Malaysia, Thailand)

Conventions vary substantially **by country** here — honor the local norm rather than one template:

- **Language — English *or* the official local language** (Mandarin, Japanese, Korean, Thai; English in SG/MY). English is standard in **Singapore and Malaysia** and at multinationals/tech across the region; the local language is expected for domestic-facing roles and local employers. CJK/Thai render in **all formats including PDF** — the renderer auto-detects CJK and switches to a XeLaTeX/xeCJK build with a cross-platform CJK font fallback, so a Chinese/Japanese/Korean PDF compiles wherever a CJK font and a Unicode engine (`xelatex`/`tectonic`) are installed (it degrades to Markdown/.docx + a ready-to-compile `.tex` if not). Localized section labels for **zh / ja / ko are built in** (no `meta.headings` needed; set it only to override a specific label or for another CJK language); optionally set `meta.cjk_font` to pin a specific font. For a CJK summary/bullets, prefer a literal block (`summary: |`) or an inline string over a YAML folded scalar (`>`) — though the renderer also strips folded-scalar spaces that fall between CJK characters.
- **Singapore & Malaysia:** closest to UK/Commonwealth — English CV, up to 2 pages. A photo and some personal details (nationality, occasionally DOB) are more commonly accepted than in the West, but a clean no-photo CV is fine for tech/MNCs.
- **China:** photo commonly included; personal details (DOB, sometimes hometown) often expected on domestic CVs. A bilingual (Chinese + English) CV is common for MNC roles.
- **Japan:** two document types — the highly-formatted *rirekisho* (履歴書, a templated form with photo and personal data, expected by many traditional employers) and the *shokumu-keirekisho* (職務経歴書, a free-form work-history CV that the normal Western render covers). Global/foreign firms accept a Western-style CV; traditional Japanese employers expect the rirekisho. **Flag this fork to the user**; when they need the rirekisho, follow `references/rirekisho.md` and render it with `scripts/render_rirekisho.py` (→ `.docx`; export to PDF from Word/LibreOffice).
- **South Korea:** photo and personal details commonly expected on domestic CVs; an English résumé is accepted at global firms.
- **Thailand:** photo commonly included; English or Thai depending on the employer.

**Japanese DOCX in LibreOffice on macOS.** A local export check found that
LibreOffice substituted the default `Yu Mincho` with an ExtraBold face even
though the same DOCX opened with regular body text in Microsoft Word. If that
happens, and the font is installed, set `meta.cjk_font: "Hiragino Mincho ProN"`
(the family name, without `W3`). Native Word and LibreOffice exports both kept
regular body text and bold headings with that setting. Reopen and review the
result in the recipient's app; do not assume this local fallback exists on
another system or change an explicitly selected template font.

### Default — unknown / unlisted market

Reverse-chronological, single column, **no photo, no personal data**, English, 1–2 pages. Match the posting's language. This conservative US/UK style is safely received almost anywhere.

### Personal-data safety interlock (apply before rendering — this is a hard rule, not a style preference)

The conventions above are not symmetric in *risk*. Adding a photo/DOB in the EU is a neutral style choice; adding one to a **US/Canada/UK/Ireland/Australia/NZ** application is a genuine problem — many employers there route such CVs straight to rejection because considering that data exposes them to discrimination-law liability. Because a returning user's master profile may have been built for an EU/Asia target (and may legitimately carry a photo, DOB, nationality, or marital status), you must not let those fields bleed into a Cluster-1 application.

So, when `meta.target_market` is a **Cluster-1** country (US, CA, UK, IE, AU, NZ) **or** the conservative default: **strip photo, date of birth, age, marital status, and nationality from the tailored profile even if they are present in the master**, and tell the user you did and why ("US employers can't consider these — including them only hurts you"). Never *add* them for a Cluster-1 target. The one deliberate exception is a Japanese *rirekisho* (`references/rirekisho.md`), which is a different document type with its own form — its photo/DOB belong only on that form and must **never** be reused for any non-Japan target. When in genuine doubt about a market, follow the conservative default and omit them.

**Where personal data and a photo live (for markets that expect them).** When the target market *does* expect them — much of continental Europe (DE, FR, traditional NL/IT/ES sectors) and East Asia (China, Korea, Japan-Western-CV) — put them in `contact.personal` (a dict, e.g. `{date_of_birth: "1992-05-01", nationality: "...", hometown: "...", marital_status: "..."}`) and set `meta.photo` to an image path. The renderer shows the personal block in the header and a passport-style photo in the header area: above the name in LaTeX/PDF, after the contact details in .docx. Markdown embeds the path. **The renderer enforces the interlock as defense-in-depth**: for a Cluster-1 `meta.target_market` it ignores `contact.personal` and `meta.photo` entirely, so a mis-tailored profile physically cannot leak protected data onto a US/UK CV. Collect these fields honestly from the user — never invent a DOB, nationality, or photo.

### File format (all clusters)

`.docx` for ATS/portal submission (see §4); PDF for the human-facing copy or when the posting requests it. Markdown/.docx for any CJK/Thai CV (PDF caveat above).

**Accents and non-Latin letters in the PDF.** The renderer emits a `fontspec` source for `tectonic`/`xelatex`/`lualatex` and an `inputenc`/`fontenc` source for `pdflatex`, so `Łukasz Wójcik`, `Politechnika Śląska`, `Škoda` and `Ștefan` come out intact under either. If a character is not in the font, the engine drops it and still exits 0 — so `render_cv.py` scans the engine's `Missing character` warnings, refuses to write the PDF, and names the codepoints; `scripts/check_pages.py` independently re-reads the finished PDF and fails if `meta.name` or any `experience[].org` is not in it. The fix when it fires is `meta.main_font: "<a font installed here>"` (Latin) or `meta.cjk_font` (CJK); the default Latin Modern covers Latin-1 and Latin Extended-A but not Cyrillic or Greek. Never hand over a PDF the renderer refused — `.md` and `.docx` are unaffected and can look perfect while the PDF has lost letters out of the candidate's own name.

---

## 3. The Bullet Pattern

### Formula

```
[Strong action verb] [what you did / what you built] [resulting in / by / which] [quantified outcome]
```

**Key rules:**
- **Tense rule:** Use past tense for completed achievements in all roles, including the current one. Use present tense only for genuinely ongoing responsibilities in the current role (e.g. "Own the production ML pipeline"). Mixing tenses within a current-role entry is correct and expected — completed projects get past tense; live responsibilities get present tense.
- Quantity wherever possible: %, $, hours, users, latency, error rate, team size.
- If you have no number, name the scope or scale: "across 3 microservices", "for a team of 12", "supporting 200k MAU".
- One bullet = one accomplishment. Not a job description.
- **Be ruthlessly concise — a recruiter skims, and a wall of text gets skipped.** Prefer **one line** per bullet; two is the ceiling. Front-load the point (result or action first) so it survives a half-second glance. Cut filler that adds no signal: "responsible for", "in order to", "successfully", "various", "a number of", "helped to", and most adjectives. Strip a clause if removing it loses no meaning. If a bullet runs to three lines, it is either two bullets or it is padded — fix it. Density of *signal* matters, not density of *words*.

### Action Verb Bank (~25 verbs, grouped)

| Category | Verbs |
|---|---|
| **Led / Managed** | Led, Managed, Directed, Owned, Oversaw, Mentored, Coordinated |
| **Built / Created** | Built, Architected, Designed, Developed, Implemented, Launched, Deployed |
| **Improved / Optimised** | Reduced, Cut, Accelerated, Optimised, Streamlined, Automated, Refactored |
| **Analysed / Modelled** | Analysed, Modelled, Evaluated, Benchmarked, Audited, Diagnosed, Investigated |
| **Delivered / Shipped** | Delivered, Shipped, Migrated, Integrated, Released, Rolled out |

Avoid weak openers: "Responsible for", "Worked on", "Helped with", "Assisted in", "Was involved in" — these describe a job description, not an achievement.

### BEFORE → AFTER Example

**BEFORE (weak):**
> Responsible for the data pipeline, including making sure it ran on time and fixing bugs when they came up.

**AFTER (strong):**
> Cut data-pipeline end-to-end latency 40% by rewriting the batch layer in Rust, eliminating a 3-hour SLA breach and saving ~6 engineer-hours/week in on-call firefighting.

**Why it's better:** Starts with the outcome-oriented verb "Cut", quantifies the improvement (40%), names the concrete action (rewrote in Rust), and shows downstream business impact (SLA, engineer hours).

**Second example:**

**BEFORE:**
> Worked on improving model accuracy for the recommendation system.

**AFTER:**
> Raised recommendation CTR by 12% (from 3.1% to 3.5%) by replacing collaborative filtering with a two-tower neural model, deployed to 4M users in production.

---

## 4. ATS (Applicant Tracking System) Rules

ATS parsers are used by most companies with 50+ employees. A CV that confuses the parser gets zero human eyes.

### Do

- **Use standard section headings exactly:** `Experience` or `Work Experience`, `Education`, `Skills`, `Summary` or `Professional Summary`. Non-standard headings like "Where I've Worked" or "My Toolkit" may not be parsed.
- **Mirror the job posting's exact phrasing.** If the posting says "CI/CD", write "CI/CD" — not only "continuous integration/continuous delivery". If it says "React.js", match that casing.
- **Single-column layout.** ATS reads left-to-right, top-to-bottom in the document order. Multi-column layouts split mid-sentence.
- **Use a common system font:** Calibri, Arial, Helvetica, Garamond, Georgia, Times New Roman. Avoid decorative or web-only fonts.
- **Keep critical content in the body.** Text in headers, footers, text boxes, and tables may be skipped by parsers. Do not put your name only in the document header.
- **File format — default to `.docx` for ATS/portal submissions.** 2025 parser testing across major ATS (Workday, Taleo, iCIMS) shows `.docx` parses more reliably than PDF in most portals. Use **PDF for the human-facing copy** (emailed directly to a recruiter, uploaded to a portfolio, or printed) and when the posting explicitly requests PDF (Greenhouse handles PDF well). If the portal gives you a choice and the posting doesn't specify, submit `.docx`. Never submit both unless asked.
- **File naming:** `FirstName_LastName_CV.docx` / `FirstName_LastName_Resume.pdf`. Avoid names like `final_v3_REVISED_2.docx` — they signal disorganisation and can mangle ATS metadata.

### Do Not

- Multi-column layouts for parsed sections (a two-column Skills section is a common trap). **Severity: two-column and table-based layouts caused parse failures in approximately 7 out of 8 ATS tested in 2025.** Keep all critical content in a single-column flow.
- Text boxes (MS Word text boxes are invisible to many parsers).
- Tables for experience/education content (thin borders sometimes parse correctly, but it's fragile).
- Images of text (e.g., scanned letterhead, logo-as-text).
- Fancy dividers, icons, progress-bar skill ratings — they add noise and confuse parsers.
- Putting your phone/email exclusively in a page header or footer.

### Keyword mirroring — practical steps

1. Copy the job posting into a text file.
2. Identify the 10–15 skills, tools, and role-specific phrases that appear most (especially in "Requirements" and "Responsibilities").
3. For each one, check if the CV already contains it in any form.
4. Add the exact keyword where it naturally fits. Do not add keywords that are not genuinely part of your background — see §7.

### Keyword placement priority

For a genuinely-held must-have keyword, placement order matters for ATS scoring:

1. **Skills section first** — ATS NER (Named Entity Recognition) models weight a dedicated Skills section more heavily than the same term buried in a bullet. Place the keyword here.
2. **Reinforce in relevant bullets** — once it appears in Skills, weave it into the accomplishment bullet(s) where it actually featured. This reinforcement also serves the human reader.
3. **Summary / profile (optional)** — high-priority must-haves can appear in the summary too, but only if the summary naturally accommodates them; never force awkward keyword drops.

Do not scatter keywords across bullets only — the Skills section is the primary signal for ATS keyword recognition.

---

## 5. Length and Trimming

### Target lengths

| Career stage | Target |
|---|---|
| Student / 0–2 years | 1 page |
| 3–7 years | 1–2 pages |
| 8–15 years | 2 pages |
| 15+ years / senior / executive | 2 pages (3 only if roles are very distinct and all relevant) |
| Academic / research CV | No page limit; list all publications, grants, talks |

**US and Canada override this ladder: 1 page, a second only at 10+ years or
senior** (§2). The ladder is the default for every other market, and the two
disagreed for years 3–9 — a reader who found §5 first shipped a two-page US
résumé that §2 calls wrong. `scripts/check_pages.py` enforces the US/CA rule
from `meta.target_market`; `meta.max_pages` is the explicit exception.

### What to cut first (in this order)

1. **Roles older than 10–15 years** that add no unique signal. If you held 5 early jobs all with the same scope, condense to one line: "2003–2008: Various junior roles in X sector."
2. **Generic soft-skill filler:** "Excellent communicator", "Team player", "Results-oriented", "Passionate about technology" — these are assumed and waste space.
3. **Obvious tools for the level:** A senior engineer does not need to list "Microsoft Word", "Slack", "Email". Reserve the skills section for things that are a real filter for the role.
4. **Repetitive bullets:** If three roles all say "collaborated with cross-functional teams", keep the most quantified one and cut the others.
5. **Long objective statements** on junior CVs (replace with a targeted 2-sentence summary or cut entirely).
6. **Bullet points beyond 4–5 per role** for older positions. Recent role: up to 6. Role from 7+ years ago: 2–3 at most.

### Getting from 3 pages to 2

- Reduce margins to 0.6–0.75 in (not less — it looks cramped).
- Reduce font size to 10–10.5pt body, 11–12pt headings.
- Merge two thin bullets into one compound bullet.
- Drop the oldest role entirely or replace with a single-line entry.
- Remove the "References available on request" line.
- Remove the "Hobbies" section unless it is genuinely relevant to the role.

### Getting from 2 pages to 1 (junior/early career)

- Keep only the most relevant 2–3 bullets per role.
- Condense Education: one line per degree (no coursework list unless it's directly requested or you have no experience).
- Merge Skills into one compact section; drop any skill you could not speak to in an interview.
- Remove the summary if the space is tight and the target role is obvious.

---

## 6. Summary / Professional Profile Writing

### When to include

- **Include:** Senior candidates (5+ years), career-changers, roles where keyword injection in the summary increases ATS score, or anyone with an unconventional path that needs framing.
- **Skip:** Students applying for their first role (let the education and projects speak), people with a clearly linear path applying in the same field, when space is tight on a 1-pager.

### Structure (2–4 sentences)

```
Sentence 1: Role/identity + years of experience + domain
Sentence 2: 1–2 signature technical/domain strengths with concrete evidence
Sentence 3: One differentiator or notable outcome
Sentence 4 (optional): What you're targeting / the value you bring next
```

### Strong example

> Machine learning engineer with 7 years building production recommendation and ranking systems at scale (50M+ users). Specialise in two-tower retrieval models and real-time feature pipelines using Spark and Flink; shipped a CTR uplift that generated $4M incremental ARR in 2023. Seeking a senior IC role in a product-led ML team where close collaboration with growth and product is expected.

**Why it works:** Specific identity, concrete scale, two named technical areas, a quantified achievement, a clear target.

### Weak example

> Experienced software engineer with a passion for technology and a proven track record of success. Strong communicator who works well in teams and individually. Looking for an exciting opportunity to contribute and grow.

**Why it fails:** No domain, no numbers, no technologies named, entirely generic — could describe anyone. Every adjective ("experienced", "proven", "strong") needs evidence to mean anything.

---

## 7. Honest Reframing Only

**What is allowed:**

- Emphasising the most relevant experience for this specific role (ordering bullets by relevance, not strictly by time within a role).
- Reframing transferable skills with accurate language: "Managed a student project team of 5" is legitimate if you did.
- Using the job posting's terminology when it accurately describes what you did: if you "built CI/CD pipelines" and they call it "DevOps automation", you can use both.
- Surfacing contributions that were real but under-documented: a performance optimisation you drove is worth a bullet even if it was never formally acknowledged.
- Choosing which roles to omit (irrelevant short-term jobs need not appear).

**What is not allowed:**

- Inventing skills you do not have.
- Inflating a title (e.g. listing "Senior Engineer" when your contract says "Engineer II").
- Changing employment dates to hide a gap or shorten tenure.
- Claiming sole credit for team accomplishments you contributed to partially — use "Co-led", "Contributed to", or "Part of the team that…" as appropriate.
- Adding a keyword from the job posting that does not reflect genuine experience.

**Cross-reference:** See `gap-analysis.md` for detailed rules on how to handle skill gaps, experience gaps, and how to frame partial/adjacent experience honestly when tailoring for a specific posting.

### AI-generated uniformity — flag and fix

Identically-structured, voiceless bullets ("Spearheaded… Leveraged… Drove…" repeated across every role) read as machine-generated to experienced recruiters. After any AI-assisted rewrite, review the full CV for mechanical uniformity: stock verbs, parallel-but-hollow sentence structures, prose that is grammatically correct but has no personality. Vary sentence structure, mix bullet lengths, and preserve the candidate's real voice. Full treatment: see `motivation-letter.md §6` (AI-Authenticity section).

---

## 8. Links and Hyperlinks

A link on a CV should read as a **label**, not a URL. `Google Scholar` and `GitHub` are clean and instantly legible; `scholar.google.com/citations?user=YDMwxZwAAAAJ` is visual noise that makes the header look like a config file. The 2026 convention (enhancv, cv4me) is a friendly display label hyperlinked to the real URL.

- **In the profile YAML**, give each link under `contact.links` keyed by service (`scholar`, `github`, `linkedin`, `orcid`, `website`, `portfolio`, …). The renderer maps the key (or the URL's host) to a friendly label automatically. For anything unusual, write the value as `{label: "...", url: "..."}` to name it yourself.
- **The renderer handles display**: Markdown emits `[Google Scholar](url)`; LaTeX/PDF emits `\href{url}{Google Scholar}`; `.docx` emits a real clickable hyperlink whose visible text is the label. You do not hand-format links — keep the profile clean and let the renderer label them.
- **ATS robustness:** because the visible text is now a label, the URL no longer sits on the page as plain text. That is fine for the human-facing PDF and for any modern ATS (all of which read hyperlink targets), and the URL stays recoverable in the Markdown source and the docx hyperlink relationship. If a posting routes through a known-primitive plain-text parser, you can fall back to showing the bare readable URL (e.g. `linkedin.com/in/name`) — but default to labels.
- **Restraint:** two or three links in the header, maximum (LinkedIn + GitHub/Scholar + portfolio). More than that dilutes. No `bit.ly` shorteners — they look spammy and some filters flag them.

---

## 9. Projects vs. Experience — keep them distinct

A common self-inflicted weakness is a CV where the Experience section is full of project descriptions **and** there is a separate Projects section — the reader can't tell what's a job and what's a side effort, and the two sections compete. Draw the line cleanly:

- **Experience** = roles held at an organisation (employer, lab, internship, contract). Each entry has a title, an org, and dates. Work done *as part of that role* — even if it was a discrete "project" internally — belongs as **bullets under that role**, not as a separate Projects entry.
- **Projects** = standalone work **not** tied to an employment role: a master's thesis, a course project, a hackathon entry, an open-source library, a competition submission, a personal build. These have no employer, so they can't live under Experience.

**Rules when tailoring:**
- Never list the same body of work in both sections. If a "project" happened inside a job, fold it into that job's bullets and remove the duplicate.
- A Projects section earns its place only if it adds signal the Experience section doesn't — relevant, independent work the target role cares about. If it merely restates the day job or lists stale coursework, cut it; a tight CV with no Projects section beats a padded one.
- For early-career/student profiles with little work history, Projects can legitimately carry real weight (see §1) — there the section is load-bearing, not padding. Judge by what the target role needs.

## Post-tailoring AI-uniformity check

Run it after the last REFRAME and KEYWORD-INSERT edit, over the **full CV**. The check
itself (five dimensions, the 2026 vocabulary `lint_cv.py` reports as `AI_VOCABULARY`, and
why a clean lint run does not replace it) lives in one place: `references/gap-analysis.md`
§4, "Post-tailoring AI-uniformity check".
