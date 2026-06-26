# Changelog - m365-planner Skill

All notable changes to the m365-planner Skill are documented in this file.

## [1.2.3] - 2026-04-18

### 🌍 Added

**English Documentation:**
- Complete translation of SKILL.md for international ClawHub availability
- All sections translated: Setup, Quick Start, Troubleshooting, References
- International audience ready

### 🔧 Changed

**Portability:**
- Env path in all scripts uses `path.join(os.homedir(), '.openclaw', '.env')`
- Works on any system without modifications
- Cross-platform compatible

### 🧹 Security

**Audit Completed:**
- Full check for hardcoded sensitive data (Group-IDs, Tenant-IDs, Client-IDs, domains, names)
- No project-specific data included
- ClawHub publication ready

---

## [1.2.2] - 2026-04-18

### 🔧 Changed

**Improved Portability:**
- Env path in all scripts changed from hardcoded `/home/claw/.openclaw/.env` to `path.join(os.homedir(), '.openclaw', '.env')`
- Skill now works on any system without modifications
- ClawHub-ready: No system-specific paths anymore

### 🧹 Cleanup

**Security & Privacy:**
- Complete check for hardcoded sensitive data (Group-IDs, Tenant-IDs, Client-IDs, Domains, Names)
- No project-specific data included
- All scripts now use generic, portable paths

### 📦 Packaging

**Prepared for ClawHub:**
- Tarball created (`m365-planner-v1.2.2.tar.gz`)
- Only necessary files included (SKILL.md, Scripts, References, Package-Files)
- node_modules excluded (installed separately)

---

## [1.2.1] - 2026-04-18

### ✅ Added

**Generic Scripts:**
- No hardcoded Group-IDs or Plan names anymore
- All scripts accept IDs as command-line parameters
- List Plans shows all groups when no ID provided
- Cleanup script works with any plans/buckets
- ClawHub-ready with no project-specific data

---

## [1.1.0] - 2026-04-17

### 🎉 Added

**Node.js Scripts (replacing mgc CLI dependency):**
- `scripts/test-connection.js` – Connection test with M365 Group Detection
- `scripts/list_plans.js` – Complete Plan/Bucket/Task overview
- `scripts/create_plan.js` – Plan creation with default buckets
- `scripts/cleanup_verlaengerungen.js` – Automated cleanup of completed tasks

**Documentation:**
- If-Match Header / ETag handling for updates and deletes
- Group-based API endpoints (`/groups/{id}/planner/plans`)
- M365 Groups vs. Security Groups explanation
- Native Planner Recurring Tasks documentation
- Expanded Troubleshooting section

### 🔧 Changed

**Setup Process:**
- No `mgc` CLI required anymore
- Node.js packages (`@microsoft/microsoft-graph-client`, `axios`) sufficient
- Credentials in `~/.openclaw/.env` (not in script)
- Admin Consent explicitly documented

**API Usage:**
- Switched from `/planner/plans` to `/groups/{id}/planner/plans`
- Automatic ETag handling in all scripts
- Better error messages for permission issues

### 🐛 Fixed

- **If-Match Header Error** – All Delete/Update operations now send correct ETag
- **Group Filter Error** – Plans now queried via Group-ID
- **Module Not Found** – Local npm installation in skill directory

### 📝 Technical Notes

**Key insights from implementation:**

1. **If-Match Header is mandatory**
   - Planner uses Optimistic Concurrency Control
   - DELETE/PATCH requests fail without `If-Match: <etag>` header
   - Solution: Always fetch resource first, then use ETag

2. **Only M365 Groups support Planner**
   - Security Groups and Distribution Lists don't work
   - Recognition: M365 Groups have mail attribute
   - Creation: Via Teams or M365 Admin Center

3. **Recurring Tasks only via UI**
   - Graph API doesn't support creating recurring tasks
   - Must be configured in Planner Web/Mobile UI
   - Native feature works reliably

---

## [1.0.0] - 2023-01-19

### 🎉 Initial Release

- Basic CRUD operations via mgc CLI
- Azure AD Setup Guide
- Foundation for Planner integration
