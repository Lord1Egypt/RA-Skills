# Language Tutor Pro — Security

## Data Handling

Language Tutor Pro stores learner data (vocabulary, grammar progress, session transcripts, and profile information) in local files within the skill's `data/` directory. This data is used exclusively to provide persistent learning across sessions.

### What Is Stored

- Learner profile: native language, target language, level, goals, interests
- Vocabulary ledger: words learned, SRS scheduling data, context sentences
- Grammar tracker: rules practiced, error counts, mastery status
- Session logs: date, type, duration, errors corrected, new vocabulary
- Conversation transcripts: full text of practice sessions

### What Is NOT Stored

- No authentication credentials
- No payment information
- No personally identifiable information beyond what you put in your learner profile
- No telemetry or usage analytics sent to any external service

## Agent Runtime

Language Tutor Pro is an agent skill — it runs within your OpenClaw agent's context. The security properties of your learning data depend entirely on:

- How your OpenClaw instance is configured
- Which LLM backend processes your conversations
- Where your agent's workspace files are stored
- Your host machine's security posture

**This skill does not make guarantees about where your data goes or who can access it.** It stores files locally, but the agent runtime, LLM API calls, and your infrastructure configuration determine the actual data flow.

## Recommendations

- Review your OpenClaw agent's LLM backend configuration to understand where conversation text is sent
- If using cloud-hosted LLM APIs, be aware that conversation content is transmitted to those providers
- The `data/` directory contains your full learning history — protect it as you would any personal files
- The `scripts/export-progress.sh` script generates a JSON summary; treat exported files with the same care

## Scripts

All scripts in `scripts/` are bash scripts that operate only on local files within the skill directory. They do not make network requests or access external services. Review them before running if you have concerns:

- `setup.sh` — creates data directories and initializes the learner profile
- `export-progress.sh` — reads data files and writes a JSON summary
- `vocab-review.sh` — reads vocabulary data and outputs due items (no writes)

## Reporting Issues

If you discover a security concern with this skill, contact: support@normieclaw.ai
