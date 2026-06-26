# Resource Hubs

Resource hubs are knowledge repositories within spaces where teams can organize documents, links, and folders in a hierarchical structure.

## Resource Hub Concept

**What is a Resource Hub?**

A resource hub is a structured knowledge base that belongs to a space. It provides:
- Central location for team documentation
- Hierarchical folder organization
- Document management
- File attachments
- Link collection
- Access control

**Key Characteristics:**
- Every space has one resource hub
- Nested folder hierarchy (unlimited depth)
- Documents, files, and links can be organized in folders
- Markdown support for documents
- Access levels inherited from space or customized

## Finding a Space's Resource Hub

Every space already has a resource hub. To find the resource hub ID for a space:

```bash
operately spaces list_tools --space-id s1
```

Use the returned resource hub ID below as `rh1`. Use `operately files create` when you need to upload a local binary file into the hub.

### Getting Resource Hub

```bash
operately resource_hubs get --id rh1
```

## Folder Organization

### Creating Folders

**Create folder at root level:**
```bash
operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Guides"
```

**Create nested folder:**
```bash
operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --folder-id f1 \
  --name "Onboarding"
```

**Create deep hierarchy:**
```bash
# Level 1: Guides
operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Guides"

# Level 2: Onboarding (inside Guides)
operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --folder-id guides_folder_id \
  --name "Onboarding"

# Level 3: Engineering (inside Onboarding)
operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --folder-id onboarding_folder_id \
  --name "Engineering Onboarding"
```

### Folder Operations

**Get folder details:**
```bash
operately resource_hubs get_folder --id f1
```

**Rename folder:**
```bash
operately resource_hubs rename_folder \
  --folder-id f1 \
  --new-name "Team Guides"
```

**Delete folder:**
```bash
operately resource_hubs delete_folder --folder-id f1
```

**Copy folder:**
```bash
operately resource_hubs copy_folder \
  --folder-id f1 \
  --dest-resource-hub-id rh1 \
  --dest-parent-folder-id f2
```

## Documents

### Creating Documents

**Create document at root:**
```bash
operately documents create \
  --resource-hub-id rh1 \
  --name "Getting Started" \
  --content "# Getting Started\n\nWelcome to the team! This guide will help you get up to speed.\n\n## First Steps\n1. Set up your development environment\n2. Read the architecture docs\n3. Join the team channels"
```

**Create document in folder:**
```bash
operately documents create \
  --resource-hub-id rh1 \
  --folder-id f1 \
  --name "Development Setup" \
  --content "# Development Environment Setup\n\n## Prerequisites\n- Node.js 18+\n- Docker\n- Git\n\n## Installation\n\`\`\`bash\nnpm install\ndocker-compose up\n\`\`\`"
```

**Create draft document:**
```bash
operately documents create \
  --resource-hub-id rh1 \
  --folder-id f1 \
  --name "Work in Progress" \
  --content "# Draft Document\n\nThis is still being written..." \
  --post-as-draft true
```

**Create document with notifications:**
```bash
operately documents create \
  --resource-hub-id rh1 \
  --name "Important Announcement" \
  --content "# New Policy\n\nPlease review the updated security policy." \
  --send-notifications-to-everyone true
```

**Create document with specific subscribers:**
```bash
operately documents create \
  --resource-hub-id rh1 \
  --name "Team Update" \
  --content "# Q2 Plans" \
  --subscriber-ids u1 \
  --subscriber-ids u2 \
  --subscriber-ids u3
```

### Managing Documents

**Get document:**
```bash
operately documents get --id d1
```

**Update document:**
```bash
operately documents update \
  --document-id d1 \
  --name "Updated Guide" \
  --content "# Updated Content\n\nRevised with latest information."
```

**Publish draft:**
```bash
operately documents publish --document-id d1
```

**Delete document:**
```bash
operately documents delete --document-id d1
```

## Files

Use files for PDFs, images, spreadsheets, and other binary attachments that should live in a resource hub. The CLI takes a local path and handles blob creation, upload, preview generation for images, and finalization automatically.

**Important file rules:**
- `operately files create` uploads exactly one `--file <path>` per command.
- `--name` changes the stored base name but keeps the source extension.
- `--description` or `--description-file` sets the file description; it does not replace the uploaded binary.

