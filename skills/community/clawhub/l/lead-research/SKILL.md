---
name: lead-research
description: Research and qualify business leads for recruiting and sales teams. Finds companies with active HR job postings, identifies decision-makers, and compiles enriched lead lists.
version: 1.0.0
author: OWL
tags: [research, leads, recruiting, sales, B2B]
---

# Lead Research Skill

## Purpose
Automatically research and qualify business leads by finding companies with active HR job postings, identifying decision-makers, and compiling enriched contact lists.

## When to Use
- Building a lead list for recruiting or sales outreach
- Researching a specific industry or geographic area
- Qualifying companies as potential clients
- Finding decision-makers at target companies

## How It Works

### Step 1: Define Search Criteria
Specify:
- **Industry**: (e.g., law firms, accounting, consulting, IT services)
- **Location**: (e.g., Seattle, King County, WA)
- **Company Size**: (e.g., 5-25 employees)
- **Signal**: Active HR job posting (key qualifier)

### Step 2: Search for Companies
Use web search to find:
1. "[Industry] companies in [Location]"
2. "[Industry] site:bbb.org [Location]"
3. "HR jobs [Industry] [Location]"
4. "[Company name] careers page"

### Step 3: Verify HR Posting
For each company found:
1. Check their careers/jobs page
2. Look for active HR-related job postings
3. Note the job title, posting date, and URL

### Step 4: Find Decision-Makers
For companies with active HR postings:
1. Search "[Company name] owner" or "[Company name] CEO"
2. Check LinkedIn for key contacts
3. Find email patterns (e.g., first@company.com)

### Step 5: Compile Lead List
Create a structured list with:
- Company name
- Industry
- Location
- Company size (estimated)
- HR job posting (title + URL)
- Decision-maker name
- Decision-maker title
- Contact email (if found)
- Source URLs

## Output Format

```markdown
# Lead Research Report: [Industry] in [Location]
Date: [Date]
Total Leads: [Number]
Qualified Leads: [Number]

## High-Quality Leads (Active HR Posting + Decision-Maker Found)

### 1. [Company Name]
- **Industry**: [Industry]
- **Location**: [City, State]
- **Size**: [X-Y employees]
- **HR Posting**: [Job Title] ([URL])
- **Decision-Maker**: [Name], [Title]
- **Email**: [email@company.com]
- **Sources**: [URLs]

[Repeat for each lead...]
```

## Tips
- BBB.org is the best free source for small business listings
- Google searches for "[trade] site:bbb.org [city]" work well
- HR job posting is the KEY signal — companies hiring HR are growing
- Focus on Owner/President/CEO/Founder as decision-makers
- Verify email patterns using tools like Hunter.io

## Limitations
- Cannot access LinkedIn without authentication
- Email verification requires additional tools
- Some companies don't list job postings publicly
