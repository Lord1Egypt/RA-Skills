# Nextcloud Sync

## Always Run After Changes

After creating/modifying files in Obsidian vault:

```bash
docker exec nextcloud php occ files:scan admin --path="/admin/files/Obsidian" -q
```

## Why This Is Needed

1. OpenClaw writes directly to filesystem
2. Nextcloud tracks files in database
3. `files:scan` syncs database with actual files
4. Nextcloud client on Windows sees changes

## Vault Path

```
/home/rodrigo/services/nextcloud/data/admin/files/Obsidian/
```
