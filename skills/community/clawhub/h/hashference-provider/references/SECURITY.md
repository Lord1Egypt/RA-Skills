# Security boundaries — version 1.0.1

## Confirmed issue fixed

The 1.0.0 helper accepted --output PATH. Exclusive creation protected existing files, but a nonexistent OpenClaw config path could still receive catalog data. Its documented output-path promise was therefore not enforced. This is a genuine implementation weakness, not merely a scanner misunderstanding.

1.0.1 removes direct filesystem output entirely. The CLI accepts no --output option (including abbreviations); arguments are parsed before reads/network access. Results go to stdout and diagnostics to stderr. Tests reject missing/existing config destinations and a directory-symlink destination, proving no file is created or changed. There is no output-path validator to evade because there is no filesystem-output capability.

Do not reconstruct the former behavior with shell redirection into a config path. Capture the text, inspect it, then use the host-approved provider configuration interface. The helper is not a config installer.

## Capabilities and limits

- Online: Python standard-library HTTPS request for the fixed public catalog URL. No authentication headers, credentials, account IDs, prompts or history. TLS verification uses Python's normal verified HTTPS handling. No downloaded code is executed.
- Offline: --input reads the explicitly chosen UTF-8-compatible public JSON file; it does not discover config files, scan directories or inspect environment variables. Select only intended catalog files.
- Output: stdout for data, stderr for counts/errors. No file creation/update/delete API, config writes or subprocess calls in the helper. Run Python with -B to suppress interpreter bytecode caches.
- Runtime: existing OpenClaw tool approvals are authoritative. This skill does not grant or preapprove tools. Setup/account/inference operations are separate from catalog discovery and require their stated user authorization and host-enforced secret/config access.
- No package installation, persistence hook, miner, shell-startup edits or automatic paid inference is bundled.
- A caller that redirects stdout controls that destination outside the helper; the helper cannot police shell redirection or sandbox an unrestricted host. These instructions do not claim such isolation.

## Scanner findings triage

The full 1.0.0 review reported an output-path issue that its secondary review confirmed; fixed above. Other raw findings were explicitly disagreed with by its secondary review:

- Safety-preserving wording containing the phrase “Never bypass policy” was matched as an anti-refusal instruction. The requirement remains, rewritten positively as using host-approved interfaces and retaining approvals.
- Tests used subprocess.run with a fixed argument list and no shell. They now exercise main(argv) in-process with captured streams and mocked I/O, reducing unnecessary process execution while preserving CLI coverage.
- Missing allowed-tools was flagged. We document actual capabilities rather than invent broad preapproved permissions; this skill grants none. Any host-specific tool allowlist remains the operator's decision.
- Standard MIT-0 license warranty language was matched as scope creep. The standard license is retained unchanged; it is legal text, not an agent instruction.

No scanner-specific suppression or scanner-directed instructions are included. Regression tests prove implementation behavior; only the registry's completed scan can establish its verdict for this version. A successful upload or preliminary clean moderation is not that final verdict.
