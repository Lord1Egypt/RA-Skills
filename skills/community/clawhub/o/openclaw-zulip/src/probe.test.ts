import { describe, it, expect, vi, afterEach } from "vitest";
import { probeZulip } from "./probe.js";

function mockFetch(data: unknown, status = 200) {
  return vi.fn().mockResolvedValue({
    status,
    headers: new Headers(),
    json: async () => data,
  } as Response);
}

describe("probeZulip", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("returns ok=true with version info on success", async () => {
    vi.spyOn(globalThis, "fetch").mockImplementation(
      mockFetch({
        result: "success",
        zulip_version: "10.0",
        zulip_feature_level: 300,
        push_notifications_enabled: true,
        require_email_format_usernames: true,
        authentication_methods: { password: true },
      }),
    );

    const result = await probeZulip({
      realm: "https://test.zulipchat.com",
      email: "bot@test.zulipchat.com",
      apiKey: "key",
    });

    expect(result.ok).toBe(true);
    expect(result.version).toBe("10.0");
    expect(result.featureLevel).toBe(300);
    expect(result.realm).toBe("https://test.zulipchat.com");
    expect(result.latencyMs).toBeGreaterThanOrEqual(0);
  });

  it("returns ok=false on network error", async () => {
    vi.spyOn(globalThis, "fetch").mockRejectedValue(new Error("ECONNREFUSED"));

    const result = await probeZulip({
      realm: "https://down.zulipchat.com",
      email: "bot@test.zulipchat.com",
      apiKey: "key",
    });

    expect(result.ok).toBe(false);
    expect(result.error).toContain("ECONNREFUSED");
    expect(result.version).toBe("unknown");
  });

  it("returns ok=false on API error response", async () => {
    vi.spyOn(globalThis, "fetch").mockImplementation(
      mockFetch({ result: "error", msg: "Unauthorized", code: "UNAUTHORIZED" }, 401),
    );

    const result = await probeZulip({
      realm: "https://test.zulipchat.com",
      email: "bot@test.zulipchat.com",
      apiKey: "bad-key",
    });

    expect(result.ok).toBe(false);
    expect(result.error).toContain("probe failed");
  });
});
