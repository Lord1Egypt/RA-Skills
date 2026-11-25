# House-Sitter Handoff

**Problem.** Every trip generates the same scramble: a wall of texts about
the cat's feeding schedule, the sticky back door, which breaker is which,
and where the water main is. Written in a hurry, it's incomplete — and the
gaps surface at the worst times (pet emergency with no vet number, burst
pipe with no shutoff location, alarm code photographed into a group chat).

**What it does.** `scripts/build_brief.py` takes a structured JSON registry
of your home (template: `sample_home.json`) and:

- **audits readiness** — CRITICAL if pets lack a vet phone, no emergency
  contact exists, or a winter packet has no water-main shutoff /
  no-heating escalation; WARN for missing wifi, quirks, key location;
- **keeps secrets out of paper by default** — alarm codes are handed over
  verbally unless you explicitly opt in (`in_doc: true`), and the audit
  warns either way;
- **generates `HANDOFF.md`** ordered the way sitters actually read:
  first-30-minutes → daily routine (per pet, per plant) → house quirks →
  shutoffs → escalation playbook → contacts;
- **generates `EMERGENCY_CARD.md`** — a fridge one-pager: owner phone,
  shutoff locations, vet, poison-control line by region.

**Why broadly useful.** Pet-sitting + house-sitting is a multi-billion
informal economy; virtually every traveling household produces this
document by hand each time. A packet that's audited for the gaps that
actually cause disasters (vet, water main, heating) is cheap insurance.

**Example.**

```bash
python3 scripts/build_brief.py sample_home.json --audit-only   # gaps first
python3 scripts/build_brief.py sample_home.json --out-dir out/ # packet
# -> out/HANDOFF.md + out/EMERGENCY_CARD.md, exit 0
```

MIT license.
