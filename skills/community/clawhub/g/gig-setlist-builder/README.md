# Gig Setlist Builder

**Problem.** Set order decides whether a live set lands. Bands sequence by
habit ("new song first?"), peak too early, stack two ballads, jump 132→96
BPM into a dance floor, then run 4 minutes over curfew. Nobody rehearses
flow — they rehearse songs.

**What it does.** `scripts/setlist_builder.py` treats your song book (key /
BPM / energy / minutes per song) as an optimization input:

- **energy arc** per set (open 7–8, first peak early, deliberate mid-set
  valley, rebuild to a 9–10 closer — the shape every road-tested act uses);
- **transition scoring**: BPM jumps >±12 % and circle-of-fifths key
  distance are penalized (relative major/minor = free smooth move);
- `must_play` guaranteed into a good slot; encore option holds back your
  best unused song;
- per-transition report flags every `HARD` seam with the reason;
- ASCII energy curve + running clock vs your slot, with ranked cut
  suggestions when you're over.

**Why broadly useful.** Millions of gigging musicians, wedding/party bands
and DJs sequence sets every weekend; "our set sags in the middle" is the
most common self-diagnosis on stage-craft forums. This turns folklore
(don't open with your best song, ladder your BPMs) into checkable
arithmetic on the actual repertoire.

**Example.**

```bash
python3 scripts/setlist_builder.py sample_songbook.json --minutes 45 --sets 2 --break-min 15
# -> 2 sets with clocks, transitions like "Am->C smooth; 132->128 BPM smooth",
#    energy arcs "[*-=:==+%#]" and an encore reserved
```

MIT license.
