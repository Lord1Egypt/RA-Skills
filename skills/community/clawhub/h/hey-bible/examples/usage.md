# Example interactions

### "What does John 3:16 say?"

```bash
npx -y @hey-bible/cli search John 3 --start-verse 16 --end-verse 16 --json
```

Parse `verse.content` (strip the HTML `<sup>` tags) and present the text with the
reference "John 3:16".

### "Read me Psalm 23 in the KJV"

```bash
npx -y @hey-bible/cli bibles --json          # find the KJV's id
npx -y @hey-bible/cli search Psalms 23 --bible-id kjv --json
```

### "Pull up my favorite verses tagged 'faith'"

```bash
npx -y @hey-bible/cli favorites --tag faith --json
```

### "Show me the verse image I generated last"

```bash
npx -y @hey-bible/cli images --limit 1 --json   # get the most recent image's id
npx -y @hey-bible/cli images --id <id> --json   # fetch its signed URL
```

### Tips

- Always pass `--json` for machine-readable output.
- Quote multi-word book names: `"1 Corinthians"`, `"Song of Solomon"`.
- Omit `--start-verse`/`--end-verse` to fetch a whole chapter.
