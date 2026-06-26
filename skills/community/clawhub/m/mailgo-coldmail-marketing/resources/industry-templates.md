# Industry Email Templates

Select the template matching the user's offerings. Customize placeholders — don't copy-paste verbatim.

## Industry Index

| ID | Industry | Key Buyers | Pain Points |
|----|----------|-----------|-------------|
| `saas` | SaaS / Software | VP Eng, CTO, Head of Product | Scalability, integration, dev velocity |
| `ecom` | E-Commerce / DTC | CMO, Head of Growth | CAC, conversion, retention |
| `consulting` | Consulting / Professional Services | Managing Partner, Practice Lead | Utilization, client acquisition |
| `fintech` | Financial Services / FinTech | CFO, VP Risk, Compliance | Compliance, security, efficiency |
| `manufacturing` | Manufacturing / Industrial | VP Ops, Plant Manager | Downtime, yield, supply chain |
| `education` | Education / EdTech | Dean, L&D Director | Engagement, completion rates |
| `health` | Healthcare / Life Sciences | CMO, CIO, VP Clinical Ops | Regulatory burden, patient outcomes |
| `agency` | Marketing / Creative Agency | Agency Owner, Account Director | Margins, client retention, ROI |
| `realestate` | Real Estate / PropTech | Broker, Property Manager | Lead quality, days on market |
| `general` | General B2B (fallback) | Any business buyer | Efficiency, growth, cost |

**Selection rules:**
1. Match user's offerings keywords to industry above
2. Ask only if ambiguous (e.g., "AI platform for healthcare AND finance")
3. Fall back to `general` if no fit
4. Log selection in change summary: `Industry template: SaaS (matched from "deployment automation")`

---

## SaaS / Software (`saas`)

**Tone:** Fellow builder. Technical credibility, not marketing fluff.
**Prefer:** ship, integrate, pipeline, velocity, deploy, API, SDK, uptime, latency
**Avoid:** synergy, leverage, revolutionary, game-changing

**Subjects:**
1. `How #{company name} can ship 40% faster without more headcount`
2. `A pattern I'm seeing in #{company name}'s stack`
3. `How [Similar Co] cut deployment time from 3 days to 2 hours`
4. `Quick question about #{company name}'s dev workflow`

**Body:**
```html
<p>Hi #{name},</p>
<p>I was looking at #{domain} and noticed #{company name} is scaling its engineering team — exciting momentum. When teams grow that fast, deployment bottlenecks usually become the biggest drag on velocity.</p>
<p>We built [Product] to solve exactly this. [Similar Co] cut their release cycle from 2 weeks to 3 days while reducing production incidents by 60%.</p>
<p>Would a 15-min walkthrough make sense? I can show you the specific integration with your current stack.</p>
<p>Best,<br>[Name]<br>[Title], [Company]</p>
<p style="font-size:12px; color:#999999;">P.S. If this isn't relevant, just reply and let me know — I won't reach out again.</p>
```

---

## E-Commerce / DTC (`ecom`)

**Tone:** DTC metrics-fluent. Revenue impact, not feature lists.
**Prefer:** conversion rate, AOV, retention, LTV, ROAS, cart abandonment, cohort, margin
**Avoid:** cutting-edge, best-in-class, world-class

**Subjects:**
1. `How #{company name} can recover 15% of abandoned carts`
2. `A trend I noticed in #{company name}'s category`
3. `How [DTC Brand] grew repeat purchase rate by 35% in 60 days`
4. `Quick thought on #{company name}'s retention strategy`

