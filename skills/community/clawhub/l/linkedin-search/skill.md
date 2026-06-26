# /linkedin-search — LinkedIn Candidate Search

Automatically search LinkedIn candidates based on user requirements using Chrome DevTools MCP. Saves profiles to `./linkedin-save/{role}/` to prevent duplicate scans.

---

## Phase 0 — Clarify Requirements Before Searching

**Before any PRE-CHECK or search begins**, ask the user the following questions if their request does not already answer them clearly. Wait for the user's response before proceeding.

### 0.1 — Target Count

If not specified:
```
How many candidates are you looking for? (default: 20)
```

### 0.2 — Criteria Classification (Hard vs. Soft)

Present the inferred criteria list and ask the user to confirm which are hard requirements and which are soft preferences:

```
I've identified the following candidate criteria from your request.
Please confirm which are hard requirements (must-have, disqualify if missing)
and which are soft preferences (nice-to-have, lower priority but not disqualifying):

Criteria detected:
  • Cloud experience ≥ X years         → [ Hard / Soft / Remove ]
  • Total experience ≤ Y years         → [ Hard / Soft / Remove ]
  • Presales title clearly stated       → [ Hard / Soft / Remove ]
  • Public cloud experience (AWS/GCP…) → [ Hard / Soft / Remove ]
  • Private cloud experience            → [ Hard / Soft / Remove ]
  • [any other criteria from user]      → [ Hard / Soft / Remove ]

Note: Current location and most-recent-role relevance are always verified on the
profile page and cannot be removed — they are built-in hard constraints.

Hard criteria: candidates failing ANY of these are rated C (flagged, not excluded).
Soft criteria: missing ones lower the match level from A → B but do not disqualify.

Reply with your preferred classification, or type "use defaults" to accept the above.
```

> **Why ask:** The same criterion (e.g., "cloud experience") can mean a dealbreaker to one hiring manager and a nice-to-have to another. Asking upfront prevents the LLM from applying the wrong threshold during profile analysis.

### 0.3 — Location Scope

If not specified:
```
Should the location filter be strict (exact city only) or broad (country-level)?
Example: "Hanoi only" vs. "anywhere in Vietnam"
(default: country-level)
```

### 0.4 — Company Target Filter (Optional)

```
Do you want to target candidates from specific companies?
(e.g., FPT, Viettel, Google, AWS, Oracle — leave blank to skip)
```

Once all answers are collected, proceed to PRE-CHECK.

---

## Parameter Layering

The user's natural language query must be split into two layers **after Phase 0 and before searching begins**:

### Layer 1: Search Parameters (hard-embedded in query)

These two types of conditions directly determine the Google/LinkedIn search string. **Without them, retrieval is impossible.**

| Parameter | Description | Example |
|-----------|-------------|---------|
| **Job keyword** | Must appear in the query | `presales solution architect` |
| **Location** | City or country, must appear in the query | `hanoi` / `vietnam` |

Built into the search query directly:
```
site:linkedin.com/in/ ("presales" OR "pre-sales") "cloud" "hanoi"
```

> **Important:** Layer 1 parameters are search *hooks* — they cast a wide net. They do **not** guarantee the candidate currently lives in that location or currently holds that type of role. Both must be re-verified on the profile page (see Constraints 1 & 2 in Layer 2 below).

### Layer 2: LLM Analysis Parameters (inferred after profile content is retrieved)

These conditions **cannot be filtered at the search stage**. The LLM reads the profile text and infers each one.

The hard/soft designation for user-defined criteria comes from **Phase 0.2**. The two location and role constraints below are always Hard.

