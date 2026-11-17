---
name: optics-framework
description: Drive Android, iOS, smart TV and browser sessions with the Optics (optics-framework) MCP server, and write or fix Optics CSV/YAML test suites (test_cases, modules, elements, error_definitions). Use when automating or testing a real app UI with Optics, or when an Optics keyword name, parameter or default is uncertain.
license: Apache-2.0
homepage: https://optics-framework.org
metadata:
  openclaw:
    homepage: https://optics-framework.org
    requires:
      anyBins:
        - uv
        - optics
    install:
      - id: uv
        kind: uv
        package: "optics-framework[mcp,appium,playwright]==1.11.0"
        bins:
          - optics
        label: Install optics-framework (uv)
---

# Optics (optics-framework)

Optics is newer than your training data. Do not guess keyword names, parameters or defaults:
look them up in the docs below, or read the MCP server's `optics://keywords` resource.

## Set up in OpenClaw

This skill drives the optics-framework MCP server. Register it once (stop the Gateway first):

```bash
openclaw mcp add optics --command uvx \
  --arg=--from --arg="optics-framework[mcp,appium,playwright]==1.11.0" \
  --arg optics --arg mcp
```

If `optics` is already on your PATH (for example from the Skills UI installer), use `--command optics --arg mcp` instead.
The first start downloads the package and can take a minute or two.

## Documentation

- Docs index for agents: https://optics-framework.org/docs/llms.txt
- Keyword reference: https://optics-framework.org/docs/reference/keywords/index.md
- MCP server (tools, resources, env vars): https://optics-framework.org/docs/reference/mcp.md
- Write a suite (CSV and YAML): https://optics-framework.org/docs/create/write.md
- YAML rules: https://optics-framework.org/docs/create/yaml.md
- config.yaml: https://optics-framework.org/docs/reference/config.md
- CLI: https://optics-framework.org/docs/reference/cli.md
- Error codes: https://optics-framework.org/docs/reference/errors.md

## Drive a device or browser over MCP

1. `start_session` with `driver` (`appium`, `playwright`, `selenium` or `ble`), `url` and
   `capabilities`. Keep the returned `session_id`; every other tool needs it.
   - Web: `driver: "playwright"`, `capabilities: {"headless": false}`, then
     `launch_app` with `app_identifier: "<url>"`.
   - Mobile and TV: an Appium server must already be running (default
     `http://127.0.0.1:4723`); the device goes in the capabilities (`udid`, `deviceName`, ...).
2. Look before you act: read `optics://session/{session_id}/elements` or call
   `get_interactive_elements`, and take a `screenshot`. Read `/source` when you need XPaths.
3. Act with the keyword tools (`press_element`, `enter_text`, `swipe`, `assert_presence`, ...).
   Pass a locator (`xpath=...`, `text=...`, an id) or a label from the elements list. Prefer a
   web element's `loc` value when it has one. Do not tap by coordinates.
   `detect_and_press` is for optional taps: it succeeds even when the target never appears.
4. Look again after each action. Action keywords do not wait for a screen to load; verification
   keywords such as `assert_presence` do (30 s default).
5. `terminate_session` when done. Sessions live only inside this server process.

Every parameter value is a string. Separate several elements with `|`. A coded failure starts
with the code, e.g. `[Code.E0201]`; look it up in the error codes page.

The MCP server has no flow-control, record or replay tools. To make a run repeatable, read
`optics://project-format` and write the steps you ran as a suite.

## Write a suite

A project is `config.yaml` plus CSV or YAML files. Optics classifies each file by its contents,
not its name or folder, and resolves module and element names across all files and both formats.
Scaffold one with `optics init <name>`.

A CSV is classified by its header row:

| header | the file holds |
| --- | --- |
| `test_case,test_step` | test cases, each a list of modules run in order |
| `module_name,module_step,param_1,...` | modules, each a list of keyword steps |
| `Element_Name,Element_ID` | elements; repeat a name for fallback locators, tried in order |
| `error_code,match_string` | error definitions (CSV only, no YAML form) |

Write the headers exactly as shown, case included. A file with a wrong-case header is still
recognised but its columns are read as empty, so it loads nothing and the run fails later with
an unrelated-looking error such as an element not found.

Step rules:

- Keyword names are case-insensitive: `Press Element`, `press_element`.
- `${name}` is replaced by the element called `name`, only when it is the whole value.
- `name=value` sets a parameter by its real name (e.g. `timeout_str=20`).
- Wrap a CSV value that contains commas in double quotes.

YAML holds `Test Cases`, `Modules` and `Elements` in one file. Its traps fail quietly:

1. Section keys are exact: `Test Cases`, `Modules`, `Elements`. `test_cases:` loads nothing.
2. `Test Cases` and `Modules` are lists of single-key mappings (`- Sign In:`), not plain mappings.
3. A step is one string: keyword, then values split on spaces. Quote any value with a space:
   `Press Element "Sign in"`. Quote XPaths.

```yaml
Test Cases:
  - Shopper can sign in:
      - Sign In
Modules:
  - Sign In:
      - Launch App
      - Enter Text ${email_field} ava@example.com
      - Press Element "Sign in"
      - Assert Presence "Welcome"
Elements:
  email_field: "//*[@resource-id='com.example:id/email']"
```

## Run it

- `optics dry_run <folder>` checks the suite without a device.
- `optics execute <folder>` runs it and writes `execution_output/junit_output.xml`.
- `optics list` prints every keyword; `optics doctor` checks the environment.
