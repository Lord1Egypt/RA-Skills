# Taste Schemas

## ConsumptionSignal
```json
{
  "signal_id": "string",
  "timestamp": "string — ISO 8601",
  "domain": "string — music|restaurant|book|movie|product|travel|event",
  "item": {
    "name": "string",
    "metadata": {
      "order_id": "string|null",
      "source_service": "string|null — doordash|instacart|good_eggs|tock|opentable|yelp|amazon|booking|manual|calendar",
      "items_ordered": [{"name": "string", "quantity": "number|null", "price": "number|null"}],
      "total_amount": "number|null",
      "currency": "string|null",
      "location": {"name": "string|null", "city": "string|null", "address": "string|null"},
      "party_size": "number|null",
      "event_date": "string|null — ISO 8601, when the consumption occurred"
    }
  },
  "strength": "number — 0.0 to 1.0",
  "source": "string — purchase|visit|play|watch|stay|manual|email_extraction|calendar_extraction",
  "source_extraction_id": "string|null — links back to ExtractionRecord if from email/calendar scan"
}
```

All `item.metadata` fields are optional. Manually ingested signals may have none; email-extracted signals will typically have `source_service`, `order_id`, and `event_date` at minimum.

## ExtractionRecord

Intermediate record between raw email/calendar event and final ConsumptionSignal. Stored in `extractions.jsonl`. Enables deduplication across confirmation/reminder/cancellation chains before promotion to signal.

```json
{
  "extraction_id": "string — ext_{uuid7}",
  "timestamp": "string — ISO 8601, when extraction occurred",
  "source_type": "string — email|calendar",
  "source_message_id": "string|null — message_id from email",
  "source_calendar_event_id": "string|null — calendar event ID",
  "source_service": "string — doordash|instacart|good_eggs|tock|opentable|yelp|amazon|booking|hotel|unknown",
  "email_type": "string — confirmation|reminder|update|cancellation|receipt|unknown",
  "extraction_confidence": "number — 0.0 to 1.0",
  "extracted_data": {
    "venue_or_item_name": "string",
    "domain": "string — restaurant|product|travel|event",
    "event_date": "string|null — ISO 8601",
    "order_id": "string|null",
    "confirmation_number": "string|null",
    "items": [{"name": "string", "quantity": "number|null", "price": "number|null"}],
    "total_amount": "number|null",
    "currency": "string|null",
    "location": {"name": "string|null", "city": "string|null", "address": "string|null"},
    "party_size": "number|null",
    "cancelled": "boolean — true if this email/event represents a cancellation"
  },
  "dedup_key": "string — composite key: {source_service}:{order_id|confirmation}:{event_date}:{venue_normalized}",
  "dedup_state": "string — distinct|possible_match|confirmed_same",
  "promoted_to_signal_id": "string|null — set when promoted to ConsumptionSignal"
}
```

### Dedup states

- **distinct**: No other extraction shares this dedup_key. Safe to promote.
- **possible_match**: Partial key overlap (e.g., same venue + similar date but different order_id). Preserved for manual review; never auto-merged.
- **confirmed_same**: Another extraction with the same dedup_key exists (e.g., confirmation + reminder for same reservation). Only the richest record (usually receipt or confirmation) is promoted; others marked `confirmed_same`.

### Cancellation handling

If any extraction in a dedup group has `cancelled: true`, the entire group is excluded from signal promotion. The extractions are still stored for audit.

## Recommendation
```json
{
  "item": {
    "name": "string",
    "domain": "string",
    "metadata": "object"
  },
  "confidence": "string — high|med|low",
  "because": [
    {
      "consumed_item": "string",
      "link": "string — why this connects",
      "evidence_ref": "string — signal_id"
    }
  ],
  "novelty_check": {
    "previously_visited": "boolean — must be false unless seasonal_menu_change is true",
    "seasonal_menu_change": "boolean — true only if menu change detected for seasonal venue"
  },
  "dietary_check": {
    "compatible": "boolean — must be true",
    "restrictions_verified": ["string — which restrictions were checked"]
  }
}
```

### Recommendation rules

- **Never recommend places the user has already been.** Exception: venues with highly seasonal menus where a menu change has been detected.
- **Always verify dietary compatibility.** Never recommend a venue that conflicts with the user's stated dietary restrictions or preferences (from `config.json` → `user_preferences`).
- **Novelty with guardrails.** Novel suggestions that violate dietary restrictions are worse than no suggestion.

## ItemRecord
```json
{
  "item_id": "string",
  "name": "string",
  "domain": "string",
  "metadata": {
    "source_services": ["string — which services this item was seen from"],
    "locations": [{"name": "string|null", "city": "string|null", "address": "string|null"}],
    "avg_order_value": "number|null",
    "typical_items": ["string — commonly ordered items at this venue"],
    "cuisine": ["string — e.g., japanese, italian, mexican"],
    "price_level": "number|null — 1 (budget) to 4 (fine dining)",
    "neighborhood": "string|null",
    "city": "string|null",
    "vibe": ["string — e.g., casual, romantic, lively, intimate"],
    "rating": "number|null — from Google Maps",
    "maps_place_id": "string|null",
    "hotel_class": "number|null — star rating for hotels",
    "style": ["string — e.g., boutique, resort, business"],
    "price_tier": "string|null — budget|mid|upscale|luxury",
    "category": "string|null — product category for Amazon items",
    "brand": "string|null"
  },
  "first_seen": "string — ISO 8601",
  "last_seen": "string — ISO 8601",
  "signal_count": "number",
  "visit_dates": ["string — ISO 8601, each consumption date"],
  "enriched": "boolean",
  "enriched_at": "string|null — ISO 8601"
}
```

### Enrichment

ItemRecords start with `enriched: false`. After entity enrichment (looking up venue on Google Maps, web search as backup), taste-relevant attributes are populated and `enriched` is set to `true`. Enrichment is what turns a raw venue name into a profile the recommendation engine can reason over.

**Restaurant enrichment targets:** `cuisine`, `price_level`, `neighborhood`, `city`, `vibe`, `rating`, `maps_place_id`

**Hotel enrichment targets:** `hotel_class`, `style`, `neighborhood`, `city`, `price_tier`, `rating`, `maps_place_id`

**Product enrichment targets:** `category`, `brand`, `price_tier`

## LinkRecord
```json
{
  "link_id": "string",
  "item_a_id": "string",
  "item_b_id": "string",
  "link_type": "string — same_cuisine|same_neighborhood|same_price_tier|same_style|cross_domain|manual",
  "strength": "number — 0.0 to 1.0",
  "evidence_refs": ["string — signal_ids or enrichment attributes that justify this link"]
}
```

Links are built from enriched attributes. Two restaurants sharing `cuisine: japanese` and `price_level: 3` get a link. Links drive recommendation discovery.

## ModelStatus
```json
{
  "timestamp": "string",
  "total_signals": "number",
  "total_items": "number",
  "total_enriched": "number",
  "domains_active": ["string"],
  "staleness_summary": "object",
  "top_items_by_domain": "object",
  "last_scan_timestamp": "string|null",
  "extractions_pending_review": "number"
}
```

## WeeklyReport
```json
{
  "report_id": "string",
  "period_start": "string",
  "period_end": "string",
  "new_signals": "number",
  "emerging_patterns": ["string"],
  "recommendations_generated": "number",
  "items_enriched": "number",
  "taste_profile_summary": {
    "top_cuisines": ["string"],
    "preferred_price_range": "string|null",
    "favorite_neighborhoods": ["string"],
    "frequency_highlights": ["string — e.g., 'Ordered from X 5 times this month'"]
  }
}
```
