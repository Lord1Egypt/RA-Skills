import os from "node:os";
import path from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";
import { resolvePreferredOpenClawTmpDir } from "openclaw/plugin-sdk/infra-runtime";
import { resolveWecomMediaMaxBytes, resolveWecomMergedMediaLocalRoots } from "./media.js";

describe("resolveWecomMergedMediaLocalRoots", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it("merges defaults with configured local roots", () => {
    vi.stubEnv("OPENCLAW_STATE_DIR", "/tmp/wecom-state");

    const roots = resolveWecomMergedMediaLocalRoots({
      cfg: {
        channels: {
          wecom: {
            media: {
              localRoots: ["~/Downloads", "/tmp/custom-root"],
            },
          },
        },
      } as never,
    });

    expect(roots).toEqual(
      expect.arrayContaining([
        path.resolve(resolvePreferredOpenClawTmpDir()),
        "/tmp/wecom-state",
        "/tmp/wecom-state/media",
        "/tmp/wecom-state/agents",
        "/tmp/wecom-state/workspace",
        "/tmp/wecom-state/sandboxes",
        path.resolve(os.homedir(), "Desktop"),
        path.resolve(os.homedir(), "Documents"),
        path.resolve(os.homedir(), "Downloads"),
        path.resolve(os.homedir(), "Movies"),
        path.resolve(os.homedir(), "Pictures"),
        "/tmp/custom-root",
      ]),
    );
  });

  it("keeps defaults, base roots, and configured roots without duplicates", () => {
    vi.stubEnv("OPENCLAW_STATE_DIR", "/tmp/wecom-state");

    const roots = resolveWecomMergedMediaLocalRoots({
      cfg: {
        channels: {
          wecom: {
            media: {
              localRoots: ["/tmp/agent-root", "/tmp/downloads"],
            },
          },
        },
      } as never,
      baseRoots: ["/tmp/agent-root", "/tmp/workspace-agent"],
    });

    expect(roots).toEqual(
      expect.arrayContaining([
        path.resolve(resolvePreferredOpenClawTmpDir()),
        "/tmp/wecom-state",
        "/tmp/workspace-agent",
        "/tmp/agent-root",
        "/tmp/downloads",
      ]),
    );
    expect(roots.filter((root) => root === "/tmp/agent-root")).toHaveLength(1);
  });
});

describe("resolveWecomMediaMaxBytes", () => {
  it("prefers account mediaMaxMb over channel and agent defaults", () => {
    expect(
      resolveWecomMediaMaxBytes(
        {
          agents: {
            defaults: {
              mediaMaxMb: 12,
            },
          },
          channels: {
            wecom: {
              mediaMaxMb: 24,
              accounts: {
                ops: {
                  mediaMaxMb: 32,
                },
              },
            },
          },
        } as never,
        "ops",
      ),
    ).toBe(32 * 1024 * 1024);
  });

  it("falls back to legacy channels.wecom.media.maxBytes when mediaMaxMb is unset", () => {
    expect(
      resolveWecomMediaMaxBytes({
        channels: {
          wecom: {
            media: {
              maxBytes: 15 * 1024 * 1024,
            },
          },
        },
      } as never),
    ).toBe(15 * 1024 * 1024);
  });
});
