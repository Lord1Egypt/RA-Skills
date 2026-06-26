# Post-Approval Planning

## Purpose
Guide users through next steps after visa approval, including pre-departure preparation, arrival procedures, and establishing life in the new country.

## When to Use
- "My visa was approved! What's next?"
- "I'm moving to [country] in 3 months"
- "What do I need to do before I leave?"
- "What should I do when I arrive?"

## Pre-Departure Checklist (30-90 days before)

### Documents & Legal
- [ ] Valid passport with visa stamp
- [ ] Print approval notices and correspondence
- [ ] Obtain certified copies of important documents
- [ ] Prepare document folder (carry-on, not checked luggage)
- [ ] Research entry requirements (what to declare)

### Financial
- [ ] Notify banks of move (avoid frozen accounts)
- [ ] Set up international banking/transfer options
- [ ] Understand tax implications (exit tax, future filing requirements)
- [ ] Convert some currency for immediate expenses
- [ ] Research credit score transferability (varies by country)

### Housing
- [ ] Research neighborhoods and housing market
- [ ] Arrange temporary accommodation for arrival
- [ ] Understand rental requirements (deposits, credit checks)
- [ ] Consider whether to ship belongings or buy new

### Healthcare
- [ ] Get medical records from current providers
- [ ] Fill prescriptions (3-6 month supply if allowed)
- [ ] Research healthcare system in destination
- [ ] Understand health insurance requirements
- [ ] Get dental/vision checkups before leaving

### Employment/Business
- [ ] Understand visa work restrictions
- [ ] Prepare for first day (documents, orientation)
- [ ] Research professional licensing requirements
- [ ] Join professional networks in destination

### Personal
- [ ] Cancel or transfer utilities and services
- [ ] Update address with all important contacts
- [ ] Arrange mail forwarding
- [ ] Say goodbyes and collect contact info
- [ ] Research cultural norms and basic language

## Arrival Checklist (First 7 days)

### Immediate (Day 1-2)
- [ ] Clear immigration and customs
- [ ] Activate phone/get local SIM
- [ ] Check into temporary accommodation
- [ ] Get local currency if needed
- [ ] Eat and rest (combat jet lag)

### First Week
- [ ] Attend any required registration (police, etc.)
- [ ] Open bank account
- [ ] Get local phone number
- [ ] Apply for Social Security/Equivalent number
- [ ] Understand public transportation
- [ ] Find grocery stores and essentials

## First 30-90 Days

### Essential Setup
| Task | Timeline | Notes |
|------|----------|-------|
| Permanent housing | 0-30 days | Start looking immediately |
| Driver's license | 30-90 days | May need tests; rules vary |
| Healthcare registration | 0-30 days | Find primary care doctor |
| Schools (if children) | Before arrival | Enrollment requirements |
| Work authorization verification | First week | With employer HR |

### Building a Life
- [ ] Join local expat/community groups
- [ ] Explore your neighborhood
- [ ] Find hobbies/activities
- [ ] Build social network
- [ ] Understand local customs and etiquette

## Rights and Restrictions by Visa Type

### Work Visas
**Typical Rights:**
- Work for sponsoring employer
- Live in country
- Travel in and out (with valid visa)
- Some allow spouse to work (varies)

**Typical Restrictions:**
- Cannot change employers without new visa
- Must maintain employment
- Limited/unauthorized work for spouse
- May need permission for extended travel

**Path to Permanent Residence:**
- Employer sponsorship for green card/permanent residency
- Time in status varies by country
- May require labor certification

### Student Visas
**Typical Rights:**
- Study at designated institution
- Limited on-campus work
- Some off-campus work authorization (varies)

**Typical Restrictions:**
- Must maintain full-time student status
- Work limitations strictly enforced
- Must show intent to return home

**Post-Graduation:**
- Optional Practical Training (US)
- Post-Study Work Visa (UK, Australia)
- PGWP (Canada)
- Pathways to permanent residence

### Family-Based Visas
**Typical Rights:**
- Live and work (conditional or permanent)
- Access to public benefits (varies)
- Travel freely

**Typical Restrictions:**
- Conditional residence may apply (2-year period)
- Must file to remove conditions
- Relationship must remain genuine

