/**
 * validate-maoyan-authkey.mjs — 校验猫眼用户 AuthKey 是否有效
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   authKey {string}  [必填] 猫眼用户认证密钥
 *             authKey 通过 Cookie 中的 token 字段传递给接口
 *
 * Output（JSON）：
 *   {
 *     isValid    {boolean}  authKey 是否有效
 *     userId     {string}   用户 ID
 *     userName   {string}   用户名
 *     nickName   {string}   昵称（可能为 null）
 *     mobile     {string}   手机号（脱敏）
 *     authKey    {string}   当前 authKey
 *     avatarUrl  {string}   头像 URL
 *   }
 */
import {
  ERROR_CODES,
  ScriptError,
  readJsonInput,
  requireFields,
  run,
  generateMaoyanHeaders,
  mapAuthKey,
  DEFAULT_TIMEOUT_MS,
} from "./_shared.mjs";

const MAOYAN_API_URL = "https://m.maoyan.com/mtrade/user/token";

await run(async () => {
  const input = mapAuthKey(await readJsonInput());

  const token = input.token || "";

  if (!token) {
    throw new ScriptError(ERROR_CODES.INVALID_INPUT, "缺少必要字段：authKey");
  }

  // token 通过 Cookie header 传递给猫眼接口
  // 过滤 token 中可能导致 Cookie header 注入的非法字符
  const safeToken = token.replace(/[;\s\n\r]/g, "");
  const cookieHeader = `token=${safeToken}`;

  const controller = new AbortController();
  const timer = setTimeout(
    () => controller.abort(),
    DEFAULT_TIMEOUT_MS
  );

  let res;
  try {
    res = await fetch(MAOYAN_API_URL, {
      method: "GET",
      headers: generateMaoyanHeaders({
        token,
        uuid: input.uuid,
        extraHeaders: { Cookie: cookieHeader },
      }),
      signal: controller.signal,
    });
  } catch (error) {
    if (error.name === "AbortError") {
      throw new ScriptError(ERROR_CODES.TIMEOUT, "请求超时");
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }

  if (!res.ok) {
    throw new ScriptError(
      ERROR_CODES.HTTP_ERROR,
      `猫眼接口请求失败，状态码 ${res.status}`
    );
  }

  const json = await res.json();

  if (!json.success || !json.data) {
    throw new ScriptError(ERROR_CODES.TOKEN_INVALID, "AuthKey 无效或已过期");
  }

  const data = json.data;

  return {
    isValid: true,
    userId: String(data.userId || ""),
    userName: data.userName || "",
    nickName: data.nickName || null,
    mobile: data.mobile || "",
    authKey: data.token || token,
    avatarUrl: data.avatarUrl || "",
  };
});
