import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe";

function runChromeScreenshot(htmlContent, outPngPath, width, height) {
	const tmpHtml = path.resolve("assets", `_tmp_${Date.now()}_${Math.random().toString(36).slice(2)}.html`);
	fs.writeFileSync(tmpHtml, htmlContent, "utf8");
	const args = [
		"--headless",
		"--disable-gpu",
		"--no-sandbox",
		`--window-size=${width},${height}`,
		"--hide-scrollbars",
		`--screenshot=${path.resolve(outPngPath)}`,
		`file:///${tmpHtml.replace(/\\/g, "/")}`,
	];
	const res = spawnSync(CHROME_PATH, args, { encoding: "utf8" });
	if (fs.existsSync(tmpHtml)) {
		fs.unlinkSync(tmpHtml);
	}
	if (res.error) throw res.error;
	console.log(`Saved screenshot: ${outPngPath}`);
}

function renderCard(innerHtml, outPngPath, width = 520, minHeight = 100) {
	const fullHtml = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 16px;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    display: inline-block;
    width: 480px;
  }
</style>
</head>
<body>
  ${innerHtml}
</body>
</html>`;
	runChromeScreenshot(fullHtml, outPngPath, width, minHeight);
}

async function main() {
	const bodyHtmlPath = "y:/06_services/mpress/work/editorial/body.html";
	const compDir = path.resolve("assets/components");
	if (!fs.existsSync(compDir)) fs.mkdirSync(compDir, { recursive: true });

	if (fs.existsSync(bodyHtmlPath)) {
		const body = fs.readFileSync(bodyHtmlPath, "utf8");

		// 1. 全长图
		const containerHtml = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {
    margin: 0;
    padding: 32px 20px;
    background: #eef2f3;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    display: flex;
    justify-content: center;
  }
  .phone-frame {
    width: 440px;
    background: #ffffff;
    box-shadow: 0 12px 36px rgba(0,0,0,0.1);
    border-radius: 14px;
    padding: 24px 18px;
    box-sizing: border-box;
    overflow: hidden;
  }
</style>
</head>
<body>
  <div class="phone-frame">${body}</div>
</body>
</html>`;
		runChromeScreenshot(containerHtml, "assets/preview-components.png", 500, 3200);

		// 2. 独立组件切片图
		const kickerLead = body.match(/<section class="wx-kicker"[\s\S]*?<\/section>\s*<section class="wx-lead"[\s\S]*?<\/section>/);
		if (kickerLead) renderCard(kickerLead[0], "assets/components/01-kicker-lead.png", 520, 260);

		const callouts = body.match(/<section class="wx-box wx-box-tip"[\s\S]*?<section class="wx-box wx-box-important"[\s\S]*?<\/section>/);
		if (callouts) renderCard(callouts[0], "assets/components/00-callouts.png", 520, 480);

		const metrics = body.match(/<section class="wx-metrics"[\s\S]*?<\/section>/);
		if (metrics) renderCard(metrics[0], "assets/components/02-metrics.png", 520, 300);

		const versus = body.match(/<section class="wx-versus"[\s\S]*?<\/section>/);
		if (versus) renderCard(versus[0], "assets/components/03-versus.png", 520, 480);

		const steps = body.match(/<section class="wx-steps"[\s\S]*?<\/section>/);
		if (steps) renderCard(steps[0], "assets/components/04-steps.png", 520, 480);

		const dossier = body.match(/<section class="wx-dossier"[\s\S]*?<\/section>/);
		if (dossier) renderCard(dossier[0], "assets/components/05-dossier.png", 520, 400);

		const verdict = body.match(/<section class="wx-verdict"[\s\S]*?<\/section>/);
		if (verdict) renderCard(verdict[0], "assets/components/06-verdict.png", 520, 220);

		const qa = body.match(/<section class="wx-qa"[\s\S]*?<\/section>/);
		if (qa) renderCard(qa[0], "assets/components/07-qa.png", 520, 420);

		const details = body.match(/<section class="custom-details-preview-box"[\s\S]*?<\/section>/);
		if (details) renderCard(details[0], "assets/components/08-details-fold.png", 520, 300);

		const checklist = body.match(/<section class="wx-checklist"[\s\S]*?<\/section>/);
		if (checklist) renderCard(checklist[0], "assets/components/09-checklist.png", 520, 380);

		const github = body.match(/<section class="wx-github-card"[\s\S]*?<\/section>\s*<section class="custom-details-preview-box"[\s\S]*?<\/section>/);
		if (github) renderCard(github[0], "assets/components/10-github-card.png", 520, 360);

		const follow = body.match(/<section class="wx-follow"[\s\S]*?<\/section>/);
		if (follow) renderCard(follow[0], "assets/components/11-follow.png", 520, 240);
	}

	// 3. 生成头图模板 Template-D 示例
	const tplD = fs.readFileSync("templates/template-d.html", "utf8");
	const coverDHtml = tplD
		.replaceAll("{{TITLE}}", "AI 时代的个人知识库发布规范与微信全流程实践")
		.replaceAll("{{EYEBROW}}", "SHXUK.CN · 个人博客与数字花园")
		.replaceAll("{{COVER_SUBTITLE}}", "从纯文本 Markdown 到全端兼容的杂志风公众号排版方案")
		.replaceAll("{{BRAND}}", "SHXUK.CN")
		.replaceAll("{{TAG}}", "开源工具")
		.replaceAll("{{ISSUE_NO}}", "PRO · 2026")
		.replaceAll("{{COVER_STAT_TAG}}", "DESIGN SYSTEM")
		.replaceAll("{{ISSUE_DATE}}", "2026.11")
		.replaceAll("{{COVER_STAT_NUM}}", "2.0")
		.replaceAll("{{COVER_STAT_CAPTION}}", "EDITORIAL MAGAZINE PRO")
		.replaceAll("{{AUTHOR}}", "shxuk")
		.replaceAll("{{STATUS_LABEL}}", "VERIFIED")
		.replaceAll("{{FOOTER_SLOGAN}}", "构建可持续的数字写作与多端发布工作流")
		.replaceAll("{{WORD_COUNT_LABEL}}", "全组件实测")
		.replaceAll("{{SITE_DOMAIN}}", "shxuk.cn");
	runChromeScreenshot(coverDHtml, "assets/preview-cover-d.png", 1800, 766);

	// 4. 生成头图模板 Template-E 示例
	const tplE = fs.readFileSync("templates/template-e.html", "utf8");
	const coverEHtml = tplE
		.replaceAll("{{TITLE}}", "给决策者的 GEO 与 AI 搜索排版指南")
		.replaceAll("{{TITLE_SHORT}}", "GEO 与 AI 搜索排版指南")
		.replaceAll("{{BOOK_OR_TAG}}", "观点长文 · AI-SEO")
		.replaceAll("{{BOOK_TITLE}}", "GEO 决策实录")
		.replaceAll("{{BOOK_TAG}}", "CH. 1/7")
		.replaceAll("{{BOOK_PALETTE}}", "墨青")
		.replaceAll("{{COVER_MODE}}", "book")
		.replaceAll("{{TAG}}", "AI 时代运营")
		.replaceAll("{{ISSUE}}", "CH. 1/7")
		.replaceAll("{{ISSUE_DATE}}", "2026.11")
		.replaceAll("{{ISSUE_SHORT}}", "CH. 1")
		.replaceAll("{{YEAR}}", "2026")
		.replaceAll("{{BRAND}}", "SHXUK.CN")
		.replaceAll("{{BRAND_UPPER}}", "SHXUK.CN")
		.replaceAll("{{AUTHOR}}", "shxuk")
		.replaceAll("{{SITE_DOMAIN}}", "shxuk.cn")
		.replaceAll("{{SPINE_TEXT}}", "SHXUK.CN · 深度专题")
		.replaceAll("{{EYEBROW}}", "SHXUK.CN 思考实录")
		.replaceAll("{{ISSUE_NO}}", "CH. 1")
		.replaceAll("{{FOOTER_SLOGAN}}", "AI 搜索我的博客：shxuk.cn 让 AI 帮你总结全文")
		.replaceAll("{{WORD_COUNT_LABEL}}", "共 7 章连载");
	runChromeScreenshot(coverEHtml, "assets/preview-cover-e.png", 1800, 766);
}

main().catch(console.error);
