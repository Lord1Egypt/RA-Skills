# Phase 0: Requirements Confirmation Full Flow

## Trigger Conditions

User's first writing request ("I want to write xxx"/"help me write a feasibility report"/"write a xxx report")

## Four-Step Confirmation Flow

### Step 1 — Confirm Writing Topic

```
Please tell me the core information for this document:

1. What is the document topic?
   (e.g., XX City People's Hospital Medical Asset Refined Management Solution)
2. What type of document is it?
   (e.g., Feasibility Study Report / Technical Proposal / Business Plan)
3. Who is the primary audience?
   (e.g., Hospital Management / Superior Regulatory Authority / Investors)
4. Overall style?
   (e.g., Professional & Rigorous / Concise & Clear)
5. Any special requirements or constraints?
   (e.g., Must include budget section / No more than 10 chapters, etc.)
```

### Step 2 — Confirm Writing Background

```
Please provide or describe the background information for this project/topic:

1. What is the project background?
   (e.g., Current hospital asset management status, problems faced)
2. What are the construction goals?
   (e.g., Improve asset utilization rate, control costs)
3. Any specific industry background?
   (e.g., National policies, industry trends)
```

### Step 3 — Provide Reference Materials (Most Important)

```
Please provide reference materials related to this writing task (provide at least one):

A. Upload file: Send local file path or paste content directly
B. Feishu document: Provide document name or link (I will search via RAG)
C. Paste directly: Send reference text directly to this assistant
D. Not provided for now (skip, write using general background knowledge)

⚠️ Strongly recommend providing reference materials!
The more reference material, the more business-aligned the content, the higher the output quality.
Reference materials will be injected as the primary RAG knowledge source into each chapter's writing context.
```

### Step 4 — Outline Confirmation

After planner outputs the outline, display it to the user for confirmation:

```
📋 Planning outline generated. Please confirm the following chapter structure:

Project: XX City People's Hospital Medical Asset Full Lifecycle Refined Management Solution
Type: Feasibility Study Report | Audience: Hospital Management

Chapter Outline:
1. Chapter 01 Project Overview (Batch A, ~2500 words)
2. Chapter 02 Construction Background & Necessity (Batch A, ~3000 words)
...

Please confirm:
 A. Outline OK, start writing
 B. Need to adjust outline (please specify which chapters need modification/addition/deletion)
 C. Cancel this writing task
```

## Saving Reference Materials

After user confirmation, save reference materials to `F:/agent/chapters/reference_material.txt`:
```python
with open('F:/agent/chapters/reference_material.txt', 'w', encoding='utf-8') as f:
    f.write(reference_text)
```
