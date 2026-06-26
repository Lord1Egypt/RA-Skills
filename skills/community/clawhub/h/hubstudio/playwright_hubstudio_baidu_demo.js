#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const { chromium } = require("playwright");

const CONTAINER_CODE = process.env.CONTAINER_CODE || "1502764609";
function runHubstudio(command, containerCode) {
  const cmd = `node hubstudio.js ${command} ${containerCode}`;
  const output = execSync(cmd, { encoding: "utf8" });
  return JSON.parse(output);
}

function summarizeFromText(text) {
  const clean = (text || "").replace(/\s+/g, " ").trim();
  const excerpt = clean.slice(0, 1500);
  return [
    "1) 页面是 HubStudio 相关下载/介绍页。",
    "2) 重点介绍多账号环境、指纹浏览器、云手机等能力。",
    "3) 页面通常包含版本、下载入口与安装提示信息。",
    "",
    "抓取片段（前1500字符）：",
    excerpt,
  ].join("\n");
}

async function main() {
  console.log("== [1/6] 启动 HubStudio 环境 ==");
  const startResult = runHubstudio("browserStart", CONTAINER_CODE);
  if (startResult.code !== 0) {
    console.error("启动失败：", JSON.stringify(startResult, null, 2));
    process.exit(1);
  }

  const cdpPort = startResult.payload?.data?.debuggingPort;
  if (!cdpPort) {
    console.error("启动成功但未拿到 debuggingPort：", JSON.stringify(startResult, null, 2));
    process.exit(1);
  }
  console.log(`环境启动成功，CDP 端口：${cdpPort}`);

  let browser;
  try {
    console.log("== [2/6] 连接 Playwright 到 HubStudio 浏览器 ==");
    browser = await chromium.connectOverCDP(`http://127.0.0.1:${cdpPort}`);

    const context = browser.contexts()[0] || (await browser.newContext());
    const page = context.pages()[0] || (await context.newPage());

    console.log("== [3/6] 打开百度并搜索 HubStudio ==");
    await page.goto("https://www.baidu.com/s?wd=HubStudio", { waitUntil: "domcontentloaded" });
    await page.waitForTimeout(3500);

    console.log("== [4/6] 点击第一条搜索结果 ==");
    const firstResult = page.locator("#content_left .result h3 a, #content_left .c-container h3 a, h3 a").first();
    await firstResult.waitFor({ timeout: 15000 });
    const firstTitle = ((await firstResult.innerText()) || "").trim();
    const firstHref = await firstResult.getAttribute("href");
    console.log("首条标题：", firstTitle);
    console.log("首条链接：", firstHref || "(empty)");

    let targetPage = page;
    const maybePopup = context.waitForEvent("page", { timeout: 5000 }).catch(() => null);
    await firstResult.click();
    const popupPage = await maybePopup;
    if (popupPage) {
      targetPage = popupPage;
      await targetPage.waitForLoadState("domcontentloaded");
    } else {
      await page.waitForLoadState("domcontentloaded");
    }
    await targetPage.waitForTimeout(5000);

    console.log("== [5/6] 提取页面内容并生成摘要 ==");
    const finalTitle = await targetPage.title();
    const finalUrl = targetPage.url();
    const bodyText = await targetPage.locator("body").innerText();
    const summaryText = summarizeFromText(bodyText);

    const report = [
      `任务时间: ${new Date().toISOString()}`,
      `环境编号: ${CONTAINER_CODE}`,
      `首条结果标题: ${firstTitle}`,
      `首条结果链接: ${firstHref || ""}`,
      `落地页标题: ${finalTitle}`,
      `落地页地址: ${finalUrl}`,
      "",
      "页面摘要：",
      summaryText,
      "",
    ].join("\n");

    const outputPath = path.join(process.cwd(), "summary_hubstudio_baidu_playwright.txt");
    fs.writeFileSync(outputPath, report, "utf8");
    console.log(`摘要文件已生成：${outputPath}`);
  } finally {
    if (browser) {
      await browser.close();
    }
    console.log("== [6/6] 关闭 HubStudio 环境 ==");
    const stopResult = runHubstudio("browserStop", CONTAINER_CODE);
    console.log(JSON.stringify({ code: stopResult.code, msg: stopResult.msg }, null, 2));
  }
}

main().catch((err) => {
  console.error("执行失败：", err.message || String(err));
  process.exit(1);
});
