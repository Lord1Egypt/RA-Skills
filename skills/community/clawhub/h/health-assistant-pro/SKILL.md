---
name: health-assistant-pro
version: 1.5.0
description: Professional health assistant with medical report analysis, evidence-based supplement recommendations (100+ supplements), machine learning personalization, external API integration, and quality verification. Features include health report storage with trend analysis, ML-powered recommendations, Examine.com and ConsumerLab integration, brand quality testing, timing optimization, interaction checking, blockchain traceability framework, and comprehensive wellness guidance.
---

# Personal Health Manager 🏥

Your comprehensive personal health companion for daily wellness management.

## When to Use

Use this skill whenever the user mentions:
- Health tracking, records, or data
- Medication management or reminders
- Symptoms, feeling unwell, or health concerns
- Exercise, fitness, or workout advice
- Diet, nutrition, or meal planning
- Travel preparation or trip planning
- First aid or emergency health advice
- General wellness questions

---

## User Profile Setup

Before providing personalized advice, always check or ask for:

### Basic Information
- **Age**: Required for exercise/diet recommendations
- **Gender**: Important for certain health considerations
- **Weight & Height**: For BMI calculation
- **Medical History**: Chronic conditions, past surgeries
- **Current Medications**: For drug interaction checks
- **Allergies**: Drug, food, environmental
- **Lifestyle**: Sedentary, active, smoking, alcohol

### Health Profile Template
```
👤 Profile:
- Name: [optional]
- Age: ___
- Gender: ___
- Height: ___cm
- Weight: ___kg
- BMI: ___ (auto-calculated)
- Blood Type: ___
- Allergies: ___
- Medical Conditions: ___
- Current Medications: ___
- Emergency Contact: ___
```

---

## Core Features

### 1. Health Data Recording 📊

Track and record various health metrics based on user profile:

#### Blood Pressure 💉
| Category | Systolic | Diastolic |
|----------|----------|-----------|
| Normal | <120 | <80 |
| Elevated | 120-129 | <80 |
| Stage 1 HTN | 130-139 | 80-89 |
| Stage 2 HTN | ≥140 | ≥90 |
| Crisis | >180 | >120 ⚠️ |

#### Blood Glucose 🍬
| Status | Fasting | 2h Post-Meal |
|--------|---------|---------------|
| Normal | <100 | <140 |
| Prediabetes | 100-125 | 140-199 |
| Diabetes | ≥126 | ≥200 |

#### Heart Rate ❤️
| Age Group | Normal Resting | Max Heart Rate |
|-----------|----------------|----------------|
| 20-29 | 60-100 | 190-200 |
| 30-39 | 60-100 | 180-190 |
| 40-49 | 60-100 | 170-180 |
| 50-59 | 60-100 | 160-170 |
| 60+ | 60-100 | 150-160 |

#### BMI Calculator ⚖️
| Category | BMI Range |
|----------|-----------|
| Underweight | <18.5 |
| Normal | 18.5-24.9 |
| Overweight | 25-29.9 |
| Obese | ≥30 |

---

### 2. Age-Specific Health Guidance

#### 👶 Children (0-12 years)
**Common Concerns:**
- Growth and development tracking
- Vaccination schedule
- Common childhood illnesses
- Screen time guidelines
- Sleep requirements by age

**Exercise:**
- Active play 60+ minutes/day
- Limit sedentary time

**Sleep:**
| Age | Hours |
|-----|-------|
| 0-3 months | 14-17 |
| 4-12 months | 12-16 |
| 1-2 years | 11-14 |
| 3-5 years | 10-13 |
| 6-12 years | 9-12 |

#### 👦 Teenagers (13-19 years)
**Common Concerns:**
- Puberty and development
- Mental health
- Academic stress
- Screen time balance
- Sports nutrition

**Exercise:**
- 60 min moderate-vigorous daily
- Muscle-strengthening 3x/week

**Nutrition Focus:**
- Calcium (bone growth)
- Iron (especially females)
- Protein for development

#### � adults (20-39 years)
**Common Concerns:**
- Work-life balance
- Stress management
- Preventive care
- Sexual health
- Building healthy habits

**Exercise:**
- 150 min moderate or 75 min vigorous/week
- Muscle-strengthening 2x/week

**Screenings:**
- Annual physical
- Blood pressure
- BMI
- Mental health check

#### 👨 Middle-Aged (40-59 years)
**Common Concerns:**
- Metabolic changes
- Heart health
- Bone density
- Vision changes
- Hormonal changes (menopause/andropause)

**Exercise:**
- 150 min moderate + 2 strength sessions/week
- Balance exercises to prevent falls

**Additional Screenings:**
- Cholesterol (every 5 years)
- Blood glucose (every 3 years)
- Colon cancer screening (45+)
- Bone density (women 65+, men 70+)

#### 👴 Seniors (60+ years)
**Common Concerns:**
- Fall prevention
- Cognitive health
- Medication management
- Chronic disease management
- Nutrition for aging

**Exercise:**
- 150 min moderate (spread out)
- Balance exercises 3x/week
- Strength training 2x/week

**Fall Prevention:**
- Home safety check
- Regular vision/hearing checks
- Review medications that cause dizziness

**Nutrition Focus:**
- Protein (prevent muscle loss)
- Vitamin D + Calcium
- Hydration (thirst decreases with age)
- Fiber (prevent constipation)

---

### 3. Gender-Specific Health

#### 🩺 Women's Health

**Reproductive Health:**
- Menstrual cycle tracking
- Pregnancy planning
- Menopause management
- PCOS/Endometriosis awareness

**Screening Schedule:**
| Age | Screening |
|-----|-----------|
| 21-29 | Pap smear every 3 years |
| 30-65 | Pap + HPV every 5 years |
| 40+ | Mammogram annually |
| 65+ | Bone density scan |

**Common Concerns:**
- Iron deficiency (especially during menstruation)
- Thyroid (women 5x more likely)
- Osteoporosis risk
- Mental health (postpartum, menopause)

**Pregnancy Considerations:**
- Pre-conception care
- Prenatal vitamins (folic acid)
- Weight gain guidelines
- Exercise during pregnancy

**Menopause:**
- Symptoms management
- Hormone therapy considerations
- Heart health post-menopause
- Bone health

#### 🩹 Men's Health

**Screening Schedule:**
| Age | Screening |
|-----|-----------|
| 30+ | Blood pressure |
| 35+ | Cholesterol |
| 45+ | Colon cancer |
| 50+ | Prostate discussion |
| 65+ | Abdominal aortic aneurysm (smokers) |

**Common Concerns:**
- Prostate health
- Testosterone changes
- Heart disease (men 2x higher risk before 65)
- Mental health stigma

**Testosterone:**
- Symptoms of low T: fatigue, low libido, mood changes
- Not always need treatment
- Discuss with doctor

---

### 4. Medication Management 💊

**Features:**
- Add/edit/delete medications
- Track dosage and frequency
- Set medication schedules
- Drug interaction warnings
- Refill reminders
- Medication history

#### Common Medications by Condition

**Hypertension:**
- ACE inhibitors (enalapril, lisinopril)
- ARBs (losartan, valsartan)
- Beta blockers (metoprolol)
- Diuretics (hydrochlorothiazide)

**Diabetes:**
- Metformin
- Sulfonylureas
- SGLT2 inhibitors
- Insulin

**High Cholesterol:**
- Statins (atorvastatin, rosuvastatin)
- Fibrates
- Ezetimibe

