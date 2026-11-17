# Failed-operation retry

The complete help fence below comes from the official, checksum-verified PlanetScale CLI v0.344.0 macOS arm64 binary with `NO_COLOR=1`, normalizing only trailing whitespace. Archive SHA-256: `1b59b271590d9b49dd52aafbb0e5c0cd788b44c00a5627d6487cd0d18815cf53`. Parent and related deployment help is in [commands.md](commands.md).

## pscale deploy-request retry

```text
Retry failed operations on a deploy request

Usage:
  pscale deploy-request retry <database> <number> [flags]

Flags:
  -h, --help   help for retry

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```
