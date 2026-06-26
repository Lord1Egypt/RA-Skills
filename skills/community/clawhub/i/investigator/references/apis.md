# API integrations

These are optional. The skill should still work in a public-only mode without them.

## HIBP
- purpose: defensive breach lookup for email addresses
- config: `HIBP_API_KEY`

## Shodan
- purpose: host and service intelligence for IPs/domains
- suggested config: `SHODAN_API_KEY`

## Google Maps / geocoding
- purpose: geocoding, place lookup, map enrichment
- suggested config: `GOOGLE_MAPS_API_KEY`

## Hunter.io / email tooling
- purpose: domain/email enrichment when legitimately needed
- suggested config: `HUNTER_API_KEY`

## Rule
These APIs should enrich a public-footprint investigation, not replace public-evidence discipline.
