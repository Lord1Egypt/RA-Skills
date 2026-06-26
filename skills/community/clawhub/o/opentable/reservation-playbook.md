# Reservation Playbook - OpenTable

## Daily Operating Loop

1. Review upcoming 7-day demand by daypart and party size.
2. Confirm staffing and kitchen throughput assumptions.
3. Adjust availability and pacing only where evidence supports change.
4. Validate reminder and cancellation messaging for high-risk windows.
5. Log changes and expected impact in `reservation-log.md`.

## Capacity Controls

| Control | Use When | Risk if Overused |
|--------|----------|------------------|
| Slot pacing | Peaks are overloading service | Artificially low availability and missed demand |
| Party-size caps | Table mix is mismatched to demand | Unbalanced floor and guest friction |
| Lead-time windows | Prime slots fill too early | Last-minute high-value demand cannot book |
| Waitlist activation | Demand exceeds fixed inventory | Support burden if communication is slow |

## Peak Period Strategy

- Keep realistic buffer for walk-ins and service variance.
- Protect table-turn assumptions with historical averages, not wishful targets.
- Separate policy for special events instead of global hard rules.
- Prepare fallback messaging before releasing additional slots.

## No-Show Mitigation

- Use reminder cadence based on lead-time profile.
- Make cancellation terms visible before confirmation.
- Track no-show clusters by daypart and booking source.
- Pair policy changes with guest-friendly explanation.

## Weekly Review Questions

- Which window had the largest mismatch between bookings and seatable covers?
- Which change improved outcomes with least operational strain?
- Which change should be rolled back immediately?
- What must be tested next week to reduce uncertainty?
