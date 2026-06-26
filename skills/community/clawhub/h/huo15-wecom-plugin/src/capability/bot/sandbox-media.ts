import crypto from "node:crypto";
import { constants } from "node:fs";
import os from "node:os";
import path from "node:path";
import { copyFile, mkdir, stat } from "node:fs/promises";

import type { OpenClawConfig } from "openclaw/plugin-sdk";
import { resolveAgentConfig, resolveAgentWorkspaceDir } from "openclaw/plugin-sdk/agent-runtime";

import { resolveWecomMediaMaxBytes } from "../../config/index.js";

function expandHomeDir(input: string): string {
  if (input === "~") return os.homedir();
  if (input.startsWith("~/")) return path.join(os.homedir(), input.slice(2));
  return input;
}

function resolveOpenClawStateDir(): string {
  const override = process.env.OPENCLAW_STATE_DIR?.trim() || process.env.CLAWDBOT_STATE_DIR?.trim();
  if (override) {
    return path.resolve(expandHomeDir(override));
  }
  return path.join(os.homedir(), ".openclaw");
}

function normalizeAgentId(agentId: string): string {
  return agentId.trim().toLowerCase() || "main";
}

function normalizeMainKey(mainKey: unknown): string {
  return typeof mainKey === "string" && mainKey.trim() ? mainKey.trim().toLowerCase() : "main";
}

function buildAgentMainSessionKey(cfg: OpenClawConfig, agentId: string): string {
  if (cfg.session?.scope === "global") {
    return "global";
  }
  return `agent:${normalizeAgentId(agentId)}:${normalizeMainKey(cfg.session?.mainKey)}`;
}

function slugifySessionKey(value: string): string {
  const trimmed = value.trim() || "session";
  const hash = crypto.createHash("sha256").update(trimmed).digest("hex").slice(0, 8);
  const prefix =
    trimmed
      .toLowerCase()
      .replace(/[^a-z0-9._-]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 32) || "session";
  return `${prefix}-${hash}`;
}

function isSandboxedSession(params: {
  cfg: OpenClawConfig;
  agentId: string;
  sessionKey: string;
}): boolean {
  const sandbox = resolveAgentConfig(params.cfg, params.agentId)?.sandbox;
  if (!sandbox || sandbox.mode === "off") {
    return false;
  }
  if (sandbox.mode === "all") {
    return true;
  }
  return params.sessionKey.trim().toLowerCase() !== buildAgentMainSessionKey(params.cfg, params.agentId);
}

function resolveSessionWorkspaceTarget(params: {
  cfg: OpenClawConfig;
  agentId: string;
  sessionKey: string;
}): { workspaceDir: string; sandboxed: boolean } {
  const sandbox = resolveAgentConfig(params.cfg, params.agentId)?.sandbox;
  const agentWorkspaceDirRaw = resolveAgentWorkspaceDir(params.cfg, params.agentId);
  const agentWorkspaceDir = path.resolve(expandHomeDir(agentWorkspaceDirRaw || process.cwd()));
  if (!sandbox || !isSandboxedSession(params)) {
    return {
      workspaceDir: agentWorkspaceDir,
      sandboxed: false,
    };
  }
  if (sandbox.workspaceAccess === "rw" || !sandbox.workspaceRoot) {
    if (sandbox.workspaceAccess === "rw") {
      return {
        workspaceDir: agentWorkspaceDir,
        sandboxed: true,
      };
    }
    return {
      workspaceDir: path.join(resolveOpenClawStateDir(), "sandboxes", slugifySessionKey(params.sessionKey.trim() || "main")),
      sandboxed: true,
    };
  }

  const workspaceRoot = path.resolve(expandHomeDir(sandbox.workspaceRoot));
  const scopeKey =
    sandbox.scope === "shared"
      ? "shared"
      : sandbox.scope === "session"
        ? params.sessionKey.trim() || "main"
        : `agent:${normalizeAgentId(params.agentId)}`;
  if (sandbox.scope === "shared") {
    return {
      workspaceDir: workspaceRoot,
      sandboxed: true,
    };
  }
  return {
    workspaceDir: path.join(workspaceRoot, slugifySessionKey(scopeKey)),
    sandboxed: true,
  };
}

function buildStagedFilenameCandidate(parsed: path.ParsedPath, suffix: number): string {
  if (suffix === 0) {
    return parsed.base || "attachment";
  }
  return `${parsed.name || "attachment"}-${suffix}${parsed.ext}`;
}

async function copyIntoWorkspaceInbound(params: {
  sourcePath: string;
  workspaceDir: string;
  filename: string;
}): Promise<{ absolutePath: string; relativePath: string }> {
  const inboundDir = path.join(params.workspaceDir, "media", "inbound");
  await mkdir(inboundDir, { recursive: true });

  const parsed = path.parse(params.filename);
  for (let suffix = 0; ; suffix += 1) {
    const candidate = buildStagedFilenameCandidate(parsed, suffix);
    const absolutePath = path.join(inboundDir, candidate);
    try {
      await copyFile(params.sourcePath, absolutePath, constants.COPYFILE_EXCL);
      return {
        absolutePath,
        relativePath: path.posix.join("media", "inbound", candidate),
      };
    } catch (error) {
      if ((error as NodeJS.ErrnoException)?.code === "EEXIST") {
        continue;
      }
      throw error;
    }
  }
}

export async function stageWecomInboundMediaForSession(params: {
  cfg: OpenClawConfig;
  accountId: string;
  agentId: string;
  sessionKey: string;
  mediaPath: string;
  filename?: string;
}): Promise<string> {
  const target = resolveSessionWorkspaceTarget({
    cfg: params.cfg,
    agentId: params.agentId,
    sessionKey: params.sessionKey,
  });

  const maxBytes = resolveWecomMediaMaxBytes(params.cfg, params.accountId);
  const sourceStat = await stat(params.mediaPath);
  if (sourceStat.size > maxBytes) {
    throw new Error(
      `Inbound media size ${(sourceStat.size / (1024 * 1024)).toFixed(2)}MB exceeds channels.wecom.mediaMaxMb ${(maxBytes / (1024 * 1024)).toFixed(2)}MB before workspace staging`,
    );
  }

  const staged = await copyIntoWorkspaceInbound({
    sourcePath: params.mediaPath,
    workspaceDir: target.workspaceDir,
    filename: params.filename || path.basename(params.mediaPath),
  });
  return target.sandboxed ? staged.relativePath : staged.absolutePath;
}
