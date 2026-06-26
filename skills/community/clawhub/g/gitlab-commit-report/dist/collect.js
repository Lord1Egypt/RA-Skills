import fs from "fs";
import path from "path";
import { today } from "@bondli-skills/shared/date";
import { connectBrowser } from "@bondli-skills/shared/browser";
import { fetchGroupPushEvents } from "./utils/gitlab-api.js";
import { appendTodayEvents } from "./utils/storage.js";
const baseDir = path.join(process.env.HOME || "~", "/openclaw-skill-data/gitlab-commit-report/");
const configPath = path.join(baseDir, "config.json");
export async function collect() {
    // 确保目录存在
    if (!fs.existsSync(baseDir)) {
        try {
            fs.mkdirSync(baseDir, { recursive: true });
            console.log(`已创建配置目录: ${baseDir}`);
        }
        catch (error) {
            console.error(`创建配置目录失败: ${error.message}`);
            process.exit(1);
        }
    }
    if (!fs.existsSync(configPath)) {
        console.error("错误: 配置文件不存在");
        console.error(`配置文件路径: ${configPath}`);
        console.error("\n请执行以下命令创建配置文件:");
        // 获取当前技能的根目录
        const skillRoot = path.join(path.dirname(new URL(import.meta.url).pathname), "..");
        const examplePath = path.join(skillRoot, "config.example.json");
        console.error(`\n  cp ${examplePath} ${configPath}`);
        console.error("\n然后编辑配置文件填入你的 GitLab 信息");
        process.exit(1);
    }
    const config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
    console.log("启动浏览器...");
    const { browser, page } = await connectBrowser();
    try {
        const targetDate = today();
        console.log(`开始拉取 ${config.groupName} ${targetDate} 的提交数据...`);
        const events = await fetchGroupPushEvents(page, config, targetDate);
        console.log(`共拉取到 ${events.length} 条 push 事件`);
        const newCount = appendTodayEvents(events);
        if (newCount === 0) {
            console.log("本次无新增提交事件（全部已存在）");
        }
        else {
            console.log(`新增 ${newCount} 条事件已保存`);
        }
        console.log("采集完成");
    }
    finally {
        await browser.close();
    }
}
//# sourceMappingURL=collect.js.map