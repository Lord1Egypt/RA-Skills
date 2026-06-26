# Issues

Verified against `glab 1.90.0`.

## Listing and Filtering

```bash
glab issue list --assignee=@me -O json
glab issue list --label bug
glab issue list --milestone release-2.0.0
glab issue list --search "login error"
glab issue list --group my-group --epic 123
```

`glab issue list` uses `-O json` for machine-readable output.

## Creating Issues

```bash
glab issue create -t "Bug in login" -d "Steps to reproduce" -l bug
glab issue create -t "Security issue" -l security -c
glab issue create -t "Release blocker" -m release-2.0.0 --assignee alice
glab issue create -t "Follow-up" --linked-mr 123
```

## Viewing and Updating

```bash
glab issue view 456
glab issue view 456 --comments
glab issue view 456 --output json
glab issue update 456 --title "New title"
glab issue update 456 --description "New description"
glab issue update 456 --label "bug,confirmed"
glab issue update 456 --assignee alice
glab issue update 456 --unlabel waiting
```

## Closing and Reopening

```bash
glab issue close 456
glab issue reopen 456
```

`glab issue close` does not support a comment flag. Close the issue first; if a comment is required, use the web UI or another supported issue discussion flow.

## Common Failures

### Issue Not Found

Verify that the repository context is correct before assuming the IID is wrong:

```bash
glab repo view
glab issue view 456 -R group/project
```

### Need More Precise Filtering

Use server-side filters before exporting to JSON:

```bash
glab issue list --label bug --assignee=@me -O json
glab issue list --search "timeout" --in title
```

### Need to Link Work Across Objects

- Link a new issue to a merge request with `glab issue create --linked-mr 123`
- Link a new merge request to an issue with `glab mr create --related-issue 123`
