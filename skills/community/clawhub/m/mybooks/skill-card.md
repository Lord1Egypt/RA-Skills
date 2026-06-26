## Description: <br>
MyBooks helps agents manage a personal MyBooks or Talebook library, including library statistics, book search and details, metadata edits, online metadata fill, ebook upload, ISBN-based physical book entry, reading states, favorites, categories, authors, and sending books to email or supported reading devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poxenstudio](https://clawhub.ai/user/poxenstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent query, organize, update, upload, and distribute books in a configured MyBooks personal library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MyBooks host, username, and password credentials. <br>
Mitigation: Provide credentials through session-level environment variables or a dedicated secrets manager, and avoid shared or global environment files. <br>
Risk: The skill can upload local ebook files and send books to email addresses or reading devices. <br>
Mitigation: Verify the exact local file path, book ID, recipient email, and device URL before allowing upload or send actions. <br>
Risk: The skill sends authenticated requests to the configured MYBOOKS_HOST server. <br>
Mitigation: Use the skill only with a MyBooks server the user trusts. <br>


## Reference(s): <br>
- [MyBooks homepage](https://www.mybooks.top) <br>
- [ClawHub skill page](https://clawhub.ai/poxenstudio/mybooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and MYBOOKS_HOST, MYBOOKS_USER, and MYBOOKS_PASSWORD environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
