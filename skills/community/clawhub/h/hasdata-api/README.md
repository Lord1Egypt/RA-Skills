# hasdata — openclaw skill

Real-time web data for openclaw agents via the `hasdata` CLI. Covers Google SERP, Maps, Amazon, Zillow, Redfin, Airbnb, Yelp, Indeed, Bing, arbitrary URL scraping, and more.

## Install

```sh
clawhub install hasdata
```

The skill itself is just instructions — it shells out to the `hasdata` binary, which the agent installs on first use:

```sh
curl -sSL https://raw.githubusercontent.com/HasData/hasdata-cli/main/install.sh | sh
```

## Configure

One-time setup:

```sh
hasdata configure
```

Prompts for the API key and saves it to `~/.hasdata/config.yaml`. Every future call picks it up automatically — no env var to re-export.

Get a key from <https://hasdata.com>.

## What's in here

```
openclaw-skill/
├── SKILL.md                  # entry point — frontmatter + decision matrix + flag patterns
├── README.md                 # this file
└── references/
    ├── enrichment.md         # person + company enrichment (LinkedIn, emails, HQ, news)
    ├── search.md             # google-serp, bing-serp, news, trends, etc.
    ├── web-scraping.md       # JS scenarios, AI extraction, markdown output
    ├── real-estate.md        # zillow / redfin / airbnb (incl. bracketed filters)
    ├── ecommerce.md          # amazon / shopify
    ├── local-business.md     # maps / yelp / yellowpages
    ├── jobs.md               # indeed / glassdoor
    └── all-commands.md       # full subcommand index with credit costs
```

`SKILL.md` is loaded into the agent's context when the skill triggers; the `references/` files are progressive-disclosure — pulled in only when the agent needs deep flag info for a specific vertical.

## Source CLI

Built on top of <https://github.com/HasData/hasdata-cli>. The skill's content is hand-authored against the CLI's `--help` output; when the CLI ships new APIs, this skill should be regenerated.
