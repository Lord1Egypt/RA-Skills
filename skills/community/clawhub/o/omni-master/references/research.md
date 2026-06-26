# Research & Fact-Checking Engine

Systematic information gathering, verification, and synthesis.

---

## 1. Research Protocol

### Step-by-Step Process
1. **Define the question** — What exactly do we need to know?
2. **Identify sources** — Where might this information live?
3. **Gather data** — Search, fetch, extract
4. **Evaluate quality** — Check credibility, currency, bias
5. **Synthesize** — Combine findings into coherent answer
6. **Cite sources** — Link where info came from

### Source Hierarchy (Most to Least Reliable)
1. Primary sources (original data, official docs)
2. Peer-reviewed research
3. Government/institutional reports
4. Established news organizations
5. Expert blogs/technical documentation
6. Community resources (Stack Overflow, forums)
7. Social media / unverified claims

---

## 2. Search Strategies

### Web Search (Brave API)
- Use specific keywords, not full sentences
- Add context: "python pandas merge" not "how to combine data"
- Use quotes for exact phrases: "externally managed environment"
- Use site: for specific domains: site:docs.python.org

### Fetch & Extract
- web_fetch for getting page content as markdown
- Prefer documentation sites over blog posts
- Check multiple sources for the same claim

### Code Research
```bash
# GitHub search
gh search code "function_name" --language python

# Package documentation
npm info package_name
pip show package_name
```

### Web Search
Use web_search tool for Stack Overflow-style queries and general information lookup.

---

## 3. Fact-Checking Checklist

### Verify Any Claim
- [ ] Found in 2+ independent sources?
- [ ] From a credible primary source?
- [ ] Current / not outdated?
- [ ] Not contradicted by known facts?
- [ ] Context preserved (not cherry-picked)?

### Technical Claims
- [ ] Tested/verified with actual tool?
- [ ] Matches official documentation?
- [ ] Version-specific information noted?
- [ ] Edge cases and limitations documented?

### Data Claims
- [ ] Source data available?
- [ ] Methodology reasonable?
- [ ] Sample size adequate?
- [ ] Confounding factors considered?

---

## 4. Common Research Pitfalls

### Confirmation Bias
Don't just search for evidence that supports your hypothesis.
Actively look for counter-evidence.

### Outdated Information
Software docs from 2+ years ago may be wrong.
Always check the latest version.

### Survivorship Bias
"Successful companies do X" ignores all the failed companies that also did X.

### Cherry-Picking
One study saying X doesn't mean X is true.
Look for consensus and meta-analyses.

---

## 5. Information Synthesis

### Note-Taking Structure
```
## Topic: X
### Key Findings
- Finding 1 (Source: URL)
- Finding 2 (Source: URL)

### Conflicting Information
- Source A says X, Source B says Y

### Gaps
- Couldn't verify claim Z

### Conclusion
Based on sources, most likely answer is...
```

### Synthesis Templates
- **Summary**: Key points from all sources
- **Comparison**: Side-by-side of different approaches
- **Timeline**: How understanding evolved
- **Consensus vs Dissent**: What most agree on, what's debated
