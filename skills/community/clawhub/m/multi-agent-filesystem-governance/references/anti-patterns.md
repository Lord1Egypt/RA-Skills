# Anti-Patterns

Use this file to recognize and avoid filesystem behaviors that create confusion, duplication, or cross-agent risk.

## 1. Shared-by-default placement

Anti-pattern:
Putting new files into shared locations before their reuse value is clear.

Why it is harmful:
This increases clutter, raises cross-agent risk, and makes ownership unclear.

Prefer instead:
Start in the narrowest private location. Promote to shared only when reuse is intentional.

---

## 2. Archive as live workspace

Anti-pattern:
Continuing to edit files directly inside archive locations.

Why it is harmful:
Archive loses its meaning as a historical or frozen state and becomes impossible to trust.

Prefer instead:
Restore or copy materials back into an active or private workspace before editing.

---

## 3. Permanent download pile

Anti-pattern:
Letting download intake locations become long-term storage.

Why it is harmful:
Downloaded files remain unclassified, hard to search, and disconnected from their real purpose.

Prefer instead:
Use a dedicated intake area, then sort files into projects, references, knowledge, private workspaces, or archive.

---

## 4. Script sprawl

Anti-pattern:
Scattering reusable scripts across random folders, project roots, temp directories, and note locations.

Why it is harmful:
Scripts become hard to find, duplicate unnecessarily, and lose ownership context.

Prefer instead:
Place reusable scripts in a shared scripts area and keep project-specific scripts inside the relevant project.

---

## 5. Knowledge vault as junk drawer

Anti-pattern:
Using the knowledge vault as a generic dump for exports, binaries, random downloads, and transient files.

Why it is harmful:
Knowledge quality collapses and the vault stops serving as durable reference.

Prefer instead:
Store only curated notes, durable references, and intentionally preserved knowledge artifacts in the knowledge location.

---

## 6. Mixing source trees with unrelated files

Anti-pattern:
Putting downloads, ad hoc notes, media exports, or unrelated utilities directly into code project roots.

Why it is harmful:
Project boundaries blur, automation becomes brittle, and cleanup gets harder.

Prefer instead:
Keep project roots focused on project content, with clearly scoped subdirectories where necessary.

---

## 7. Cross-agent overwrite without intent

Anti-pattern:
Editing or reorganizing another agent’s private files without explicit need.

Why it is harmful:
This breaks ownership expectations and can destroy structure that only the owning agent understands.

Prefer instead:
Treat private agent areas as protected by default. Use shared or coordinated areas for collaboration.

---

## 8. Duplicate variants without purpose

Anti-pattern:
Keeping multiple copies of the same skill, script, template, or note across private, shared, and project locations without clear precedence.

Why it is harmful:
It becomes unclear which version is authoritative and updates drift apart.

Prefer instead:
Keep one authoritative version whenever possible. Use overrides intentionally and document the reason.

---

## 9. Temp-only critical files

Anti-pattern:
Keeping the only important copy of a file in a temp or scratch location.

Why it is harmful:
Temporary storage is disposable and may be cleaned up or ignored.

Prefer instead:
Move or copy important artifacts into an active private, shared, project, or archival location as soon as they matter.

---

## 10. Flat shared root chaos

Anti-pattern:
Putting all shared files into one undifferentiated shared directory.

Why it is harmful:
The shared area becomes hard to search, hard to automate, and risky to modify.

Prefer instead:
Separate shared content by type, such as skills, scripts, downloads, projects, templates, assets, or references.

---

## 11. No lifecycle distinction

Anti-pattern:
Treating temporary, active, frozen, and archived files as if they belong in the same places.

Why it is harmful:
Agents cannot tell what is safe to modify, ignore, clean up, or preserve.

Prefer instead:
Use different areas or clear conventions for lifecycle states.

---

## 12. Cosmetic reorganization churn

Anti-pattern:
Renaming and moving files frequently without improving ownership, lifecycle clarity, or discoverability.

Why it is harmful:
Path churn breaks links, scripts, habits, and recovery efforts while adding little value.

Prefer instead:
Reorganize only when it clarifies scope, lifecycle, or future automation.
