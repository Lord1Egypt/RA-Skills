# User Profile System

## Design Principles

The user profile is the highest-priority context for the entire skill. **All analysis, recommendations, tone, and tracking dimensions must be personalized based on profile data.**

Profile fields are divided into three weight tiers:
- **W1 (Required, High Weight)**: Directly determines the skill's behavior patterns; all functionality depends on these fields
- **W2 (Recommended, Medium Weight)**: Significantly improves recommendation quality; precision increases dramatically after collection
- **W3 (Optional, Supplementary)**: Used for deep personalization; collected when the user is willing to share

---

## First-Time Use: Onboarding Questionnaire

### Question Design Principles
- Warm, direct, like chatting with a friend, not filling out a hospital form
- Ask at most 2-3 questions at a time, in priority batches
- Allow "skip for now" but mark as pending
- Extract profile information from natural conversation (e.g., "I'm pregnant" → auto-detect stage)

---

### Batch 1 Questions (Required for First-Time Use, W1 Fields)

**Q1. Hi! Before we begin, I'd like to understand your current situation so I can give you the most relevant suggestions.**

```
Please select the description closest to your current situation:

A. Haven't had my first period yet (waiting for menarche)
B. Regular menstrual cycles
C. Irregular periods
D. Trying to conceive
E. Currently pregnant
F. Recently gave birth (postpartum recovery)
G. Periods becoming lighter / increasingly delayed (possibly menopause)
H. Postmenopausal (no period for over 1 year)
I. Other situation (please describe)
```

→ Field: `life_stage` (W1)
→ Mapping: A=premenarche, B=menstruating, C=menstruating_irregular, D=ttc, E=pregnant, F=postpartum, G=perimenopause, H=postmenopause

---

**Q2. (If B/C/D selected) Roughly how many days between your periods? And how many days do they usually last?**

```
Example: "About 28 days apart, lasts 4-5 days"
→ If unsure, "irregular" is also fine
```

→ Fields: `typical_cycle_length` (W1), `typical_period_length` (W1)

---

**Q3. (If E selected) Roughly how many weeks pregnant are you? Or what's your due date?**

```
→ Fields: `pregnancy_week` (W1), `due_date` (W1)
```

**Q3. (If F selected) How old is your baby? Are you breastfeeding?**

```
→ Fields: `postpartum_weeks` (W1), `is_breastfeeding` (W2)
```

**Q3. (If G/H selected) Are you still having periods? Roughly how long since your last one?**

```
→ Fields: `last_period_date` (W1), `menopause_confirmed` (W2)
```

---

### Batch 2 Questions (After First Recording, W2 Fields)

After the user completes their first recording, naturally segue in:

**"Let me learn a few more things — it'll help me give you much more precise suggestions —"**

```
Q4. Roughly how old are you? (Enter a number, or choose "prefer not to say")
→ Field: age (W2)

Q5. Have you ever been diagnosed with any of the following?
  □ Polycystic Ovary Syndrome (PCOS)
  □ Endometriosis
  □ Uterine fibroids
  □ Thyroid issues (hyperthyroidism/hypothyroidism)
  □ Anemia
  □ None of the above
  □ Unsure / prefer not to answer
→ Field: medical_conditions (W2)

Q6. Are you taking any long-term medications or hormonal treatments?
(e.g., birth control pills, progesterone, thyroid medication, antidepressants)
→ Field: medications (W2)
```

---

### Batch 3 Questions (Deep Personalization — When User Initiates or Mentions Related Topics)

**W3 fields, collected on demand:**

```
Q7. What's your typical sleep schedule (bedtime to wake time)?
→ Field: sleep_schedule (W3)

Q8. How often do you exercise?
(Rarely / 1-2x per week / 3-5x per week / Almost daily)
→ Field: exercise_frequency (W3)

Q9. How stressed have you been lately? (1-5 scale)
→ Field: stress_level (W3)

Q10. What's your typical diet like?
(Standard / Vegetarian / Calorie-restricted / Special diet)
→ Field: diet_type (W3)

Q11. Height and weight? (Optional)
→ Fields: height, weight (W3)
```

---

## Profile Data Structure

```json
{
  "user_profile": {

    // W1 Fields — Must collect first
    "life_stage": "menstruating",
    "typical_cycle_length": 28,
    "typical_period_length": 5,
    "profile_version": "1.0",
    "created_at": "2024-01-01",
    "last_updated": "2024-06-09",

    // Pregnancy-specific W1
    "due_date": null,
    "pregnancy_week": null,

    // Postpartum-specific W1
    "postpartum_weeks": null,
    "is_breastfeeding": null,

    // Perimenopause/Postmenopause W1
    "last_period_date": null,
    "menopause_confirmed": false,

    // W2 Fields — Recommended
    "age": null,
    "medical_conditions": [],
    "medications": [],

    // W3 Fields — Optional
    "sleep_schedule": null,
    "exercise_frequency": null,
    "stress_level": null,
    "diet_type": null,
    "height": null,
    "weight": null,

    // System Fields
    "profile_completeness": 0.3,
    "pending_questions": ["Q4", "Q5", "Q6"],
    "stage_history": [
      { "stage": "menstruating", "since": "2024-01-01", "notes": "" }
    ]
  }
}
```

