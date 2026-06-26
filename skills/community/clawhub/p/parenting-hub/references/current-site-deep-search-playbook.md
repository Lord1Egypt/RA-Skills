# Current-Site Deep Search Playbook

This reference records how the crawler is currently used to deeply search already-configured authoritative maternal-child sources.

Date anchor: `2026-04-22`

## Purpose

Use this playbook when the goal is:

- keep the source universe fixed
- search deeper inside existing authoritative sites
- improve extraction success before expanding to new domains
- record what has actually been searched versus only configured

This is an operational crawl/search playbook, not a public evidence-answering spec.

## Code Paths

Core files:

- `/Users/cathleenlin/Desktop/code/momaiagentweb/website/nextjs-project/scripts/scrapers/global-sources-config.js`
- `/Users/cathleenlin/Desktop/code/momaiagentweb/website/nextjs-project/scripts/scrapers/global-auto-scraper.js`
- `/Users/cathleenlin/Desktop/code/momaiagentweb/website/nextjs-project/scripts/scrapers/scraper-utils.js`

Outputs:

- local snapshots: `/Users/cathleenlin/Desktop/code/momaiagentweb/website/nextjs-project/data/scraped`
- database tables: `articles`, `citations`

## What "Search" Means Here

In this project, "search" does not mean a generic web search engine query.

It means:

1. choose a configured authority source
2. start from `categories`, `directSeeds`, `searchUrl`, or `sitemapUrl`
3. recursively discover more leaf pages inside that same site
4. filter to maternal-child / clinical / safety / feeding / postpartum topics
5. extract page content with source-specific selectors
6. dedupe and save good pages into the article store

## Current Search Method

### 1. Keep the source universe fixed

Do not add new domains until the current domains are better exhausted.

Current deep-search priority set:

- `US_CDC`
- `US_MAYO_CLINIC`
- `US_STANFORD_CHILDRENS`
- `UK_NHS`
- `CA_HEALTH_CANADA`
- `CA_PHAC`
- `GLOBAL_WHO`
- `US_AAP`
- `CA_CARING_FOR_KIDS`
- `AU_PREGNANCY_BIRTH_BABY`
- `US_WOMENS_HEALTH`
- `UK_NHS_START4LIFE`
- `AU_RAISING_CHILDREN`
- `NZ_PLUNKET`
- `US_KIDSHEALTH`
- `US_CLEVELAND_CLINIC`
- `EU_WHO_EUROPE`
- `SG_HEALTH_HUB`
- `US_FDA`
- `US_NICHD_SAFE_TO_SLEEP`
- `US_ACOG`

### 2. Prefer site-native entry points

For each source, define one or more of:

- `categories`: hub or section pages
- `directSeeds`: known high-value leaf pages
- `searchUrl`: site-specific search page
- `sitemapUrl`: sitemap feed

Rule of thumb:

- use `categories` when section pages expose many child links
- use `directSeeds` when the site is heavy, dynamic, or known to hide good leaf pages
- use both when the site needs a strong starting inventory plus recursive discovery

### 3. Separate discovery from extraction

Discovery should stay light and fast.

Current implementation:

- `fetchPage(url, source, 'discovery')`
- shorter timeout
- no forced browser rendering by default
- `usePuppeteerFallback` only if the source explicitly opts into it for discovery

Content extraction is slower and may use browser rendering if needed.

Why:

- browser-heavy discovery wastes time on hub pages
- Mayo and some Canada pages are expensive enough that discovery and extraction must be treated differently

For anti-bot domains such as Mayo Clinic, use a browser-discovered search page when plain HTTP category discovery returns `403` or `Page Not Found`.

Current pattern:

- use browser search to collect official result URLs
- ignore external/news network results
- convert the official result URLs into `directSeeds`
- keep extraction on the canonical Mayo article URL
- if headless browser extraction still returns a generic section title, prefer `playwright` with `browserHeadless: false`
- when a page `h1` is only a generic section label such as `Infant and toddler health`, fall back to `og:title` / document title

### 4. Normalize URLs before dedupe

All candidate URLs are normalized before storage.

Current normalization:

- remove `#hash` fragments
- keep the canonical absolute URL when possible

Why:

