# Limitations

## What this skill does not do

- It does not log into BOSS or any other hiring platform.
- It does not replace a recruiter or hiring manager.
- It does not make final hiring decisions.
- It does not guess missing JD or resume information.

## Where it works best

- Clear, single-role JDs
- Roles with explicit skills, tools, or experience bands
- Teams that already want a repeatable screening rubric

## Where it is weaker

- Very vague JDs
- Mixed roles in one posting
- Highly senior roles with subtle context
- Scanned resumes without extractable text

## Operational note

Default to conservative outputs:

- use `null` or `[]` when evidence is missing
- add assumptions instead of inventing facts
- return `needs_ocr` for image-only PDFs

## Practical takeaway

Use it as a fast first pass, then calibrate the thresholds with real screening results.
