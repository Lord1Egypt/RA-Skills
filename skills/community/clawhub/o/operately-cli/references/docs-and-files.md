# Docs & Files

Docs & Files is the knowledge base within spaces and projects. Teams organize documents, files, links, and folders in a hierarchical structure.

## Concept

**What is Docs & Files?**

Each space, project, and goal has a Docs & Files hub that provides:
- Central location for team documentation
- Hierarchical folder organization
- Document management (markdown)
- File attachments (binary uploads)
- Link collection
- Access control inherited from the parent space or project

**Key characteristics:**
- One Docs & Files hub per space, project, or goal
- Nested folder hierarchy (unlimited depth, but keep it shallow for usability)
- Documents, files, and links can live in folders
- Markdown support for documents
- All CLI commands live under the **`documents`** namespace

## Scope Rules

Hub-scoped create and list commands require **`--space-id`**, **`--project-id`**, or **`--goal-id`** (mutually exclusive — provide one, not both).

```bash
# Space-scoped
operately documents create_document --space-id s1 --name "Guide" --content "# Guide"

# Project-scoped
operately documents create_document --project-id p1 --name "Spec" --content "# Spec"

# Goal-scoped
operately documents create_document --goal-id g1 --name "Playbook" --content "# Playbook"
```

**Folder-scoped listing** works with **`--folder-id` alone** — no space or project ID needed:

```bash
operately documents list_contents --folder-id f1
```

**Do not** resolve a hub ID via `spaces list_tools`. Pass the space or project ID directly on `documents/*` commands.

## Folder Operations

### Creating Folders

**Create folder at root level:**
```bash
operately documents create_folder \
  --space-id s1 \
  --name "Guides"
```

**Create nested folder:**
```bash
operately documents create_folder \
  --space-id s1 \
  --folder-id f1 \
  --name "Onboarding"
```

**Create deep hierarchy:**
```bash
# Level 1: Guides
operately documents create_folder \
  --space-id s1 \
  --name "Guides"

# Level 2: Onboarding (inside Guides)
operately documents create_folder \
  --space-id s1 \
  --folder-id guides_folder_id \
  --name "Onboarding"

# Level 3: Engineering (inside Onboarding)
operately documents create_folder \
  --space-id s1 \
  --folder-id onboarding_folder_id \
  --name "Engineering Onboarding"
```

### Folder Operations

**Get folder details:**
```bash
operately documents get_folder --id f1
```

**Rename folder:**
```bash
operately documents rename_folder \
  --folder-id f1 \
  --new-name "Team Guides"
```

**Delete folder:**
```bash
operately documents delete_folder --folder-id f1
```

**Copy folder:**
```bash
operately documents copy_folder \
  --folder-id f1 \
  --folder-name "Copied Guides" \
  --dest-parent-folder-id f2
```

## Documents

### Creating Documents

**Create document at root:**
```bash
operately documents create_document \
  --space-id s1 \
  --name "Getting Started" \
  --content "# Getting Started\n\nWelcome to the team! This guide will help you get up to speed.\n\n## First Steps\n1. Set up your development environment\n2. Read the architecture docs\n3. Join the team channels"
```

**Create document in folder:**
```bash
operately documents create_document \
  --space-id s1 \
  --folder-id f1 \
  --name "Development Setup" \
  --content "# Development Environment Setup\n\n## Prerequisites\n- Node.js 18+\n- Docker\n- Git\n\n## Installation\n\`\`\`bash\nnpm install\ndocker-compose up\n\`\`\`"
```

**Create draft document:**
```bash
operately documents create_document \
  --space-id s1 \
  --folder-id f1 \
  --name "Work in Progress" \
  --content "# Draft Document\n\nThis is still being written..." \
  --post-as-draft true
```

**Create document with notifications:**
```bash
operately documents create_document \
  --space-id s1 \
  --name "Important Announcement" \
  --content "# New Policy\n\nPlease review the updated security policy." \
  --send-notifications-to-everyone true
```