**Body:**
```html
<p>Hi #{name},</p>
<p>I was browsing #{domain} — great product lineup. I noticed you're in a category where repeat purchase rate is the real margin driver, yet most brands leave 20–30% of revenue on the table with post-purchase flows.</p>
<p>We help DTC brands like [Similar Brand] turn one-time buyers into repeat customers — 35% lift in 90-day repeat purchase rate and 22% LTV increase in their first quarter.</p>
<p>Worth 15 minutes to see how this applies to #{company name}? I can pull category benchmarks.</p>
<p>Best,<br>[Name]<br>[Title], [Company]</p>
<p style="font-size:12px; color:#999999;">P.S. Not the right time? Just let me know and I'll update my notes.</p>
```

---

## Consulting / Professional Services (`consulting`)

**Tone:** Concise, intellectually rigorous. Respect partner/principal hierarchy.
**Prefer:** utilization, pipeline, engagement, practice area, thought leadership, deliverable, bench time
**Avoid:** disrupt, game-changer, out-of-the-box

**Subjects:**
1. `Helping #{company name} improve consultant utilization by 20%`
2. `A challenge I hear from firms like #{company name}`
3. `How [Consulting Firm] filled their Q2 pipeline in 6 weeks`
4. `Quick question about #{company name}'s business development`

**Body:**
```html
<p>Hi #{name},</p>
<p>I know from working with professional services firms that the gap between "great at the work" and "consistently filling the pipeline" is where most firms struggle — especially when partners are stretched across delivery and BD.</p>
<p>We help firms like [Similar Firm] systematize client acquisition. They reduced partner-led BD time by 40% while increasing qualified inbound leads by 3x in one quarter.</p>
<p>Would a brief conversation make sense to see if this applies to #{company name}'s growth stage?</p>
<p>Best,<br>[Name]<br>[Title], [Company]</p>
<p style="font-size:12px; color:#999999;">P.S. If you'd prefer I didn't follow up, just let me know.</p>
```

---

## Financial Services / FinTech (`fintech`)

**Tone:** Trust and risk reduction first. Regulatory awareness is mandatory.
**Prefer:** compliance, regulatory, audit trail, risk management, SOC 2, reconciliation, AML, KYC, SLA
**Avoid:** disrupt, move fast, hack, workaround

**Subjects:**
1. `Helping #{company name} reduce compliance overhead by 50%`
2. `A regulatory shift that affects #{company name}'s operations`
3. `How [FinTech Co] automated 80% of their reconciliation`
4. `Quick question about #{company name}'s compliance workflow`

**Body:**
```html
<p>Hi #{name},</p>
<p>I've been following regulatory developments in your space, and I know the compliance burden on teams like #{company name}'s has grown significantly over the past year.</p>
<p>We help financial services firms automate manual compliance without compromising auditability. [Similar Firm] reduced their monthly reconciliation time by 80% while passing their SOC 2 Type II audit on the first attempt.</p>
<p>Would it make sense to show you how this works in about 15 minutes?</p>
<p>Best,<br>[Name]<br>[Title], [Company]</p>
<p style="font-size:12px; color:#999999;">P.S. If this isn't relevant to your current priorities, just reply and I'll note it.</p>
```

---

## Manufacturing / Industrial (`manufacturing`)

**Tone:** Pragmatic. Operational outcomes: uptime, yield, throughput.
**Prefer:** uptime, OEE, yield, downtime, preventive maintenance, supply chain, lead time, IoT, SCADA
**Avoid:** digital transformation (overused), moonshot, paradigm shift

**Subjects:**
1. `How #{company name} can reduce unplanned downtime by 30%`
2. `A trend I'm seeing on plant floors like #{company name}'s`
3. `How [Manufacturer] improved OEE from 65% to 82% in 90 days`
4. `Quick question about #{company name}'s maintenance scheduling`

**Body:**
```html
<p>Hi #{name},</p>
<p>I work with manufacturing operations teams, and unplanned downtime is consistently the single biggest drain on plant profitability — even at well-run operations like #{company name}.</p>
<p>We built [Product] to shift maintenance from reactive to predictive. [Similar Manufacturer] saw a 30% reduction in unplanned downtime within the first quarter — $1.2M in recovered production capacity.</p>
<p>Would it be worth a 15-minute call? I can share benchmark data from similar plants in your sector.</p>
<p>Best,<br>[Name]<br>[Title], [Company]</p>
<p style="font-size:12px; color:#999999;">P.S. Not the right person? Feel free to point me to whoever handles maintenance or operations planning.</p>
```

