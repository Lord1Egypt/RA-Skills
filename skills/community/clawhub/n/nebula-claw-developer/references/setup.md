# Restricted User Setup Reference

## Purpose

Use a dedicated non-admin OpenNebula user for restricted control plane actions, while still executing the local CLI on the node through the local service account.

## Example values

- OpenNebula user: `restrictedapi`
- Curated image: `curated-ubuntu-24-04-for-nebula-claw-developer`
- Curated template: `curated-ubuntu-24-04-for-nebula-claw-developer`
- Curated network: `vm`

## Create the restricted user

```bash
sudo -u oneadmin env HOME=/var/lib/one \
  oneuser create restrictedapi StrongTempPass123!
```

## Import a curated Ubuntu 24.04 image from the marketplace

```bash
sudo -u oneadmin env HOME=/var/lib/one \
  onemarketapp export "Ubuntu 24.04" curated-ubuntu-24-04-for-nebula-claw-developer --datastore default
```

## Share curated resources with the non-admin group

Template:

```bash
sudo -u oneadmin env HOME=/var/lib/one \
  onetemplate chgrp curated-ubuntu-24-04-for-nebula-claw-developer users
sudo -u oneadmin env HOME=/var/lib/one \
  onetemplate chmod curated-ubuntu-24-04-for-nebula-claw-developer 640
```

Image:

```bash
sudo -u oneadmin env HOME=/var/lib/one \
  oneimage chgrp curated-ubuntu-24-04-for-nebula-claw-developer users
sudo -u oneadmin env HOME=/var/lib/one \
  oneimage chmod curated-ubuntu-24-04-for-nebula-claw-developer 640
```

Network:

```bash
sudo -u oneadmin env HOME=/var/lib/one \
  onevnet chgrp vm users
sudo -u oneadmin env HOME=/var/lib/one \
  onevnet chmod vm 640
```

## Direct command tests as restricted user

List:

```bash
sudo -u oneadmin env HOME=/var/lib/one \
  onevm list --csv --user restrictedapi --password StrongTempPass123!
```

Create:

```bash
sudo -u oneadmin env HOME=/var/lib/one \
  onetemplate instantiate curated-ubuntu-24-04-for-nebula-claw-developer \
  --name restricted-api-test \
  --user restrictedapi \
  --password StrongTempPass123!
```

Delete:

```bash
sudo -u oneadmin env HOME=/var/lib/one \
  onevm terminate restricted-api-test \
  --hard \
  --user restrictedapi \
  --password StrongTempPass123!
```

## API config example

```json
{
  "opennebula": {
    "user": "restrictedapi",
    "password": "change-me"
  },
  "templates": [
    {
      "name": "curated-ubuntu-24-04-for-nebula-claw-developer",
      "description": "Ubuntu 24.04 curated development VM for disposable OpenClaw and infrastructure experiments."
    }
  ]
}
```

## Follow-up hardening

- Move the password out of JSON config.
- Add API authentication.
- Keep the curated `templates` allowlist small and documented with descriptions.
- Add TTL-based cleanup for disposable VMs.
- Restrict bind address and network exposure according to the deployment.
- Ensure the service account has passwordless sudo for the exact `one*` binaries used by the API, otherwise systemd runs can hang on sudo prompts.
