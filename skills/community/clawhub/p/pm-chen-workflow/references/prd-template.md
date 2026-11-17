# AI-Friendly PRD Template

This template produces PRDs optimized for AI-to-dev handoff. Every field is structured so that developers can consume it without additional clarification meetings.

## Structure

### 1. Meta
- Feature name:
- Version:
- Author:
- Date:
- Status: [draft / review / approved]

### 2. Problem Statement (≤150 words)
What user pain are we solving? What evidence supports this?

Avoid solution language. Describe the user's current state and the gap.
Bad: "Users need a notification center"
Good: "Users miss time-sensitive alerts because notifications are scattered across email, SMS, and in-app banners with no unified view. Support tickets related to missed alerts average 15/day."

### 3. Target Users
- Primary persona:
- Secondary persona (if any):
- What they do today to solve this problem:

### 4. Core Scenarios (3-5 scenarios)
Each scenario: "When [context], the user needs to [action], so that [outcome]."

Example:
- When a course is about to start, the teacher needs to see last-minute cancellations in one place, so that they can adjust the lesson plan before class begins.

### 5. Page List
- Page 1: [name] - [purpose]
- Page 2: [name] - [purpose]
... (5-15 pages for MVP)

### 6. Key Interaction Flows
Each flow: Start page → intermediate pages → end page, with trigger conditions.

Example:
Flow 1: Dashboard → tap "New Course" → Course creation form → fill fields → submit → return to Dashboard with new course card

### 7. Acceptance Criteria
For each scenario, write testable criteria:
- [ ] Given [condition], when [action], then [expected result]
- [ ] Edge case: what happens with 0 items
- [ ] Edge case: what happens with 10,000+ items
- [ ] Error state: what happens on network failure
- [ ] Loading state: what shows while waiting

### 8. Success Metrics
- Primary metric: [e.g., reduce support tickets by 30%]
- Baseline:
- Target:
- Measurement method:

### 9. Out of Scope
Explicitly list what is NOT included in this version.

### 10. API Interface Definitions
See api-spec-template.md for detailed format.
Key endpoints needed:
- Endpoint:
- Method:
- Request body:
- Response body:
- Error responses:
