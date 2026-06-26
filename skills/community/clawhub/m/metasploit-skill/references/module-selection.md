# Module Selection Heuristics

## Inputs Required Before Choosing a Module

- Service type and exposed endpoint
- Product name and version confidence level
- Authentication requirement
- Target OS and architecture (if known)
- Reliability constraints (production safety, maintenance window)

## Selection Rules

1. Prefer modules with explicit compatibility to observed version range.
2. Prefer modules with non-destructive checks and stable public usage.
3. Prefer payloads that match objective and minimize operational impact.
4. Avoid noisy options unless explicitly approved in scope.
5. Record why one module was chosen over alternatives.

## Common Service-to-Module Discovery Patterns

### HTTP/Web
- Search: `search type:exploit service:http <product|cve>`
- Verify options: `TARGETURI`, `SSL`, `VHOST`, auth fields
- Typical payload families:
  - `linux/x64/meterpreter/reverse_tcp`
  - `cmd/unix/reverse_bash`
  - `php/meterpreter/reverse_tcp`

### SMB/Windows
- Search: `search type:exploit service:smb <product|cve>`
- Verify options: `RHOSTS`, `RPORT`, `SMBUser`, `SMBPass`, domain options
- Typical payload families:
  - `windows/x64/meterpreter/reverse_tcp`
  - `windows/shell/reverse_tcp`

### SSH
- Search: `search type:exploit service:ssh <product|cve>`
- Verify options: credentials, key paths, brute-force limits
- Typical payload families:
  - command or session payloads aligned with module support

### Database Services
- Search: `search type:exploit mysql` or `search type:auxiliary postgres`
- Verify options: DB credentials, database name, TLS settings
- Prefer auxiliary enumeration before exploit where possible

## Payload Choice Guidelines

1. Choose architecture-compatible payloads first.
2. Choose staged vs stageless based on network controls and reliability.
3. Choose meterpreter only when its post-exploitation features are required.
4. Keep fallback payloads ready for one-step retries.

## Verification Checklist Before Execution

- `show options` has no missing required fields
- Payload listener values are reachable from target network
- Target host is in approved scope
- Check mode is enabled when module supports it
- Logging method is defined (`spool` or equivalent)
