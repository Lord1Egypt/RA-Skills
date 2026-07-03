# Change Management

## Objectives

Design and drive a change management plan to ensure IT transformation is accepted and adopted by the organization, turning "resistance" into "momentum" so that new systems and processes are actually used.

---

## Prerequisites
- Change scope is clearly defined (what is changing? who is impacted?)
- Project plan is already underway (change management must run in parallel with the project, not as an afterthought)
- Key stakeholders have been preliminarily identified

## Inputs
- Project charter and plan
- Stakeholder analysis (from workflow 02-02)
- Change impact assessment (which roles/processes/tools will change)
- Organizational chart

---

## Operation Steps

### Step 1: Change Impact Assessment

#### 1.1 Four Dimensions of Change

| Dimension | Question to Answer | Example |
|------|-----------|------|
| **Process** | How will people's way of working change? | "Before: manual order entry → After: system auto-capture" |
| **Role** | Whose role/responsibility/authority will change? | "Regional managers lose independent pricing authority, replaced by system AI pricing" |
| **Skills** | What new skills are needed? Which old skills are no longer needed? | "Data analysis skills are needed; pure manual report-making skills are no longer required" |
| **Culture** | How will "the way we do things around here" change? | "From 'the boss decides' → 'the data decides'" |

#### 1.2 Impacted Group Analysis

| Impacted Group | Headcount | Impact Level (1-5) | What They Lose (Acknowledge) | What They Gain (Emphasize) |
|-----------|------|-------------|-----------|-----------|
| Frontline Customer Service | 200 | 4 | Familiar interface + room for improvisation | Standardized scripts reduce errors + AI assistance improves efficiency |
| Regional Managers | 20 | 5 | Pricing discretion | More time for client relationships + AI pricing recommendations |
| IT Operations | 10 | 3 | Familiar tech stack | New skills (Cloud/K8s) + increased market value |

**Key Insight**: You must acknowledge what people are losing — you cannot just say "this will be better." People are twice as sensitive to "loss" as to "gain" (loss aversion).

---

### Step 2: Change Strategy Design

#### 2.1 ADKAR Model Application

ADKAR is a personal change model developed by Prosci. Every individual goes through these five stages when experiencing change:

