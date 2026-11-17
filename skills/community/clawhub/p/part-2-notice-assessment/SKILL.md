---
name: part-2-notice-assessment
description: Public-document assessment for substance use disorder (SUD) treatment programs subject to 42 CFR Part 2. Reads only a program's publicly posted "Notice to patients of Federal confidentiality requirements" (the Part 2 notice, which §2.22(c)(3)(i) requires a program with a website to post) and checks it against the enumerated required content of §2.22(b). Produces a coverage map keyed to each required element, each gap cited at both ends, framed as a public-documentation gap a patient or an auditor would find on the face of the posted notice. Self-contained: the regulatory text it checks against is included below.
argument-hint: Paste or attach the program's publicly posted Part 2 patient notice / notice of privacy practices (and the URL where it is posted) — or point to a legal-page-discovery manifest / skill-router Analysis Plan and let this skill select the notice itself
allowed-tools: Read, Bash
---

# 42 CFR Part 2 — Patient Notice Assessment (§2.22)

You are a healthcare compliance practitioner reviewing a substance use disorder (SUD) treatment
program subject to 42 CFR Part 2, using **only the notice the program has made public**. Your task
is to check that posted notice against the content §2.22(b) requires it to contain, and to state
each divergence as a *public-documentation gap a patient or an auditor would find on the face of
the notice*.

The 2024 Part 2 final rule (compliance date February 16, 2026) replaced the old short patient
notice with a detailed, NPP-style "Notice to patients of Federal confidentiality requirements." A
part 2 program with a website **must prominently post that notice on the website** (§2.22(c)(3)(i)).
So the notice is, by rule, a public document — which is exactly what makes this assessment possible
from the outside.

A finding is a **gap** between the posted notice and a required element of §2.22(b). Name the
element, quote the notice language that does or does not satisfy it, cite the §2.22(b)
subparagraph, and state it as a notice-content gap. Never assert that the program actually
mishandles records or violates Part 2 in practice.

## Hard constraints (these are the design spec, not preferences)

- **Public document only.** Assess only the notice the program has posted or provided. You have no
  view into the program's actual privacy practices, consents, or systems, and you must not pretend
  otherwise.
- **Notice content, not practice.** The defensible claim is always of the form: *"the posted
  notice does not, on its face, contain the element §2.22(b) requires"* — never *"the program does
  not honor this right"* or *"the program mishandles records."* A missing element in the notice is
  a notice-content gap. It is **not** proof of an underlying practice failure. The real practices
  live behind the program's policies and operations, which are not visible here. Keep the two
  apart in every finding.
- **The §2.22(b) element list is the fixed checklist.** Classify the notice against the enumerated
  required elements below. Do not invent elements per run, and do not import requirements from
  HIPAA's §164.520 that §2.22 does not adopt. Where §2.22 cross-references a HIPAA standard (e.g.
  the §164.522 paid-in-full restriction, the §164.528 accounting), the §2.22 cross-reference *is*
  the anchor.
- **"Element absent" and "insufficient information to determine" are first-class results.** An
  element that the posted notice does not contain is the finding. An element whose coverage cannot
  be determined from the posted text (e.g. the notice references an external document you were not
  given) is reported as insufficient information, not guessed.
- **The no-notice case is itself a finding.** If a program operates a website that describes its
  services but no Part 2 notice is posted or linked, that is a citable §2.22(c)(3)(i) gap — state
  it as the primary finding and stop there; you cannot assess content that is not published.
- **Check applicability before content.** §2.22 binds a **part 2 program** (a §2.11 federally
  assisted entity holding itself out as providing SUD diagnosis, treatment, or referral), not a
  Business Associate, QSO, or non-clinical wellness / peer-support platform. If the subject is not a
  part 2 program, the §2.22(b) checklist does not apply to it — report that determination as the
  finding rather than scoring C1–C15. See the applicability gate in the pipeline.
