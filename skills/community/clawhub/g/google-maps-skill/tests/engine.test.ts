import { beforeAll, describe, expect, it } from "bun:test";

import { executeCommandDef } from "../scripts/lib/engine.ts";
import { CliError, ExitCode } from "../scripts/lib/config.ts";
import type { HttpRequest } from "../scripts/lib/http.ts";
import type { HttpResult } from "../scripts/lib/types.ts";
import { COMMAND_REGISTRY } from "../scripts/commands/index.ts";

const fixturePath = (name: string) => new URL(`./fixtures/${name}`, import.meta.url);

async function loadFixture(name: string): Promise<unknown> {
  return JSON.parse(await Bun.file(fixturePath(name)).text());
}

function mockRequestFn(payload: unknown, status = 200): (request: HttpRequest) => Promise<HttpResult> {
  return async () => ({ status, payload });
}

describe("engine: geocode", () => {
  let geocodeSuccess: unknown;
  let geocodeError: unknown;

  beforeAll(async () => {
    geocodeSuccess = await loadFixture("geocode-success.json");
    geocodeError = await loadFixture("geocode-error.json");
  });

  it("returns raw geocode JSON on success", async () => {
    const calls: HttpRequest[] = [];
    const command = COMMAND_REGISTRY.get("geocode")!;

    const result = await executeCommandDef(
      command,
      { address: "Tokyo Tower" },
      {
        apiKey: "test-key",
        requestFn: async (request) => {
          calls.push(request);
          return { status: 200, payload: geocodeSuccess };
        },
      },
    );

    expect(result).toEqual(geocodeSuccess);
    expect(calls).toHaveLength(1);
    expect(calls[0]?.url).toContain("geocode");
    expect(calls[0]?.params?.key).toBe("test-key");
    expect(calls[0]?.params?.address).toBe("Tokyo Tower");
  });

  it("uses query auth for legacy APIs", async () => {
    const calls: HttpRequest[] = [];
    const command = COMMAND_REGISTRY.get("geocode")!;

    await executeCommandDef(
      command,
      { address: "Tokyo" },
      {
        apiKey: "test-key",
        requestFn: async (request) => {
          calls.push(request);
          return { status: 200, payload: geocodeSuccess };
        },
      },
    );

    expect(calls[0]?.params?.key).toBe("test-key");
    expect(calls[0]?.headers?.["X-Goog-Api-Key"]).toBeUndefined();
  });

  it("fails with exit code 4 when geocode returns non-OK status", async () => {
    const command = COMMAND_REGISTRY.get("geocode")!;

    try {
      await executeCommandDef(
        command,
        { address: "invalid" },
        {
          apiKey: "test-key",
          requestFn: mockRequestFn(geocodeError),
        },
      );
      expect(true).toBe(false);
    } catch (error) {
      expect(error).toBeInstanceOf(CliError);
      const cliError = error as CliError;
      expect(cliError.exitCode).toBe(ExitCode.API_BUSINESS);
      expect(cliError.rawResponse).toEqual(geocodeError);
    }
  });
});

describe("engine: directions (POST + header auth)", () => {
  let directionsSuccess: unknown;
  let newApiError: unknown;

  beforeAll(async () => {
    directionsSuccess = await loadFixture("directions-success.json");
    newApiError = await loadFixture("new-api-error.json");
  });

  it("returns routes on success", async () => {
    const calls: HttpRequest[] = [];
    const command = COMMAND_REGISTRY.get("directions")!;

    const result = await executeCommandDef(
      command,
      { origin: "Shibuya Station", dest: "Tokyo Tower" },
      {
        apiKey: "test-key",
        requestFn: async (request) => {
          calls.push(request);
          return { status: 200, payload: directionsSuccess };
        },
      },
    );

    expect(result).toEqual(directionsSuccess);
    expect(calls).toHaveLength(1);
    expect(calls[0]?.method).toBe("POST");
    expect(calls[0]?.headers?.["X-Goog-Api-Key"]).toBe("test-key");
    expect(calls[0]?.headers?.["X-Goog-FieldMask"]).toContain("routes");
    expect(calls[0]?.body).toEqual({
      origin: { address: "Shibuya Station" },
      destination: { address: "Tokyo Tower" },
      travelMode: "DRIVE",
    });
  });

  it("sends correct travel mode", async () => {
    const calls: HttpRequest[] = [];
    const command = COMMAND_REGISTRY.get("directions")!;

    await executeCommandDef(
      command,
      { origin: "A", dest: "B", mode: "TRANSIT" },
      {
        apiKey: "test-key",
        requestFn: async (request) => {
          calls.push(request);
          return { status: 200, payload: directionsSuccess };
        },
      },
    );

    const body = calls[0]?.body as Record<string, unknown>;
    expect(body.travelMode).toBe("TRANSIT");
  });

  it("fails with exit code 4 when routes array is empty", async () => {
    const command = COMMAND_REGISTRY.get("directions")!;

    try {
      await executeCommandDef(
        command,
        { origin: "Shibuya Station", dest: "Tokyo Tower", mode: "TRANSIT" },
        {
          apiKey: "test-key",
          requestFn: mockRequestFn({}, 200),
        },
      );
      expect(true).toBe(false);
    } catch (error) {
      expect(error).toBeInstanceOf(CliError);
      const cliError = error as CliError;
      expect(cliError.exitCode).toBe(ExitCode.API_BUSINESS);
      expect(cliError.message).toContain("No routes found");
    }
  });

  it("fails with exit code 4 on new API error response", async () => {
    const command = COMMAND_REGISTRY.get("directions")!;

    try {
      await executeCommandDef(
        command,
        { origin: "A", dest: "B" },
        {
          apiKey: "test-key",
          requestFn: mockRequestFn(newApiError, 400),
        },
      );
      expect(true).toBe(false);
    } catch (error) {
      expect(error).toBeInstanceOf(CliError);
      const cliError = error as CliError;
      expect(cliError.exitCode).toBe(ExitCode.API_BUSINESS);
      expect(cliError.rawResponse).toEqual(newApiError);
    }
  });
});

