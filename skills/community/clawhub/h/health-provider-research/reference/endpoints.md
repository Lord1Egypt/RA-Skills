# health-provider-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**16 endpoints across 1 platform group(s).**

## Healthgrades (16)

### `healthgrades_autocomplete`

- **HTTP:** `GET /healthgrades/autocomplete`
- **What:** Get Healthgrades search suggestions. Returns dynamic provider, specialty, condition, procedure, and other suggestions for a free-text query. Group categories vary with the query and are returned as data, not accepted as a closed enum.
- **Params:** `term` (string, **required**) — Free-text provider, specialty, condition, or procedure query

### `healthgrades_facilities_filters`

- **HTTP:** `GET /healthgrades/facilities/filters`
- **What:** List Healthgrades facility search filters. Returns the sorts and filters for a Healthgrades facility search: distance values and, for hospitals, every specialty rating and award value accepted by /healthgrades/facilities/search.
- **Params:** `query` (string, optional) — Optional facility name or keyword; `type` (string, **required**) — Facility type; `where` (string, **required**) — City and state, or ZIP code

### `healthgrades_facilities_search`

- **HTTP:** `GET /healthgrades/facilities/search`
- **What:** Search Healthgrades hospitals, pharmacies, group practices, and urgent care. Returns one page of Healthgrades facility search results near a location for one facility type (hospital, pharmacy, group practice, or urgent care), with name, address, phone, distance, profile URL, affiliated provider and rating counts, hospital awards, and the filters available for the search. Requests use US egress because Healthgrades restricts content by region.
- **Params:** `award` (string, optional) — Hospital award value from /healthgrades/facilities/filters (type=hospital only); `distance` (string, optional) — Search radius in miles; `page` (integer, optional) — Result page (1-500, 20 results per page); `query` (string, optional) — Optional facility name or keyword; `rating` (string, optional) — Hospital specialty-rating value from /healthgrades/facilities/filters (type=hospital only); `sort` (string, optional) — Result order; patientsatisfaction is hospital-only and group_practice supports only distance; `type` (string, **required**) — Facility type; `where` (string, **required**) — City and state, or ZIP code

### `healthgrades_facility`

- **HTTP:** `GET /healthgrades/facility`
- **What:** Get a Healthgrades pharmacy, urgent care, or group practice profile. Returns one Healthgrades pharmacy, urgent care center, or group practice profile; the type (pharmacy, urgent_care, or group_practice) is inferred from the URL. Pharmacies: opening hours, services (for example compounding, immunizations, Medicare), and nearby pharmacies. Urgent care centers: opening hours and aggregated visitor answers to amenity questions. Group practices: specialties, providers with specialty and rating, medical services offered, language services, office locations with phones and coordinates, FAQs, and nearby offices. All types include name, address, and phone. Patient-authored reviews are not returned. Requests use US egress because Healthgrades restricts content by region.
- **Params:** `url` (string, **required**) — Healthgrades pharmacy, urgent care, or group practice profile URL from /healthgrades/facilities/search

### `healthgrades_health_article`

- **HTTP:** `GET /healthgrades/health-article`
- **What:** Get a Healthgrades Health A-Z article. Returns one Healthgrades Health A-Z or drug article: headline, description, authors, medical reviewers, published and modified dates, image, the conditions the article is tagged with, and the article body as headed sections of paragraphs and lists. Works for standard, chaptered, and slideshow articles. Requests use US egress because Healthgrades restricts content by region.
- **Params:** `url` (string, **required**) — Article URL from /healthgrades/health-articles

### `healthgrades_health_articles`

- **HTTP:** `GET /healthgrades/health-articles`
- **What:** List Healthgrades Health A-Z articles in a topic. Returns one page of a Healthgrades Health A-Z topic's articles (slug, URL, and last-modified date), most recently modified first, with total and total pages. Use topic=drugs for drug articles. Use an article URL with /healthgrades/health-article.
- **Params:** `page` (integer, optional) — Page number, starting at 1; `page_size` (integer, optional) — Articles per page (1-200); `topic` (string, **required**) — Topic slug from /healthgrades/health-topics

### `healthgrades_health_topics`

- **HTTP:** `GET /healthgrades/health-topics`
- **What:** List Healthgrades Health A-Z topics. Returns every topic of Healthgrades' Health A-Z library (conditions, body systems, treatments, and wellness topics) with its article count, last-modified date, and topic hub URL where one exists, plus the drugs topic for Healthgrades' drug articles. Use a slug with /healthgrades/health-articles.
- **Params:** _none_

### `healthgrades_hospital`

- **HTTP:** `GET /healthgrades/hospital`
- **What:** Get a Healthgrades hospital profile. Returns one Healthgrades hospital profile: hospital-wide and specialty awards with years, clinical outcome ratings by service line (procedure or condition, measure, outcome rating, and 1-5 stars), patient-experience measures with national comparisons, address, and phone. Patient-authored reviews are not returned. Requests use US egress because Healthgrades restricts content by region.
- **Params:** `url` (string, **required**) — Healthgrades hospital profile URL from /healthgrades/facilities/search

### `healthgrades_hospital_award_filters`

- **HTTP:** `GET /healthgrades/hospital-awards/filters`
- **What:** List Healthgrades hospital award filters. Returns the filter values Healthgrades offers for one hospital award list: list sizes, specialty codes, Ob-Gyn award types, award years, states with recipients, and (with a state) cities with recipient counts, plus the sort options. Each group's param names the /healthgrades/hospital-awards parameter that accepts its values.
- **Params:** `award` (string, **required**) — Award list; `state` (string, optional) — State slug, to list its cities; `year` (string, optional) — Award year

