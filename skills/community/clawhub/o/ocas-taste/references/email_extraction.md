# Email & Calendar Extraction

How Taste scans the user's email and calendar to extract consumption signals.

## Overview

`taste.scan` reads the user's email and Google Calendar to find transactional messages — order confirmations, reservation bookings, delivery receipts, hotel bookings — and extracts structured consumption signals from them. It handles deduplication across the confirmation/reminder/cancellation lifecycle of a single event.

## Access

- Access the user's email account (never the agent's account)
- Email subjects are often sufficient for extraction; read full body when needed for details like items ordered or total amount
- Access the user's Google Calendar for restaurant reservations and hotel bookings visible in event titles and locations

## Sender allowlist

Configured in `config.json` under `email_sources`. Each entry maps a service name to sender patterns, target domain, and source type.

```json
"email_sources": {
  "doordash": {
    "sender_patterns": ["no-reply@doordash.com", "orders@doordash.com"],
    "domain": "restaurant",
    "source_type": "purchase",
    "extraction_hints": "Restaurant name, items ordered, order total, order ID"
  },
  "instacart": {
    "sender_patterns": ["no-reply@instacart.com"],
    "domain": "product",
    "source_type": "purchase",
    "extraction_hints": "Store name, items list, quantities, total, order ID"
  },
  "good_eggs": {
    "sender_patterns": ["*@goodeggs.com"],
    "domain": "product",
    "source_type": "purchase",
    "extraction_hints": "Items ordered, producer names, total, order ID"
  },
  "tock": {
    "sender_patterns": ["*@exploretock.com"],
    "domain": "restaurant",
    "source_type": "visit",
    "extraction_hints": "Restaurant name, date/time, party size, reservation ID, experience name"
  },
  "opentable": {
    "sender_patterns": ["*@opentable.com"],
    "domain": "restaurant",
    "source_type": "visit",
    "extraction_hints": "Restaurant name, date/time, party size, confirmation number"
  },
  "yelp": {
    "sender_patterns": ["no-reply@yelp.com"],
    "domain": "restaurant",
    "source_type": "visit",
    "extraction_hints": "Restaurant name, reservation date/time, party size"
  },
  "amazon": {
    "sender_patterns": ["auto-confirm@amazon.com", "ship-confirm@amazon.com"],
    "domain": "product",
    "source_type": "purchase",
    "extraction_hints": "Product name, quantity, price, order ID"
  },
  "hotels": {
    "sender_patterns": ["*@booking.com", "*@hotels.com", "*@marriott.com", "*@hilton.com", "*@hyatt.com", "*@ihg.com", "*@airbnb.com"],
    "domain": "travel",
    "source_type": "stay",
    "extraction_hints": "Hotel name, city, check-in/check-out dates, confirmation number"
  }
}
```

The allowlist is extensible — add new services by adding entries to `email_sources` in config.json.

## Scan workflow (`taste.scan`)

1. Search the user's email for messages from senders in the allowlist
2. Search the user's Google Calendar for events with restaurant or hotel names in titles/locations
3. For each matching message or calendar event, extract structured data into an ExtractionRecord (see `schemas.md`)
4. Classify `email_type`: confirmation, reminder, update, cancellation, receipt
5. Compute `dedup_key` for each extraction
6. Run dedup pass (see below)
7. Promote non-cancelled, non-duplicate extractions to ConsumptionSignals
8. Create or update ItemRecords (increment `signal_count`, append to `visit_dates`)
9. Queue unenriched items for enrichment (see `enrichment.md`)
10. Persist all records to JSONL files
11. Write journal

## Extraction approach

Use LLM-based extraction with source-specific hints from the `extraction_hints` field. Email subjects alone are often sufficient for identifying the service, venue name, and date. Read the full email body when:
- Items ordered / specific dishes are needed
- Price/total is needed
- The subject line is ambiguous

For calendar events, extract from event title, location, and description fields.

## Deduplication

A single real-world event (e.g., a dinner reservation) may generate multiple emails: booking confirmation, reminder, update, receipt. These must be collapsed to a single signal.

### Dedup key

Composite key: `{source_service}:{order_id|confirmation_number}:{event_date}:{venue_name_normalized}`

Venue name normalization: lowercase, strip "the", collapse whitespace, remove punctuation.

### Dedup rules

1. **Exact key match**: Group extractions with identical dedup_key
2. Within a group:
   - If any extraction has `cancelled: true` → entire group is cancelled, no signal promoted
   - Otherwise, select the richest extraction (most fields populated; prefer receipts > confirmations > reminders) as canonical
   - Mark canonical as `distinct`, others as `confirmed_same`
3. **Partial key match** (same venue + similar date ±1 day, different order_id): Mark as `possible_match`. Do not auto-merge. Surface in `taste.scan.report` for review.
4. **No match**: Mark as `distinct`, promote to signal.

### Cancellation handling

Cancellation emails are detected by `email_type: cancellation` and `cancelled: true`. When a cancellation is found:
- The extraction is stored (for audit)
- All extractions in the same dedup group are excluded from signal promotion
- A DecisionRecord is written explaining the cancellation

## Frequency tracking

Each time a signal is promoted for an item that already has an ItemRecord:
- Increment `signal_count`
- Append the event date to `visit_dates[]`
- Update `last_seen`
- Frequency is a strong signal — see `strength_model.md` for how repeat visits affect strength

## Scan watermark

To avoid re-processing, `config.json` stores:

```json
"email_scan": {
  "enabled": true,
  "last_scan_timestamp": "ISO 8601 or null",
  "extraction_confidence_threshold": 0.6,
  "auto_promote_threshold": 0.8
}
```

Each scan processes messages/events newer than `last_scan_timestamp`, then updates the watermark.

## Scan report (`taste.scan.report`)

Summarizes the last scan run:
- Extractions processed (by service, by domain)
- Signals created
- Cancellations detected
- Dedup matches (confirmed_same count)
- Pending review (possible_match count)
- Items queued for enrichment
