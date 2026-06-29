## Description: <br>
Search and browse the MusicBrainz music encyclopedia, fetch Cover Art Archive images, resolve musicbrainz.org URLs, and, with OAuth configured, submit user-approved tags, ratings, and collection edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up music metadata, discographies, MusicBrainz identifiers, release details, and cover art. Users with configured MusicBrainz OAuth credentials can also prepare and approve account-specific tag, rating, and collection edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Account edit tools can modify the user's MusicBrainz tags, ratings, or collections when OAuth credentials are configured. <br>
Mitigation: Use the dry-run preview first and only repeat the write action with confirm:true after the user reviews and approves the change. <br>
Risk: OAuth credentials are required for write actions and should be treated as sensitive. <br>
Mitigation: Configure credentials only in trusted environments and avoid using write tools unless the account action is intentional. <br>


## Reference(s): <br>
- [MusicBrainz](https://musicbrainz.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance] <br>
**Output Format:** [Markdown and structured tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only lookups do not require credentials; account edits require MusicBrainz OAuth credentials and explicit confirm:true approval after a dry-run preview.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
