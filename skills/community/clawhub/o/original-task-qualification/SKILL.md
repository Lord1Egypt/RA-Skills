---
name: original-task-qualification
description: "Qualify one public SameDayDesk original task with the included correspondence client and read that private attempt. This is not delivery, acceptance, or payment."
license: MIT
compatibility: Requires Node.js >=22 and tar. No wallet, signup, or API key. The command does not fetch an executable for describe or map. Submit and read are explicit online calls. Loopback origins are owner QA only. Any other origin is refused before connect.
metadata:
  author: neomorphic
  version: "0.2.0"
  hermes:
    tags: [original-task, correspondence, qualification, no-spend]
  openclaw:
    requires:
      bins:
        - node
        - tar
---

# Original task qualification

Use this when the caller has one public SameDayDesk original task and needs that task qualified through the included correspondence client, then read back from the same private directory. A description match does not run the task. The installed command is `scripts/cli.mjs`.

This skill does not clone the website. It does not enroll by itself. Reading a descriptor does not submit a task, spend funds, or promise delivery. Pending qualification is the ordinary submitted state. It is not delivery, acceptance, payment, or repeat use.

The supported public task is the correspondence request: objective, publicInput, usefulOutput, and friction. Spend, a paid gateway, an MCP tool call, observatory work, and hosted execution stay refusals from the included client. A source label on the task is not authentication.

## Included client

The pinned archive, its extracted source, and the discovery document ship in this folder. Describe and map run that included client. They do not fetch an executable. Describe does not contact the network. Its output is the included descriptor, not a fresh claim that a hosted file changed. Map stays offline unless the caller passes `--discovery-url`. That optional read is JSON only. A pin mismatch does not run fetched code.

Acquire reads the public descriptor JSON and compares its archive pin with the included bytes. It does not download the archive. Submit and read are explicit online actions for the correspondence API. They use the included client. `--submit` must be `yes` before a submit contacts that API.

The archive hash and byte length in [references/pins.json](references/pins.json) are the only archive this command extracts. The included copy must match that pin, and each file under `client/source` must match the archive member with the same path. A mismatch is refused before extract.

## Caller input

```sh
node scripts/cli.mjs acquire --cache CACHE
node scripts/cli.mjs describe --cache CACHE
node scripts/cli.mjs map --cache CACHE --task-file task.json
node scripts/cli.mjs submit --cache CACHE --base-url https://samedaydesk.com/api/correspondence --directory PRIVATE --task-file task.json --submit yes
node scripts/cli.mjs read --cache CACHE --directory PRIVATE
```

`--cache` is a directory outside this skill. This command creates it, or reuses it only when this command already owns that directory. An existing unrelated directory is refused and left unchanged. The cache may receive the public descriptor JSON. It does not receive the executable archive. Each command extracts the included pinned archive into a private temporary directory, runs that extract, and removes the temporary directory. A `client/` entry already in the cache is ignored. It is not executed or deleted. `PRIVATE` must also sit outside this skill. The cache and `PRIVATE` must not be the same directory, and neither may contain the other. Sibling directories are the ordinary layout. The cache does not receive `registration.secret`, `continuation.json`, or `retrieval.json`. Those stay in `PRIVATE`.

`--submit` must be the value `yes`. Without that pair the command does not register and does not post. `--pay`, `--settle`, `--sign`, `--wallet`, and `--purchase` are refused before any fetch.

`--discovery-url` may be the pinned public descriptor or the same pathname on loopback `127.0.0.1` or `localhost`. Acquire always reads a descriptor. Map reads one only when this flag is present. Describe does not. `--base-url` may be `https://samedaydesk.com/api/correspondence` or that same path on loopback. Credentialed URLs, queries, fragments, and other origins are refused before connect. Redirects are not followed.

`--timeout-ms` is 1000 through 60000. The default is 20000. `--refresh yes` does not download an executable. Acquire reads the descriptor on every run. Describe does not add a request for refresh. Map reads a descriptor only when `--discovery-url` is also present. `read` does not fetch a descriptor or an archive.

Map may receive `--directory` and `--handle`. The included client decides whether a continuation is present and whether a handle belongs to that directory. This command does not invent a handle.

## Observations

Every result is one JSON object. These keys are separate observations: `acquisition`, `encounter`, `install`, `registration`, `submission`, `disposition`, `delivery`, `acceptance`, `payment`, and `repeatUse`. Null means this command did not observe that stage. It does not mean the stage succeeded.

`acquisition.source` is `included` when this command verified the bundled archive. `acquisition.fetched` stays false because the client bytes are not downloaded. `acquisition.matched` is true only after those bytes match the pin. `encounter.descriptorUrl` is null for an offline describe or map. It is set only when this command read a descriptor JSON document.

`install` here means this command extracted the included pinned archive for that invocation and ran that extract. Installing this skill into Hermes or ClawHub is a different observation and is not implied by that field. `registration` is `present` or `absent`. The command does not print the registration id or the registration file. A later `read` from the same private directory sets `repeatUse` to local continuation retrieval. That is not acceptance, a new submission, or customer demand.

Exit 0 is a classified result. Read `result.action` and `disposition`. A refusal decision is still exit 0. Exit 1 means the descriptor was unavailable, the included archive or source did not match, confirmation or the runtime was missing, the origin was refused, or the included client failed.

Owner QA fixtures are not demand. They are not acceptance and they are not payment.

## Install

This document does not claim that a public index already lists the skill. Directory install uses this folder. The Hermes path, after the package is on the default branch, is:

```sh
hermes skills install epistemedeus/samedaydesk/distribution/original-task-qualification --yes
```

Do not pass `--force` to hide a scanner finding. Root publishes to a registry. This command does not.

## Bundle files

[LICENSE](LICENSE)
[references/pins.json](references/pins.json)
[references/included-client.json](references/included-client.json)
[scripts/cli.mjs](scripts/cli.mjs)
[client/original-task-client.tar.gz](client/original-task-client.tar.gz)
[client/included-discovery.json](client/included-discovery.json)
[client/source](client/source)
