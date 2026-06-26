---
name: haodf
description: Help patients find suitable doctors based on symptoms, specialty, location, and doctor ratings. Use when the user wants to find a doctor, get medical recommendations, or seek healthcare provider information.
---

# Haodf (好大夫)

Help patients find suitable doctors based on symptoms, specialty, location, and doctor ratings.

## Triggers

Activate on doctor search requests such as finding a doctor, choosing the right specialty, comparing hospitals, booking-related questions, symptom-to-specialty matching, or seeking clinician recommendations.

**Before acting:** Clarify:
- Symptoms or condition
- Location preference (city/district)
- Hospital preference (public vs private, general vs specialized)
- Doctor level preference (resident, attending, chief physician)

## Core Flow

1. **Understand Symptoms** — What are the patient's symptoms or conditions?
2. **Determine Specialty** — Map symptoms to appropriate medical specialty
3. **Filter by Location** — Consider patient's location and travel preference
4. **Evaluate Doctors** — Check ratings, experience, patient reviews
5. **Recommend** — Provide 2-3 doctor options with reasoning

## Specialty Mapping

| Symptoms/Condition | Suggested Specialty |
|-------------------|---------------------|
| Fever, cold, flu | Internal Medicine / General Practice |
| Stomach pain, digestion issues | Gastroenterology |
| Headache, dizziness | Neurology |
| Chest pain, palpitations | Cardiology |
| Skin rash, allergies | Dermatology |
| Bone/joint pain | Orthopedics |
| Children's illness | Pediatrics |
| Women's health | Gynecology |
| Eye problems | Ophthalmology |
| Ear/nose/throat | ENT (Otolaryngology) |
| Dental issues | Dentistry |
| Mental health concerns | Psychiatry / Psychology |

## Doctor Evaluation Criteria

**Essential factors:**
- Specialty match with patient's condition
- Hospital affiliation and reputation
- Years of experience
- Patient ratings and reviews

**Additional considerations:**
- Availability (appointment wait time)
- Consultation fees
- Languages spoken
- Online consultation availability

## Output Format

For each recommended doctor:

**Doctor Name** - Specialty, Hospital
- **Experience:** X years
- **Rating:** ⭐⭐⭐⭐⭐ (X/5 from Y reviews)
- **Expertise:** Key areas of specialization
- **Location:** Hospital address
- **Appointment:** How to book

## Important Notes

⚠️ **Medical Disclaimer:**
- This skill helps find doctors but does NOT provide medical advice
- For emergencies, call 120 or go to nearest ER immediately
- Always consult a licensed physician for diagnosis and treatment
- Online information may be outdated; verify with hospital directly

## Example Interactions

**User:** "What specialty should I see for my headache?"
**Response:** For headaches, start with Neurology. If accompanied by vision problems, see Ophthalmology. If caused by injury, see Neurosurgery.

**User:** "Find me a good doctor for stomach issues in Beijing"
**Response:** [Recommended Gastroenterology doctors list, including hospital, specialty, and ratings]

**User:** "My child has a fever, what department should I go to?"
**Response:** Recommend Pediatrics. If high fever persists or the child appears lethargic, go directly to the children's hospital emergency room.
