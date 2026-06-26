<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/import.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# Import

The `import` subcommand converts traffic data from external formats into HTTPeep's internal representation. This is useful for migrating test cases, reproducing browser-captured traffic, or importing requests from other tools.

## import curl

Import a request from a cURL command string.

```bash
httpeep-cli import curl "curl -X POST https://api.example.com/users -H 'Content-Type: application/json' -d '{\"name\":\"Alice\"}'"
```

## import har

Import traffic from a HAR (HTTP Archive) file.

```bash
httpeep-cli import har ./network.har
```

## import http

Import a request from a raw HTTP message file.

```bash
httpeep-cli import http ./request.http
```

> **Warning:**
> The `import` commands are currently in development and are not reliable for automation unless you verify them first in the target CLI build. In standalone CLI mode, these commands may report that they require a running HTTPeep instance or are not yet fully implemented. Prefer `request`, `record`, or `replay` for scripted flows until an import smoke test succeeds.