- Canada and PHAC pages often expose many anchor links to the same document
- without hash stripping, one page can look like hundreds of false new pages

### 5. Filter aggressively before extraction

Before a URL becomes a candidate article:

- reject excluded hosts such as `tools.cdc.gov`
- reject non-English paths such as `/espanol`
- apply source-level `excludePatterns`
- apply page-level `pageRules`
- require maternal-child topic fit via `TOPIC_PATTERNS`
- require URL fit via `linkPattern`

This keeps the inventory closer to real clinical or guidance pages.

### 6. Use recursive discovery, but keep it bounded

Current deep-search default in the current pass is usually:

- `discoveryDepth: 2`
- source-specific `discoveryMaxPages`

This means:

- start from seed/category pages
- collect matching links
- revisit those discovered pages once
- collect their matching child links

This has been enough to unlock many missed NHS, Canada, CDC, WHO, Stanford, and Mayo leaf pages without turning into an uncontrolled crawl.

### 6a. Use official-domain search and browser verification when recursion plateaus

When recursive discovery starts mostly producing duplicate slugs, continue searching inside the same current sites with targeted official-domain search.

Current pattern:

- run official-domain searches such as `site:mayoclinic.org ...`, `site:cdc.gov ...`, `site:canada.ca ...`, `site:stanfordchildrens.org ...`
- only keep official-domain leaf pages
- verify suspicious Stanford or Mayo URLs with a real browser or a direct `200/404` check
- convert confirmed good pages into `directSeeds`
- convert confirmed dead pages into `pageRules` with `exclude: true`

Examples from the current pass:

- `CDC`: expanded into `infant-feeding-emergencies-toolkit/php/*`
- `Health Canada`: corrected canonical paths for `Safety of Donor Human Milk in Canada` and `Safety of Homemade Infant Formulas in Canada`
- `Stanford`: confirmed `how-breastmilk-is-made` and `breastfeeding-your-premature-baby` as real pages, and confirmed `newborn-care-90-P02692` as a real `404`
- `Mayo`: added postpartum and disease-condition leaf pages found via official-domain search instead of only section recursion
- `AAP/HealthyChildren`: added formula-feeding, crying/colic, preemie, and teething branches found through official-domain search
- `CPS/Caring for Kids`: added breastfeeding, pregnancy-and-babies, and safe-sleep handout branches found through official-domain search
- `Pregnancy Birth & Baby`: added baby feeding, safety, sleep/settling, and development branches found through official-domain search
- `FDA`: corrected infant-formula canonical paths and added parent/caregiver, professional safe-handling, Cronobacter, homemade formula, and infant formula outbreak pages
- `NICHD Safe to Sleep`: added back sleeping, tummy time, safe sleep environment, breastfeeding/safe sleep, and risk-factor pages
- `ACOG`: added postpartum, breastfeeding, pregnancy mental health, postpartum pain, birth control, and newborn bonding pages

Official-domain search queries recorded from the latest pass:

