import { CliError, ExitCode } from "./config.ts";
import type { CommandDef } from "./types.ts";

export function validateFlags(
  command: CommandDef,
  rawFlags: Record<string, string>,
): Record<string, string> {
  const allowedKeys = new Set(Object.keys(command.flags));
  const unknownFlags: string[] = [];

  for (const key of Object.keys(rawFlags)) {
    if (!allowedKeys.has(key)) {
      unknownFlags.push(`--${key}`);
    }
  }

  if (unknownFlags.length > 0) {
    throw new CliError(
      `Invalid flags for ${command.name}: unknown flags: ${unknownFlags.join(", ")}`,
      ExitCode.PARAM_OR_CONFIG,
    );
  }

  const validated: Record<string, string> = {};

  for (const [key, def] of Object.entries(command.flags)) {
    const raw = rawFlags[key];

    if (raw === undefined) {
      if (def.required) {
        throw new CliError(
          `Invalid flags for ${command.name}: --${key} is required`,
          ExitCode.PARAM_OR_CONFIG,
        );
      }
      continue;
    }

    const trimmed = raw.trim();
    if (trimmed.length === 0) {
      throw new CliError(
        `Invalid flags for ${command.name}: --${key} must be a non-empty string`,
        ExitCode.PARAM_OR_CONFIG,
      );
    }

    if (def.validate) {
      const errorMsg = def.validate(trimmed);
      if (errorMsg !== null) {
        throw new CliError(
          `Invalid flags for ${command.name}: --${key}: ${errorMsg}`,
          ExitCode.PARAM_OR_CONFIG,
        );
      }
    }

    validated[key] = trimmed;
  }

  return validated;
}
