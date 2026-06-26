import path from "node:path";
import { mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises";

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { stageWecomInboundMediaForSession } from "./sandbox-media.js";

describe("stageWecomInboundMediaForSession", () => {
  const root = path.join("/tmp", `wecom-sandbox-stage-${process.pid}`);

  beforeEach(async () => {
    await mkdir(root, { recursive: true });
  });

  afterEach(async () => {
    vi.unstubAllEnvs();
    await rm(root, { recursive: true, force: true });
  });

  it("stages inbound media into the session sandbox workspace using channels.wecom.mediaMaxMb", async () => {
    const mediaPath = path.join(root, "openclaw-media", "inbound", "big.bin");
    const agentWorkspace = path.join(root, "agent-workspace");
    const sandboxRoot = path.join(root, "sandboxes");

    await mkdir(path.dirname(mediaPath), { recursive: true });
    await mkdir(agentWorkspace, { recursive: true });
    await writeFile(mediaPath, Buffer.alloc(6 * 1024 * 1024, 7));

    const staged = await stageWecomInboundMediaForSession({
      cfg: {
        channels: {
          wecom: {
            mediaMaxMb: 8,
          },
        },
        agents: {
          list: [
            {
              id: "ops",
              workspace: agentWorkspace,
              sandbox: {
                mode: "non-main",
                scope: "session",
                workspaceRoot: sandboxRoot,
                workspaceAccess: "ro",
                docker: {
                  workdir: "/workspace",
                },
              },
            },
          ],
        },
      } as any,
      accountId: "default",
      agentId: "ops",
      sessionKey: "agent:ops:wecom:default:dm:zhangsan",
      mediaPath,
      filename: "big.bin",
    });

    expect(staged).toMatch(/^media\/inbound\/big\.bin$/);
    const sandboxEntries = await readdir(sandboxRoot);
    const stagedBuffer = await readFile(
      path.join(sandboxRoot, sandboxEntries[0]!, "media", "inbound", "big.bin"),
    );
    expect(stagedBuffer.byteLength).toBe(6 * 1024 * 1024);
  });

  it("uses the default sandbox workspace root when workspaceRoot is omitted", async () => {
    vi.stubEnv("OPENCLAW_STATE_DIR", root);
    const mediaPath = path.join(root, "openclaw-media", "inbound", "default-root.bin");
    const agentWorkspace = path.join(root, "agent-workspace");

    await mkdir(path.dirname(mediaPath), { recursive: true });
    await mkdir(agentWorkspace, { recursive: true });
    await writeFile(mediaPath, Buffer.alloc(2 * 1024 * 1024, 5));

    const staged = await stageWecomInboundMediaForSession({
      cfg: {
        channels: {
          wecom: {
            mediaMaxMb: 8,
          },
        },
        agents: {
          list: [
            {
              id: "ops",
              workspace: agentWorkspace,
              sandbox: {
                mode: "non-main",
                scope: "session",
                workspaceAccess: "ro",
                docker: {
                  workdir: "/workspace",
                },
              },
            },
          ],
        },
      } as any,
      accountId: "default",
      agentId: "ops",
      sessionKey: "agent:ops:wecom:default:dm:lisi",
      mediaPath,
      filename: "default-root.bin",
    });

    expect(staged).toMatch(/^media\/inbound\/default-root\.bin$/);
    const sandboxEntries = await readdir(path.join(root, "sandboxes"));
    const stagedBuffer = await readFile(
      path.join(root, "sandboxes", sandboxEntries[0]!, "media", "inbound", "default-root.bin"),
    );
    expect(stagedBuffer.byteLength).toBe(2 * 1024 * 1024);
  });

  it("stages inbound media into the agent workspace for non-sandbox sessions", async () => {
    const mediaPath = path.join(root, "openclaw-media", "inbound", "small.bin");
    const agentWorkspace = path.join(root, "agent-workspace");

    await mkdir(path.dirname(mediaPath), { recursive: true });
    await mkdir(agentWorkspace, { recursive: true });
    await writeFile(mediaPath, Buffer.alloc(1024, 1));

    const staged = await stageWecomInboundMediaForSession({
      cfg: {
        channels: {
          wecom: {
            mediaMaxMb: 8,
          },
        },
        agents: {
          list: [
            {
              id: "ops",
              workspace: agentWorkspace,
              sandbox: {
                mode: "off",
                scope: "session",
                workspaceRoot: path.join(root, "sandboxes"),
                workspaceAccess: "ro",
                docker: {
                  workdir: "/workspace",
                },
              },
            },
          ],
        },
      } as any,
      accountId: "default",
      agentId: "ops",
      sessionKey: "agent:ops:wecom:default:dm:zhangsan",
      mediaPath,
      filename: "small.bin",
    });

    expect(staged).toBe(path.join(agentWorkspace, "media", "inbound", "small.bin"));
    const stagedBuffer = await readFile(staged);
    expect(stagedBuffer.byteLength).toBe(1024);
  });

  it("allocates distinct staged filenames for concurrent same-name uploads", async () => {
    const mediaPathA = path.join(root, "openclaw-media", "inbound", "dup-a.bin");
    const mediaPathB = path.join(root, "openclaw-media", "inbound", "dup-b.bin");
    const agentWorkspace = path.join(root, "agent-workspace");

    await mkdir(path.dirname(mediaPathA), { recursive: true });
    await mkdir(agentWorkspace, { recursive: true });
    await writeFile(mediaPathA, Buffer.from("first"));
    await writeFile(mediaPathB, Buffer.from("second"));

    const cfg = {
      channels: {
        wecom: {
          mediaMaxMb: 8,
        },
      },
      agents: {
        list: [
          {
            id: "ops",
            workspace: agentWorkspace,
            sandbox: {
              mode: "off",
              scope: "session",
              workspaceAccess: "ro",
              docker: {
                workdir: "/workspace",
              },
            },
          },
        ],
      },
    } as any;

    const [stagedA, stagedB] = await Promise.all([
      stageWecomInboundMediaForSession({
        cfg,
        accountId: "default",
        agentId: "ops",
        sessionKey: "agent:ops:wecom:default:dm:zhangsan",
        mediaPath: mediaPathA,
        filename: "dup.bin",
      }),
      stageWecomInboundMediaForSession({
        cfg,
        accountId: "default",
        agentId: "ops",
        sessionKey: "agent:ops:wecom:default:dm:lisi",
        mediaPath: mediaPathB,
        filename: "dup.bin",
      }),
    ]);

    expect(stagedA).not.toBe(stagedB);
    expect([path.basename(stagedA), path.basename(stagedB)].sort()).toEqual(["dup-1.bin", "dup.bin"]);
    expect((await readFile(stagedA)).toString()).toMatch(/first|second/);
    expect((await readFile(stagedB)).toString()).toMatch(/first|second/);
    expect((await readFile(stagedA)).toString()).not.toBe((await readFile(stagedB)).toString());
  });
});
