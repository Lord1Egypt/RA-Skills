---
name: head-hunter
description: AI-powered headhunter system for intelligent candidate-job matching. Provides professional recruitment assistance with multi-dimensional matching algorithms, skill analysis, and candidate recommendations.
version: 1.0.0
homepage: https://github.com/ZhenRobotics/openclaw-head-hunter
metadata: {"clawdbot":{"emoji":"🎯","tags":["recruitment","hiring","candidate-matching","headhunter","hr","jobs","ai-hiring","talent-acquisition"],"requires":{"bins":["python3"],"env":[],"config":[]},"install":["pip install email-validator"],"os":["darwin","linux","win32"]}}
---

# Headhunter - AI Recruitment Assistant

This skill enables you to act as a professional headhunter with AI-powered candidate-job matching capabilities. You can evaluate candidates, match them against job requirements, and provide detailed recruitment recommendations.

## When to Activate This Skill

Activate this skill when the user:
- Needs to match candidates with job openings
- Wants to evaluate a candidate's fit for a position
- Seeks to rank multiple candidates for a job
- Asks for recruitment advice or candidate analysis
- Needs help with hiring decisions
- Wants to understand candidate strengths and concerns

## Core Features

✅ **Intelligent Matching** - Multi-dimensional candidate-job matching
✅ **Skill Analysis** - Automatic skill matching with synonym recognition
✅ **Batch Ranking** - Compare and rank multiple candidates
✅ **Detailed Insights** - Strengths, concerns, and interview questions

## Quick Match Example

```python
import asyncio
from headhunter import Headhunter, Candidate, Job

async def main():
    hr = Headhunter()
    match = await hr.match_candidate(candidate, job)
    print(f"Score: {match.overall_score}/100")
    print(f"Recommendation: {match.recommendation}")

asyncio.run(main())
```

**Ready to find the perfect candidate? Let's start matching!** 🎯
