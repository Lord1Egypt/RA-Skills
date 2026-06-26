## Description: <br>
Looks up the current public egress IP address, approximate city location including a best-effort Chinese city name, and ISP or autonomous system information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daguniang](https://clawhub.ai/user/daguniang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to answer questions about the current session's public IP address, approximate city or country, and ISP. It helps distinguish the public egress IP from local private network addresses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public IP address and approximate location lookup requests are sent to third-party IP and geocoding providers. <br>
Mitigation: Use the skill only when the user intends to perform an IP or location lookup, and make clear that those providers can observe the request. <br>
Risk: IP geolocation can reflect a VPN, proxy, or network egress point rather than the user's precise physical location. <br>
Mitigation: Present the result as the public egress IP and broad location only, without treating it as a precise device location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daguniang/ip-lookup-tool) <br>
- [ipinfo.io JSON endpoint](https://ipinfo.io/json) <br>
- [ifconfig.co JSON endpoint](https://ifconfig.co/json) <br>
- [IP.SB GeoIP endpoint](https://api.ip.sb/geoip) <br>
- [OpenStreetMap Nominatim reverse geocoding](https://nominatim.openstreetmap.org/reverse) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON returned by a Node.js command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes public IP, city, optional Chinese city name, region, country, ISP or autonomous system, source, timestamp, and raw provider data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
