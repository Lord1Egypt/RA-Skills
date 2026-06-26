/**
 * clear-authkey.mjs — 清除本地保存的猫眼 AuthKey
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   无需参数
 *
 * Output（JSON）：
 *   {
 *     success: true,
 *     data: { cleared: true, hadAuthKey: true }
 *   }
 *   或
 *   {
 *     success: true,
 *     data: { cleared: true, hadAuthKey: false }
 *   }
 */
import { unlinkSync, existsSync } from "fs";
import { run, AUTHKEY_FILE } from "./_shared.mjs";

await run(async () => {
  const hadAuthKey = existsSync(AUTHKEY_FILE);

  if (hadAuthKey) {
    try {
      unlinkSync(AUTHKEY_FILE);
    } catch (error) {
      // 删除失败也返回成功，因为文件可能已经不存在
    }
  }

  return {
    cleared: true,
    hadAuthKey,
  };
});
