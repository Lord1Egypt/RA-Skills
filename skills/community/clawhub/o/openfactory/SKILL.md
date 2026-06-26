---
name: open-factory
slug: open-factory
description: Build, test, and deploy custom Linux ISOs with OpenFactory. Create VMs, run compliance tests, manage recipes.
version: 1.0.0
author: OpenFactory
homepage: https://openfactory.tech
---

# OpenFactory Skill

Build custom Linux ISOs, deploy VMs, run compliance tests, and manage infrastructure — all through natural language.

## Connection

OpenFactory exposes an MCP (Model Context Protocol) server over SSE.

**Endpoint:** `https://build.openfactory.tech/api/mcp/sse`

**Authentication** (pick one):
- **API Key** (recommended): Generate at the OpenFactory console under Settings > MCP Keys. Pass as `api_key` parameter on every tool call, or as `Authorization: Bearer of_mcp_<key>` HTTP header.
- **Session Token**: The first tool call returns a `session_token` in its response. Pass it to all subsequent calls for session continuity.

**Session token is critical** — cloud MCP clients rotate IPs between requests. Without passing `session_token` back, each call looks like a new anonymous user.

## Tools

### Builds

| Tool | What it does |
|------|-------------|
| `list_builds(status_filter?, limit?)` | List your builds. Filter by `queued`, `building`, `built`, `failed`, `completed`. |
| `get_build(build_id)` | Get full build details including recipe, ISO path, test results. |
| `get_build_status(build_id)` | Get current status, stage, and progress percentage. |
| `create_build(recipe)` | Create a new build from a recipe (see Recipe Schema below). |
| `retry_build(build_id)` | Retry a failed build with the same recipe. |
| `get_iso_download_url(build_id)` | Get a download URL for the completed ISO. |
| `deploy_from_git(repo_url, base_image?, branch?)` | Build an ISO that auto-deploys a git repo as a service. |

### Recipes

| Tool | What it does |
|------|-------------|
| `list_recipes(category?, search?)` | Browse pre-built recipe templates. Categories: `healthcare`, `industrial`, `education`, `municipal`, `research`, `ai-development`. |
| `list_recipe_categories()` | List all available categories with descriptions. |
| `get_recipe(recipe_id)` | Get full recipe details. |
| `validate_recipe(recipe)` | Validate a recipe without starting a build. |
| `create_recipe_from_template(template_id, name, modifications)` | Fork a template and customize it. |

### Tests

| Tool | What it does |
|------|-------------|
| `run_tests(build_id, tests?, memory_mb?, vcpus?, timeout_seconds?, keep_environment?)` | Spin up a VM from the ISO and run tests. Leave `tests` empty for defaults (boot, login, packages, network + feature tests). |
| `get_test_results(run_id)` | Get test results: passed/failed assertions, screenshots, VM info. |
| `list_test_runs(build_id?, limit?)` | List test runs, optionally filtered by build. |
| `stop_test_run(run_id)` | Stop a running test and clean up VMs. |

### VMs

| Tool | What it does |
|------|-------------|
| `list_vms(build_id?)` | List running VMs, optionally filtered by build. |
| `create_vm(build_id, name?, memory_mb?, vcpus?)` | Create and boot a VM from a built ISO. |
| `start_vm(vm_name)` | Start a stopped VM. |
| `stop_vm(vm_name, force?)` | Stop a VM. `force=true` for immediate power-off. |
| `delete_vm(vm_name)` | Delete a VM and its disk. |
| `screenshot_vm(vm_name)` | Capture a PNG screenshot of the VM display. |
| `get_vm_console_url(vm_name)` | Get a VNC console URL for browser access. |

## Recipe Schema

```json
{
  "name": "My Custom Server",
  "base_image": "ubuntu-24.04",
  "description": "What this variant is for",
  "features": ["ssh", "docker", "monitoring"],
  "packages": ["curl", "htop", "vim"],
  "users": [
    {"username": "admin", "password": "changeme", "groups": ["sudo"]}
  ],
  "services": [
    {"name": "ssh", "config": {"port": 22}}
  ],
  "security": {"hardening_level": "standard"},
  "hardware": {"min_memory_gb": 4, "min_storage_gb": 32},
  "networking": {
    "dns_servers": ["8.8.8.8", "1.1.1.1"]
  }
}
```

**Supported base images:** `debian-bookworm`, `debian-trixie`, `ubuntu-24.04`, `fedora-40`, `fedora-43`, `opensuse-tumbleweed`, `elster-os`

**Common features:** `ssh`, `docker`, `desktop`, `development-tools`, `python`, `nodejs`, `monitoring`, `security-hardening`, `audit-logging`, `gxp`, `hipaa`, `ollama`, `claude-code`, `openclaw`, `nspawn-containers`, `agent-containers`

## Workflows

### Build a custom Linux ISO

```
1. create_build(recipe)          → returns build_id
2. get_build_status(build_id)    → poll until status is "built"
3. run_tests(build_id)           → returns run_id
4. get_test_results(run_id)      → check passed/failed
5. get_iso_download_url(build_id) → download the ISO
```

### Deploy a git repo as a service

```
1. deploy_from_git("https://github.com/user/app.git", base_image="ubuntu-24.04")
   → builds ISO with app auto-deployed at boot
2. get_build_status(build_id) → poll until built
3. create_vm(build_id)        → boot a VM running your app
```

### Start from a template

```
1. list_recipe_categories()
2. list_recipes(category="healthcare")
3. create_recipe_from_template("gxp-medtech-station", "My MedTech", {
     "add_features": ["monitoring"],
     "add_packages": ["prometheus-node-exporter"]
   })
4. create_build(modified_recipe)
```

### Test a build with compliance checks

```
1. run_tests(build_id, tests=["boot", "login", "network"], keep_environment=true)
2. get_test_results(run_id)
3. screenshot_vm(vm_name)  → visually verify the desktop
```

## Error Handling

- **Build failed**: Use `retry_build(build_id)` or check the recipe for issues with `validate_recipe(recipe)`.
- **Test failed**: Use `get_test_results(run_id)` to see which assertions failed and why.
- **VM won't start**: Check that the build completed successfully with `get_build_status(build_id)`.

## Rate Limits

- Builds: 1 concurrent per user (queued if busy)
- VMs: Up to 10 per user
- Tests: 1 concurrent per build
- API calls: No hard limit, be reasonable

## Examples

**"Build me an Ubuntu server with Docker and SSH"**
```json
{
  "name": "Docker Server",
  "base_image": "ubuntu-24.04",
  "features": ["ssh", "docker"],
  "users": [{"username": "admin", "password": "admin", "groups": ["sudo", "docker"]}]
}
```

**"Create a Fedora desktop with AI tools"**
```json
{
  "name": "AI Workstation",
  "base_image": "fedora-43",
  "features": ["desktop", "ssh", "python", "ollama", "claude-code"],
  "hardware": {"min_memory_gb": 16, "min_storage_gb": 64}
}
```

**"Build a GxP-compliant medical device image"**
```json
{
  "name": "MedTech Station",
  "base_image": "debian-bookworm",
  "features": ["ssh", "desktop", "gxp", "hipaa", "audit-logging", "security-hardening"],
  "security": {"hardening_level": "strict"}
}
```
