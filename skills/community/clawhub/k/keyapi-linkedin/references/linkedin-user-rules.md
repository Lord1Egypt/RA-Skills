# LinkedIn User Module Rules

## 1. Module Scope

Use this module for people search, profile baseline, about/contact information, career background, skills, credentials, social proof, user posts/comments/media, and interest context.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## 2. People search and profile baseline

- Documentation: `https://docs.keyapi.ai/en/linkedin/search_people.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_profile.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_about.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_follower_and_connection.md`
- Purpose: Find professionals and build a reliable profile baseline before section-specific enrichment.

### Best Suited For

- prospect or candidate discovery
- profile validation
- headline/about/follower context
- shortlist enrichment

### Routing Rules

- Use search people when the exact profile target is unknown.
- Use user profile for baseline information before calling many adjacent sections.
- Use about and follower/connection endpoints only when that context is needed.
- Avoid calling every profile section unless the user asks for a full report.

## 3. Contact and outreach context

- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_contact.md`
- Purpose: Retrieve documented contact information for a selected LinkedIn user.

### Best Suited For

- sales or recruiting outreach preparation
- contact field verification
- profile enrichment

### Routing Rules

- Use only after the person target is identified.
- Do not infer missing contact information.
- Keep contact fields separate from public profile/about facts.

## 4. Career background and credentials

- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_experience.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_educations.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_skills.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_certifications.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_publications.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_honors.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_recommendations.md`
- Purpose: Retrieve structured career, education, skill, and credibility sections.

### Best Suited For

- candidate qualification
- expertise verification
- background reports
- speaker or advisor research

### Routing Rules

- Call only the sections requested or clearly useful for the user goal.
- Group output by section rather than mixing credentials with activity.
- Use profile baseline first if the user identity is ambiguous.

## 5. Activity, media, and interests

- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_posts.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_comments.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_videos.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_images.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_interests_companies.md`
- Documentation: `https://docs.keyapi.ai/en/linkedin/get_user_interests_groups.md`
- Purpose: Analyze user content activity and ecosystem interests.

### Best Suited For

- thought leadership review
- recent activity checks
- content/media audit
- interest and affiliation context

### Routing Rules

- Use posts/comments/videos/images based on the requested activity surface.
- Use interests only when the user asks for companies/groups or ecosystem context.
- Enrich only selected posts/media unless a broader content audit is approved.

## 6. Common Workflows

- People qualification: search people -> user profile -> about/follower-contact sections as needed.
- Candidate/background report: profile -> experience/education/skills/certs/publications/honors/recommendations.
- Activity report: profile -> posts/comments/media -> selected content summary.
