import * as p from "@clack/prompts";
import { existsSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve, dirname } from "node:path";

const SKILL_DIR = resolve(dirname(import.meta.dirname!));
const CONFIG_PATH = resolve(SKILL_DIR, "config.json");
const TEMPLATE_PATH = resolve(SKILL_DIR, "config.template.json");
const ENV_PATH = resolve(SKILL_DIR, ".env");

interface ExistingConfig {
  obsidian_vault?: string;
  cookies?: { weibo?: string; xiaohongshu?: string; wechat?: string };
  asr?: {
    provider?: string;
    iflytek?: { app_id?: string; api_key?: string; api_secret?: string };
    openai?: { api_key?: string; base_url?: string };
  };
}

function loadExisting(): ExistingConfig {
  if (!existsSync(CONFIG_PATH)) return {};
  try {
    return JSON.parse(readFileSync(CONFIG_PATH, "utf-8"));
  } catch {
    return {};
  }
}

function loadExistingEnv(): Record<string, string> {
  if (!existsSync(ENV_PATH)) return {};
  const vars: Record<string, string> = {};
  try {
    for (const line of readFileSync(ENV_PATH, "utf-8").split("\n")) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) continue;
      const eq = trimmed.indexOf("=");
      if (eq === -1) continue;
      const key = trimmed.slice(0, eq).trim();
      let val = trimmed.slice(eq + 1).trim();
      if (
        (val.startsWith('"') && val.endsWith('"')) ||
        (val.startsWith("'") && val.endsWith("'"))
      ) {
        val = val.slice(1, -1);
      }
      vars[key] = val;
    }
  } catch {
    /* ignore */
  }
  return vars;
}

function mask(value: string | undefined): string {
  if (!value) return "";
  if (value.length <= 8) return "****";
  return value.slice(0, 4) + "****" + value.slice(-4);
}

function cancelled(): never {
  p.cancel("已取消配置。");
  process.exit(0);
}

