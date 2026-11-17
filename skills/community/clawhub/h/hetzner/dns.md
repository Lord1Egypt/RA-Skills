# DNS and Certificates — Zones, Records, and What Managed TLS Requires

Scope: Hetzner's DNS service, domain registration, and the certificate paths that depend on them. Record-design theory beyond this provider is a separate skill (`dns`).

**Before changing anything**, read `~/Clawic/data/domains/domains.md`: which domains exist, where each zone is hosted, and when each expires. Moving a zone that a managed certificate depends on breaks TLS renewals silently.

**Contents:** [What Hetzner DNS Is](#what-hetzner-dns-is) · [Zones and Records](#zones-and-records) · [Managed Certificates Need the Zone Here](#managed-certificates-need-the-zone-here) · [ACME Without Hetzner DNS](#acme-without-hetzner-dns) · [Reverse DNS Is Not in the Zone](#reverse-dns-is-not-in-the-zone) · [Domain Registration and Renewal](#domain-registration-and-renewal) · [Moving a Zone](#moving-a-zone) · [Records That Break Deploys](#records-that-break-deploys)

## What Hetzner DNS Is

- A free authoritative DNS service with a web console and an API, usable for any domain regardless of where it is registered.
- Anycast nameservers, standard record types, zone file import and export.
- No edge features: no proxying, no WAF, no geo-routing, no analytics, no DDoS absorption in front of your origin. If those are the requirement, an edge provider goes in front and this is not the tool (`dns_provider: external`).
- The API is what makes it useful for automation: ACME DNS-01 challenges, dynamic records, and Terraform-managed zones.

## Zones and Records

- A zone is created per domain and takes effect once the registrar's nameservers point at Hetzner's. Until then, edits change nothing — the classic "I updated the record and nothing happened".
- TTL is the tool that decides how long a mistake lasts. Lower TTL to 300 seconds **before** a planned cutover, wait for the old TTL to expire, then make the change; raise it back afterwards.
- Apex records: an A/AAAA at the apex works normally here since the apex points at an IP, not a hostname. A load balancer is reached by its IP or by a CNAME on a subdomain — do not put a CNAME at the apex.
- Zone import from a zone file is the fast path when migrating from another provider, and it is also the fast way to lose records the export omitted. Diff the record list on both sides before switching nameservers.
- Keep the zone in code when `iac_tool` is set: a DNS record created by hand during an incident is the one that nobody can explain six months later (`automation.md`).

## Managed Certificates Need the Zone Here

The load balancer can obtain and renew a managed TLS certificate automatically, **only** for domains whose zone is hosted in Hetzner DNS. The validation runs against the zone the provider controls.

Consequences to state before someone plans around it:

- A domain on an external DNS provider cannot use managed certificates. The options are: upload a certificate to the load balancer and renew it yourself, or terminate TLS on the backend with Caddy or nginx.
- A certificate stuck pending is almost always this: the zone is not here, or the nameservers have not switched yet (`debug.md`).
- **Moving a zone away later breaks renewal**, not the current certificate — so the failure appears weeks after the change, when nobody connects the two. Record the dependency in `domains.md` `Notes` the moment a managed certificate is created.

## ACME Without Hetzner DNS

When TLS is terminated on the server rather than the load balancer:

- **HTTP-01** needs port 80 reachable from the internet for the challenge. Keep 80 open in the cloud firewall even when it only redirects to 443 — closing it is a renewal outage 60 days later, long after the change (`firewall.md`).
- **DNS-01** is required for wildcards and for servers with no public HTTP, and it needs an API credential for whichever DNS provider holds the zone. That credential is a secret: pointer only, and scoped to the single zone if the provider supports it.
- Renewal failures are silent by design — the certificate is valid until it is not. Monitor expiry as a metric, not as a log line, and put the check in `## Due`.

## Reverse DNS Is Not in the Zone

PTR records for a server's public addresses are set on the **IP address**, in the cloud panel or in Robot, not in the DNS zone. The forward record does live in the zone, and both must agree for outbound mail to work (`mail.md`). This split catches people every time an address changes.

## Domain Registration and Renewal

- Domains can be registered through Hetzner, or registered elsewhere with the zone hosted here. Both are normal; the row in `domains.md` records which is which, because a transfer touches only one of them.
- **Renewal is the risk.** An expired domain is a total outage that DNS changes cannot fix, and recovery after the grace period is expensive or impossible. Every domain row gets a matching `## Due` line with its expiry date, whether or not auto-renew is on — auto-renew fails when the payment method expires.
- Transfers need the auth/EPP code from the losing registrar and a domain that is not locked. The code is a credential: pointer only, and it expires.
- Registrant contact data is what the registry acts on: an unreachable registrant email can suspend a domain regardless of payment.

## Moving a Zone

The order that avoids downtime:

1. Export the existing zone; build the new zone here with an identical record set, including MX, TXT, SPF/DKIM/DMARC, and anything a third-party service verified with a TXT record.
2. Diff the two record sets. Verification records for mail, search consoles and SaaS integrations are the ones that get dropped.
3. Lower TTLs at the old provider and wait out the old TTL.
4. Switch nameservers at the registrar.
5. Query both nameserver sets directly and confirm they answer identically before considering it done.
6. Leave the old zone in place for a week — nameserver changes propagate unevenly.
7. Check anything that depended on the old provider's features: managed certificates, redirect rules, proxying.

**Write it down.** A domain registered, transferred, or whose zone moved updates its row in `~/Clawic/data/domains/domains.md` in the same turn (`Registrar`, `Zone hosted at`, `Expires`, `Notes` for any managed-certificate dependency), and its expiry goes into `## Due` in `~/Clawic/data/hetzner/memory.md`. A migration that took real work — the record diff, the surprises — becomes `~/Clawic/data/hetzner/artifacts/dns-migration-<domain>.md` with its `## Boxes` line.

## Records That Break Deploys

| Record situation | What breaks | Fix |
|---|---|---|
| A record still pointing at a deleted server's IP | Traffic to an address that now belongs to someone else's server | Update DNS as part of the teardown, before deleting the server |
| CNAME at the apex | Resolution failures at some resolvers, mail delivery problems | A/AAAA at the apex; CNAME only on subdomains |
| TTL 86400 during a cutover | A day of split traffic | Lower to 300 before, raise after |
| Two SPF records | Both invalid; mail scored as unauthenticated | One SPF record, merged (`mail.md`) |
| Wildcard `*` A record | Every typo and every unrouted subdomain hits one server, including staging and admin hosts | Explicit records; wildcard only with a deliberate catch-all handler |
| DNSSEC enabled at the registrar but not matching the zone | Total resolution failure, and it looks like an outage everywhere at once | Keep DS records and the zone's keys in step; disable DNSSEC before a nameserver move and re-enable after |
