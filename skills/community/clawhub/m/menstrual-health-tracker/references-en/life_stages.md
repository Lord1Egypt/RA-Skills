# Multi-Life-Stage Adaptation Logic

## Stage Identification

The user profile (`user_profile.life_stage`) is the single authoritative source for stage identification. It is explicitly set during first-time onboarding via the questionnaire, and updated thereafter through the stage transition logic.

**Strictly prohibited: inferring stage from age alone** — must be based on user self-reporting or profile data.

Complete questionnaire design and stage transition logic can be found in `references/user_profile.md` (or `references-en/user_profile.md` for English).

### Recognition Signals & Profile Mapping

| Stage | Identifier | Recognition Signal | Key Tracking Dimensions | Required W1 Fields |
|-------|-----------|-------------------|------------------------|-------------------|
| Premenarche | premenarche | User explicitly states hasn't had first period | Physical development, knowledge preparation | life_stage |
| Menstruating | menstruating | Has cycle records, selected A/B/C | Cycle regularity, symptoms, ovulation | life_stage, typical_cycle_length, typical_period_length |
| TTC | ttc | User mentions trying to conceive | Ovulation day, BBT, fertile window | life_stage, typical_cycle_length |
| Pregnant | pregnant | User mentions pregnancy/due date | Gestational weeks, symptoms, weight | life_stage, due_date or pregnancy_week |
| Postpartum | postpartum | User mentions childbirth/breastfeeding | Recovery, breastfeeding, mood | life_stage, postpartum_weeks, is_breastfeeding |
| Perimenopause | perimenopause | User mentions hot flashes/irregularity (40+) | Cycle changes, hot flashes, mood | life_stage, last_period_date |
| Postmenopause | postmenopause | User confirms 12 months without period | Bone, cardiovascular, overall | life_stage, menopause_confirmed=true |

## Stage-Specific Logic

### premenarche
- **Data tracking**: Do not track cycles; track physical changes instead (height, weight, breast development, and other milestones)
- **Content focus**: Menstrual education, body awareness, emotional preparation
- **Interaction tone**: Warm and encouraging, like an older sister/aunt, not a doctor
- **Parent perspective**: If a parent is using the skill, provide "How to talk to your daughter about menarche" guides
- **Special attention**: Do not over-medicalize; maintain a natural, positive narrative

### menstruating
- **Data tracking**: Complete cycle data, symptoms, mood, physical signs, events
- **Analysis focus**: Cycle regularity, symptom patterns, prediction, health optimization
- **Content focus**: Cycle-syncing lifestyle, menstrual self-care, ovulation awareness
- **Alert focus**: Cycle abnormalities, severe PMS/PMDD signals, endometriosis/PCOS risk indicators

### ttc (Trying to Conceive)
- **Data tracking**: BBT required, cervical mucus, ovulation test results, intercourse records
- **Analysis focus**: Precise ovulation day prediction, fertile window, luteal function assessment
- **Content focus**: Fertility window optimization, lifestyle impact on fertility, stress management
- **Boundary**: Do not promise pregnancy outcomes; emphasize "optimize health = optimize fertility"
- **Sensitive handling**: If user expresses anxiety, provide psychological support, remind that "TTC is a journey"

### pregnant
- **Data tracking**: Gestational weeks (calculated from due date), symptoms, weight, fetal movement, contractions
- **Analysis focus**: Pregnancy symptom tracking, weight gain curve, prenatal checkup milestone reminders
- **Content focus**: Prenatal nutrition, safe exercise, emotional changes, birth preparation
- **Strict boundary**: Any abnormality (bleeding, severe pain, reduced fetal movement) → immediately recommend contacting obstetrician
- **Safety first**: All recommendations include "please consult your obstetrician"

### postpartum
- **Data tracking**: Lochia, breastfeeding records, wound recovery, mood screening
- **Analysis focus**: Postpartum recovery progress, breastfeeding & period return, mood tracking
- **Content focus**: Pelvic floor recovery, nutritional supplementation, sleep strategies, mother-baby bonding
- **Special attention**: Postpartum depression screening (simplified EPDS), "baby blues" vs PPD distinction
- **Empathy focus**: Acknowledge postpartum challenges; do not impose "perfect mom" pressure

### perimenopause
- **Data tracking**: Cycle changes (may suddenly shorten/lengthen/skip), hot flash frequency, sleep, mood, weight
- **Analysis focus**: Cycle variability trends, symptom burden, quality of life impact
- **Content focus**: Hormonal change education, symptom management (non-pharmacological + pharmacological options), bone protection, cardiovascular health
- **De-stigmatization**: This is a natural transition, not "aging" or "losing femininity"
- **Empowerment**: Many women experience new freedom and creativity after menopause

### postmenopause
- **Data tracking**: Weight, bone density (if available), blood pressure, blood lipids, overall symptoms
- **Analysis focus**: Health risk assessment, lifestyle optimization, annual checkup tracking
- **Content focus**: Bone health (calcium + vitamin D + exercise), cardiovascular protection, urogenital health, cognitive maintenance
- **Positive perspective**: Health management for a new stage; focus on overall vitality
- **Special attention**: Abnormal bleeding (postmenopausal bleeding requires medical evaluation), osteoporosis risk

## Stage Transition Detection

When the following signals are detected, gently ask the user whether to switch stages:
- 3 consecutive months without cycle records → ask whether pregnant/entering perimenopause
- User adds "due date" information → suggest switching to pregnancy mode
- User mentions "childbirth" → suggest switching to postpartum mode
- Age > 40 + increasing cycle variability → mention perimenopause possibility (do not force switch)
