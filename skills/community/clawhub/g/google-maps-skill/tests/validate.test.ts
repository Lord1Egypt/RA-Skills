import { describe, expect, it } from "bun:test";

import { validateFlags } from "../scripts/lib/validate.ts";
import { CliError, ExitCode } from "../scripts/lib/config.ts";
import { COMMAND_REGISTRY } from "../scripts/commands/index.ts";

describe("validateFlags", () => {
  it("validates geocode with required address", () => {
    const command = COMMAND_REGISTRY.get("geocode")!;
    const result = validateFlags(command, { address: "Tokyo Tower" });
    expect(result.address).toBe("Tokyo Tower");
  });

  it("trims whitespace from values", () => {
    const command = COMMAND_REGISTRY.get("geocode")!;
    const result = validateFlags(command, { address: "  Tokyo Tower  " });
    expect(result.address).toBe("Tokyo Tower");
  });

  it("throws on missing required flag", () => {
    const command = COMMAND_REGISTRY.get("geocode")!;
    expect(() => validateFlags(command, {})).toThrow(CliError);

    try {
      validateFlags(command, {});
    } catch (error) {
      const cliError = error as CliError;
      expect(cliError.exitCode).toBe(ExitCode.PARAM_OR_CONFIG);
      expect(cliError.message).toContain("--address is required");
    }
  });

  it("throws on unknown flags", () => {
    const command = COMMAND_REGISTRY.get("geocode")!;

    try {
      validateFlags(command, { address: "Tokyo", foo: "bar" });
    } catch (error) {
      const cliError = error as CliError;
      expect(cliError.exitCode).toBe(ExitCode.PARAM_OR_CONFIG);
      expect(cliError.message).toContain("unknown flags");
      expect(cliError.message).toContain("--foo");
    }
  });

  it("throws on empty string value", () => {
    const command = COMMAND_REGISTRY.get("geocode")!;

    try {
      validateFlags(command, { address: "   " });
    } catch (error) {
      const cliError = error as CliError;
      expect(cliError.exitCode).toBe(ExitCode.PARAM_OR_CONFIG);
      expect(cliError.message).toContain("non-empty");
    }
  });

  it("validates reverse-geocode latlng format", () => {
    const command = COMMAND_REGISTRY.get("reverse-geocode")!;

    const result = validateFlags(command, { latlng: "35.6585,139.7454" });
    expect(result.latlng).toBe("35.6585,139.7454");
  });

  it("rejects invalid latlng", () => {
    const command = COMMAND_REGISTRY.get("reverse-geocode")!;

    expect(() => validateFlags(command, { latlng: "invalid" })).toThrow(CliError);
    expect(() => validateFlags(command, { latlng: "999,999" })).toThrow(CliError);
  });

  it("validates directions with optional mode", () => {
    const command = COMMAND_REGISTRY.get("directions")!;

    const result = validateFlags(command, { origin: "A", dest: "B" });
    expect(result.origin).toBe("A");
    expect(result.dest).toBe("B");
    expect(result.mode).toBeUndefined();
  });

  it("validates directions mode enum", () => {
    const command = COMMAND_REGISTRY.get("directions")!;

    const result = validateFlags(command, { origin: "A", dest: "B", mode: "TRANSIT" });
    expect(result.mode).toBe("TRANSIT");
  });

  it("rejects invalid directions mode", () => {
    const command = COMMAND_REGISTRY.get("directions")!;

    expect(() => validateFlags(command, { origin: "A", dest: "B", mode: "FLY" })).toThrow(CliError);
  });

  it("validates elevation locations", () => {
    const command = COMMAND_REGISTRY.get("elevation")!;

    const result = validateFlags(command, { locations: "35.6585,139.7454|34.0522,-118.2437" });
    expect(result.locations).toBe("35.6585,139.7454|34.0522,-118.2437");
  });

  it("rejects invalid elevation locations", () => {
    const command = COMMAND_REGISTRY.get("elevation")!;

    expect(() => validateFlags(command, { locations: "not-a-coord" })).toThrow(CliError);
  });

  it("validates timezone with optional timestamp", () => {
    const command = COMMAND_REGISTRY.get("timezone")!;

    const result = validateFlags(command, { location: "35.6585,139.7454" });
    expect(result.location).toBe("35.6585,139.7454");
    expect(result.timestamp).toBeUndefined();
  });

  it("validates timezone timestamp", () => {
    const command = COMMAND_REGISTRY.get("timezone")!;

    const result = validateFlags(command, { location: "35.6585,139.7454", timestamp: "1672531200" });
    expect(result.timestamp).toBe("1672531200");
  });

  it("rejects invalid timezone timestamp", () => {
    const command = COMMAND_REGISTRY.get("timezone")!;

    expect(() => validateFlags(command, { location: "35.6585,139.7454", timestamp: "abc" })).toThrow(CliError);
  });

  it("validates places-nearby with required location and radius", () => {
    const command = COMMAND_REGISTRY.get("places-nearby")!;

    const result = validateFlags(command, { location: "35.6585,139.7454", radius: "1000" });
    expect(result.location).toBe("35.6585,139.7454");
    expect(result.radius).toBe("1000");
  });

  it("validates place-detail with place-id", () => {
    const command = COMMAND_REGISTRY.get("place-detail")!;

    const result = validateFlags(command, { "place-id": "ChIJCewJkL2LGGAR2HQ6PeTfivU" });
    expect(result["place-id"]).toBe("ChIJCewJkL2LGGAR2HQ6PeTfivU");
  });
});
