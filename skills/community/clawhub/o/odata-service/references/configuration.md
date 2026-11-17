# One-time service configuration

OData defines how to use a service after its service root is known; it does not define a universal registry or `/.well-known/odata` endpoint. Do not guess or scan for an endpoint. Resolve it from an explicit URL, a saved profile, project configuration, an existing OData link, or provider documentation.

## Profile storage

Both OData skills use the same JSON profile store. Path precedence is:

1. `--config PATH`
2. the `ODATA_SKILL_CONFIG` environment variable
3. `~/.config/odata-skill/services.json`

The file stores service roots, OData versions, and environment-variable names. It never stores token, password, API-key, or tenant-secret values. Provide those values through the named environment variables using the user's shell, OS credential facility, or secret manager.

## Configure once

Bearer token profile:

```text
python scripts/odata_config.py set production --service-root https://api.example.com/odata/ --odata-version 4.0 --bearer-env PROD_ODATA_TOKEN --default
```

API-key/custom-header profile:

```text
python scripts/odata_config.py set warehouse --service-root https://data.example.com/odata/ --header-env X-API-Key=WAREHOUSE_API_KEY
```

Basic authentication profile:

```text
python scripts/odata_config.py set legacy --service-root https://legacy.example.com/odata/ --basic-user-env LEGACY_USER --basic-password-env LEGACY_PASSWORD
```

These commands store names such as `PROD_ODATA_TOKEN`, not their values. Never put a literal credential after an `*-env` option.

Manage profiles:

```text
python scripts/odata_config.py list
python scripts/odata_config.py show production
python scripts/odata_config.py default warehouse
python scripts/odata_config.py remove legacy
```

Place `--config PATH` before the subcommand when using a non-default configuration file.

## Use profiles

With a default profile configured, omit both URL and profile:

```text
python scripts/odata_get.py metadata
python scripts/odata_request.py request --path '$metadata' --accept application/xml
```

Select another saved service explicitly:

```text
python scripts/odata_get.py get --profile warehouse --resource Products --top 20
python scripts/odata_request.py pages --profile warehouse --path Products --query '$top=20'
```

An explicit `--service-root` remains available for one-off use. Do not combine it with `--profile`.

## Agent endpoint resolution

For each task:

1. Use a profile explicitly named by the user.
2. Otherwise inspect `odata_config.py list` and use the configured default.
3. If no profile is available, check only in-scope project configuration or documentation for an explicit service root.
4. If still unresolved, ask the user for the OData service root and offer the one-time `odata_config.py set` command.
5. After resolving the root, request the service document and `$metadata`; those discover the model but cannot discover an unknown server address.

Do not silently select a non-default profile when multiple services exist. For state-changing operations, state which profile and service root will be used before execution.
