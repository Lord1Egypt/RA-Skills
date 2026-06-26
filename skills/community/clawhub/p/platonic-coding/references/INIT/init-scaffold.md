# Scaffold Project

Create the Platonic Coding infrastructure for a project.

## Objective

Set up the directory structure, configuration file, RFC infrastructure, and templates needed for Platonic Coding.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| Project name | Yes | — | Name of the project |
| Project root | Yes | Current directory | Root directory of the project |
| Language | No | Auto-detect | Primary programming language |
| Framework | No | Auto-detect | Framework if applicable |
| Specs path | No | `docs/specs` | Path for RFC specifications |
| Impl path | No | `docs/impl` | Path for implementation guides |
| Drafts path | No | `docs/drafts` | Path for design drafts |

## Steps

### Step 1: Gather Project Information

If not provided:

1. **Auto-detect language** from build files:
   - `Cargo.toml` → Rust
   - `package.json` → JavaScript/TypeScript
   - `pyproject.toml` / `setup.py` / `requirements.txt` → Python
   - `go.mod` → Go
   - `pom.xml` / `build.gradle` → Java
   - `*.csproj` / `*.sln` → C#
2. **Auto-detect framework** from dependencies in build files
3. **Ask user** for project name if not provided

### Step 2: Create .platonic.yml

1. Read `assets/templates/template-platonic.yml`
2. Replace placeholders:
   - `{{PROJECT_NAME}}` → project name
   - `{{PROJECT_DESCRIPTION}}` → description (ask user or leave as placeholder)
   - `{{LANGUAGE}}` → detected or provided language
   - `{{FRAMEWORK}}` → detected or provided framework
   - `{{DATE}}` → today's date
3. Write to `<project-root>/.platonic.yml`
4. **Skip if file already exists** (read existing config instead)

### Step 3: Create Specs Directory

1. Create `<specs-path>/` directory
2. Read and process RFC infrastructure templates from `assets/templates/`:
   - `template-rfc-standard.md` → `rfc-standard.md`
   - `template-rfc-history.md` → `rfc-history.md`
   - `template-rfc-index.md` → `rfc-index.md`
   - `template-rfc-namings.md` → `rfc-namings.md`
3. Replace `{{PROJECT_NAME}}` in each template
4. Write output files to specs directory
5. **Skip files that already exist**

### Step 4: Create Spec Templates

1. Create `<specs-path>/templates/` directory
2. Copy template files from `assets/specs/`:
   - `rfc-template.md` → `templates/rfc-template.md`
   - `template-conceptual-design.md` → `templates/conceptual-design.md`
   - `template-architecture-design.md` → `templates/architecture-design.md`
   - `template-impl-interface-design.md` → `templates/impl-interface-design.md`
3. Replace `{{PROJECT_NAME}}` in each template (except rfc-template.md which is generic)
4. **Skip files that already exist**

### Step 5: Create Impl Directory

1. Create `<impl-path>/` directory
2. Read `assets/templates/template-impl-readme.md`
3. Replace `{{PROJECT_NAME}}` → project name
4. Write to `<impl-path>/README.md`
5. **Skip if file already exists**

### Step 6: Create Drafts Directory

1. Create `<drafts-path>/` directory
2. Read `assets/templates/template-drafts-readme.md`
3. Replace `{{PROJECT_NAME}}` → project name
4. Write to `<drafts-path>/README.md`
5. **Skip if file already exists**

### Step 7: Verify

Confirm all expected files exist:
- `.platonic.yml`
- `<specs-path>/rfc-standard.md`
- `<specs-path>/rfc-history.md`
- `<specs-path>/rfc-index.md`
- `<specs-path>/rfc-namings.md`
- `<specs-path>/templates/` (4 template files)
- `<impl-path>/README.md`
- `<drafts-path>/README.md`

Report any files that were skipped (already existed) vs. newly created.

## Template Processing Rules

- `{{PROJECT_NAME}}`: Replace with exact project name (case-sensitive)
- `{{DATE}}`: Replace with current date in YYYY-MM-DD format
- `{{LANGUAGE}}`: Replace with detected/provided language (lowercase)
- `{{FRAMEWORK}}`: Replace with detected/provided framework (lowercase), or empty string
- Preserve all other content exactly as in templates
- Maintain markdown formatting and structure

## Notes

- If a file already exists, **skip it** (never overwrite without explicit user permission)
- Use exact capitalization provided for project name
- Create parent directories as needed
- The specs templates directory contains copies of the spec-kind templates for user reference and customization
