---
name: ansible
description: >
  Generate, review, and optimize Ansible automation artifacts. Use this skill whenever
  the user mentions Ansible, playbooks, roles, inventory, tasks, handlers, Jinja2
  templates, ansible.cfg, Galaxy, AWX, or any infrastructure automation using YAML-based
  configuration management. Trigger even for vague requests like "automate server setup",
  "deploy my app with Ansible", "write a role for nginx", "create an inventory file",
  or "how do I configure hosts in Ansible". This skill covers the full lifecycle:
  generating playbooks, scaffolding roles, writing inventories, creating Jinja2 templates,
  designing variable structures, and producing CI/CD-ready Ansible project layouts.
---

# Ansible Skill

A skill for generating production-grade Ansible automation: playbooks, roles, inventories,
Jinja2 templates, variable files, and complete project structures following official
best practices.

---

## Workflow Overview

```
1. Clarify Intent        → Understand target OS, task type, scale, idempotency needs
2. Choose Output Type    → Playbook / Role / Inventory / Template / Full Project
3. Generate Artifacts    → Produce YAML files with best practices embedded
4. Validate & Annotate  → Add lint hints, --check commands, and idempotency notes
5. Deliver Structure     → Present files with clear directory paths and run instructions
```

---

## Step 1: Clarify Intent

Before generating, collect the following (infer from context when possible):

| Parameter         | Description                                      | Example                    |
|-------------------|--------------------------------------------------|----------------------------|
| `target_os`       | OS family of managed hosts                       | Ubuntu 22.04, RHEL 9       |
| `task_type`       | What to automate                                 | deploy app, manage users   |
| `connection_type` | How Ansible connects                             | SSH (default), WinRM       |
| `privilege`       | Needs sudo/become?                               | yes / no                   |
| `scale`           | Number of hosts / groups                         | 3 webservers, 1 DB         |
| `idempotency`     | Must be safe to re-run?                          | yes (always recommended)   |
| `var_source`      | Where variables come from                        | group_vars, vault, extra   |

If context is clear, skip the interview and generate directly.

---

## Step 2: Output Types

### A) Single Playbook

Use for: ad-hoc tasks, simple automation, one-off operations.

**Template:**
```yaml
---
# playbooks/<name>.yml
- name: <Descriptive play name>
  hosts: <inventory_group>
  become: true
  gather_facts: true

  vars:
    app_port: 8080
    app_user: deploy

  pre_tasks:
    - name: Ensure required packages are present
      ansible.builtin.package:
        name: "{{ item }}"
        state: present
      loop:
        - curl
        - git

  roles:
    - role: <role_name>
      when: ansible_os_family == "Debian"

  tasks:
    - name: Task description (use verb + object)
      ansible.builtin.module:
        param: value
      notify: Restart service
      tags:
        - setup
        - deploy

  handlers:
    - name: Restart service
      ansible.builtin.service:
        name: <service>
        state: restarted
```

**Rules:**
- Always use FQCN (Fully Qualified Collection Names): `ansible.builtin.copy`, not `copy`
- Use `state: present/absent` for idempotency
- Add `tags` for selective execution
- Use `notify` + handlers for service restarts (never restart inline)
- Prefer `loop` over `with_items` (deprecated)

---

### B) Role Scaffold

Use for: reusable, shareable, testable automation units.

**Directory structure:**
```
roles/<role_name>/
├── defaults/
│   └── main.yml          # Low-priority defaults (overridable)
├── vars/
│   └── main.yml          # High-priority role-internal vars
├── tasks/
│   ├── main.yml          # Entry point (import_tasks per OS/feature)
│   ├── install.yml
│   ├── configure.yml
│   └── service.yml
├── handlers/
│   └── main.yml
├── templates/
│   └── <config>.conf.j2
├── files/
│   └── <static_files>
├── meta/
│   └── main.yml          # Galaxy metadata, dependencies
└── README.md
```

**tasks/main.yml pattern:**
```yaml
---
- name: Include OS-specific variables
  ansible.builtin.include_vars: "{{ ansible_os_family }}.yml"
  failed_when: false

- ansible.builtin.import_tasks: install.yml
  tags: [install]

- ansible.builtin.import_tasks: configure.yml
  tags: [configure]

- ansible.builtin.import_tasks: service.yml
  tags: [service]
```

**defaults/main.yml pattern:**
```yaml
---
# Role: <role_name>
# All variables with safe defaults

role_package_name: nginx
role_service_name: nginx
role_config_path: /etc/nginx/nginx.conf
role_user: www-data
role_port: 80
role_enabled: true
```

---

### C) Inventory

