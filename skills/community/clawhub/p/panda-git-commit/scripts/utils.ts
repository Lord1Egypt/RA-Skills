import { readFile, access } from "node:fs/promises";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const exec = promisify(execFile);

export async function fileExists(p: string): Promise<boolean> {
  try {
    await access(p);
    return true;
  } catch {
    return false;
  }
}

export async function readJson(p: string): Promise<unknown> {
  try {
    const raw = await readFile(p, "utf-8");
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export async function readText(p: string): Promise<string | null> {
  try {
    return await readFile(p, "utf-8");
  } catch {
    return null;
  }
}

export async function getRepoRoot(): Promise<string> {
  const { stdout } = await exec("git", ["rev-parse", "--show-toplevel"]);
  return stdout.trim();
}
