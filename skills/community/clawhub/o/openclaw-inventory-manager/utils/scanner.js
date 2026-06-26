const fs = require("fs");
const path = require("path");
const os = require("os");
const logger = require("./logger");

/**
 * Scanner Logic (v1.0.0)
 * Targeted scanning, mtime check, realpath handling, and depth control.
 */

const scanner = {
  /**
   * Translates common shortcuts like '~' to the user's home directory.
   */
  resolvePath: (p) => {
    if (p.startsWith("~")) {
      return path.join(os.homedir(), p.slice(1));
    }
    return path.resolve(p);
  },

  /**
   * Recursively scans for directories containing SKILL.md.
   */
  scan: (roots, options) => {
    const { maxDepth = 5, excludedDirs = [], manifest = {} } = options;
    const foundSkills = [];

    roots.forEach((root) => {
      const resolvedRoot = scanner.resolvePath(root);
      if (!fs.existsSync(resolvedRoot)) {
        logger.warn(`Search root does not exist: ${resolvedRoot}`);
        return;
      }
      logger.info(`Scanning: ${resolvedRoot}`);
      scanner._recursiveScan(resolvedRoot, 0, maxDepth, excludedDirs, foundSkills);
    });

    return foundSkills;
  },

  _recursiveScan: (dir, currentDepth, maxDepth, excludedDirs, foundSkills) => {
    if (currentDepth > maxDepth) return;

    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });

      // Check if current directory is a skill (contains SKILL.md)
      const skillFile = entries.find(e => e.isFile() && (e.name === "SKILL.md" || e.name === "SKILL.private.md"));
      if (skillFile) {
        const stats = fs.statSync(dir);
        const realPath = fs.realpathSync(dir);
        const isPrivate = skillFile.name === "SKILL.private.md";

        foundSkills.push({
          name: path.basename(dir),
          path: dir,
          realPath: realPath,
          isPrivate: isPrivate,
          mtime: stats.mtime,
          skillFilePath: path.join(dir, skillFile.name)
        });
        // We don't need to scan deeper if we already found a skill in this folder
        return;
      }

      // Deeper search if not found
      // NOTE: We intentionally do NOT skip all dot-folders here.
      // OpenClaw skills live in `.agents/skills/`, which would be incorrectly pruned.
      // Only directories listed in `excludedDirs` (from inventory.json) are skipped.
      entries.forEach((entry) => {
        if (!entry.isDirectory()) return;
        if (excludedDirs.includes(entry.name)) return;

        scanner._recursiveScan(
          path.join(dir, entry.name),
          currentDepth + 1,
          maxDepth,
          excludedDirs,
          foundSkills
        );
      });
    } catch (err) {
      logger.error(`Failed to scan ${dir}: ${err.message}`);
    }
  }
};

module.exports = scanner;