### `healthgrades_hospital_awards`

- **HTTP:** `GET /healthgrades/hospital-awards`
- **What:** List Healthgrades hospital award recipients. Returns one page (20 hospitals) of a Healthgrades hospital quality award list: America's Best Hospitals (top 50, 100, or 250), Specialty Excellence (by specialty, top 50 or 100), Patient Safety Excellence, Outstanding Patient Experience, Ob-Gyn Care, or Specialty State Rankings. Filter by year, state, city, specialty, and Ob-Gyn award type; sort by name or, with latitude and longitude, by distance. Each hospital includes its profile URL (for /healthgrades/hospital), address, coordinates, phone, and every award it holds with years. Read accepted filter values from /healthgrades/hospital-awards/filters. Requests use US egress because Healthgrades restricts content by region.
- **Params:** `award` (string, **required**) — Award list; `city` (string, optional) — City slug from the filters for the state (requires state); `latitude` (number, optional) — Latitude for distance sorting; `list` (string, optional) — America's Best Hospitals list size (award=americas-best-hospitals); `list_category` (string, optional) — Specialty Excellence list size (award=specialty-excellence-americas-best-care); `longitude` (number, optional) — Longitude for distance sorting; `ob_gyn_type` (string, optional) — Ob-Gyn award (award=ob-gyn-care-excellence-awards): GYS gynecologic surgery, LAB labor and delivery, OBG obstetrics and gynecology; `page` (integer, optional) — Page number (20 hospitals per page); `sort` (string, optional) — Result order; distance requires latitude and longitude; `specialty` (string, optional) — Specialty code (award=specialty-excellence-americas-best-care or state-rankings); `state` (string, optional) — State slug from the filters; `year` (string, optional) — Award year from the filters (defaults to the latest)

### `healthgrades_locations`

- **HTTP:** `GET /healthgrades/locations`
- **What:** Get Healthgrades location suggestions. Returns location autocomplete suggestions for a city, state, ZIP code, or other free-text location. Private upstream metadata and coordinates are omitted.
- **Params:** `term` (string, **required**) — City, state, or ZIP code

### `healthgrades_physician`

- **HTTP:** `GET /healthgrades/physician`
- **What:** Get a Healthgrades physician profile. Returns public professional profile fields and practice locations for one Healthgrades physician. Patient-authored review text is not returned. Requests use US egress because Healthgrades restricts some content by region.
- **Params:** `url` (string, **required**) — Canonical Healthgrades physician profile URL

### `healthgrades_physicians_filters`

- **HTTP:** `GET /healthgrades/physicians/filters`
- **What:** List Healthgrades physician search filters. Returns every filter available for a Healthgrades provider search at a location, with accepted values, labels, and result counts: insurers (with plan IDs), gender, distance, age, availability, language, patient rating, clinical focus, affiliated hospitals, practicing specialties, and affirming care. Insurer, language, clinical focus, hospital, and specialty values depend on the query and location. Each group's param names the /healthgrades/physicians/search parameter that accepts its values.
- **Params:** `query` (string, **required**) — Specialty, condition, procedure, or provider name; `where` (string, optional) — City and state, or ZIP code

### `healthgrades_physicians_search`

- **HTTP:** `GET /healthgrades/physicians/search`
- **What:** Search Healthgrades physicians. Returns one page of Healthgrades provider search results for a specialty, condition, procedure, or provider name near a location, with each provider's NPI, specialty, office, aggregate patient rating, accepted insurers, and profile URL, plus the filters available for the search. Closed-set filters accept the listed values; insurance, insurance_plan, language, clinical_focus, affiliated_hospital, and specialty accept values returned in the filters for the same query/where. List filters take comma-separated values. Requests use US egress because Healthgrades restricts content by region. Patient review text is not returned.
- **Params:** `affiliated_hospital` (string, optional) — Comma-separated hospital codes from the affiliated_hospital filter; `affirming_care` (boolean, optional) — Only providers marked LGBTQ+ affirming; `age` (string, optional) — Comma-separated provider age bands; `availability` (string, optional) — Comma-separated availability filters; `clinical_focus` (string, optional) — Comma-separated clinical focus codes from the clinical_focus filter; `distance` (string, optional) — Search radius in miles; `gender` (string, optional) — Provider gender; `insurance` (string, optional) — Comma-separated insurer codes from the insurance filter; `insurance_plan` (string, optional) — Comma-separated plan IDs from an insurer's plans (requires insurance); `language` (string, optional) — Comma-separated language codes from the language filter; `page` (integer, optional) — Result page (1-500, 20 results per page); `query` (string, **required**) — Specialty, condition, procedure, or provider name; `rating` (string, optional) — Minimum patient-satisfaction stars (5 means exactly 5); `sort` (string, optional) — Result order; `specialty` (string, optional) — Comma-separated practicing-specialty codes from the specialty filter; `where` (string, optional) — City and state, or ZIP code

### `healthgrades_specialties`

- **HTTP:** `GET /healthgrades/specialties`
- **What:** List Healthgrades physician specialties. Returns every specialty name and directory URL shown on Healthgrades' public A-Z specialty directory.
- **Params:** _none_

### `healthgrades_top_searches`

- **HTTP:** `GET /healthgrades/top-searches`
- **What:** List popular Healthgrades searches. Returns the popular specialty searches Healthgrades currently suggests, in `groups`. Each group has a category, a title such as Popular Healthcare Specialties, and suggestions with a label and value. The set changes over time and is not a fixed list.
- **Params:** _none_