**Create document with specific subscribers:**
```bash
operately documents create_document \
  --space-id s1 \
  --name "Team Update" \
  --content "# Q2 Plans" \
  --subscriber-ids u1 \
  --subscriber-ids u2 \
  --subscriber-ids u3
```

### Managing Documents

**Get document:**
```bash
operately documents get_document --id d1
```

**Update document:**
```bash
operately documents update_document \
  --document-id d1 \
  --name "Updated Guide" \
  --content "# Updated Content\n\nRevised with latest information."
```

**Publish draft:**
```bash
operately documents publish_document --document-id d1
```

**Delete document:**
```bash
operately documents delete_document --document-id d1
```

## Files

Use `documents create_file` for PDFs, images, spreadsheets, and other binary attachments. The CLI takes a local path and handles blob creation, upload, preview generation for images, and finalization automatically.

**Important file rules:**
- `operately documents create_file` uploads exactly one `--file <path>` per command.
- `--name` changes the stored base name but keeps the source extension.
- `--description` or `--description-file` sets the file description; it does not replace the uploaded binary.

**Create file at root:**
```bash
operately documents create_file \
  --space-id s1 \
  --file ./architecture.pdf
```

**Create file in folder with custom name and description:**
```bash
operately documents create_file \
  --space-id s1 \
  --folder-id f1 \
  --file ./quarterly-report.pdf \
  --name "Quarterly Report" \
  --description-file ./quarterly-report.md
```

**Create file with targeted notifications:**
```bash
operately documents create_file \
  --project-id p1 \
  --file ./launch-plan.png \
  --send-notifications-to-everyone false \
  --subscriber-ids u1 \
  --subscriber-ids u2
```

**Get file:**
```bash
operately documents get_file --id file1
```

**Update file metadata:**
```bash
operately documents update_file \
  --file-id file1 \
  --name "Quarterly Report.pdf" \
  --description "# Updated Notes\n\nAttached the final version."
```

**Delete file:**
```bash
operately documents delete_file --file-id file1
```

## Links

### Creating Links

**Create link at root:**
```bash
operately documents create_link \
  --space-id s1 \
  --name "Company Handbook" \
  --url "https://handbook.example.com" \
  --type "other"
```

**Create link in folder:**
```bash
operately documents create_link \
  --space-id s1 \
  --folder-id f1 \
  --name "Design System" \
  --url "https://design.example.com" \
  --type "other" \
  --description "# Design System\n\nOur component library and design guidelines."
```

**Create link with notifications:**
```bash
operately documents create_link \
  --space-id s1 \
  --name "New Tool" \
  --url "https://tool.example.com" \
  --type "other" \
  --description "Check out our new project management tool" \
  --send-notifications-to-everyone true
```

### Managing Links

**Get link:**
```bash
operately documents get_link --id l1
```

**Update link:**
```bash
operately documents update_link \
  --link-id l1 \
  --name "Updated Link Title" \
  --type "other" \
  --url "https://new-url.example.com" \
  --description "Updated description"
```

**Delete link:**
```bash
operately documents delete_link --link-id l1
```

## Moving Items Between Folders

### Move Document

```bash
operately documents update_parent_folder \
  --resource-id d1 \
  --resource-type "document" \
  --new-folder-id f2
```

### Move File

```bash
operately documents update_parent_folder \
  --resource-id file1 \
  --resource-type "file" \
  --new-folder-id f2
```

### Move Link

```bash
operately documents update_parent_folder \
  --resource-id l1 \
  --resource-type "link" \
  --new-folder-id f2
```

### Move Folder

```bash
operately documents update_parent_folder \
  --resource-id f1 \
  --resource-type "folder" \
  --new-folder-id f2
```

### Move to Root

```bash
# Move to root by setting new-folder-id to null
operately documents update_parent_folder \
  --resource-id d1 \
  --resource-type "document" \
  --new-folder-id null
```

