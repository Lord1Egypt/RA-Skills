# Demo Prompt

Use this prompt to test the skill end to end:

```text
Use $lead-finder-outreach to build a 50 companies prospect pack.

Use this JSON input:
{
  "request": {
    "niche": "dental clinics",
    "location": "California, United States",
    "fit_criteria": "Clinics with a visible website, clear local service footprint, and a usable public contact path."
  }
}

Return:
- a short request summary
- a 50-company shortlist in a CSV-friendly structure
- public contact paths only
- notes on any coverage gaps or low-confidence entries
```

The skill defaults to a `50 companies` pack unless you explicitly customize the implementation later.
