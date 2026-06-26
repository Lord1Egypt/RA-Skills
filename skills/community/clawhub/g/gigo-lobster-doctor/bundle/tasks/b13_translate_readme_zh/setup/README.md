# jsonpeek

A small CLI to peek into deeply-nested JSON files without loading the whole tree into your editor.

## Installation

```bash
npm install -g jsonpeek
```

## Usage

```bash
jsonpeek path/to/file.json --query "users[0].profile.email"
```

### Flags

- `--query <jsonpath>` — JSONPath expression to evaluate
- `--pretty` — pretty-print the result
- `--depth <n>` — limit object expansion depth

## Why?

When working with large API responses (think GitHub Actions logs or Kubernetes events), opening the file in an editor is slow. `jsonpeek` streams the file and only materializes the slice you ask for.

## License

MIT.
