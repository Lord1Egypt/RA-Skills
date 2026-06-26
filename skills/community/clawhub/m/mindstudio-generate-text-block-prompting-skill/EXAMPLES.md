# Examples — MindStudio Generate Text Block Prompting Skill

Two fully worked scenarios showing what this skill produces: one text output, one JSON output.

---

## Example 1: Text Output — Customer Support Reply

**Scenario:** A customer support agent. The user sends a message and account details have already been pulled from a previous block. This Generate Text block writes a helpful, personalized reply shown directly to the user.

**Available variables:**
- `userMessage` — the customer's message (text)
- `accountDetails` — JSON object with `name`, `plan`, `lastOrderDate`

**Block settings:**
- Output Behavior: `Display to User`
- Output Schema: `Text (Default)`

**Prompt:**

```
<customerMessage>
  {{userMessage}}
</customerMessage>

<accountContext>
  Name: {{accountDetails.name}}
  Plan: {{accountDetails.plan}}
  Last Order Date: {{accountDetails.lastOrderDate}}
</accountContext>

## Task
You are a friendly and knowledgeable customer support agent. Read the customer's message and write a clear, helpful reply that directly addresses their question or issue.

## Rules
- Address the customer by their first name ({{accountDetails.name}})
- Reference their plan or last order only if it is relevant to their message
- Keep the tone warm, professional, and concise
- Do not make up information you don't have
- If you cannot resolve the issue, tell them you are escalating to a human agent

## Format
Write your reply as a single block of plain text, 2-4 sentences. No bullet points, no headers.
```

---

## Example 2: JSON Output — Job Application Analyzer

**Scenario:** A job application assistant. The user pastes a job description and their resume text. This block analyzes both and outputs a structured result — a match score, strengths, gaps, and a cover letter opener — saved to a variable for a downstream Display Content block.

**Available variables:**
- `jobDescription` — the job posting text (text)
- `resumeText` — the candidate's resume (text)

**Block settings:**
- Output Behavior: `Assign to Variable` → `analysisResult`
- Output Schema: `JSON`

**Prompt:**

```
<jobDescription>
  {{jobDescription}}
</jobDescription>

<resume>
  {{resumeText}}
</resume>

## Task
You are an expert career coach and recruiter. Analyze how well the candidate's resume matches the job description above.

## Instructions
- Read the job description carefully and identify the key requirements: skills, experience, qualifications
- Read the resume and assess how well the candidate meets each requirement
- Assign an overall match score from 0 to 100
- Identify the candidate's top 3 strengths relative to this role
- Identify the top 3 gaps or missing qualifications
- Write a 3-sentence cover letter opener tailored to this specific role, written in first person as the candidate

## Rules
- Be honest and specific — reference actual content from both documents
- Do not invent skills or experience not present in the resume
- Keep each strength and gap to one clear sentence

Respond only with valid JSON. No explanation, no markdown, no code fences.

JSON Output:
{
  "score": 0,
  "strengths": ["string", "string", "string"],
  "gaps": ["string", "string", "string"],
  "summary": "string"
}
```

**Sample Output — paste into the MindStudio block setting:**

```json
{
  "score": 78,
  "strengths": [
    "5 years of hands-on experience with React and TypeScript directly matches the core stack listed in the job description.",
    "Led a cross-functional team of 6 at a previous role, satisfying the team leadership requirement.",
    "Demonstrated history of shipping products under tight deadlines, aligning with the fast-paced startup environment described."
  ],
  "gaps": [
    "No experience with AWS infrastructure, which is listed as a required qualification.",
    "Resume does not mention any exposure to GraphQL, listed as preferred.",
    "Lacks a formal computer science degree, which the posting lists as a preference."
  ],
  "summary": "With five years building React-powered products at scale, I've developed a deep instinct for clean, performant interfaces that users actually love. At my last company, I led a team that shipped a redesigned checkout flow that reduced drop-off by 22%. I'm excited to bring that same product focus to this role at your company."
}
```

**Accessing fields downstream (e.g., in a Display Content block):**

```
Match Score: {{analysisResult.score}}
Cover Letter Opener: {{analysisResult.summary}}
Top Strength: {{analysisResult.strengths.[0]}}
First Gap: {{analysisResult.gaps.[0]}}
```

---

## Example 3: JSON Output — Lead Extraction from Scraped HTML

**Scenario:** A lead enrichment agent running via the Browser Extension. A page has been scraped and the raw HTML is available. This block extracts a list of people from the page as a JSON array, which then feeds into a Run Workflow block that enriches each person one at a time.

**Available variables:**
- `rawHtml` — the full HTML of the scraped page (text)

**Block settings:**
- Output Behavior: `Assign to Variable` → `people`
- Output Schema: `JSON`

**Prompt:**

```
<pageContent>
  {{rawHtml}}
</pageContent>

## Task
Extract all people mentioned in the page content above.

For each person, return:
- First name
- Last name
- Job title
- Company name
- LinkedIn profile URL (no query parameters)

## Rules
- Only extract people from the main content of the page — ignore navigation, ads, or sidebar content
- If a LinkedIn URL is not available, use null
- Do not include yourself or the page owner in the list

Respond only with a valid JSON array. No explanation, no markdown, no code fences.

JSON Output:
[
  {
    "firstName": "string",
    "lastName": "string",
    "jobTitle": "string",
    "company": "string",
    "linkedin": "string"
  }
]
```

**Sample Output — paste into the MindStudio block setting:**

```json
[
  {
    "firstName": "Sarah",
    "lastName": "Chen",
    "jobTitle": "VP of Marketing",
    "company": "Acme Corp",
    "linkedin": "https://www.linkedin.com/in/sarahchen"
  }
]
```

**Run Workflow block configuration:**
- Iterator: `JSON Array Input (Advanced)`
- Input Array: `{{people}}`
- Launch Variable: `person : {{item}}`

**Accessing fields in the sub-workflow prompt:**

```
Find the work email for {{person.firstName}} {{person.lastName}},
who is the {{person.jobTitle}} at {{person.company}}.
```
