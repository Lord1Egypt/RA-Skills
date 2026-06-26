// G.workspace OpenClaw Plugin v3.2.0
// All Discord slash commands proxied to G.workspace REST API (localhost:3080)
// Single bot, no conflict — G.workspace runs web-only.
// v3.0.1: return { text } objects instead of plain strings
// v3.1.0: add sync-choices on startup — PATCH command options with file dropdown
// v3.1.1: improve error messages — distinguish service-down vs API errors
// v3.1.2: fix package.json extension path (./src/index.ts → ./index.ts)
// v3.1.3: ws_create adds force option; prompt user when workspace exists
// v3.1.4: dedupe guard (prevent multi-register); friendlier create prompt
// v3.2.0: replace force:yes with interactive confirm button; register Discord interactive handler
// v3.2.1: restore options arrays for Discord slash command parameter registration

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

const GW_BASE = "http://localhost:3080";

async function gwFetch(method: string, path: string, body?: any): Promise<any> {
  const opts: any = { method, headers: { "Content-Type": "application/json" }, signal: AbortSignal.timeout(8000) };
  if (body) opts.body = JSON.stringify(body);
  let res: Response;
  try {
    res = await fetch(`${GW_BASE}${path}`, opts);
  } catch (err: any) {
    if (err?.name === "AbortError" || err?.code === "UND_ERR_CONNECT_TIMEOUT") {
      throw new Error("G.workspace 服务连接超时，请检查服务是否启动 (localhost:3080)");
    }
    if (err?.cause?.code === "ECONNREFUSED" || err?.message?.includes("ECONNREFUSED") || err?.message === "fetch failed") {
      throw new Error("G.workspace 服务未启动，请先运行后端服务 (localhost:3080)");
    }
    throw new Error("网络错误: " + (err?.message || String(err)));
  }
  const ct = res.headers.get("content-type") || "";
  const data = ct.includes("json") ? await res.json() : await res.text();
  if (!res.ok) {
    const msg = typeof data === "object" ? (data.error || JSON.stringify(data)) : data;
    throw new Error(msg);
  }
  return data;
}

function extractGuildId(ctx: any): string | undefined {
  const raw = ctx.to || ctx.guildId;
  if (!raw) return undefined;
  const match = String(raw).match(/(\d{10,})/);
  return match ? match[1] : String(raw);
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / 1024 / 1024).toFixed(1) + " MB";
}

const ok = (text: string) => ({ text });

