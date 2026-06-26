# Publishing Checklist

This repository is ready to publish once GitHub authentication is available.

## Preflight

```bash
git status --short --ignored
git log --format=fuller -1
git grep -n -E "(LOCAL_HOSTNAME|PRIVATE_PROJECT|PRIVATE_AUTHOR|PRIVATE_PATH)" -- . || true
./examples/minimal/qc_commands.sh
```

Expected state:

- Only `build/` should appear as ignored output.
- The latest commit should use a non-private author identity.
- The privacy scan should return no matches.
- The example should produce a DOCX, convert it to PDF, and render one page image.

## Create and Push

After `gh auth login` succeeds:

```bash
gh repo create manuscript-math-docx-qc --public --source=. --remote=origin --push \
  --description "Portable agent skill for Word/PDF-safe manuscript math, DOCX, and visual QC"
```

If the remote repository already exists:

```bash
git remote add origin git@github.com:<owner>/manuscript-math-docx-qc.git
git push -u origin main
```

Replace `<owner>` with the target GitHub account or organization.