| Parameter | Hard/Soft | Inference Method |
|-----------|-----------|-----------------|
| Cloud experience (≥ N years) | **Hard** (configurable) | Sum duration of cloud-related roles |
| Total experience (≤ N years) | **Hard** (configurable) | Infer first job start year → years to today |
| Presales explicitly stated | **Hard** (configurable) | Job title contains presales/pre-sales/solution consultant, or bio describes it |
| **Current location matches target** | **Always Hard** | Read profile header location — must match target city/country; a past role's location does not count |
| **Most recent role is relevant** | **Always Hard** | Candidate's latest job must relate to the target role — a keyword match in an older position is not sufficient |
| Public cloud experience | Soft (default) | Role mentions AWS/Azure/GCP/OCI/VNG/Viettel Cloud etc. |
| Private cloud experience | Soft (default) | Role mentions OpenStack/VMware/private deployment/on-premise cloud |

**LLM Inference Rules:**
- If duration is insufficient to judge, mark `unknown`; lower match_level to B or C
- **[Constraint 1 — Location re-validation]:** The search query embeds the target location to surface profiles — but a profile can appear because the location keyword appeared in an old job entry or a past employer's address. After loading the profile, read the **location shown in the profile header** (e.g., "Hanoi, Vietnam") as the candidate's *current* location. If it does not match the target, set `location_match: false` and downgrade match_level one tier (A→B, B→C). If the header location is hidden or empty, mark `location_match: unknown` and treat as B.
- **[Constraint 2 — Current role relevance]:** The search query embeds job keywords — but the matching title may be from years ago while the candidate's current work is completely unrelated. After loading the profile, find the **first (most recent) entry in the Experience section**. Check whether that role's title or description is relevantly related to the target role. If unrelated, set `current_role_relevant: false` and downgrade match_level one tier. "Relevant" means same domain (e.g., presales, solution architecture, cloud consulting) — an exact title match is not required, but a pivot to an unrelated field (e.g., now a full-time developer or finance manager) is a fail.
- All **hard** criteria met (including Constraints 1 & 2) → **A**; some met or one `unknown` → **B**; URL only or very little content → **C**

> **Match level is driven by the user-confirmed hard/soft split from Phase 0.2.** If the user reclassified "presales title" as Soft, a candidate without it can still reach A. However, **location match and current-role relevance are always Hard** and cannot be reclassified to Soft.

---

## Runtime Environment Requirements

All conditions below must be met before execution. **Complete PRE-CHECK in order before starting the search. If any condition fails, output the fix instructions and stop.**

### Condition 1: Chrome Debug Session is Running

Chrome must be running in remote debug mode on **port 9222**, using a user profile with an active LinkedIn session.

**Verification:** Call `mcp__chrome-devtools__list_pages`. If it returns a page list, pass.

**If not met:**
```
❌ Chrome debug session not ready

Run the following steps in your terminal:

1. Close all Chrome windows (or force-quit):
   pkill -9 -f "Google Chrome"

2. Copy your login profile (first time only):
   mkdir -p /tmp/chrome_debug_profile
   cp -r ~/Library/Application\ Support/Google/Chrome/Default/{Cookies,"Login Data","Web Data",Preferences,"Local State"} \
     /tmp/chrome_debug_profile/ 2>/dev/null

3. Launch Chrome in debug mode:
   nohup "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --remote-debugging-port=9222 \
     --user-data-dir="/tmp/chrome_debug_profile" \
     --no-first-run --disable-sync \
     > /tmp/chrome_debug.log 2>&1 &

4. Wait 3 seconds, then re-run /linkedin-search
```

### Condition 2: LinkedIn is Logged In

The browser must have an active LinkedIn session (used to access profiles and internal search).

**Verification:** Navigate to `https://www.linkedin.com/feed/` and run:
```javascript
() => document.querySelector('.global-nav__me-photo') !== null ||
      document.querySelector('[data-control-name="nav.homepage"]') !== null ||
      !document.URL.includes('/login')
```
Returns `true` → pass.

**If not met:**
```
❌ LinkedIn not logged in

Please log in to LinkedIn manually in Chrome:
1. Visit https://www.linkedin.com in the already-open Chrome window
2. Complete login (credentials or verification code)
3. Confirm you reach the LinkedIn feed, then re-run /linkedin-search
```

