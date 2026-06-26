import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export interface CliAvailability {
  claude: boolean;
  codex: boolean;
}

export async function detectAvailableCli(): Promise<CliAvailability> {
  const check = async (cmd: string): Promise<boolean> => {
    try {
      await execFileAsync(cmd, ["--version"], { timeout: 5000 });
      return true;
    } catch {
      return false;
    }
  };

  const [claude, codex] = await Promise.all([check("claude"), check("codex")]);
  return { claude, codex };
}

export async function detectGitRemote(projectDir: string, remote = "origin"): Promise<boolean> {
  try {
    await execFileAsync("git", ["ls-remote", "--exit-code", remote], {
      cwd: projectDir,
      timeout: 10000,
    });
    return true;
  } catch {
    return false;
  }
}
