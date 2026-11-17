import { access, lstat } from "node:fs/promises";
import { constants } from "node:fs";
import { basename, dirname, isAbsolute, parse } from "node:path";

const WINDOWS_RESERVED = new Set([
  "CON", "PRN", "AUX", "NUL",
  ...Array.from({ length: 9 }, (_, index) => `COM${index + 1}`),
  ...Array.from({ length: 9 }, (_, index) => `LPT${index + 1}`),
]);

export function portabilityErrors(path, label = "path") {
  const text = String(path);
  const errors = [];
  if (/[\r\n\0]/u.test(text)) errors.push(`${label} path contains a newline or NUL: ${JSON.stringify(text)}`);
  const windowsAbsolute = /^[A-Za-z]:[\\/]/u.test(text);
  const withoutDrive = windowsAbsolute ? text.slice(2) : text;
  if (withoutDrive.includes(":")) errors.push(`${label} path contains a colon: ${JSON.stringify(text)}`);
  if (text.includes("\\") && !windowsAbsolute && !text.startsWith("\\\\")) {
    errors.push(`${label} path contains a non-portable backslash: ${JSON.stringify(text)}`);
  }
  const components = withoutDrive.split(/[\\/]+/u);
  if (components.includes("..")) errors.push(`${label} path contains traversal ('..'): ${JSON.stringify(text)}`);
  for (const component of components) {
    if (!component || component === ".") continue;
    const stem = component.split(".", 1)[0].toUpperCase();
    if (WINDOWS_RESERVED.has(stem)) errors.push(`${label} path uses a Windows-reserved name: ${component}`);
    if (/[ .]$/u.test(component) || /[\x01-\x1f]/u.test(component)) {
      errors.push(`${label} path has a non-portable component: ${JSON.stringify(component)}`);
    }
  }
  return errors;
}

async function pathType(path) {
  try {
    const details = await lstat(path);
    if (details.isSymbolicLink()) return "symlink";
    return details.isFile() ? "file" : details.isDirectory() ? "directory" : "other";
  } catch (error) {
    if (error.code === "ENOENT") return "missing";
    throw error;
  }
}

export async function preflightPaths(inputs, output = null, { outputKind = "file" } = {}) {
  const errors = [];
  for (const input of inputs) {
    const type = await pathType(input);
    if (type === "missing") errors.push(`input does not exist: ${input}`);
    else if (type === "symlink") errors.push(`input must not be a symbolic link: ${input}`);
    else if (type !== "file") errors.push(`input must be an explicit file: ${input}`);
    errors.push(...portabilityErrors(input, "input"));
  }
  if (output !== null && output !== undefined) {
    const type = await pathType(output);
    if (basename(output).toLowerCase() === "memory.md") errors.push("output may not be MEMORY.md");
    if (outputKind === "file") {
      if (type === "directory") errors.push(`output is a directory: ${output}`);
      else if (type === "symlink") errors.push(`output must not be a symbolic link: ${output}`);
      else if (type !== "missing") errors.push(`refusing to overwrite existing output: ${output}`);
    } else if (type !== "missing") {
      errors.push(type === "symlink"
        ? `render output must not be a symbolic link: ${output}`
        : `render output must not already exist: ${output}`);
    }
    const writableParent = dirname(output);
    const parentType = await pathType(writableParent);
    if (parentType === "symlink") errors.push(`output parent must not be a symbolic link: ${writableParent}`);
    try {
      await access(writableParent, constants.W_OK);
    } catch {
      errors.push(`output parent is not writable or does not exist: ${writableParent}`);
    }
    errors.push(...portabilityErrors(output, "output"));
  }
  return errors;
}

export function actionFor(command, output) {
  if (!isAbsolute(output)) throw new Error("approval actions require a resolved absolute output path");
  return `${command}:${parse(output).root}${output.slice(parse(output).root.length)}`;
}
