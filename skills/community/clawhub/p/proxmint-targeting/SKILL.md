---
name: proxmint-targeting
description: Build Proxmint proxy usernames for location targeting and sticky sessions. Use when the user needs exits in a specific country, state, city, ZIP code or ISP (ASN), wants to exclude countries, needs one IP held through a login or multi-step flow, or wants each worker, account or browser profile on its own IP.
---

# Proxmint targeting and sessions

Targeting rides in the proxy username, so it works in any tool that accepts a proxy login. The password never
changes. Explicit instructions from the user take priority over this skill.

## Username format

```
LOGIN__key.value;key.value
```

- `LOGIN` is the product's username. Then two underscores, then `key.value` pairs separated by semicolons.
- Several values for one key are separated by commas: `cr.us,gb`.
- In code, read the login from `PROXMINT_USERNAME` and append the targeting:
  `os.environ["PROXMINT_USERNAME"] + "__cr.us;city.newyork"`.
- In a shell, quote the whole proxy URL or username: an unquoted `;` ends the command.

## Location keys

| Key | Example | Meaning |
|---|---|---|
| `cr` | `cr.us` | Country, as a two-letter ISO code in lowercase. Several codes mean any of them: `cr.us,gb` |
| `state` | `state.california` | State or region, as its full name in lowercase with no spaces. Abbreviations such as `ca` or `us-ca` match nothing |
| `city` | `city.newyork` | City, written the same way |
| `zip` | `zip.10001` | ZIP or postal code |
| `asn` | `asn.7922` | Internet provider or mobile carrier, by AS number |
| `nocr` | `nocr.cn,ru` | Countries to leave out. Works only without `cr` |

Rules:

- Use `state`, `city`, `zip` and `asn` together with `cr`.
- Write place names in lowercase with spaces, punctuation and accents removed: São Paulo is `saopaulo`, Łódź is
  `lodz`, New York is `newyork`.
- A combination that matches no IP returns `503 NO_RAY`. Drop the narrowest key or fix the spelling.
- Don't invent location codes. When the spelling is uncertain, say so; the **Targeting** tab on the product page
  lists the live locations and writes the codes.
- State, city, ZIP and ASN targeting counts twice against the bandwidth balance on Datacenter, Residential and
  Mobile, and once on Premium Residential. Country targeting always counts once. Mention this when the user plans
  heavy city-level traffic.

## Sessions

By default every new connection gets a new IP. A session keeps one:

| Key | Example | Meaning |
|---|---|---|
| `sessid` | `sessid.job42` | Session ID: letters and digits. The same ID keeps the same IP while that IP stays online; a new ID gets a new IP |
| `sessttl` | `sessttl.30` | Minutes before the session moves to a new IP, from 1 to 120 |

- Give each worker, account or browser profile its own `sessid`.
- If a site refuses the IP a session drew, switch to a new `sessid`.
- Sticky ports from the proxy generator on the product page also hold one IP each without a `sessid`. Only the
  ports it lists work; any other answers `407 PORT_NOT_ALLOWED`. When the username has a `sessid`, the `sessid`
  decides the IP and the port doesn't matter.
- A residential IP can go offline mid-session. Code that must survive that should catch the error and continue
  with a new `sessid`.

## Saved Targeting and the username

The **Targeting** tab saves a default location for the product. It applies when the username carries no location
key, including connections from an allowlisted IP.

A location key in the username **replaces** the saved location; it doesn't add to it. With saved Targeting of
California and a username with `cr.us`, exits come from anywhere in the US. To keep a state or city, put the full
target in the username. Session keys leave the saved location alone.

## Tools that rewrite the username

Some apps cut the username at a semicolon or limit its length, and some bulk importers split each line on `;`,
`@`, `:` or spaces. If targeting seems ignored, check that the field kept the whole username. For bulk imports,
use a login with only a country (`LOGIN__cr.us` has no semicolon) together with sticky ports.

## Workflow

1. Ask for the location and session needs if they aren't clear.
2. Build the username. When the plugin's account tools are connected, start from the product's username in
   `get_account`; otherwise show it with `LOGIN` as the placeholder. Never include a password.
3. Show where it goes in the user's code or tool, reading the login from the environment.
4. For many workers, generate session IDs in code, for example `f"{login}__cr.us;sessid.w{n};sessttl.30"`.
5. Verify with an IP echo service, then a geolocation lookup. IP geolocation databases often disagree about
   residential and mobile IPs, so compare more than one before calling an exit wrong.

## Examples

```
# Any US IP, a new one per connection
LOGIN__cr.us

# New York City, one IP held for 30 minutes
LOGIN__cr.us;city.newyork;sessid.a1b2;sessttl.30

# The UK or Germany
LOGIN__cr.gb,de

# Anywhere except China and Russia
LOGIN__nocr.cn,ru

# A Comcast IP in the US
LOGIN__cr.us;asn.7922
```

## Links

- Docs: [proxmint.com/docs](https://proxmint.com/docs)
- Pricing: [proxmint.com/pricing](https://proxmint.com/pricing)
- Status: [proxmint.com/status](https://proxmint.com/status)