**Create file at root:**
```bash
operately files create \
  --resource-hub-id rh1 \
  --file ./architecture.pdf
```

**Create file in folder with custom name and description:**
```bash
operately files create \
  --resource-hub-id rh1 \
  --folder-id f1 \
  --file ./quarterly-report.pdf \
  --name "Quarterly Report" \
  --description-file ./quarterly-report.md
```

**Create file with targeted notifications:**
```bash
operately files create \
  --resource-hub-id rh1 \
  --file ./launch-plan.png \
  --send-notifications-to-everyone false \
  --subscriber-ids u1 \
  --subscriber-ids u2
```

**Get file:**
```bash
operately files get --id file1
```

**Update file metadata:**
```bash
operately files update \
  --file-id file1 \
  --name "Quarterly Report.pdf" \
  --description "# Updated Notes\n\nAttached the final version."
```

**Delete file:**
```bash
operately files delete --file-id file1
```

## Links

### Creating Links

**Create link at root:**
```bash
operately links create \
  --resource-hub-id rh1 \
  --name "Company Handbook" \
  --url "https://handbook.example.com" \
  --type "other"
```

**Create link in folder:**
```bash
operately links create \
  --resource-hub-id rh1 \
  --folder-id f1 \
  --name "Design System" \
  --url "https://design.example.com" \
  --type "other" \
  --description "# Design System\n\nOur component library and design guidelines."
```

**Create link with notifications:**
```bash
operately links create \
  --resource-hub-id rh1 \
  --name "New Tool" \
  --url "https://tool.example.com" \
  --type "other" \
  --description "Check out our new project management tool" \
  --send-notifications-to-everyone true
```

### Managing Links

**Get link:**
```bash
operately links get --id l1
```

**Update link:**
```bash
operately links update \
  --link-id l1 \
  --name "Updated Link Title" \
  --type "other" \
  --url "https://new-url.example.com" \
  --description "Updated description"
```

**Delete link:**
```bash
operately links delete --link-id l1
```

## Moving Items Between Folders

### Move Document

```bash
operately resource_hubs update_parent_folder \
  --resource-id d1 \
  --resource-type "document" \
  --new-folder-id f2
```

### Move File

```bash
operately resource_hubs update_parent_folder \
  --resource-id file1 \
  --resource-type "file" \
  --new-folder-id f2
```

### Move Link

```bash
operately resource_hubs update_parent_folder \
  --resource-id l1 \
  --resource-type "link" \
  --new-folder-id f2
```

### Move Folder

```bash
operately resource_hubs update_parent_folder \
  --resource-id f1 \
  --resource-type "folder" \
  --new-folder-id f2
```

### Move to Root

```bash
# Move to root by setting new-folder-id to null
operately resource_hubs update_parent_folder \
  --resource-id d1 \
  --resource-type "document" \
  --new-folder-id null
```

## Listing and Navigating Contents

### List Root Contents

```bash
operately resource_hubs list_nodes --resource-hub-id rh1
```

### List Folder Contents

```bash
operately resource_hubs list_nodes --folder-id f1
```

### List with Metadata

```bash
operately resource_hubs list_nodes \
  --resource-hub-id rh1 \
  --include-comments-count \
  --include-children-count
```

If `comments_count` or `children_count` is missing from the response, treat that as “metadata not requested” unless the matching include flag was passed.

## Common Patterns

### Team Knowledge Base Pattern

```bash
# 1. Find the space's resource hub ID
operately spaces list_tools --space-id engineering_space
# Use the returned resource hub ID below as rh1

# 2. Create folder structure
operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Onboarding"

operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Architecture"

operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Processes"

operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Tools & Resources"

# 3. Add onboarding documents
operately documents create \
  --resource-hub-id rh1 \
  --folder-id onboarding_folder \
  --name "Day 1 Guide" \
  --content "# Welcome!\n\n## Your First Day\n- Meet the team\n- Set up accounts\n- Review codebase"

operately documents create \
  --resource-hub-id rh1 \
  --folder-id onboarding_folder \
  --name "Development Setup" \
  --content "# Dev Environment\n\n[setup instructions]"

# 4. Add architecture docs
operately documents create \
  --resource-hub-id rh1 \
  --folder-id architecture_folder \
  --name "System Overview" \
  --content "# Architecture\n\n[system design]"

# 5. Add tool links
operately links create \
  --resource-hub-id rh1 \
  --folder-id tools_folder \
  --name "CI/CD Dashboard" \
  --url "https://ci.example.com" \
  --type "other"
```

