# Output

## Human summary
Return:
1. input investigated
2. platforms checked
3. exact matches
4. likely matches
5. weak matches
6. confidence summary
7. caveats

When useful, include:
- final profile links
- profile image links if publicly exposed

## JSON shape
Use this shape when exporting:

```json
{
  "input": {
    "username": null,
    "email": null
  },
  "checked_platforms": [],
  "matches": [
    {
      "platform": "github",
      "url": "https://github.com/example",
      "final_url": "https://github.com/example",
      "profile_image": "https://...",
      "match_type": "exact",
      "signals": ["exact_username_match"],
      "confidence_score": 20,
      "notes": "public profile exists"
    }
  ],
  "summary": {
    "overall_confidence": "possible"
  }
}
```

## Minimal reporting rule
Do not dump raw noise from every failed platform unless the user wants the full report.
Lead with the strongest matches first.