describe("engine: places-search", () => {
  let placesSuccess: unknown;

  beforeAll(async () => {
    placesSuccess = await loadFixture("places-search-success.json");
  });

  it("sends POST with header auth and fieldMask", async () => {
    const calls: HttpRequest[] = [];
    const command = COMMAND_REGISTRY.get("places-search")!;

    await executeCommandDef(
      command,
      { query: "Tokyo Tower" },
      {
        apiKey: "test-key",
        requestFn: async (request) => {
          calls.push(request);
          return { status: 200, payload: placesSuccess };
        },
      },
    );

    expect(calls[0]?.headers?.["X-Goog-Api-Key"]).toBe("test-key");
    expect(calls[0]?.headers?.["X-Goog-FieldMask"]).toBeDefined();
    expect(calls[0]?.body).toEqual({ textQuery: "Tokyo Tower" });
  });

  it("includes location bias when location flag provided", async () => {
    const calls: HttpRequest[] = [];
    const command = COMMAND_REGISTRY.get("places-search")!;

    await executeCommandDef(
      command,
      { query: "coffee", location: "35.6585,139.7454", radius: "1000" },
      {
        apiKey: "test-key",
        requestFn: async (request) => {
          calls.push(request);
          return { status: 200, payload: placesSuccess };
        },
      },
    );

    const body = calls[0]?.body as Record<string, unknown>;
    expect(body.textQuery).toBe("coffee");
    expect(body.locationBias).toBeDefined();
  });
});

describe("engine: place-detail (buildUrl)", () => {
  it("uses dynamic URL with place ID", async () => {
    const calls: HttpRequest[] = [];
    const command = COMMAND_REGISTRY.get("place-detail")!;

    await executeCommandDef(
      command,
      { "place-id": "ChIJCewJkL2LGGAR2HQ6PeTfivU" },
      {
        apiKey: "test-key",
        requestFn: async (request) => {
          calls.push(request);
          return { status: 200, payload: { id: "ChIJCewJkL2LGGAR2HQ6PeTfivU" } };
        },
      },
    );

    expect(calls[0]?.url).toContain("ChIJCewJkL2LGGAR2HQ6PeTfivU");
    expect(calls[0]?.method).toBe("GET");
  });
});

describe("engine: elevation", () => {
  let elevationSuccess: unknown;

  beforeAll(async () => {
    elevationSuccess = await loadFixture("elevation-success.json");
  });

  it("sends locations as query parameter", async () => {
    const calls: HttpRequest[] = [];
    const command = COMMAND_REGISTRY.get("elevation")!;

    const result = await executeCommandDef(
      command,
      { locations: "35.6585,139.7454" },
      {
        apiKey: "test-key",
        requestFn: async (request) => {
          calls.push(request);
          return { status: 200, payload: elevationSuccess };
        },
      },
    );

    expect(result).toEqual(elevationSuccess);
    expect(calls[0]?.params?.locations).toBe("35.6585,139.7454");
    expect(calls[0]?.params?.key).toBe("test-key");
  });
});

describe("engine: timezone", () => {
  let timezoneSuccess: unknown;

  beforeAll(async () => {
    timezoneSuccess = await loadFixture("timezone-success.json");
  });

  it("sends location and timestamp as query params", async () => {
    const calls: HttpRequest[] = [];
    const command = COMMAND_REGISTRY.get("timezone")!;

    const result = await executeCommandDef(
      command,
      { location: "35.6585,139.7454", timestamp: "1672531200" },
      {
        apiKey: "test-key",
        requestFn: async (request) => {
          calls.push(request);
          return { status: 200, payload: timezoneSuccess };
        },
      },
    );

    expect(result).toEqual(timezoneSuccess);
    expect(calls[0]?.params?.location).toBe("35.6585,139.7454");
    expect(calls[0]?.params?.timestamp).toBe("1672531200");
  });

  it("defaults timestamp to current time when not provided", async () => {
    const calls: HttpRequest[] = [];
    const command = COMMAND_REGISTRY.get("timezone")!;

    await executeCommandDef(
      command,
      { location: "35.6585,139.7454" },
      {
        apiKey: "test-key",
        requestFn: async (request) => {
          calls.push(request);
          return { status: 200, payload: timezoneSuccess };
        },
      },
    );

    const ts = Number(calls[0]?.params?.timestamp);
    expect(ts).toBeGreaterThan(0);
  });
});

describe("engine: network failure", () => {
  it("propagates network failures with exit code 3", async () => {
    const command = COMMAND_REGISTRY.get("geocode")!;

    try {
      await executeCommandDef(
        command,
        { address: "Tokyo" },
        {
          apiKey: "test-key",
          requestFn: async () => {
            throw new CliError("network timeout", ExitCode.NETWORK);
          },
        },
      );
      expect(true).toBe(false);
    } catch (error) {
      expect(error).toBeInstanceOf(CliError);
      const cliError = error as CliError;
      expect(cliError.exitCode).toBe(ExitCode.NETWORK);
      expect(cliError.message).toContain("network timeout");
    }
  });
});