## Listing and Navigating Contents

### List Root Contents

```bash
operately documents list_contents --space-id s1
```

### List Folder Contents

```bash
operately documents list_contents --folder-id f1
```

### List with Metadata

```bash
operately documents list_contents \
  --space-id s1 \
  --include-comments-count \
  --include-children-count
```

If `comments_count` or `children_count` is missing from the response, treat that as "metadata not requested" unless the matching include flag was passed.

## Project-Scoped Docs & Files

Projects have their own Docs & Files hub. Use `--project-id` instead of `--space-id`:

```bash
# List project hub contents
operately documents list_contents --project-id p1

# Add a spec document
operately documents create_document \
  --project-id p1 \
  --name "Technical Spec" \
  --content "# Spec\n\nArchitecture overview..."

# Upload a PDF
operately documents create_file \
  --project-id p1 \
  --file ./spec.pdf
```

## Common Patterns

### Team Knowledge Base Pattern

```bash
# 1. Create folder structure
operately documents create_folder \
  --space-id s1 \
  --name "Onboarding"

operately documents create_folder \
  --space-id s1 \
  --name "Architecture"

operately documents create_folder \
  --space-id s1 \
  --name "Processes"

operately documents create_folder \
  --space-id s1 \
  --name "Tools & Resources"

# 2. Add onboarding documents
operately documents create_document \
  --space-id s1 \
  --folder-id onboarding_folder \
  --name "Day 1 Guide" \
  --content "# Welcome!\n\n## Your First Day\n- Meet the team\n- Set up accounts\n- Review codebase"

operately documents create_document \
  --space-id s1 \
  --folder-id onboarding_folder \
  --name "Development Setup" \
  --content "# Dev Environment\n\n[setup instructions]"

# 3. Add architecture docs
operately documents create_document \
  --space-id s1 \
  --folder-id architecture_folder \
  --name "System Overview" \
  --content "# Architecture\n\n[system design]"

# 4. Add tool links
operately documents create_link \
  --space-id s1 \
  --folder-id tools_folder \
  --name "CI/CD Dashboard" \
  --url "https://ci.example.com" \
  --type "other"
```

### Project Documentation Pattern

```bash
# 1. Create project phases as folders
operately documents create_folder \
  --project-id p1 \
  --name "Discovery"

operately documents create_folder \
  --project-id p1 \
  --name "Design"

operately documents create_folder \
  --project-id p1 \
  --name "Development"

operately documents create_folder \
  --project-id p1 \
  --name "Launch"

# 2. Add phase-specific content
operately documents create_document \
  --project-id p1 \
  --folder-id discovery_folder \
  --name "User Research Findings" \
  --content "# Research Summary\n\n[findings]"

operately documents create_link \
  --project-id p1 \
  --folder-id design_folder \
  --name "Figma Mockups" \
  --url "https://figma.com/file/abc" \
  --type "other"
```

### Policy & Procedures Pattern

```bash
# 1. Create policy categories
operately documents create_folder \
  --space-id s1 \
  --name "HR Policies"

operately documents create_folder \
  --space-id s1 \
  --name "Security Policies"

operately documents create_folder \
  --space-id s1 \
  --name "Engineering Processes"

# 2. Add policies
operately documents create_document \
  --space-id s1 \
  --folder-id hr_folder \
  --name "Time Off Policy" \
  --content "# Time Off\n\n## Vacation\n- 20 days per year\n- Request 2 weeks in advance"

operately documents create_document \
  --space-id s1 \
  --folder-id security_folder \
  --name "Access Control Policy" \
  --content "# Access Control\n\n## Principles\n- Least privilege\n- Regular reviews\n- MFA required"
```

## Gotchas

### One Hub per Space or Project

Each space and each project has one Docs & Files hub. Scope commands with `--space-id` or `--project-id` — do not look up hub IDs.

### Folder Hierarchy Depth