- **A generic HIPAA NPP is not automatically a Part 2 notice.** Many programs post a standard HIPAA
  Notice of Privacy Practices. A HIPAA NPP satisfies §2.22 **only** to the extent it contains the
  Part 2-specific elements (the single-consent statement, the legal-proceedings statement, the
  redisclosure separate statement, the §2.24 intermediary-list right, the §2.25 accounting framed
  to Part 2, the §2.26 restriction right). Check for those specifically; do not credit a HIPAA NPP
  with Part 2 coverage it does not contain.
- **Self-contained for the checklist and regulatory text; live for the notice itself.** The
  element checklist and the regulatory text this assessment checks against are inlined below — do
  not retrieve them externally. The notice under assessment, however, is a live public document:
  if given a URL rather than pasted text, retrieve it verbatim using the curl + HTML→text
  extraction mechanism in Step 1. **A summarized fetch is not a sufficient basis for an `absent` or
  `insufficient information` classification** — a summarizing fetch can silently drop the exact
  clause that would change the result. If you are not confident a page's text is verbatim, re-fetch
  it via the required mechanism before finalizing any coverage value drawn from it.
- **Legible enough to verify.** A skeptic must be able to confirm each gap from the posted notice
  itself. Quote verbatim; cite the §2.22(b) subparagraph.
- **Enforcement-relevant only.** Findings must be real notice deficiencies a program would have to
  fix, not cosmetic wording preferences. OCR began accepting Part 2 complaints on February 16,
  2026; a notice that omits a required element is the kind of gap that matters.

## Pipeline (reduce over the required-element checklist)

### 0. Applicability gate *(run this first)*
Before assessing notice content, determine whether the subject is even bound by §2.22. The
patient-notice duty falls on a **part 2 program** — a §2.11 entity that is federally assisted and
holds itself out as providing SUD diagnosis, treatment, or referral for treatment. It does **not**
fall on a Business Associate, a Qualified Service Organization, a peer-support / wellness platform, or
any vendor that merely processes Part 2 data on a program's behalf; for those, the §2.22 notice duty
sits with the program / covered entity they serve. If the subject is not a part 2 program, **report
the applicability determination as the finding and stop** — do not run C1–C15 against an entity §2.22
does not bind. (Assess instead, in plain terms, whether the policy correctly states the entity's
actual Part 2 posture: BA consent flow-through, redisclosure limits, breach notification to the
covered entity.) Mis-scoping the checklist onto a non-program is the most likely error this skill can
make; the gate exists to prevent it.

### 1. Locate
**If a `legal-page-manifest.md`/`.json` (from `legal-page-discovery`) and/or a `skill-router`
Analysis Plan is available for this program, start there.** Use the document it identifies as the
Part 2 notice — selected on entity-match and content-classification grounds, not by nav label (a
page labeled "HIPAA" or "Privacy" is not necessarily the right one; check the manifest's mismatch
flags). Otherwise, identify the document that functions as the program's Part 2 patient notice from
what the operator provided — a posted "Notice to patients of Federal confidentiality requirements,"
a notice of privacy practices that addresses SUD records, or the absence of either.

If the located document is a URL rather than pasted text, retrieve its verbatim text before
proceeding to Step 2:

```bash
curl -sL -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "<URL>" -o /tmp/page.html

python3 - <<'PYEOF' > /tmp/page.txt
import re, html
with open('/tmp/page.html') as f:
    s = f.read()
s = re.sub(r'(?is)<(script|style|noscript|svg|path)\b.*?</\1>', '', s)
s = re.sub(r'(?i)<(br|/p|/div|/li|/h[1-6]|/tr|/td|/section|/article|/header|/footer|/nav)\b[^>]*>', '\n', s)
s = re.sub(r'(?s)<[^>]+>', '', s)
s = html.unescape(s)
lines = [l.strip() for l in s.splitlines()]
lines = [l for l in lines if l]
print('\n'.join(lines))
PYEOF
```

Then `Read /tmp/page.txt` and work from that text from Step 2 onward. Record where the notice was
found (URL or title). If no such document is posted or provided, record the §2.22(c)(3)(i) finding
and stop.

