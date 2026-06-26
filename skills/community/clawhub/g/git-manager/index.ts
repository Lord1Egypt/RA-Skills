/**
 * Git Manager Skill
 * Entry point for OpenClaw
 */

import { Skill } from "@openclaw/sdk";

const skill = new Skill({
  name: "git-manager",
  description: "Execute Git operations safely: commit, push, pull, branch management",

  triggers: {
    includes: ["git", "commit", "push", "pull", "分支", "合并", "仓库", "版本控制"],
    commands: ["git-status", "git-commit", "git-push", "git-pull", "git-branch", "git-checkout"],
  },

  async run(input, context) {
    const { action, repo, message, files, branch, create, from, dryRun } = input;

    // Build command line
    const args = ["--action", action];
    if (repo) args.push("--repo", repo);
    if (message) args.push("--message", message);
    if (files && Array.isArray(files)) args.push("--files", files.join(","));
    if (branch) args.push("--branch", branch);
    if (create) args.push("--create");
    if (from) args.push("--from", from);
    if (dryRun) args.push("--dry-run");
    args.push("--json");

    // Execute the shell script
    const { exec } = await import("child_process");
    const path = "/Users/nico/.openclaw/workspace/skills/git-manager/scripts/git-manager";

    return new Promise((resolve, reject) => {
      exec(`"${path}" ${args.join(" ")}`, { maxBuffer: 1024 * 1024 }, (error, stdout, stderr) => {
        if (error) {
          reject(new Error(stderr || error.message));
          return;
        }
        try {
          const result = JSON.parse(stdout);
          resolve(result);
        } catch (e) {
          resolve({ raw: stdout, error: stderr });
        }
      });
    });
  },
});

export default skill;