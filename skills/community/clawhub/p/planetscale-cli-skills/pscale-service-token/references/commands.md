Create, list, and manage access for service tokens

Usage:
  pscale service-token [command]

Available Commands:
  add-access    add access to a service token in the organization
  create        create a service token for the organization
  delete        delete an entire service token in an organization
  delete-access delete access granted to a service token in the organization
  list          list service tokens for the organization
  show-access   fetch a service token and its accesses

Flags:
  -h, --help         help for service-token
      --org string   The organization for the current user

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale service-token [command] --help" for more information about a command.

## pscale service-token parent with show

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Create, list, and manage access for service tokens

Usage:
  pscale service-token [command]

Available Commands:
  add-access    add access to a service token in the organization
  create        create a service token for the organization
  delete        delete an entire service token in an organization
  delete-access delete access granted to a service token in the organization
  list          list service tokens for the organization
  show          show a service token in the organization
  show-access   fetch a service token and its accesses

Flags:
  -h, --help         help for service-token
      --org string   The organization for the current user

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale service-token [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale service-token show

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
show a service token in the organization

Usage:
  pscale service-token show <id> [flags]

Flags:
  -h, --help   help for show

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
