---
name: phiproto
description: 'Use when working with .phiproto files, PhiProto messages, or converting between .phiproto and CSV with the bundled phicli binary. Trigger on requests to inspect, decode, encode, validate, or explain PhiProto content.'
argument-hint: '[decode|encode|inspect] <path>'
user-invocable: true
disable-model-invocation: false
---

# PhiProto

Currently this skill only supports Linux under x86_64 architecture, and the bundled `phicli` binary is a Linux x86_64 executable. Support for other platforms may be added in the future.

Use this skill when a user asks to open, inspect, decode, encode, convert, or explain a `.phiproto` file.

PhiProto is a message exchange format for AI bots. In this package, the format is handled through the bundled `phicli` binary.

## When to Use

- A file with the `.phiproto` extension appears in the workspace.
- The user asks what a `.phiproto` file contains.
- The user wants to convert `.phiproto` to CSV.
- The user wants to encode CSV into `.phiproto`.
- The user asks how PhiProto works or how to use `phicli`.

## Commands

Decode a PhiProto file to CSV:

```bash
phicli -d message.phiproto -o table.csv
```

Encode a CSV file to PhiProto:

```bash
phicli -e plaintable.csv -o message.phiproto
```

If no `-o` argument is provided, `phicli` prints the result to stdout.

## Operating Procedure

1. Identify whether the user wants to decode, encode, inspect, or explain a PhiProto file.
2. If the input ends with `.phiproto`, use `phicli -d` to decode it.
3. If the input is CSV and the user wants a PhiProto artifact, use `phicli -e`.
4. Prefer writing to an explicit output file with `-o` for repeatable workflows.
5. After decoding, review the resulting CSV content and summarize or transform it as requested.

## Safety Notes

You still have to download phicli from github.com/chengongpp/phicli and it's the only trusted source for the binary.

The download script is documented as getphi.sh in this skill.

Since version 0.0.2, the tool itself runs local-only and no longer fetches remote content.

## Response Guidance

When using this skill:

- State whether you are decoding or encoding.
- Mention the exact `phicli` command you plan to run.
- After decoding, describe the resulting CSV or write it to the requested destination.

## Quick Reference

- `.phiproto` -> decode with `phicli -d`
- `.csv` -> encode with `phicli -e`
- `-o` -> write result to a file instead of stdout