---

## Education / EdTech (`education`)

**Tone:** Mission-driven, collaborative. Avoid hard-sell language.
**Prefer:** learner outcomes, engagement, completion rates, enrollment, LMS, credentialing, skills gap
**Avoid:** monetize, exploit, aggressive growth

**Subjects:**
1. `Helping #{company name} improve course completion rates by 25%`
2. `A shift I'm seeing in learner engagement at institutions like #{company name}`
3. `How [Institution] doubled enrollment in 6 months`
4. `Quick question about #{company name}'s learner experience`

**Body:**
```html
<p>Hi #{name},</p>
<p>I know that improving learner engagement and completion rates is a top priority for teams at #{company name} — especially as expectations around digital learning keep rising.</p>
<p>We work with education organizations to close the gap between enrollment and completion. [Similar Institution] saw completion rates increase by 25%, with learner satisfaction scores jumping from 3.8 to 4.5 out of 5.</p>
<p>Would a 15-minute conversation make sense? I'd love to learn more about #{company name}'s current approach.</p>
<p>Best,<br>[Name]<br>[Title], [Company]</p>
<p style="font-size:12px; color:#999999;">P.S. If this isn't aligned with your current focus, just let me know.</p>
```

---

## Healthcare / Life Sciences (`health`)

**Tone:** Regulatory sensitivity paramount. Patient outcomes and operational efficiency.
**Prefer:** patient outcomes, clinical workflow, EHR, interoperability, HIPAA, FDA, care coordination
**Avoid:** cure, guarantee, revolutionary treatment, miracle

**Subjects:**
1. `Helping #{company name} reduce clinical documentation time by 40%`
2. `An interoperability challenge I'm hearing from teams like #{company name}`
3. `How [Health System] saved 12 hours/week per clinician on documentation`
4. `Quick question about #{company name}'s clinical workflow`

**Body:**
```html
<p>Hi #{name},</p>
<p>I work with healthcare organizations navigating the challenge of doing more with less — particularly around clinician time on documentation versus patient care. I imagine this resonates with #{company name}'s team.</p>
<p>We help health systems reduce administrative burden without compromising compliance. [Similar Health System] reduced documentation time by 40%, giving clinicians back 12 hours per week for patient-facing activities.</p>
<p>Would a 15-minute call make sense? I can walk through how we handle HIPAA compliance and EHR integration.</p>
<p>Best,<br>[Name]<br>[Title], [Company]</p>
<p style="font-size:12px; color:#999999;">P.S. If this isn't relevant right now, just reply — no further follow-up.</p>
```

---

## Marketing / Creative Agency (`agency`)

**Tone:** Agency owners scan fast. Speak to how you help them serve their clients better.
**Prefer:** client retention, billable hours, deliverables, attribution, retainer, scope creep, pitch win rate
**Avoid:** one-stop-shop, turnkey, holistic (overused)

**Subjects:**
1. `How #{company name} can increase client retention by 30%`
2. `A margin challenge I hear from agencies like #{company name}`
3. `How [Agency] doubled their retainer revenue in 6 months`
4. `Quick question about #{company name}'s client reporting`

**Body:**
```html
<p>Hi #{name},</p>
<p>Running an agency means constantly balancing creative quality with operational margins — and at #{company name}, proving measurable ROI is what keeps retainers growing instead of churning.</p>
<p>We help agencies like [Similar Agency] automate the parts of client reporting that eat into billable hours. They increased client retention by 30% and freed up 15 hours per week across their account team.</p>
<p>Worth a 15-minute look to see if this applies to #{company name}?</p>
<p>Best,<br>[Name]<br>[Title], [Company]</p>
<p style="font-size:12px; color:#999999;">P.S. Not the right fit? Just let me know — I appreciate the candor.</p>
```

