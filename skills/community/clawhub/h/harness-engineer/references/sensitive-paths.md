# SENSITIVE PATH POLICY

Agents must not read, list, log, or store the contents of files that typically
contain credentials, authentication material, or infrastructure secrets.
This policy is enforced in the skill. Platform enforcement is an additional layer,
not the primary control.

---

## FORBIDDEN READ PATHS

The following path categories are off-limits to ALL agents, including the researcher.
A matching path must be skipped silently and noted as "excluded -- sensitive" in output.

### Credential and authentication material
  .env and .env.* variants (local, production, staging, etc.)
  .envrc
  Certificate files (*.pem, *.key, *.p12, *.pfx, *.cer, *.crt)
  SSH material (id_rsa, id_ed25519, id_ecdsa, authorized_keys, known_hosts)
  Files with "secret" or "credentials" in the filename
  Any file matching patterns typically used for authentication tokens

### CI/CD and infrastructure configuration
  CI workflow files (.github/workflows/*.yml, .gitlab-ci.yml, .circleci/config.yml, etc.)
  Infrastructure state files (terraform.tfvars, *.tfstate, *.tfstate.backup)
  Vault configuration (.vault-token, vault*.hcl)

### Git internals
  .git/config (may contain embedded credentials in remote URLs)
  .git/credentials
  .git/hooks/* (executable files -- do not read)

### Package manager authentication
  .npmrc, .pypirc, .netrc (may contain registry tokens)

### Application configuration that commonly embeds credentials
  Database and secrets configuration files
  Encrypted credentials files and their master keys
  Framework configuration with embedded secrets (Spring Boot, Django, Rails)

---

## ALLOWED READS (examples of what IS safe to read)

  src/**/*.ts, src/**/*.py, src/**/*.go   (source code)
  tests/**                                (test files)
  docs/**                                 (documentation)
  *.md                                    (markdown)
  package.json, pyproject.toml            (dependency manifests -- not lock files with hashes)
  tsconfig.json, .eslintrc                (tool config -- no secrets)
  Dockerfile                              (review for secrets before reading)
  docker-compose.yml                      (review for secret references before reading)

---

## RESEARCHER EXCLUSION PROTOCOL

When the researcher orchestrator scans the file structure (Phase A Step 1):

1. Run list_dir on each directory
2. Before dispatching a sub-researcher to any directory, filter its file list:
   - Remove any file matching the FORBIDDEN READ PATHS patterns above
   - Include the filtered list in the sub-researcher's scope
3. Note excluded files in RESEARCH-NNN.md under a "Excluded -- sensitive" section
4. Do NOT include the count or names of excluded files in any log that an agent
   stores in MEMORY.md (the existence of a .env file is itself sensitive context)

When a sub-researcher encounters a path matching FORBIDDEN READ PATHS mid-scan:
  - Skip it immediately
  - Do not log its contents or any value from it
  - Add one line to the Module Report: "Excluded: <pattern matched> -- sensitive path policy"

---

## CI/CD CONFIG EXCEPTION

CI/CD config files (GitHub Actions, GitLab CI, etc.) may be read for structural
analysis ONLY -- to understand the pipeline shape, not to extract values.
Rules for reading CI configs:
  - Read only the structural keys (job names, step names, trigger conditions)
  - Immediately discard any environment variable or secrets sections from working memory
  - Do not log, store, or record any value from those sections
  - Do not pass CI config contents to MEMORY.md or tool-logs

---

## MEMORY REDACTION RULE

Before writing any entry to MEMORY.md, RESEARCH-NNN.md, GAPS-NNN.md, or any
tracking log, the agent must verify the content does not contain:

  - A file path from the FORBIDDEN READ PATHS list
  - Any value that resembles a credential or authentication token
  - Any content extracted from a file in the forbidden categories

If uncertain: omit the value and write "redacted -- possible sensitive content".