### Condition 3: linkedin-save Directory Exists

`./linkedin-save/` must exist in the current working directory.

**Verification:**
```bash
ls ./linkedin-save/ 2>/dev/null || echo "MISSING"
```

**If not met:**
```
❌ linkedin-save directory missing

Auto-creating now... (running mkdir -p ./linkedin-save)
```
> This condition is auto-fixed by the skill — no user action needed.

### Condition 4: Correct Working Directory

The skill runs under `/Users/junye/project/test-case/linkedin-zp` for relative paths to resolve correctly.

**Verification:**
```bash
pwd
```

**If not met:**
```
❌ Working directory mismatch

Current: {actual pwd}
Expected: /Users/junye/project/test-case/linkedin-zp

Please reopen the session in the correct directory, or confirm the actual location of linkedin-save.
```

---

## PRE-CHECK Execution Order

```
[0] Clarify requirements (Phase 0)    → wait for user response, then continue
[1] Check Chrome debug session        → fail: output fix, stop
[2] Check LinkedIn login              → fail: output fix, stop
[3] Check/create linkedin-save        → auto-fix
[4] Check working directory           → mismatch: warn (do not force stop)
[5] Parse query → output Layer 1 / Layer 2 breakdown
[6] Load already-scanned URL set      → continue
✅ All passed → begin search
```

**[5] Breakdown output example:**
```
🔍 Search parameter breakdown:

[Layer 1 — Search Query (hard-embedded)]
  Job keywords: presales solution architect / pre-sales / solution consultant
  Location: hanoi, vietnam
  Company filter: FPT, Viettel (if specified)

[Layer 2 — LLM Analysis Conditions (inferred from profile)]
  Always Hard: current location verified on profile page / most recent role relevance
  Hard: cloud experience ≥ 5 years / total experience ≤ 15 years / presales explicitly stated
  Soft: public cloud preferred / private cloud is a bonus

Target candidates: 20
Save directory: ./linkedin-save/presales-architect/
Location scope: country-level (Vietnam)
```

---

## Execution Steps

> All steps below run only after **PRE-CHECK** (including Phase 0 and parameter breakdown) has fully passed.

### STEP 0 — Determine Save Directory, Load Scanned URLs (dedup)

Map job keywords to subdirectory:

| Role Type | Directory |
|-----------|-----------|
| Presales Architect | `./linkedin-save/presales-architect/` |
| Solution Architect | `./linkedin-save/solution-architect/` |
| Cloud Sales | `./linkedin-save/cloud-sales/` |
| Other | `./linkedin-save/general/` |

Load already-scanned URLs:
```bash
grep -h "^url:" ./linkedin-save/{role_dir}/*.md 2>/dev/null | awk '{print $2}'
```

### STEP 1 — Collect Candidate URLs (Google → LinkedIn internal)

Use **Layer 1 parameters** (job keywords + location) to build search queries.

**Primary: Google site search**

Try strategies in order (replace `{role}` and `{location}` with actual Layer 1 values):
```
# A: Exact title
site:linkedin.com/in/ ("presales" OR "pre-sales") "cloud" "{location}"

# B: Extended title variants
site:linkedin.com/in/ "solution architect" "cloud" "presales" "{location}"

# C: Target company filter (if user specified companies in Phase 0.4)
site:linkedin.com/in/ ("presales" OR "solution architect") "cloud" ("FPT" OR "Viettel" OR "VNPT" OR "CMC" OR "AWS" OR "Oracle") "{location}"
```

Paginate: append `&start=10`, `&start=20` to the URL.

