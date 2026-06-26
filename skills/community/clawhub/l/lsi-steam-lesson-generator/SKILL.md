# AI-Integrated STEAM Lesson Generator

Generate complete lesson plans with AI tool integration for Hong Kong schools.

## When to Use

Use this skill when the user wants to:
- Create an AI-integrated lesson plan for any subject
- Generate teaching resources for EDB AI funding requirements
- Design lessons that incorporate AI tools for student learning
- Produce lesson plans for Primary or Secondary education in Hong Kong

## Input Required

Ask the user for:
1. **Subject** — What subject? (Math, Science, English, Chinese, STEAM, etc.)
2. **Grade Level** — Primary or Secondary? Which year?
3. **Topic** — Specific topic within the subject
4. **Duration** — Lesson length (default: 40 minutes for Primary, 35-70 minutes for Secondary)
5. **Language** — Chinese, English, or Bilingual (default: Bilingual)

## AI Tools Available

This skill integrates these AI tools into lessons:

| Tool | Use Case | Type |
|------|----------|------|
| **GLM5** | Research, writing, brainstorming, Q&A, **assessment assistance** | Text |
| **Canva AI** | Design, presentations, infographics | Visual |
| **Gamma** | AI-powered presentations | Presentation |
| **HeyGen** | Avatar video creation | Video |
| **Blender** | 3D modeling & animation | 3D |
| **Tripo3D.ai** | AI 3D model generation | 3D |

---

## Output Format

Generate a complete lesson plan with these sections:

---

### 0. Teacher Quick Start (NEW)

For teachers unfamiliar with AI tools, provide a simple getting-started guide:

```
Before the Lesson:

□ [Tool 1] - Quick Setup (5 min)
  - Step 1: [What to do]
  - Step 2: [What to do]
  - Link: [Direct URL to tool]
  - Video Tutorial: [If available]

□ [Tool 2] - Quick Setup (5 min)
  - Step 1: [What to do]
  - Step 2: [What to do]
  - Link: [Direct URL to tool]

Need Help?
- Stuck on AI tools? Ask the school IT coordinator or contact [support]
- All tools have free versions sufficient for this lesson

Time Investment: [X minutes] setup before class
Time Saved: [Y minutes] compared to traditional lesson prep
```

---

### 1. Lesson Overview

```
Subject: [Subject]
Topic: [Topic]
Grade: [Primary/Secondary Year X]
Duration: [X minutes]
Language: [Chinese/English/Bilingual]

Learning Objectives:
- [Objective 1 - Knowledge]
- [Objective 2 - Skills]
- [Objective 3 - AI Literacy]

AI Tools Used:
- [Tool 1]: [Purpose]
- [Tool 2]: [Purpose]

Materials Needed:
- [Digital tools]
- [Physical materials]
```

---

### 2. AI Tool Integration

For each AI tool used, provide:

```
Tool: [Tool Name]
Purpose: [What students/teachers will use it for]
Setup Required: [Account creation, installation, etc.]
Activity: [Specific task using this tool]
Time Allocation: [X minutes]
Tips for Teachers: [Best practices, common issues]
```

---

### 3. Teaching Steps

```
Minute 0-5: Introduction
- [Opening activity]
- [Connect to prior knowledge]

Minute 5-15: Direct Instruction
- [Core content delivery]
- [Demonstration of AI tool]

Minute 15-30: Guided Practice
- [Students try AI tool with support]
- [Collaborative activity]

Minute 30-40: Independent Practice
- [Students create/use AI independently]
- [Apply to task]

Minute 40-45: Closure & Assessment
- [Review key concepts]
- [Exit ticket or quick check]
```

---

### 4. Student Activities

```
Activity 1: [Name]
- Type: [Individual/Pair/Group]
- Tool: [AI tool used]
- Instructions: [Step-by-step for students]
- Output: [What students produce]

Activity 2: [Name]
- Type: [Individual/Pair/Group]
- Tool: [AI tool used]
- Instructions: [Step-by-step for students]
- Output: [What students produce]
```

---

### 5. Assessment Rubric

