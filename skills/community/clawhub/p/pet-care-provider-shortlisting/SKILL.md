---
name: pet-care-provider-shortlisting
description: Build pet-care or dog-training shortlists from Crawlora public Rover listings and profiles. Use to compare advertised services, starting rates, local fit, experience claims, and sampled reviews with price units, availability, badges, and safety/qualification limits preserved.
---

# Pet-care provider shortlisting

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Compare public providers against the user's pet/service needs, area, budget,
dates, and practical constraints. A listing shortlist is not a booking, safety
certification or clinical/training recommendation for an individual animal.

## Discover the correct service and verify profile identity

1. Sitter/walker search requires location and one of `overnight-boarding`,
   `overnight-traveling`, `drop-in`, `doggy-day-care`, `dog-walking`. Dog training
   uses the separate trainer-search/profile routes; it is not a sitter service
   code. Use supported `pet_type` and rate filters only where documented.
2. Resolve returned profile slugs and canonical URLs before detail. Sitter and
   trainer namespaces differ. Match location/service explicitly; a failed
   geocode does not justify using unrelated IP-derived results. Unknown or
   incomplete location evidence remains a qualification gap.
3. Preserve advertised services, price/unit, method/skill tags, experience claims,
   rating/review counts, repeat-client signals and public profile excerpts. A
   sitter can offer several separately priced services, while trainer search
   shows a session starting rate rather than a complete package price.
4. There is no date-based inventory/calendar request in these selected routes.
   The user's dates should appear as a question to confirm, not an invented
   search parameter or guaranteed vacancy. Profiles show public review excerpts,
   not every review or the provider's complete client history.

```sh
scripts/crawlora.sh /rover/search location="Seattle, WA" service_type=dog-walking pet_type=dog page=1
scripts/crawlora.sh /rover/trainer-search location="Seattle, WA"
# Follow a returned sitter/trainer slug into its matching public profile route.
```

## Compare service terms and unresolved care requirements

Preserve currency and market context; an ambiguous currency symbol does not
establish a verified conversion basis. Keep per-night, per-walk, per-visit,
per-day, per-session and package pricing
separate. Multiply only a verified unit and the user's declared quantity, marking
extras, additional pets, duration, holiday rates, taxes/fees, cancellation and
travel as unknown unless supported. A starting price is not a checkout quote.
Training methodology/credentials and years of experience are provider claims;
Star Sitter status, ratings and repeat-client counts do not independently verify
qualifications, background checks, insurance, suitability or a safe outcome.

Build a requirement matrix with supported/unclear/not-observed states, source
excerpts and questions for availability, handling needs, supervision, emergency
arrangements or requested medication assistance. Do not invent certifications,
medical competence, personal attributes, household conditions or exact residential
addresses. A need requiring professional veterinary input cannot be resolved
from a public listing alone.

Return a bounded provider shortlist with service/price basis, locality, attributed
experience/review evidence, date questions and missing criteria. Use the user's
needs rather than a universal popularity ranking. Do not message providers,
share pet/home/medical details, submit bookings, pay or alter accounts unless requested.
