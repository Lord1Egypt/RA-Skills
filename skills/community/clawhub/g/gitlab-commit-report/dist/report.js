import fs from "fs";
import path from "path";
import { today } from "@bondli-skills/shared/date";
import { readEventsByDate } from "./utils/storage.js";
const baseDir = path.join(process.env.HOME || "~", "/openclaw-skill-data/gitlab-commit-report/");
function aggregate(events) {
    const authorMap = new Map();
    const projectMap = new Map();
    let totalCommits = 0;
    for (const event of events) {
        totalCommits += event.commitCount;
        const authorKey = event.authorUsername;
        const existing = authorMap.get(authorKey);
        if (existing) {
            existing.count += event.commitCount;
        }
        else {
            authorMap.set(authorKey, {
                author: event.author,
                authorUsername: event.authorUsername,
                count: event.commitCount,
            });
        }
        const projectKey = event.projectPath;
        const existingProject = projectMap.get(projectKey);
        if (existingProject) {
            existingProject.count += event.commitCount;
        }
        else {
            projectMap.set(projectKey, {
                projectName: event.projectName,
                projectPath: event.projectPath,
                count: event.commitCount,
            });
        }
    }
    const top10Authors = Array.from(authorMap.values())
        .sort((a, b) => b.count - a.count)
        .slice(0, 10);
    const top5Projects = Array.from(projectMap.values())
        .sort((a, b) => b.count - a.count)
        .slice(0, 5);
    return {
        totalCommits,
        activeAuthors: authorMap.size,
        activeProjects: projectMap.size,
        top10Authors,
        top5Projects,
        events,
    };
}
function formatTime(isoString) {
    const d = new Date(isoString);
    const hh = String(d.getHours()).padStart(2, "0");
    const mm = String(d.getMinutes()).padStart(2, "0");
    return `${hh}:${mm}`;
}
function buildMarkdown(data, dateStr) {
    const lines = [];
    lines.push(`# GitLab 代码提交日报 - ${dateStr}`);
    lines.push("");
    lines.push("## 概览");
    lines.push("");
    lines.push(`- 提交总次数：${data.totalCommits}`);
    lines.push(`- 活跃提交人数：${data.activeAuthors} 人`);
    lines.push(`- 涉及仓库数：${data.activeProjects} 个`);
    lines.push("");
    lines.push("## Top 10 提交者");
    lines.push("");
    lines.push("| 排名 | 姓名 | 提交次数 |");
    lines.push("|------|------|---------|");
    data.top10Authors.forEach((item, i) => {
        lines.push(`| ${i + 1} | ${item.author} | ${item.count} |`);
    });
    lines.push("");
    lines.push("## Top 5 活跃仓库");
    lines.push("");
    lines.push("| 排名 | 仓库 | 提交次数 |");
    lines.push("|------|------|---------|");
    data.top5Projects.forEach((item, i) => {
        lines.push(`| ${i + 1} | ${item.projectName} | ${item.count} |`);
    });
    lines.push("");
    lines.push("## 提交明细");
    lines.push("");
    lines.push("| 时间 | 提交人 | 仓库 | 提交信息 |");
    lines.push("|------|--------|------|---------|");
    const sorted = [...data.events].sort((a, b) => new Date(b.pushedAt).getTime() - new Date(a.pushedAt).getTime());
    for (const event of sorted) {
        const time = formatTime(event.pushedAt);
        if (event.commits.length > 0) {
            for (const commit of event.commits) {
                const msg = commit.message.split("\n")[0].slice(0, 80);
                lines.push(`| ${time} | ${event.author} | ${event.projectName} | ${msg} |`);
            }
        }
        else {
            lines.push(`| ${time} | ${event.author} | ${event.projectName} | (共 ${event.commitCount} 次提交) |`);
        }
    }
    lines.push("");
    return lines.join("\n");
}
export function report(dateStr) {
    const targetDate = dateStr ?? today();
    const events = readEventsByDate(targetDate);
    if (events.length === 0) {
        console.log(`${targetDate} 暂无采集数据，请先运行 collect 命令`);
        return;
    }
    console.log(`共读取 ${events.length} 条 push 事件，正在聚合统计...`);
    const data = aggregate(events);
    const markdown = buildMarkdown(data, targetDate);
    if (!fs.existsSync(baseDir)) {
        fs.mkdirSync(baseDir, { recursive: true });
    }
    const reportFile = path.join(baseDir, `${targetDate}.md`);
    fs.writeFileSync(reportFile, markdown);
    console.log(`日报已生成: ${reportFile}`);
    console.log(`\n提交总次数: ${data.totalCommits}`);
    console.log(`活跃提交人数: ${data.activeAuthors} 人`);
    console.log(`涉及仓库数: ${data.activeProjects} 个`);
}
//# sourceMappingURL=report.js.map