---

## Real Estate / PropTech (`realestate`)

**Tone:** Relationship-driven, deal-focused. Local and personal.
**Prefer:** listings, days on market, closing rate, occupancy, lead quality, CRM, MLS, cap rate, NOI
**Avoid:** disruptive, revolutionary, paradigm

**Subjects:**
1. `How #{company name} can reduce average days on market by 20%`
2. `A lead quality challenge I hear from teams like #{company name}`
3. `How [Brokerage] increased their close rate by 25% in one quarter`
4. `Quick question about #{company name}'s lead pipeline`

**Body:**
```html
<p>Hi #{name},</p>
<p>I work with real estate teams, and the consistent challenge I hear is that lead volume isn't the problem — lead quality is. Too much time on leads that never convert while high-intent prospects slip through.</p>
<p>We help teams like [Similar Brokerage] prioritize their pipeline. They improved close rate by 25% and reduced average days to close by 15 days within the first quarter.</p>
<p>Would a quick 15-minute call make sense? I can show how this works with your current CRM.</p>
<p>Best,<br>[Name]<br>[Title], [Company]</p>
<p style="font-size:12px; color:#999999;">P.S. If now isn't a good time, just let me know and I'll circle back.</p>
```

---

## General B2B (`general`)

Fallback when no specific industry fits.

**Subjects:**
1. `How #{company name} can improve [key metric] by [X]%`
2. `A pattern I'm seeing in #{company name}'s industry`
3. `How [Similar Company] achieved [specific result] in [timeframe]`
4. `Quick question about #{company name}'s [relevant process]`

**Body:**
```html
<p>Hi #{name},</p>
<p>I came across #{company name} and noticed [specific observation]. It seems like your team is focused on [inferred priority].</p>
<p>We work with companies like [Similar Company] to [one-sentence value prop]. They saw [specific metric] within [timeframe].</p>
<p>Would a 15-minute conversation make sense to see if this could help #{company name}?</p>
<p>Best,<br>[Name]<br>[Title], [Company]</p>
<p style="font-size:12px; color:#999999;">P.S. If this isn't relevant, just reply and let me know — I won't reach out again.</p>
```

---

## Usage Rules

1. Replace all `[bracketed placeholders]` with real data from user's offerings. **NEVER leave `[brackets]` in the final email output** — they must be replaced with actual sender data or the sentence must be rewritten without them.
2. **Conditional `#{...}` variables:** Only use a `#{...}` placeholder if the corresponding recipient data is confirmed available. If data is NOT available:
   - `#{name}` → use "Hi" / "您好" (no name)
   - `#{company name}` → use "your company" / "贵公司" or omit the sentence
   - `#{domain}` → omit the sentence referencing it
   - `#{title}` → omit or use generic phrasing
3. Match vocabulary from "Prefer" list; avoid words in "Avoid" list
4. Replace `[Similar Company]` with realistic reference if available; otherwise use "a mid-size [industry] company"
5. Target 100–150 words; never exceed 150 for cold emails
6. **Sender signature must use real data** (collected from user): actual name, title, company name, and optionally website. Never output placeholder text like `[Name]` or `[Company]` in the sent email.

### Placeholder Availability Examples

**All recipient data available** (name, company, domain):
```html
<p>Hi #{name},</p>
<p>I was looking at #{domain} and noticed #{company name} is scaling...</p>
```

**Only name available** (no company, no domain):
```html
<p>Hi #{name},</p>
<p>I work with companies in your industry that are scaling their operations...</p>
```

**No recipient data available** (email only):
```html
<p>Hi there,</p>
<p>I work with companies in your industry that are scaling their operations...</p>
```