```
| Criterion | Excellent (4) | Good (3) | Developing (2) | Beginning (1) |
|-----------|---------------|----------|----------------|---------------|
| [Subject Knowledge] | [Description] | [Description] | [Description] | [Description] |
| [AI Tool Usage] | [Description] | [Description] | [Description] | [Description] |
| [Creativity] | [Description] | [Description] | [Description] | [Description] |
| [Collaboration] | [Description] | [Description] | [Description] | [Description] |

Total Score: ___ / 16
```

---

### 5B. AI-Assisted Assessment (NEW)

Use GLM5 or other AI tools to help evaluate student work:

```
How to Use AI for Assessment:

1. Take a photo/screenshot of student work
2. Upload to GLM5 (or paste text description)
3. Use this prompt:

---
PROMPT FOR AI:
"I am a [Subject] teacher assessing student work.

The learning objectives were:
- [Objective 1]
- [Objective 2]
- [Objective 3]

Please evaluate this student work on a scale of 1-4 for each criterion:
- [Criterion 1]: [Description]
- [Criterion 2]: [Description]
- [Criterion 3]: [Description]
- [Criterion 4]: [Description]

Provide:
1. A score (1-4) for each criterion
2. Specific feedback for the student (2-3 sentences)
3. One suggestion for improvement

Student work: [Describe or paste content]
---

4. Review AI's evaluation and adjust as needed
5. AI provides a starting point — YOU make the final judgment

Important:
- AI assists, not replaces, teacher judgment
- Always review AI suggestions before giving to students
- Use AI for initial feedback, not final grades
```

### 6. Teacher Notes

```
Preparation Checklist:
☐ [Setup task 1]
☐ [Setup task 2]
☐ [Prepare backup if AI tools unavailable]

Differentiation:
- For struggling learners: [Support strategies]
- For advanced learners: [Extension activities]

Common Issues & Solutions:
- [Issue 1]: [Solution]
- [Issue 2]: [Solution]

EDB Alignment:
- This lesson contributes to the AI teaching resource requirement.
- Recommended for: [Subject 1], [Subject 2], [Subject 3] integration
```

---

## Quality Standards

Every lesson plan must:

1. **Be practical** — AI tools must be realistically usable by students/teachers
2. **Be age-appropriate** — Match complexity to grade level
3. **Include real AI usage** — Not just "learn about AI" but "use AI to learn"
4. **Match Hong Kong curriculum** — Reference local curriculum where relevant
5. **Be EDB-ready** — Can be submitted as one of the 6 AI teaching resources
6. **Support AI-novice teachers** — Include step-by-step guidance for every AI tool used
7. **Include AI-assisted assessment** — Show how to use AI to help grade/evaluate student work

---

## Examples

### Example 1: Primary 4 Science - Plant Life Cycle

**Input:**
- Subject: Science
- Grade: Primary 4
- Topic: Plant Life Cycle
- Duration: 40 minutes
- Language: Bilingual

**AI Tools to Use:**
- Canva AI — Students create infographic of plant life cycle
- HeyGen — Teacher creates intro video with plant avatar

### Example 2: Secondary 2 English - Descriptive Writing

**Input:**
- Subject: English
- Grade: Secondary 2
- Topic: Descriptive Writing
- Duration: 70 minutes (double period)
- Language: English

**AI Tools to Use:**
- GLM5 — Brainstorming descriptive vocabulary
- Gamma — Students create visual story presentation
- HeyGen — Create character narration videos

### Example 3: Secondary 4 Math - 3D Geometry

**Input:**
- Subject: Mathematics
- Grade: Secondary 4
- Topic: 3D Geometry (Volume & Surface Area)
- Duration: 35 minutes
- Language: Chinese

**AI Tools to Use:**
- Tripo3D.ai — Generate 3D shapes for visualization
- Blender — Explore and manipulate 3D objects
- Canva AI — Create formula reference cards

---

## File Output

After generating the lesson plan, offer to save it as:
- `[Subject]_[Grade]_[Topic]_Lesson_Plan.md`
- Or export as PDF if requested

Save location: `~/Desktop/LSI/Curriculum/lessons/`

---

## Notes

- Always ask clarifying questions if input is unclear
- Default to bilingual (Chinese/English) for Hong Kong context
- Suggest age-appropriate AI tools — younger students need simpler interfaces
- Consider school tech infrastructure — some AI tools may be blocked
- Include both teacher-led and student-led AI activities
