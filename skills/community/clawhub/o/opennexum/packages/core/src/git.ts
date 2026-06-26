import { execFile } from "node:child_process";

export class GitError extends Error {
  command: string;
  exitCode?: string | number | null;
  stderr?: string;

  constructor(
    message: string,
    options: {
      command: string;
      exitCode?: string | number | null;
      stderr?: string;
      cause?: unknown;
    }
  ) {
    super(message, { cause: options.cause });
    this.name = "GitError";
    this.command = options.command;
    this.exitCode = options.exitCode;
    this.stderr = options.stderr;
  }
}

export async function getHeadCommit(projectDir: string): Promise<string> {
  return runGit(projectDir, ["rev-parse", "HEAD"]);
}

export async function getChangedFiles(
  projectDir: string,
  baseCommit: string,
  headCommit: string
): Promise<string[]> {
  const output = await runGit(projectDir, [
    "diff",
    "--name-only",
    baseCommit,
    headCommit
  ]);

  return output
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line !== "");
}

export async function commitFiles(
  projectDir: string,
  files: string[],
  message: string
): Promise<string> {
  if (files.length === 0) {
    throw new GitError("No files provided for commit", {
      command: "git add --"
    });
  }

  await runGit(projectDir, ["add", "--", ...files]);
  await runGit(projectDir, ["commit", "-m", message]);
  return getHeadCommit(projectDir);
}

async function runGit(projectDir: string, args: string[]): Promise<string> {
  try {
    const stdout = await new Promise<string>((resolve, reject) => {
      execFile(
        "git",
        ["-C", projectDir, ...args],
        { encoding: "utf8", maxBuffer: 10 * 1024 * 1024 },
        (
          error: (Error & { code?: string | number | null }) | null,
          output: string,
          stderr: string
        ) => {
          if (error) {
            reject({ ...error, stderr });
            return;
          }

          resolve(output);
        }
      );
    });

    return stdout.trim();
  } catch (error) {
    const details = error as {
      code?: string | number | null;
      stderr?: string;
      message?: string;
    };

    throw new GitError(details.message ?? "Git command failed", {
      cause: error,
      command: `git -C ${projectDir} ${args.join(" ")}`,
      exitCode: details.code,
      stderr: details.stderr
    });
  }
}
