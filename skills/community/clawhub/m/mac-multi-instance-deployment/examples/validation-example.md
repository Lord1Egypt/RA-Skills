# Validation Example

After updating the layout, run the repository checks:

```bash
./validate_repo.sh
./generate_public_pack.sh --dry-run
./generate_public_pack.sh --list
```

Check that:

- public files are included
- private runtime files are excluded
- the instance index still uses generic labels
- the pack output matches the intended layout

