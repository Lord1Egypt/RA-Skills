# Troubleshooting

## gsheet data source with interactive OAuth

Configuring a Google Sheet data source with OAuth will require an interactive
browser based auth flow. This may not be feasible in some agent environments -
e.g. Claude Code subshells. To work around this ask the user to manually perform
the auth flow before they kick off AI agent driven calls to `plydb`. Auth
context will be cached after they finish the OAuth flow and later calls to
`plydb` by the AI agent will be authorized.

The Google Sheet auth flow can be initiated like so:

e.g.

```sh
plydb auth --config path/to/config.json
```
