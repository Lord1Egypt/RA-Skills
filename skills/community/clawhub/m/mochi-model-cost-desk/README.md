# Model API Cost Desk

[Simplified Chinese guide](README.zh-CN.md)

Estimate model API costs from exported token usage and supplied rates, separating cached input, output and currencies.

## What it does

Estimate model API costs from exported token usage and supplied rates, separating cached input, output and currencies.

## Examples

After installation, send an example with its required files or parameters.

```text
Estimate costs from this token usage CSV and these model rates.
```

```text
Summarize USD and CNY costs separately without currency conversion.
```

```text
Compare estimated model costs against my monthly budget.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

Ask for the provider’s current rate units and whether input includes cached tokens. Save the rate date/source. Estimates are not official invoices, and do not include tool, search, storage, tax or other charges unless already represented by the supplied data.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-model-cost-desk
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
