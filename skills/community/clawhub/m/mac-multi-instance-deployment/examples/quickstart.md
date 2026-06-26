# Quickstart

Use this shortest path to get a generic Mac multi-instance layout in place.

## 1. Copy the sample config

```bash
cp config/local-multi-instance.example.env /path/to/private/local-multi-instance.env
```

## 2. Edit the private copy

Update the workspace roots so they point to your own Mac paths.

## 3. Review the instance map

Read [references/instances.md](../../references/instances.md) and keep the
roles generic:

- `main`
- `workbench`
- `publish`
- `archive`
- `private`

## 4. Validate the repo

```bash
./validate_repo.sh
./generate_public_pack.sh --dry-run
```

## 5. Confirm the pack boundary

Make sure the public pack includes only public-safe files and leaves runtime
state local.

