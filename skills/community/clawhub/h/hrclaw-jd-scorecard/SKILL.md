---
name: jd-scorecard
description: Turn job descriptions and PDF resumes into structured hiring decisions, interview questions, and Feishu/DingTalk-friendly output.
---

# JD Scorecard Skill

HRClaw turns messy JD text and PDF resumes into recruiter-ready decisions.
It keeps screening consistent, fast, and easy to share in team chat.

把 JD 和 PDF 简历变成结构化、可执行的招聘结论。

Use this skill for two related flows:

- JD -> scorecard
- Resume PDF/text -> score against a scorecard

## Best for

- high-volume recruiting
- QA / Python / operations roles
- teams that want one repeatable scoring standard
- Feishu / DingTalk collaboration

If the user gives both a JD and a resume, generate the scorecard first and then score the resume.

## JD flow

Default to a single JSON object with:
- `role_title`
- `summary`
- `filters`
- `must_have`
- `nice_to_have`
- `exclude`
- `weights`
- `thresholds`
- `interview_questions`
- `red_flags`
- `assumptions`
- `next_steps`

If the user asks for a readable version, format the same content with `templates/scorecard.md`.
If the user asks for a Feishu/DingTalk-friendly chat view, format the same content with `templates/chat-scorecard.md`.

## Resume score flow

Use this flow when the user uploads a resume PDF or pastes resume text together with a scorecard.

If the user only provides a resume, ask for a scorecard or JD before scoring.

1. Extract the resume text from the PDF first.
2. If the PDF is image-only and no readable text is available, set `extraction_status` to `needs_ocr` and stop.
3. Normalize the resume into a candidate profile.
4. Score it against the provided scorecard using the same filters, weights, and thresholds.
5. Return one pure JSON object first.

Resume output should include:

- `mode`
- `source_type`
- `extraction_status`
- `scorecard_name`
- `candidate_profile`
- `hard_filter_pass`
- `hard_filter_fail_reasons`
- `dimension_scores`
- `total_score`
- `decision`
- `review_reasons`
- `matched_terms`
- `missing_terms`
- `blocked_terms`
- `evidence`
- `summary`
- `next_steps`

If the user asks for a Feishu/DingTalk-friendly chat view, format the same content with `templates/chat-resume-score.md`.

Candidate profile fields:

- `name`
- `location`
- `years_experience`
- `education_level`
- `current_title`
- `current_company`
- `skills`
- `industry_tags`

If the user provides a JD and a resume together, generate the scorecard first, then score the resume against it.

## Rules

- Use only explicit evidence from the JD.
- For resume scoring, use only explicit evidence from the resume and scorecard.
- Do not invent requirements or hidden intent.
- Keep one primary role per scorecard.
- If the JD is mixed or vague, add short `assumptions` instead of guessing.
- Prefer practical screening signals over generic hiring advice.
- Generate 5 to 10 interview questions that test real work.
- If a resume PDF is unreadable and OCR text is not available, say so clearly instead of guessing.

## Flow

1. Extract the role, location, years of experience, education, tools, and exclusions.
2. Convert those signals into a scorecard.
3. Add interview questions that verify the must-haves.
4. Add red flags that help a recruiter reject quickly.
5. For resumes, extract the profile, apply the scorecard, and return the scoring JSON first.

## References

- `references/quickstart.md`
- `references/faq.md`
- `references/limitations.md`
- `prompts/jd-to-scorecard.md`
- `prompts/resume-score.md`
- `prompts/interview-questions.md`
- `templates/scorecard.json`
- `templates/scorecard.md`
- `templates/chat-scorecard.md`
- `templates/resume-score.json`
- `templates/resume-score.md`
- `templates/chat-resume-score.md`
