# Writing Clarity and Fact Check

[Simplified Chinese guide](README.zh-CN.md)

Flag generic wording, long sentences and repeated paragraphs; compare numeric and URL tokens after editing.

## What it does

Flag generic wording, long sentences and repeated paragraphs; compare numeric and URL tokens after editing.

## Examples

After installation, send an example with its required files or parameters.

```text
Check this draft for vague phrases and long sentences while preserving my voice.
```

```text
Compare the original and rewrite for changed numbers or links.
```

```text
Find repeated paragraphs and suggest a tighter edit.
```

## Runtime and scope

Python 3.10+, standard library only. Uses selected inputs in the current agent workspace and saves new report files.

Do not label writing as AI-generated or promise to evade detectors. Use findings as editorial hints. Verify names, quotations and meaning separately; unchanged numeric tokens are not a semantic accuracy guarantee.

## Requirements

Python 3.10+; standard library

## Installation and first use

First [connect the MochiLab Skills assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-writing-clarity
```

A free account can connect the assistant and download this free Skill. Each BOT should use its own MochiLab account. Alternatively, get the ZIP and put its Skill folder in the target workspace’s skills/ directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
