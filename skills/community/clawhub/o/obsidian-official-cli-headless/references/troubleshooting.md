# Troubleshooting

## Root cause patterns

### Obsidian fails as root

Symptom:
- Electron sandbox/root errors
- startup crash when launching directly as `root`

Fix:
- run through the dedicated `obsidian` user
- do not expose raw root launch as the recommended path

### No display session

Symptom:
- headless server
- `DISPLAY` absent
- Electron starts inconsistently or crashes

Fix:
- launch through `xvfb-run -a`
- keep the wrapper command as the normal entrypoint

### Vault under `/root`

Symptom:
- CLI starts but cannot read or write the vault
- file/path errors despite correct vault location

Fix:
- allow directory traversal on `/root`
- grant ACL access on the chosen vault path
- prefer ACLs over changing ownership of the vault

### Wrong active vault

Symptom:
- commands succeed but hit the wrong vault
- `read` or `search` returns unexpected results

Fix:
- verify `obs vault`
- ensure the wrapper `cd`s into the intended vault root
- avoid juggling multiple vaults unless requested

### GPU noise on headless hosts

Symptom:
- GPU initialization warnings in output

Fix:
- keep `--disable-gpu` in the wrapper
- treat warning-only GPU messages as non-blocking if commands still work

## Known-good acceptance set

```bash
obs help
obs vault
obs daily:path
obs daily:append content="skill verification"
obs daily:read
obs search query="skill verification"
```

If these pass, the headless adaptation is usually good enough for practical use.