**Pain:**
- Acetaminophen
- Ibuprofen
- Naproxen

**Drug Interactions to Watch:**
| Drug A | Drug B | Effect |
|--------|--------|--------|
| Warfarin | Aspirin | Bleeding risk |
| Metformin | Alcohol | Lactic acidosis |
| Statins | Grapefruit | Increased side effects |
| ACE inhibitors | Potassium | High potassium |

---

### 5. Symptom Analysis 🩺

**Process:**
1. Collect symptom details (location, duration, severity)
2. Ask relevant follow-up questions
3. Provide possible causes (informational only)
4. Recommend when to seek medical attention
5. Suggest self-care measures if appropriate

#### Age-Specific Symptom Considerations

**Children:**
- Temperature thresholds lower
- Behavior changes more important than specific symptoms
- Dehydration happens faster
- When to seek care: fever >48h, unable to drink, rash with fever

**Adults:**
- Standard symptom assessment
- Chronic conditions affect presentation
- Medication side effects

**Elderly:**
- Symptoms often less typical
- Confusion can be only sign of infection
- Falls may indicate underlying problem
- Medication side effects more common

#### Red Flags - Seek Immediate Care 🚨
- Chest pain + sweating + pain in arm/jaw
- Difficulty breathing
- Severe bleeding
- Sudden severe headache
- Confusion/loss of consciousness
- Sudden weakness/numbness (stroke)
- High fever + rash
- Severe vomiting + unable to keep fluids down
- Overdose symptoms

---

### 6. Exercise Recommendations 🏃

#### By Age & Fitness Level

**Beginner (Any Age):**
- Start with 10-minute walks
- Chair exercises
- Water aerobics
- Dancing

**Intermediate:**
- Brisk walking 30 min
- Swimming
- Cycling
- Light strength training

**Advanced:**
- Running
- HIIT
- Heavy strength training
- Sports

#### By Health Condition

**High Blood Pressure:**
- Walking, swimming, cycling
- Avoid heavy weightlifting
- Include cool-down

**Diabetes:**
- Check blood sugar before/after exercise
- Carry fast-acting carbs
- Avoid exercise if glucose >250

**Arthritis:**
- Swimming (joint-friendly)
- Stationary bike
- Gentle yoga
- Avoid high-impact

**Heart Disease:**
- Cardiac rehab programs
- Start slow, gradual increase
- Monitor heart rate

---

### 7. Nutrition Advice 🥗

#### By Age

**Children:**
- Make food fun
- Involve in cooking
- Model healthy eating
- Don't force foods

**Adults:**
- Balanced macronutrients
- Meal prep for busy days
- Mindful eating
- Limit processed foods

**Seniors:**
- High protein (1.0-1.2g/kg)
- Vitamin D + B12
- Easy-to-chew foods
- Small, frequent meals

#### By Condition

**High Blood Pressure:**
- Low sodium (<1500mg/day)
- DASH diet
- Limit alcohol

**Diabetes:**
- Consistent carb intake
- High fiber
- Limit simple sugars
- Spread meals throughout day

**High Cholesterol:**
- Low saturated fat
- High fiber
- Omega-3 fatty acids
- Plant sterols

**Weight Management:**
- Calorie awareness (not counting)
- Protein + fiber for fullness
- Limit added sugars
- Drink water before meals

---

### 8. Travel Health Preparation ✈️

#### Pre-Trip Planning

**🧳 Clothing Checklist:**
- Weather-appropriate attire
- Comfortable shoes
- Extra layers
- Rain gear
- Sun protection

**💊 Medications:**
- Regular meds (extra supply)
- Pain relievers
- Anti-diarrheal
- Antihistamines
- Motion sickness pills
- First aid basics
- Destination-specific needs

**🏥 Health Documents:**
- Travel insurance
- Emergency contacts
- Medical history
- Prescription copies
- Vaccination records

#### By Destination

**Tropical:**
- Mosquito protection
- Sun protection
- Water safety
- Food safety

**Cold Climate:**
- Layer clothing
- Protect extremities
- Indoor air dryness
- Frostbite awareness

**High Altitude:**
- Acclimatization days
- Altitude sickness meds
- Extra hydration
- Limited exertion

**Long Flights:**
- Compression socks
- Move every 2 hours
- Stay hydrated
- Avoid alcohol/caffeine

---

## Data Storage

**Local Storage:**
- JSON files in workspace
- Export to CSV/JSON

**Privacy:**
- All data stored locally
- No external servers by default
- Easy export/deletion

---

## Emergency Information Template

```
🚨 EMERGENCY HEALTH CARD
─────────────────────────────────
Name: _________________
Blood Type: ___
Allergies: _________________
Medical Conditions: _________________
Current Medications: _________________

Emergency Contact:
Name: _________________
Phone: _________________

Doctor:
Name: _________________
Phone: _________________

Insurance: _________________
Policy #: _________________
─────────────────────────────────
```

---

## Disclaimer

⚠️ This provides health INFORMATION only, not medical advice. Always:
- Recommend professional medical consultation
- Suggest emergency services for serious symptoms
- Never claim to diagnose conditions
- Encourage regular health checkups
- Respect user privacy with health data

---

## Best Practices

1. **Personalize**: Ask age, gender, conditions before advice
2. **Clarify**: Ask follow-up questions
3. **Context**: Remember conversation history
4. **Empathize**: Be supportive about health concerns
5. **Safety First**: Err on side of caution
6. **Empower**: Teach, don't just give answers
7. **Follow Up**: Check on previous concerns

---

## 9. Drug Regulations & International Travel 🌍

When users ask about bringing medications across borders, traveling with medicines, or drug regulations in different countries, provide accurate information based on official sources.

### General Principles

| Category | Rule |
|----------|------|
| Personal use | "Self-use, reasonable quantity" - typically 1-3 months supply |
| Prescription drugs | Always carry prescription/doctor's note |
| Controlled substances | Check destination country regulations |
| Declare when in doubt | Red channel if uncertain |

### Key Countries/Regions

#### 🇯🇵 Japan
- OTC medicines available in drugstores (drugstore cosmetics)
- Some cold medicines contain codeine/methylephedrine - restricted
- Personal import: up to 2 months supply for personal use
- Declare at customs

#### 🇺🇸 USA
- FDA regulates all drugs entering US
- 3-month supply allowed for personal use
- Controlled substances require prescription
- Some ingredients banned (ephedrine in large quantities)

#### 🇦🇺 Australia
- Strict customs control
- TGA approval needed for some medicines
- Declare all medications
- 3-month supply for prescription drugs

#### 🇸🇬 Singapore
- Very strict drug laws
- Codeine-containing medicines restricted
- Prescription required for many drugs
- Severe penalties for violations

#### 🇨🇦 Canada
- 90-day supply allowed
- Prescription for controlled substances
- Health Canada import rules

#### 🇳🇿 New Zealand
- 3-month supply for prescription drugs
- 1 month for controlled drugs (e.g., pseudoephedrine)
- Declare all medications

#### 🇹🇭 Thailand
- Codeine/morphine controlled
- Prescription needed for sedatives
- Tourist-friendly but check ingredients

#### 🇭🇰 Hong Kong
- 7-day supply for prescription drugs
- RX标志 (registered pharmacy) recommended
- Avoid unregistered "药坊"

### Common Restricted Ingredients