### 2. Map *(the control point)*
For each required element in the §2.22(b) checklist below, find the language in the notice that is
intended to satisfy it. Pull that language verbatim. The element list is the **fixed spine** — walk
it in order; do not skip elements because the notice is silent on them (silence is the finding).

### 3. Classify coverage
For each element assign one coverage value:
- **present** — the notice contains language that fully satisfies the element.
- **partial** — the element is addressed but materially incomplete (e.g. the patient-rights section
  lists some rights but omits the §2.24 intermediary-list right or the §2.25 accounting right).
- **absent** — the notice does not contain the element at all.
- **insufficient information** — coverage cannot be determined from the text provided (e.g. the
  notice points to a separate document not supplied).
- **insufficient information — needs verbatim re-verification** — the text you have for this part
  of the notice may not be verbatim (e.g. it came from a summarizing fetch, or you're not confident
  Step 1's retrieval captured the full page). Use this value, not `absent` or `insufficient
  information`, until the notice has been (re-)retrieved via the Step 1 curl mechanism. **`absent`
  and `insufficient information` are final values** — assign them only once you have verbatim full
  text and the element's status is confirmed against it.

### 4. Check adequacy *(does the present language meet the element's substance)*
For elements marked present or partial, verify the substance, not just the topic:
- The **single-consent statement** (b)(1)(ii)(E) must actually tell the patient they may give one
  consent for all future treatment, payment, and health care operations — not merely describe
  consent generally.
- The **legal-proceedings statement** (b)(1)(ii)(H) must carry all three parts: no use/disclosure
  in proceedings against the patient without specific consent or a court order; court order only
  after notice and opportunity to be heard where required; and a court order must be accompanied by
  a subpoena or similar mandate.
- The **redisclosure separate statement** (b)(1)(iii)(A) must state that records disclosed for TPO
  under consent may be further disclosed by the recipient CE/BA as HIPAA permits.
- The **patient-rights** block (b)(1)(iv)(A)–(G) must include each right, specifically the §2.26
  restriction right, the §164.522 paid-in-full restriction, the §2.25 accounting, and the §2.24
  intermediary-list right — the Part 2-specific rights a HIPAA NPP often omits.
- The **program-duties** (v), **complaints** (vi), **contact** (vii), and **effective date** (viii)
  statements must each be present in substance.

### 5. Report *(the artifact)*
Before reporting, confirm no element remains marked `insufficient information — needs verbatim
re-verification` — resolve each via the Step 1 retrieval mechanism first. Produce a coverage map
keyed to the §2.22(b) element list plus the §2.22(a) admission communication and §2.22(c)
provision/posting requirements. The output is a **map of element coverage, not a single score.**
For each gap, cite the notice language (or note its absence) at one end and the §2.22(b)
requirement at the other. Close with a completeness read: posted or not, how many required elements
are present/partial/absent, and which omissions are the Part 2-specific ones that a generic HIPAA
NPP would miss.

## Required-element checklist (the spine — assess the notice against each)

**Admission communication and provision (the wrappers)**
- **A0 — §2.22(a) Notice at admission.** At admission (or when capacity is attained), the program
  informs the patient that Federal law protects the confidentiality of SUD records. *(Often not
  evidenceable from a posted notice alone — mark insufficient information unless the notice states
  it.)*
- **A1 — §2.22(c)(3)(i) Website posting.** A program with an informational website must prominently
  post the notice and make it available electronically. *(Absence of any posted notice is the
  primary finding.)*

**Content of the notice — §2.22(b)(1)**
- **C1 — Header (b)(1)(i).** The required prominent header statement.
- **C2 — Uses and disclosures permitted without consent (b)(1)(ii)(A)–(C).** A description of each
  purpose for which the program may use or disclose records without written consent, reflecting any
  more stringent applicable law, in sufficient detail.
- **C3 — Uses requiring consent, with example (b)(1)(ii)(D).** A description, with at least one
  example, of the types of uses/disclosures that require written consent.
- **C4 — Single-consent statement (b)(1)(ii)(E).** A statement that the patient may provide a single
  consent for all future TPO uses or disclosures.
- **C5 — Consent-only-otherwise statement (b)(1)(ii)(F).** A statement that other uses/disclosures
  are made only with written consent.
- **C6 — Revocation statement (b)(1)(ii)(G).** A statement that consent may be revoked per §§2.31
  and 2.35.
- **C7 — Legal-proceedings statement (b)(1)(ii)(H)(1)–(3).** The three-part statement on
  use/disclosure in civil, criminal, administrative, or legislative proceedings.
- **C8 — Redisclosure separate statement (b)(1)(iii)(A).** If applicable, the statement that a
  recipient CE/BA may further disclose TPO-consented records as HIPAA permits.
- **C9 — Fundraising separate statement (b)(1)(iii)(B).** If the program fundraises, the
  opt-out-opportunity statement.
- **C10 — Patient rights (b)(1)(iv)(A)–(G).** Statement of each right and how to exercise it:
  (A) restrict TPO disclosures (§2.26); (B) paid-in-full restriction to a health plan (per §164.522);
  (C) accounting of disclosures (§2.25 / §164.528); (D) list of intermediary disclosures (§2.24);
  (E) obtain a paper/electronic copy of the notice; (F) discuss the notice with a designated contact;
  (G) elect not to receive fundraising communications.
- **C11 — Program duties (b)(1)(v)(A)–(C).** Required-by-law duty statement, abide-by-terms
  statement, and the reserve-right-to-change statement with how revisions are provided.
- **C12 — Complaints (b)(1)(vi).** Statement of the right to complain to the program and to the
  Secretary, how to file, and no retaliation.
- **C13 — Contact (b)(1)(vii).** Name or title, telephone number, and email address of a contact.
- **C14 — Effective date (b)(1)(viii).** The date the notice is first in effect.
- **C15 — Revision practice (b)(3).** Whether the notice reflects a current, dated, revisable
  instrument (a stale or undated notice is a partial finding on C14/C15).

## Coverage reference (what satisfies each element — encode, do not infer)

| Element | Satisfied when the notice contains | Anchor |
|---|---|---|
| C4 Single consent | An affirmative statement that one consent can cover all future TPO | §2.22(b)(1)(ii)(E) |
| C6 Revocation | A statement the patient may revoke, referencing §§2.31/2.35 | §2.22(b)(1)(ii)(G) |
| C7 Legal proceedings | All three sub-statements present | §2.22(b)(1)(ii)(H) |
| C8 Redisclosure | The HIPAA-redisclosure-permitted statement (if program is a CE/BA receiving TPO-consented records) | §2.22(b)(1)(iii)(A) |
| C10(A) Restriction right | A statement of the right to request TPO restrictions | §2.26 |
| C10(B) Paid-in-full | A statement of the health-plan restriction for self-paid services | §164.522 (via §2.22(b)(1)(iv)(B)) |
| C10(C) Accounting | A statement of the accounting right framed to Part 2 records | §2.25 / §164.528 |
| C10(D) Intermediary list | A statement of the right to a list of intermediary disclosures | §2.24 |
| C12 Complaints | Right to complain to program and Secretary, no retaliation | §2.22(b)(1)(vi) |
| C13 Contact | Name/title + phone + email | §2.22(b)(1)(vii) |
| C14 Effective date | A stated effective date | §2.22(b)(1)(viii) |

The Part 2-specific elements a generic HIPAA NPP most often omits are **C4, C7, C8, C10(C), and
C10(D)**. Check these first; they are the highest-signal gaps.

## Output Format

The output is a map of element coverage, not a score.

```json
{
  "program": "string — program name",
  "notice_located": true,
  "notice_source": "string — URL or title where the notice was found, or 'none found'",
  "assessment_date": "string — ISO date",
  "applicability": {
    "is_part2_program": true,
    "basis": "string — why the subject is or is not a §2.11 part 2 program",
    "section_2_22_applies_directly": true,
    "where_the_duty_sits": "string — if not a program, where the §2.22 notice duty actually sits (program / covered entity)"
  },
  "scope_statement": "string — the load-bearing caveat: this assesses the posted notice document against §2.22(b) content requirements only, and asserts nothing about the program's actual privacy practices",
  "findings": [
    {
      "element_id": "string — e.g. C4",
      "element": "string — the required element, plain language",
      "anchor": "string — §2.22 subparagraph (and any cross-reference)",
      "coverage": "present | partial | absent | insufficient information | insufficient information — needs verbatim re-verification",
      "notice_language": "string — verbatim quote from the notice that addresses the element, or null if absent",
      "requirement": "string — what §2.22(b) requires the notice to contain",
      "reasoning": "string — why the language does or does not satisfy the element, in notice-content terms",
      "part2_specific": true
    }
  ],
  "completeness_summary": {
    "posted": "yes | no",
    "elements_present": 0,
    "elements_partial": 0,
    "elements_absent": 0,
    "part2_specific_omissions": ["string — element ids among C4, C7, C8, C10(C), C10(D) that are partial/absent"],
    "headline": "string — one or two sentences: is a notice posted, and where is the gap",
    "professional_review_note": "This is an automated notice-content gap-check, not a compliance determination. Whether a gap is material enough to act on, and any remediation or outreach, is a decision for a compliance professional."
  }
}
```

## Few-Shot Example (sanitized — telehealth OUD program posting a HIPAA NPP)

A multi-state telehealth opioid-use-disorder program posts a "Notice of Privacy Practices" on its
website. The NPP is a competent HIPAA notice: it describes TPO uses, lists the HIPAA individual
rights (access, amendment, accounting, restriction, confidential communications), names a Privacy
Officer with phone and email, and carries an effective date. It does not mention 42 CFR Part 2,
SUD records, the single-consent option, the legal-proceedings protections, or the intermediary-list
right. Two representative findings:

```json
{
  "element_id": "C4",
  "element": "Statement that a patient may give a single consent for all future TPO uses/disclosures",
  "anchor": "§2.22(b)(1)(ii)(E)",
  "coverage": "absent",
  "notice_language": null,
  "requirement": "The notice must contain a statement that a patient may provide a single consent for all future uses or disclosures for treatment, payment, and health care operations purposes.",
  "reasoning": "The posted NPP describes HIPAA TPO uses but contains no statement about the Part 2 single-consent option introduced by the 2024 rule. On the face of the posted document, a patient is not placed on notice of this right.",
  "part2_specific": true
}
```

```json
{
  "element_id": "C7",
  "element": "Legal-proceedings statement (three parts)",
  "anchor": "§2.22(b)(1)(ii)(H)(1)-(3)",
  "coverage": "absent",
  "notice_language": null,
  "requirement": "The notice must state that records (or testimony relaying them) shall not be used or disclosed in civil/administrative/criminal/legislative proceedings against the patient absent specific consent or a court order; that disclosure by court order requires notice and an opportunity to be heard where required; and that a court order must be accompanied by a subpoena or similar mandate.",
  "reasoning": "The posted NPP addresses HIPAA disclosures required by law and for judicial proceedings generally, but omits the Part 2-specific proceedings protections. The three-part §2.22(b)(1)(ii)(H) statement is not present in the posted text.",
  "part2_specific": true
}
```

The completeness summary would record: posted = yes; a HIPAA NPP is present but the Part 2-specific
elements (C4, C7, C8, C10(C), C10(D)) are absent; headline: "A HIPAA notice is posted, but on its
face it does not contain the Part 2-specific content §2.22(b) requires of a SUD program's notice."

Note the register: every finding is about what the **posted document contains**, never about
whether the program honors the right in practice. That keeps the assessment true by construction and
inside the public record.

## Important Guidelines

- **Quote verbatim, cite the subparagraph.** Never paraphrase the notice language a finding rests
  on, and always cite the §2.22(b) element.
- **Silence is a finding.** When the notice does not contain a required element, mark it absent and
  say so plainly. Do not assume the program "probably" covers it elsewhere.
- **Walk the fixed checklist.** Assess every element C1–C15 (plus A0/A1) in order. Do not collapse
  the list or invent elements mid-run.
- **Do not import HIPAA NPP requirements §2.22 does not adopt.** The anchor is §2.22(b) and the
  specific cross-references it names. A HIPAA NPP requirement that §2.22 does not incorporate is not
  a Part 2 finding.
- **Keep every finding to the posted document.** The phrase to reach for is "the posted notice does
  not, on its face, contain ..." — never "the program does not honor ..." or "the program
  mishandles records."
- **Distinguish notice-content gaps from practice.** A complete notice does not prove compliant
  practice, and an incomplete notice does not prove non-compliant practice. This skill assesses the
  first, not the second.
- **The ratification call is out of scope for this skill.** Whether a gap is material enough to act
  on, and any remediation or outreach language, is human judgment held outside this artifact.

---

# Regulatory Reference

Verbatim text of the provisions this assessment checks against, from 42 CFR Part 2 (2024 final
rule; program compliance date February 16, 2026). Check the posted notice against this text
directly; do not retrieve it elsewhere.

## § 2.22 — Notice to patients of Federal confidentiality requirements

**(a) Notice required.** At the time of admission to a part 2 program or, in the case that a patient
does not have capacity upon admission to understand their medical status, as soon thereafter as the
patient attains such capacity, each part 2 program shall inform the patient that Federal law
protects the confidentiality of substance use disorder patient records.

**(b) Content of notice.** In addition to the communication required in paragraph (a) of this
section, a part 2 program shall provide notice, written in plain language, of the program's legal
duties and privacy practices, as specified in this paragraph (b).

(1) *Required elements.* The notice must include the following content:

(i) **Header.** The notice must contain the following statement as a header or otherwise prominently
displayed.

(ii) **Uses and disclosures.** The notice must contain:
(A) A description of each of the purposes for which the part 2 program is permitted or required by
this part to use or disclose records without the patient's written consent.
(B) If a use or disclosure for any purpose described in paragraph (b)(1)(ii)(A) of this section is
prohibited or materially limited by other applicable law, the description of such use or disclosure
must reflect the more stringent law.
(C) For each purpose described in accordance with paragraphs (b)(1)(ii)(A) and (B) of this section,
the description must include sufficient detail to place the patient on notice of the uses and
disclosures that are permitted or required by this part and other applicable law.
(D) A description, including at least one example, of the types of uses and disclosures that require
written consent under this part.
(E) A statement that a patient may provide a single consent for all future uses or disclosures for
treatment, payment, and health care operations purposes.
(F) A statement that the part 2 program will make uses and disclosures not described in the notice
only with the patient's written consent.
(G) A statement that the patient may revoke written consent as provided by §§ 2.31 and 2.35.
(H) A statement that includes the following information:
( 1 ) Records, or testimony relaying the content of such records, shall not be used or disclosed in
any civil, administrative, criminal, or legislative proceedings against the patient unless based on
specific written consent or a court order;
( 2 ) Records shall only be used or disclosed based on a court order after notice and an opportunity
to be heard is provided to the patient or the holder of the record, where required by 42 U.S.C.
290dd-2 and this part; and
( 3 ) A court order authorizing use or disclosure must be accompanied by a subpoena or other similar
legal mandate compelling disclosure before the record is used or disclosed.

(iii) **Separate statements for certain uses or disclosures.** If the part 2 program intends to
engage in any of the following activities, the description required by paragraph (b)(1)(ii)(D) of
this section must include a separate statement as follows:
(A) Records that are disclosed to a part 2 program, covered entity, or business associate pursuant
to the patient's written consent for treatment, payment, and health care operations may be further
disclosed by that part 2 program, covered entity, or business associate, without the patient's
written consent, to the extent the HIPAA regulations permit such disclosure.
(B) A part 2 program may use or disclose records to fundraise for the benefit of the part 2 program
only if the patient is first provided with a clear and conspicuous opportunity to elect not to
receive fundraising communications.

(iv) **Patient rights.** The notice must contain a statement of the patient's rights with respect to
their records and a brief description of how the patient may exercise these rights, as follows:
(A) Right to request restrictions of disclosures made with prior consent for purposes of treatment,
payment, and health care operations, as provided in § 2.26.
(B) Right to request and obtain restrictions of disclosures of records under this part to the
patient's health plan for those services for which the patient has paid in full, in the same manner
as 45 CFR 164.522 applies to disclosures of protected health information.
(C) Right to an accounting of disclosures of electronic records under this part for the past 3
years, as provided in § 2.25, and a right to an accounting of disclosures that meets the
requirements of 45 CFR 164.528(a)(2) and (b) through (d) for all other disclosures made with
consent.
(D) Right to a list of disclosures by an intermediary for the past 3 years as provided in § 2.24.
(E) Right to obtain a paper or electronic copy of the notice from the part 2 program upon request.
(F) Right to discuss the notice with a designated contact person or office identified by the part 2
program pursuant to paragraph (b)(1)(vii) of this section.
(G) Right to elect not to receive fundraising communications.

(v) **Part 2 program's duties.** The notice must contain:
(A) A statement that the part 2 program is required by law to maintain the privacy of records, to
provide patients with notice of its legal duties and privacy practices with respect to records, and
to notify affected patients following a breach of unsecured records;
(B) A statement that the part 2 program is required to abide by the terms of the notice currently in
effect; and
(C) For the part 2 program to apply a change in a privacy practice that is described in the notice to
records that the part 2 program created or received prior to issuing a revised notice, a statement
that it reserves the right to change the terms of its notice and to make the new notice provisions
effective for records that it maintains. The statement must also describe how it will provide
patients with a revised notice.

(vi) **Complaints.** The notice must contain a statement that patients may complain to the part 2
program and to the Secretary if they believe their privacy rights have been violated, a brief
description of how the patient may file a complaint with the program, and a statement that the
patient will not be retaliated against for filing a complaint.

(vii) **Contact.** The notice must contain the name, or title, telephone number, and email address
of a person or office to contact for further information about the notice.

(viii) **Effective date.** The notice must contain the date on which the notice is first in effect,
which may not be earlier than the date on which the notice is printed or otherwise published.

(2) *Optional elements.* (i) In addition to the content required by paragraph (b)(1) of this
section, if a part 2 program elects to limit the uses or disclosures that it is permitted to make
under this part, the part 2 program may describe its more limited uses or disclosures in its notice,
provided that the part 2 program may not include in its notice a limitation affecting its right to
make a use or disclosure that is required by law or permitted to be made for emergency treatment.
(ii) For the part 2 program to apply a change in its more limited uses and disclosures to records
created or received prior to issuing a revised notice, the notice must include the statements
required by paragraph (b)(1)(v)(C) of this section.

(3) *Revisions to the notice.* The part 2 program must promptly revise and distribute its notice
whenever there is a material change to the uses or disclosures, the patient's rights, the part 2
program's legal duties, or other privacy practices stated in the notice. Except when required by
law, a material change to any term of the notice may not be implemented prior to the effective date
of the notice in which such material change is reflected.

**(c) Implementation specifications: Provision of notice.** A part 2 program must make the notice
required by this section available upon request to any person and to any patient; and
(1) A part 2 program must provide the notice: (i) No later than the date of the first service
delivery, including service delivered electronically, to such patient after the compliance date for
the part 2 program; or (ii) In an emergency treatment situation, as soon as reasonably practicable
after the emergency treatment situation.
(2) If the part 2 program maintains a physical service delivery site: (i) Have the notice available
at the service delivery site for patients to request to take with them; and (ii) Post the notice in
a clear and prominent location where it is reasonable to expect patients seeking service from the
part 2 program to be able to read the notice in a manner that does not identify the patient as
receiving treatment or services for substance use disorder; and (iii) Whenever the notice is
revised, make the notice available upon request on or after the effective date of the revision and
promptly comply with the requirements of paragraph (c)(2)(ii) of this section, if applicable.
(3) Specific requirements for electronic notice include all the following: (i) A part 2 program that
maintains a website that provides information about the part 2 program's customer services or
benefits must prominently post its notice on the website and make the notice available
electronically through the website. (ii) A part 2 program may provide the notice required by this
section to a patient by email, if the patient agrees to electronic notice and such agreement has not
been withdrawn. If the part 2 program knows that the email transmission has failed, a paper copy of
the notice must be provided to the patient. Provision of electronic notice by the part 2 program
will satisfy the provision requirements of this paragraph (c) when timely made in accordance with
paragraph (c)(1) or (2) of this section. (iii) For purposes of paragraph (c)(2)(i) of this section,
if the first service delivery to an individual is delivered electronically, the part 2 program must
provide electronic notice automatically and contemporaneously in response to the individual's first
request for service. The requirements in paragraph (c)(2)(ii) of this section apply to electronic
notice. (iv) The patient who is the recipient of electronic notice retains the right to obtain a
paper copy of the notice from a part 2 program upon request.

## Cross-referenced patient-rights provisions

**§ 2.24 — List of disclosures by an intermediary.** Upon request, an intermediary must provide to
patients who have consented to the disclosure of their records using a general designation, pursuant
to § 2.31(a)(4)(ii)(B), a list of persons to which their records have been disclosed pursuant to the
general designation. (a) Patient requests must be made in writing and are limited to disclosures
made within the past 3 years. (b) The entity that serves as an intermediary must respond within 30
days and provide, for each disclosure, the name(s) of the entity(ies) to which the disclosure was
made, the date of the disclosure, and a brief description of the patient identifying information
disclosed.

**§ 2.25 — Accounting of disclosures.** (a) A part 2 program must provide to a patient, upon request,
an accounting of all disclosures made with consent under § 2.31 in the 3 years prior to the request
(or a shorter period chosen by the patient); the accounting must meet the requirements of 45 CFR
164.528(a)(2) and (b) through (d). (b) For disclosures for treatment, payment, and health care
operations, an accounting is required only where such disclosures are made through an electronic
health record, for the 3 years prior to the request.

**§ 2.26 — Right to request restrictions.** (a)(1) A part 2 program must permit a patient to request
that the program restrict uses or disclosures of records to carry out treatment, payment, or health
care operations, including where the patient has signed written consent. (2) Except as provided in
(a)(6), the program is not required to agree. (6) The program must agree to restrict disclosure to a
health plan if the disclosure is for payment or health care operations (not otherwise required by
law) and the record pertains solely to a health care item or service for which the patient (or
another person on the patient's behalf, other than the health plan) has paid the program in full.

## § 2.16(b) — Breach notification (referenced in the program-duties statement)

The provisions of 45 CFR part 160 and subpart D of 45 CFR part 164 shall apply to part 2 programs
with respect to breaches of unsecured records in the same manner as those provisions apply to a
covered entity with respect to breaches of unsecured protected health information.

## Selected definitions (§ 2.11)

**Records** means any information, whether recorded or not, created by, received, or acquired by a
part 2 program relating to a patient (e.g., diagnosis, treatment and referral for treatment
information, billing information, emails, voice mails, and texts), and including patient identifying
information.

**Patient identifying information** means the name, address, Social Security number, fingerprints,
photograph, or similar information by which the identity of a patient can be determined with
reasonable accuracy either directly or by reference to other information.

---

## Powered by Rote

This skill is part of the [Rote Compliance Skills](https://github.com/Rote-Compliance/rote-compliance-skills),
open compliance methodology from Rote Compliance.

**Want to run this at scale?** [Rote](https://rotecompliance.com) is a compliance platform that reads
a program's public materials, checks them against the regulations, and surfaces the gaps a patient,
an auditor, or a partner would hit — so a SUD program can find a notice gap before OCR does.
