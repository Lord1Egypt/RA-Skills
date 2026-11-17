# Hotel Room Safeguard

**The first 15 minutes of every hotel stay, done like someone who's been
burned before.**

Two risks dominate bad rooms: bedbugs (a pregnant female rides home in
your luggage → $1,500–$5,000 extermination) and hidden cameras (found in
smoke detectors, clock radios, and charger bricks in rentals every year).
Both are detectable in minutes with eyes and a phone flashlight — if you
know the order to check and what the signatures look like.

## What It Does

`scripts/room_sweep.py`:

```bash
python3 scripts/room_sweep.py --sweep        # guided 15-minute audit
python3 scripts/room_sweep.py --hotspots     # camera risk table
python3 scripts/room_sweep.py --log --room 407 --property "Riverside Inn" \
    --finding "fecal smears on mattress piping" --photos 3
python3 scripts/room_sweep.py --letter --room 407 --property "Riverside Inn"
```

- **Bedbug sweep** in harborage-probability order (box spring > mattress
  seams > headboard > frame > nightstand > perimeter) with verdict logic:
  live bugs/eggs = leave; signs only = different room, not adjacent.
- **Camera check**: darkness lens-glint scan over risk-ranked hotspots,
  driven by line-of-sight doctrine (what can see the bed/bath?).
- **Security/valuables audit**: door hardware, exits, safe-bolted check,
  never-in-drawers rule.
- **Evidence mode**: timestamped findings log + auto-drafted escalation
  letter (room change, refund, pest-inspection proof or police reference,
  laundry credit) ready for the front desk or booking platform.

## Who Needs This

- Every traveler who books budget/high-turnover accommodation
- Frequent work travelers with luggage that goes home to a bedroom
- Families (kids' luggage on beds is how infestations start)
- Rental guests concerned about surveillance

## Example

Check-in, 22:40, tired. Luggage in the bathtub. `--sweep` on the phone:
mattress piping at the head end shows marker-dot fecal clusters. Photos,
`--log`, front desk with the `--letter` output already drafted. New room,
different floor, night comped — and your suitcase never touched the bed.

## License

MIT — see LICENSE.
