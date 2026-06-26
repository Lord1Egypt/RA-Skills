# Nooks 📍

> *Save places worth returning to. Find them when it matters.*

**Nooks** is an open-source skill for your agent that helps you build a personal library of places — cafes, coworking spots, libraries, restaurants, anywhere worth going back to. One markdown file per place, organized by city, fully searchable.

No app. No account. Just your agent and a folder of files.

---

## What it does

- **Saves places** — searches the web first to pre-fill what's publicly known (type, wifi, price), then asks you what it's good for and captures your personal take
- **Finds places** — "where can I focus in HK?" greps your nooks by vibe, features, and purpose
- **Logs over time** — dated notes capture how your experience of a place evolves
- **Travels with you** — files organized by city so moving between places stays clean

```
nooks/
  hk/
    blue-bottle-central.md
  sf/
    sightglass-soma.md
  sg/
    common-ground-tanjong-pagar.md
```

---

## Install

### Claude Code

```bash
mkdir -p ~/.claude/skills/nooks
curl -o ~/.claude/skills/nooks/SKILL.md https://raw.githubusercontent.com/haah-ing/nooks-skill/main/SKILL.md
```

### Other agents

```bash
npx skills add haah-ing/nooks-skill
```

Works with OpenClaw, Cursor, and any agent that supports the skills ecosystem.

---

## Then just ask

```
"Save this place — Sightglass Coffee in SoMa SF"
"Where can I focus in HK?"
"Find somewhere quiet with wifi and charging in Singapore"
"Add a note to Amber — packed on Friday evenings"
```

Each place file looks like this:

```markdown
# Sightglass Coffee

- **Type:** cafe
- **Area:** SoMa, SF
- **Maps:** https://maps.app.goo.gl/abc123
- **Price:** $$
- **Vibe:** moderate
- **Good for:** focus, casual catch-up, leisure
- **Features:** #wifi #charging #coffee #food

## Notes

4 Apr 2026: upper floor is quieter, communal tables fill fast after 10am
```

---

## Auto Maps links (optional, free)

Nooks can automatically fetch a stable Google Maps link when saving a place — no copy-pasting from your phone needed.

It uses the **Google Places API (Text Search, IDs only)**, which has no monthly cap and costs nothing.

**Setup:**

1. Go to [console.cloud.google.com](https://console.cloud.google.com) → New Project
2. Enable **Places API (New)**
3. Create an API key and restrict it to Places API (New)
4. Add a billing account (required by Google, but ID-only searches are free)
5. Create `nooks/nooksconfig.yml`:

```yaml
google_places_api_key: YOUR_KEY_HERE
```

Once set, your agent will call the API automatically and store a `place_id`-based link like:
`https://www.google.com/maps/place/?q=place_id:ChIJ...`

> `nooksconfig.yml` is excluded from git by default — your key stays local.

---

## Good for vs Notes

Two distinct layers of personal knowledge:

- **Good for** — your standing assessment of what this place suits. Updated if your opinion changes.
- **Notes** — a dated log of observations over time. What you noticed, tips, surprises.

---

## Works best with

Nooks is part of a suite of personal intelligence skills:

- [**Haah** 🪩](https://github.com/haah-ing/haah-skill) — dispatch to your trusted circles. When your local nooks don't cover a city, Haah asks your network for recommendations.
- [**Peeps** 👥](https://github.com/haah-ing/peeps-skill) — your personal network. When you save a nook from a coffee meeting, Peeps remembers who you met there.
- [**Pages** 📖](https://github.com/haah-ing/pages-skill) — your reading life. A quiet nook with good wifi is where books get read and notes get written.
- [**Vibes** 🎧](https://github.com/haah-ing/vibes-skill) — your cultural context. Some places have a sound; your agent knows both.
- [**Digs** 🔭](https://github.com/haah-ing/digs-skill) — your active research threads. A coffee meeting at a nook can turn into a finding.

Install all six and your agent knows your people, your places, your reads, your culture, and your open questions.

---

## Contributing

The skill lives in `SKILL.md` — that's the brain. Edit it, improve it, make it yours. PRs welcome.

---

## License

MIT. Take it, fork it, build on it.

---

*Designed by Ilya Belikin @ Haah Inc*