export default definePluginEntry({
  id: "gworkspace",
  name: "G.workspace",
  description: "Shared file space — slash commands via REST API",

  register(api) {

    const logger = (api as any).logger;

    // ── /ws_create [name] ──
    api.registerCommand({
      name: "ws_create",
      description: "🗂️ 创建群共享文件空间",
      options: [
        { name: "name", description: "空间名称（不填则用服务器名）", type: "string", required: false },
      ],
      acceptsArgs: true,
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID，请在Discord群内使用此命令");
        const args: any = ctx.args;
        const name = (typeof args === "object" ? args?.name : undefined) || undefined;
        try {
          const data = await gwFetch("POST", `/api/guild/${guildId}/create`, { name });
          if (data.existed) {
            // Interactive buttons for confirmation (works on Discord, Telegram, Slack)
            const confirmValue = name ? `confirm_create:${name}` : "confirm_create";
            return {
              text: `ℹ️ 本群已有空间：**${data.name}**\n📁 文件: ${data.stats.fileCount} · 👥 成员: ${data.stats.memberCount}\n🔗 ${GW_BASE}/w/${data.workspace_id}\n\n是否继续创建新空间？`,
              interactive: {
                blocks: [
                  {
                    type: "buttons" as const,
                    buttons: [
                      { label: "✅ 继续创建", value: confirmValue, style: "primary" as const },
                      { label: "❌ 取消", value: "cancel_create", style: "secondary" as const },
                    ],
                  },
                ],
              },
            };
          }
          return ok(`🗂️ 空间创建成功！\n\n📛 名称: **${data.name}**\n📁 默认文件夹: 📦产品 · ⚙️技术 · 🎨设计\n🔗 Web: ${GW_BASE}/w/${data.workspace_id}`);
        } catch (e: any) {
          return ok("❌ 创建失败: " + e.message);
        }
      },
    });

    // ── Discord Interactive Handler (button clicks) ──
    api.registerInteractiveHandler({
      channel: "discord",
      namespace: "gworkspace",
      handler: async (ctx) => {
        const payload = ctx.interaction.payload;
        const guildId = ctx.guildId;

        // ── Confirm create ──
        if (payload.startsWith("confirm_create")) {
          if (!guildId) {
            await ctx.respond.reply({ text: "❌ 无法获取服务器ID", ephemeral: true });
            return { handled: true };
          }
          const name = payload.includes(":") ? payload.split(":").slice(1).join(":") : undefined;
          try {
            await ctx.respond.acknowledge();
            const data = await gwFetch("POST", `/api/guild/${guildId}/create`, { name, force: true });
            await ctx.respond.clearComponents({
              text: `🗂️ 新空间创建成功！\n\n📛 名称: **${data.name}**\n📁 默认文件夹: 📦产品 · ⚙️技术 · 🎨设计\n🔗 Web: ${GW_BASE}/w/${data.workspace_id}`,
            });
          } catch (e: any) {
            await ctx.respond.clearComponents({
              text: "❌ 创建失败: " + e.message,
            });
          }
          return { handled: true };
        }

        // ── Cancel create ──
        if (payload === "cancel_create") {
          await ctx.respond.clearComponents({
            text: "❌ 已取消创建新空间",
          });
          return { handled: true };
        }

        return { handled: false };
      },
    });

    // ── /ws_info ──
    api.registerCommand({
      name: "ws_info",
      description: "📊 查看空间信息和统计",
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          const members = data.members?.map((m: any) => `${m.role === 'admin' ? '👑' : '👤'} ${m.nickname}`).join(", ") || "无";
          return ok(`🗂️ **${data.name}**\n\n📁 文件: ${data.stats.fileCount}\n👥 成员: ${data.stats.memberCount}\n💾 占用: ${formatSize(data.stats.totalSize)}\n👥 成员列表: ${members}\n🔗 ${GW_BASE}/w/${data.workspace_id}`);
        } catch (e: any) {
          return ok("❌ " + e.message);
        }
      },
    });

    // ── /ws_files [folder] ──
    api.registerCommand({
      name: "ws_files",
      description: "📋 查看空间文件列表",
      options: [{ name: "folder", description: "文件夹筛选", type: "string", required: false }],
      acceptsArgs: true,
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          const wsId = data.workspace_id;
          const args: any = ctx.args;
          const folder = typeof args === "object" ? args?.folder : (typeof args === "string" ? args.trim() || undefined : undefined);
          const q = folder ? `?folder=${encodeURIComponent(folder)}` : "";
          const filesData = await gwFetch("GET", `/w/${wsId}/api/files${q}`);
          const files = filesData.files;
          if (!files || files.length === 0) return ok(`🗂️ **${data.name}** — 暂无文件\n\n使用 \`/ws_upload\` 上传第一个文件`);
          const list = files.slice(0, 20).map((f: any) => {
            const folder = f.folder_name ? `[${f.folder_name}]` : "";
            return `📄 **${f.filename}** ${folder} — v${f.current_version} · ${formatSize(f.size)}${f.summary ? `\n   ${f.summary}` : ""}`;
          }).join("\n");
          return ok(`🗂️ **${data.name}** (${files.length}个文件)\n\n${list}${files.length > 20 ? `\n\n...共${files.length}个文件` : ""}`);
        } catch (e: any) {
          return ok("❌ " + e.message);
        }
      },
    });

    // ── /ws_file <filename> ──
    api.registerCommand({
      name: "ws_file",
      description: "📄 查看文件详情",
      options: [{ name: "filename", description: "文件名（输入关键词搜索）", type: "string", required: true }],
      acceptsArgs: true,
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          const args: any = ctx.args;
          const filename = typeof args === "object" ? args?.filename : (typeof args === "string" ? args.trim() : "");
          const file = data.files?.find((f: any) => f.filename === filename);
          if (!file) {
            const keyword = (filename || "").toLowerCase();
            const matches = data.files?.filter((f: any) => f.filename.toLowerCase().includes(keyword)) || [];
            if (matches.length === 0) return ok(`❌ 找不到文件: ${filename}\n\n💡 使用 /ws_files 查看所有文件`);
            if (matches.length === 1) {
              const f = matches[0];
              return ok(`📄 **${f.filename}**\n📝 ${f.summary || "无摘要"}\n📁 ${f.folder || "根目录"} · v${f.current_version}\n🔗 ${GW_BASE}/w/${data.workspace_id}/preview/${f.id}`);
            }
            return ok(`🔍 匹配到 ${matches.length} 个文件:\n${matches.map((f: any) => `• **${f.filename}** [${f.folder || "根目录"}]`).join("\n")}\n\n请输入完整文件名`);
          }
          return ok(`📄 **${file.filename}**\n📝 ${file.summary || "无摘要"}\n📁 ${file.folder || "根目录"} · v${file.current_version}\n🔗 ${GW_BASE}/w/${data.workspace_id}/preview/${file.id}`);
        } catch (e: any) {
          return ok("❌ " + e.message);
        }
      },
    });

    // ── /ws_search <keyword> ──
    api.registerCommand({
      name: "ws_search",
      description: "🔍 搜索文件",
      options: [{ name: "keyword", description: "搜索关键词", type: "string", required: true }],
      acceptsArgs: true,
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          const wsId = data.workspace_id;
          const args: any = ctx.args;
          const keyword = typeof args === "object" ? args?.keyword : (typeof args === "string" ? args.trim() : "");
          const q = encodeURIComponent(keyword || "");
          const result = await gwFetch("GET", `/w/${wsId}/api/search?q=${q}`);
          if (!result.results || result.results.length === 0) return ok(`🔍 未找到匹配「${keyword}」的文件`);
          const list = result.results.slice(0, 10).map((f: any) =>
            `📄 **${f.filename}** [${f.folder_name || "根目录"}] v${f.current_version}${f.snippet ? `\n   ...${f.snippet}...` : ""}`
          ).join("\n");
          return ok(`🔍 搜索「${keyword}」— ${result.results.length}个结果\n\n${list}`);
        } catch (e: any) {
          return ok("❌ " + e.message);
        }
      },
    });

    // ── /ws_delete ──
    api.registerCommand({
      name: "ws_delete",
      description: "🗑️ 删除文件（移入回收站）",
      options: [{ name: "filename", description: "选择要删除的文件", type: "string", required: true }],
      acceptsArgs: true,
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          const wsId = data.workspace_id;
          const args: any = ctx.args;
          const filename = typeof args === "object" ? args?.filename : (typeof args === "string" ? args.trim() : "");
          const keyword = (filename || "").toLowerCase();
          const file = data.files?.find((f: any) => f.filename === filename)
            || data.files?.find((f: any) => f.filename.toLowerCase().includes(keyword));
          if (!file) {
            if (data.files && data.files.length > 0) {
              const list = data.files.map((f: any, i: number) => `${i + 1}. 📄 **${f.filename}** [${f.folder || "根目录"}]`).join("\n");
              return ok(`❌ 找不到「${filename}」\n\n📋 当前文件列表:\n${list}\n\n请输入完整文件名重试`);
            }
            return ok(`❌ 找不到文件: ${filename}`);
          }
          await gwFetch("DELETE", `/w/${wsId}/api/files/${file.id}`);
          return ok(`🗑️ **${file.filename}** 已移入回收站\n30天内可使用 \`/ws_trash\` 恢复`);
        } catch (e: any) {
          return ok("❌ 删除失败: " + e.message);
        }
      },
    });

    // ── /ws_versions <filename> ──
    api.registerCommand({
      name: "ws_versions",
      description: "📜 查看文件版本历史",
      options: [{ name: "filename", description: "选择文件", type: "string", required: true }],
      acceptsArgs: true,
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          const wsId = data.workspace_id;
          const args: any = ctx.args;
          const filename = typeof args === "object" ? args?.filename : (typeof args === "string" ? args.trim() : "");
          const keyword = (filename || "").toLowerCase();
          const file = data.files?.find((f: any) => f.filename === filename)
            || data.files?.find((f: any) => f.filename.toLowerCase().includes(keyword));
          if (!file) return ok(`❌ 找不到文件: ${filename}`);
          const result = await gwFetch("GET", `/w/${wsId}/api/files/${file.id}/versions`);
          if (!result.versions || result.versions.length === 0) return ok(`📜 **${file.filename}** — 无版本记录`);
          const list = result.versions.map((v: any) =>
            `**v${v.version}**${v.version === file.current_version ? " ✅当前" : ""} — ${v.summary || "无说明"} · ${new Date(v.created_at).toLocaleDateString()}`
          ).join("\n");
          return ok(`📜 **${file.filename}** — ${result.versions.length}个版本\n\n${list}`);
        } catch (e: any) {
          return ok("❌ " + e.message);
        }
      },
    });

    // ── /ws_ref <filename> ──
    api.registerCommand({
      name: "ws_ref",
      description: "🔗 生成文件引用链接",
      options: [{ name: "filename", description: "选择文件", type: "string", required: true }],
      acceptsArgs: true,
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          const args: any = ctx.args;
          const filename = typeof args === "object" ? args?.filename : (typeof args === "string" ? args.trim() : "");
          const keyword = (filename || "").toLowerCase();
          const file = data.files?.find((f: any) => f.filename === filename)
            || data.files?.find((f: any) => f.filename.toLowerCase().includes(keyword));
          if (!file) return ok(`❌ 找不到文件: ${filename}`);
          const refLink = `workspace://${data.workspace_id}/${file.filename}`;
          return ok(`🔗 **${file.filename}**\n\`\`\`\n${refLink}\n\`\`\`\n💡 复制链接发到群聊中，AI 可以通过链接定位文件内容\n🌐 ${GW_BASE}/w/${data.workspace_id}/preview/${file.id}`);
        } catch (e: any) {
          return ok("❌ " + e.message);
        }
      },
    });

    // ── /ws_upload ──
    api.registerCommand({
      name: "ws_upload",
      description: "📤 上传文件",
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          return ok(`📤 请在 Web 界面上传文件:\n🔗 ${GW_BASE}/w/${data.workspace_id}\n\n或者直接在群内发送文件附件，我会提示保存`);
        } catch (e: any) {
          return ok("❌ " + e.message);
        }
      },
    });

    // ── /ws_trash [action] ──
    api.registerCommand({
      name: "ws_trash",
      description: "🗑️ 管理回收站",
      options: [
        { name: "action", description: "操作: list(查看) / restore(恢复) / empty(清空)", type: "string", required: false },
        { name: "filename", description: "恢复的文件名", type: "string", required: false },
      ],
      acceptsArgs: true,
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          const wsId = data.workspace_id;
          const args: any = ctx.args;
          const action = (typeof args === "object" ? args?.action : (typeof args === "string" ? args.trim().split(/\s+/)[0] : "")) || "list";
          const filename = typeof args === "object" ? args?.filename : undefined;

          if (action === "list" || !action) {
            const result = await gwFetch("GET", `/w/${wsId}/api/trash`);
            if (!result.files || result.files.length === 0) return ok("🗑️ 回收站是空的");
            const list = result.files.map((f: any) => {
              const daysAgo = Math.floor((Date.now() - new Date(f.deleted_at).getTime()) / 86400000);
              return `📄 **${f.filename}** · ${formatSize(f.size)} · 删除${daysAgo}天前 · 剩${Math.max(0, 30 - daysAgo)}天`;
            }).join("\n");
            return ok(`🗑️ 回收站 (${result.files.length})\n\n${list}\n\n使用 \`/ws_trash action:restore filename:文件名\` 恢复`);
          }

          if (action === "restore") {
            if (!filename) return ok("❌ 请指定文件名: /ws_trash action:restore filename:文件名");
            const result = await gwFetch("GET", `/w/${wsId}/api/trash`);
            const file = result.files?.find((f: any) => f.filename === filename);
            if (!file) return ok(`❌ 回收站中找不到: ${filename}`);
            await gwFetch("POST", `/w/${wsId}/api/trash/${file.id}/restore`);
            return ok(`✅ **${filename}** 已从回收站恢复`);
          }

          if (action === "empty") {
            const result = await gwFetch("GET", `/w/${wsId}/api/trash`);
            if (!result.files || result.files.length === 0) return ok("🗑️ 回收站已经是空的");
            for (const f of result.files) {
              await gwFetch("DELETE", `/w/${wsId}/api/trash/${f.id}`);
            }
            return ok(`🗑️ 已永久删除 ${result.files.length} 个文件`);
          }

          return ok("❌ 未知操作，可选: list / restore / empty");
        } catch (e: any) {
          return ok("❌ " + e.message);
        }
      },
    });

    // ── /ws_invite ──
    api.registerCommand({
      name: "ws_invite",
      description: "🔗 获取空间访问链接",
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          return ok(`🔗 **${data.name}** 空间链接\n\n🌐 Web: ${GW_BASE}/w/${data.workspace_id}\n📁 文件: ${data.stats.fileCount} · 👥 成员: ${data.stats.memberCount}`);
        } catch (e: any) {
          return ok("❌ " + e.message);
        }
      },
    });

    // ── /ws_members ──
    api.registerCommand({
      name: "ws_members",
      description: "👥 查看空间成员列表",
      handler: async (ctx) => {
        const guildId = extractGuildId(ctx);
        if (!guildId) return ok("❌ 无法获取服务器ID");
        try {
          const data = await gwFetch("GET", `/api/guild/${guildId}`);
          if (!data.members || data.members.length === 0) return ok("👥 暂无成员");
          const list = data.members.map((m: any) =>
            `${m.role === 'admin' ? '👑' : '👤'} **${m.nickname}** (${m.role})`
          ).join("\n");
          return ok(`👥 **${data.name}** — ${data.members.length}位成员\n\n${list}`);
        } catch (e: any) {
          return ok("❌ " + e.message);
        }
      },
    });

    // ═══════════════════════════════════════
    // AGENT TOOLS (for AI batch processing)
    // ═══════════════════════════════════════

    api.registerTool({
      name: "gworkspace_files",
      description: "List files in G.workspace for a guild",
      parameters: {
        type: "object",
        properties: { guild_id: { type: "string", description: "Discord guild (server) ID" } },
        required: ["guild_id"],
      },
      handler: async ({ guild_id }: { guild_id: string }) => {
        const data = await gwFetch("GET", `/api/guild/${guild_id}`);
        return JSON.stringify({ workspace_id: data.workspace_id, name: data.name, files: data.files, stats: data.stats });
      },
    });

    api.registerTool({
      name: "gworkspace_create",
      description: "Create a G.workspace for a guild",
      parameters: {
        type: "object",
        properties: {
          guild_id: { type: "string", description: "Discord guild ID" },
          name: { type: "string", description: "Workspace name" },
        },
        required: ["guild_id"],
      },
      handler: async ({ guild_id, name }: { guild_id: string; name?: string }) => {
        const data = await gwFetch("POST", `/api/guild/${guild_id}/create`, { name });
        return JSON.stringify(data);
      },
    });

    api.registerTool({
      name: "gworkspace_tasks",
      description: "Get pending annotation tasks for a workspace",
      parameters: {
        type: "object",
        properties: { guild_id: { type: "string", description: "Discord guild ID" } },
        required: ["guild_id"],
      },
      handler: async ({ guild_id }: { guild_id: string }) => {
        const data = await gwFetch("GET", `/api/guild/${guild_id}`);
        const tasks = await gwFetch("GET", `/w/${data.workspace_id}/api/tasks`);
        return JSON.stringify({ workspace_id: data.workspace_id, ...tasks });
      },
    });

    api.registerTool({
      name: "gworkspace_claim_task",
      description: "Claim an annotation task",
      parameters: {
        type: "object",
        properties: {
          workspace_id: { type: "string" },
          task_id: { type: "string" },
          claimed_by: { type: "string" },
        },
        required: ["workspace_id", "task_id", "claimed_by"],
      },
      handler: async ({ workspace_id, task_id, claimed_by }: any) => {
        const data = await gwFetch("POST", `/w/${workspace_id}/api/tasks/${task_id}/claim`, { claimed_by });
        return JSON.stringify(data);
      },
    });

    api.registerTool({
      name: "gworkspace_complete_task",
      description: "Complete an annotation task",
      parameters: {
        type: "object",
        properties: {
          workspace_id: { type: "string" },
          task_id: { type: "string" },
          result_summary: { type: "string" },
        },
        required: ["workspace_id", "task_id", "result_summary"],
      },
      handler: async ({ workspace_id, task_id, result_summary }: any) => {
        const data = await gwFetch("POST", `/w/${workspace_id}/api/tasks/${task_id}/complete`, { result_summary });
        return JSON.stringify(data);
      },
    });

    logger?.info?.("[gworkspace] ✅ Plugin v3.2.1 registered (12 commands + 5 tools + Discord interactive handler)");
  },
});
