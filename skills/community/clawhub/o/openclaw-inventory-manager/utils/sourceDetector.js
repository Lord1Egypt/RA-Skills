const fs = require("fs");
const path = require("path");
const logger = require("./logger");

/**
 * Source Detection Logic (v1.0.0)
 * Identifies the origin of a skill (Git, NPM, ClawHub, Local).
 */

const sourceDetector = {
  /**
   * Detects the source of a skill at the given path.
   */
  detect: (skillPath, realPath) => {
    const findFile = (name) => {
      const p1 = path.join(skillPath, name);
      if (fs.existsSync(p1)) return p1;
      if (realPath && realPath !== skillPath) {
        const p2 = path.join(realPath, name);
        if (fs.existsSync(p2)) return p2;
      }
      return null;
    };

    const clawhubJson = findFile("clawhub.json");
    const managedClawhubJson = findFile(".clawhub.json");
    const gitDir = findFile(".git");
    const pkgJson = findFile("package.json");

    // 1. Check for ClawHub specific metadata
    if (clawhubJson || managedClawhubJson) {
      try {
        const metadataFile = clawhubJson || managedClawhubJson;
        const config = JSON.parse(fs.readFileSync(metadataFile, "utf8"));
        return {
          method: "clawhub",
          source: config.repository || config.url || "ClawHub Registry",
          icon: "🦀"
        };
      } catch (e) {
        logger.debug(`Failed to parse clawhub.json in ${skillPath}`);
      }
    }

    // 2. Check for SkillsMP (agent-skills-cli) lockfile
    const skillsMPPath = path.join(process.env.HOME || process.env.USERPROFILE || "~", ".skills", "skills.lock");
    if (fs.existsSync(skillsMPPath)) {
      try {
        const lockData = JSON.parse(fs.readFileSync(skillsMPPath, "utf8"));
        const normalizedPath = path.normalize(skillPath);
        
        const findSkillInLock = (lockObj) => {
          if (lockObj.skills) {
            for (const [skillName, skillData] of Object.entries(lockObj.skills)) {
              if (skillData.path && path.normalize(skillData.path) === normalizedPath) {
                return { name: skillName, version: skillData.version };
              }
            }
          }
          if (Array.isArray(lockObj)) {
            for (const skillData of lockObj) {
              if (skillData.path && path.normalize(skillData.path) === normalizedPath) {
                return { name: skillData.name, version: skillData.version };
              }
            }
          }
          return null;
        };

        const matchedSkill = findSkillInLock(lockData);
        if (matchedSkill) {
          return {
            method: "skillsmp",
            source: matchedSkill.name,
            version: matchedSkill.version,
            icon: "📦"
          };
        }
      } catch (e) {
        logger.debug(`Failed to parse skills.lock in ${skillsMPPath}: ${e.message}`);
      }
    }

    // 3. Check for Git Repository
    if (gitDir) {
      try {
        const configPath = path.join(gitDir, "config");
        if (fs.existsSync(configPath)) {
          const configContent = fs.readFileSync(configPath, "utf8");
          const urlMatch = configContent.match(/url\s*=\s*(.*)/);
          if (urlMatch) {
            return {
              method: "git",
              source: urlMatch[1].trim(),
              icon: "📁"
            };
          }
        }
      } catch (e) {
        logger.debug(`Failed to read git config in ${skillPath}`);
      }
    }

    // 4. Check for NPM Package
    if (pkgJson) {
      try {
        const pkg = JSON.parse(fs.readFileSync(pkgJson, "utf8"));
        return {
          method: "npm",
          source: pkg.name || "NPM Package",
          icon: "📦"
        };
      } catch (e) {
        logger.debug(`Failed to parse package.json in ${skillPath}`);
      }
    }

    // 5. Default to Local/Manual
    return {
      method: "manual",
      source: "Local/Manual Installation",
      icon: "👤"
    };
  }
}
;

module.exports = sourceDetector;
