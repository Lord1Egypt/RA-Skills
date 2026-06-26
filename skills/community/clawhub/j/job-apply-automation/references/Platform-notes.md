# Platform Notes
### job-email-apply / references

Platform-specific behaviour, quirks, and tips the agent should know
before searching or applying. Update this file as you learn more.

---

## LinkedIn

**Finding emails:**
LinkedIn hides emails by default. In order of reliability:
1. Check the job listing itself — some smaller companies include an email
2. Click "Easy Apply" — if there's an email field listed in the form, that's the address
3. Check the recruiter's LinkedIn profile — some list contact emails
4. Search "[company name] recruiter email" or "[company name] jobs email"
5. Try the company's LinkedIn page → About → Website → find careers page there

**Rate limiting:**
LinkedIn monitors for unusual search patterns. Do not run more than
30 listing searches in a single session. Spread across natural pauses.

**Easy Apply listings:**
Prefer these — they signal the company is actively processing volume
and is more likely to check their email pipeline too.

**InMail:**
Do not use InMail. It costs credits and has lower response rates than
a direct email for developer roles.

---

## Indeed

**Finding emails:**
Indeed has moved most applications in-house via their apply system,
which doesn't give you the company's email. Workaround:
1. Check if the listing includes a company website link
2. Visit the company's careers page directly
3. Look for a "apply via email" option — some listings still have it
4. If no email route exists, mark EMAIL_NOT_FOUND and move on

**Listing quality:**
Indeed aggregates from many sources — some listings are months old.
Check the "Posted X days ago" label. Skip listings older than 30 days.

**Salary data:**
Indeed often shows estimated salary ranges even when the company
doesn't list one. These are estimates — treat them as rough signals,
not hard data. Do not cite them in emails.

---

## Glassdoor

**Finding emails:**
Similar to Indeed. Most applications go through Glassdoor's internal system.
Best approach: find the company website from the Glassdoor listing and
locate the careers/jobs page directly — most companies with Glassdoor
listings also have a direct application route on their site.

**Reviews as signal:**
Glassdoor reviews are useful for scoring the `company quality` factor.
Red flags: consistent mentions of poor management, frequent layoffs,
"looks great on paper", engineering team instability.
Check the "Culture & Values" and "CEO Approval" scores as quick proxies.

**Listing freshness:**
Glassdoor listings can go stale. Prioritise listings posted within 14 days.

---

## Wellfound (AngelList Talent)

**Best platform for:**
Startups, Series A–C companies, remote-first roles, roles with equity.

**Finding emails:**
Wellfound is more transparent than other platforms. Many listings include:
- The hiring manager's name and Wellfound profile
- A "Message" button that functions like an email
- Some include direct email addresses

Use the startup-application template for all Wellfound listings.

**Salary and equity:**
Wellfound listings usually include salary ranges and equity grants.
These are more reliable than estimates on other platforms. Use them
for the salary matching in the scoring criteria.

**Company signals:**
- Check funding stage: Seed/Series A = high risk, high upside
- Check team size on the listing — under 20 people = early stage tone
- Check when the company was founded — less than 2 years old = very early

---

## Direct Company Careers Pages

Some companies post roles exclusively on their own site.
Check these regularly if they are companies you actively want to work at.
Add them to the TARGET COMPANIES list below.

**Finding the application email:**
Most company careers pages have one of:
1. A direct "Apply" button that opens a mailto: link — this gives you the email
2. An application form — look in the page source for `action="mailto:..."` 
3. A generic jobs@ or careers@ address listed in the footer or About page

---

## TARGET COMPANIES
Companies you specifically want to work at.
Agent should check these career pages every session even if they don't
appear in job board searches.

```
- https://stripe.com/jobs
- https://linear.app/careers
- https://vercel.com/careers
- [ADD YOUR TARGET COMPANIES HERE]
```

---

## EXCLUDE LIST
Companies to never apply to, regardless of listing quality or match score.
Agent cross-references this with the `do_not_apply` array in Applications.json.

```
[Add companies here as you encounter them]
```

Reasons to add a company:
- Known for ghosting or poor candidate experience
- Publicly known poor engineering culture
- Personal decision (previous bad experience, conflict of interest, etc.)
- Company is in a sector you don't want to work in

---

## General Email Tips

**Best days to send:**
Tuesday, Wednesday, Thursday. Avoid Friday afternoons and Monday mornings.
If the agent runs daily, deprioritise Friday sends for roles at companies
where getting lost in a weekend inbox would hurt your chances.

**Follow-up timing:**
Send the follow-up template (Template 5) after exactly 7 days with no response.
Do not follow up a second time. One follow-up per application, maximum.

**Response rate benchmarks:**
These are rough industry averages for developer roles via email:
- Cold email to large company: 5–15% response rate
- Cold email to startup: 20–35% response rate
- Referral email: 40–60% response rate

If your response rate drops below 5% across 20+ applications,
something is wrong — likely the email templates, the CV, or the
match scoring threshold. Review and adjust before continuing.

**Red flags in job listings:**
- "We move fast" without specifying what that means
- "Unlimited PTO" (often means no actual PTO culture)
- No salary listed + startup without public funding info
- Role has been reposted multiple times (check the listing date history)
- "Rockstar" or "ninja" in the title
- Requirements list asks for 5+ years of experience in a technology
  that is less than 5 years old
