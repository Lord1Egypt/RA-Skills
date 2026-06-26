/**
 * Local File Manager Skill
 * Entry for OpenClaw - provides safe file I/O within cwd
 */

import { Skill } from "@openclaw/sdk";
import { exec } from "child_process";
import { promisify } from "util";
import { join, basename, dirname } from "path";

const execAsync = promisify(exec);

const skill = new Skill({
  name: "local-file-manager",
  description: "Read, write, append, list files in the session's working directory",

  triggers: {
    includes: ["文件", "读取", "写入", "保存", "append", "list files", "cat", "写文件", "读文件"],
    commands: ["file-read", "file-write", "file-append", "file-list", "file-mkdir", "file-delete"],
  },

  async run(input, context) {
    const { action, path, dir, content, pattern, dryRun = false } = input;

    // Build command line
    const args = ["--action", action];
    if (path) args.push("--path", path);
    if (dir) args.push("--dir", dir);
    if (content) args.push("--content", content);
    if (pattern) args.push("--pattern", pattern);
    if (dryRun) args.push("--dry-run");

    // Pass cwd via env
    const cwd = context.session?.cwd || process.cwd();

    const scriptPath = "/Users/nico/.openclaw/workspace/skills/local-file-manager/scripts/file_manager.sh";

    try {
      const { stdout } = await execAsync(`CWD="${cwd}" "${scriptPath}" ${args.join(" ")}`, {
        maxBuffer: 1024 * 1024,
      });

      // For read/write/append/list, return stdout directly
      return {
        success: true,
        action,
        output: stdout.trim(),
        file: path || dir,
      };
    } catch (error: any) {
      return {
        success: false,
        action,
        error: error.stderr || error.message,
      };
    }
  },
});

export default skill;