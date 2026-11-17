# Role-Family Conventions (non-technical and regulated professions)

Most of this skill's defaults grew up around software/research hiring — Experience-first, a Skills block, metrics in every bullet, GitHub/publications as proof. That template quietly mis-serves the rest of the labour market. A nurse, a litigator, a sales director, an electrician, and a primary-school teacher each prove competence in a *different currency*, and each surfaces a different section first. This reference is the per-family adjustment: **what to lead with, what counts as evidence, and the concrete render recipe** so the CV reads the way a hiring manager in that field expects.

Read this when the target role is not a software/research/engineering job. It composes with everything else — `cv-craft.md` (format, length, region), `gap-analysis.md` (the qualitative-evidence note in §2 matters most here), `candidate-situations.md` (if the candidate is also a switcher, returner, etc.).

## The mechanism you'll use everywhere

The renderer already supports every ordering below — you don't need new sections, you re-sequence and relabel the ones that exist:

- **`meta.section_order`** — an explicit list wins over the auto-pick. Use it to surface what this family scans for first.
- **`meta.headings`** — relabel an existing section key for this profession. The most common move: rename `certifications` to the family's expected header, e.g. `headings: {certifications: "Licenses & Certifications"}` for clinical/legal/finance, or `headings: {projects: "Selected Matters"}` for law, `{projects: "Portfolio"}` for design. (Only the built-in section keys can be relabelled — see the renderer's `headings()`.)
- Put licences, registrations, and tickets in the `certifications` section (relabelled), because for regulated work they are a hard gate the screener checks *first*.

**Honest-only still governs everything.** Surface a real licence, never imply one not held; name a real quota or caseload, never invent one. The qualitative-evidence ladder in `gap-analysis.md §2` applies — for these families a concrete qualitative statement usually beats a manufactured percentage.

## Table of contents
1. Clinical / licensed healthcare (nursing, allied health, medicine)
2. Sales / business development
3. Skilled trades (electrician, plumber, HVAC, CDL driver, construction)
4. Legal
5. Finance / accounting
6. Public sector / government
7. Creative / design
8. Education / teaching
9. Hospitality / retail / service
10. A family not listed here

---

## 1. Clinical / licensed healthcare

**The currency:** an active licence/registration, then clinical scope and patient/unit outcomes. A recruiter or credentialing office confirms the licence *before* anything else — if it isn't near the top, the CV reads as a risk.

- **Lead with** a relabelled **Licenses & Certifications** section (RN/NMC/BIG registration with number + status, BLS/ACLS/PALS and expiry), then Experience, then Education. New grads: Education + Clinical Rotations rise above Experience.
- **Evidence is scope and outcome, not metrics:** unit type and bed count ("32-bed cardiac ICU"), patient acuity, shift leadership, EHR systems (Epic/Cerner), quality/safety results (infection-rate reduction, a Joint Commission / CQC rating), preceptor/charge roles. Don't force revenue-style numbers onto care work.
- **Recipe:** `section_order: [summary, certifications, experience, education, skills]`, `headings: {certifications: "Licenses & Certifications"}`.

## 2. Sales / business development

**The currency:** quota attainment and revenue, stated honestly. Sales CVs are the one non-engineering family that *is* intensely quantitative — lean into it where the numbers are real.

- **Lead with** a summary naming segment + deal size + a headline number, then Experience carrying quota/attainment per role.
- **Evidence:** quota attainment as a % ("achieved 142% of $2.4M quota, FY24"), ranking ("#2 of 38 reps"), President's Club, ramp time, ACV/ARR closed, logo wins, territory size, new-vs-expansion split. If a figure is confidential, give an honest band or a ranking rather than a fake precise number.
- **Recipe:** standard Experience-first order; keep Skills short (CRM/tooling like Salesforce, methodologies like MEDDIC/Challenger).

## 3. Skilled trades

**The currency:** tickets/cards, safety certifications, and hands-on scope. Often screened by a person or a simple form, not a heavyweight ATS — keep it clean and concrete.

- **Lead with** a relabelled **Licenses & Certifications** (trade licence/journeyman/master status, CSCS/OSHA/CDL class, equipment certs), then Experience.
- **Evidence:** project types and scale (commercial vs residential, voltage/systems worked, square footage, fleet/route), safety record, union/local status where relevant, equipment operated. Reliability and safety read as strongly as any number.
- **Recipe:** `section_order: [summary, certifications, experience, skills, education]`, `headings: {certifications: "Licenses & Certifications", skills: "Equipment & Skills"}`.

