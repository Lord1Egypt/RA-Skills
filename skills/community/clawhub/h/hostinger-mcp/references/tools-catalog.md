# Tools Catalog — Hostinger MCP

The official tool catalog for the **Hostinger MCP server** (npm `hostinger-api-mcp`), from [hostinger/api-mcp-server](https://github.com/hostinger/api-mcp-server). 127 tools across 6 categories (VPS, hosting, domains, DNS, Reach, billing), each category also available as a standalone binary (6 category binaries + the all-in-one `hostinger-api-mcp` = 7 binaries). Tools appear in Claude as `mcp__hostinger-<account>__<tool>`.

Flags: **R** = read-only · **W** = write (requires confirmation) · **W!** = destructive or money-spending (requires double confirmation).

> **Load only the category binaries you need** (see `installation.md`) — connecting all 127 tools at once bloats context. The live server is the source of truth if Hostinger changes tool names.

> 💸 **Money-spending tools** (domain/VPS purchase, subscriptions, payment-method changes) are flagged **W!** — always confirm the cost and the account before executing.

## VPS

| Tool | Flag | What it does |
|------|------|--------------|
| `VPS_getVirtualMachinesV1` | R | List all available virtual machines. |
| `VPS_getVirtualMachineDetailsV1` | R | Get detailed configuration for a single virtual machine. |
| `VPS_getDataCenterListV1` | R | List available data centers (location options before deploying). |
| `VPS_getTemplatesV1` | R | List available OS templates for virtual machines. |
| `VPS_getTemplateDetailsV1` | R | Get details about a specific OS template. |
| `VPS_getMetricsV1` | R | Retrieve historical CPU/memory/disk metrics for a VM. |
| `VPS_getScanMetricsV1` | R | Retrieve Monarx malware-scanner metrics for a VM. |
| `VPS_getActionsV1` | R | List actions/operations executed on a VM. |
| `VPS_getActionDetailsV1` | R | Get detailed info about a specific VM action. |
| `VPS_getBackupsV1` | R | List available backup points for a VM. |
| `VPS_getSnapshotV1` | R | Get current snapshot info for a VM. |
| `VPS_getPublicKeysV1` | R | List public (SSH) keys on your account. |
| `VPS_getAttachedPublicKeysV1` | R | List public keys attached to a specific VM. |
| `VPS_getFirewallListV1` | R | List all available firewalls. |
| `VPS_getFirewallDetailsV1` | R | Get a firewall and its rules by ID. |
| `VPS_getPostInstallScriptsV1` | R | List post-install scripts on your account. |
| `VPS_getPostInstallScriptV1` | R | Get a single post-install script by ID. |
| `VPS_getProjectListV1` | R | List Docker Compose projects deployed on a VM. |
| `VPS_getProjectContentsV1` | R | Get a project's docker-compose.yml, metadata, and state. |
| `VPS_getProjectContainersV1` | R | List containers belonging to a Docker Compose project. |
| `VPS_getProjectLogsV1` | R | Retrieve aggregated log entries from a project's services. |
| `VPS_purchaseNewVirtualMachineV1` | W! | 💸 Purchase and set up a new virtual machine (spends money). |
| `VPS_setupPurchasedVirtualMachineV1` | W | Configure and initialize a purchased VM in `initial` state. |
| `VPS_recreateVirtualMachineV1` | W! | Recreate a VM from scratch — reinstalls OS, wipes data. |
| `VPS_startVirtualMachineV1` | W | Start a virtual machine. |
| `VPS_stopVirtualMachineV1` | W | Stop a virtual machine. |
| `VPS_restartVirtualMachineV1` | W | Restart a virtual machine (full stop + start). |
| `VPS_startRecoveryModeV1` | W | Boot a VM into recovery mode for system repair. |
| `VPS_stopRecoveryModeV1` | W | Exit recovery mode on a VM. |
| `VPS_setHostnameV1` | W | Set a VM's hostname (does not update PTR automatically). |
| `VPS_resetHostnameV1` | W | Reset a VM's hostname and PTR record to default. |
| `VPS_setNameserversV1` | W | Set nameservers for a VM. |
| `VPS_setRootPasswordV1` | W | Set the root password for a VM. |
| `VPS_setPanelPasswordV1` | W | Set the panel password for a VM. |
| `VPS_restoreBackupV1` | W | Restore a VM from a backup point. |
| `VPS_createSnapshotV1` | W | Create a snapshot capturing a VM's state and data. |
| `VPS_restoreSnapshotV1` | W | Restore a VM to a previous state from a snapshot. |
| `VPS_deleteSnapshotV1` | W! | Delete a VM snapshot. |
| `VPS_createPublicKeyV1` | W | Register a new SSH public key on your account. |
| `VPS_attachPublicKeyV1` | W | Attach existing public keys to a VM. |
| `VPS_deletePublicKeyV1` | W! | Delete a public key from your account. |
| `VPS_createPTRRecordV1` | W | Create or update a PTR (reverse DNS) record for a VM. |
| `VPS_deletePTRRecordV1` | W! | Delete a VM's PTR record (reverse DNS lookups stop resolving). |
| `VPS_createNewFirewallV1` | W | Create a new firewall configuration. |
| `VPS_createFirewallRuleV1` | W | Add a new rule to a firewall. |
| `VPS_updateFirewallRuleV1` | W | Update a firewall rule. |
| `VPS_deleteFirewallRuleV1` | W! | Delete a firewall rule. |
| `VPS_deleteFirewallV1` | W! | Delete a firewall (auto-deactivates on attached VMs). |
| `VPS_activateFirewallV1` | W | Activate a firewall on a VM (one active firewall per VM). |
| `VPS_deactivateFirewallV1` | W | Deactivate a firewall on a VM. |
| `VPS_syncFirewallV1` | W | Re-sync a firewall to a VM after rule changes. |
| `VPS_createPostInstallScriptV1` | W | Add a new post-install script to your account. |
| `VPS_updatePostInstallScriptV1` | W | Update an existing post-install script. |
| `VPS_deletePostInstallScriptV1` | W! | Delete a post-install script from your account. |
| `VPS_installMonarxV1` | W | Install the Monarx malware scanner on a VM. |
| `VPS_uninstallMonarxV1` | W | Uninstall the Monarx malware scanner from a VM. |
| `VPS_createNewProjectV1` | W | Deploy a new Docker Compose project from YAML or URL. |
| `VPS_updateProjectV1` | W | Pull latest images and recreate a project's containers. |
| `VPS_startProjectV1` | W | Start all stopped services in a Docker Compose project. |
| `VPS_stopProjectV1` | W | Stop all running services in a Docker Compose project. |
| `VPS_restartProjectV1` | W | Restart all services in a Docker Compose project. |
| `VPS_deleteProjectV1` | W! | Remove a Docker Compose project, stopping/cleaning containers. |

## Hosting

| Tool | Flag | What it does |
|------|------|--------------|
| `hosting_listWebsitesV1` | R | List websites (main and addon) for the authenticated client. |
| `hosting_listOrdersV1` | R | List hosting orders accessible to the client. |
| `hosting_listAvailableDatacentersV1` | R | List datacenters available for setting up hosting plans. |
| `hosting_listAccountDatabasesV1` | R | List databases for an account (filter by domain/assigned). |
| `hosting_listWebsiteSubdomainsV1` | R | List subdomains created under a website. |
| `hosting_listWebsiteParkedDomainsV1` | R | List parked/alias domains created under a website. |
| `hosting_listJsDeployments` | R | List JavaScript application deployments and their status. |
| `hosting_showJsDeploymentLogs` | R | Retrieve logs for a JS application deployment (debugging). |
| `hosting_verifyDomainOwnershipV1` | R | Check whether a domain is verified/accessible. |
| `hosting_generateAFreeSubdomainV1` | W | Generate a unique free subdomain for hosting. |
| `hosting_createWebsiteV1` | W | Create a new website (domain + order ID). |
| `hosting_createWebsiteSubdomainV1` | W | Create a new subdomain for a website. |
| `hosting_deleteWebsiteSubdomainV1` | W! | Delete a subdomain from a website. |
| `hosting_createWebsiteParkedDomainV1` | W | Create a parked/alias domain for a website. |
| `hosting_deleteWebsiteParkedDomainV1` | W! | Delete a parked/alias domain from a website. |
| `hosting_createAccountDatabaseV1` | W | Create a database with user and password for an account. |
| `hosting_deleteAccountDatabaseV1` | W! | Permanently delete a database and its remote connections. |
| `hosting_importWordpressWebsite` | W | Import a WordPress site from an archive + database dump. |
| `hosting_deployWordpressPlugin` | W | Upload and deploy a WordPress plugin from a directory. |
| `hosting_deployWordpressTheme` | W | Upload and deploy a WordPress theme (optionally activate it). |
| `hosting_deployJsApplication` | W | Deploy a JS application from an archive (builds on server). |
| `hosting_deployStaticWebsite` | W | Deploy a pre-built static website from an archive. |

## Domains

| Tool | Flag | What it does |
|------|------|--------------|
| `domains_getDomainListV1` | R | List all domains on your account. |
| `domains_getDomainDetailsV1` | R | Get detailed configuration and status for a domain. |
| `domains_checkDomainAvailabilityV1` | R | Check domain-name availability across multiple TLDs. |
| `domains_getDomainForwardingV1` | R | View a domain's forwarding/redirect configuration. |
| `domains_getWHOISProfileListV1` | R | List WHOIS contact profiles. |
| `domains_getWHOISProfileV1` | R | Get a WHOIS contact profile. |
| `domains_getWHOISProfileUsageV1` | R | List domains using a given WHOIS contact profile. |
| `domains_purchaseNewDomainV1` | W! | 💸 Purchase and register a new domain (spends money). |
| `domains_updateDomainNameserversV1` | W | Set nameservers for a domain. |
| `domains_createDomainForwardingV1` | W | Set up domain forwarding/redirect to another URL. |
| `domains_deleteDomainForwardingV1` | W! | Remove a domain's forwarding configuration. |
| `domains_enableDomainLockV1` | W | Enable domain lock (blocks transfer to another registrar). |
| `domains_disableDomainLockV1` | W | Disable domain lock (required before transferring out). |
| `domains_enablePrivacyProtectionV1` | W | Hide the owner's personal info in WHOIS. |
| `domains_disablePrivacyProtectionV1` | W | Expose the owner's personal info in WHOIS. |
| `domains_createWHOISProfileV1` | W | Add a new WHOIS contact profile for registration. |
| `domains_deleteWHOISProfileV1` | W! | Delete an unused WHOIS contact profile. |
| `v2_getDomainVerificationsDIRECT` | R | List pending and completed domain verifications. (Tool name uses a non-standard `v2_…DIRECT` prefix; it belongs to domain verification.) |

## DNS

| Tool | Flag | What it does |
|------|------|--------------|
| `DNS_getDNSRecordsV1` | R | Retrieve the DNS zone records for a domain. |
| `DNS_getDNSSnapshotListV1` | R | List DNS snapshots (backup points) for a domain. |
| `DNS_getDNSSnapshotV1` | R | Retrieve a specific DNS snapshot's zone records. |
| `DNS_validateDNSRecordsV1` | R | Validate DNS records before applying an update. |
| `DNS_updateDNSRecordsV1` | W | Update DNS records (optionally overwrite existing ones). |
| `DNS_deleteDNSRecordsV1` | W! | Delete DNS records for a domain (filter by name/type). |
| `DNS_resetDNSRecordsV1` | W! | Reset a DNS zone to its default records. |
| `DNS_restoreDNSSnapshotV1` | W | Restore a DNS zone to a previous snapshot. |

## Reach (email marketing)

| Tool | Flag | What it does |
|------|------|--------------|
| `reach_listProfilesV1` | R | List all profiles available to the client. |
| `reach_listContactsV1` | R | List contacts (filter by group and subscription status). |
| `reach_listContactGroupsV1` | R | List contact groups used to organize contacts. |
| `reach_listSegmentsV1` | R | List all contact segments. |
| `reach_getSegmentDetailsV1` | R | Get details of a specific segment by UUID. |
| `reach_listSegmentContactsV1` | R | List/filter contacts belonging to a specific segment. |
| `reach_createANewContactV1` | W | Create a single new contact. |
| `reach_createNewContactsV1` | W | Create new contacts (bulk). |
| `reach_createANewContactSegmentV1` | W | Create a new contact segment. |
| `reach_deleteAContactV1` | W! | Permanently delete a contact by UUID. |

## Billing

| Tool | Flag | What it does |
|------|------|--------------|
| `billing_getCatalogItemListV1` | R | List catalog items available for order (prices in cents). |
| `billing_getSubscriptionListV1` | R | List all subscriptions on your account. |
| `billing_getPaymentMethodListV1` | R | List payment methods available for placing orders. |
| `billing_enableAutoRenewalV1` | W! | 💸 Enable auto-renewal for a subscription (charges automatically at renewal). |
| `billing_disableAutoRenewalV1` | W | Disable auto-renewal for a subscription. |
| `billing_setDefaultPaymentMethodV1` | W! | 💸 Set the default payment method for future orders. |
| `billing_deletePaymentMethodV1` | W! | Delete a payment method from your account. |