- `site:healthychildren.org/English/ages-stages/baby/Pages OR site:healthychildren.org/English/ages-stages/baby/feeding-nutrition/Pages HealthyChildren baby breastfeeding formula sleep newborn AAP`
- `site:fda.gov/food infant formula parents caregivers safety preparation powdered formula FDA`
- `site:pregnancybirthbaby.org.au breastfeeding newborn baby formula safe sleep pregnancy birth baby`
- `site:caringforkids.cps.ca/handouts/pregnancy-and-babies breastfeeding feeding baby newborn Caring for Kids`
- `site:fda.gov/food infant formula preparation storage powdered infant formula cronobacter parents caregivers FDA`
- `site:fda.gov/food infant formula recalls safety alerts parents caregivers FDA`
- `site:fda.gov/food food safety babies pregnant people infant formula FDA`
- `site:fda.gov/food infant formula information caregivers "FDA"`
- `site:safetosleep.nichd.nih.gov safe sleep baby infant SIDS tummy time caregivers NICHD`
- `site:safetosleep.nichd.nih.gov reduce risk safe sleep babies NICHD`
- `site:safetosleep.nichd.nih.gov resources caregivers baby safe sleep NICHD`
- `site:acog.org/womens-health/faqs breastfeeding your baby postpartum care having a baby ACOG`
- `site:acog.org/womens-health/faqs postpartum depression breastfeeding pregnancy baby ACOG`
- `site:acog.org/womens-health/faqs newborn postpartum birth control breastfeeding ACOG`
- `site:womenshealth.gov breastfeeding postpartum depression postpartum care infant feeding womenshealth.gov`
- `site:womenshealth.gov breastfeeding your baby pumping milk formula postpartum womenshealth.gov`
- `site:womenshealth.gov/mental-health/mental-health-conditions/postpartum-depression womenshealth.gov postpartum depression signs treatment help`
- `site:womenshealth.gov/pregnancy/childbirth-and-beyond/postpartum-care womenshealth.gov postpartum care recovery warning signs`
- `site:nhs.uk/start-for-life/baby/ breastfeeding bottle feeding formula newborn sleep start for life`
- `site:nhs.uk/start-for-life/baby/ safe sleep crying colic newborn feeding start for life`
- `site:raisingchildren.net.au/newborns breastfeeding bottle feeding sleep health daily care newborns raising children`
- `site:raisingchildren.net.au/newborns/breastfeeding-bottle-feeding/ raisingchildren newborns breastfeeding bottle feeding`
- `site:raisingchildren.net.au/newborns/sleep/ raisingchildren newborn sleep settling safe sleep`
- `site:plunket.org.nz your-child baby feeding and nutrition sleep plunket breastfeeding newborn`
- `site:nice.org.uk postnatal care breastfeeding newborn recommendations nice ng194 cg93 infant feeding`
- `site:nice.org.uk guidance newborn jaundice faltering growth maternal child nutrition postnatal care NICE`
- `site:kidshealth.org/en/parents/pregnancy-newborn breastfeeding formula feeding newborn sleep safe sleep parents`
- `site:my.clevelandclinic.org/health/articles infant sleep baby feeding formula newborn postpartum Cleveland Clinic`
- `site:my.clevelandclinic.org/health/diseases newborn jaundice colic diaper rash postpartum depression Cleveland Clinic`
- `site:who.int/europe breastfeeding infant feeding newborn safe sleep WHO Europe`
- `site:healthhub.sg/en baby breastfeeding formula sleep feeding newborn HealthHub`
- `site:unicef.org/parenting food nutrition breastfeeding positions common breastfeeding problems solid foods SIDS UNICEF`
- `site:unicef.org/parenting/food-nutrition breastfeeding 6-12 months 1-2 years solid foods UNICEF`
- `site:llli.org/breastfeeding-info positioning storing human milk pumping milk postpartum mood disorders La Leche League`
- `site:llli.org/breastfeeding-info safe sleep skin-to-skin bottle introduction starting solids LLLI`

Search result handling:

- only official-domain results were accepted as seeds
- AAP, CPS/Caring for Kids, Pregnancy Birth & Baby, FDA, NICHD Safe to Sleep, and ACOG were converted into direct/category seeds and re-crawled
- WomensHealth.gov and NHS Start for Life were converted into direct/category seeds and re-crawled
- external share URLs, `mailto:` links, PDFs, and non-English FDA Spanish slugs were excluded or cleaned after verification
- low-value NHS Start for Life `recipes-and-meal-ideas` pages were cleaned back out and then excluded from future passes
- candidate URL normalization now removes non-root trailing slashes so slash variants do not create duplicate crawl attempts
- `medical-only` authority filtering now includes `national-child-health-service`, which is needed to crawl Plunket
- `medical-only` authority filtering now includes `nonprofit-health-system`, which is needed to crawl KidsHealth

Latest ingestion verification:

- query window: last 6 hours on `2026-04-22`
- total newly inserted scraper articles: `212`
- `Pregnancy, Birth & Baby (Australian Government)`: `103`
- `American Academy of Pediatrics (AAP)`: `79`
- `Caring for Kids (Canadian Paediatric Society) (CPS)`: `30`
- suspicious URL audit for ReadSpeaker, external Mater brochures, Spanish WomensHealth, and PBB A-Z letter pages: `0`

Latest continuation ingestion verification:

