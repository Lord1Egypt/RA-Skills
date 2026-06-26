import { collect } from "./collect.js";
import { report } from "./report.js";
const command = process.argv[2];
const dateArg = process.argv[3];
async function main() {
    if (command === "collect") {
        await collect();
    }
    else if (command === "report") {
        report(dateArg);
    }
    else {
        console.log("用法:");
        console.log("  node dist/index.js collect              # 采集今天的 GitLab push events");
        console.log("  node dist/index.js report               # 生成今日提交日报");
        console.log("  node dist/index.js report 2026-03-18    # 生成指定日期的提交日报");
        process.exit(1);
    }
}
main().catch(err => {
    if (err.message === "LOGIN_REQUIRED") {
        console.error("\n程序终止：需要登录 GitLab\n");
    }
    else {
        console.error("\n程序运行失败:");
        console.error(err);
    }
    process.exit(1);
});
//# sourceMappingURL=index.js.map