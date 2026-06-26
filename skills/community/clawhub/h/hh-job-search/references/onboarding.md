# Onboarding

Use this flow when a user is starting from scratch or sends a resume/CV.

## Goal

Turn a raw resume into a usable job-search project and, when relevant, prepare the user for HH Browser Relay automation.

## Resume-first onboarding

When the user sends a resume, CV, or pasted experience summary:

1. Extract factual candidate data only.
2. Initialize a job-search project if it does not exist yet.
3. Fill or update:
   - `PROFILE.md`
   - `TARGET_ROLES.md`
   - `SEARCH_RULES.md`
4. Keep uncertainty explicit:
   - unknown salary targets stay blank or marked for confirmation
   - inferred target roles should be marked as draft assumptions until the user confirms
5. After parsing the resume, give the user a short summary:
   - what was extracted confidently
   - what still needs confirmation
   - what sources can already be searched safely

## Minimum questions after resume parsing

Ask only the missing high-value questions, for example:
- desired salary floor / target
- remote vs hybrid vs office
- preferred cities / countries
- whether recruiter outreach is allowed
- whether automatic applications are allowed

Do not ask for details already present in the resume.

## HH / Browser Relay onboarding

If the user wants hh.ru automation (resume raising, logged-in vacancy review, or assisted HH apply), explain that a logged-in browser session is required.

Give concise instructions:

1. Open hh.ru in Chrome.
2. Log into the desired hh account.
3. Open the target tab you want the agent to use.
4. Click the OpenClaw Browser Relay extension icon on that tab so the badge turns ON.
5. Tell the agent the relay is attached, then continue.

Explain why only briefly: Browser Relay lets the agent work with the user’s already logged-in tab without asking for passwords.

## What to do after relay setup

Once the relay is attached:
- refresh the active hh search or resume page before trusting visible state
- verify whether resumes are available to raise or still in cooldown
- only then run hh-specific automation

## When not to push Browser Relay

Do not ask the user to set up Browser Relay unless the task actually needs logged-in browser automation.

Examples that usually do NOT need relay:
- parsing a resume
- building a candidate profile
- scoring already exported vacancies
- editing search rules
- preparing a shortlist from local files

## First-run response shape

For a brand-new user who sent a resume, prefer this response shape:

1. short acknowledgement
2. extracted role/profile summary
3. missing confirmations
4. next step recommendation
5. Browser Relay instruction only if hh automation is part of the next step