**Static inventory (INI format):**
```ini
# inventory/hosts

[webservers]
web01.example.com ansible_host=10.0.1.10
web02.example.com ansible_host=10.0.1.11

[databases]
db01.example.com ansible_host=10.0.2.10

[loadbalancers]
lb01.example.com

[production:children]
webservers
databases
loadbalancers

[all:vars]
ansible_user=deploy
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3
```

**Static inventory (YAML format — preferred):**
```yaml
# inventory/hosts.yml
all:
  vars:
    ansible_user: deploy
    ansible_python_interpreter: /usr/bin/python3

  children:
    webservers:
      hosts:
        web01:
          ansible_host: 10.0.1.10
          http_port: 80
        web02:
          ansible_host: 10.0.1.11
          http_port: 80

    databases:
      hosts:
        db01:
          ansible_host: 10.0.2.10
          db_port: 5432

    staging:
      children:
        webservers:
        databases:
```

**group_vars structure:**
```
inventory/
├── hosts.yml
├── group_vars/
│   ├── all.yml              # Applies to all hosts
│   ├── all/
│   │   ├── vars.yml
│   │   └── vault.yml        # ansible-vault encrypted secrets
│   ├── webservers.yml
│   └── databases.yml
└── host_vars/
    └── web01.yml
```

---

### D) Jinja2 Templates

**Config file template pattern:**
```jinja2
{# templates/nginx.conf.j2 #}
{# Managed by Ansible - Do not edit manually #}

user {{ nginx_user | default('www-data') }};
worker_processes {{ nginx_worker_processes | default(ansible_processor_vcpus) }};

events {
    worker_connections {{ nginx_worker_connections | default(1024) }};
}

http {
    include mime.types;
    default_type application/octet-stream;

    {% if nginx_log_format is defined %}
    log_format main '{{ nginx_log_format }}';
    {% endif %}

    {% for vhost in nginx_vhosts | default([]) %}
    server {
        listen {{ vhost.port | default(80) }};
        server_name {{ vhost.name }};
        root {{ vhost.root }};

        {% if vhost.ssl | default(false) %}
        listen 443 ssl;
        ssl_certificate {{ vhost.ssl_cert }};
        ssl_certificate_key {{ vhost.ssl_key }};
        {% endif %}
    }
    {% endfor %}
}
```

**Key Jinja2 patterns:**
```jinja2
{# Default filter #}
{{ variable | default('fallback_value') }}

{# Conditional block #}
{% if ansible_os_family == "Debian" %}
apt_cache_valid_time: 3600
{% elif ansible_os_family == "RedHat" %}
yum_releasever: latest
{% endif %}

{# Loop over dict #}
{% for key, value in config_dict.items() %}
{{ key }} = {{ value }}
{% endfor %}

{# Join list #}
{{ my_list | join(', ') }}

{# Uppercase / replace #}
{{ service_name | upper | replace('-', '_') }}
```

---

### E) Variable Files

**Priority order (high → low):**
```
extra vars (-e)           # Highest priority
task vars
block vars
role and include vars
play vars
host facts
host_vars
group_vars/all
role defaults            # Lowest priority
```

**vault.yml pattern (sensitive data):**
```yaml
# group_vars/all/vault.yml
# Encrypt with: ansible-vault encrypt vault.yml

vault_db_password: "super_secret_password"
vault_api_key: "abc123xyz"
vault_ssl_cert_content: |
  -----BEGIN CERTIFICATE-----
  ...
  -----END CERTIFICATE-----
```

**vars.yml (reference vault vars):**
```yaml
# group_vars/all/vars.yml
db_password: "{{ vault_db_password }}"
api_key: "{{ vault_api_key }}"
```

---

### F) ansible.cfg

```ini
[defaults]
inventory           = ./inventory/hosts.yml
roles_path          = ./roles:~/.ansible/roles
collections_paths   = ./collections:~/.ansible/collections
remote_user         = deploy
private_key_file    = ~/.ssh/id_rsa
host_key_checking   = False
retry_files_enabled = False
stdout_callback     = yaml
callbacks_enabled   = profile_tasks, timer
interpreter_python  = auto_silent

# Performance tuning
forks               = 10
pipelining          = True
gathering           = smart
fact_caching        = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 3600

[privilege_escalation]
become              = True
become_method       = sudo
become_user         = root
become_ask_pass     = False

[ssh_connection]
ssh_args            = -C -o ControlMaster=auto -o ControlPersist=60s
control_path_dir    = /tmp/.ansible/cp
```

---

## Step 3: Full Project Structure

For complete projects, generate this layout:

