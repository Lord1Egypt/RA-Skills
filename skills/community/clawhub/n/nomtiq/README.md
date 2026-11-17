# 小饭票 Nomtiq 🎫

**Personalized restaurant discovery for AI agents. No ads, no generic rankings.**

Nomtiq helps an agent answer “where should we eat?” with live restaurant data and a local taste profile. It supports nearby dining, date night, business meals, family gatherings, solo dining, and Chinese or English queries around the world.

## Install

OpenClaw:

```bash
openclaw skills install @oakcoderx/nomtiq --global
```

After a public GitHub source is available, Agent Skills-compatible clients can install the same skill with:

```bash
npx skills add oakcoderx/nomtiq -g
```

## Try it

Ask the agent naturally:

- `今晚想在三里屯找一家安静、适合聊天的餐厅，人均 200。`
- `北京商务请客，6 个人，需要包间和停车。`
- `Find a relaxed date-night restaurant in Tokyo, around ¥8,000 per person.`

Nomtiq returns a `2+1`: two well-supported fits and one clearly labeled exploration choice.

## Setup

Nomtiq routes by restaurant destination:

| Destination | Provider | Credential |
|---|---|---|
| Mainland China | Amap Web Service | `AMAP_WEBSERVICE_KEY` |
| Outside mainland China | Google Maps through Serper | `SERPER_API_KEY` |

Keep keys in the agent process environment or a secret manager. Never paste them into chat, source files, command arguments, or logs. Run the built-in check after installation:

```bash
python3 /path/to/nomtiq/scripts/doctor.py
```

## Privacy and trust boundary

- Restaurant queries and destinations are sent only to the selected live-search provider.
- Taste, visit feedback, and optional occasion history stay in local JSON files.
- Nomtiq core does not post reviews, monitor communities, collect promotion intelligence, send messages, book tables, place orders, or contain a shared API key.
- Authenticated HTTP calls reject redirects; provider text is treated as untrusted data.
- Users can export or reset the local profile at any time.

See [SKILL.md](SKILL.md) for activation and workflow instructions and [AGENT_GUIDE.md](AGENT_GUIDE.md) for the detailed agent operating guide.

## Why it exists

**一顿饭就是一段时光。 A meal is a moment.**

A friend of mine would take me to dinner along Liangma River—not the trending spots or ranked lists, just a local place worth sitting in. Two people, a table, time to talk.

Everything has to fit: the people, the mood, the budget, the neighborhood, and the food. Popularity lists do not know that. Nomtiq learns from the restaurants a user actually liked and helps find the next place that fits.

> The right fit isn't a rating. It's the time we spend together.

## License

MIT-0. ClawHub release: <https://clawhub.ai/oakcoderx/skills/nomtiq>
