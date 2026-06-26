---
name: collaborative-research
description: Lucky (internet) + Jinx (analysis) collaborative research workflow. Lucky gathers raw data from web sources, Jinx analyzes and structures findings. Use for market research, competitive analysis, marketplace intelligence, API documentation review, trend analysis, pricing research, or any research requiring both web access and deep analysis. Includes market research templates for competitor/product analysis.
---

# Collaborative Research Workflow

**Core Principle:** Divide research into Lucky (data gathering) + Jinx (analysis) for maximum efficiency and parallel processing.

## When to Use This Skill

✅ **Perfect for:**
- Market research (competitor analysis, pricing)
- API documentation review 
- Trend analysis (Google Trends, marketplaces)
- Technical documentation analysis
- Large-scale content analysis
- Multi-source data comparison

❌ **Not suitable for:**
- Simple lookups (use direct web_search/web_fetch)
- Real-time data that changes quickly
- Single-page analysis (not worth the overhead)

## The 3-Phase Process

### Phase 1: Raw Data Gathering (Lucky)
**Time:** 30-60% of total project time  
**Focus:** Speed and coverage, not precision

1. **Set up data directory structure**
   ```bash
   mkdir -p /workspace/research/raw-data/YYYY-MM-DD-project
   ```

2. **Use Puppeteer for systematic data collection**
   - Navigate to target sites
   - Capture BOTH html and text: `{ html: document.body.innerHTML, text: document.body.innerText }`
   - Save with metadata: URL, timestamp, query/source
   - Don't fight DOM selectors — capture everything

3. **Save structured files for Jinx**
   ```
   METADATA:
   URL: [source_url]
   TIMESTAMP: [iso_timestamp] 
   QUERY: [search_query]
   
   RAW TEXT:
   [page_text_content]
   
   RAW HTML:
   [full_html_content]
   ```

4. **Transfer to Mac Mini SSD**
   ```bash
   scp -i ~/.ssh/lucky_to_mac file.html luckyai@100.90.7.148:~/temp/
   ssh -i ~/.ssh/lucky_to_mac luckyai@100.90.7.148 "mv ~/temp/* '/Volumes/Crucial X10/research/raw-data/project/'"
   ```

### Phase 2: Parallel Analysis (Jinx)
**Time:** 20-40% of total project time  
**Focus:** Pattern extraction and structured output

1. **Task Assignment Validation**
   - ✅ Analyzing local files (no internet needed)
   - ✅ Structured data processing
   - ✅ Text analysis and extraction

2. **Send structured analysis tasks to Jinx**
   ```bash
   curl -X POST http://localhost:3001/task -H 'Content-Type: application/json' -d '{
     "prompt": "Analyze files in /Volumes/Crucial X10/research/raw-data/project/. Extract: [specific_data_points]. Output structured JSON with [required_format]. Provide analysis summary with [specific_insights].",
     "priority": "high"
   }'
   ```

3. **Key prompting strategies for Jinx:**
   - Be specific about data extraction requirements
   - Request JSON output format
   - Ask for both raw findings AND summary analysis
   - Include comparison requirements if multiple sources

### Phase 3: Compilation & Skills Documentation (Lucky)
**Time:** 10-20% of total project time  
**Focus:** Synthesis and actionable insights

1. **Collect Jinx results**
   ```bash
   curl -s http://localhost:3001/results/[task-id]
   ```

2. **Compile comprehensive report**
   - Executive summary with key findings
   - Structured data tables/comparisons  
   - Strategic recommendations
   - Process insights and improvements

3. **Document process learnings**
   - What worked well / areas for improvement
   - Time saved vs sequential approach
   - Quality of analysis vs manual extraction

## Best Practices

### Data Gathering (Lucky)
- **Capture everything** — let Jinx filter, don't pre-filter
- **Use consistent file naming** — project-source-timestamp.html
- **Include rich metadata** — helps Jinx understand context
- **Work in batches** — send first batch to Jinx while gathering more

### Analysis Tasks (Jinx)  
- **Be specific** about extraction requirements
- **Request execution** — ask Jinx to run analysis scripts, not just provide them
- **Structure output** — JSON format for easy parsing
- **Ask for insights** — not just data extraction but pattern analysis

### Collaboration
- **Send tasks early** — don't wait for all data before starting analysis
- **Check progress regularly** — curl status API to monitor queue
- **Quality over quantity** — better to analyze fewer sources deeply

## Time Estimates

| Research Scope | Lucky Time | Jinx Time | Total Effective |
|---|---|---|---|
| Small (3-5 sources) | 20 min | 15 min | 25 min |
| Medium (5-10 sources) | 40 min | 20 min | 45 min |
| Large (10+ sources) | 60 min | 30 min | 70 min |

*Effective time = max(Lucky, Jinx) due to parallelization*

## Security Considerations

- **HTML sanitization** — Strip `<script>` tags before sending to Jinx
- **No executable content** — Only pass text/HTML data, never code
- **Local processing** — Jinx has no internet access, data stays secure
- **File permissions** — Ensure Jinx can read files on SSD

## Success Metrics

- **Speed:** 30-50% time savings vs sequential research
- **Coverage:** Ability to analyze larger datasets comprehensively  
- **Quality:** Structured, actionable insights vs raw data dumps
- **Scalability:** Process works for 5 sources or 50 sources

## Example Use Cases

1. **Market Research:** Lucky scrapes Gumroad/Etsy → Jinx extracts pricing/features
2. **API Comparison:** Lucky gathers docs → Jinx compares capabilities/pricing
3. **Trend Analysis:** Lucky gets Google Trends → Jinx identifies patterns
4. **Competitor Analysis:** Lucky browses sites → Jinx structures competitive matrix
5. **Content Analysis:** Lucky gathers articles → Jinx summarizes themes/insights

## Market Research Template

For marketplace/competitor analysis specifically, use this structured approach:

### Data Collection Checklist
For each competitor/product found:
```
## Competitor: [Name]
- Product: [Title]
- Price: $[Amount]
- Bundle Size: [X items]
- Format: [Canva/PSD/AI/etc]
- Sales Indicators: [Reviews/ratings/badges]
- Key Features: [List]
- Customer Complaints: [Common issues from reviews]
- Opportunities: [What they're missing]
```

### Market Analysis Phases
1. **Market Mapping** — Browse categories on target platforms (Gumroad, Etsy, Creative Market, Redbubble). Screenshot layouts. Document pricing patterns.
2. **Competitor Deep Dive** — Top performers, pricing intelligence, positioning, visual trends.
3. **Customer Intelligence** — Mine reviews for pain points, gaps, price sensitivity, feature requests.
4. **Trend Analysis** — Style evolution, platform preferences, niche saturation, seasonal patterns.
5. **Gap Analysis** — What customers want but can't find. Underserved niches.

### Browser Research Workflow
1. Start browser session
2. Navigate to marketplace, search category
3. Capture screenshots of results
4. Visit top competitor pages
5. Document structured data per template above
6. Save to SSD, feed to Jinx for pattern analysis

### Output Deliverables
- Structured competitor profiles
- Pricing analysis with recommendations
- Market gap identification
- Customer pain point summary
- Launch strategy recommendations

## Process Evolution

Track and improve:
- Which DOM selectors/sites work best
- Jinx prompt patterns that yield best results  
- File transfer automation opportunities
- Quality indicators for different research types

This skill creates a scalable, repeatable process for any research requiring both web access and deep analysis.