| Ingredient | Concern | Countries |
|-----------|---------|------------|
| Codeine | Controlled narcotic | Most countries |
| Pseudoephedrine | Methamphetamine precursor | USA, Japan, Australia, NZ |
| Ephedrine | Controlled | Many countries |
| Melatonin | Regulated differently | EU, China |
| Traditional Chinese Medicine | Endangered animals | CITES restrictions |

### Special Cases

**Traditional Chinese Medicine:**
- 麝香 (musk), 虎骨 (tiger bone), 犀牛角 (rhino horn) - BANNED
- Other TCM usually OK in reasonable quantities
- Keep original packaging

**Online Pharmacy:**
- Many countries restrict cross-border drug sales
- Personal import usually OK in small quantities
- Requires prescription documentation

---

## 10. Mental Health Support 🧠

When users ask about mental health, psychological issues, emotional wellbeing, or psychological counseling.

### When to Use

Use this section for:
- Depression, anxiety, stress
- Sleep disorders
- Mental health of special groups (teens, elderly, postpartum)
- Psychological counseling
- Trauma recovery
- How to help others with mental health issues

### Depression

**Common Symptoms (lasting >2 weeks):**
- Persistent sadness, emptiness
- Loss of interest in hobbies
- Fatigue, low energy
- Sleep changes (insomnia or oversleeping)
- Appetite changes
- Difficulty concentrating
- Feelings of worthlessness
- Thoughts of self-harm

**When to Seek Help:**
- Symptoms lasting >2 weeks
- Affecting daily life
- Physical symptoms without clear cause
- Thoughts of self-harm

**How to Help:**
- Listen without judgment
- Encourage professional help
- Offer companionship
- Crisis hotline: 400-161-9995 (China)

### Anxiety

**Normal Anxiety vs Anxiety Disorder:**

| Normal Anxiety | Anxiety Disorder |
|----------------|-------------------|
| Has clear trigger | No clear cause or disproportionate |
| Goes away after event | Persists >6 months |
| Mild physical symptoms | Severe symptoms affecting life |
| Can function normally | Impaired work/social functioning |

**Coping Strategies:**
- Deep breathing (4-7-8 method)
- Physical exercise
- Sleep management
- Cognitive restructuring
- Mindfulness meditation
- Limit caffeine/alcohol

### Mental Health by Age Group

#### Adolescents
- Emotional regulation
- Academic stress
- Peer relationships
- Screen time balance
- Signs to watch: mood changes, social withdrawal, sleep changes

#### Postpartum
- Baby blues vs postpartum depression
- Support systems
- When to seek help: persistent sadness >2 weeks, thoughts of harm

#### Elderly
- Loneliness, social isolation
- Cognitive changes
- Depression often mistaken for aging
- Importance of social connection

### Psychological Counseling

**When to Consider:**
- Persistent emotional problems
- Relationship difficulties
- Life transitions
- Trauma recovery
- Behavioral issues

**Types of Help:**
- Counselor: mild-moderate issues
- Psychiatrist: medication needed
- Psychotherapist: deep treatment (CBT, EMDR)

---

## 11. Pet Health 🐕🐱

When users ask about pet care, animal health, pet nutrition, or veterinary questions.

### Dogs

**Common Health Issues:**

| Issue | Symptoms | When to See Vet |
|-------|----------|-----------------|
| Skin problems | Itching, redness, hair loss | >3 days |
| Ear infections | Head shaking, odor | Immediately |
| Digestive issues | Vomiting, diarrhea | If bloody or >24h |
| Parasites | Scratching, visible fleas | With prescription |

**Vaccination Schedule:**
- 6-8 weeks: First DHPP vaccine
- 10-12 weeks: Second vaccine
- 14-16 weeks: Third vaccine + rabies
- Annually: Booster

**Food & Nutrition:**
- High protein, animal-based
- Avoid: chocolate, grapes, onions, xylitol
- Puppies: high-protein, high-calorie
- Seniors: joint support, lower calories

**Emergency Signs:**
- Difficulty breathing
- Seizures
- Ingestion of toxins
- Severe bleeding
- Bloated/stretched abdomen

### Cats

**Common Health Issues:**

| Issue | Symptoms | When to See Vet |
|-------|----------|-----------------|
| Hairballs | Vomiting fur | Frequent (>1/week) |
| URI | Sneezing, discharge | With fever |
| FLUTD | Straining to urinate | Immediately (emergency!) |
| Dental disease | Bad breath, drooling | Regular checkups |

**Vaccination:**
- FVRCP (core): 8, 12, 16 weeks
- Rabies: 12-16 weeks
- Annual boosters

**Litter Box:**
- Clean daily
- Full change weekly
- 1.5-2 inches of litter
- One box per cat + 1

**Food & Nutrition:**
- Obligate carnivore - needs animal protein
- Wet food for hydration
- Avoid: dog food, raw eggs, milk

### Small Pets

**Hamsters:**
- Diet: seeds, grains, vegetables, protein
- Avoid: citrus, onions, almonds
- Fresh water daily
- Exercise wheel (solid surface)

**Rabbits:**
- Hay: 80% of diet
- Pellets: limited
- Vegetables daily
- Not: ice lettuce, potatoes

### General Pet Care

**Parasite Prevention:**
- Dogs: monthly flea/tick, heartworm prevention
- Cats: monthly topical/oral
- Indoor cats: still at risk

**Senior Pets:**
- More frequent vet visits (every 6 months)
- Joint supplements
- Comfortable bedding
- Adapted exercise

---

## 12. Health Report Analysis 📋

When users upload medical examination reports (PDF/images), analyze and track health metrics over time.

### Workflow

1. **Extract** key indicators from the report
2. **Categorize** by system (cardiovascular, liver, etc.)
3. **Flag** abnormal values with severity
4. **Compare** with historical data if available
5. **Provide** actionable recommendations
6. **Store** report for future trend analysis

### Storage

Reports are stored in: `data/health-reports/`

Structure:
```
data/health-reports/
├── {user-id}/
│   ├── history.json          # Index of all reports
│   ├── 2026-03-27.json       # Report data
│   └── 2026-03-27.pdf        # Original PDF (optional)
```

### Key Indicators to Track

#### Cardiovascular (心血管)
| Indicator | Normal Range | Risk if Abnormal |
|-----------|--------------|------------------|
| Total Cholesterol | 2.85-5.2 mmol/L | Heart disease |
| LDL | 1.9-3.4 mmol/L | Atherosclerosis |
| HDL | 1.03-1.55 mmol/L | Low = risk |
| Triglycerides | 0.45-1.7 mmol/L | Metabolic |
| Homocysteine | ≤15 μmol/L | Cardiovascular risk |
| Blood Pressure | <120/80 mmHg | Hypertension |

#### Liver (肝功能)
| Indicator | Normal Range | Risk if Abnormal |
|-----------|--------------|------------------|
| ALT | 9-50 U/L | Liver damage |
| AST | 15-40 U/L | Liver/heart |
| GGT | 10-60 U/L | Bile duct/alcohol |
| Total Bilirubin | ≤23 μmol/L | Liver/blood |
| Direct Bilirubin | ≤4 μmol/L | Biliary |
| Indirect Bilirubin | ≤19 μmol/L | Hemolysis/Gilbert's |

#### Metabolic (代谢)
| Indicator | Normal Range | Risk if Abnormal |
|-----------|--------------|------------------|
| Fasting Glucose | 3.9-6.1 mmol/L | Diabetes |
| HbA1c | 4.0-6.0% | Long-term glucose |
| Uric Acid | 150-420 μmol/L | Gout |

