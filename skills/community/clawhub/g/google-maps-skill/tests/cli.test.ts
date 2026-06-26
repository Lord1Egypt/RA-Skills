import { describe, expect, it } from "bun:test";

const CLI_PATH = new URL("../scripts/gmaps.ts", import.meta.url).pathname;

interface CliResult {
  exitCode: number;
  stdout: string;
  stderr: string;
}

async function runCli(args: string[], envOverrides: Record<string, string | null> = {}): Promise<CliResult> {
  const env: Record<string, string> = {};

  for (const [key, value] of Object.entries(process.env)) {
    if (typeof value === "string") {
      env[key] = value;
    }
  }

  for (const [key, value] of Object.entries(envOverrides)) {
    if (value === null) {
      delete env[key];
    } else {
      env[key] = value;
    }
  }

  const processHandle = Bun.spawn(["bun", CLI_PATH, ...args], {
    env,
    stdout: "pipe",
    stderr: "pipe",
  });

  const stdout = await new Response(processHandle.stdout).text();
  const stderr = await new Response(processHandle.stderr).text();
  const exitCode = await processHandle.exited;

  return { exitCode, stdout, stderr };
}

describe("gmaps CLI", () => {
  it("shows global help", async () => {
    const result = await runCli(["--help"]);

    expect(result.exitCode).toBe(0);
    expect(result.stdout).toContain("Google Maps Script CLI");
    expect(result.stdout).toContain("geocode --address");
    expect(result.stdout).toContain("directions --origin");
  });

  it("shows global help when no arguments", async () => {
    const result = await runCli([]);

    expect(result.exitCode).toBe(0);
    expect(result.stdout).toContain("Google Maps Script CLI");
  });

  it("shows command-specific help", async () => {
    const result = await runCli(["geocode", "--help"]);

    expect(result.exitCode).toBe(0);
    expect(result.stdout).toContain("geocode --address");
    expect(result.stdout).toContain("Address to geocode");
  });

  it("shows directions command help with flags", async () => {
    const result = await runCli(["directions", "--help"]);

    expect(result.exitCode).toBe(0);
    expect(result.stdout).toContain("--origin");
    expect(result.stdout).toContain("--dest");
    expect(result.stdout).toContain("--mode");
    expect(result.stdout).toContain("(optional)");
  });

  it("returns exit code 2 for unknown command", async () => {
    const result = await runCli(["unknown-command"]);

    expect(result.exitCode).toBe(2);
    expect(result.stderr).toContain("Unknown command");
  });

  it("returns exit code 2 when API key is missing", async () => {
    const result = await runCli(["geocode", "--address", "Tokyo Tower"], {
      GOOGLE_MAPS_API_KEY: null,
    });

    expect(result.exitCode).toBe(2);
    expect(result.stderr).toContain("GOOGLE_MAPS_API_KEY is required");
  });

  it("returns exit code 2 for invalid latlng format", async () => {
    const result = await runCli(["reverse-geocode", "--latlng", "invalid"]);

    expect(result.exitCode).toBe(2);
    expect(result.stderr).toContain("Invalid flags");
  });

  it("returns exit code 2 for missing required flag", async () => {
    const result = await runCli(["geocode"], {
      GOOGLE_MAPS_API_KEY: "test-key",
    });

    expect(result.exitCode).toBe(2);
    expect(result.stderr).toContain("--address is required");
  });

  it("returns exit code 2 for unknown flags", async () => {
    const result = await runCli(["geocode", "--address", "Tokyo", "--foo", "bar"], {
      GOOGLE_MAPS_API_KEY: "test-key",
    });

    expect(result.exitCode).toBe(2);
    expect(result.stderr).toContain("unknown flags");
    expect(result.stderr).toContain("--foo");
  });

  it("returns exit code 2 for invalid directions mode", async () => {
    const result = await runCli(["directions", "--origin", "A", "--dest", "B", "--mode", "FLY"], {
      GOOGLE_MAPS_API_KEY: "test-key",
    });

    expect(result.exitCode).toBe(2);
    expect(result.stderr).toContain("must be one of");
  });
});
