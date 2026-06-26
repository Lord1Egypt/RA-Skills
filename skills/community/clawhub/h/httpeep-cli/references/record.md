<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/record.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# Record

The `record` subcommand captures traffic into a portable script file that you can replay later. This enables a record-once, replay-many workflow for regression testing: record production or staging traffic once, then replay it against new builds to verify behavior hasn't changed.

## record start

Start recording traffic. All sessions captured after this point are stored in the recording buffer.

```bash
httpeep-cli record start
```

## record stop

Stop recording and save the captured traffic to a file.

```bash
httpeep-cli record stop --output test-flow.httpeep
```

| Flag | Description |
|---|---|
| `--output <path>` / `-o <path>` | Output file path for the recording |

## record status

Check whether a recording is currently in progress.

```bash
httpeep-cli record status
```

## Typical workflow

```bash
# Start recording
httpeep-cli record start

# Run your tests or interact with your application
npm run integration-tests

# Stop and save
httpeep-cli record stop --output baseline.httpeep
```

The output file is a self-contained script that stores the full request sequence, including headers, bodies, and timing metadata. You can replay it later with:

```bash
httpeep-cli replay file baseline.httpeep
```

> **Tip:**
> Combine recording with focused host filtering in your test suite to keep script files small and fast to replay.