## 4. Legal

**The currency:** bar admission(s), practice area, and notable matters.

- **Lead with** Bar Admissions (jurisdiction + year + status) — put them in a relabelled `certifications` section near the top — then Experience, then a relabelled `projects` section as **Selected Matters** (deals/cases, anonymised as ethics require), then Education (law school + honours/journal/moot).
- **Evidence:** matter type and value/complexity, role on the matter, clerkships, publications for academic-track roles, languages for international practice. Cite outcomes honestly; never imply lead credit on a matter you supported.
- **Recipe:** `section_order: [summary, certifications, experience, projects, education]`, `headings: {certifications: "Bar Admissions", projects: "Selected Matters"}`.

## 5. Finance / accounting

**The currency:** professional designation (CPA, ACCA, CFA, Series 7/63) and quantified deal/portfolio work.

- **Lead with** designations in a relabelled `certifications` section (CFA Level/charter, CPA licence + state), then Experience with quantified scope.
- **Evidence:** AUM, deal sizes and count, P&L/budget owned, audit scope, modelling/systems (Bloomberg, SAP, advanced Excel/SQL), regulatory frameworks (GAAP/IFRS, SOX, Basel). This family is genuinely numeric — quantify, honestly.
- **Recipe:** `section_order: [summary, certifications, experience, education, skills]`, `headings: {certifications: "Licenses & Certifications"}` (or "Professional Designations").

## 6. Public sector / government

**The currency:** demonstrated competencies mapped to the posting, clearances, and process knowledge. **Many public-sector roles don't use a free CV at all** — they use a structured application form where you evidence each criterion. If the posting reads that way (numbered essential/desirable criteria, "Success Profiles", "behaviours"), switch to `structured-applications.md` — that document, not the CV, is the deliverable.

- For a CV-style public-sector role: **lead with** a summary, then Experience written against the role's competencies, surface security clearance level/status (an asset where required, omit where irrelevant), and policy/regulatory domains.
- **Evidence:** programme scale, budget, stakeholders/citizens served, statutory frameworks, named competencies demonstrated. Plain, specific, jargon-light.

## 7. Creative / design

**The currency:** the portfolio. The CV exists mainly to route the reader to the work.

- **Lead with** the portfolio link in the contact header (this is the one family where the link *is* the application), a short summary, then Experience, then a relabelled `projects` section as **Selected Work**.
- **Evidence:** shipped products and their reach/impact, named clients/brands, tools (Figma/Adobe CC), awards, the role you played in collaborative work (honestly — not sole credit for a team piece). For UX/product design, outcomes ("redesign lifted activation 18%") are fair when real.
- **Recipe:** `headings: {projects: "Selected Work"}`; keep it to 1–2 pages — the portfolio carries the depth.

## 8. Education / teaching

**The currency:** teaching credential/licence, levels and subjects taught, and student outcomes.

- **Lead with** a relabelled **Licenses & Certifications** (teaching licence/QTS, subject endorsements, grade bands), then Experience, then Education.
- **Evidence:** grade levels and subjects, class sizes, curriculum developed, measurable student progress where it genuinely exists (exam pass rates, value-added) but also concrete non-numeric outcomes (programmes founded, interventions led, inspection ratings). Don't manufacture a "+30% engagement" figure.
- **Recipe:** `section_order: [summary, certifications, experience, education, skills]`, `headings: {certifications: "Licenses & Certifications"}`.

## 9. Hospitality / retail / service

**The currency:** scope of operation run and reliability. Often screened in person or by a brief form.

- **Lead with** a summary, then Experience carrying operational scope.
- **Evidence:** covers/footfall served, team size supervised, venue type and revenue, certifications (food-safety/ServSafe, alcohol licence, first aid), languages for customer-facing roles, guest-satisfaction scores where real. "Wear many hats" is the job here, not a red flag.
- **Recipe:** standard Experience-first; short, concrete bullets; one page is usually right.

---

## 10. A family not listed here

Don't guess from the tech template. Ask one question that resolves the whole layout: **"In your field, what's the first thing a hiring manager looks for on a CV — a licence, a portfolio, a number, a named result?"** That answer tells you what to surface first and what the evidence currency is. Then apply the same two mechanisms — `section_order` to lead with it, `headings` to label sections in the field's own words — and fall back to the conservative reverse-chronological default for everything else.
