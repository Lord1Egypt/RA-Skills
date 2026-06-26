# Visa Interview Preparation

## Purpose
Generate comprehensive interview preparation materials including likely questions, practice answers, document organization, and what to expect.

## When to Use
- "Prep me for my visa interview"
- "What questions will they ask?"
- "What should I bring to my interview?"
- "How do I prepare for [visa] interview?"

## Interview Types

### Employment-Based Visas (H-1B, L-1, O-1, etc.)
**Focus Areas:**
- Job qualifications and specialty occupation
- Employer legitimacy and relationship
- Intent to return home (for non-immigrant visas)
- Previous US immigration history

### Family-Based Visas (CR-1, IR-1, K-1, etc.)
**Focus Areas:**
- Relationship authenticity
- Financial sponsorship adequacy
- Previous marriages/relationships
- Intent to establish permanent residence

### Student Visas (F-1, J-1, M-1)
**Focus Areas:**
- Educational intent and program fit
- Financial ability to pay
- Ties to home country
- Post-graduation plans

### Tourist/Business Visas (B-1/B-2)
**Focus Areas:**
- Temporary nature of visit
- Strong ties to home country
- Financial ability to support trip
- Previous travel history

## Common Question Categories

### Personal Background
- Tell me about yourself
- What is your educational background?
- What is your current employment?
- Have you traveled to other countries?

### Purpose of Immigration
- Why do you want to [work/study/live] in [country]?
- Why did you choose this [employer/school/program]?
- What are your long-term career goals?
- How does this fit into your career plan?

### Financial Questions
- How will you support yourself?
- Who is paying for your [education/living expenses]?
- What is your current salary?
- Do you have sufficient funds?

### Relationship Questions (Family visas)
- How did you meet your [spouse/sponsor]?
- When did you get married?
- Have you met your [spouse/sponsor] in person?
- Tell me about your wedding

### Ties to Home Country
- What property do you own in your home country?
- What family members remain in your home country?
- What will you do after [completing studies/contract ends]?
- Why will you return to your home country?

## Data Structure

```json
{
  "interview_prep": [
    {
      "id": "uuid",
      "visa_type": "F-1",
      "country": "USA",
      "interview_date": "2024-04-15",
      "location": "US Consulate Mumbai",
      "preparation_status": "in-progress",
      
      "likely_questions": [
        {
          "question": "Why did you choose this university?",
          "category": "program-fit",
          "strong_answer": "I chose Stanford for its renowned Computer Science program...",
          "tips": ["Be specific about program features", "Mention professors or research"],
          "what_not_to_say": ["I heard it's easy to get into", "My friend goes there"]
        }
      ],
      
      "documents_organized": {
        "essential": ["passport", "i20", "visa-appointment-confirmation"],
        "supporting": ["transcripts", "financial-docs", "test-scores"],
        "optional": ["resume", "admission-letter"]
      },
      
      "practice_notes": "User mentioned nervousness about financial questions",
      "mock_interview_completed": false
    }
  ]
}
```

## Script Usage

```bash
# Generate interview prep for F-1 visa
python scripts/prep_interview.py \
  --visa "F-1" \
  --country "USA" \
  --consulate "Mumbai" \
  --program "Computer Science MS"

# Generate family visa interview prep
python scripts/prep_interview.py \
  --visa "CR-1" \
  --country "USA" \
  --relationship "spouse" \
  --petitioner-citizenship "US"

# Save practice session notes
python scripts/prep_interview.py \
  --action save-notes \
  --prep-id "uuid" \
  --notes "User practiced financial questions, needs more confidence"
```

## Output Format

