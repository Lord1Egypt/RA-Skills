# Outbound Mail — Port 25, rDNS, and Whether to Send From Here At All

Scope: getting mail out of a Hetzner server and into an inbox. DNS zone mechanics are a separate route (`dns.md`).

**Before designing anything that sends mail**, read `~/Clawic/data/domains/domains.md` for the domain and where its zone lives, and `## Current Infrastructure` for whether a relay is already in use.

**Contents:** [Port 25 Is Blocked](#port-25-is-blocked) · [The First Decision: Relay or Self-Host](#the-first-decision-relay-or-self-host) · [Reverse DNS](#reverse-dns) · [SPF, DKIM, DMARC](#spf-dkim-dmarc) · [Reputation of the Address Space](#reputation-of-the-address-space) · [Transactional Mail From an Application](#transactional-mail-from-an-application) · [Receiving Mail](#receiving-mail) · [Debugging a Rejection](#debugging-a-rejection)

## Port 25 Is Blocked

Outbound SMTP on port 25 is blocked by default for new accounts. This is the single most common "my app cannot send mail" cause on this provider, and it looks like a network problem: connections to port 25 simply time out.

- Confirm it in one step: from the server, open a TCP connection to a known mail exchanger on 25 and watch it hang, then try the same to port 587 on a relay and watch it succeed. Timeouts on 25 with 587 working is the signature.
- **Unblocking is a support request**, granted after the account has some history and a plausible use case. It is not instant, and it is not guaranteed.
- Submission ports (587, 465) to *other people's* relays are generally not affected — which is why relaying works while direct sending does not.
- Plan around it: if the launch depends on sending mail, either request the unblock weeks early or design for a relay from the start.

## The First Decision: Relay or Self-Host

| | Relay through a mail provider | Run your own mail server |
|---|---|---|
| Port 25 | Not needed outbound | Required, and must be unblocked |
| Reputation | The provider's, already warm | Yours, cold, on address space with history |
| Setup | An API key or SMTP credentials | Postfix, TLS, DKIM signing, queue monitoring, blocklist monitoring |
| Failure mode | Provider outage, quota | Silent delivery failure nobody notices for a week |
| Cost | Per-message above a free tier | The server you already have |

**Default: relay.** For transactional mail — password resets, receipts, notifications — the delivery rate difference is large and the operational cost of self-hosting is permanent. Self-hosting earns its place when the mail *is* the product, when the volume makes per-message pricing painful, or when the content cannot leave your infrastructure for legal reasons.

If self-hosting: the credentials for that relay or mail server are secrets — pointer only, never in a config file committed anywhere or in a note under `~/Clawic/data/` (`security.md`).

## Reverse DNS

A PTR record for the sending IP that resolves to a hostname, and a matching forward A/AAAA record back to the same IP, is a hard requirement for many receivers. Without it, mail is rejected or scored as spam before content is even considered.

- rDNS is set **per IP address** in the panel or Robot, not per server and not in the DNS zone.
- The name must match the hostname the server uses in its SMTP `HELO`/`EHLO`, and the forward record must exist and point back. All three have to agree.
- Set it for IPv6 too if the server will send over IPv6, or disable IPv6 sending — a missing IPv6 PTR fails just as hard as a missing IPv4 one, and is easier to overlook.
- After a server is rebuilt or recreated with a new IP, the rDNS is gone. This is a standing item on the restore checklist (`storage.md`).

## SPF, DKIM, DMARC

The three records that decide whether a receiver trusts the message. All three live in the domain's zone (`dns.md`):

| Record | What it says | The common mistake |
|---|---|---|
| SPF | Which hosts may send for this domain | More than one SPF record on the domain, or exceeding the DNS lookup limit by chaining `include:` — both invalidate it |
| DKIM | A signature proving the message was not altered | Key published for one selector while the server signs with another; or a key rotated in the zone but not on the server |
| DMARC | What to do when SPF or DKIM fails, and where to send reports | Publishing `p=reject` on day one and silently killing legitimate mail from a forgotten sender |

Order of operations that avoids the outage: publish SPF and DKIM, publish DMARC at `p=none` with a reports address, read the reports for two weeks to find every legitimate sender, then move to `quarantine` and finally `reject`.

The DKIM **private** key is a secret and is referenced by pointer; the public key in the TXT record is not.

## Reputation of the Address Space

Cheap hosting attracts abuse, and some receivers and blocklists treat parts of this provider's address space with suspicion regardless of your behaviour. That is a fact to design around, not to argue with:

- Check the sending IP against the major blocklists before launching, not after the first bounce. A newly allocated address can arrive with someone else's history.
- If the address is listed, the delisting process belongs to the blocklist, not to the hosting provider. Some delist automatically after a quiet period; some require a request.
- Warm-up matters: sending a large first campaign from a cold address is how a clean IP becomes a listed one.
- This is the strongest practical argument for relaying transactional mail even when everything else runs here.

## Transactional Mail From an Application

- Send through the relay's submission port with authentication, over TLS. Never send unauthenticated on 25 from an application.
- Queue and retry are the application's problem or the local MTA's — a synchronous send in a web request turns a mail-provider hiccup into a user-visible error.
- Bounce and complaint handling is not optional: a service that keeps mailing addresses that hard-bounce gets its reputation destroyed by its own retry logic.
- Rate limits exist on every relay. Know the number before a launch sends 50,000 password resets.

## Receiving Mail

- Receiving needs inbound 25 open to the server and a correct MX record; inbound is not blocked the way outbound is.
- Running a full mail server for receiving (spam filtering, storage, IMAP, TLS certificates, upgrades) is a considerably larger commitment than sending. For most projects, a mailbox provider is the right answer and the domain's MX points there.
- An open relay is the fastest route to an abuse notice and a locked account (`security.md`). If a mail server is deployed, verify it is not relaying for anyone before it stays up overnight.

## Debugging a Rejection

| Symptom | Likely cause | Check |
|---|---|---|
| Connections to port 25 time out | Outbound 25 blocked on the account | Try a relay's 587; then open a support request |
| Receiver rejects with a policy/PTR message | Missing or mismatched rDNS | PTR for the sending IP, forward record, and `HELO` name all agreeing |
| Mail accepted but lands in spam | SPF/DKIM alignment, or reputation | DMARC aggregate reports name the failing mechanism |
| Some receivers accept, one rejects everything | Blocklist entry, or that receiver's own policy | Look up the IP on the major lists; read the exact SMTP reply text |
| Worked yesterday, fails today after a rebuild | New IP, no rDNS, DKIM key not on the new host | The restore checklist item that always gets missed |
| Bounces to a forwarded address | Forwarding breaks SPF; the forwarder must rewrite the sender | Not fixable from your side alone; DMARC reports show it |

**Write it down.** Whether outbound 25 is unblocked on this account, which relay is in use, and the rDNS set for each sending address are facts the next session needs and cannot discover cheaply — they go into `## Current Infrastructure` in `~/Clawic/data/hetzner/memory.md`. The domain, its zone location and its SPF/DKIM/DMARC state go into `~/Clawic/data/domains/domains.md`. A working mail configuration that took effort — the relay setup, the DKIM selector, the delisting outcome — becomes `~/Clawic/data/hetzner/artifacts/mail-<domain>.md` with its `## Boxes` line.
