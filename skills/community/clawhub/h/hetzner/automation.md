# Automation — hcloud, Terraform, cloud-init, and the 3,600-Request Ceiling

Scope: provisioning and configuration as code against the Hetzner APIs. Terraform language mechanics themselves are a separate skill (`terraform`).

**Before generating anything**, read `iac_tool`, `os_image`, `cpu_arch` and `default_location` in `~/Clawic/data/hetzner/config.yaml`, and `conventions` for naming and labels. Generated code that ignores the user's conventions is code they will rewrite.

**Contents:** [The API Rate Ceiling](#the-api-rate-ceiling) · [hcloud CLI and Contexts](#hcloud-cli-and-contexts) · [Terraform](#terraform) · [What Forces a Re-Create](#what-forces-a-re-create) · [cloud-init](#cloud-init) · [Configuration Management](#configuration-management) · [CI Runners and Deploy Tokens](#ci-runners-and-deploy-tokens) · [Drift](#drift) · [Autoscaling, and Why It Is Rare Here](#autoscaling-and-why-it-is-rare-here)

## The API Rate Ceiling

**3,600 requests per hour, per project** — one bucket shared by the CLI, Terraform, CI, monitoring exporters and anything else you write. It is the limit most automation hits first, and it appears as `429` in the middle of an apply that worked last week.

- The cost is per API call, not per resource: a plan that reads 200 resources spends 200 requests before it changes anything, and a monitoring exporter polling every 30 seconds spends 120 an hour on its own.
- Reduce it in this order: lower Terraform `-parallelism` (10 by default), split state by lifecycle so a plan reads fewer resources, cache inventory in a scheduled job rather than polling, and back off with jitter on retry.
- A loop that polls "is the server ready" every second is the classic self-inflicted `429`. Poll every 5-10 seconds, with a timeout.
- If several environments live in one project, they share the ceiling — another reason for one project per environment (SKILL.md Rule 2).

## hcloud CLI and Contexts

- The CLI stores named **contexts**, each holding one project's token. Switching context switches the entire blast radius, and every destructive command runs against whatever context is active — which is exactly how staging commands get run against production.
- Make the active context visible: show it in the shell prompt, or state it explicitly in the command rather than relying on the default.
- Prefer read-only tokens for anything that only lists. A reporting script with write access is an accident waiting for a typo (`security.md`).
- Structured output (JSON) plus label selectors is what makes the CLI scriptable: filter by `env` and `role` rather than by naming conventions in `grep`.
- Tokens for CI live in CI's secret store, never in a context file on a shared machine.

## Terraform

The `hcloud` provider covers servers, volumes, networks, subnets, routes, firewalls, load balancers, floating and primary IPs, SSH keys, placement groups, certificates and snapshots.

Practices that matter specifically here:

- **State per lifecycle**: network and long-lived data resources in one state, application servers in another. One state for everything means every plan reads every resource, which is both slow and the fastest way to the rate ceiling.
- **Protection flags in code.** `delete_protection` and `rebuild_protection` on stateful resources make `terraform destroy` fail loudly rather than succeed quietly (`servers.md`). Pair with `prevent_destroy` in the lifecycle block for anything holding data.
- **Pin the provider version.** Provider upgrades occasionally change defaults, and a surprise diff on 40 servers during an unrelated change is how outages start.
- **Remote state, locked.** Local state on one laptop is a single point of failure for the whole fleet; the state file also contains resource details you do not want in a repository.
- **Never put the token in a committed variables file.** It goes in the environment or a secret manager, referenced as a pointer in any notes (`security.md`).
- Import before rewriting: a project built by hand can be adopted resource by resource, and adopting is far cheaper than recreating.

## What Forces a Re-Create

Attributes that cannot be changed in place — knowing them before the plan runs is the difference between a reboot and an outage:

| Change | Effect |
|---|---|
| `user_data` (cloud-init) | Re-create — first-boot configuration only exists at creation |
| Image | Re-create |
| Location | Re-create |
| Architecture (x86 ↔ ARM) | Re-create; the snapshot will not boot the other way (`servers.md`) |
| Server type, disk kept | In-place, with a reboot |
| Server type, disk grown | In-place, reboot, and **irreversible** thereafter |
| Placement group membership | Re-create — a running server cannot join a placement group |
| Network attachment, firewall attachment, labels, volumes | In-place, live |

Read every plan for `# forces replacement` before applying. On a stateful server that phrase means "delete the data" unless a protection flag stops it.

## cloud-init

First-boot configuration passed as `user_data` at creation. It runs once, and it can only be set at creation — changing it later means a new server.

- Stay small and idempotent: create the deploy user, install the SSH keys, set the MTU if the image does not (`network.md`), install the configuration-management agent, and hand off. A 300-line cloud-init is a configuration-management system with no logging and no re-run.
- Debug it on the machine: cloud-init writes its logs locally and its output is the only evidence of why a boot half-worked. A server that "came up but did nothing" is nearly always a cloud-init error visible there.
- **Never put a secret in `user_data`.** It is readable from the instance metadata by any process on the machine, it is stored by the provider, and it appears in Terraform state and plan output. Fetch secrets at first boot from a secret manager the machine authenticates to, or inject them with configuration management over SSH.
- A cloud-init that finally boots a node cleanly is an artifact worth keeping: save it to `~/Clawic/data/hetzner/artifacts/cloud-init-<role>.md` with its `## Boxes` line, with every secret replaced by its pointer, so the next node is not re-derived.

## Configuration Management

- Split responsibilities cleanly: Terraform (or the CLI) creates infrastructure; Ansible or equivalent configures the operating system. Mixing them means neither is authoritative and drift becomes undetectable.
- The inventory should come from the API by label, not from a hand-maintained file — a static inventory diverges from reality the first time someone adds a server.
- Make runs idempotent and run them on a schedule, not only at provisioning. Configuration that is only applied once is configuration that decays.
- For a small fleet, cloud-init plus a short provisioning playbook is enough; reach for more when more than one person deploys (`production.md`).

## CI Runners and Deploy Tokens

- A dedicated or cloud CI runner needs a token, and it should be the most restricted one in the account: read-only if it only reports; write scoped to its own project if it provisions ephemeral environments.
- Ephemeral environments are the pattern the hourly billing actually rewards: create a server per branch, run the tests, delete it. Only make it automatic once the delete step is verified — orphaned per-branch servers are the most expensive kind of waste (`costs.md`).
- Cache aggressively on a dedicated runner (`dedicated.md`): the price per core is where the savings are, and CI is exactly the workload that tolerates a rebuild.
- Every automated create must also automate the corresponding delete and the corresponding row update, or the inventory becomes fiction.

## Drift

- **Check before change.** A plan that is not clean before your edit means you are about to codify someone's console fix as an accident. Fix the drift first, deliberately, then make the change.
- Console changes during an incident are legitimate — the mistake is not writing them back. The rule: whatever the incident changed by hand goes into code before the incident is closed.
- Recurring drift on the same resource is a signal that the code is wrong about how the resource is actually used.

**Write it down.** Provisioning that took real effort — the Terraform layout, the cloud-init, the runner setup — belongs in `~/Clawic/data/hetzner/artifacts/` with its `## Boxes` line, and the tool actually in use goes into `iac_tool` in `config.yaml` the moment the user states it. Every server that automation creates or deletes still updates `~/Clawic/data/servers/servers.md`: automation does not exempt the inventory, it just means the row changes more often.

## Autoscaling, and Why It Is Rare Here

There is no managed autoscaling group. Building one means a controller that watches a metric, calls the API to create and delete servers, registers them with the load balancer, and handles the API rate ceiling and the inventory rows.

Before building it, price the alternative honestly: a fleet sized for peak on this provider often costs less than the engineering time for elasticity, because the compute is cheap and the servers are small. Scale-to-zero for batch and per-branch environments is where scripted create/delete genuinely pays — steady web traffic usually is not.