- query window: last 2 hours on `2026-04-22`
- total newly inserted scraper articles after cleanup: `32`
- `American College of Obstetricians and Gynecologists (ACOG)`: `23`
- `U.S. Food and Drug Administration (FDA)`: `6`
- `NICHD Safe to Sleep (NICHD / NIH)`: `3`
- suspicious URL audit for LinkedIn, `mailto:`, Spanish FDA slugs, Spanish WomensHealth, external Mater brochures, and ReadSpeaker: `0`

Latest continuation ingestion verification after WomensHealth + NHS Start for Life cleanup:

- query window: last 8 hours on `2026-04-23`
- total newly inserted scraper articles after cleanup: `67`
- `NHS Start4Life (NHS)`: `58`
- `Office on Women's Health (U.S. Department of Health and Human Services)`: `9`
- suspicious URL audit for recipes, LinkedIn, `mailto:`, Spanish variants, and ReadSpeaker: `0`

Latest continuation ingestion verification after Raising Children + Plunket:

- query window: last 6 hours on `2026-04-23`
- total newly inserted scraper articles after cleanup: `107`
- `Plunket (Plunket)`: `34`
- `Raising Children Network (Australian Government)`: `6`
- `NHS Start4Life (NHS)`: `58`
- `Office on Women's Health (U.S. Department of Health and Human Services)`: `9`
- suspicious URL audit for recipes, LinkedIn, `mailto:`, Spanish variants, ReadSpeaker, and PDF asset pages: `0`

Latest continuation ingestion verification after KidsHealth + Cleveland Clinic + WHO Europe + HealthHub:

- query window: last 6 hours on `2026-04-23`
- total newly inserted scraper articles after cleanup: `128`
- `Cleveland Clinic (Cleveland Clinic)`: `6`
- `HealthHub Singapore (Health Promotion Board)`: `6`
- `KidsHealth (Nemours) (Nemours Foundation)`: `7`
- `World Health Organization (Europe) (WHO)`: `2`
- `Plunket (Plunket)`: `34`
- `Raising Children Network (Australian Government)`: `6`
- `NHS Start4Life (NHS)`: `58`
- `Office on Women's Health (U.S. Department of Health and Human Services)`: `9`
- suspicious URL audit for ReadSpeaker, recipes, LinkedIn, `mailto:`, Spanish variants, support/helpdesk URLs, API URLs, and PDF asset pages: `0`

### 7. Use site-specific selectors instead of generic largest-block extraction

Each source should declare strong selectors when possible.

Examples:

- CDC: `#content`, `#main-content`, `main`, `article`, `.syndicate`
- NHS: `#maincontent`, `.nhsuk-grid-column-two-thirds`, `main`, `article`
- Health Canada / PHAC: `main`, `.mwsgeneric-base-html`, `#wb-main-in`, `#wb-cont`
- Mayo: `main`, `article`, `.article-body`
- Stanford: `[role="main"]`, `#PageContent_C001_Col00`, `main`, `article`

Use `noiseSelectors` to strip nav, share, alerts, sidebars, and page-tools.

### 8. Relax thresholds where needed

Global defaults in the current deep-search pass are intentionally looser than the earlier strict pass:

- `minContentLength: 150`
- `minParagraphs: 1`
- `maxContentLength: 200000`

Per-page or per-source overrides are allowed when:

- the page is valid but short
- the site has long government guidance pages
- the page is a known clinical leaf page with thin markup

### 9. Fix failures with page-level rules, not by giving up on the site

When a page or URL family repeatedly fails, add `pageRules`.

Use `pageRules` for:

- `exclude: true` on soft-404 pages, index shells, or fake content pages
- `forcePuppeteer: false` on pages that break under browser rendering
- extraction overrides such as lower `minContentLength`
- per-page request headers or timeouts

This is how the current pass handled:

- AAP soft-404 pages
- old CDC Ebola URL
- NHS `height-weight-and-reviews`
- Stanford high-risk newborn hub page
- Mayo generic expert-answer page

### 10. Dedupe twice before insert

The crawler currently dedupes by:

1. URL match inside the stored `license` field
2. website-aware title dedupe

Implication:

- same website + same title stays blocked
- different websites with the same title are allowed
- when the same title is allowed from a different website, the slug gets a website suffix such as `-cdc-gov` or `-stanfordchildrens-org`
- repeated runs can safely continue chewing through current-site inventory

