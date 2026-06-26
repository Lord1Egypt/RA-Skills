---
name: local-skill
version: 0.2.0
description: "Local skill repository for publish and pre-publish inspection. Provides inspectSkill and summarizeSkill utilities."
license: MIT
author: Acme
---
# local-skill

A skill for local inspection and release workflows before publishing.

## Usage

```js
const { inspectSkill, summarizeSkill } = require('./src');

inspectSkill();    // returns { name, version, status }
summarizeSkill();  // returns a human-readable summary string
```

## Release checklist

1. `bash scripts/check.sh`
2. `bash scripts/publish.sh --dry-run`
3. Review metadata
4. `bash scripts/publish.sh`