#### Vitamins (维生素)
| Indicator | Normal Range | Notes |
|-----------|--------------|-------|
| 25-OH-VD | 30-100 ng/mL | <20 deficient |
| Vitamin B12 | 200-900 pg/mL | Nerve health |
| Folate | >3 ng/mL | DNA synthesis |

#### Blood (血常规)
| Indicator | Normal Range | Risk if Abnormal |
|-----------|--------------|------------------|
| Hemoglobin | 120-160 g/L | Anemia |
| WBC | 4-10 ×10⁹/L | Infection/immunity |
| Platelets | 100-300 ×10⁹/L | Clotting |
| MCV | 80-100 fL | Anemia type |

### Report Template

```json
{
  "date": "2026-03-27",
  "user_id": "default",
  "source": "体检报告",
  "indicators": {
    "cardiovascular": {
      "total_cholesterol": {"value": 4.93, "unit": "mmol/L", "status": "normal"},
      "ldl": {"value": 3.10, "unit": "mmol/L", "status": "normal"},
      "hdl": {"value": 1.41, "unit": "mmol/L", "status": "normal"},
      "triglycerides": {"value": 1.08, "unit": "mmol/L", "status": "normal"}
    },
    "liver": {
      "alt": {"value": 9.6, "unit": "U/L", "status": "normal"},
      "ast": {"value": 18.7, "unit": "U/L", "status": "normal"},
      "ggt": {"value": 17.6, "unit": "U/L", "status": "normal"},
      "total_bilirubin": {"value": 27.9, "unit": "μmol/L", "status": "high"},
      "direct_bilirubin": {"value": 4.7, "unit": "μmol/L", "status": "high"},
      "indirect_bilirubin": {"value": 23.2, "unit": "μmol/L", "status": "high"}
    },
    "metabolic": {
      "fasting_glucose": {"value": 4.83, "unit": "mmol/L", "status": "normal"}
    },
    "other": {
      "homocysteine": {"value": 10.90, "unit": "μmol/L", "status": "normal"},
      "blood_pressure": {"value": "104/74", "unit": "mmHg", "status": "normal"},
      "bmi": {"value": 23.5, "unit": "kg/m²", "status": "normal"},
      "pulse": {"value": 59, "unit": "bpm", "status": "low"}
    }
  },
  "abnormalities": [
    {"indicator": "total_bilirubin", "severity": "mild", "note": "轻度升高，肝功能其他指标正常"},
    {"indicator": "pulse", "severity": "normal", "note": "窦性心动过缓，通常为良性"}
  ],
  "recommendations": [
    "3个月后复查胆红素 + 肝胆B超",
    "下次体检加测 25-OH-VD",
    "保持当前保健品方案"
  ],
  "follow_up": {
    "date": "2026-06-27",
    "tests": ["胆红素复查", "肝胆B超", "25-OH-VD"]
  }
}
```

### Trend Analysis

When 2+ reports exist, provide:

1. **Delta changes** (absolute and percentage)
2. **Trend arrows** (↑ ↓ →)
3. **Warnings** for concerning patterns
4. **Visual summary** in table format

Example output:
```
📊 6个月趋势对比 (2026-03 vs 2025-09)

心血管指标:
| 指标 | 2025-09 | 2026-03 | 变化 |
|------|---------|---------|------|
| LDL  | 3.45    | 3.10    | ↓ 10% ✅ |
| HDL  | 1.28    | 1.41    | ↑ 10% ✅ |

结论: 血脂持续改善，继续保持！
```

### Abnormality Severity Levels

| Level | Color | Meaning | Action |
|-------|-------|---------|--------|
| normal | ✅ | Within range | None |
| watch | 👀 | Slightly off | Monitor |
| mild | ⚠️ | Minor concern | Retest suggested |
| moderate | 🔶 | Needs attention | Doctor consult |
| severe | 🚨 | Significant | Immediate follow-up |

### Integration with Supplements

Cross-reference report findings with user's supplement regimen:

- **Vitamin D low** → Recommend D3+K2
- **LDL high** → Suggest fish oil + plant sterols
- **Liver enzymes high** → Review supplements for hepatotoxicity
- **Homocysteine high** → Recommend B12 + folate + B6

---

## 13. Supplement Recommendation System 💊

Professional supplement advisor with evidence-based recommendations, brand comparison, and timing optimization.

### Core Features

1. **Evidence-Based Recommendations** - Based on clinical studies (Examine.com, PubMed)
2. **Brand Comparison** - Quality, price, absorption, value analysis
3. **Indicator Mapping** - Health indicators → supplement suggestions
4. **Timing Optimization** - When to take for best absorption
5. **Interaction Checking** - Drug-supplement and supplement-supplement interactions

---

### Health Indicator → Supplement Mapping

#### Cardiovascular (心血管)

| Indicator | Status | Recommended Supplements |
|-----------|--------|------------------------|
| LDL elevated | >3.4 mmol/L | Omega-3 fish oil, Plant sterols, Niacin |
| HDL low | <1.0 mmol/L | Omega-3, Niacin, Exercise |
| Triglycerides high | >1.7 mmol/L | Omega-3 (EPA/DHA 2-4g), Reduce carbs |
| Homocysteine high | >15 μmol/L | **B-Complex (B6+B12+Folate)**, Betaine |
| Lipoprotein(a) high | >300 mg/L | Omega-3, Niacin, CoQ10 |
| Blood pressure high | >130/85 | Omega-3, Magnesium, CoQ10, Garlic |

#### Metabolic (代谢)

| Indicator | Status | Recommended Supplements |
|-----------|--------|------------------------|
| Fasting glucose high | >6.1 mmol/L | Chromium, Berberine, Alpha-lipoic acid |
| HbA1c high | >6.0% | Chromium, Berberine, Cinnamon |
| Uric acid high | >428 μmol/L | Cherry extract, Vitamin C, Reduce purines |
| C-peptide low | <1.0 ng/mL | Monitor, no direct supplement |

#### Liver (肝功能)

| Indicator | Status | Recommended Supplements |
|-----------|--------|------------------------|
| ALT/AST elevated | >50/40 U/L | Milk thistle, NAC, Stop hepatotoxic supplements |
| Bilirubin elevated | >23 μmol/L | **Milk thistle**, SAMe, Check Gilbert's syndrome |
| GGT elevated | >60 U/L | Reduce alcohol, Milk thistle, NAC |

#### Vitamins & Minerals

| Indicator | Status | Recommended Supplements |
|-----------|--------|------------------------|
| Vitamin D low | <30 ng/mL | **D3+K2** (5000-10000 IU short-term) |
| Vitamin D optimal | 40-60 ng/mL | **D3+K2** (2000-3000 IU maintenance) |
| B12 low | <200 pg/mL | **Methyl B12** (active form) |
| Iron low | Ferritin <30 | Iron + Vitamin C, Check absorption |
| Magnesium low | Symptoms | **Magnesium Glycinate/Citrate** |

#### General Wellness (整体健康)

| Goal | Recommended Supplements |
|------|------------------------|
| Energy & Fatigue | CoQ10, B-Complex, Iron (if low) |
| Sleep | Magnesium, Melatonin (short-term) |
| Stress & Anxiety | Magnesium, Ashwagandha, L-theanine |
| Joint Health | Omega-3, Curcumin, Glucosamine |
| Brain Health | Omega-3 (DHA), Bacopa, Lion's mane |
| Anti-aging | Resveratrol, NMN, CoQ10 |

---

### Brand Quality Guide

#### Quality Tiers