### 11. Save both database record and local snapshot

On successful extraction:

- insert article into `articles`
- insert citation into `citations`
- write a local JSON snapshot into `data/scraped`

This is important because the local snapshot is the easiest way to audit what was actually ingested.

## How To Write Or Tune A Source

Use this source template when adding or tightening a configured authority domain:

```js
EXAMPLE_SOURCE: {
  name: 'Example Authority',
  organization: 'Example Org',
  baseUrl: 'https://example.org',
  region: 'US',
  grade: 'A',
  priority: 'P0',
  authorityClass: 'government',
  language: 'en',
  directSeedOnly: false,
  categories: [
    '/baby/feeding/',
    '/baby/sleep/'
  ],
  directSeeds: [
    'https://example.org/baby/feeding/formula-safety'
  ],
  discoveryDepth: 1,
  discoveryMaxPages: 20,
  linkPattern: /example\.org\/baby\/.+/i,
  discoveryLinkPattern: /example\.org\/baby\/.+/i,
  extractOptions: {
    contentSelectors: ['main', 'article', '#content'],
    noiseSelectors: ['header', 'footer', '.share', '.breadcrumbs']
  },
  excludePatterns: [
    /search/i,
    /video/i
  ],
  pageRules: [
    {
      match: /site-index/i,
      exclude: true
    },
    {
      match: /known-short-valid-page/i,
      extractOptions: {
        minContentLength: 120
      }
    }
  ]
}
```

Write sources this way:

- start narrow on `linkPattern`
- use `discoveryLinkPattern` to allow only on-topic internal recursion
- prefer real leaf URLs in `directSeeds`
- add selectors before widening crawl depth
- fix repeated failures with `pageRules`

## Commands

Run a deep-search batch on the current core sites:

```bash
node /Users/cathleenlin/Desktop/code/momaiagentweb/website/nextjs-project/scripts/scrapers/global-auto-scraper.js \
  --sources US_CDC,US_MAYO_CLINIC,US_STANFORD_CHILDRENS,UK_NHS,CA_HEALTH_CANADA,CA_PHAC,GLOBAL_WHO \
  --limit 80 \
  --quick \
  --medical-only
```

Continue deep-search after a plateau by targeting the sources that just received new seeds:

```bash
node /Users/cathleenlin/Desktop/code/momaiagentweb/website/nextjs-project/scripts/scrapers/global-auto-scraper.js \
  --sources US_CDC,US_MAYO_CLINIC,US_STANFORD_CHILDRENS,CA_HEALTH_CANADA \
  --limit 120 \
  --quick \
  --medical-only
```

For anti-bot source discovery, browser-assisted Mayo search is acceptable:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
"$PWCLI" open 'https://www.mayoclinic.org/search/search-results?q=newborn%20breastfeeding%20postpartum%20infant'
```

Run one source at a time:

```bash
node /Users/cathleenlin/Desktop/code/momaiagentweb/website/nextjs-project/scripts/scrapers/global-auto-scraper.js \
  --sources UK_NHS \
  --limit 40 \
  --quick \
  --medical-only
```

Run the latest AAP/CPS/Pregnancy Birth & Baby deep-search batch:

```bash
node /Users/cathleenlin/Desktop/code/momaiagentweb/website/nextjs-project/scripts/scrapers/global-auto-scraper.js \
  --sources US_AAP,CA_CARING_FOR_KIDS,AU_PREGNANCY_BIRTH_BABY \
  --limit 180 \
  --quick \
  --medical-only
```

Run only a region:

```bash
node /Users/cathleenlin/Desktop/code/momaiagentweb/website/nextjs-project/scripts/scrapers/global-auto-scraper.js \
  --regions CA \
  --limit 50 \
  --quick \
  --medical-only
