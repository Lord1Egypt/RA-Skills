## Description:

Deploy a self-hosted Obsidian LiveSync server (CouchDB in Docker behind a Cloudflare Tunnel with zero inbound ports), covering upstream provisioning, Setup URI generation with mandatory end-to-end encryption, a post-deploy security audit, and a tested backup/restore procedure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinian5216](https://clawhub.ai/user/xinian5216)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Obsidian users use this skill to deploy and maintain a private LiveSync backend with CouchDB, a Cloudflare Tunnel, end-to-end encryption, and rehearsed backup and restore steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: On older Docker versions, loopback-published CouchDB ports may still be reachable from nearby machines, exposing private notes.

Mitigation: Use Docker 28.0.0 or a verified patched equivalent, and verify database isolation from another machine before syncing private notes.

Risk: CouchDB credentials and the LiveSync Setup URI can grant access to the database and its contents.

Mitigation: Review downloaded scripts before running them, keep credentials in a mode-600 environment file, store the encryption passphrase in a password manager, and deliver Setup URIs through a channel that does not retain them.

Risk: The setup creates persistent services and changes Cloudflare DNS, which can have ongoing operational effects.

Mitigation: Review the planned services and DNS changes, and complete the documented post-deployment security audit.

## Reference(s):

- [Obsidian LiveSync project](https://github.com/vrtmrz/obsidian-livesync)
- [LiveSync CouchDB provisioning script](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/1.0.42/utils/couchdb/couchdb-init.sh)
- [LiveSync Setup URI generator](https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/1.0.42/utils/setup/generate_setup_uri.ts)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deployment steps and examples for a Linux host; adapt paths and domain values to the deployment.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