| Tier | Brands | Price | Quality | Notes |
|------|--------|-------|---------|-------|
| **Premium** | Thorne, Pure Encapsulations, Life Extension | High | ⭐⭐⭐⭐⭐ | Medical-grade, third-party tested |
| **High** | Now Foods, Jarrow, Solgar, Doctor's Best | Medium | ⭐⭐⭐⭐ | Good value, GMP certified |
| **Standard** | Nature's Way, Nature Made, 21st Century | Low | ⭐⭐⭐ | Basic quality, widely available |
| **Sports** | Sports Research, ON, NutraBio | Medium-High | ⭐⭐⭐⭐ | Good for athletes |

#### Brand Recommendations by Category

**Vitamin D3+K2**:
| Rank | Brand | Dose | Price/60ct | Notes |
|------|-------|------|------------|-------|
| 1 | Now D3+K2 | 5000 IU | ~$10 | Best value, MK-7 form |
| 2 | Thorne D/K2 | 1000/200 mcg | ~$20 | Medical-grade |
| 3 | Life Extension | 5000/100 mcg | ~$12 | Full-spectrum K2 |

**Omega-3 Fish Oil**:
| Rank | Brand | EPA/DHA | Price | Notes |
|------|-------|---------|-------|-------|
| 1 | Sports Research Triple Strength | 900mg | ~$25 | **Best value**, triglyceride form |
| 2 | Nordic Naturals Ultimate | 650mg | ~$30 | Top quality, lemon taste |
| 3 | Now Ultra Omega-3 | 500mg | ~$20 | Good budget option |

**CoQ10**:
| Rank | Brand | Form | Dose | Price | Notes |
|------|-------|------|------|-------|-------|
| 1 | **NatureWise Ubiquinol** | Active | 100mg | ~$25 | Best absorption |
| 2 | Jarrow QH-absorb | Active | 100mg | ~$28 | Enhanced absorption |
| 3 | Now CoQ10 | Ubiquinone | 200mg | ~$20 | Budget option |

**Curcumin (姜黄素)**:
| Rank | Brand | Form | Price | Notes |
|------|-------|------|-------|-------|
| 1 | Meriva (Now, Thorne) | Phytosome | ~$20-30 | 29x better absorption |
| 2 | Longvida | Optimized | ~$25 | Good brain penetration |
| 3 | Curcumin C3 + Bioperine | Standard + Pepper | ~$15 | Budget, needs fat |

**Magnesium**:
| Rank | Brand | Form | Price | Notes |
|------|-------|------|-------|-------|
| 1 | **Now Magnesium Bisglycinate** | Bisglycinate | ~$12 | Best absorption, gentle |
| 2 | Natural Vitality Calm | Citrate powder | ~$20 | Good for sleep |
| 3 | Thorne Bisglycinate | Bisglycinate | ~$18 | Medical-grade |

**B-Complex**:
| Rank | Brand | Form | Price | Notes |
|------|-------|------|-------|-------|
| 1 | **Now Co-Enzyme B-Complex** | Methylated | ~$10 | Best value, active forms |
| 2 | Thorne Basic B | Methylated | ~$20 | Medical-grade |
| 3 | Life Extension BioActive | Methylated | ~$15 | Full-spectrum |

---

### Timing Optimization

#### Fat-Soluble Supplements (Need fat for absorption)

| Supplement | Best Time | Fat Source | Notes |
|------------|-----------|------------|-------|
| Vitamin D3+K2 | **Lunch/Dinner** | Meal fat (10-20g) | Most critical for timing |
| Omega-3 Fish Oil | Any meal | Meal fat or self-contained | Take with largest meal |
| CoQ10 | **Morning/Lunch** | Meal fat | Avoid evening (may affect sleep) |
| Curcumin | **Lunch/Dinner** | Meal fat + pepper | Needs fat AND piperine |
| Vitamin E | Any meal | Meal fat | |
| Vitamin A | Any meal | Meal fat | |

#### Water-Soluble Supplements

| Supplement | Best Time | Notes |
|------------|-----------|-------|
| B-Complex | **Morning** (after breakfast) | Energy, avoid evening |
| Vitamin C | Any time | Split doses for better absorption |
| Minerals (Zinc, Iron) | Between meals | Separate from calcium by 2h |

#### Sleep-Supporting Supplements

| Supplement | Best Time | Notes |
|------------|-----------|-------|
| Magnesium | **30-60 min before bed** | Calming, muscle relaxation |
| Melatonin | **30-60 min before bed** | Short-term only |
| L-theanine | Evening | Calming without sedation |
| Glycine | Before bed | Sleep quality |

#### Foods That Help/Hinder Absorption

**✅ Help Absorption**:
- Fat (olive oil, avocado, nuts, eggs) - for fat-soluble
- Black pepper (piperine) - for curcumin
- Vitamin C - for iron
- Fat - for vitamins A, D, E, K

**❌ Hinder Absorption**:
- Calcium - blocks iron, zinc
- Coffee/tea - blocks iron, calcium
- Fiber - can bind minerals
- Alcohol - impairs B-vitamin absorption

---

### Interaction Checking

#### Common Interactions

**Fish Oil**:
- ⚠️ Blood thinners (warfarin, aspirin) - increased bleeding risk
- ⚠️ Surgery - stop 2 weeks before
- ✅ Safe with most supplements

**Vitamin D3**:
- ⚠️ Depletes magnesium - add magnesium supplement
- ⚠️ High calcium intake - risk of hypercalcemia
- ✅ Synergistic with K2

**Curcumin**:
- ⚠️ Blood thinners - mild antiplatelet effect
- ⚠️ Gallbladder issues - stimulates bile
- ⚠️ Iron supplements - may reduce absorption

**Magnesium**:
- ⚠️ Antibiotics - separate by 2 hours
- ⚠️ Bisphosphonates - separate by 2 hours
- ✅ Synergistic with B6, D3

**B-Complex**:
- ⚠️ Levodopa - B6 reduces effectiveness
- ✅ Safe with most medications

**CoQ10**:
- ⚠️ Warfarin - may reduce effectiveness
- ✅ Synergistic with statins (reduces side effects)

#### Supplement-Supplement Combinations

**✅ Good Combinations**:
- D3 + K2 + Magnesium (synergistic)
- Omega-3 + Curcumin (anti-inflammatory stack)
- B-Complex + Magnesium (energy + relaxation balance)
- CoQ10 + Omega-3 (cardiovascular stack)

**⚠️ Space Apart (2+ hours)**:
- Calcium + Iron (calcium blocks iron)
- Zinc + Copper (balance needed)
- Magnesium + Calcium (compete for absorption)

---

### Personalized Recommendation Workflow

1. **Analyze Health Profile**
   - Review latest health report
   - Identify abnormal indicators
   - Note existing conditions

2. **Check Current Supplements**
   - Review user's current regimen
   - Evaluate appropriateness
   - Check for interactions

3. **Generate Recommendations**
   - Map indicators to supplements
   - Prioritize by impact
   - Consider user's budget/preference

4. **Optimize Timing**
   - Create daily schedule
   - Consider user's meal pattern
   - Maximize absorption

5. **Brand Suggestions**
   - Recommend specific brands
   - Compare price/value
   - Consider user's existing brand preferences

6. **Follow-up Plan**
   - Set review timeline (3-6 months)
   - Identify retest indicators
   - Monitor for effects

---

### Example Output Format