**Extract Google results JS:**
```javascript
() => {
  const out = [];
  document.querySelectorAll('h3').forEach(h3 => {
    const block = h3.closest('.g') || h3.closest('[data-hveid]') || h3.closest('[jscontroller]');
    const a = block && block.querySelector('a[href*="linkedin.com/in/"]');
    if (a) out.push({
      url: a.href.split('?')[0].replace(/^https?:\/\/[a-z]+\.linkedin\.com/, 'https://www.linkedin.com'),
      title: h3.innerText,
      snippet: block ? block.innerText.slice(0, 300) : ''
    });
  });
  return out;
}
```

**Fallback: LinkedIn internal search** (when Google results are insufficient)

Embed Layer 1 parameters in the URL (`{keywords}` = job keywords, `{geoUrn}` = location ID):
```
https://www.linkedin.com/search/results/people/?keywords={keywords}&geoUrn=%5B%22{geoUrn}%22%5D&origin=FACETED_SEARCH&page=N
```

Common geoUrns:
- Vietnam: `104195383`
- Hanoi: `104195383` (country-level, no single-city ID)
- Ho Chi Minh City: `104195383`

**Extract LinkedIn search results JS:**
```javascript
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  for (let y = 0; y <= 5000; y += 300) { window.scrollTo(0, y); await sleep(150); }
  await sleep(2000);
  return Array.from(document.querySelectorAll('a[href*="/in/"]'))
    .map(a => ({ href: a.href.split('?')[0], text: a.innerText.trim().slice(0, 200) }))
    .filter(l => /linkedin\.com\/in\/[^/]+\/?$/.test(l.href) && l.text.length > 3)
    .filter((v, i, a) => a.findIndex(x => x.href === v.href) === i);
}
```

### STEP 2 — Visit Each Profile (skip already-scanned), LLM Analyzes Layer 2

For each new URL:

1. `navigate_page` (allow timeout, continue executing)
2. Run scroll + extract script to get raw text:

```javascript
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  for (let y = 0; y <= 8000; y += 300) { window.scrollTo(0, y); await sleep(200); }
  await sleep(2000);
  const t = document.body.innerText;
  const ei = t.indexOf('Experience');
  return {
    header: t.slice(0, 2500),
    exp: ei > -1 ? t.slice(ei, Math.min(ei + 4000, t.length)) : '',
    url: location.href.split('?')[0]
  };
}
```

> Note: The extraction script searches for `'Experience'` (English). If the profile is in another language, also try `'工作经历'` (Chinese) as a fallback index key.

3. **LLM analyzes Layer 2 conditions** (inferred from header + exp text):

```
Analyze each criterion below. Mark "unknown" if insufficient data.
Apply the hard/soft classification confirmed by the user in Phase 0.2.

STEP A — Constraint 1: Location re-validation
  Read the location line in the profile header (the line directly under the candidate's name).
  Compare it against the target location.
  → location_match: true / false / unknown

STEP B — Constraint 2: Current role relevance
  Identify the first (topmost) entry in the Experience section — this is the most recent role.
  Check whether its title or description is relevantly related to the target role domain.
  → current_role_relevant: true / false / unknown
  → current_role: "{title} @ {company} ({start}–{end})"

STEP C — User-defined criteria
  - cloud_years: sum duration of roles mentioning AWS/Azure/GCP/OCI/cloud keywords
  - total_years: infer earliest job start year → years to today
  - presales: does job title or bio contain presales/pre-sales/solution consultant?
  - public_cloud: any AWS/Azure/GCP/OCI/public cloud experience?
  - private_cloud: any OpenStack/VMware/private deployment/on-premise experience?

STEP D — match_level
  Start from the highest possible level and downgrade for each failure:
  Base: A
  → If location_match = false or unknown: downgrade one tier
  → If current_role_relevant = false or unknown: downgrade one tier
  → If any Hard user criterion fails or is unknown: downgrade one tier
  → If content is URL-only or nearly empty: set C directly

  Final: A / B / C
```

4. **Save profile immediately** → STEP 3

### STEP 3 — Save Profile (URL is mandatory; content is best-effort)

