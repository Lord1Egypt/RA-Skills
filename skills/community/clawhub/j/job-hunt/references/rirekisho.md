# Rirekisho (履歴書) Reference — Japanese CV form

The rirekisho is the standardized Japanese CV **form** that many traditional Japanese employers expect. It is a different document from the Western CV. Use this reference when the target market is **Japan** and the employer is traditional/domestic (see `cv-craft.md §2`, Cluster 3 — Japan).

## When to use it (the Japan fork)

- **Global / foreign-capital firms, startups, most tech:** a Western-style CV (the normal `render_cv.py` output, written in Japanese or English) is accepted. Use that.
- **Traditional / domestic Japanese employers:** they expect the **rirekisho (履歴書)**, almost always paired with a **職務経歴書 (shokumu-keirekisho)** — a free-form work-history document. The Western CV the skill already produces serves as (or directly informs) the shokumu-keirekisho. Render the rirekisho with `scripts/render_rirekisho.py`.

**Always flag this fork to the user** and confirm which they need before producing a rirekisho. When unsure, ask; default to the Western CV for international roles.

## The honesty rule still governs

The rirekisho asks for **personal data** a Western CV omits — date of birth, age, sometimes gender, address, and a photo. These are **provided by the candidate, never invented or inferred.** Ask the user for them; do not guess a birth date, fabricate an address, or assume a gender.

- **Gender (性別):** modern Japanese practice increasingly **omits** gender (the 2021 JIS-style template dropped the field). Include it only if the user chooses to. Default: omit unless asked.
- **Photo:** a 36–40mm × 24–30mm headshot. If the user supplies an image path (`jp.photo_path`), it is embedded; otherwise the form shows a labelled placeholder box.
- **学歴・職歴 dates and entries** are derived from the candidate's real `education`/`experience` — same honest-reframing rules as the Western CV.

## Japan-specific profile fields (`jp:` block — all optional, user-supplied)

```yaml
jp:
  name_furigana:    "やまだ たろう"     # reading of the name (ふりがな)
  date_of_birth:    "1995-04-12"
  age:              "31"               # the model computes this from DOB + today
  gender:           ""                  # commonly omitted now; include only if the user wants
  address:          "東京都新宿区1-1-1"
  address_furigana: "とうきょうと しんじゅくく…"
  photo_path:       ""                  # path to a headshot image; placeholder box if empty
  date:             "2026年6月6日"       # the "as of" date printed on the form
  motivation:       "志望の動機 … (why this employer)"
  personal_request: "本人希望記入欄 … (e.g. desired role, or 「貴社の規定に従います」)"
```

`age` is conventionally written as 満○歳. The skill (which knows today's date) computes it from `date_of_birth`; the renderer only prints what it is given (it does not compute dates).

## How the form is built

`render_rirekisho.py` produces:

- **基本情報** — name + ふりがな, 生年月日 (満N歳), optional 性別, 現住所 (+ ふりがな), TEL, E-mail, and a photo box.
- **学歴・職歴** — one combined chronological table: a 学歴 header, 入学/卒業 (or 在学中) rows per degree, a 職歴 header, 入社/退社 (or 現在に至る) rows per role, closed with 以上. Built from `education` + `experience`, sorted by date.
- **免許・資格** — from `certifications` (特になし if none).
- **志望の動機** and **本人希望記入欄** — free-text boxes from `jp.motivation` / `jp.personal_request`.

## Rendering

```bash
# .docx is the authentic, editable form (the idiomatic Japanese workflow).
python scripts/render_rirekisho.py <workspace>/tailored-profile.yaml --format docx --out <workspace>/rirekisho.docx
# Markdown for quick preview.
python scripts/render_rirekisho.py <workspace>/tailored-profile.yaml --format md   --out <workspace>/rirekisho.md
```

**PDF:** the rirekisho is a CJK form and is **not** routed through the Latin LaTeX template. Produce the PDF by exporting the `.docx` from Word or LibreOffice (`File → Export as PDF`). Tell the user this; the `.docx` is the deliverable to submit or print.

## Review note

The three pipeline judges (ATS screener + Recruiter/HR + Hiring Manager) are calibrated to the Western CV / ATS pipeline, which is **not** how traditional Japanese rirekisho screening works. For a Japan rirekisho package:

- Run the three-judge review on the **companion shokumu-keirekisho / Western CV** (the keyword-and-fit document), as usual.
- For the **rirekisho form itself**, do a completeness/correctness check instead: all required personal fields present, 学歴・職歴 chronological and gap-explained, dates consistent, motivation specific to the employer, no fabricated personal data. Report this to the user rather than an ATS coverage %.
