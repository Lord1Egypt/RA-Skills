# Noise Ordinances, Evidence, and Escalation — Reference

## Finding your local rules (10 minutes)

1. Search `"<your city> noise ordinance"`. Most codes live on municode.com or the city
   site under "municipal code."
2. Look for the **quiet hours** section (often "Noise; prohibited times" or
   "Nuisance noise"). Common defaults: 22:00–07:00 nightly; some cities 23:00–06:00;
   some add Sunday-morning protections.
3. Look for **decibel limits** by zone (residential is strictest; typical residential
   night limits are in the 45–55 dBA range measured at the property line).
4. Note **exemptions**: construction hours (often 07:00/08:00–18:00 weekdays only),
   emergency work, municipal services, and sometimes leaf blowers/mowers with daytime
   windows.
5. Find **who enforces**: police non-emergency line, a dedicated noise office, code
   enforcement, or the health department. The letter generator's `--to city` output is
   addressed generically — put the actual office name on the envelope.

Set the tool to match: `--night-start 23 --night-end 6` if that's your city.

## What makes noise evidence credible

**Strong (use freely):**
- Contemporaneous timestamped log — dates, start times, durations, character of the
  noise, impact. This tool's core output.
- Corroboration: household members logging independently, neighbors with their own logs.
- Your documented complaints (front-desk calls with times, letters sent, responses).
- Recordings that capture time/date metadata and audible context (indoors, normal
  volume, closed windows noted).

**Medium (use with care):**
- Phone dB apps. Uncalibrated phone microphones can be off by several dB and some
  enforcement offices dismiss them. They're fine for *relative* patterns ("inside our
  bedroom it reads 15 dB above ambient"); weak as absolute proof of a limit violation.

**Weak (avoid leading with):**
- Estimates written from memory days later.
- Recordings made at amplified volume or with the phone pressed to the shared wall.
- Characterizations ("slamming doors all night on purpose") without times/dates.

The counterintuitive truth: **a clean timestamped pattern beats a dB measurement** in
most landlord/HOA/mediation contexts, because the decision-makers care about
frequency, hours, and impact — and because your log is hard to argue with.

## Escalation ladder (try in order)

1. **Direct conversation** — many noise makers genuinely don't know they're audible.
   One calm visit, no log shown yet. Solved here more often than people expect.
2. **Written note / message** — friendly, specific ("the bass after 22:00 comes
   straight through; would you mind headphones after 10?").
3. **Landlord/HOA letter** (this tool's `letter --to landlord|hoa`) — after 2+ weeks
   of logging. Cites the pattern, requests specific action and written confirmation.
4. **Mediation** — many cities offer free community dispute mediation; both sides
   present, a neutral facilitates. Your log is your exhibit.
5. **City noise office / code enforcement / police non-emergency** during an active
   incident (they can hear it themselves — that's evidence you can't manufacture) plus
   the written complaint with your log.
6. **Constructive eviction / rent escrow / civil nuisance** — last resorts; talk to a
   tenant attorney or legal aid first. Your contemporaneous log is exactly what they
   will ask for.

## Special cases

**Barking dogs.** Log duration and time-of-day patterns for the dog; check whether
your city has a specific animal-noise ordinance (many do, with lower thresholds than
general noise codes). Defending against a complaint about your own dog: same tool,
`--note "checked on dog, was responding to delivery truck"` builds your defense log.

**Construction outside permitted hours.** Photograph the posted permit (it usually
states permitted hours), log start times, report to the permitting office — sites get
fined and supervisors care.

**Businesses/venues/HVAC.** Mechanical equipment violations are usually continuous
(dBA at property line) rather than time-of-day; a pattern of measurements at consistent
times/places matters more than incident counts. The log still organizes your record.

**Retaliation fears.** If you're a tenant worried about retaliation, complain through
the landlord (written) rather than confronting, keep every communication, and know that
many jurisdictions prohibit landlord retaliation for good-faith complaints — your
documented, polite paper trail is also your protection.

## Sound basics for better notes

- **Low frequencies (bass, thumps) penetrate structures** — this is why "music" notes
  should say "bass" when that's what you hear. High frequencies (talking, TV treble)
  attenuate through walls; persistent audible speech usually means a path (gap, vent,
  door).
- **Impact noise (footsteps, dropped objects)** transmits through the building
  structure and is governed by floor/ceiling construction — the practical fix is
  usually rugs/underlay, which is worth knowing when you get to the remedy stage.
- Duration and **sleep-stage impact** (waking you at 01:00 vs 23:00) matter to
  decision-makers more than loudness adjectives — always fill `--impact`.