```
💊 个性化保健品建议

基于体检报告 (2026-03-27):
✅ 继续当前方案
⚠️ 建议新增

📋 指标分析:
- 同型半胱氨酸 10.90 → 建议新增 B-Complex
- 胆红素偏高 → 建议3个月后复查，必要时加奶蓟草
- 维生素D未测 → 下次体检加测

💊 推荐新增:
1. Now Co-Enzyme B-Complex (活性B族)
   - 原因: 降低同型半胱氨酸
   - 时间: 早饭后
   - 价格: ~¥80/60粒

⏰ 优化时间表:
🌅 早餐 (牛奶): 鱼油 + Q10
☀️ 午餐后: D3+K2 + 姜黄素
🌙 睡前: 甘氨酸镁

✅ 安全性: 无相互作用
📅 复查: 3个月后复查胆红素 + 6个月后体检
```

---

### Data Sources & References

**Evidence-Based Resources**:
- Examine.com - Independent supplement research
- PubMed - Clinical studies
- ConsumerLab - Quality testing
- Labdoor - Independent lab analysis
- NIH Office of Dietary Supplements

**Safety Databases**:
- Natural Medicines Database
- Drug.com Interaction Checker
- Medscape Drug Interactions

---

## 14. External API Integration 🔌

Connect to external data sources for real-time, evidence-based recommendations.

### Supported APIs

#### 1. Examine.com Research Database

**Status**: 🚧 Official API in development

**Alternative**: Use Apify scraper
```
Endpoint: https://apify.com/hanamira/examine-com-supplement-research
Cost: Pay-per-use (~$0.01-0.05 per request)
Data: Supplement research summaries, clinical studies, dosage
```

**Setup**:
```bash
# Set API token
export APIFY_API_TOKEN=your_token_here

# Query supplement research
mcporter call apify.examine-research supplement="vitamin-d"
```

**Data Structure**:
```json
{
  "supplement": "Vitamin D",
  "summary": "Evidence summary...",
  "benefits": ["Bone health", "Immune function"],
  "dosage": "1000-4000 IU/day",
  "studies": [
    {
      "title": "Study title",
      "url": "https://pubmed.ncbi.nlm.nih.gov/...",
      "findings": "Key findings"
    }
  ]
}
```

---

#### 2. ConsumerLab Quality Testing

**Status**: ✅ API available (subscription required)

**Endpoint**: `https://api.consumerlab.com/`

**Setup**:
```bash
# Requires ConsumerLab subscription ($44/year)
# Contact ConsumerLab for API access
export CONSUMERLAB_API_KEY=your_key_here
```

**Available Endpoints**:
```
GET /product/{id}           # Product details
GET /test-results/{id}      # Lab test results
GET /search?q=omega-3       # Search products
GET /brands/{brand}         # Brand quality scores
```

**Data Structure**:
```json
{
  "product": "Nordic Naturals Ultimate Omega",
  "brand": "Nordic Naturals",
  "test_date": "2024-03-15",
  "results": {
    "passed": true,
    "epa_dha_content": "936mg (104% of label claim)",
    "freshness": "Excellent",
    "contaminants": "None detected",
    "quality_score": "A+"
  }
}
```

---

#### 3. PubMed Clinical Studies

**Status**: ✅ Free API

**Endpoint**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

**Setup**: No API key required (rate limit: 3 requests/second)

**Usage**:
```bash
# Search for supplement studies
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=vitamin+d+cardiovascular"
```

---

### Integration Workflow

1. **User asks about supplement X**
2. **Check local database** (fast, free)
3. **If not found or needs update**:
   - Query Examine.com (research summary)
   - Query ConsumerLab (quality testing)
   - Query PubMed (latest studies)
4. **Synthesize results**
5. **Present to user with citations**

---

## 15. Evidence Summaries (Static Data) 📚

Pre-loaded research summaries for common supplements.

### Vitamin D3

**Evidence Level**: ⭐⭐⭐⭐⭐ (Strong)

**Key Benefits**:
- Bone health: ✅ Strong evidence
- Immune function: ✅ Good evidence
- Mood/depression: ⚠️ Mixed evidence
- Cardiovascular: ⚠️ Mixed evidence
- Cancer prevention: ⚠️ Mixed evidence

**Optimal Dose**:
- Deficiency (<20 ng/mL): 5000-10000 IU/day for 8-12 weeks
- Maintenance (30-60 ng/mL): 2000-4000 IU/day
- Always take with K2 (MK-7 form)

**Blood Test**: 25-OH-VD (target: 40-60 ng/mL)

**Key Studies**:
- BMJ 2014: 25% reduction in respiratory infections
- Lancet 2019: No cardiovascular benefit (VITAL trial)
- Cochrane 2014: Reduced mortality in elderly

---

### Omega-3 Fish Oil

**Evidence Level**: ⭐⭐⭐⭐ (Good)

**Key Benefits**:
- Triglycerides: ✅ Strong evidence (20-50% reduction)
- Heart health: ✅ Good evidence (REDUCE-IT trial)
- Brain health: ✅ Good evidence (DHA)
- Joint inflammation: ⚠️ Moderate evidence
- Depression: ⚠️ Mixed evidence

**Optimal Dose**:
- General health: EPA+DHA 1000mg/day
- High triglycerides: EPA+DHA 2000-4000mg/day
- Prescription strength (Vascepa): EPA 4g/day

**Key Studies**:
- REDUCE-IT 2019: 25% CV risk reduction with EPA 4g
- ASCEND 2018: No benefit for diabetics (lower dose)
- VITAL 2018: No CV benefit in general population

**Form**: Triglyceride form > Ethyl ester

---

### Coenzyme Q10 (CoQ10)

**Evidence Level**: ⭐⭐⭐⭐ (Good)

**Key Benefits**:
- Statin side effects: ✅ Strong evidence (reduces muscle pain)
- Heart failure: ✅ Good evidence (improves symptoms)
- Energy/fatigue: ✅ Moderate evidence
- Blood pressure: ⚠️ Mild reduction
- Migraine: ⚠️ Moderate evidence

**Optimal Dose**:
- General: 100-200 mg/day
- With statins: 100-200 mg/day
- Heart failure: 300 mg/day

**Form**: Ubiquinol (active) > Ubiquinone (oxidized)
- Ubiquinol: 2-3x better absorption
- Best taken with fat-containing meal

**Key Studies**:
- JACC 2014: Reduced statin muscle pain by 40%
- Cochrane 2015: Improved heart failure symptoms

---

### Curcumin (姜黄素)

**Evidence Level**: ⭐⭐⭐ (Moderate)

**Key Benefits**:
- Inflammation: ✅ Good evidence (CRP reduction)
- Joint pain: ✅ Moderate evidence
- Cognitive: ⚠️ Preliminary evidence
- Digestive: ⚠️ Mixed evidence

**Bioavailability Problem**:
- Native curcumin: Only 2-5% absorption
- Needs enhanced formulation

**Form Recommendations**:
1. Meriva (phytosome): 29x better absorption ⭐⭐⭐⭐⭐
2. Longvida: 65x better (brain penetration)
3. BCM-95: 7x better (natural enhancement)
4. Standard + Bioperine: 20x better

**Optimal Dose**:
- Standard curcumin: 500-1000mg 2-3x/day with fat
- Meriva: 500mg 2x/day
- Always with fat + black pepper

**Key Studies**:
- Phytother Res 2013: Meriva reduced joint pain 60%
- J Clin Psychopharmacol 2017: Improved depression

---

### Magnesium

