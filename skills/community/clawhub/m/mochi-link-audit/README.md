# Website Link and Content Audit

[Simplified Chinese guide](README.zh-CN.md)

Crawl a bounded same-origin site and report broken links, missing fragments, duplicate titles and image alt omissions.

## Features

Crawl a bounded same-origin site and report broken links, missing fragments, duplicate titles and image alt omissions.

Runs in the active agent workspace and saves results and reports while preserving source files.

## Usage examples

After installation, send an example to your AI with the relevant files or URLs.

```text
Check the first30 pages of my site and list broken internal links with source pages.
```

```text
Find duplicate or missing titles and images lacking alt attributes.
```

```text
Verify in-page navigation anchors and sample-check10 external links.
```

## Requirements

Python 3.10+; standard library

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-link-audit
```

Alternatively, get the ZIP on this page and place its Skill folder in the active workspace's `skills/` directory. Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
