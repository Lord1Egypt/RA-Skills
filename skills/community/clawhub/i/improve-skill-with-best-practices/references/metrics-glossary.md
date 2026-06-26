# Key Metrics & Analysis Dimensions

## Six Analysis Dimensions

### 1. SEO

**Primary data source**: GSC Search Analytics

| Metric | Healthy Range | Warning Signal |
|--------|---------------|----------------|
| Average CTR | > 3% (overall) | < 1% requires immediate optimization |
| Average Position | < 20 (first two pages) | > 30 low exposure value |
| Impressions Trend | Steady growth | Sustained decline |
| Index Coverage | > 90% | < 70% structural issues |

**Diagnostic points**:
- High impressions, low CTR → Title/description needs optimization
- Keywords ranked 4-10 → Best optimization targets (push into top 3)
- Pages with declining rankings → Content needs updating or competitors overtaking

### 2. Performance

**Primary data source**: PageSpeed Insights API + agent-browser profiling

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5-4s | > 4s |
| INP (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |
| TTFB (Time to First Byte) | < 800ms | 800-1800ms | > 1800ms |

### 3. Content Strategy

**Primary data source**: GA4 top_pages + GSC search_analytics

**Diagnostic points**:
- **High-traffic low-engagement pages**: High pageViews but low engagementRate → Content quality doesn't match user expectations
- **High-ranking low-traffic pages**: Good rankings but low clicks → Title/description lacks appeal
- **Zero-traffic content**: Indexed but no impressions → Keyword strategy failure or poor content quality
- **Content decay**: Pages with sustained traffic decline → Needs updating or merging

### 4. User Experience (UX)

**Primary data source**: GA4 user_behavior + landing_pages

| Metric | Healthy Range | Warning Signal |
|--------|---------------|----------------|
| Bounce Rate | < 50% | > 70% (non-blog sites) |
| Engagement Rate | > 60% | < 40% |
| Average Session Duration | > 2 min | < 30s |
| Page Depth | > 2 | = 1 (single-page exit) |

**Diagnostic points**:
- Mobile bounce rate much higher than desktop → Poor mobile experience
- Specific pages with abnormally high bounce rate → Page content or design issues
- Very short session duration → Slow page load or irrelevant content

### 5. Conversion Rate Optimization

**Primary data source**: GA4 conversion_events + landing_pages

**Diagnostic points**:
- Large conversion rate variance across landing pages → A/B testing opportunity
- High-traffic low-conversion pages → CTA or user path issues
- Conversion funnel drop-off points → Identify where users are lost
- Cross-device conversion rate differences → Device-specific experience issues

### 6. Technical Issues

**Primary data source**: GSC URL Inspect + source code analysis + agent-browser

**Checklist**:
- [ ] robots.txt configured correctly
- [ ] sitemap.xml complete and accessible
- [ ] No 4xx/5xx error pages
- [ ] Pages have correct meta tags
- [ ] Structured data (JSON-LD) error-free
- [ ] Mobile-friendly (viewport meta)
- [ ] HTTPS configured correctly
- [ ] No mixed content warnings
- [ ] Images have alt attributes
- [ ] No broken internal links

## Priority Matrix

Classified by **Impact** x **Implementation Effort**:

| Priority | Impact | Effort | Typical Items |
|----------|--------|--------|---------------|
| P0 Critical | High | Low | Fix 4xx errors, add meta descriptions, fix indexing issues |
| P1 High | High | Medium | Optimize high-impression low-CTR pages, improve Core Web Vitals |
| P2 Medium | Medium | Medium | Content updates, landing page optimization, add structured data |
| P3 Low | Low/Medium | High | Large-scale refactoring, internationalization, new feature development |
