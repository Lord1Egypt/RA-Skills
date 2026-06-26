import { copyFileSync, existsSync } from 'fs';
// 若 skill 根目录仍有旧版 trust_experience.json，则同步到 trust/（迁移用）
const src = 'trust_experience.json';
const dst = 'trust/trust_experience.json';
if (existsSync(src)) copyFileSync(src, dst);
