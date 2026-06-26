# Command Reference

## lulu-cli list [filter]

List all firewall rules. Optionally filter by keyword (matches against key and binary path, case-insensitive).

- No sudo required
- Output: `[key]` header, then one line per rule showing UUID, action, addr, port, type, and status

**Examples:**
```bash
lulu-cli list              # all rules
lulu-cli list curl         # rules where key or path contains "curl"
lulu-cli list node         # rules for node
lulu-cli list '*'          # global/wildcard rules only
```

## lulu-cli recent [N]

Show the N most recent block rules, sorted by creation date (newest first). Default: 20.

- No sudo required
- Output: date, addr:port, type, key, UUID, and path (if different from key)
- Only shows rules with action=block

**Examples:**
```bash
lulu-cli recent            # last 20 blocks
lulu-cli recent 5          # last 5 blocks
```

## lulu-cli add

Add a new firewall rule.

**Required flags:**
- `--key KEY` - signing identity (e.g. `com.apple.curl`) or `*` for global
- `--path PATH` - full binary path or `*` for global
- `--action allow|block` - the rule action

**Optional flags:**
- `--addr ADDR` - domain, IP, or regex pattern. Default: `*` (any)
- `--port PORT` - port number or `*` for any. Default: `*`
- `--regex` - treat `--addr` value as a regular expression

**Requires sudo.** Run `reload` after.

**Examples:**
```bash
# Allow a domain for all apps
sudo lulu-cli add --key '*' --path '*' --action allow --addr example.com --port 443

# Allow domain + all subdomains via regex
sudo lulu-cli add --key '*' --path '*' --action allow \
  --addr '^(.+\.)?example\.com$' --port '*' --regex

# Allow for a specific binary only
sudo lulu-cli add --key "/usr/bin/curl" --path /usr/bin/curl \
  --action allow --addr example.com --port 443

# Block a domain
sudo lulu-cli add --key '*' --path '*' --action block --addr malicious.com --port '*'
```

## lulu-cli delete

Delete rule(s) by key.

**Required flags:**
- `--key KEY` - the rule key

**Optional flags:**
- `--uuid UUID` - delete only the rule with this UUID. If omitted, deletes ALL rules for the key.

**Requires sudo.** Run `reload` after.

**Examples:**
```bash
# Delete specific rule
sudo lulu-cli delete --key "com.apple.curl" --uuid "A1B2C3D4-..."

# Delete ALL rules for a key (careful!)
sudo lulu-cli delete --key "com.apple.curl"
```

## lulu-cli delete-match

Delete rules matching specific criteria within a key.

**Required flags:**
- `--key KEY` - the rule key

**Optional flags (at least one recommended):**
- `--action allow|block` - match by action
- `--addr ADDR` - match by address (exact match)
- `--port PORT` - match by port (exact match)

All optional flags are ANDed together.

**Requires sudo.** Run `reload` after.

**Examples:**
```bash
# Delete all block rules on port 53 for curl
sudo lulu-cli delete-match --key "com.apple.curl" --action block --port 53

# Delete all allow rules for a specific domain
sudo lulu-cli delete-match --key '*' --action allow --addr example.com
```

## lulu-cli enable

Re-enable a previously disabled rule.

**Required flags:**
- `--key KEY` - the rule key
- `--uuid UUID` - the rule UUID

**Requires sudo.** Run `reload` after.

## lulu-cli disable

Disable a rule without deleting it.

**Required flags:**
- `--key KEY` - the rule key
- `--uuid UUID` - the rule UUID

**Requires sudo.** Run `reload` after.

## lulu-cli reload

Kill the LuLu system extension process. macOS auto-restarts registered system extensions, causing it to reload rules from disk.

- ~8 second gap in filtering during restart
- **Requires sudo**
- Run after any add, delete, enable, or disable operation

## lulu-cli help

Display usage information and available commands.
