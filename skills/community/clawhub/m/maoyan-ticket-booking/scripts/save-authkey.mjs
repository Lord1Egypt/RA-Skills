/**
 * save-authkey.mjs — 保存猫眼 AuthKey 到本地
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   authKey    {string}  [必填] 用户认证密钥
 *   userId     {string}  [必填] 用户ID
 *   userName   {string}  [必填] 用户名
 *   mobile     {string}  [可选] 手机号
 *   avatarUrl  {string}  [可选] 头像URL
 *
 * 本地调试示例：
 *   echo '{"authKey":"xxx","userId":"123","userName":"test","mobile":"138****1234"}' | node scripts/save-authkey.mjs
 *
 * Output（JSON）：
 *   {
 *     success: true,
 *     data: { saved: true, userName: "test", mobile: "138****1234" }
 *   }
 */
import {
  ERROR_CODES,
  ScriptError,
  readJsonInput,
  requireFields,
  run,
  mapAuthKey,
  saveAuthKey,
} from "./_shared.mjs";

await run(async () => {
  const input = mapAuthKey(await readJsonInput());
  requireFields(input, ["token", "userId", "userName"]);

  const authKeyData = {
    token: input.token,
    userId: input.userId,
    userName: input.userName,
    mobile: input.mobile || "",
    avatarUrl: input.avatarUrl || "",
    savedAt: new Date().toISOString(),
  };

  try {
    saveAuthKey(authKeyData);
    return {
      saved: true,
      userName: authKeyData.userName,
      mobile: authKeyData.mobile,
    };
  } catch (error) {
    throw new ScriptError(
      ERROR_CODES.UNEXPECTED_ERROR,
      `保存 AuthKey 失败: ${error.message}`
    );
  }
});
