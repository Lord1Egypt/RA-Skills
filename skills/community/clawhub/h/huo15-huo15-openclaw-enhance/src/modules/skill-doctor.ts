/**
 * 模块: 技能巡检（enhance_skill_doctor）
 *
 * 龙虾原生技能（skills）存在于 `{openclawHome}/workspace/skills/` 下。
 * 当本插件通过 ClawHub 安装 huo15-openclaw-{explore,memory,plan,verify}-mode 到 workspace，
 * 用户容易碰到：技能目录缺失 / 残缺 / 未更新。
 *
 * 本工具只做"只读诊断+提示安装命令"，不自动重新安装（避免 cold path 上擅自动用 clawhub）。
 * 真正安装由 index.ts 的 startup 流程统一处理。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import { existsSync, statSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { resolveOpenClawHome } from "../utils/resolve-home.js";

const EXPECTED_SKILLS = [
  "huo15-openclaw-explore-mode",
  "huo15-openclaw-memory-curator",
  "huo15-openclaw-plan-mode",
  "huo15-openclaw-verify-mode",
  "huo15-openclaw-frontend-design",
  "huo15-openclaw-design-director",
  "huo15-openclaw-brand-protocol",
  "huo15-openclaw-design-critique",
  "huo15-openclaw-simplify",
  "huo15-openclaw-security-review",
  "huo15-openclaw-code-review",
];

interface SkillInfo {
  id: string;
  path: string;
  installed: boolean;
  hasSkillMd: boolean;
  version?: string;
  name?: string;
}

function inspect(skillsDir: string, id: string): SkillInfo {
  const path = join(skillsDir, id);
  if (!existsSync(path) || !statSync(path).isDirectory()) {
    return { id, path, installed: false, hasSkillMd: false };
  }
  const entries = readdirSync(path);
  const manifestName = entries.find((f) => /^skill\.(md|json|yaml|yml)$/i.test(f));
  let version: string | undefined;
  let name: string | undefined;
  if (manifestName) {
    try {
      const raw = readFileSync(join(path, manifestName), "utf8");
      const versionMatch = raw.match(/version:\s*["']?([\d.]+)/i);
      const nameMatch = raw.match(/name:\s*["']?([^"'\n]+)/i);
      version = versionMatch?.[1];
      name = nameMatch?.[1]?.trim();
    } catch {
      // ignore
    }
  }
  return { id, path, installed: true, hasSkillMd: !!manifestName, version, name };
}

export function registerSkillDoctor(api: OpenClawPluginApi) {
  api.registerTool(
    ((_ctx: OpenClawPluginToolContext) => ({
      name: "enhance_skill_doctor",
      description: "巡检 enhance 11 个配套技能是否齐全可读，输出修复建议",
      parameters: Type.Object({
        workspace: Type.Optional(Type.String({ description: "workspace 目录" })),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const openclawHome = resolveOpenClawHome(api);
        const workspace = (params.workspace as string | undefined)?.trim() || join(openclawHome, "workspace");
        const skillsDir = join(workspace, "skills");

        if (!existsSync(skillsDir)) {
          return {
            content: [
              {
                type: "text" as const,
                text: [
                  `❌ 技能目录不存在: ${skillsDir}`,
                  "",
                  "修复建议：",
                  `  mkdir -p "${skillsDir}"`,
                  ...EXPECTED_SKILLS.map((id) => `  clawhub install ${id} --dir "${skillsDir}"`),
                ].join("\n"),
              },
            ],
          };
        }

        const results = EXPECTED_SKILLS.map((id) => inspect(skillsDir, id));
        const missing = results.filter((r) => !r.installed);
        const broken = results.filter((r) => r.installed && !r.hasSkillMd);
        const ok = results.filter((r) => r.installed && r.hasSkillMd);

        const lines: string[] = [`🔬 技能巡检 · workspace: ${workspace}`, `目录: ${skillsDir}`, ""];
        if (ok.length) {
          lines.push(`✓ 正常 (${ok.length})：`);
          for (const s of ok) {
            lines.push(`  · ${s.id}${s.version ? ` @ ${s.version}` : ""}${s.name ? ` — ${s.name}` : ""}`);
          }
          lines.push("");
        }
        if (broken.length) {
          lines.push(`⚠️ 存在目录但缺少 SKILL.md/json (${broken.length})：`);
          for (const s of broken) lines.push(`  · ${s.id}`);
          lines.push("");
        }
        if (missing.length) {
          lines.push(`✗ 未安装 (${missing.length})：`);
          for (const s of missing) lines.push(`  · ${s.id}`);
          lines.push("");
          lines.push("修复建议（逐个重新安装）：");
          for (const s of missing) {
            lines.push(`  clawhub install ${s.id} --dir "${skillsDir}"`);
          }
        }
        if (!missing.length && !broken.length) {
          lines.push("🎉 四个技能均正常。");
        }
        return { content: [{ type: "text" as const, text: lines.join("\n") }] };
      },
    })) as any,
    { name: "enhance_skill_doctor" },
  );

  api.logger.info("[enhance] 技能巡检模块已加载（enhance_skill_doctor）");
}
