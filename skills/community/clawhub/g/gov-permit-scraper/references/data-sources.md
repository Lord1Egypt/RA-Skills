# Government Permit Data Sources

## Texas
- **TABC (Liquor):** https://www.tabc.texas.gov/public-information/new-permits-issued/
- **TDLR (Licenses):** https://www.tdlr.texas.gov/LicenseSearch/
- **SOS (Business):** https://www.sos.state.tx.us/corp/sosda/index.shtml

## California
- **ABC (Liquor):** https://www.abc.ca.gov/licensing/license-queries/
- **CSLB (Contractors):** https://www.cslb.ca.gov/onlineservices/checklicenseII/checklicense.aspx
- **SOS:** https://bizfileonline.sos.ca.gov/search/business

## Florida
- **DBPR (Business/Prof):** https://www.myfloridalicense.com/wl11.asp
- **SunBiz (Corps):** https://search.sunbiz.org/

## New York
- **SLA (Liquor):** https://www.sla.ny.gov/license-search
- **DOS (Business):** https://appext20.dos.ny.gov/corp_public/CORPSEARCH.ENTITY_SEARCH_ENTRY

## General Pattern
1. Find the state agency that issues your target permit type
2. Most have a public search or "recent permits" page
3. Scrape the HTML table or use their API if available
4. Filter by date to get only new permits
5. Enrich with email via Brave Search
6. Auto-email within 48 hours of permit issuance (freshness = response rate)
