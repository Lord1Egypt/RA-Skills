## Description: <br>
A free music discovery app that uses unauthenticated music APIs for search, lyrics, internet radio, artist metadata, and concert information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this local web app to search music, view lyrics, browse internet radio, and query artist events through a Next.js frontend and FastAPI backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music searches, artist names, song titles, radio queries, and event lookups are sent to external music services. <br>
Mitigation: Use the app only where those outbound requests are acceptable, review the listed services, and avoid entering sensitive information. <br>
Risk: The backend may be exposed beyond the local machine if run or deployed on a public interface. <br>
Mitigation: Bind the backend to localhost unless network exposure is intended, set explicit CORS origins, and place any public deployment behind appropriate network controls. <br>
Risk: TLS configuration can be weakened if certificate checks are disabled in production settings. <br>
Mitigation: Use valid certificates and required verification for production; do not enable TLS settings that disable certificate checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fish1981bimmer/music-discovery-app) <br>
- [iTunes Search API documentation](https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/) <br>
- [Lyrics.ovh API documentation](https://lyricsovh.docs.apiary.io/) <br>
- [MusicBrainz](https://musicbrainz.org/) <br>
- [Radio Browser API](https://api.radio-browser.info/) <br>
- [Bandsintown](https://www.bandsintown.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with application source files, API configuration, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local web app that makes outbound requests to third-party music services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontend package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