```
<project_name>/
├── ansible.cfg
├── requirements.yml          # Galaxy roles/collections
├── site.yml                  # Master playbook
├── playbooks/
│   ├── deploy.yml
│   ├── rollback.yml
│   └── maintenance.yml
├── roles/
│   └── <role_name>/          # See Role Scaffold above
├── inventory/
│   ├── production/
│   │   ├── hosts.yml
│   │   ├── group_vars/
│   │   └── host_vars/
│   └── staging/
│       ├── hosts.yml
│       └── group_vars/
├── collections/
│   └── requirements.yml
├── filter_plugins/           # Custom Jinja2 filters
├── library/                  # Custom modules
└── .github/
    └── workflows/
        └── ansible-lint.yml  # CI validation
```

**requirements.yml:**
```yaml
---
collections:
  - name: community.general
    version: ">=7.0.0"
  - name: ansible.posix
  - name: community.docker
    version: "3.4.0"

roles:
  - name: geerlingguy.nodejs
    version: "6.1.0"
  - src: https://github.com/org/role.git
    scm: git
    version: main
    name: custom_role
```

---

## Step 4: Validation & Run Instructions

Always append these to generated output:

**Syntax check:**
```bash
ansible-playbook playbooks/deploy.yml --syntax-check
```

**Dry run (no changes):**
```bash
ansible-playbook playbooks/deploy.yml --check --diff
```

**Lint (requires ansible-lint):**
```bash
pip install ansible-lint
ansible-lint playbooks/deploy.yml
```

**Run with vault:**
```bash
ansible-playbook playbooks/deploy.yml --ask-vault-pass
# or with vault password file:
ansible-playbook playbooks/deploy.yml --vault-password-file ~/.vault_pass
```

**Limit to specific hosts/groups:**
```bash
ansible-playbook site.yml --limit webservers
ansible-playbook site.yml --limit web01.example.com
```

**Run specific tags:**
```bash
ansible-playbook site.yml --tags deploy,configure
ansible-playbook site.yml --skip-tags debug
```

**Ad-hoc commands:**
```bash
# Ping all hosts
ansible all -m ping

# Gather facts
ansible webservers -m ansible.builtin.setup

# Run shell command
ansible databases -m ansible.builtin.shell -a "df -h"

# Copy file
ansible all -m ansible.builtin.copy -a "src=file.conf dest=/etc/file.conf"
```

---

## Best Practices Checklist

Always apply these principles:

- ✅ **FQCN**: Use `ansible.builtin.copy`, not `copy`
- ✅ **Idempotency**: Every task must be safe to re-run
- ✅ **State explicit**: Always specify `state:` on resource modules
- ✅ **No shell when avoidable**: Prefer native modules over `shell`/`command`
- ✅ **Handlers for restarts**: Never restart services inline in tasks
- ✅ **Tags**: Tag every task/block for selective execution
- ✅ **Vault for secrets**: Never hardcode passwords or keys in plaintext
- ✅ **Defaults for all role vars**: Every role var must have a default
- ✅ **`changed_when` / `failed_when`**: Set on `shell`/`command` tasks
- ✅ **`when` conditions**: Use Ansible facts, not shell conditionals
- ✅ **Header comment**: First line of every file: `# Managed by Ansible`

---

## Common Module Reference

| Task                    | Module                          |
|-------------------------|---------------------------------|
| Install packages        | `ansible.builtin.package`       |
| Copy files              | `ansible.builtin.copy`          |
| Template files          | `ansible.builtin.template`      |
| Manage services         | `ansible.builtin.service`       |
| Manage users            | `ansible.builtin.user`          |
| Run commands            | `ansible.builtin.command`       |
| Run shell               | `ansible.builtin.shell`         |
| Manage files/dirs       | `ansible.builtin.file`          |
| Edit lines in files     | `ansible.builtin.lineinfile`     |
| Download files          | `ansible.builtin.get_url`       |
| Unarchive tarballs      | `ansible.builtin.unarchive`     |
| Manage cron jobs        | `ansible.builtin.cron`          |
| Manage firewall         | `ansible.posix.firewalld`       |
| Docker containers       | `community.docker.docker_container` |
| Git clone               | `ansible.builtin.git`           |
| Wait for condition      | `ansible.builtin.wait_for`      |
| Set facts               | `ansible.builtin.set_fact`      |
| Assert conditions       | `ansible.builtin.assert`        |
| Include variables       | `ansible.builtin.include_vars`  |
| Debug output            | `ansible.builtin.debug`         |

---

## Output Format Guidelines

When delivering Ansible artifacts:

1. **Always show full file path** as a comment at top of each file
2. **Group related files** together with clear separators
3. **Explain non-obvious choices** inline with `# comment`
4. **Provide run command** at the end of every response
5. **Flag secrets** — point out where vault encryption is needed
6. **One file per code block** — never mix multiple files in one block
