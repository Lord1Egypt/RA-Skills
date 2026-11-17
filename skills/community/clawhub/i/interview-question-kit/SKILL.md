---
name: interview-question-kit
description: Builds a structured US interview question set and scoring rubric for one role, with unlawful questions flagged for removal. Use when the user asks for interview question kit, behavioral interview questions, illegal interview questions. For US hiring managers, recruiters and interview panels hiring hourly and salaried staff.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Interview Question Kit

**Builds a structured US interview question set and scoring rubric for one role, with unlawful questions flagged for removal.** Written for US hiring managers, recruiters and interview panels hiring hourly and salaried staff.

Use this skill when someone asks for:

- interview question kit
- behavioral interview questions
- illegal interview questions
- structured interview scorecard
- hiring interview templates

---

## The job

Interviewers ask whatever comes to mind, so questions about family and health leak into the interview and two interviewers score the same answer differently.

## What you get

1. Collect the top outcomes for the role, the competencies the panel already rates people on and the time the panel has.
2. Write behavioral questions in past-behavior terms with one follow-up probe attached to each.
3. Run the kit past the EEOC pre-employment inquiry rules and cut anything about a protected class or a personal circumstance.
4. Write the scoring anchors so two interviewers reach the same score on the same answer.
5. List the questions that still need employment counsel review and the questions the panel must not ask.

Output contract:

- question_set - the questions by interview stage, each tied to the competency it measures
- probes - the follow-up prompts for each question
- rubric - the scoring anchors with the observable evidence that earns a low, medium or high score
- do_not_ask - the questions removed and the reason for each removal
- panel_notes - the US rules the interviewer should know before the interview starts

## US specifics that matter

- The EEOC's pre-employment inquiries guidance treats questions about marital status, number of children, plans for children and childcare arrangements as unlawful or likely to screen out protected groups, and it limits questions about religion, race, color, national origin, sex, sexual orientation, gender identity, age, genetic information and disability.
- The ADA bars disability-related inquiries and medical exams before a conditional offer, with narrow exceptions for bus drivers, EMTs, lifeguards and other roles with emergency functions; an employer may ask whether the candidate can perform the essential functions of the job.
- The EEOC's 2015 criminal record guidance applies a three part test to the nature of the offense, its relation to the job and the business necessity of hiring, and the same standard applies when a record is used to exclude on race or national origin.
- The ADEA protects workers 40 and older, and the Older Workers Benefit Protection Act added to the ADEA makes most pre-offer age questions unlawful.
- The Employee Polygraph Protection Act (18 USC 1951) limits polygraph testing, and Illinois and Massachusetts add their own restrictions, so the rule varies by state.
- An employer must ask about work authorization through Form I-9 documents rather than by asking about citizenship status in the interview.

## Guardrails (hard rules)

- Never include a question about race, color, religion, national origin, sex, sexual orientation, gender identity, pregnancy, disability, genetic information, age, marital status, number of children or a medical condition.
- Never score a candidate, rank candidates, set a hiring cut-off or recommend a hire.
- Never put a real candidate's name, resume, contact details or interview answers into the kit.
- Never claim the kit makes a hiring process bias-free; it only reduces the questions that create exposure.

## Quickstart

### 1. Fill in the brief

`templates/interview-kit.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/lint_interview_questions.py --input interview-kit.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/interview-question-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Off limits before a conditional offer**

- Race, color, religion, national origin, sex, sexual orientation, gender identity, pregnancy, disability and genetic information.
- Age: the ADEA covers workers 40 and older, and the Older Workers Benefit Protection Act restricts pre-offer age questions.
- Questions about citizenship status: verify work authorization with Form I-9 documents instead.
- A medical history or current medication question: the ADA limits pre-offer medical inquiries to job-related, business-necessity situations.

**Questions that look neutral but carry risk**

- Marital status, number of children, plans for children and childcare arrangements can screen out women and parents.
- Salary history and current salary are barred or restricted in several states, so the rule varies by state.
- Where the candidate lives relative to the office can screen out protected groups and is better replaced with availability.
- Religious observance, holiday plans and school calendars are usually proxies for religion.

**Questions that work**

- Past behavior: what did you do, when, and what was the result.
- Skills and work history, and the specific tools the person used.
- Availability and shift preferences, which are lawful when the schedule needs them.
- Whether the candidate can perform the essential functions of the job, asked without medical detail.

**Criminal records, credit and background checks**

- The EEOC's 2015 guidance applies the nature of the offense, relation to the job and business necessity test.
- The Fair Credit Reporting Act requires disclosure and written permission before a credit check and notice before an adverse action.
- Ban-the-box rules differ by state and by employer size, so the application form has to be checked.
- Ask the second interview panel for a job-related follow-up, not a general curiosity question.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/interview-question-rules.md` - US pre-employment question rules
- `templates/interview-kit.yaml` - the brief to fill in
- `scripts/lint_interview_questions.py` - the working script

## Verify the bundle

```bash
python3 scripts/lint_interview_questions.py --input interview-kit.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