```

## Search Status Ledger

Status definitions:

- `deep-searched`: recursive current-site search has already been run and tuned
- `seed-searched`: source has been crawled earlier, but not yet exhausted through the current recursive deep-search method
- `configured-not-searched`: source exists in config, but this current deep-search cycle has not systematically covered it
- `blocked`: source is known to be blocked by environment or transport constraints

### Deep-searched in the current cycle

- `US_CDC`
- `US_MAYO_CLINIC`
- `US_STANFORD_CHILDRENS`
- `UK_NHS`
- `CA_HEALTH_CANADA`
- `CA_PHAC`
- `GLOBAL_WHO`
- `US_AAP`
- `CA_CARING_FOR_KIDS`
- `AU_PREGNANCY_BIRTH_BABY`

Branches explicitly searched in the current cycle:

- `CDC`: `breastfeeding-special-circumstances`, `infant-toddler-nutrition`, `breast-milk-preparation-and-storage`, `infant-feeding-emergencies-toolkit`
- `Health Canada`: `infant-feeding`, `infant-formula`, `supplemented-foods`, `breastfeeding surveillance`
- `Stanford`: breastfeeding, infant nutrition, high-risk newborn feeding, premature baby feeding topic pages
- `Mayo`: infant-toddler health, labor-and-delivery, postpartum, selected disease-condition pages relevant to infant or postpartum care
- `AAP/HealthyChildren`: baby formula feeding, crying/colic, premature babies, newborn care, teething/tooth care, feeding/nutrition
- `CPS/Caring for Kids`: breastfeeding, feeding first year, skin-to-skin, pacifiers, thrush, well-child visits, safe sleep
- `Pregnancy Birth & Baby`: baby feeding, bottle/formula feeding, breastfeeding, newborn care, sleep/settling, baby safety, development
- `FDA`: infant formula parent/caregiver guidance, professional safe handling, Cronobacter, homemade formula, current and historical infant formula safety investigations
- `NICHD Safe to Sleep`: reduce risk, back sleeping, tummy time, safe sleep environment, breastfeeding and safe sleep, risk factors
- `ACOG`: breastfeeding, having a baby, postpartum depression, pregnancy depression/anxiety, postpartum pain, postpartum birth control, postpartum checklist, newborn bonding
- `WomensHealth.gov`: breastfeeding, pumping/storing milk, breastfeeding at work/in public, breastfeeding special situations, weaning, postpartum recovery, postpartum depression
- `NHS Start for Life`: newborn care, safe sleep, feeding your newborn, bottle feeding, mixed feeding, breastfeeding challenges, weaning, baby mental health and bonding
- `Raising Children`: bottle-feeding equipment, giving the bottle, infant formula, mixed feeding, breastfeeding attachment, newborn sleep routines
- `Plunket`: breastfeeding, bottle feeding, formula feeding, solids, choking, food allergies, newborn sleep, understanding baby cues
- `KidsHealth`: breastfeeding, formula feeding, feeding your newborn, baby sleep, breastfeeding FAQs
- `Cleveland Clinic`: breastfeeding, infant sleep, feeding in the first year, cluster feeding, postpartum, newborn jaundice
- `WHO Europe`: breastfeeding promotion, complementary feeding, infant food policy concerns
- `HealthHub Singapore`: baby sleep, early nutrition, breastfeeding, starting solids, baby first foods
- `NICE`: postnatal care recommendations, donor milk banks, newborn jaundice, faltering growth, maternal-child nutrition
- `UNICEF`: common breastfeeding problems, breastfeeding positions, baby feeding 6-12 months, baby feeding 1-2 years, starting solid foods, SIDS
- `La Leche League International`: breastfeeding positioning, storing human milk, pumping milk, postpartum mood disorders, skin-to-skin, bottle introduction

### Recursively deep-searched in the current cycle

- `UK_NICE`
- `GLOBAL_UNICEF`
- `GLOBAL_LA_LECHE_LEAGUE`

### Blocked or constrained

- `US_USDA_FOODSAFETY`
  - current issue: `Access Denied`

## Known Search Constraints

- `FoodSafety.gov` currently blocks this environment.
- `Mayo Clinic` often needs browser-assisted extraction, but discovery should remain HTTP-first.
- `Canada.ca` pages need strong selector and noise filtering because hub pages are navigation-heavy.
- `CDC tools.cdc.gov` URLs are false-positive shells and should stay excluded.
- `HealthyChildren/AAP` page content is wrapped inside the ASP.NET form. Use `extractOptions.preserveForm: true` or the content will be removed as generic form noise.
- `Pregnancy Birth & Baby` exposes ReadSpeaker helper URLs and A-Z index letter pages. Keep `app-oc.readspeaker.com`, `/cgi-bin/rsent`, `readid=mainContentArticleText`, and `/pregnancy-and-baby-topics/[A-Z]` excluded.
- `UNICEF` child leaf pages often require browser-assisted discovery/extraction even when the section hub loads over HTTP. Prefer direct leaf seeds plus `discoveryUsePuppeteer`.
- `LLLI` historical DB rows may store trailing-slash URLs while current discovery normalizes them away. Normalize both sides before using exact-URL coverage as a KPI.
- `NICE` can expose the same recommendation page with different path casing (`Recommendations` vs `recommendations`). Expect duplicate-title collisions even after exact URL coverage improves.
- same-website duplicate-title dedupe can still hide near-duplicate pages on the same hostname; check before assuming a source is exhausted.

## Current Coverage Snapshot

Latest structured coverage report:

- script: `node scripts/scrapers/current-site-coverage-report.js --sources UK_NICE,GLOBAL_UNICEF,GLOBAL_LA_LECHE_LEAGUE --probe 4`
- report: `docs/current-site-coverage-2026-04-23.md`

As of `2026-04-23T22:06Z`:

- `UK_NICE`: discovered `9`, normalized exact-URL coverage `5`, remaining `4`, probe result `0` unique / `4` duplicate-title / `0` extraction-failed
- `GLOBAL_UNICEF`: discovered `6`, normalized exact-URL coverage `6`, remaining `0`
- `GLOBAL_LA_LECHE_LEAGUE`: discovered `106`, normalized exact-URL coverage `102`, remaining `4`, probe result `0` unique / `3` duplicate-title / `1` extraction-failed

Operational conclusion:

- `UNICEF` is currently exhausted for the curated leaf seed set
- `NICE` remaining stock is path-case / same-title duplication, not true missing clinical leaf pages
- `LLLI` is mostly already covered after URL normalization; remaining exact misses are the hub root plus a small set of alias/problem pages, not a large untouched inventory

## Global Medical Coverage Snapshot

Latest full medical-only coverage run:

- script: `node scripts/scrapers/current-site-coverage-report.js --medical-only --probe 4 --output docs/current-site-coverage-medical-2026-04-23`
- report: `docs/current-site-coverage-medical-2026-04-23.md`

As of `2026-04-23T22:45Z`:

- targets: `24` medical-authority sources
- discovered candidates: `925`
- normalized exact-URL coverage: `826/925` (`89.3%`)
- probe totals: `11` extractable unique, `32` duplicate-title, `0` extraction-failed

Priority backlog sources from the latest run:

- `US_ACOG`: `3` true missing leaves
- `NZ_PLUNKET`: `3` true missing leaves
- `CA_CARING_FOR_KIDS`: `2` true missing leaves inside `5` remaining exact URLs
- `UK_NHS`: `2` true missing leaves inside `3` remaining exact URLs
- `UK_NHS_START4LIFE`: `1` true missing leaf inside `15` remaining exact URLs

Duplicate-dominated, not true backlog in the latest run:

- `US_AAP`
- `US_CDC`
- `CA_HEALTH_CANADA`
- `UK_NICE`
- `CA_PHAC`
- `GLOBAL_WHO`
- `AU_PREGNANCY_BIRTH_BABY`
- `EU_WHO_EUROPE`
- `US_NICHD_SAFE_TO_SLEEP`
- `AU_RAISING_CHILDREN`
- `US_KIDSHEALTH`

Operational interpretation:

- next crawl effort should prioritize `ACOG`, `Plunket`, `Caring for Kids`, `NHS`, and `NHS Start4Life`
- the biggest remaining page counts are not automatically the best targets; if probe says duplicate-title, treat them as near-exhausted
- use full coverage plus probe classification before deciding whether to add more page-level rules or expand to new domains

## Current Working Rule

When the user asks to "continue deep digging" inside existing authorities:

1. do not add new domains first
2. run another current-site deep-search batch
3. inspect failures and duplicates
4. add selectors, excludes, or page-level rules
5. rerun the same domains
6. only expand the source universe after current-site yield clearly drops

## Audit Rule

If reporting coverage, always distinguish among:

- configured
- searched once
- recursively deep-searched
- blocked

Do not say a site was "searched" just because it exists in config.