### Project Documentation Pattern

```bash
# 1. Find the space's resource hub ID
operately spaces list_tools --space-id product_space
# Use the returned resource hub ID below as rh1

# 2. Create project phases as folders
operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Discovery"

operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Design"

operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Development"

operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Launch"

# 3. Add phase-specific content
operately documents create \
  --resource-hub-id rh1 \
  --folder-id discovery_folder \
  --name "User Research Findings" \
  --content "# Research Summary\n\n[findings]"

operately links create \
  --resource-hub-id rh1 \
  --folder-id design_folder \
  --name "Figma Mockups" \
  --url "https://figma.com/file/abc" \
  --type "other"
```

### Policy & Procedures Pattern

```bash
# 1. Find the space's resource hub ID
operately spaces list_tools --space-id company_space
# Use the returned resource hub ID below as rh1

# 2. Create policy categories
operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "HR Policies"

operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Security Policies"

operately resource_hubs create_folder \
  --resource-hub-id rh1 \
  --name "Engineering Processes"

# 3. Add policies
operately documents create \
  --resource-hub-id rh1 \
  --folder-id hr_folder \
  --name "Time Off Policy" \
  --content "# Time Off\n\n## Vacation\n- 20 days per year\n- Request 2 weeks in advance"

operately documents create \
  --resource-hub-id rh1 \
  --folder-id security_folder \
  --name "Access Control Policy" \
  --content "# Access Control\n\n## Principles\n- Least privilege\n- Regular reviews\n- MFA required"
```

## Gotchas

### Resource Hub per Space

Each space has one resource hub. Find its ID with:

```bash
operately spaces list_tools --space-id s1
```

### Folder Hierarchy Depth

There's no technical limit on folder depth, but keep it shallow (3-4 levels max) for usability:
- Level 1: Main categories (Onboarding, Architecture, Processes)
- Level 2: Subcategories (Frontend, Backend, DevOps)
- Level 3: Specific topics (React Guide, API Design)
- Level 4: Detailed docs (rarely needed)

### Moving Items

When moving items between folders, the `resource-type` must be exact:
- `"document"` for documents
- `"link"` for links
- `"folder"` for folders

### Deleting Folders

Deleting a folder will delete its contents (documents, links, subfolders). Check the folder contents first:

```bash
operately resource_hubs list_nodes --folder-id f1
```

Move important items before deleting:

```bash
# Move items out first
operately resource_hubs update_parent_folder \
  --resource-id d1 \
  --resource-type "document" \
  --new-folder-id safe_folder_id

# Then delete folder
operately resource_hubs delete_folder --folder-id f1
```

### Document Drafts

Draft documents are visible to editors but not published to the team. Use drafts for work-in-progress:

```bash
# Create draft
operately documents create \
  --resource-hub-id rh1 \
  --name "WIP: New Policy" \
  --content "# Draft\n\nStill writing..." \
  --post-as-draft true

# Publish when ready
operately documents publish --document-id d1
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
operately documents create \
  --resource-hub-id rh1 \
  --name "API Guide" \
  --content "# API Documentation\n\n## Authentication\n\nUse Bearer tokens:\n\n\`\`\`bash\ncurl -H 'Authorization: Bearer TOKEN' https://api.example.com\n\`\`\`\n\n## Endpoints\n\n### GET /users\n\nReturns all users.\n\n**Response:**\n\`\`\`\n{\n  \"users\": [...]\n}\n\`\`\`"

operately documents create \
  --resource-hub-id rh1 \
  --name "API Guide" \
  --content-file ./api-guide.md
```

### Notifications

Use `--send-notifications-to-everyone` sparingly. For targeted notifications, use `--subscriber-ids`:

```bash
# Notify specific people
operately documents create \
  --resource-hub-id rh1 \
  --name "Team Update" \
  --content "# Update" \
  --subscriber-ids u1 \
  --subscriber-ids u2
```

### Searching Content

Use the company global search to find documents and links:

```bash
operately companies global_search --query "onboarding"
```

This searches across all resource hubs, documents, and links in the company.
