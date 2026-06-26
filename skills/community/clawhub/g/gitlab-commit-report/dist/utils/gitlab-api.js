function decodeHtmlEntities(str) {
    return str
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/&middot;/g, "·")
        .replace(/&nbsp;/g, " ");
}
function parseActivityHtml(html) {
    const results = [];
    const eventItemRegex = /<div class="event-item">([\s\S]*?)<\/div>\s*(?=<div class="event-item"|$)/g;
    let match;
    while ((match = eventItemRegex.exec(html)) !== null) {
        const block = match[1];
        const eventTypeMatch = block.match(/<span class="event-type[^"]*">([\s\S]*?)<\/span>/);
        const eventType = eventTypeMatch?.[1]?.trim() ?? "";
        if (!eventType.includes("pushed to branch") && !eventType.includes("pushed new branch")) {
            continue;
        }
        const datetimeMatch = block.match(/datetime="([^"]+)"/);
        const pushedAt = datetimeMatch?.[1] ?? "";
        const authorMatch = block.match(/<span class="author-name">\s*<a[^>]*href="\/([^"]+)"[^>]*>([\s\S]*?)<\/a>/);
        const authorUsername = authorMatch?.[1]?.trim() ?? "";
        const authorName = authorMatch?.[2]?.trim() ?? authorUsername;
        const projectNameMatch = block.match(/<span class="project-name">([\s\S]*?)<\/span>/);
        const projectName = projectNameMatch?.[1]?.trim() ?? "";
        const projectLinkMatch = block.match(/<a[^>]*class="gl-link"[^>]*href="\/([^"]+)"[^>]*>/);
        const projectPath = projectLinkMatch?.[1]?.trim() ?? "";
        const commitShaMatch = block.match(/<a class="commit-sha"[^>]*href="[^"]*\/-\/commit\/([a-f0-9]+)"/);
        const commitId = commitShaMatch?.[1] ?? "";
        const commitRowMatch = block.match(/<div class="commit-row-title">([\s\S]*?)<\/div>/);
        let commitMessage = "";
        if (commitRowMatch) {
            const rawRow = commitRowMatch[1];
            const afterMiddot = rawRow.replace(/<a[^>]*>[\s\S]*?<\/a>/, "").replace(/&middot;/g, "").trim();
            commitMessage = decodeHtmlEntities(afterMiddot.replace(/<[^>]+>/g, "").trim());
        }
        if (!pushedAt || !authorUsername || !projectName)
            continue;
        results.push({
            author: authorName,
            authorUsername,
            projectName,
            projectPath,
            commitId,
            commitMessage,
            pushedAt,
        });
    }
    return results;
}
export async function checkLogin(page, gitlabUrl) {
    await page.goto(gitlabUrl, { waitUntil: "domcontentloaded" });
    await new Promise(r => setTimeout(r, 3000));
    const url = page.url();
    const loginKeywords = ["login", "signin", "sign_in", "users/sign_in"];
    const isLoginPage = loginKeywords.some(k => url.toLowerCase().includes(k));
    if (isLoginPage) {
        console.error("\n❌ 检测到未登录状态\n");
        console.error("当前URL:", url);
        console.error("请先在浏览器登录 GitLab，然后重新运行程序\n");
        throw new Error("LOGIN_REQUIRED");
    }
}
export async function fetchGroupPushEvents(page, config, targetDate) {
    const { gitlabUrl, groupId } = config;
    const allEvents = [];
    const limit = 20;
    let offset = 0;
    let hasMore = true;
    console.log(`拉取 ${targetDate} 的 push events，分页拉取中...`);
    const activityPageUrl = `${gitlabUrl}/groups/${groupId}/-/activity`;
    await page.goto(activityPageUrl, { waitUntil: "domcontentloaded" });
    await new Promise(r => setTimeout(r, 2000));
    const currentUrl = page.url();
    const loginKeywords = ["login", "signin", "sign_in", "users/sign_in"];
    if (loginKeywords.some(k => currentUrl.toLowerCase().includes(k))) {
        throw new Error("LOGIN_REQUIRED");
    }
    while (hasMore) {
        const apiUrl = `${activityPageUrl}?limit=${limit}&offset=${offset}`;
        const result = await page.evaluate(async (url) => {
            const res = await fetch(url, {
                credentials: "include",
                headers: { "X-Requested-With": "XMLHttpRequest", "Accept": "application/json" },
            });
            if (!res.ok)
                throw new Error(`HTTP ${res.status}`);
            const contentType = res.headers.get("content-type") ?? "";
            if (!contentType.includes("application/json")) {
                throw new Error(`非 JSON 响应: ${contentType}`);
            }
            return res.json();
        }, apiUrl);
        if (!result.html || result.count === 0)
            break;
        const events = parseActivityHtml(result.html);
        console.log(`  offset=${offset} 解析到 ${events.length} 条 push 事件`);
        let hasTargetDate = false;
        let hasOlderDate = false;
        for (const event of events) {
            const eventDate = event.pushedAt.split("T")[0];
            if (eventDate === targetDate) {
                hasTargetDate = true;
                allEvents.push({
                    author: event.author,
                    authorUsername: event.authorUsername,
                    projectName: event.projectName,
                    projectPath: event.projectPath,
                    commitCount: 1,
                    commits: event.commitId
                        ? [{ id: event.commitId, message: event.commitMessage, timestamp: event.pushedAt }]
                        : [],
                    pushedAt: event.pushedAt,
                });
            }
            else if (eventDate < targetDate) {
                hasOlderDate = true;
            }
        }
        if (hasOlderDate && !hasTargetDate) {
            console.log("  已超出目标日期范围，停止翻页");
            break;
        }
        if (hasOlderDate) {
            console.log("  已到达目标日期边界，停止翻页");
            break;
        }
        if (result.count < limit) {
            break;
        }
        offset += limit;
    }
    return allEvents;
}
//# sourceMappingURL=gitlab-api.js.map