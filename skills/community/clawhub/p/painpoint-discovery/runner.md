# Painpoint Discovery Runner

## Usage

When user triggers painpoint discovery, follow this flow:

### Step 1: Confirm Domain
```
Ask user: "Which domain would you like to explore?"
Examples: weight loss, remote work, pets, education, fitness...
```

### Step 2: Execute Web Research (Browser Mode)

Use the following search strategies:

```javascript
// Search for complaints and painpoints
browser.navigate("https://www.google.com/search?q=[domain]+problems+OR+frustration+OR+complaints+OR+issues")
browser.snapshot() → Extract titles and summaries

browser.navigate("https://www.bing.com/search?q=[domain]+painpoints+OR+struggles")
browser.snapshot() → Extract titles and summaries

// Search for existing solutions
browser.navigate("https://www.google.com/search?q=best+[domain]+tools+OR+apps+OR+software")
browser.snapshot()

// Search for market size
browser.navigate("https://www.google.com/search?q=[domain]+market+size+OR+trends+OR+statistics")
browser.snapshot()
```

### Step 3: Deep Scraping

For high-quality search results:
```javascript
browser.navigate(<Reddit/Quora/forum link>)
browser.snapshot() → Extract detailed content
```

### Step 4: Extract and Structure

From scraped content, extract:
1. Specific complaints (quote originals)
2. Problem scenarios
3. Gaps in existing solutions
4. Signals of willingness to pay

### Step 5: Generate Report

Output complete report following `example-report.md` format

---

## Quick Start Command

When user says "Find painpoints in X domain":

```
1. Confirm domain → User responds
2. Execute 3-5 browser searches (Google/Bing/Reddit)
3. Scrape 5-10 high-quality pages
4. Analyze and generate report
5. Output to user

Estimated time: 10-15 minutes (browser mode is slower)
```

---

## Quality Checklist

Before outputting report, ensure:
- [ ] Each painpoint has specific scenarios, not vague generalizations
- [ ] Has source citations (which forum/which comment)
- [ ] Distinguished real painpoints from pseudo-needs
- [ ] Solution recommendations are specific and actionable
- [ ] Business assessment has data support (or clearly marked as estimate)
- [ ] Provided next-step validation methods

---

## User Collaboration

After report output, guide user:
1. "Which of these three painpoints interests you most?"
2. "Have you experienced similar problems yourself?"
3. "Want me to deep dive into a specific painpoint?"
4. "Should we create a validation plan?"
