# Output Schema

The model must return one valid JSON object per evaluated resume. The object must follow this contract before reports are rendered.

```json
{
  "candidate_id": "resume filename based id",
  "inferred_profile": {
    "role_family": "",
    "seniority": "",
    "domain_context": "",
    "confidence": 0.0
  },
  "scores": {
    "score_basis": "resume_quality_only|resume_plus_jd_company",
    "overall": 0,
    "resume_quality": 0,
    "jd_company_match": null,
    "dimensions": [
      {
        "name": "",
        "score": 0,
        "max_score": 0,
        "evidence": [],
        "deductions": []
      }
    ]
  },
  "evidence": [],
  "deductions": [],
  "strengths": [],
  "concerns": [],
  "interview_validation_points": [],
  "compliance": {
    "sensitive_or_irrelevant_information": [],
    "must_not_use_for_screening": [],
    "manual_review_required": [],
    "no_auto_reject_reasons": []
  },
  "recommendation": {
    "screening_bucket": "strong_review|review|weak_review|manual_review",
    "summary": "",
    "next_steps": []
  }
}
```

## Required Score Rules

- `scores.score_basis` must be either `resume_quality_only` or `resume_plus_jd_company`.
- For `resume_plus_jd_company`, `scores.overall` must equal `scores.resume_quality + scores.jd_company_match`.
- For `resume_quality_only`, `scores.jd_company_match` must be `null` and `scores.overall` must be normalized from resume quality to 100.
- Every score dimension must include evidence, deductions, or both.
- Evidence must come from the resume, JD, or company background. Do not invent facts.

## Compliance Fields

- `compliance.sensitive_or_irrelevant_information`: protected or job-irrelevant traits visible in the resume.
- `compliance.must_not_use_for_screening`: traits or facts that must be excluded from scoring and screening decisions.
- `compliance.manual_review_required`: reasons a human recruiter must review the record.
- `compliance.no_auto_reject_reasons`: reasons the report must not be treated as an automatic rejection or elimination.

## Recommendation Rules

`recommendation.screening_bucket` must be one of:

- `strong_review`
- `review`
- `weak_review`
- `manual_review`

The recommendation is a recruiter review aid only. It must not contain final hiring, rejection, elimination, pass, fail, or admission decisions.
