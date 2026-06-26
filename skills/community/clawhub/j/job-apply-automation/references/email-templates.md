# Email Templates
### job-email-apply / references

These are the base templates the agent uses to compose application emails.
The agent fills in [BRACKETED] placeholders based on the job listing and CV.
Do not remove brackets — they are the agent's insertion points.

Keep all emails under 200 words. Recruiters skim. Brevity signals confidence.

---

## Template 1: cold-application
**Use for:** Most applications. Direct to a careers email or recruiter.

---

**Subject:** Application — [JOB TITLE] | [YOUR FULL NAME]

Hi [RECRUITER NAME / "there" if unknown],

I'm a [YOUR SENIORITY] developer with [X] years building [ONE-LINE SUMMARY OF YOUR STACK]. I came across the [JOB TITLE] role at [COMPANY] and wanted to reach out directly.

A few things that stood out in the listing:

→ [SKILL/REQUIREMENT 1 from JD] — [one sentence connecting this to your experience]
→ [SKILL/REQUIREMENT 2 from JD] — [one sentence connecting this to your experience]
→ [SKILL/REQUIREMENT 3 from JD] — [one sentence connecting this to your experience]

[OPTIONAL: One sentence about why this company specifically interests you. Only include if you have something genuine — skip otherwise.]

I've attached my CV. Happy to jump on a call at your convenience.

Best,
[YOUR FULL NAME]
[YOUR LINKEDIN URL]
[YOUR PHONE — optional]

---

## Template 2: startup-application
**Use for:** Companies under ~50 people, early-stage startups, Wellfound listings.
Warmer tone. Shows you understand startup context.

---

**Subject:** [JOB TITLE] — [YOUR FULL NAME]

Hi [NAME],

I've been following [COMPANY] for a while — [ONE GENUINE OBSERVATION about the product, recent launch, or founding story. Agent: check the company's website and recent news before writing this line. Do not fabricate].

I'm a [SENIORITY] developer focused on [YOUR MAIN STACK]. I've been in startup environments before and know what it means to move fast, own things end to end, and not wait for a ticket to fix something obvious.

Your listing mentioned [SKILL 1] and [SKILL 2] — both are areas I've shipped production work in. [ONE SPECIFIC EXAMPLE — brief, concrete].

CV attached. Would love to chat if you think there's a fit.

[YOUR FULL NAME]
[YOUR LINKEDIN]

---

## Template 3: referral-application
**Use for:** When you have a named contact at the company, or someone referred you.

---

**Subject:** [JOB TITLE] referral — [REFERRING PERSON'S NAME] suggested I reach out

Hi [NAME],

[REFERRING PERSON] suggested I get in touch about the [JOB TITLE] opening at [COMPANY].

I'm a [SENIORITY] developer with [X] years in [STACK]. [REFERRING PERSON] thought my background in [RELEVANT AREA] would be a good fit for what you're building.

[TWO BULLET POINTS connecting your experience to the role — same format as cold-application template]

Happy to share more — CV is attached.

[YOUR FULL NAME]
[YOUR LINKEDIN]

---

## Template 4: interview-reply
**Use for:** Responding to a recruiter who wants to schedule an interview.
Agent uses this automatically when processing inbox.

---

**Subject:** Re: [ORIGINAL SUBJECT]

Hi [NAME],

Great to hear from you — I'd love to connect.

I'm available:
→ [DAY 1], [DATE] between [TIME RANGE] [TIMEZONE]
→ [DAY 2], [DATE] between [TIME RANGE] [TIMEZONE]
→ [DAY 3], [DATE] between [TIME RANGE] [TIMEZONE]

Happy to work around your schedule if none of those suit. Looking forward to speaking.

[YOUR FULL NAME]

---

## Template 5: follow-up
**Use for:** Following up on an application with no response after 7 days.
Agent sends this once per application maximum. Do not send a second follow-up.

---

**Subject:** Following up — [JOB TITLE] application | [YOUR FULL NAME]

Hi [NAME / "there"],

I sent an application for the [JOB TITLE] role on [DATE APPLIED] and wanted to follow up briefly.

I'm still very interested in the position and happy to provide any additional information. If the role has been filled, no worries at all.

[YOUR FULL NAME]

---

## Customisation Notes for the Agent

When filling these templates:

1. The opening line referencing the company should be specific and real.
   Check the company website for: recent product launches, blog posts,
   funding announcements, notable customers. One real observation lands
   better than three generic compliments.

2. Match the exact terminology from the job description.
   If they say "distributed systems" say "distributed systems" not
   "scalable infrastructure." ATS systems and humans both respond to
   vocabulary mirroring.

3. Never invent experience. If the CV does not evidence a skill the JD
   requires, do not claim it in the email. Mention adjacent skills instead.

4. Salary. Do not mention salary in the outbound email unless the listing
   explicitly asks for it, in which case use the range from PROFILE in SKILL.md.

5. Subject lines matter more than most people think.
   Format is always: [Role] — [Your Name] or [Role] | [Your Name]
   Never: "RE: Job Application" or "Enquiry about position"
