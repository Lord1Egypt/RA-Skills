# `ghst member`

Member management in Ghost.

## Usage
```bash
ghst member [options] [command]
```

## Commands
- `list [options]`: List members.
- `get [options] [id]`: Get a member by id or email.
- `create [options]`: Create a member.
- `update [options] [id]`: Update a member by id or email.
- `delete [options] <id>`: Delete a member.
- `import [options] <filePath>`: Import members from CSV.
- `export [options]`: Export members as CSV.
- `bulk [options]`: Run a bulk member operation.

## Example
```bash
ghst member list --json --limit 5
```