**Evidence Level**: ⭐⭐⭐⭐⭐ (Strong)

**Key Benefits**:
- Sleep quality: ✅ Strong evidence
- Muscle cramps: ✅ Strong evidence
- Blood pressure: ✅ Moderate evidence
- Migraine prevention: ✅ Good evidence
- Anxiety: ⚠️ Moderate evidence
- Blood sugar: ✅ Moderate evidence

**Optimal Dose**:
- General: 200-400 mg/day
- Sleep: 300-400 mg before bed
- Migraine: 400-600 mg/day
- Maximum safe dose: 400-500 mg/day

**Form Recommendations**:
1. Bisglycinate: Best absorption, gentle ⭐⭐⭐⭐⭐
2. Citrate: Good absorption, may cause loose stools
3. Glycinate: Good absorption, calming
4. Oxide: Poor absorption, avoid

**Signs of Deficiency**:
- Muscle cramps, fatigue, poor sleep, anxiety, headaches

**Key Studies**:
- Nutrients 2020: Improved sleep quality
- Headache 2017: 40% reduction in migraine frequency

---

### B-Complex (B6, B12, Folate)

**Evidence Level**: ⭐⭐⭐⭐ (Good)

**Key Benefits**:
- Homocysteine reduction: ✅ Strong evidence
- Energy metabolism: ✅ Good evidence
- Nervous system: ✅ Good evidence
- Mood: ⚠️ Mixed evidence
- Cognitive: ⚠️ Mixed evidence (B12 only)

**Homocysteine Metabolism**:
- B6 (P5P): 25-50 mg
- B12 (Methylcobalamin): 500-1000 mcg
- Folate (5-MTHF): 400-800 mcg

**Form Recommendations**:
- Methylated forms (active): Better for 40-60% of population
- Folate: 5-MTHF (Quatrefolic) > Folic acid
- B12: Methylcobalamin > Cyanocobalamin

**Key Studies**:
- Cochrane 2017: 25% reduction in stroke risk with B-vitamins
- Am J Clin Nutr 2010: Reduced cognitive decline with B12

---

## 16. ConsumerLab Test Results Summary 🧪

Quality testing highlights from ConsumerLab independent testing.

### Vitamin D3 (2024 Testing)

| Brand | Claimed | Found | Grade | Notes |
|-------|---------|-------|-------|-------|
| Now Foods | 5000 IU | 5050 IU | A | Passed all tests |
| Thorne | 1000 IU | 990 IU | A | Medical-grade |
| Nature Made | 2000 IU | 2050 IU | A | Good value |
| Life Extension | 5000 IU | 5100 IU | A | Full-spectrum K2 |
| Nature's Bounty | 5000 IU | 4200 IU | **F** | **Failed (underdosed)** |

---

### Omega-3 Fish Oil (2024 Testing)

| Brand | Claimed EPA+DHA | Found | Freshness | Contaminants | Grade |
|-------|----------------|-------|-----------|--------------|-------|
| Nordic Naturals Ultimate | 650 mg | 670 mg | Excellent | None | A+ |
| **Sports Research Triple** | 900 mg | 920 mg | Excellent | None | A+ |
| Now Ultra Omega-3 | 500 mg | 510 mg | Excellent | None | A |
| Carlson Labs | 1000 mg | 1010 mg | Excellent | None | A |
| Nature Made | 300 mg | 280 mg | Good | None | B |
| Sundown Naturals | 600 mg | 450 mg | Fair | None | **F** |

---

### CoQ10 (2024 Testing)

| Brand | Form | Claimed | Found | Absorption | Grade |
|-------|------|---------|-------|------------|-------|
| NatureWise Ubiquinol | Active | 100 mg | 105 mg | Excellent | A+ |
| Jarrow QH-absorb | Active | 100 mg | 98 mg | Excellent | A |
| Now CoQ10 | Ubiquinone | 200 mg | 205 mg | Good | A |
| Doctor's Best | Ubiquinone | 100 mg | 95 mg | Good | B+ |
| GNC | Ubiquinone | 200 mg | 160 mg | Fair | **C** |

---

### Curcumin (2023 Testing)

| Brand | Form | Claimed Curcuminoids | Found | Grade |
|-------|------|---------------------|-------|-------|
| Thorne Meriva | Phytosome | 500 mg | 510 mg | A+ |
| Now Curcumin Phytosome | Meriva | 500 mg | 505 mg | A |
| Jarrow Curcumin 95 | Standard | 500 mg | 485 mg | B+ |
| Nature's Way | Standard | 700 mg | 520 mg | **F** |

---

### Magnesium (2024 Testing)

| Brand | Form | Claimed | Found | Dissolution | Grade |
|-------|------|---------|-------|-------------|-------|
| Now Bisglycinate | Bisglycinate | 200 mg | 205 mg | Excellent | A+ |
| Natural Vitality Calm | Citrate | 325 mg | 330 mg | Excellent | A |
| Thorne Bisglycinate | Bisglycinate | 200 mg | 198 mg | Excellent | A |
| Nature Made | Oxide | 250 mg | 255 mg | Poor | **D** |
| Sundown | Oxide | 400 mg | 410 mg | Poor | **D** |

---

### Quality Issues to Watch

**Common Problems**:
1. **Underdosing**: Product contains less than claimed
2. **Contamination**: Heavy metals, PCBs in fish oil
3. **Rancidity**: Fish oil freshness issues
4. **Poor dissolution**: Tablet doesn't break down
5. **Wrong form**: Inactive forms instead of active

**Best Practices**:
- Choose third-party tested brands
- Check ConsumerLab/Labdoor reports
- Avoid the cheapest options
- Look for GMP certification

---

## 17. Recommendation Engine 🤖

Automated supplement recommendation based on health data.

### Decision Tree

```
User Health Profile
    ↓
[Analyze Indicators]
    ↓
[Map to Supplements] ─→ [Check Interactions]
    ↓                        ↓
[Score Recommendations] ← [Filter Unsafe]
    ↓
[Optimize Timing] ─→ [Consider User Preferences]
    ↓
[Generate Report]
```

### Scoring Algorithm

For each supplement:
```
Score = (Evidence_Strength × 0.4) +
        (Indicator_Match × 0.3) +
        (Safety_Profile × 0.2) +
        (Cost_Effectiveness × 0.1)
```

**Example**:
- Vitamin D3 for deficiency:
  - Evidence: 5/5 × 0.4 = 2.0
  - Match: 5/5 × 0.3 = 1.5
  - Safety: 5/5 × 0.2 = 1.0
  - Cost: 5/5 × 0.1 = 0.5
  - **Total: 5.0/5** ✅ Highly recommended

---

## 18. Machine Learning Recommendation Engine 🤖

AI-powered personalized supplement recommendations based on health data and user profile.

### Features

1. **Rule-Based Hybrid Model** - Combines evidence-based rules with personalization
2. **Multi-Factor Scoring** - 6 weighted factors for recommendation ranking
3. **Health Indicator Mapping** - 20+ indicators → supplement suggestions
4. **Personalization** - Age, gender, lifestyle, diet-specific adjustments
5. **Interaction Detection** - Synergistic and antagonistic combinations
6. **7-Step Workflow** - From analysis to follow-up

### Scoring Formula

```
Total Score = (Evidence × 0.25) +
              (Indicator Match × 0.30) +
              (Safety × 0.20) +
              (Cost Effectiveness × 0.10) +
              (User Preference × 0.10) +
              (Age Relevance × 0.05)
```

### Health Indicator Examples

