# Meta Ads Collector Skill

## Purpose
Scans the Meta Ad Library API to find active advertisements for a given brand. Extracts the number of active ads, ad formats used, ad types, and the longest-running ad duration. This collector feeds into the Marketing Audit Pipeline to populate the Paid Ads Strategy section of the final report.

## Input Schema
```typescript
// Function signature
collectMetaAds(brandName: string, domain?: string): Promise<MetaAdsData>

// brandName: The brand name to search for in the Ad Library (e.g. "Gymshark")
// domain: Optional domain to refine search (e.g. "gymshark.com"). Used to filter
// results and improve relevance when the brand name is ambiguous.
```

## Output Schema
```typescript
interface MetaAdsData {
 activeAds: number; // Total count of currently active ads
 formatsUsed: string[]; // e.g. ["image", "video", "carousel"]
 longestRunningAdDays: number; // Days the longest-running active ad has been live
 adTypes: string[]; // e.g. ["POLITICAL_AND_ISSUE_ADS", "HOUSING_ADS", "OTHER"]
 estimatedSpend?: string; // e.g. "$10,000 - $50,000" (if available from API)
 error?: string; // Present only when collector fails
}
```

## API Dependencies
- **API Name:** Meta Ad Library API
- **Endpoint:** `https://graph.facebook.com/v19.0/ads_archive`
- **Auth:** `META_ACCESS_TOKEN` environment variable (requires a Facebook App with Ad Library API access)
- **Additional env vars:** `META_APP_ID`, `META_APP_SECRET` (used for token generation if needed)
- **Cost estimate:** Free (no per-request charge)
- **Rate limits:** Subject to Meta's standard Graph API rate limits (~200 calls/hour)

## Implementation Pattern

### Data Flow
1. Receive `brandName` and optional `domain` from the pipeline
2. Call `metaAdsService.getMetaAds(brandName, domain)` which queries the Ad Library API
3. Process the returned ads array to extract metrics
4. Map processed data to the `MetaAdsData` interface

### API Query Parameters
```typescript
{
 access_token: process.env.META_ACCESS_TOKEN,
 search_terms: brandName,
 ad_reached_countries: "['US']", // Default to US; can be expanded
 ad_active_status: "ACTIVE", // Only fetch currently active ads
 ad_type: "ALL", // Include all ad types
 fields: "id,ad_creation_time,ad_creative_bodies,ad_creative_link_captions,ad_creative_link_titles,ad_delivery_start_time,ad_snapshot_url,page_name",
 limit: 100 // Max results per page
}
```

### Metrics Calculation

**Active Ads Count:**
- Count the total number of ads returned from the API response

**Formats Detection:**
- Analyze `ad_snapshot_url` or creative fields to classify format
- Categories: `"image"`, `"video"`, `"carousel"`, `"dynamic"`, `"collection"`
- Deduplicate into a unique list

**Longest Running Ad:**
```typescript
const now = new Date();
const longestRunningAdDays = Math.max(
 ...ads.map(ad => {
 const startDate = new Date(ad.ad_delivery_start_time);
 return Math.floor((now.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
 })
);
```

**Ad Types:**
- Extract unique `ad_type` values from the response
- Common types: `"POLITICAL_AND_ISSUE_ADS"`, `"HOUSING_ADS"`, `"CREDIT_ADS"`, `"EMPLOYMENT_ADS"`, general/uncategorized

**Estimated Spend:**
- Only available for political/issue ads (Meta requirement)
- For other ad types, this field will be `undefined`
- If available, format as a range string: `"$10,000 - $50,000"`

### Domain Filtering
When `domain` is provided:
- Filter results to only include ads where the creative body, link caption, or link title references the domain
- This improves accuracy for brands with common names

## Error Handling
- Entire function wrapped in `try/catch`
- On failure, return `EMPTY_META_ADS_DATA` with `error` field set:
 ```typescript
 return { ...EMPTY_META_ADS_DATA, error: 'Meta Ads data unavailable: <reason>' };
 ```
- Never throw -- always return a valid `MetaAdsData` object
- Log errors with Winston logger including brandName and error details:
 ```typescript
 logger.error('Meta Ads collector failed', { brandName, domain, err });
 ```
- Common failure scenarios:
 - Access token invalid, expired, or lacking Ad Library permissions
 - Brand name returns zero results (not necessarily an error -- return zeroed data without error flag)
 - Rate limit exceeded (Meta Graph API throttling)
 - Network timeout

## Example Usage
```typescript
import { collectMetaAds } from '../collectors/metaAdsCollector';

// Successful collection
const data = await collectMetaAds('Gymshark', 'gymshark.com');
// Returns:
// {
// activeAds: 47,
// formatsUsed: ["image", "video", "carousel"],
// longestRunningAdDays: 182,
// adTypes: ["OTHER"],
// estimatedSpend: undefined,
// }

// No ads found (not an error)
const noAds = await collectMetaAds('TinyLocalShop');
// Returns:
// {
// activeAds: 0,
// formatsUsed: [],
// longestRunningAdDays: 0,
// adTypes: [],
// }

// Failed collection (graceful degradation)
const failedData = await collectMetaAds('Gymshark');
// Returns:
// {
// activeAds: 0,
// formatsUsed: [],
// longestRunningAdDays: 0,
// adTypes: [],
// error: "Meta Ads data unavailable: Access token expired"
// }
```

## Notes
- The collector depends on `metaAdsService.ts` for the actual API communication. The collector handles only data aggregation and metric calculation.
- Meta Ad Library API requires a Facebook App registered with Ad Library access. The app must be reviewed and approved by Meta for production use.
- The API only returns publicly available ad data. Spend data is only available for political/issue ads as mandated by Meta's transparency policies.
- Zero active ads is a valid result (small or new brands may not run Meta ads) and should be returned without an error flag.
- The `EMPTY_META_ADS_DATA` constant is defined in `src/types/audit.types.ts` and should be imported for fallback returns.
- This collector must never block the pipeline. Even a complete failure returns valid typed data with an error flag.
- Pagination: the Meta API returns a maximum of 100 results per page. For brands with many ads, pagination via the `after` cursor may be needed. For audit purposes, the first page (100 ads) is sufficient.
