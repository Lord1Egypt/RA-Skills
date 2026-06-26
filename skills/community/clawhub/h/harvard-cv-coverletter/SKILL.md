---
name: harvard-cv-coverletter
description: >
  Expert engine for creating Harvard-standard CVs (resumes) and cover letters following the
  official Harvard Office of Career Services guidelines. Use this skill when a user asks
  to create, write, build, draft, or improve a resume, CV, or cover letter. Relevant
  trigger phrases include: "write my resume", "help me with my CV", "draft a cover letter",
  "update my resume", "I need a CV for a job application", "create a professional resume",
  "I'm applying for a job and need a cover letter", or any explicit request involving job
  application documents. Also use when the user shares their background and asks for help
  getting it into document form. Produces .docx files matching Harvard's exact formatting
  guidelines, including bullet-format and paragraph-format resume variants.
compatibility: "Requires Node.js. Run: npm list -g docx | grep docx || npm install -g docx"
---

# Harvard CV & Cover Letter Engine

Produces professional, Harvard-standard CVs and cover letters as `.docx` files.

## ⚠️ CARDINAL RULE — NO HALLUCINATION

**DO NOT hallucinate, create, infer, or assume ANY information about the person's skills,
experience, education, achievements, or background. ADHERE STRICTLY AND EXCLUSIVELY to
the information explicitly provided by the person in this conversation. If information is
missing, ask for it. Never fill in gaps with invented content.**

This rule applies to every field: job titles, dates, company names, responsibilities,
quantified results, skills, languages, education details — everything. Only use what the
user has told you.

---

## Step 0 — Collect Information

Before writing anything, determine what documents are needed and gather the necessary
context. Ask only what you don't already have from the conversation.

### For CV/Resume, collect:
1. **Contact info**: Full name, address (optional), email, phone
2. **Education**: Institution(s), degree(s), concentration/major, GPA (optional), graduation date, thesis (optional), relevant coursework (optional), honors/awards (optional)
3. **Experience**: For each role — organization name, city/state, job title, dates (Month Year – Month Year), and bullet-point responsibilities/achievements
4. **Leadership & Activities**: Organizations, roles, dates, descriptions (optional)
5. **Skills & Interests** (optional): Technical skills, languages (with fluency), lab techniques, interests
6. **Format preference**: Bullet-style or paragraph-style experience descriptions
7. **Target role or industry** (to guide section ordering if needed)

### For Cover Letter, collect:
1. **Applicant's contact info**: Name, address, email, phone
2. **Date**
3. **Recipient**: Name, title, organization, address
4. **Position being applied for** and where it was found
5. **Organization context**: What specifically about this organization excites the person (they must tell you — do NOT invent this)
6. **Key experiences from their background** most relevant to this role (drawn only from what they share)
7. **Any specific skills or achievements** they want highlighted

**If any critical information is missing, ask for it before proceeding. DO NOT hallucinate, create, infer, or assume ANY information to fill gaps.**

---

## Step 1 — Select Format

**Resume formats:**
- **Bullet style** (default): Experience described as bullet points starting with action verbs
- **Paragraph style**: Experience described in short paragraph form, same action-verb rules apply

Ask the user which they prefer if not specified. Default to bullet style.

---

## Step 2 — Apply Harvard Guidelines

Read `references/harvard-rules.md` before generating any document. All documents must strictly follow those rules.

Key rules to enforce at all times:
- Language: specific, active, fact-based, no personal pronouns, no narrative style, no slang
- Each bullet/sentence begins with an action verb (see action verbs list in the reference)
- Reverse chronological order within each section
- Sections ordered by relevance to target role
- No pictures, age, gender, or references
- Cover letter: max one page, no flowery language, minimal use of "I"
- Same font type and size on both resume and cover letter

---

## Step 3 — Generate the Document

Use the `docx` npm package (v9+) to produce `.docx` files via a Node.js script.
All necessary patterns are included below — this skill is self-contained, no external skill files need to be read.

### CV/Resume formatting rules (from Harvard templates):

**Header:**
```
[Bold, centered] FirstName LastName
[Centered] Street Address • City, State Zip • email@example.com • phone number
```

