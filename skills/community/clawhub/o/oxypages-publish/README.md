# oxypages-publish (OpenClaw skill)

The ClawHub skill that teaches an OpenClaw agent to publish a static site to
[OxyPages](https://oxypages.com): a 30-minute unclaimed link with no account,
or a permanent site with an `oxy_` API key.

`SKILL.md` is the whole skill - the frontmatter carries the ClawHub metadata
(`metadata.openclaw`: optional `OXYPAGES_API_KEY`, needs `curl`) and the body
is what the agent reads.

## Publish to ClawHub

```bash
# from this folder's parent
clawhub skill publish ./oxypages-publish --slug oxypages-publish --name "OxyPages Publish"
```

Publishing needs a GitHub account older than a week. Published skills are
MIT-0 on ClawHub; that is the registry's licence, not ours to change.

## Keep it honest

- Sizes and file counts are read from `GET https://api.oxypages.com/limits`
  at run time, so they cannot go stale. Hourly publish caps are deliberately
  NOT written down anywhere in the skill: they are tuned from the admin panel,
  and the `429` response states the live one. Re-check `/limits` before
  bumping `version`.
- The consent rule is the product's rule, not a nicety: a page an agent
  wrote is not a page the user asked to be public.
