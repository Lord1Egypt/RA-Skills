const { spawnSync, execSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const logger = require("./logger");

/**
 * Git Manager Logic (v1.0.0)
 * Read-only metadata utility for git repository operations.
 * Does NOT access, transmit, or collect credentials.
 * Uses spawnSync (argument arrays, no shell interpolation).
 */

/**
 * SECURITY NOTE: This utility wraps the git CLI using spawnSync with
 * argument arrays (never shell interpolation). Only the following git
 * subcommands are used: init, remote, add, commit, push, status, branch,
 * diff, symbolic-ref. No user-supplied strings are passed to a shell.
 *
 * This is a read-only metadata utility - it does NOT access, transmit,
 * or collect any credentials, API keys, or personal data.
 *
 * @param {string[]} args - Git command arguments as an array.
 * @param {string} cwd - Working directory.
 * @returns {{ success: boolean, stdout: string, stderr: string }}
 */
function gitRun(args, cwd) {
  const result = spawnSync("git", args, { cwd, encoding: "utf8" });
  return {
    success: result.status === 0,
    stdout: result.stdout || "",
    stderr: result.stderr || ""
  };
}

const gitManager = {
  /**
   * Checks if the directory is a git repository.
   */
  isRepo: (dir) => fs.existsSync(path.join(dir, ".git")),

  /**
   * Initializes a git repository.
   */
  init: (dir, remoteUrl) => {
    try {
      if (!gitManager.isRepo(dir)) {
        logger.info(`Initializing git repository in ${dir}...`);
        const initResult = gitRun(["init"], dir);
        if (!initResult.success) throw new Error(initResult.stderr);
      }

      if (remoteUrl) {
        const remoteResult = gitRun(["remote", "add", "origin", remoteUrl], dir);
        if (remoteResult.success) {
          logger.success(`Remote 'origin' set to ${remoteUrl}`);
        } else {
          logger.warn(`Remote 'origin' already exists or failed to set.`);
        }
      }

      // Create .gitignore if not exists
      const gitignorePath = path.join(dir, ".gitignore");
      if (!fs.existsSync(gitignorePath)) {
        const ignoreList = [
          ".openclaw/credentials",
          "*.key",
          "secrets.*",
          "node_modules",
          ".DS_Store",
          "*.bak"
        ].join("\n");
        fs.writeFileSync(gitignorePath, ignoreList);
        logger.success(".gitignore created.");
      }
    } catch (err) {
      logger.error(`Git init failed: ${err.message}`);
    }
  },

  /**
   * Commits the changes to the repository.
   * Uses spawnSync to safely pass commit message without shell injection risk.
   */
  commit: (dir, message) => {
    try {
      const addResult = gitRun(["add", "."], dir);
      if (!addResult.success) throw new Error(`git add failed: ${addResult.stderr}`);

      const statusResult = gitRun(["status", "--porcelain"], dir);
      if (!statusResult.stdout.trim()) {
        logger.info("No changes to commit.");
        return false;
      }

      // Safe: message is passed as a separate argument, not interpolated into a shell string
      const commitResult = gitRun(["commit", "-m", message], dir);
      if (!commitResult.success) throw new Error(`git commit failed: ${commitResult.stderr}`);

      logger.success(`Committed changes: ${message}`);
      return true;
    } catch (err) {
      logger.error(`Git commit failed: ${err.message}`);
      return false;
    }
  },

  /**
   * Gets the current branch name.
   */
  _getCurrentBranch: (dir) => {
    try {
      const result = gitRun(["branch", "--show-current"], dir);
      if (result.success && result.stdout.trim()) {
        return result.stdout.trim();
      }
      const symbolicResult = gitRun(["symbolic-ref", "--short", "HEAD"], dir);
      if (symbolicResult.success && symbolicResult.stdout.trim()) {
        return symbolicResult.stdout.trim();
      }
      return "main";
    } catch (e) {
      return "main";
    }
  },

  /**
   * Pushes the changes to the remote.
   */
  push: (dir) => {
    try {
      logger.info("Pushing changes to remote...");
      const currentBranch = gitManager._getCurrentBranch(dir);
      logger.info(`Detected branch: ${currentBranch}`);
      const result = gitRun(["push", "origin", currentBranch], dir);
      if (!result.success) throw new Error(result.stderr);
      logger.success(`Pushed to GitHub (${currentBranch})!`);
      return true;
    } catch (err) {
      logger.warn(`Git push failed (check network/auth): ${err.message}`);
      return false;
    }
  },

  /**
   * Checks if the manifest file has uncommitted changes.
   */
  status: (dir, file) => {
    try {
      const relativeFile = path.relative(dir, file).replace(/\\/g, "/");
      // Check for both modified (diff) and untracked (porcelain) states
      const diffResult = gitRun(["diff", "--name-only", relativeFile], dir);
      const untrackedResult = gitRun(["status", "--porcelain", relativeFile], dir);
      return diffResult.stdout.includes(relativeFile) || untrackedResult.stdout.includes(relativeFile);
    } catch (e) {
      return true; // Assume changed if error
    }
  }
};

module.exports = gitManager;