File path: `./linkedin-save/{role_dir}/{linkedin_id}.md`
`linkedin_id` = last segment of the URL, e.g., `nguyen-the-hung-70725b1b`

**Minimal format (URL only):**
```markdown
---
name: unknown
url: {full LinkedIn URL}
location: unknown
location_match: unknown
current_role: unknown
current_role_relevant: unknown
cloud_years: unknown
total_years: unknown
public_cloud: unknown
private_cloud: unknown
presales: unknown
match_level: C
scanned_date: {YYYY-MM-DD}
---
```

**Full format (LLM-inferred content):**
```markdown
---
name: Nguyen The Hung
url: https://www.linkedin.com/in/nguyen-the-hung-70725b1b/
location: Hanoi, Vietnam
location_match: true
current_role: Customer Solution Consultant – GCP @ Google (2022–present)
current_role_relevant: true
cloud_years: 8
total_years: 15
public_cloud: true
private_cloud: true
presales: true
match_level: A
scanned_date: 2026-04-28
---

## Summary
{LLM's 2–3 sentence evaluation of Layer 2 criteria, including explicit notes on
location verification and current role relevance}

## Experience
{Work experience text extracted from the page}
```

### STEP 4 — Loop Until Target Met

Count profiles where match_level is A or B:
```bash
grep -l "match_level: [AB]" ./linkedin-save/{role_dir}/*.md 2>/dev/null | wc -l
```

If target not reached, switch search terms and continue (only vary **Layer 1 parameters**; Layer 2 criteria stay fixed):
- Job variants: `"technical presales"` / `"pre-sales engineer"` / `"solution consultant"`
- Location stays the same, but may substitute company names: `FPT` / `Viettel` / `CMC` / `VNPT` / `Noventiq`

---

## Output Summary

When complete, output:

```
## Candidate Summary — {role}, {location}

[Search criteria]  Role: presales solution architect | Location: hanoi
[Analysis criteria] Location verified on profile (Hard) | Current role relevance (Hard)
                    Cloud exp ≥ 5yr (Hard) | Total exp ≤ 15yr (Hard) | Presales stated (Hard) | Public cloud preferred (Soft)

| # | Name | Current Role @ Company | Location | Loc✓ | Role✓ | Cloud Yrs | Presales | Level | Link |
|---|------|------------------------|----------|------|-------|-----------|----------|-------|------|
| 1 | Nguyen The Hung | GCP Consultant @ Google | Hanoi, VN | ✅ | ✅ | 8yr | ✅ | A | [🔗](url) |
| 2 | Tran Van A | Dev Manager @ Bank | HCMC, VN | ❌ | ❌ | 3yr | ❌ | C | [🔗](url) |
...

A: N  |  B: N  |  C: N (needs manual review)
Saved to ./linkedin-save/presales-architect/ (N profiles total)
```

---

## Notes

- **URL must always be saved**: even if the page is completely blank, save the minimal profile with the URL
- **3rd-degree wall**: 3rd-degree connections' experience sections are not visible; LLM infers from header/bio only — mark as C, leave `exp` empty
- **Navigation timeout**: on timeout, continue running the scroll script (page may have partially loaded)
- **Dedup check**: before saving, grep to check if the URL already exists — skip if already scanned
- **Rate limiting**: natural delay is built in (the scroll script takes ~4 seconds per profile)
- **Layer 1 is non-negotiable**: location and job keywords must go into the query — post-hoc LLM filtering alone is not sufficient
- **Hard/soft classification governs match_level**: always apply the classification confirmed in Phase 0.2, not the defaults
- **Location re-validation is always required** (Constraint 1): the profile header location is ground truth — a past job's city is not the candidate's current location
- **Current role relevance is always required** (Constraint 2): check the topmost Experience entry, not the one that matched the search keyword — a presales role from 5 years ago does not make a current developer relevant