| Stage | Meaning | What to Do at This Stage | Indicator of Completion |
|------|------|---------------|----------------|
| **A**wareness | Know why change is needed | Communicate the reason for change: "what happens if we don't change" + "what it looks like after change" | Employees can articulate why change is needed |
| **D**esire | Willingness to participate and support | Address WIIFM (What's In It For Me): what's the benefit for me? | Employees actively participate rather than passively accept |
| **K**nowledge | Know how to change | Training: how to use new processes/systems — not generic slide decks | Employees can demonstrate how to use the new system |
| **A**bility | Can perform at the expected level | Hands-on practice + coaching + tolerance for initial inefficiency | Employees reach expected performance levels under the new process |
| **R**einforcement | Can sustain the change | Positive feedback + course correction + celebrate success + institutionalize new behaviors | New behaviors become "this is how we've always done it" |

#### 2.2 Kotter's 8-Step Change Model Application

```
Step 1: Create Urgency
   → Not "IT wants to roll out a new system," but "the market is abandoning companies that fail to digitize"

Step 2: Form a Powerful Coalition
   → Find cross-functional influential supporters, not just the CIO

Step 3: Create a Vision for Change
   → "Where are we going together?" Articulate it in one sentence

Step 4: Communicate the Vision
   → Through multiple channels / repetition / leading by example — not a mass email blast

Step 5: Remove Obstacles
   → Identify and clear out systems / processes / people that block change

Step 6: Create Short-Term Wins
   → Produce visible success within the first 3–6 months so skeptics see "this thing actually works"

Step 7: Build on the Change
   → Don't declare victory after one small win; keep pushing until change becomes DNA

Step 8: Anchor the Changes in Culture
   → "This is how we do things," not "that IT project from last year"
```

---

### Step 3: Communication Plan

#### 3.1 Core Communication Principles

1. **Answer "why" first, then "how"** — People don't resist change; they resist "not knowing why we're changing"
2. **Repeat 7 times** — People typically need to hear something 7 times to remember and internalize it
3. **Multiple channels** — Email + meetings + 1-on-1s + intranet + posters + watercooler conversations = all are essential
4. **Leaders go first** — If the CEO is still using the old way, no one will believe the change is serious
5. **Be honest** — "I don't know" > making up answers; "this will be hard for some people" > "everything will go smoothly"

#### 3.2 Segmented Communication Plan

| Audience | What They Care About | Channel | Spokesperson | Frequency |
|------|-----------|----------|--------|------|
| CEO / Board | ROI / competitiveness / risk | Monthly briefing + SteerCo | CIO / Project Sponsor | Monthly |
| Business VPs | Team efficiency / goal achievement | SteerCo + 1-on-1 | CIO + Business Sponsor | Biweekly |
| Middle Managers | Team stability / performance | Monthly communication meeting + FAQ | Change Lead + Department VP | Monthly |
| Frontline Employees | Will my job change / will it get harder | Team meeting + intranet + WeCom | Direct manager + Change Champion | Biweekly |
| IT Team | Technical details / workload | Sprint Review + tech sharing | IT Director | Weekly |
| External (Customers / Suppliers) | Will service be disrupted | Account Manager / Procurement | Account Manager | Per milestone |

#### 3.3 Key Communication Milestones

```
Project Kickoff: CEO all-staff email — why we are changing
  ↓
Month 1: Department Town Hall — what this means for your department
  ↓
2 weeks before each milestone: "What's coming" — advance notice
  ↓
1 week after each milestone: "What we accomplished" — celebrate
  ↓
When problems arise: "What happened + what we're doing + estimated resolution time" — honest and transparent
```

---

### Step 4: Training Plan

#### 4.1 Training Is Not About Slide Decks

```
Wrong training:                          Right training:
"Please look at this system feature      "Now, open your computer and follow me
 overview slide deck, 120 slides..."     to complete the first thing you'll do
                                         today..."
                                         (Hands-on + Real Scenario + Immediate Feedback)
```

#### 4.2 Tiered Training Design

| Tier | Audience | Training Content | Method | Duration | Timing |
|------|------|---------|------|------|------|
| Awareness | All staff | Why change + what the change is + what it means for me | All-hands meeting + video | 1 hour | At project kickoff |
| Management | Managers with teams | How to lead teams through change + how to answer subordinates' questions + how to identify team anxiety | Workshop | Half day | 1 month before training |
| Super Users | 1–2 people per department | Deep system usage + common issues + how to help others | Hands-on training | 2 days | 3 weeks before Go-live |
| End Users | All users | How to complete their own scenarios in the new system | Group hands-on + simulation exercises | 1–3 days (by role) | 2 weeks before Go-live |
| New Hires | Subsequent onboardees | New system training integrated into onboarding | Online / recorded | As needed | Ongoing after Go-live |

#### 4.3 Training Effectiveness Verification

- [ ] Post-training test: Can they independently complete 3 core tasks?
- [ ] Go-live Week 1: Super Users present on-site in every department
- [ ] Go-live Month 1: Track each user's usage frequency; identify non-users and misusers; conduct 1-on-1 coaching

---

### Step 5: Change Champion Network

#### 5.1 How to Select Change Champions

- Trusted by colleagues (not necessarily a manager / leader)
- Curious about new things
- Influential within their department (people listen to their opinions)
- Willing to spend time helping others

#### 5.2 What Change Champions Do

```
What Change Champions are NOT:             What Change Champions ARE:
- IT's mouthpiece                          - The "first responder" within their own team
- An extra workload burden                 - Peer Support (colleague helping colleague)
- Only showing up during Go-live Week 1    - A role sustained for 3–6 months
```

**Monthly Commitment**: Approximately 5–10% of working time
**Incentives**: Recognition (public CEO acknowledgment) + career development (this is a leadership experience) + small reward (e.g. $500)

---

### Step 6: Resistance Management

#### 6.1 Forms of Resistance

| Overt Resistance | Covert Resistance (More Common) |
|---------|---------------|
| Open opposition / questioning | Skipping training |
| Complaints / grievances | "Too busy, no time to learn" |
| Demanding restoration of old ways | Doing it the old way privately, entering fake data in the new system |
| Threatening to quit | Passive usage (doing only the bare minimum) |

#### 6.2 Root Causes of Resistance and Responses

| Root Cause | What They're Really Thinking | Response Strategy |
|------|---------|---------|
| Fear of job loss | "AI / automation will replace me" | Clearly state change ≠ layoffs; emphasize new skills = new value; provide transfer / training opportunities |
| Loss of power | "I used to have the final say, now the system decides" | Understand the importance of power; convert "lost power" into "new forms of power" (e.g. becoming an expert / trainer) |
| Burned before | "They said the same thing last time, spent $X, and nothing changed" | Acknowledge history; explain specifically what's different this time; prove it with a Quick Win first |
| Don't understand | "I don't get why we need to change — isn't everything fine now?" | Explain "the cost of not changing" in their language; have peers who have already changed share their stories |
| Distrust | "I don't trust IT / consultants / management to pull this off" | Transparent communication of progress (including problems); deliver on small promises to build trust |
| Fatigue | "We've already changed so many times — can we just take a break?" | Acknowledge change fatigue; explain how this change relates to others; clarify "no more upheaval after this one" |

#### 6.3 Resistance Escalation Path

```
Level 1: Individual complaints / passivity → Change Champion 1-on-1 listening, understand specific concerns
Level 2: Small-group resistance → Change Lead intervenes, responds together with department head
Level 3: Department-level resistance → Sponsor (CIO + Business VP) responds directly; adjust approach if necessary
Level 4: Systemic resistance → Pause, reassess change strategy; may need to adjust pace / scope / communication approach
```

---

### Step 7: Adoption Tracking

#### 7.1 Adoption Dashboard

| Metric | How to Measure | Pre-Go-live | M1 Target | M3 Target | M6 Target |
|------|---------|--------|--------|--------|--------|
| System Login Rate | System logs | — | 80% | 95% | 98% |
| Core Feature Usage Rate | Feature instrumentation | — | 60% | 80% | 90% |
| Data Completion Rate | Required field completion | — | 70% | 85% | 95% |
| Old-Way Abandonment Rate | Process audit | 0% | 30% | 70% | 95% |
| User Satisfaction (NPS) | Survey | — | -10 | +10 | +30 |
| Training Completion Rate | LMS | — | 80% | 95% | 100% |
| Help Desk Ticket Volume | ITSM system | 0 | High | Declining | Low and stable |

#### 7.2 When to Sound the Alarm

| Signal | Threshold | Response |
|------|------|------|
| Login Rate | <50% (M1) | Investigate causes: system broken? don't know how to use it? not needed? |
| Help Desk Tickets | Sustained increase (M2–3) | Indicates insufficient training or too many system issues |
| Old ways still in use | >50% (M2) | Targeted department 1-on-1s; understand why "new is worse than old" |
| Satisfaction | NPS persistently negative (M3) | In-depth interviews; could be a system issue or a change management issue |

---

## Outputs
1. **Change Impact Assessment**: Four-dimension impact + impacted group analysis
2. **Change Strategy**: ADKAR + Kotter application
3. **Communication Plan**: Segmented audience + multi-channel + timed milestones
4. **Training Plan**: Tiered training + hands-on design + effectiveness verification
5. **Change Champion Network**: Roster + responsibilities + incentives
6. **Resistance Management Plan**: Anticipated resistance + responses + escalation path
7. **Adoption Dashboard**: Metrics + baselines + targets

*(See templates/change-management-plan-template.md for detailed templates)*

---

## Quality Checklist
- [ ] Change impact assessment is not "everyone will benefit" — honestly acknowledges "who loses what"
- [ ] Communication plan has specific people / times / channels (not "we need to communicate more")
- [ ] Training is hands-on, not slide-deck-based
- [ ] Change Champions are volunteers (not assigned by managers)
- [ ] Adoption metrics are tracked from Day 1 (not discovered after Go-live that no one is using it)
- [ ] Sponsor (CEO / CIO) is willing to personally participate in key communication milestones

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Right Approach |
|------|---------|---------|
| Change management = something to do after Go-live | Doing change management after Go-live = buying insurance after a fire | Change management runs in parallel from Day 1 of the project |
| Communication = sending a mass email | An email's open rate <30%, read-thoroughly rate <10% | Multi-channel + multi-frequency + leader-delivered in person + interactive Q&A |
| Only saying "this is great" without saying "who will feel pain" | People see through false propaganda instantly | Be honest: "This will be a challenge for Group XX, and here's how we'll support them..." |
| Neglecting middle managers | CEO supports it, frontline is willing, but middle managers are stuck (they have the most to lose) | Invest extra energy caring for middle managers; help them find their value in the new world |
| Backing down at the first sign of resistance | Normal change will encounter resistance; backing down empowers opponents | Distinguish "constructive feedback" (listen) from "pure resistance" (manage) |
| Declaring victory too early | "System went live! Change succeeded!" → in reality, no one is using it | Let adoption data do the talking; don't rely on "gut feeling" |

---

## IT Organizational Change Management

### The Unique Nature of IT Change
Unlike general change, IT change has the following unique challenges:
- **Dual transformation of technology and people**: Not just process changes — the technology itself is also changing
- **Ambidextrous organization**: Daily operations (Keep the Lights On) vs. innovation transformation (Runway to the Future) coexist
- **Technical debt as a resistance to change**: Legacy systems are not just a technical issue — they are also a power-structure issue
- **Digitization paradox**: Digitization improves efficiency, but for displaced employees it means job-loss anxiety

### Supplementary IT Change Management Frameworks
| Change Type | ADKAR Focus | Key Additional Tools |
|---------|---------|------------|
| ERP Go-live | K→A (Knowledge→Ability) | Super User network + Simulation testing |
| Cloud Migration | A→D (Awareness→Desire) | FinOps change management (cost transparency reduces resistance) |
| AI Transformation | A→D→R (Awareness→Desire→Reinforcement) | AI literacy assessment + Job Crafting |
| DevOps / Agile Transformation | D→A→R (Desire→Ability→Reinforcement) | Team Topologies + Psychological safety measurement |
| Zero Trust Security | A→D (Awareness→Desire) | Security behavior Change Agents |

### Ten Disciplines of IT Change Management
1. **Data beats Opinion**: Measure change with adoption data, not "gut feeling"
2. **Acknowledge loss**: Be honest and transparent about "who loses what"; loss aversion coefficient = 2
3. **Middle managers are the decisive factor**: CEO support + frontline willingness + middle managers stuck = change deadlock
4. **Quick Win in 90 Days**: Must have visible results within 90 days
5. **70-20-10 Rule**: 70% practice + 20% coaching + 10% training
6. **Change fatigue monitoring**: Be alert when there are >3 concurrent changes
7. **Super Users are Volunteers**: Super Users must be volunteers
8. **System decommissioning ≠ change success**: The old way no longer being used is what success looks like
9. **KPI / OKR alignment**: Compensation must align with change objectives
10. **CIO leads by example**: Leaders demonstrate new behaviors first