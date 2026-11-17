# Migrate old Creator/Publish installations

This source package supplies one `onimi-pages` Skill. It has no direct-download
installer, receipt or update manager. Do not run package-installer commands against
this source or relabel old receipts. Existing immutable archives retain their identities.

First identify the current Agent's actual Skill directory and who owns each installed
copy. A plugin or registry owns its installation lifecycle: use its supported replacement
or disable/remove flow after preserving personal changes. Do not edit its registry state
or silently install a second active entrypoint. If the host cannot preserve or restore a
customized installation, stop with the old copy intact and explain the missing capability.

For manually installed directories, review the following plan with the user before changing
any active copy:

1. Download or clone the reviewed source revision into a staging directory outside every
   Skill discovery directory. Verify it contains the complete `skills/onimi-pages/` folder.
   Inspect the two old directories and preserve all files, permissions and personal changes.
   Unknown files or ownership require review; do not infer that they are safe to overwrite.
2. Prepare a complete new Skill in staging. Compare old instructions and helpers with the
   reviewed source, explicitly reconcile personal instructions, and preserve extra personal
   files separately. Do not copy a second `SKILL.md` entrypoint into the active directory.
3. With user authorization, move each complete old directory into a clearly identified backup
   outside **all** discovery roots. A backup folder inside a recursively scanned skills directory
   is not sufficient. Record original paths and verify every backup file matches before activation.
4. Activate only the complete staged `onimi-pages` folder in the verified directory. Reload the
   current Agent and check it discovers one entrypoint and can read its bundled references/helpers.
   Installation is a local check; it does not authorize a cloud write or publication.
5. If activation fails, move the new folder out of discovery, restore the original folders from
   the verified backups to their original paths, and reload. Keep backups and reconciled personal
   content until the user confirms the new installation works. Never delete them as cleanup.

Do not overwrite an existing canonical installation or migrate an unfamiliar layout automatically.
If the source or local ownership cannot be verified, leave the active installation intact.
