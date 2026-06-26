/**
 * get-authkey-link.mjs — 生成猫眼 AuthKey 获取链接
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   无需参数（返回固定的 AuthKey 获取链接）
 *
 * 本地调试示例：
 *   node scripts/get-authkey-link.mjs
 *   echo '{}' | node scripts/get-authkey-link.mjs
 *
 * Output（JSON）：
 *   {
 *     success: true,
 *     data: {
 *       authKeyUrl: "https://m.maoyan.com/mtrade/openclaw/token",
 *       description: "猫眼 AuthKey 获取页面，用户可在此获取认证密钥"
 *     }
 *   }
 */
import { run } from "./_shared.mjs";

// 固定的 AuthKey 获取链接（不允许修改或添加参数）
const AUTHKEY_URL = "https://m.maoyan.com/mtrade/openclaw/token";

await run(async () => {
  return {
    authKeyUrl: AUTHKEY_URL,
    description: "猫眼 AuthKey 获取页面，用户可在此获取认证密钥",
    note: "此链接为固定链接，不允许添加任何查询参数",
    instruction: "用户访问此链接后，将看到认证密钥，复制后粘贴到对话中即可",
  };
});
