## Description:

ObsPy allows you to easily download earthquake data from various data centers/networks through its client API. This is an overview of available services and a demo of the client API for International Federation of Digital Seismograph Networks (FDSN). Use this if you need to download earthquake research data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and seismology researchers use this skill to get guidance and examples for downloading seismic waveforms, event data, and station metadata from FDSN-compatible data centers with ObsPy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the documented ObsPy client examples can send data-query parameters to external FDSN routing services and data centers.

Mitigation: Avoid putting sensitive or private information in query fields, and review destination services before running examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ink5725/skills/obspy-datacenter-client)
- [obspy-clients-fdsn.md](obspy-clients-fdsn.md)
- [FDSN Web Services](https://www.fdsn.org/webservices/)
- [FDSN Data Centers](https://www.fdsn.org/webservices/datacenters/)
- [IRIS Federator](https://service.iris.edu/irisws/fedcatalog/1/)
- [EIDAWS Routing Service](http://www.orfeus-eu.org/data/eida/webservices/routing/)
- [Earthworm](http://www.earthwormcentral.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Python examples and explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; example API calls may contact external FDSN routing services and data centers when run by a user.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