There is no technical limit on folder depth, but keep it shallow (3–4 levels max) for usability:
- Level 1: Main categories (Onboarding, Architecture, Processes)
- Level 2: Subcategories (Frontend, Backend, DevOps)
- Level 3: Specific topics (React Guide, API Design)
- Level 4: Detailed docs (rarely needed)

### Moving Items

When moving items between folders, the `resource-type` must be exact:
- `"document"` for documents
- `"file"` for files
- `"link"` for links
- `"folder"` for folders

### Deleting Folders

Deleting a folder will delete its contents (documents, links, subfolders). Check the folder contents first:

```bash
operately documents list_contents --folder-id f1
```

Move important items before deleting:

```bash
# Move items out first
operately documents update_parent_folder \
  --resource-id d1 \
  --resource-type "document" \
  --new-folder-id safe_folder_id

# Then delete folder
operately documents delete_folder --folder-id f1
```

### Document Drafts

Draft documents are visible to editors but not published to the team. Use drafts for work-in-progress:

```bash
# Create draft
operately documents create_document \
  --space-id s1 \
  --name "WIP: New Policy" \
  --content "# Draft\n\nStill writing..." \
  --post-as-draft true

# Publish when ready
operately documents publish_document --document-id d1
```

### Link Types

The `--type` parameter for links is required. Valid values:
- `airtable`
- `dropbox`
- `figma`
- `google`
- `google_doc`
- `google_sheet`
- `google_slides`
- `notion`
- `other`

### Markdown in Documents

Documents support full markdown including:
- Headings (`# H1`, `## H2`, etc.)
- Lists (`-` or `1.`)
- Links (`[text](url)`)
- Code blocks (` ``` `)
- Bold (`**text**`) and italic (`*text*`)

Use markdown for rich, readable documentation. For larger documents, use `--content-file <path>` to load markdown from disk:

```bash
operately documents create_document \
  --space-id s1 \
  --name "API Guide" \
  --content-file ./api-guide.md
```

### Notifications

Use `--send-notifications-to-everyone` sparingly. For targeted notifications, use `--subscriber-ids`:

```bash
# Notify specific people
operately documents create_document \
  --space-id s1 \
  --name "Team Update" \
  --content "# Update" \
  --subscriber-ids u1 \
  --subscriber-ids u2
```

### Searching Content

**Full-text company search** (preferred for content discovery):

```bash
operately companies search --query "onboarding" --sort best_match
operately companies search --query "roadmap" --space-ids s1 --types resource_hub_document --sort most_recent
```

**Scoped Docs & Files search** (exactly one of `--space-id`, `--project-id`, or `--goal-id`):

```bash
operately documents search --space-id s1 --query "onboarding"
operately documents search --goal-id g1 --query "metrics"
```

**Quick/broad lookup** (compatibility; includes discussions, folders, documents, files, links):

```bash
operately companies global_search --query "onboarding"
operately companies quick_search --query "roadmap"
```

For template blueprint resources, use `project_templates` commands — not live `documents/*`. See [Project Template Workflows](project-template-workflows.md).

### Document Version History

```bash
# List versions
operately documents list_document_versions --document-id d1

# Read a specific version
operately documents get_document_version --document-id d1 --version-number 3

# Restore a previous version
operately documents restore_document_version --document-id d1 --version-number 3 --expected-current-version 5
```

When updating a document, pass `--expected-version` to detect concurrent edits:

```bash
operately documents update_document \
  --document-id d1 \
  --name "Updated Guide" \
  --content "# Updated\n\nNew content." \
  --expected-version 5
```

If another edit landed first, the CLI returns a version conflict — re-fetch the document and retry.

### Legacy CLI Commands (CLI ≤ 1.6)

Older CLI versions used separate `resource_hubs/*`, `files/*`, and `links/*` namespaces with `--resource-hub-id`. Those routes still exist on the API for backward compatibility but are hidden from the current CLI catalog. Always use the `documents/*` commands documented above.
