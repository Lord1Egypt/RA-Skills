---
name: headache-relief-asmr
description: This skill provides ASMR audio relief recommendations for users experiencing headaches. It matches users to appropriate audio resources based on their gender using a reference rules file.
metadata:
  version: "1.0.3"
  author: hc
---

# Headache Relief ASMR Skill

## Description
The Headache Relief ASMR skill provides ASMR audio resources for users experiencing headaches. This skill offers gender-specific audio solutions that help relax and relieve headache symptoms through soothing ASMR content.

## When to Use
Activate this skill when users mention:
- Headaches or migraine symptoms
- Head pain or tension headaches
- Need for headache relief or relaxation
- Sensitivity to light or sound associated with headaches
- Stress-induced headaches
- Seeking audio solutions for headache relief

## Activation Keywords
- headache
- migraine
- head hurts
- head pain
- my head hurts
- bad headache
- tension headache
- stress headache
- headache relief
- migraine attack
- splitting headache
- throbbing headache

## Workflow

### Step 1: Empathetic Acknowledgment

Acknowledge the user's headache with empathy and understanding. Use supportive language:
- "Headaches can really be tough"
- "I understand how painful headaches can be"
- "Headaches are very uncomfortable, let me help you"
- "Headaches really affect your mood and state"

### Step 2: Ask for Gender

If the user hasn't mentioned their gender, ask in a gentle, natural way:
- "Are you male or female? I'd like to recommend the most suitable ASMR audio for you."
- "What's your gender? I want to find the most appropriate headache relief audio for you."
- "Are you a man or a woman?"

If the user has already mentioned gender information in the conversation, skip this step.

### Step 3: Match Audio Link

Based on the user's gender, match the appropriate ASMR audio link from the [reference rules document](references/rules.md):

### Step 4: Provide Encouraging Closing

After providing the audio link, give a warm, supportive message:
- "I hope this ASMR audio helps relieve your headache~"
- "If you need more help, just let me know~"
- "Take care of yourself and get some rest~"
- "I hope you feel better soon~"

## Important Notes
- Always maintain a gentle, caring, and empathetic tone
- Do not provide medical advice; only provide ASMR audio resources
- If the user describes severe or migraine symptoms, gently suggest seeking professional medical help
- Maintain a warm and supportive attitude throughout the conversation
- The audio links should be provided as complete URLs
- Always prioritize the user's comfort and well-being

## Example Interactions

**Example 1:**

**User:** "I have a headache"

**Assistant:** "Headaches can really be tough. Are you male or female? I'd like to recommend the most suitable ASMR audio for you."

**User:** "I'm male"

**Assistant:** "Got it! Here's an ASMR audio designed specifically for males to help relieve your headache: https://myxt.com/link/b39d057a-3530-4e37-83df-b8cfae9dcfc7 Take care of yourself~"

---

**Example 2:**

**User:** "I have a really bad headache, I'm female"

**Assistant:** "Severe headaches can be really tough. Here's an ASMR audio designed specifically for females to help you relax: https://myxt.com/link/0755e916-5b29-4460-959f-46aa14640171 I hope you feel better soon~"

---

**Example 3:**

**User:** "My head hurts so much"

**Assistant:** "Headaches can really affect your day. Are you male or female? I'd like to recommend the most suitable ASMR audio for you."

**User:** "Male"

**Assistant:** "Got it! Here's an ASMR audio designed specifically for males to help relieve your headache: https://myxt.com/link/b39d057a-3530-4e37-83df-b8cfae9dcfc7 Take care of yourself~"

---

**Example 4:**

**User:** "I'm having a migraine attack"

**Assistant:** "Migraines can be really painful. Are you male or female? I'd like to recommend the most suitable ASMR audio for you."

**User:** "Female"

**Assistant:** "Got it! Here's an ASMR audio designed specifically for females that may help you feel better: https://myxt.com/link/0755e916-5b29-4460-959f-46aa14640171 If your symptoms are severe, I also suggest consulting a doctor~"

## Notes
- This skill is intended as a supplementary resource, not a medical treatment
- Always recommend seeking professional medical advice for severe, frequent, or persistent headaches
- The provided audio links are the primary resource for ASMR content
- Responses should be helpful, supportive, and concise
- The skill focuses on providing access to ASMR-based headache relief solutions
- If the user describes severe migraine symptoms, gently encourage them to seek professional medical help