## Data Structure

```json
{
  "post_approval": {
    "application_id": "APP-12345",
    "approval_date": "2024-03-01",
    "visa_type": "H-1B",
    "country": "USA",
    "planned_move_date": "2024-04-15",
    
    "pre_departure_tasks": [
      {
        "task": "Notify bank of move",
        "category": "financial",
        "completed": true,
        "due_date": "2024-03-15"
      }
    ],
    
    "arrival_tasks": [
      {
        "task": "Apply for SSN",
        "category": "legal",
        "completed": false,
        "due_date": "2024-04-22"
      }
    ],
    
    "notes": "Moving to San Francisco; employer providing temporary housing"
  }
}
```

## Script Usage

```bash
# Generate post-approval checklist
python scripts/post_approval_checklist.py \
  --application-id "APP-12345" \
  --move-date "2024-04-15" \
  --destination "San Francisco, CA"

# Mark task complete
python scripts/post_approval_checklist.py \
  --action update \
  --task "Apply for SSN" \
  --status completed
```

## Output Format

```
POST-APPROVAL CHECKLIST
H-1B Visa Approved | USA
Planned Move: April 15, 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 CONGRATULATIONS! Your H-1B visa has been approved.

PRE-DEPARTURE (Next 45 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Documents & Legal [2/5 complete]
☑ Print all approval notices
☐ Obtain certified copies of birth/marriage certificates
☐ Prepare document folder for carry-on
☐ Research customs/declaration requirements
☐ Verify passport validity (6+ months)

Financial [1/4 complete]
☑ Notify banks of move date
☐ Set up international transfers
☐ Understand US tax filing requirements
☐ Research US credit building options

Housing [0/3 complete]
☐ Research SF neighborhoods
☐ Arrange temporary accommodation
☐ Join housing/roommate groups

Healthcare [0/3 complete]
☐ Request medical records
☐ Fill 90-day prescription supply
☐ Research US health insurance options

⚠️  IMPORTANT TASKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 Book flight (prices rising)
🚨 Request medical records (takes 2-4 weeks)
📅 Notify current landlord by March 15

---

ARRIVAL CHECKLIST (First 30 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Week 1:
☐ Clear immigration at SFO
☐ Check into temporary housing
☐ Activate US phone number
☐ Attend HR orientation
☐ Get employee badge/ID

Week 2:
☐ Apply for Social Security Number
☐ Open US bank account
☐ Find permanent housing
☐ Get local transit card

Week 3-4:
☐ Enroll in health insurance
☐ Find primary care doctor
☐ Get California driver's license
☐ Register car (if shipping)
☐ Explore neighborhood

---

VISA-SPECIFIC INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your H-1B Rights:
• Work for [Petitioning Employer] in approved position
• Live anywhere in the US
• Travel internationally with valid visa
• Spouse can apply for H-4 (work authorization possible)

Your H-1B Restrictions:
• Cannot change employers without H-1B transfer
• Must maintain employment with petitioning employer
• Maximum 6 years in H-1B status (extensions possible if PR pending)
• Unemployment = 60-day grace period to find new sponsor

Path to Permanent Residence:
• Employer can sponsor for green card
• Process: PERM → I-140 → I-485
• Timeline: 1-3+ years depending on country of birth
• Discuss with employer HR about sponsorship timeline

---

RESOURCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

San Francisco Specific:
• Housing: Craigslist, Facebook groups, Zillow
• Expat communities: InterNations, Meetup
• Transportation: Clipper card for transit

Important Numbers:
• USCIS Contact: 1-800-375-5283
• SSA (Social Security): 1-800-772-1213
• Your employer HR: [Contact info]

⚠️  Remember: You have 60 days grace period if employment ends.
    Keep emergency fund accessible.
```

## Reverse Culture Shock

Many immigrants experience adjustment challenges:
- **Week 1-2**: Excitement, novelty
- **Month 1-3**: Reality sets in, homesickness common
- **Month 3-6**: Establishing routines, making friends
- **Month 6+**: Settling in, feeling at home

**Tips:**
- Stay connected with home but build local life
- Be patient with yourself
- Join expat groups for support
- Celebrate small wins
- Learn the local language even if not required