```
VISA INTERVIEW PREPARATION
F-1 Student Visa | US Consulate Mumbai
Interview Date: April 15, 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 DOCUMENTS TO BRING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ESSENTIAL (Must have):
☐ Valid Passport (6+ months validity)
☐ Form I-20 (signed by you and DSO)
☐ DS-160 Confirmation Page
☐ Visa Appointment Confirmation
☐ Visa Application Fee Receipt
☐ Photo (if not uploaded to DS-160)

SUPPORTING (Have ready):
☐ Academic Transcripts (original + copies)
☐ Standardized Test Scores (GRE/GMAT/TOEFL/IELTS)
☐ Financial Documents:
   • Bank statements (last 6 months)
   • Affidavit of Support (if sponsored)
   • Sponsor's employment letter
   • Tax returns (if applicable)
☐ Admission Letter from university
☐ SEVIS Fee Receipt (I-901)

OPTIONAL (Bring if applicable):
☐ Resume/CV
☐ Previous degrees/diplomas
☐ Proof of ties to home country:
   • Property documents
   • Family business documents
   • Job offer letter (if returning to work)

ORGANIZATION TIP: Arrange in clear plastic folders by category

---

❓ LIKELY QUESTIONS & STRONG ANSWERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q1: Why did you choose this university?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What they're assessing: Genuine academic intent, program fit

Strong Answer Framework:
"I chose [University] because of its strong [specific program/research 
area]. I'm particularly interested in Professor [Name]'s work on [topic], 
and the [specific lab/center] aligns with my career goal of [specific goal]. 
The curriculum includes [specific courses] that will prepare me for 
[specific career path]."

Tips:
  ✓ Research specific professors or programs
  ✓ Connect to your career goals
  ✓ Show you've done your homework

What NOT to say:
  ✗ "I heard it's easy to get into"
  ✗ "My friend said it's good"
  ✗ "I just want to go to America"

---

Q2: How will you pay for your education?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What they're assessing: Financial ability, intent to return home

Strong Answer Framework:
"My education is being funded by [source]. [Details about sponsor/self]. 
I have [amount] available in [accounts]. Here are my financial documents 
showing [specific evidence]. After graduation, I plan to return to [home 
country] where I have [ties - job offer/family business/property]."

Tips:
  ✓ Know exact amounts in your accounts
  3 Be specific about funding source
  ✓ Emphasize ties to home country

What NOT to say:
  ✗ "I'll work part-time to cover costs"
  ✗ "I'm not sure of the exact amount"
  ✗ "I'll figure it out when I get there"

---

Q3: What are your plans after graduation?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What they're assessing: Non-immigrant intent (F-1 requirement)

Strong Answer Framework:
"After completing my degree, I plan to return to [home country] to [specific 
plan - join family business / apply skills to local industry / start 
company]. My long-term goal is [specific goal that requires returning home]. 
I have [specific ties] waiting for me in [home country]."

Tips:
  ✓ Be specific about post-graduation plans
  ✓ Emphasize strong ties to home country
  ✓ Mention family, property, or career opportunities at home

What NOT to say:
  ✗ "I hope to find a job in the US"
  ✗ "I want to stay as long as possible"
  ✗ "I don't have plans yet"

[Additional questions based on visa type...]

---

🎭 INTERVIEW LOGISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What to Wear:
• Business professional or business casual
• Conservative, neat appearance
• Avoid excessive jewelry or accessories

Arrival:
• Arrive 15-30 minutes early
• Security screening - no electronics
• Wait for your number to be called

During Interview:
• Be concise (1-2 minute answers)
• Make eye contact
• Answer only what's asked
• Stay calm if interrupted
• It's okay to ask for clarification

Common Mistakes to AVOID:
✗ Memorized, robotic answers
✗ Arguing with the officer
✗ Offering unsolicited information
✗ Fidgeting or appearing nervous
✗ Bringing unnecessary documents

---

✅ PRE-INTERVIEW CHECKLIST

☐ All documents organized in folders
☐ Practiced likely questions 3+ times
☐ Reviewed strong answer frameworks
☐ Know key facts: program details, funding amounts
☐ Planned outfit
☐ Arranged transportation to consulate
☐ Confirmed appointment time and location

💡 Final Tip: The officer wants to grant the visa. 
Make it easy for them to say yes by being prepared, honest, and genuine.

⚠️  DISCLAIMER: This preparation guide is for practice only. 
Actual questions may vary. Be honest in all responses.
```

## Practice Session Guide

### Mock Interview Format
1. Set timer for 5-10 minutes (typical interview length)
2. Ask 5-8 common questions
3. Provide feedback on:
   - Answer clarity and conciseness
   - Body language observations
   - Areas needing improvement
   - Documents organization

### Red Flags to Address
- Inconsistent answers about purpose
- Unclear funding sources
- Weak ties to home country
- Evasive body language
- Over-rehearsed responses

## Post-Interview

### Outcomes
- **Approved**: Passport collected for visa stamping
- **Administrative Processing**: Additional review needed
- **Denied**: Reason given, next steps discussed

### If Denied
1. Log denial reason
2. Identify if reapplication is possible
3. Address deficiencies before reapplying
4. Consider consulting immigration attorney
