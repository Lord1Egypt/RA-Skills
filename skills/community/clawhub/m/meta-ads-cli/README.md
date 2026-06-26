# meta-ads-cli skill

A lean agent skill for using Meta's official `meta ads ...` CLI safely from a shell-capable AI agent.

## Contents

```text
SKILL.md                         Primary instructions for agents
requirements-meta-ads-cli.txt     Pinned direct CLI dependency
scripts/meta_ads_agent.py         Safety wrapper around `meta ads ...`
resources/provenance.json         Package/source metadata and wheel hashes
templates/                        Small JSON command-plan examples
evals/evals.json                  Behaviour checks for agents
```

## Quick start

```bash
python3.12 -m pip install -r requirements-meta-ads-cli.txt
export ACCESS_TOKEN=<meta-access-token>
export AD_ACCOUNT_ID=act_<ad-account-id>
python3 scripts/meta_ads_agent.py doctor
python3 scripts/meta_ads_agent.py run -- meta ads campaign list --limit 25
```

Writes require a specific approval string and, for higher-risk actions, an extra flag such as `--allow-budget`, `--allow-active`, or `--allow-destructive`.

The guard keeps persistent logging disabled unless `META_ADS_AGENT_LOG` or `--log-file` is supplied.
