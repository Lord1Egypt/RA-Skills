## Description: <br>
Find high-quality Instagram photos for any destination or place. Searches for Instagram posts via web search, downloads candidate images, vision-scores them for quality and iconic-ness, and returns the best matches with source URLs. Use when you need travel/destination photos from Instagram, hero images for a location, or Instagram post images for any place or attraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and content teams use this skill to find scenic public Instagram post images for destinations, places, attractions, or travel-focused hero imagery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may download untrusted public images into /tmp for vision scoring. <br>
Mitigation: Use it only for public content you are comfortable fetching and processing, and delete temporary image files after use if retention is not desired. <br>
Risk: Image scoring may select misleading, low-quality, or non-representative destination photos. <br>
Mitigation: Review the returned descriptions, scores, source URLs, and local files before reusing any image. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/psyduckler/instagram-photo-find) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown text with ranked results, source URLs, local file paths, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns score, brief description, Instagram post URL, and local /tmp file path for each selected image.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