---

## Stage Transition Logic

### Transition Signal Words

| Signal Word / Scenario | Target Stage | Transition Priority |
|------------------------|-------------|-------------------|
| "I'm pregnant" / "tested positive" / "ultrasound confirmed" | pregnant | Immediate switch |
| "I gave birth" / "just finished postpartum confinement" / "baby was born" | postpartum | Immediate switch |
| "My period is back" (postpartum/post-pregnancy) | menstruating | Confirm first |
| "Started trying to conceive" / "want to have a baby" | ttc | Switch + adjust tracking dimensions |
| "I've stopped menstruating" / "no period for a year" | postmenopause | Confirm first |
| "Started having hot flashes" / "periods increasingly irregular (40+)" | perimenopause | Gentle inquiry |
| User states age 10-12, never had a period | premenarche | Confirm first |

### Transition Flow

**Auto-detect → Gentle confirmation → Update profile → Adjust service mode**

```
1. Detect transition signal
2. Gentle confirmation: "It sounds like your situation has changed — are you saying [new stage]?"
3. User confirms → Execute:
   a. Update life_stage field
   b. Record in stage_history (preserve historical stage records)
   c. Collect new stage W1 supplementary fields
   d. Adjust all subsequent recommendation weighting and tone
   e. Inform user: "I've switched to [new stage] mode. From now on, I'll provide matching suggestions ✨"
4. Do not force: keep original stage if user declines confirmation
```

---

## Profile Field Weighting Impact on Recommendations

### life_stage (W1 — Highest Weight)

| Stage | Recommendation Adjustment | Tracking Focus | Prohibited Content |
|-------|--------------------------|----------------|-------------------|
| premenarche | Educational perspective, avoid medical jargon | Development milestones | Do not analyze "cycle abnormalities" |
| menstruating | Full-dimension analysis, regularity optimization | Cycle/symptoms/prediction | None |
| ttc | Ovulation prediction weighted highest | BBT/ovulation/fertile window | Do not promise pregnancy outcomes |
| pregnant | Strict safety boundaries | Gestational weeks/symptoms/fetal movement | All recommendations must include "consult your obstetrician" |
| postpartum | High psychological support weighting | Recovery/breastfeeding/mood | Do not set "perfect recovery" standards |
| perimenopause | De-stigmatizing narrative | Cycle changes/menopause symptoms | Do not use negative terms like "aging" |
| postmenopause | Overall health management | Bone/cardiovascular/abnormal bleeding | Postmenopausal bleeding must trigger medical referral |

### medical_conditions (W2 — Medium Weight)

| Diagnosis | Recommendation Adjustment |
|-----------|--------------------------|
| PCOS | Ovulation prediction note: "LH surge may be inaccurate, consider ultrasound monitoring"; recommend adjusting carb ratio; watch for high-sugar foods |
| Endometriosis | High dysmenorrhea management weighting; not recommended: high caffeine; watch for deep dyspareunia and non-menstrual pelvic pain |
| Uterine fibroids | Monitor flow changes; heavy flow: recommend medical consultation |
| Thyroid issues | Prioritize thyroid impact when cycles are abnormal; recommend regular T3/T4 testing |
| Anemia | High flow tracking weighting; recommend iron-rich diet; heavy bleeding: emphasize medical referral |

### medications (W2 — Medium Weight)

| Medication | Recommendation Adjustment |
|-----------|--------------------------|
| Birth control / Hormonal | Ovulation prediction meaningless (note explanation); cycle data reference meaning differs |
| Thyroid medication | Monitor relationship between cycle changes and medication dosage |
| Antidepressants | Consider medication factors in mood tracking; do not recommend self-discontinuation |

### age (W2 — Reference Weight)

| Age Range | Recommendation Tendency |
|-----------|------------------------|
| < 20 | Cycle irregularity is normal; generous normal range |
| 20-35 | Standard reference values, normal assessment |
| 35-45 | Begin noting fertility preservation (if relevant), mention perimenopause possibility |
| > 45 | High perimenopause screening weight; add bone health recommendations |

---

## Profile Completeness Prompts

`profile_completeness` ranges from 0-1.0, updated after each field supplement:

- **0.0-0.3 (Basic)**: Only life_stage. Show basic features, gently prompt at key moments
- **0.3-0.6 (Moderate)**: Has basic cycle data and age. Most features available, moderate recommendation quality
- **0.6-0.8 (Good)**: Has medical history and medications. Highly personalized recommendations
- **0.8-1.0 (Complete)**: All key fields filled. Extremely precise recommendations, optimal experience

**Prompt templates (use at appropriate moments):**
- "Just one more detail and I can give you even more precise suggestions — have you been diagnosed with any gynecological conditions?"
- "Your profile could be even more complete. Are you taking any long-term medications? (This affects how I interpret your cycle data)"
