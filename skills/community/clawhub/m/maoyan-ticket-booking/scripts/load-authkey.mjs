/**
 * load-authkey.mjs — 从本地读取猫眼 AuthKey
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   无需参数
 *
 * 本地调试示例：
 *   node scripts/load-authkey.mjs
 *
 * Output（JSON）：
 *   {
 *     success: true,
 *     data: {
 *       exists: true,
 *       hasToken: true,
 *       userId: "123",
 *       userName: "test",
 *       mobile: "138****1234",
 *       savedAt: "2026-03-26T02:30:00.000Z"
 *     }
 *   }
 *   或
 *   {
 *     success: true,
 *     data: { exists: false }
 *   }
 */
import { readFileSync, existsSync, unlinkSync } from "fs";
import { run, AUTHKEY_FILE } from "./_shared.mjs";

await run(async () => {
  // 检查文件是否存在
  if (!existsSync(AUTHKEY_FILE)) {
    return { exists: false };
  }

  try {
    const content = readFileSync(AUTHKEY_FILE, "utf-8");
    const authKeyData = JSON.parse(content);

    // 检查 AuthKey 是否过期（7天）
    const savedAt = new Date(authKeyData.savedAt || 0);
    const now = new Date();
    const daysDiff = (now - savedAt) / (1000 * 60 * 60 * 24);

    if (daysDiff > 7) {
      // 过期后立即删除文件，避免敏感数据长期留存
      try { unlinkSync(AUTHKEY_FILE); } catch {}
      return {
        exists: true,
        expired: true,
        message: "AuthKey 已过期（超过7天），请重新登录",
      };
    }

    return {
      exists: true,
      expired: false,
      hasToken: !!authKeyData.token,
      userId: authKeyData.userId,
      userName: authKeyData.userName,
      mobile: authKeyData.mobile,
      avatarUrl: authKeyData.avatarUrl,
      savedAt: authKeyData.savedAt,
    };
  } catch (error) {
    // 文件损坏或解析失败
    return {
      exists: false,
      error: `读取 AuthKey 失败: ${error.message}`,
    };
  }
});
