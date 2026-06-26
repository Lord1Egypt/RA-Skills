# Marketing Orchestrator Skill

## Purpose
Orchestrates the marketing audit pipeline by sequentially running the following collector agents:
- Instagram Collector
- Meta Ads Collector
- SEO / Keyword Collector
- Competitor Finder
- Website Audit Collector

Aggregates the individual results and invokes the Report Generator skill to produce the final comprehensive marketing audit report.

## Input Schema
```typescript
interface MarketingInput {
  instagramHandle?: string;
  websiteDomain?: string;
}
```

## Output Schema
```typescript
interface MarketingAuditReport {
  reportMarkdown: string;
  rawData: any;
  error?: string;
}
```

## Implementation Pattern

- Validate input: either `instagramHandle` or `websiteDomain` is required
- Sequentially call each collector skill, passing relevant input
- Collect results in a composite data object
- Call report-generator skill with the aggregated data
- Return the final report markdown and raw data

## Example Usage

```typescript
const input = { instagramHandle: 'gymshark', websiteDomain: 'gymshark.com' };
const report = await marketingOrchestrator(input);
console.log(report.reportMarkdown);
```

## Orchestration Logic (Pseudocode)

```typescript
async function marketingOrchestrator(input: MarketingInput): Promise<MarketingAuditReport> {
  if (!input.instagramHandle && !input.websiteDomain) {
    throw new Error("Either instagramHandle or websiteDomain is required");
  }

  const auditData: any = {
    input,
    collectedAt: new Date().toISOString(),
  };

  if (input.instagramHandle) {
    auditData.instagram = await runSkill('instagram-collector', { handle: input.instagramHandle });
  }

  if (input.websiteDomain) {
    auditData.metaAds = await runSkill('meta-ads-collector', { brandName: input.websiteDomain, domain: input.websiteDomain });
    auditData.keywords = await runSkill('seo-collector', { domain: input.websiteDomain });
    auditData.competitors = await runSkill('competitor-finder', { brandName: input.websiteDomain, domain: input.websiteDomain });
    auditData.websiteAudit = await runSkill('website-audit', { domain: input.websiteDomain });
  }

  const report = await runSkill('report-generator', auditData);

  return {
    reportMarkdown: report.reportMarkdown,
    rawData: auditData,
  };
}
```

## Notes
- Each runSkill call corresponds to invoking another skill as a sub-agent or subprocess.
- The calling framework should handle API keys, env vars for external services.
- Errors in individual collectors should not block the overall orchestration.
- Extend as needed for additional collectors or data sources.
