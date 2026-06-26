#!/usr/bin/env node
/**
 * @deprecated
 * 
 * milestone-execution v2.x 的启动脚本，已被 milestone-executor 取代。
 * 
 * 请使用 milestone-executor 代替：
 *   milestone-executor start "任务" "m1|m2|m3"
 * 
 * 旧版用法（不再支持）：
 *   node start.js --task "任务" --milestones "m1,m2,m3"
 */

console.log(`
⚠️ start.js 已弃用

请改用 milestone-executor：
  milestone-executor start "任务描述" "m1|m2|m3"

或者使用完整路径：
  ~/.openclaw/skills/milestone-execution/scripts/milestone-executor start "任务" "m1|m2|m3"
`);

process.exit(0);
