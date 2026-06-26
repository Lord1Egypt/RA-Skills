/**
 * 开发用：默认每 10 秒推进一天（与 `npm run auto-worker -- 10` 相同）。
 * 生产节奏请用：`start`（固定 20 分钟）。
 */
export {};

if (process.argv[2] === undefined) {
  process.argv[2] = "10";
}
await import("./auto-worker.js");
