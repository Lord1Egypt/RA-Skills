import fs from "fs";
import path from "path";
import { today } from "@bondli-skills/shared/date";
const DATA_DIR = path.join(process.env.HOME || "~", "/openclaw-skill-data/gitlab-commit-report/");
function ensureDataDir() {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}
export function readEventsByDate(dateStr) {
    ensureDataDir();
    const file = path.join(DATA_DIR, `${dateStr}.json`);
    if (!fs.existsSync(file)) {
        return [];
    }
    try {
        return JSON.parse(fs.readFileSync(file, "utf-8"));
    }
    catch (e) {
        throw new Error(`数据文件解析失败: ${e}`);
    }
}
export function readTodayEvents() {
    ensureDataDir();
    const file = path.join(DATA_DIR, `${today()}.json`);
    if (!fs.existsSync(file)) {
        return [];
    }
    try {
        return JSON.parse(fs.readFileSync(file, "utf-8"));
    }
    catch (e) {
        throw new Error(`数据文件解析失败: ${e}`);
    }
}
export function appendTodayEvents(events) {
    ensureDataDir();
    const file = path.join(DATA_DIR, `${today()}.json`);
    let existing = [];
    if (fs.existsSync(file)) {
        try {
            existing = JSON.parse(fs.readFileSync(file, "utf-8"));
        }
        catch {
            console.warn("⚠️ 当天数据文件损坏，已重置");
            existing = [];
        }
    }
    const existingIds = new Set(existing.flatMap(e => e.commits.map(c => c.id)));
    const newEvents = events.filter(e => e.commits.every(c => !existingIds.has(c.id)));
    if (newEvents.length > 0) {
        fs.writeFileSync(file, JSON.stringify([...existing, ...newEvents], null, 2));
    }
    return newEvents.length;
}
//# sourceMappingURL=storage.js.map