# Feishu Sync

## 1. Goal

Sync a local novel project into Feishu Wiki while preserving a clean and predictable structure.

The sync target is not random document upload.  
It is a mirrored project hierarchy that remains readable and maintainable.

---

## 2. Sync source

Default local source:

`/root/.openclaw/novels/[小说名称]/`

Default sync scope:
- top-level project files
- `characters/`
- `manuscript/`

---

## 3. Sync target model

Default Wiki model:

- one root node for the novel
- top-level planning files under the novel root
- one `characters` node under the novel root
- one `manuscript` node under the novel root
- child documents under those nodes

---

## 4. Node creation rules

### 4.1 Wiki node type
When creating Wiki nodes:
- use `obj_type: docx`
- do not use `doc`

### 4.2 Node type
When creating nodes:
- use `node_type: origin`

### 4.3 Parent-child order
Always:
1. create or locate the project root node
2. sync top-level files
3. create or locate `characters`
4. sync character files
5. create or locate `manuscript`
6. sync manuscript files

Do not create child nodes before parent nodes exist.

---

## 5. Existing node reuse

If a node with the same title already exists under the intended parent:
- reuse it
- update its content instead of creating duplicates

Avoid duplicate nodes caused by repeated syncs.

---

## 6. Content sync rule

For each markdown file:
- map filename stem to Wiki node title
- map markdown content into the corresponding `docx` document
- prefer overwrite mode when the local file is the current source of truth

---

## 7. Sync order

Default sync order:

1. novel root
2. top-level planning files
3. characters directory
4. manuscript directory

This order keeps structure understandable and reduces orphan content risk.

---

## 8. Large manuscript handling

For projects with many chapter files:
- sync sequentially or in stable small batches
- avoid bursty parallel writes
- preserve order
- log progress
- retry carefully if a single node fails

Do not create hundreds of nodes in an uncontrolled parallel burst.

---

## 9. Naming mapping

### 9.1 Root title
Use the confirmed novel title as the Feishu root node title whenever possible.

### 9.2 Top-level file mapping
Examples:
- `00_选题报告.md` -> `00_选题报告`
- `01_想法.md` -> `01_想法`
- `02_大纲.md` -> `02_大纲`

### 9.3 Directory container mapping
Directories become container-like nodes:
- `characters/` -> `characters`
- `manuscript/` -> `manuscript`

### 9.4 Child file mapping
Use the filename stem as the child document title.

---

## 10. Error handling

### 10.1 Validation failures
If node creation fails:
- verify `obj_type` is `docx`
- verify `node_type` is `origin`
- verify parent node exists
- verify required permissions are granted

### 10.2 Partial syncs
If sync stops midway:
- keep already-created valid nodes
- resume from missing or outdated nodes
- avoid recreating already-synced structure unnecessarily

### 10.3 Duplicate risk
Before creating a node, list the parent’s children and compare titles first.

---

## 11. Sync completion summary

At the end of sync, report:
- root node created or reused
- top-level files synced count
- character files synced count
- manuscript files synced count
- failures count
- any skipped or reused nodes

A good sync is not silent. It should produce a usable summary.

---

## 12. Philosophy

Feishu sync is the final projection of a structured local project.

Do not treat Wiki as a dumping ground.  
Treat it as a readable mirrored knowledge space.
