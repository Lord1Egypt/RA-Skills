/**
 * Async Python Executor
 * Supports both execFile-style (path, args, opts) and inline script modes.
 */
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFilePromise = promisify(execFile);

/**
 * Execute a Python script or command.
 * 
 * Signatures:
 *   execPython(scriptPath, args?, options?)  — runs: python3 scriptPath ...args
 *   execPython("python3", ["-c", code, ...], options?) — runs: python3 -c code ...
 * 
 * @param {string} scriptOrCommand - Path to .py file, or "python3" for inline
 * @param {string[]} [args=[]] - Arguments to pass
 * @param {object} [options={}] - { timeout, env, cwd }
 * @returns {Promise<{stdout: string, stderr: string}>}
 */
export async function execPython(scriptOrCommand, args = [], options = {}) {
  const { timeout = 30000, env = {}, cwd } = options;
  const mergedEnv = { ...process.env, ...env };

  try {
    if (scriptOrCommand === "python3" || scriptOrCommand === "python") {
      const { stdout, stderr } = await execFilePromise(scriptOrCommand, args, {
        timeout,
        env: mergedEnv,
        cwd,
        maxBuffer: 10 * 1024 * 1024,
      });
      return { stdout: stdout || "", stderr: stderr || "" };
    } else {
      const { stdout, stderr } = await execFilePromise("python3", [scriptOrCommand, ...args], {
        timeout,
        env: mergedEnv,
        cwd,
        maxBuffer: 10 * 1024 * 1024,
      });
      return { stdout: stdout || "", stderr: stderr || "" };
    }
  } catch (error) {
    const msg = error.stderr || error.message || String(error);
    throw new Error(`Python execution failed: ${msg}`);
  }
}