**Section headings:** Full-width, bold, with a horizontal line underneath (use paragraph border)

**Education entry format:**
```
[Bold left] Organization Name          [Right-aligned] City, State
[Left] Degree, Concentration. GPA (optional)    [Right-aligned] Graduation Date
[Left, italic optional] Thesis: ... (optional)
[Left] Relevant Coursework: ... (optional)
```

**Experience entry format:**
```
[Bold left] Organization Name          [Right-aligned] City, State
[Bold left] Position Title             [Right-aligned] Month Year – Month Year
• Bullet starting with action verb, describing accomplishment with quantified results where possible.
• No personal pronouns. Phrase, not full sentence.
```

**Paragraph style alternative for experience:**
```
[Bold left] Organization Name          [Right-aligned] City, State
[Bold left] Position Title             [Right-aligned] Month Year – Month Year
Short paragraph beginning with action verb. No personal pronouns. Avoid articles for flow.
```

**Skills & Interests (optional):**
```
Technical: [list]
Language: [list with fluency levels]
Interests: [list]
```

### Cover Letter formatting rules:

```
[Date]

[Recipient Name]
[Title]
[Organization]
[Address]

Dear [Name]:

[Opening paragraph — state who you are, position applying for, source of posting, enthusiasm]

[Body paragraph 1 — most relevant experience, specific to the organization's mission]

[Body paragraph 2 — additional experience or skill, quantified where possible]

[Closing paragraph — thank reader, express desire to discuss further]

Sincerely,

[Applicant Name]
```

**Cover letter rules:**
- Address to a specific person whenever possible
- Max one page
- Give concrete examples supporting qualifications
- Use action words throughout
- Reference the job description and connect to credentials
- Match font/size to resume

---

## Step 4 — Technical Implementation

### Dependency: `docx` npm package

Check if already installed, install if not:
```bash
npm list -g docx 2>/dev/null | grep docx || npm install -g docx
```

This skill requires `docx` v9+. No other runtime dependencies beyond Node.js.

### Page setup (US Letter, 1-inch margins)
```javascript
properties: {
  page: {
    size: { width: 12240, height: 15840 },
    margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
  }
}
```

### Name header style
```javascript
new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "FirstName LastName", bold: true, size: 28, font: "Times New Roman" })]
})
```

### Contact line with bullets
```javascript
new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: "Address • City, State • email • phone", size: 22, font: "Times New Roman" })]
})
```

### Section heading with border
```javascript
new Paragraph({
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000", space: 1 } },
  spacing: { before: 240, after: 60 },
  children: [new TextRun({ text: "EDUCATION", bold: true, size: 24, font: "Times New Roman" })]
})
```

### Two-column line (org name left, city right) — use tab stops
```javascript
new Paragraph({
  tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
  children: [
    new TextRun({ text: "Organization Name", bold: true, size: 22, font: "Times New Roman" }),
    new TextRun({ text: "\t", size: 22 }),
    new TextRun({ text: "City, State", size: 22, font: "Times New Roman" })
  ]
})
```

### Bullets (NEVER use unicode — use numbering config)
```javascript
numbering: {
  config: [{
    reference: "resume-bullets",
    levels: [{
      level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 360, hanging: 360 } } }
    }]
  }]
}
// Then in paragraphs:
new Paragraph({
  numbering: { reference: "resume-bullets", level: 0 },
  children: [new TextRun({ text: "Action verb + achievement.", size: 22, font: "Times New Roman" })]
})
```

---

## Step 5 — Output

1. Generate the `.docx` file(s) to `/home/claude/` first
2. Validate by opening the file in Word or running: `python /mnt/skills/public/docx/scripts/office/validate.py output.docx` (only if that path exists in the environment; skip otherwise)
3. Copy final file to `/mnt/user-data/outputs/`
4. Present files to user with `present_files`
5. Remind the user to review all content for accuracy — verify dates, titles, and wording

---

## ⚠️ FINAL REMINDER — NO HALLUCINATION

**DO NOT hallucinate, create, infer, or assume ANY information about the person's skills,
experience, education, achievements, or background. If something wasn't explicitly stated
by the person, do not include it. Ask if you need more information.**
