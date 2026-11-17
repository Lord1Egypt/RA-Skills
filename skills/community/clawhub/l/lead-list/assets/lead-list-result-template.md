# Find Leads: result layout

Fill in each {placeholder} and keep this order. Leave out a line that has
nothing to say. Per-call costs and identifiers go only in Details.

**{ready} of {asked} ready · {verified} verified · {catch_all} catch-all · ${spent} · {minutes} min**
{Titles} at {who the user sells to}, one per company.
CRM-ready file: {file name} ({ready} rows).
{The main gap in one plain sentence, or: Everything you asked for is here.}

| # | Name | Title | Company | Why it matched | Email | Status |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Alex Example | Founder & CEO | Example Books Ltd | Bookkeeping for UK tradespeople · 23 staff · Bristol, UK | alex@example.com | verified |
| 2 | Sam Sample | Managing Director | Example Accounts Ltd | Accountants for UK dental practices · 41 staff · Leeds, UK | sam@example.org | catch-all: test first |

Catch-all means the company's mail server accepts any address, so the check
can't confirm this one. Test first: send at most 50, keep going only if bounces
stay under 1%.

{n} failed: provider unavailable, not charged. Retry with the backup route for up to ${x}?
{n} had no one with those titles. Try {other title} at those companies for up to ${x}?

**Before you email**

- Keep each contact's Source URL. In the UK and EU you must tell people where
  you got their details, in your first email at the latest (GDPR Article 14).
- US: CAN-SPAM covers business email too: an honest subject line, your postal
  address and a working unsubscribe.
- UK: you can email people at companies, but sole traders and some
  partnerships must have opted in first.
- Germany: expect to need opt-in consent before a cold email, even to
  businesses.
- This is a summary, not legal advice.

**Research the top 10 →** See which of these to contact now, why (with dated
sources) and what to ask first. When fewer than 10 are ready, offer them all:
"Research these {ready} →".

## Details

**How the list was built:** {found} companies found → {checked} checked →
{fit} fit → {searched} searched → {people} people found → {ready} ready.
{Only if it happened: Paused after 10 companies with {n} ready; you chose
{other titles, a smaller batch or to carry on}.}

**Left out**

| Company | Reason |
| --- | --- |
| {company} | Not a fit: {reason} |
| {company} | Website now redirects to {other firm}: merged or acquired |
| {company} | No one with those titles found |
| {company} | Provider unavailable, not charged |
| {company} | Email didn't pass the check |

**Every paid call**

| Step | Tool | Run ID | Cost |
| --- | --- | --- | ---: |
| {step} | {tool id} | {run id} | ${cost} |
| **Total** (approved maximum ${max}) | | | **${spent}** |

**Limits.** Verified means the address accepted mail today; it isn't consent
and doesn't promise a reply. Titles come from public sources and can be out of
date. Fit comes from company data and websites, not from talking to the
company. Nothing was sent and nothing was added to your CRM.
