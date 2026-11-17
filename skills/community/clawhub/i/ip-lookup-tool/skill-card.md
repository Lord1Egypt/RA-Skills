## Description:

Looks up the current public egress IP address, approximate city, country, and ISP for the running agent session, including a best-effort Chinese city name when coordinates are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daguniang](https://clawhub.ai/user/daguniang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about the current session's public internet-facing IP address and approximate network location. It is intended to report the public egress IP, not a private LAN address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party IP and geocoding services may receive the user's public IP address, request timing, and approximate location lookup data.

Mitigation: Install and run the skill only when that disclosure is acceptable, and disclose the contacted services before use in privacy-sensitive environments.

Risk: IP-based geolocation can be approximate or misleading, especially for VPNs, proxies, carrier-grade NAT, or cloud egress addresses.

Mitigation: Present location as approximate public egress information and avoid treating it as the user's exact physical location.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daguniang/skills/ip-lookup-tool)
- [Publisher Profile](https://clawhub.ai/user/daguniang)
- [ipinfo.io JSON endpoint](https://ipinfo.io/json)
- [ifconfig.co JSON endpoint](https://ifconfig.co/json)
- [ip.sb GeoIP endpoint](https://api.ip.sb/geoip)
- [OpenStreetMap Nominatim reverse geocoding endpoint](https://nominatim.openstreetmap.org/reverse)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text summary or JSON from a Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON output may include ip, city, cityZh, region, country, org, loc, source, fetchedAt, and raw provider data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
