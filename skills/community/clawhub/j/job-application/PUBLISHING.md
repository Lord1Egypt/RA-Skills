# Publishing safety

The published package must contain only the skill code, templates, tests, and
fictional examples. It must never contain a real profile, photograph, signature,
application, generated PDF, or credential. The two bundled PDFs are fictional
regression examples.

## Runtime data locations

- Real profile: set `JOB_APPLICATION_PROFILE_DIR` to a directory outside this
  skill.
- Applications: set `JOB_APPLICATION_OUTPUT_DIR`, or set
  `JOB_APPLICATION_DATA_DIR` and use its `applications/` child. If neither is
  configured, the skill uses the platform's per-user data directory, not its
  installation directory.
- Signature images: reference them only from an external
  `application_content.json` via `cover_letter.signature_image`.

The bundled profile, including the Mira Hoffmann signature asset, and examples are fictional. `.gitignore` is a guard rail,
not the only safety control. In installations where this skill sits inside a
larger repository, ClawHub can discover that repository root. Always publish a
whitelist-only staging export instead of the installed directory itself. The
export script uses an explicit allowlist of source files and fictional example
assets; new public files must be added deliberately.

## Before every ClawHub publish

1. Keep the real profile, applications, photos, and signatures outside this
   folder.
2. Create a new or empty staging directory outside the repository, then export
   only the public allowlist:

   ```text
   python3 scripts/export_public_skill.py --output /tmp/job-application-clawhub
   ```

3. Preview the isolated staging directory:

   ```text
   clawhub skill publish /tmp/job-application-clawhub --dry-run
   ```

4. Reproduce the bundled fictional example from the staging directory:

   ```text
   python3 /tmp/job-application-clawhub/scripts/render_example.py --output /tmp/job-application-example
   ```

5. Inspect the preview and generated files. They must contain no real personal
   names, addresses, emails, phone numbers, photographs, signatures, CVs,
   cover letters, or credentials.
6. Only then publish the reviewed staging directory with an explicit version:

   ```text
   clawhub skill publish /tmp/job-application-clawhub --version <version>
   ```

The dry-run is deliberately part of the release process; do not rely on ignore
rules alone for private-data protection.
