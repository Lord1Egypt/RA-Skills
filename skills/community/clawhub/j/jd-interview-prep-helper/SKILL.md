---
name: jd-interview-prep-helper
description: Help users prepare for job interviews by analyzing job descriptions and company information. Use this skill when the user wants to prepare for an interview, provides a job description (JD) and company name, or mentions interview preparation. Make sure to use this skill whenever the user asks about interview prep, mentions a specific company and JD, or wants to prepare for a technical interview.
compatibility:
  tools:
    - web-search
    - tavily
    - read
    - write
---

# Interview Preparation Skill

## When to Use

Use this skill when:
- User provides a job description (JD) and company name
- User mentions interview preparation
- User asks about what to study for a specific interview
- User wants interview questions or preparation checklist

## Input Format

Provide:
1. **Job Description (JD)** - Full text or file reference
2. **Company Name** - The company user is interviewing with
3. **Optional Context**:
   - Target role/position
   - Years of experience required
   - Specific technologies mentioned in JD
   - Company industry/field

## Process

1. **Read JD** - Parse the job description to understand:
   - Required technologies and frameworks
   - Responsibilities and duties
   - Qualifications and requirements
   - Seniority level
   - Company domain/industry

2. **Research Company** (if not provided):
   - Search for company business model, products, services
   - Find recent news, company culture, values
   - Identify key technologies they use
   - Look for interview patterns (common questions, focus areas)

3. **Analyze Technical Requirements**:
   - Break down into technical domains (backend, frontend, algorithms, etc.)
   - Identify core technologies and their depth
   - Note any specialized skills or tools

4. **Generate Interview Checklist**:
   - Technical knowledge points
   - Coding challenges to practice
   - System design topics
   - Behavioral interview questions

5. **Create Preparation Plan**:
   - Prioritize topics by importance
   - Suggest time allocation
   - Recommend resources

## Output Format

Use this exact structure:

# [Company Name] - [Position] Interview Preparation

## 📋 Executive Summary

Brief overview of what to focus on (2-3 sentences).

## 🎯 Key Technical Areas

### [Area 1: e.g., Backend Architecture]
- **Core Concepts**: [list 3-5 key concepts]
- **Key Technologies**: [list technologies]
- **Depth Level**: [e.g., foundational / intermediate / advanced]
- **Practice Topics**: [2-3 coding/system design topics]

### [Area 2: e.g., Database Design]
...

## 🏢 Company Knowledge

### Business Model
[describe what the company does, their main products/services]

### Key Technologies Used
[list technologies mentioned in JD + researched ones]

### Company Culture & Values
[based on research, describe culture, work style, what they value]

### Recent Developments
[1-2 recent news or projects]

## 🗓️ Interview Preparation Plan

### Week 1: Foundation
- [Topic 1] - [3-5 hours]
- [Topic 2] - [3-5 hours]
- [Topic 3] - [2-3 hours]

### Week 2: Advanced Topics
...

### Week 3: Practice
- [Coding challenges]
- [Mock interviews]
- [System design]

## 📚 Recommended Resources

### Books
- [Book 1]
- [Book 2]

### Online Resources
- [Website 1]
- [Website 2]

### Practice Platforms
- [Platform 1]
- [Platform 2]

## 🎤 Behavioral Interview Questions

### Teamwork
1. Tell me about a time you worked in a team...
2. How do you handle conflicts...

### Problem Solving
1. Describe a challenging problem you solved...
2. How do you approach debugging...

### Growth Mindset
1. What's a skill you're currently learning...
2. How do you stay updated...

## ⚡ Quick Reference

**Must Know** (before interview):
- [Top 5 technical concepts]
- [Top 3 company-specific topics]

**Nice to Know**:
- [Bonus topics]

**Red Flags to Avoid**:
- [Common mistakes to avoid]

---

## Examples

**Example 1 - Text Input:**
```
JD: Senior Backend Engineer - Python/Django
Company: ByteDance
```

**Example 2 - File Input:**
```
Please prepare for my interview at Alibaba as a Data Engineer.
I've attached my JD in the file: JD_20260321.txt
```

**Example 3 - Company Only:**
```
Help me prepare for my interview at Tencent as a frontend engineer.
I'll provide the JD after.
```

---

## Tips for Best Results

1. **Be Specific**: Include all relevant details from the JD
2. **Provide Context**: Mention years of experience, target role level
3. **Share Company Info**: If you know about the company, share it
4. **Ask Follow-ups**: If you need clarification, ask before generating

## Output File

Save the preparation guide as:
`interview-prep-[company]-[position]-[date].md`

Example: `interview-prep-bytedance-senior-backend-20260321.md`