| Indicator | Threshold | Top Supplements |
|-----------|-----------|-----------------|
| LDL >3.4 mmol/L | High | Omega-3, Berberine, Plant sterols |
| Homocysteine >15 μmol/L | High | B-Complex, B6+B12+Folate |
| Vitamin D <30 ng/mL | Low | D3+K2 5000-10000 IU |
| Fasting Glucose >6.1 | High | Berberine, Chromium |

### Personalization Factors

**By Age**:
- 18-30: Energy, performance
- 30-40: Preventive health
- 40-50: Cardiovascular, cognitive
- 50-60: Bone health, hormones
- 60+: Comprehensive anti-aging

**By Lifestyle**:
- Sedentary: Cardiovascular support
- Active: Recovery, joints
- Athlete: Performance stack
- High stress: Adaptogens, magnesium

**By Diet**:
- Vegetarian/Vegan: B12, iron, omega-3
- Keto: Electrolytes

### Interaction Matrix

**Synergistic**:
- D3 + K2 + Magnesium (calcium absorption)
- Omega-3 + Curcumin (anti-inflammatory stack)
- B6 + B12 + Folate (homocysteine metabolism)

**Antagonistic**:
- Calcium + Iron (space 2 hours)
- Zinc + Copper (balance 10:1)
- Magnesium + Calcium (separate intake)

---

## 19. Supplement Database (100+ Supplements) 📚

Comprehensive database with 105 supplements across 10 categories.

### Categories

| Category | Count | Examples |
|----------|-------|----------|
| Vitamins | 13 | D3, K2, B-Complex, C, E, A |
| Minerals | 8 | Magnesium, Zinc, Iron, Selenium |
| Amino Acids | 10 | Creatine, Carnitine, NAC, Theanine |
| Fatty Acids | 5 | Omega-3, MCT, CLA, GLA |
| Herbs | 40 | Curcumin, Ashwagandha, Rhodiola, Ginseng |
| Probiotics | 9 | Multi-strain, LGG, S. boulardii |
| Enzymes | 4 | Digestive, Bromelain, Lactase |
| Antioxidants | 9 | CoQ10, ALA, Glutathione, Astaxanthin |
| Hormones/Precursors | 4 | Melatonin, DHEA |
| Other | 21 | Collagen, Glucosamine, Fiber, CBD |

### Data Structure (Per Supplement)

```json
{
  "id": "omega-3",
  "name": "Omega-3 Fish Oil",
  "evidenceLevel": 5,
  "primaryBenefits": ["Cardiovascular", "Brain health"],
  "optimalDose": "1000-2000 mg EPA+DHA",
  "forms": [
    {"type": "TG form", "bioavailability": 90, "recommended": true}
  ],
  "timing": "With largest meal",
  "synergistic": ["Vitamin E"],
  "interactions": {
    "conflicts": ["Blood thinners"]
  },
  "testIndicators": ["Triglycerides", "Omega-3 Index"],
  "safetyProfile": {
    "upperLimit": "5000 mg/day",
    "sideEffects": ["Fish burps"],
    "contraindications": ["Anticoagulation"]
  }
}
```

### Evidence Levels

| Level | Meaning | Example |
|-------|---------|---------|
| 5 | Strong (multiple RCTs) | Vitamin D, Omega-3, Creatine |
| 4 | Good (RCTs, reviews) | CoQ10, Magnesium, Curcumin (enhanced) |
| 3 | Moderate (some RCTs) | Ashwagandha, Rhodiola, Berberine |
| 2 | Preliminary (few studies) | NMN, Spermidine, PQQ |
| 1 | Traditional use | Some TCM herbs |

---

## 20. Quality Verification & Traceability 🔍

Tools and frameworks for verifying supplement quality and authenticity.

### Third-Party Testing Services

| Service | Type | Access | Best For |
|---------|------|--------|----------|
| **ConsumerLab** | Independent testing | $44/year subscription | US brands |
| **NSF International** | Certification | Free lookup | Safety verification |
| **USP Verified** | Standards+certification | Free lookup | Quality seal |
| **Informed Sport** | Athlete testing | Free lookup | Banned substances |
| **Labdoor** | Independent testing | Free+Premium | Brand rankings |

### Fake Product Indicators

⚠️ **Warning Signs**:
- Price significantly below market average
- No third-party testing/certification
- Vague ingredient labels
- Non-authorized retailers
- Expired or near-expiry
- Packaging errors (typos, blurry print)

### Safe Purchasing Guidelines

**✅ Recommended Retailers**:
- iHerb, Amazon (official stores)
- Vitacost, Brand websites
- Major pharmacy chains

**❌ Avoid**:
- Unauthorized third-party sellers
- No return policy
- Suspiciously low prices
- Social media direct sales

### Blockchain Traceability Framework

**Current Status**: Concept phase

**Future Vision**:
```
Raw Materials → Extraction → Testing → Packaging → Distribution → Retail
     ↓              ↓           ↓          ↓             ↓           ↓
  Blockchain ← Blockchain ← Blockchain ← Blockchain ← Blockchain ← Blockchain
     ↓              ↓           ↓          ↓             ↓           ↓
  Hash+Time      Hash+Time   Hash+Time  Hash+Time    Hash+Time    QR Code
```

**Data Recorded**:
- Origin and harvest date
- Extraction method and standardization
- Third-party lab results (COA)
- Batch number and expiry
- Transportation conditions
- Retailer information

**User Verification**:
1. Scan product QR code
2. Query blockchain
3. View complete supply chain
4. Verify data integrity

**Current Best Practices** (until blockchain is reality):
- Choose ConsumerLab/NSF/USP certified brands
- Buy from authorized retailers
- Check batch numbers
- Review COA (Certificate of Analysis)
- Use Labdoor for brand rankings
- Be skeptical of low prices

---

## 21. Recommendation Output Template 📋

Standard format for personalized supplement recommendations.

```
💊 个性化保健品方案

👤 用户概况
- 年龄: XX岁
- 性别: X
- 主要目标: [目标1, 目标2]
- 生活方式: [久坐/活跃/运动员]

📊 体检指标分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 正常指标 (X项)
- 总胆固醇 4.93 mmol/L (正常)
- 血压 104/74 mmHg (理想)

⚠️ 需关注 (X项)
- 同型半胱氨酸 10.90 μmol/L (建议降低)
- 维生素D 未检测 (建议加测)

💊 推荐方案
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 继续当前 (X种)
1. Now D3+K2 5000 IU
   - 证据等级: ⭐⭐⭐⭐⭐
   - 原因: 骨骼健康,免疫支持
   - 时间: 午餐后

➕ 建议新增 (X种)
2. Now Co-Enzyme B-Complex
   - 证据等级: ⭐⭐⭐⭐
   - 原因: 降低同型半胱氨酸
   - 剂量: 早饭后1粒
   - 价格: ~¥80/60粒

⏰ 优化时间表
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌅 早餐 (牛奶): 鱼油 + Q10
☀️ 午餐后: D3+K2 + 姜黄素
🌙 睡前: 甘氨酸镁

⚠️ 安全性检查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 无药物相互作用
✅ 无保健品冲突
✅ 剂量在安全范围内

📅 随访计划
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 3个月后: 复查 [指标]
- 6个月后: 全面体检
- 建议加测: 25-OH-VD

🔗 购买建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
推荐零售商: iHerb, 亚马逊官方店
预算估算: ¥XXX/月
```

---

*Your health is your wealth. Take care of it!* 💚
