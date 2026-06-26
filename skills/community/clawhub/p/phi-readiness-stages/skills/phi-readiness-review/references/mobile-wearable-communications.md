# Mobile, Wearable, and Communications Review

Last reviewed: March 17, 2026.

Use this reference when the reviewed workflow includes phones, tablets, wearables, push notifications, email, SMS, voice calls, local device storage, lock-screen previews, widgets, watch displays, or background sync.

## Core rule

Do not treat mobile and wearable communications as categorically banned or categorically safe. Assess message content, delivery surface, safeguards, user direction, and device controls.

## Questions to answer

- Can PHI appear in push notifications, lock-screen previews, widgets, watch faces, default displays, email subject lines, or SMS previews?
- Is PHI cached locally on the device, stored offline, exported to files, copied into screenshots, or included in backups?
- What happens if a device is lost, stolen, shared, unlocked, or synced to a companion device?
- Are outbound communications user-directed, treatment-related, operational, or marketing-oriented?
- Are timeout, logout, token revocation, remote wipe, device encryption, and local access restrictions evidenced?
- Does wearable or companion-device behavior expose PHI by default or through background sync?

## Conservative review rules

### Push notifications and default displays

Avoid PHI in push notifications, lock-screen previews, widgets, watch faces, and default displays unless the team can show tight content restriction and supporting safeguards.

### Email, SMS, phone, and similar channels

Do not use blanket rules like `email is never compliant`. Instead, ask whether the communication purpose, content, safeguards, and user direction are evidenced. If the team cannot show those safeguards, treat the channel as a blocker for higher-stage claims.

### Local device storage

If PHI resides on the device, require evidence for local encryption, access control, session timeout or logout, lost-device response, and token or key revocation where applicable.

### Wearables and companion devices

Treat wearables and companion devices as an extension of the same exposure path. Review what is shown by default, what syncs automatically, what remains cached, and how deletion or revocation propagates.

## Evidence to seek

- notification content rules and examples
- local storage and cache design
- device-control expectations, MDM support, or remote-wipe procedures where relevant
- session timeout, logout, revocation, and lost-device response evidence
- wearable sync and deletion behavior

## Output guidance

- name the exact exposed surface if PHI can appear outside the primary app view
- separate channel risk from HIPAA role analysis
- if device safeguards are unclear, cap confidence and treat operational claims conservatively

## Verify these official sources live

- `Resources for Mobile Health Apps Developers` in `references/source-registry.md`
- `Protecting the privacy and security of your health information when using your personal cell phone or tablet` in `references/source-registry.md`
- `Treatment by fax, email, or phone FAQ` in `references/source-registry.md`
- `Right to have PHI sent by unsecure email` in `references/source-registry.md` when user-directed transmission matters
- Security Rule and device-related guidance from `references/source-registry.md`
