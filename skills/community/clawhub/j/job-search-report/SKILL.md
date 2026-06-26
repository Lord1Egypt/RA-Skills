---
name: job-search-report
description: Generate a comprehensive job search progress report by analyzing sent applications and received replies from Gmail. Activate when user asks for a job search summary, report, dashboard, progress update, or wants to see all their applications in one view. Pulls data from Gmail and produces a structured markdown report.
metadata: {"openclaw": {"emoji": "📊", "requires": {"bins": ["gog"]}}}
---

# Job Search Report Generator

Analyzes Gmail history to generate a complete job search progress report.

## Prerequisites

`gog` authenticated with Gmail:
```bash
gog auth add you@gmail.com --services gmail
```

## When to Activate

- "生成求职报告"、"job search summary"、"show me my application status"
- "我投了哪些公司"、"how many companies have I applied to"
- "求职进展怎么样"、"create a job search dashboard"

## Data Collection Workflow

### Step 1: Pull sent applications

```bash
# Find all job application emails sent
gog gmail messages search "in:sent (application OR resume OR apply OR applying OR interested in the position) newer_than:90d" \
  --max 100 \
  --account you@gmail.com \
  --json
```

### Step 2: Pull all replies received

```bash
# Find all recruiter/HR replies
gog gmail messages search "in:inbox (interview OR application OR resume OR opportunity OR position OR hiring OR recruiter) newer_than:90d" \
  --max 100 \
  --account you@gmail.com \
  --json
```

### Step 3: Cross-reference and build application map

For each sent application, find matching replies by:
- Matching domain (sent to `hr@company.com` → replies from `*@company.com`)
- Matching subject thread (`Re:` prefix)
- Date ordering (reply must be after application)

## Report Structure

Generate the full report in this format:

```markdown
# 📊 Job Search Report
Generated: [date]
Period: Last [N] days
Account: [email]

---

## 📈 Overview

| Metric | Count |
|---|---|
| Total Applications Sent | [N] |
| Companies Replied | [N] |
| Reply Rate | [N]% |
| Interview Invites | [N] |
| Currently In Process | [N] |
| Rejections Received | [N] |
| Awaiting Reply (>7 days) | [N] |

---

## 🟢 Active Opportunities (Priority)

### [Company Name] — [Job Title]
- **Applied**: [date]
- **Status**: 🟢 Interview Scheduled / 🔵 In Discussion
- **Contact**: [recruiter name] <email>
- **Latest Update**: [date] — "[key sentence from last email]"
- **Next Action**: [specific action + deadline]

---

## 🔵 Positive / In Progress

### [Company Name] — [Job Title]
- **Applied**: [date]
- **Status**: 🔵 Responded Positively
- **Latest**: [date] — [summary]
- **Next Action**: [action]

---

## 🟡 Awaiting Your Response

### [Company Name] — [Job Title]
- **They need**: [salary info / portfolio / references / assessment]
- **Deadline**: [if mentioned]
- **Next Action**: Prepare and reply ASAP

---

## ⚪ Applied — No Reply Yet

| Company | Role | Applied | Days Since | Follow Up? |
|---|---|---|---|---|
| [Company] | [Role] | [date] | [N] days | [Yes if >7d] |

---

## 🔴 Closed (Rejections)

| Company | Role | Applied | Rejected | Notes |
|---|---|---|---|---|
| [Company] | [Role] | [date] | [date] | [reason if given] |

---

## ⚡ Action Items

Priority actions sorted by urgency:

1. 🔴 **[URGENT]** Reply to [Company] interview invite — respond today
2. 🟠 **[HIGH]** Send follow-up to [Company] — applied 10 days ago, no reply
3. 🟡 **[MEDIUM]** Prepare portfolio for [Company] request
4. 🟢 **[LOW]** Research [Company] before scheduled interview on [date]

---

## 📅 Timeline View

[Month Year]
  [Date] ✉️  Applied to [Company] — [Role]
  [Date] 📬 Reply from [Company] — Interview invite
  [Date] ✉️  Applied to [Company] — [Role]
  [Date] 📬 Rejection from [Company]
  ...

---

## 💡 Insights & Suggestions

**Response rate by industry**: [Tech: X% | Finance: X% | Marketing: X%]
**Average days to reply**: [N] days
**Most active day to apply**: [Day of week from data]

Suggestions:
- [Insight based on data, e.g. "You've applied mostly to large companies — 
   consider adding more startups for higher reply rates"]
- [e.g. "5 applications have been waiting >14 days — consider following up"]
- [e.g. "Your interview rate is X% — above/below the typical 5-10% benchmark"]
```

## Save Report Options

After generating, offer to save:

```bash
# Save as markdown file
cat > ~/job-search-report-[date].md << 'EOF'
[report content]
EOF
```

Or ask if user wants to save to a Google Doc:
```bash
# If user has gog docs access
gog docs export [docId] --format txt
```

## Weekly Update Mode

If user asks "update my report" or "refresh":
1. Fetch only new emails since last report date
2. Show only the **delta** (new replies, status changes)
3. Update the action items list

```
📬 Updates since [last report date]:
• [Company] replied — moved from "Awaiting" to "Interview Invite"
• [Company] — 14 days with no reply, suggested follow-up added
• New application sent to [Company]
```

## Metrics Benchmarks (context for user)

| Metric | Typical Range | What it means |
|---|---|---|
| Reply rate | 5–20% | Industry average; 20%+ means strong resume/targeting |
| Application-to-interview | 5–15% | Higher = strong resume + good fit |
| Days to first reply | 3–14 days | Most replies come in first week |
| Interview-to-offer | 20–30% | Varies widely by company |

Use these to contextualize the user's numbers in the Insights section.
