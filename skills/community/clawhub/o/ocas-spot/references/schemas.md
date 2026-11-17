# Spot Schemas

## VenueRecord

Stored in `{agent_root}/commons/data/ocas-spot/venues.jsonl`. One record per venue.

```json
{
  "venue_id": "venue_{slug}",
  "name": "Human-readable venue name",
  "platform": "acuity | square | opentable | sevenrooms | resy | tock | meevo | vagaro | mindbody | fresha | styleseat | calendly | booksy | glossgenius | simplybook | boulevard | mangomint | daysmart | yelp-reservations | resdiary | eatapp | unknown",
  "booking_url": "https://...",
  "services": [
    {
      "name": "Service name",
      "service_id": "platform-specific service ID"
    }
  ],
  "platform_config": {
    "owner": "acuity owner ID (acuity only)",
    "calendar_id": "provider/staff ID (acuity only)",
    "business_id": "business location ID (square only)"
  },
  "added_at": "ISO 8601",
  "last_checked": "ISO 8601 or null"
}
```

## BookingRecord

Stored in `{agent_root}/commons/data/ocas-spot/bookings.jsonl`. One record per booking attempt.

```json
{
  "booking_id": "bk_{YYYYMMDD}_{random6}",
  "venue_id": "venue_{slug}",
  "venue_name": "Human-readable venue name",
  "service": "Service name",
  "datetime": "ISO 8601 (local timezone)",
  "status": "confirmed | pending | cancelled | failed",
  "confirmation_ref": "Platform confirmation code or null",
  "booked_at": "ISO 8601 UTC",
  "signal_emitted": true
}
```

## PlatformConfig

Embedded in VenueRecord under `platform_config`. Platform-specific fields:

### Acuity Scheduling
```json
{
  "owner": "a73e3599",
  "appointment_type_id": "66903512",
  "calendar_id": "5949533",
  "timezone": "America/Los_Angeles"
}
```

### Square Appointments
```json
{
  "booking_url": "https://app.squareup.com/appointments/book/{location_id}/start",
  "location_id": "L6SV5MCXN00CB",
  "service_ids": {
    "Peppermint Pedi": "XA4S2WKU7HYBHTWNKCPBIBDJ"
  }
}
```

### SevenRooms
```json
{
  "venue_slug": "fiorellanoe",
  "booking_url": "https://www.sevenrooms.com/explore/fiorellanoe/reservations/create/search/",
  "availability_api": "https://www.sevenrooms.com/api-yoa/availability/widget/range"
}
```

## config.json

Stored at `{agent_root}/commons/data/ocas-spot/config.json`.

```json
{
  "timezone": "America/Los_Angeles",
  "name": "<agent-name>",
  "email": "<agent-email>",
  "phone": null
}
```

## Signal formats

### Place Signal (to Elephas)

```json
{
  "signal_id": "sig_spot_place_{venue_id}_{timestamp}",
  "signal_type": "entity",
  "entity_type": "Place",
  "source_skill": "ocas-spot",
  "emitted_at": "ISO 8601 UTC",
  "data": {
    "name": "Shade Nail Spa",
    "url": "https://app.squareup.com/appointments/book/L6SV5MCXN00CB/start",
    "category": "salon"
  }
}
```

### Concept/Event Signal (to Elephas)

```json
{
  "signal_id": "sig_spot_event_{booking_id}_{timestamp}",
  "signal_type": "entity",
  "entity_type": "Concept/Event",
  "source_skill": "ocas-spot",
  "emitted_at": "ISO 8601 UTC",
  "data": {
    "event_type": "appointment",
    "venue": "Shade Nail Spa",
    "service": "Peppermint Pedi",
    "datetime": "2026-04-07T10:30:00-07:00",
    "booking_id": "bk_20260330_abc123",
    "status": "confirmed"
  }
}
```

### InsightProposal (to Vesper)

```json
{
  "proposal_id": "ip_spot_{booking_id}",
  "source_skill": "ocas-spot",
  "proposal_type": "upcoming_appointment",
  "priority": "medium",
  "emitted_at": "ISO 8601 UTC",
  "data": {
    "venue": "Shade Nail Spa",
    "service": "Peppermint Pedi",
    "datetime": "2026-04-07T10:30:00-07:00",
    "confirmation_ref": "ABC-123"
  }
}
```