async function main() {
  const args = process.argv.slice(2);
  const vaultIdx = args.indexOf("--vault");
  if (vaultIdx !== -1 && vaultIdx + 1 < args.length) {
    const vault = args[vaultIdx + 1];
    if (!existsSync(vault)) {
      console.error(`错误：路径不存在 "${vault}"`);
      process.exit(1);
    }
    writeFileSync(
      CONFIG_PATH,
      JSON.stringify({ obsidian_vault: vault }, null, 2) + "\n",
    );
    console.log(`已写入 ${CONFIG_PATH}`);
    return;
  }

  p.intro("LinkMind Setup");

  const existing = loadExisting();
  const existingEnv = loadExistingEnv();

  if (existsSync(CONFIG_PATH)) {
    p.log.info("检测到已有配置，当前值将作为默认值。");
  }

  // --- 1. Obsidian vault path (required) ---

  const vaultPath = await p.text({
    message: "Obsidian 知识库的绝对路径",
    placeholder: "/Users/yourname/MyVault",
    initialValue: existing.obsidian_vault || "",
    validate: (v = "") => {
      if (!v.trim()) return "路径不能为空";
      if (!existsSync(v.trim())) return `路径不存在: ${v.trim()}`;
    },
  });
  if (p.isCancel(vaultPath)) cancelled();

  // --- 2. Cookies (optional → .env) ---

  const wantCookies = await p.confirm({
    message: "是否配置平台 Cookie？（可选，仅用于获取需登录的内容，不配置不影响基础功能）",
    initialValue: false,
  });
  if (p.isCancel(wantCookies)) cancelled();

  let weiboCookie = "";
  let xhsCookie = "";
  let wxmpCookie = "";

  if (wantCookies) {
    p.log.info(
      "获取 Cookie：在浏览器中登录平台 → F12 → Application → Cookies → 复制为分号分隔字符串",
    );

    const prevWeibo =
      existingEnv.LINKMIND_WEIBO_COOKIE || existing.cookies?.weibo || "";
    const wb = await p.text({
      message: `微博 Cookie${prevWeibo ? "（已有配置，回车保留）" : "（可留空）"}`,
      placeholder: "SUB=xxx; SUBP=yyy",
      initialValue: prevWeibo,
    });
    if (!p.isCancel(wb)) weiboCookie = wb.trim();

    const prevXhs =
      existingEnv.LINKMIND_XHS_COOKIE || existing.cookies?.xiaohongshu || "";
    const xhs = await p.text({
      message: `小红书 Cookie${prevXhs ? "（已有配置，回车保留）" : "（可留空）"}`,
      placeholder: "a1=xxx; web_session=yyy",
      initialValue: prevXhs,
    });
    if (!p.isCancel(xhs)) xhsCookie = xhs.trim();

    const prevWxmp =
      existingEnv.LINKMIND_WXMP_COOKIE || existing.cookies?.wechat || "";
    const wxmp = await p.text({
      message: `微信公众号文章 Cookie${prevWxmp ? "（已有配置，回车保留）" : "（可留空）"}`,
      placeholder: "LINKMIND_WXMP_COOKIE",
      initialValue: prevWxmp,
    });
    if (!p.isCancel(wxmp)) wxmpCookie = wxmp.trim();
  }

  // --- 3. ASR (optional → .env) ---

  const wantAsr = await p.confirm({
    message: "是否配置视频转写 (ASR)？（可选，不配置不影响基础功能，视频帖仍可抓取但无转写）",
    initialValue: false,
  });
  if (p.isCancel(wantAsr)) cancelled();

  let iflytekAppId = "";
  let iflytekApiKey = "";
  let iflytekApiSecret = "";
  let openaiApiKey = "";

  if (wantAsr) {
    const asrProvider = await p.select({
      message: "选择 ASR 服务商",
      options: [
        { value: "iflytek", label: "科大讯飞（推荐，中文效果好）" },
        { value: "openai", label: "OpenAI Whisper" },
        { value: "both", label: "两者都配置（讯飞优先，OpenAI 备选）" },
      ],
    });
    if (p.isCancel(asrProvider)) cancelled();

    if (asrProvider === "iflytek" || asrProvider === "both") {
      p.log.info("讯飞凭据：xfyun.cn → 创建应用 → 开通「语音转写」服务");

      const prevAppId =
        existingEnv.LINKMIND_IFLYTEK_APP_ID ||
        existing.asr?.iflytek?.app_id ||
        "";
      const aid = await p.text({
        message: "讯飞 App ID",
        initialValue: prevAppId,
      });
      if (!p.isCancel(aid)) iflytekAppId = aid.trim();

      const prevApiKey =
        existingEnv.LINKMIND_IFLYTEK_API_KEY ||
        existing.asr?.iflytek?.api_key ||
        "";
      const akey = await p.text({
        message: "讯飞 API Key",
        initialValue: prevApiKey,
      });
      if (!p.isCancel(akey)) iflytekApiKey = akey.trim();

      const prevSecret =
        existingEnv.LINKMIND_IFLYTEK_API_SECRET ||
        existing.asr?.iflytek?.api_secret ||
        "";
      const asec = await p.text({
        message: "讯飞 API Secret",
        initialValue: prevSecret,
      });
      if (!p.isCancel(asec)) iflytekApiSecret = asec.trim();
    }

    if (asrProvider === "openai" || asrProvider === "both") {
      const prevKey =
        existingEnv.LINKMIND_OPENAI_API_KEY ||
        existing.asr?.openai?.api_key ||
        "";
      const okey = await p.text({
        message: "OpenAI API Key",
        placeholder: "sk-xxx",
        initialValue: prevKey,
      });
      if (!p.isCancel(okey)) openaiApiKey = okey.trim();
    }
  }

  // --- 4. Confirmation ---

  const envLines: string[] = [];
  if (weiboCookie) envLines.push(`LINKMIND_WEIBO_COOKIE="${weiboCookie}"`);
  if (xhsCookie) envLines.push(`LINKMIND_XHS_COOKIE="${xhsCookie}"`);
  if (wxmpCookie) envLines.push(`LINKMIND_WXMP_COOKIE="${wxmpCookie}"`);
  if (iflytekAppId) envLines.push(`LINKMIND_IFLYTEK_APP_ID=${iflytekAppId}`);
  if (iflytekApiKey) envLines.push(`LINKMIND_IFLYTEK_API_KEY=${iflytekApiKey}`);
  if (iflytekApiSecret)
    envLines.push(`LINKMIND_IFLYTEK_API_SECRET=${iflytekApiSecret}`);
  if (openaiApiKey) envLines.push(`LINKMIND_OPENAI_API_KEY=${openaiApiKey}`);

  p.log.step("配置预览：");
  p.log.message(`  Obsidian 路径: ${vaultPath}`);
  if (weiboCookie) p.log.message(`  微博 Cookie:   ${mask(weiboCookie)}`);
  if (xhsCookie) p.log.message(`  小红书 Cookie: ${mask(xhsCookie)}`);
  if (wxmpCookie) p.log.message(`  微信 Cookie:   ${mask(wxmpCookie)}`);
  if (iflytekAppId) p.log.message(`  讯飞 App ID:   ${mask(iflytekAppId)}`);
  if (iflytekApiKey) p.log.message(`  讯飞 API Key:  ${mask(iflytekApiKey)}`);
  if (openaiApiKey) p.log.message(`  OpenAI Key:    ${mask(openaiApiKey)}`);

  const confirmed = await p.confirm({
    message: "确认写入？",
    initialValue: true,
  });
  if (p.isCancel(confirmed) || !confirmed) cancelled();

  // --- 5. Write config.json (non-sensitive only) ---

  const config: Record<string, unknown> = {
    obsidian_vault: (vaultPath as string).trim(),
  };
  writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2) + "\n");
  p.log.success(`已写入 config.json`);

  // --- 6. Write .env (sensitive credentials) ---

  if (envLines.length > 0) {
    writeFileSync(ENV_PATH, envLines.join("\n") + "\n");
    p.log.success(`已写入 .env（${envLines.length} 项凭据）`);
  }

  // --- 7. Ensure vault LinkMind directory exists ---

  const linkMindDir = resolve((vaultPath as string).trim(), "LinkMind");
  if (!existsSync(linkMindDir)) {
    mkdirSync(linkMindDir, { recursive: true });
    p.log.info(`已创建笔记目录: ${linkMindDir}`);
  }

  p.outro("配置完成！现在可以使用 LinkMind 了。");
}

main().catch((err) => {
  console.error("Setup failed:", err);
  process.exit(1);
});
