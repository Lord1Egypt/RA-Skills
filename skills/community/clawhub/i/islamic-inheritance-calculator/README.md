# Islamic Inheritance Calculator (Faraid) - Agent Skill

An offline AI agent skill that walks a user through dividing a Muslim's estate under Islamic inheritance law (Faraid / Mirath / Meeras / Wirasat / Waris), and **cites the evidence behind every rule**.

## What it does

- Interviews the user: the deceased, estate, debts, will, surviving relatives, impediments.
- Settles the estate in the correct order: funeral costs -> debts -> will (max 1/3) -> heirs.
- Computes fixed shares (1/2, 1/4, 1/8, 2/3, 1/3, 1/6), residuaries ('asabah), blocking (hajb), 'awl, radd and correction (tashih).
- Tags every ruling by source, in priority order:
  `[QURAN]` > `[SAHIH HADITH]` > `[HADITH]` > `[SAHABA]` > `[IJMA]` > `[MADHHAB]`
- Uses madhhab positions only where no direct text exists, and says so explicitly.
- Shows who does not inherit and why.

## Coverage

Spouses, children, son's children, parents, grandparents, full / paternal / maternal siblings, nephews, paternal uncles and cousins. Special cases: Umariyyatan, Mushtarakah, grandfather with siblings (both views), Akdariyyah, 'awl, radd.

Refers to a scholar for: Ja'fari rulings, missing persons, khuntha, mu'addah, distant kindred division, successive deaths (munasakhat).

## Requirements

None. No APIs, no environment variables, no scripts. Works fully offline.

## Install

**OpenClaw (ClawHub)**

```bash
clawhub install islamic-inheritance-calculator
```

**Claude Code**

```bash
cp -r islamic-inheritance-calculator ~/.claude/skills/
```

**Hermes Agent and other Agent Skills-compatible clients**
Copy the `islamic-inheritance-calculator` folder into your client's skills directory (e.g. `~/.hermes/skills/`). The skill follows the open Agent Skills (SKILL.md) standard.

## Example prompts

- "My father passed away. He left my mother, 2 sons and 1 daughter. How should his estate be divided?"
- "What share does a wife get if her husband had no children?"
- "Can my grandfather leave part of his wealth to me in his will if my father died before him?"

## Sources

Quran (4:7, 4:11, 4:12, 4:176 and related ayat), Sahih al-Bukhari, Sahih Muslim, the Sunan collections (with gradings noted), the rulings of the Companions, and the consensus of the scholars. Hadith numbering follows sunnah.com.

## Disclaimer

Educational tool, not a fatwa or legal advice. Always confirm the final distribution with a qualified scholar and check your country's inheritance laws.

## License

MIT-0 (ClawHub default).
