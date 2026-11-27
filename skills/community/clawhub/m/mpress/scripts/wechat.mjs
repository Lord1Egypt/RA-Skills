#!/usr/bin/env node
/**
 * mpress 的唯一入口（旧名 wechat-publisher），两个动作：
 *
 *   node scripts/wechat.mjs gen  <任意.md> [--source-url URL]   固定模板渲染 + 内联 HTML + layout.json
 *   node scripts/wechat.mjs push <任意.md> [--source-url URL]   渲染 + 换图片地址 + 合成头图 + 新建/更新草稿
 */
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";
import MarkdownIt from "markdown-it";
import juice from "juice";

import {
	BOX_KINDS,
	blockHtml,
	boxHtml,
	chapterHtml,
	checklistHtml,
	cjkStrong,
	codeHtml,
	compText,
	dossierHtml,
	figureHtml,
	followHtml,
	githubCardHtml,
	kickerHtml,
	leadHtml,
	metricsHtml,
	qaHtml,
	quoteHtml,
	stepsHtml,
	verdictHtml,
	versusHtml,
} from "../components/cards.mjs";
import { renderSvgFold } from "../components/svg-fold.mjs";

const md = new MarkdownIt({
	html: true,
	breaks: true,
	linkify: false,
});

const SKILL_DIR = path.resolve(import.meta.dirname, "..");
const CWD = process.cwd();

// 自动加载 .env 配置文件
const envFile = path.join(SKILL_DIR, ".env");
if (fs.existsSync(envFile)) {
	try {
		if (typeof process.loadEnvFile === "function") {
			process.loadEnvFile(envFile);
		} else {
			for (const line of fs.readFileSync(envFile, "utf8").split(/\r?\n/)) {
				const m = line.match(/^\s*(?:export\s+)?([A-Za-z_]\w*)\s*=\s*(.*?)\s*$/);
				if (m && !process.env[m[1]]) {
					process.env[m[1]] = m[2].replace(/^(['"])(.*)\1$/, "$2");
				}
			}
		}
	} catch {}
}

// 产物和草稿状态留在仓库外，源码目录保持只读
const WORK = process.env.WECHAT_WORK_DIR || path.join(os.homedir(), ".wechat-article", "work");
const STATE_DIR = path.join(WORK, "state");
const THEME = path.join(SKILL_DIR, "assets", "theme.css");
const DEFAULT_COVER = path.join(SKILL_DIR, "assets", "default-cover.png");
const HEAD_BASE = path.join(SKILL_DIR, "assets", "head-base.jpg");
const DRAFTS = path.join(STATE_DIR, "drafts.json");
const UPLOADS = path.join(STATE_DIR, "uploads.json");
const AUTHOR = process.env.WECHAT_AUTHOR || "";
const API = "https://api.weixin.qq.com/cgi-bin";

/** 只有显式给了 BLOG_ROOT 才做站内链接补全和 /public 图片解析；独立使用时不依赖博客仓库 */
const BLOG_ROOT = (() => {
	if (process.env.BLOG_ROOT && fs.existsSync(process.env.BLOG_ROOT)) return process.env.BLOG_ROOT;
	if (fs.existsSync(path.join(process.cwd(), "astro.config.mjs"))) return process.cwd();
	return "";
})();

const EXIT_CODES = { 凭证: 2, 白名单: 3, 图片: 4, 结构: 5, 网络: 6 };

// ---------- 计时 ----------

const TIMING = process.env.WECHAT_TIMING === "1" || process.argv.includes("--timing");
const timingStart = performance.now();
let timingLast = timingStart;
const timingRows = [];

function mark(name) {
	if (!TIMING) return;
	const now = performance.now();
	timingRows.push([name, now - timingLast]);
	timingLast = now;
}

function printTiming(label) {
	if (!TIMING) return;
	console.error(
		`\n耗时（${label}）：进程内 ${(performance.now() - timingStart).toFixed(0)} ms · 含 Node 启动 ${(process.uptime() * 1000).toFixed(0)} ms`,
	);
	for (const [name, ms] of timingRows) console.error(`  ${name} ${ms.toFixed(0)} ms`);
}

class PublishError extends Error {
	constructor(kind, message, hint) {
		super(message);
		this.kind = kind;
		this.hint = hint;
	}
}

function fail(kind, message, hint) {
	throw new PublishError(kind, message, hint);
}

const readJson = (file, fallback) => {
	try {
		return JSON.parse(fs.readFileSync(file, "utf8"));
	} catch {
		return fallback;
	}
};

const writeJson = (file, value) => {
	fs.mkdirSync(path.dirname(file), { recursive: true });
	fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`, "utf8");
};

// ---------- 站点统计（供封面模板使用） ----------

function getSiteStats(blogRoot) {
	let totalChars = 0;
	let runningDays = 12;

	try {
		const contentDir = blogRoot ? path.join(blogRoot, "content") : "";
		if (contentDir && fs.existsSync(contentDir)) {
			function scan(dir) {
				for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
					const full = path.join(dir, ent.name);
					if (ent.isDirectory()) {
						if (!ent.name.includes("backup") && !ent.name.startsWith(".")) scan(full);
					} else if (/\.(md|mdx)$/i.test(ent.name)) {
						const raw = fs.readFileSync(full, "utf8");
						const text = raw.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, "");
						const cjk = (text.match(/[\u4e00-\u9fff]/g) || []).length;
						totalChars += cjk;
					}
				}
			}
			scan(contentDir);
		}
	} catch (e) {
		console.error("统计字数失败:", e);
	}

	let brand = "";
	try {
		const cfgPath = blogRoot ? path.join(blogRoot, "src", "config", "siteConfig.ts") : "";
		if (cfgPath && fs.existsSync(cfgPath)) {
			const text = fs.readFileSync(cfgPath, "utf8");
			const m = text.match(/siteStartDate:\s*["'](\d{4}-\d{2}-\d{2})["']/);
			if (m) {
				const start = new Date(m[1]).getTime();
				runningDays = Math.ceil(Math.abs(Date.now() - start) / 86400000);
			}
			const t = text.match(/^\s*title:\s*["']([^"']+)["']/m);
			if (t) brand = t[1].trim();
		}
	} catch (e) {
		console.error("统计天数失败:", e);
	}

	const wordCountLabel = totalChars > 0 ? `${totalChars.toLocaleString()} 字总结` : "151,710 字总结";
	const statusLabel = `DAY ${runningDays} · 推进中`;
	return { totalChars, wordCountLabel, runningDays, statusLabel, brand };
}

// ---------- Markdown 固定映射（唯一模板规则） ----------

function expandComponents(body) {
	const lines = body.split(/\r?\n/);
	const out = [];
	const mappings = [];
	let h2Counter = 1;
	let seenChapter = false;
	const mapped = (rule, line) => mappings.push({ line: line + 1, rule });

	const gap = () => {
		if (out.length && out[out.length - 1] !== "") out.push("");
	};

	for (let i = 0; i < lines.length; ) {
		let line = lines[i];

		// 链接包图片 [![alt](src)](href)：微信会剥掉 <a>，只保留图片，否则渲染出乱码
		const withoutLink = line.replace(/\[(!\[[^\]]*\]\([^)\s]+\))\]\([^)\s]+\)/g, "$1");
		if (withoutLink !== line) {
			mapped("image:linked-stripped", i);
			line = withoutLink;
		}

		// 容器：::: githubcard / ::: details / ::: tip|note|warning|important|caution
		const container = line.match(/^:::\s*([A-Za-z][A-Za-z0-9_-]*)(?:\[(.*?)\])?(?:\s+(.*?))?\s*$/);
		if (container) {
			const kind = container[1].toLowerCase();
			const bracketArg = (container[2] || "").trim();
			const restArg = (container[3] || "").trim();
			const hasTrailingColons = /\s*:::$/.test(restArg) || restArg === ":::";
			const cleanRest = restArg.replace(/\s*:::$/, "").trim();
			const argText = bracketArg || cleanRest;
			const openLine = i;

			if (kind === "kicker" && hasTrailingColons) {
				mapped("container:kicker", openLine);
				i++;
				gap();
				out.push(kickerHtml([], argText));
				out.push("");
				continue;
			}

			if (kind === "githubcard" && hasTrailingColons) {
				mapped("container:githubcard", openLine);
				i++;
				gap();
				out.push(githubCardHtml(argText));
				out.push("");
				continue;
			}

			const buf = [];
			let j = i + 1;
			while (j < lines.length && lines[j].trim() !== ":::") {
				buf.push(lines[j]);
				j++;
			}
			if (j >= lines.length) fail("结构", "::: 容器没有闭合", "补一行单独的 :::");
			i = j + 1;

			if (kind === "kicker") {
				mapped("container:kicker", openLine);
				gap();
				out.push(kickerHtml(buf, argText));
				out.push("");
				continue;
			}

			if (kind === "follow") {
				mapped("container:follow", openLine);
				gap();
				out.push(followHtml(buf, argText));
				out.push("");
				continue;
			}

			if (kind === "lead") {
				mapped("container:lead", openLine);
				gap();
				out.push(leadHtml(buf, argText));
				out.push("");
				continue;
			}

			if (kind === "metrics") {
				mapped("container:metrics", openLine);
				gap();
				out.push(metricsHtml(buf, argText));
				out.push("");
				continue;
			}

			if (kind === "dossier") {
				mapped("container:dossier", openLine);
				gap();
				out.push(dossierHtml(buf, argText));
				out.push("");
				continue;
			}

			if (kind === "versus") {
				mapped("container:versus", openLine);
				gap();
				out.push(versusHtml(buf, argText));
				out.push("");
				continue;
			}

			if (kind === "checklist") {
				mapped("container:checklist", openLine);
				gap();
				out.push(checklistHtml(buf, argText));
				out.push("");
				continue;
			}

			if (kind === "steps") {
				mapped("container:steps", openLine);
				gap();
				out.push(stepsHtml(buf, argText));
				out.push("");
				continue;
			}

			if (kind === "verdict") {
				mapped("container:verdict", openLine);
				gap();
				out.push(verdictHtml(buf, argText));
				out.push("");
				continue;
			}

			if (kind === "qa") {
				mapped("container:qa", openLine);
				gap();
				out.push(qaHtml(buf, argText));
				out.push("");
				continue;
			}

			if (kind === "githubcard") {
				mapped("container:githubcard", openLine);
				gap();
				out.push(githubCardHtml(argText || buf.join(" ").trim()));
				out.push("");
				continue;
			}

			if (["githubreadme", "githubreadme-preview", "githubreadmepreview", "githubreadme:preview"].includes(kind)) {
				mapped("container:githubreadme", openLine);
				gap();
				const cleanRepo = argText.replace(/--preview|preview/gi, "").trim();
				out.push(renderSvgFold(buf.join("\n"), fail, cleanRepo ? `README · ${cleanRepo}` : "README"));
				out.push("");
				continue;
			}

			if (["details", "details-preview", "detailspreview", "details:preview"].includes(kind)) {
				mapped("container:details", openLine);
				gap();
				out.push(renderSvgFold(buf.join("\n"), fail, argText));
				out.push("");
				continue;
			}

			const ADMONITION_ALIAS = {
				caution: "warning",
				danger: "warning",
				failure: "warning",
				missing: "warning",
				fail: "warning",
				error: "warning",
				bug: "warning",
				attention: "warning",
				info: "note",
				abstract: "note",
				summary: "note",
				tldr: "note",
				example: "note",
				question: "tip",
				help: "tip",
				faq: "tip",
				success: "tip",
				check: "tip",
				done: "tip",
				todo: "important",
			};
			if (ADMONITION_ALIAS[kind] || BOX_KINDS[kind.toUpperCase()]) {
				const boxKind = ADMONITION_ALIAS[kind] || BOX_KINDS[kind.toUpperCase()];
				mapped(`container:${kind}`, openLine);
				gap();
				out.push(boxHtml(boxKind, buf, argText));
				out.push("");
				continue;
			}

			out.push(line);
			out.push(...buf);
			out.push(":::");
			continue;
		}

		// 围栏：end / sign / mermaid / 普通代码
		const fence = line.match(/^```([A-Za-z0-9_-]+)?(?:\s+(.*))?$/);
		if (fence) {
			const lang = (fence[1] || "").toLowerCase();
			const buf = [];
			let j = i + 1;
			while (j < lines.length && !/^```\s*$/.test(lines[j])) {
				buf.push(lines[j]);
				j++;
			}
			if (j >= lines.length) fail("结构", "代码块没有闭合", "补一行 ```");
			mapped(`fence:${lang || "code"}`, i);
			i = j + 1;
			gap();
			if (lang === "end") {
				out.push(blockHtml("wx-end", "wx-end-text", buf));
			} else if (lang === "sign") {
				out.push(blockHtml("wx-sign", "", buf));
			} else if (lang === "mermaid") {
				out.push("```mermaid", ...buf, "```");
			} else {
				out.push(codeHtml(lang, buf));
			}
			out.push("");
			continue;
		}

		// 引用块：提示块 / 长引（出处以 —— 开头）/ 普通引用
		if (/^>/.test(line)) {
			const buf = [];
			let j = i;
			while (j < lines.length && /^>/.test(lines[j])) {
				buf.push(lines[j].replace(/^>\s?/, ""));
				j++;
			}
			const first = (buf[0] || "").trim();
			const boxToken = first.split(/\s+/, 1)[0];
			const boxKind = BOX_KINDS[boxToken];
			const boxTitle = boxKind ? first.slice(boxToken.length).trim() : "";
			const isLongQuote = /^——/.test((buf[buf.length - 1] || "").trim());
			mapped(boxKind ? `box:${boxToken.toLowerCase()}` : isLongQuote ? "quote:source" : "quote", i);
			i = j;
			gap();
			if (boxKind) {
				out.push(boxHtml(boxKind, buf.slice(1), boxTitle));
			} else if (isLongQuote) {
				out.push(quoteHtml(buf.slice(0, -1), buf[buf.length - 1].trim()));
			} else {
				const paragraphs = buf
					.join("\n")
					.split(/\n{2,}/)
					.map((p) => p.replace(/\s*\n\s*/g, "").trim())
					.filter(Boolean);
				out.push(...paragraphs.map((p) => `<p>${compText(p)}</p>`));
			}
			out.push("");
			continue;
		}

		// 一级标题：首个 H1 在公众号正文剥除，后续 H1 为篇章标题
		const h1 = line.match(/^#\s+(.+)$/);
		if (h1) {
			if (!seenChapter) {
				mapped("chapter:stripped-for-wechat", i);
				seenChapter = true;
				i++;
				continue;
			}
			mapped("chapter", i);
			gap();
			out.push(`<h1 class="wx-chapter">${compText(h1[1].trim())}</h1>`);
			out.push("");
			i++;
			continue;
		}

		// 二级标题（唯一样式）：全部输出墨青色正方形数字页签（01、02...），并自动剥离冗余的中文/阿拉伯序号（如「一、」「1.」）
		const h2Match = line.match(/^##\s+(?:(\d{1,2})\s+)?(\S.*)$/);
		if (h2Match) {
			mapped("chapter-tab", i);
			gap();
			let no = h2Match[1];
			let titleText = h2Match[2].trim();
			// 若未显式写阿拉伯编号，剥除前导「一、」「二、」「1.」「01、」防止与墨青方块页签重复
			titleText = titleText.replace(/^(?:[一二三四五六七八九十百]+[、.．]\s*|\d{1,2}[、.．]\s*)/, "").trim();
			if (no) {
				no = String(parseInt(no, 10)).padStart(2, "0");
				h2Counter = parseInt(no, 10) + 1;
			} else {
				no = String(h2Counter++).padStart(2, "0");
			}
			const isFirst = out.length === 0 || (out.length === 1 && out[0] === "");
			out.push(chapterHtml(no, titleText, isFirst));
			out.push("");
			i++;
			continue;
		}

		// 三级标题：3px 墨色左竖线小节标题
		const h3 = line.match(/^###\s+(.+)$/);
		if (h3) {
			mapped("heading-3", i);
			gap();
			out.push(`<h3 class="wx-h3">${compText(h3[1].trim())}</h3>`);
			out.push("");
			i++;
			continue;
		}

		// 图片 + 下一行斜体图注
		const img = line.match(/^!\[(.*?)\]\((.+?)\)\s*$/);
		if (img) {
			let k = i + 1;
			while (k < lines.length && !lines[k].trim()) k++;
			const cap = k < lines.length ? lines[k].trim().match(/^\*([^*].*)\*$/) : null;
			mapped(cap ? "figure:caption" : "figure", i);
			gap();
			out.push(figureHtml(img[1], img[2], cap ? cap[1].trim() : ""));
			i = cap ? k + 1 : i + 1;
			out.push("");
			continue;
		}

		if (line.trim()) mapped("native", i);
		out.push(cjkStrong(line));
		i++;
	}

	return { body: out.join("\n"), mappings };
}

// ---------- 源稿解析与产物构建 ----------

function parseFrontmatter(text) {
	const data = {};
	const unquote = (value) =>
		(value.startsWith('"') && value.endsWith('"')) ||
		(value.startsWith("'") && value.endsWith("'"))
			? value.slice(1, -1)
			: value;
	const parseInlineList = (raw) =>
		raw
			.slice(1, -1)
			.split(",")
			.map((item) => unquote(item.trim()))
			.filter(Boolean);
	const lines = text.split(/\r?\n/);
	for (let i = 0; i < lines.length; i++) {
		const kv = lines[i].match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
		if (!kv) continue;
		const val = kv[2].trim();
		if (val) {
			data[kv[1]] = /^\[.*\]$/.test(val) ? parseInlineList(val) : unquote(val);
			continue;
		}
		const nested = {};
		const list = [];
		while (i + 1 < lines.length) {
			const item = lines[i + 1].match(/^\s*-\s+(.*)$/);
			if (item) {
				i++;
				if (item[1].trim()) list.push(unquote(item[1].trim()));
				continue;
			}
			const child = lines[i + 1].match(/^\s{1,}([A-Za-z_][\w-]*):\s*(.*)$/);
			if (!child) break;
			i++;
			if (child[2].trim()) nested[child[1]] = unquote(child[2].trim());
		}
		if (list.length) data[kv[1]] = list;
		else if (Object.keys(nested).length) data[kv[1]] = nested;
	}
	return data;
}

function resolveAsset(src, sourcePath) {
	if (!src || /^(https?:|data:)/i.test(src)) return src;
	if (src.startsWith("/") && !BLOG_ROOT) {
		fail(
			"图片",
			`站内图片需要站点根目录：${src}`,
			"设 BLOG_ROOT 指向仓库根，或把图片改成相对源稿的路径",
		);
	}
	const local = src.startsWith("/")
		? path.join(BLOG_ROOT, "public", src)
		: path.resolve(path.dirname(sourcePath), decodeURIComponent(src));
	if (!fs.existsSync(local)) {
		fail("图片", `找不到图片：${src}`, `期望路径 ${local}`);
	}
	return local;
}

function assertWritable(target) {
	const workRel = path.relative(WORK, target);
	if (!workRel || workRel.startsWith("..") || path.isAbsolute(workRel)) {
		fail("结构", `产物目录越界：${target}`, "slug 不能指向上级目录");
	}
}

function bookTitleOf(abs) {
	if (!BLOG_ROOT) return "";
	const rel = path.relative(path.join(BLOG_ROOT, "content", "books"), abs);
	if (rel.startsWith("..") || path.isAbsolute(rel)) return "";
	const name = rel.split(path.sep)[0];
	const index = path.join(BLOG_ROOT, "content", "books", `${name}.md`);
	if (!fs.existsSync(index)) return "";
	const fm = fs.readFileSync(index, "utf8").match(/^---\r?\n([\s\S]*?)\r?\n---/);
	return fm ? (parseFrontmatter(fm[1]).title || "").trim() : "";
}

function buildArticle(source, sourceUrl) {
	if (/\.mdx$/i.test(source)) {
		fail("结构", "MDX 不支持：公众号没有 Astro 运行时", "改用纯 .md");
	}
	const abs = path.resolve(CWD, source);
	if (path.extname(abs).toLowerCase() !== ".md") {
		fail("结构", "源文件必须是纯 .md", "不要传 .mdx、Astro 组件或派生稿");
	}
	if (!fs.existsSync(abs)) {
		fail("结构", `源文件不存在：${abs}`, "路径按当前目录解析，例如 ./文章.md");
	}

	const contentRoot = BLOG_ROOT ? path.join(BLOG_ROOT, "content") : "";
	if (!sourceUrl && contentRoot) {
		const rel = path.relative(contentRoot, abs).replace(/\\/g, "/");
		const site = siteUrl();
		if (site && !rel.startsWith("..") && !path.isAbsolute(rel)) {
			if (rel.startsWith("essay/")) {
				sourceUrl = `${site}/essay/${rel.replace(/^essay\//, "").replace(/\.md$/i, "")}/`;
			} else if (rel.startsWith("books/")) {
				sourceUrl = `${site}/case/${rel.replace(/^books\//, "").replace(/\.md$/i, "")}/`;
			}
		}
	}

	let sourceRel = path.basename(abs);
	let slug = path.basename(abs, path.extname(abs));
	if (contentRoot) {
		const contentRel = path.relative(contentRoot, abs);
		if (!contentRel.startsWith("..") && !path.isAbsolute(contentRel)) {
			sourceRel = contentRel;
			slug = contentRel.replace(/\.md$/i, "").split(path.sep).join("-");
		}
	}
	if (path.basename(path.dirname(abs)) === "样例") slug = `sample-${slug}`;

	const raw = fs.readFileSync(abs, "utf8");
	const fm = raw.match(/^---\r?\n([\s\S]*?)\r?\n---[ \t]*\r?\n?/);
	const data = parseFrontmatter(fm?.[1] || "");
	let body = fm ? raw.slice(fm[0].length) : raw;

	let title = (data.title || "").trim();
	if (!title) {
		const h1 = body.match(/^#\s+(.+)$/m);
		if (h1) title = h1[1].trim();
	}

	const expanded = expandComponents(body);
	body = expanded.body;

	body = body.replace(
		/(!\[[^\]]*\]\()([^)\s]+)(\))/g,
		(_, head, src, tail) => head + resolveAsset(src, abs) + tail,
	);
	body = body.replace(
		/(<img\b[^>]*?\bsrc=["'])([^"']+)(["'])/gi,
		(_, head, src, tail) => head + resolveAsset(src, abs) + tail,
	);

	if (!title) title = path.basename(abs, path.extname(abs));

	let cover = resolveAsset((data.image || data.banner?.image || "").trim(), abs);
	if (!cover) {
		const first = body.match(/!\[[^\]]*\]\(([^)\s]+)\)/) || body.match(/<img\b[^>]*?\bsrc=["']([^"']+)["']/i);
		if (first && !/^https?:/i.test(first[1])) cover = first[1];
	}
	if (!cover && fs.existsSync(DEFAULT_COVER)) cover = DEFAULT_COVER;
	if (!cover) fail("图片", "没有封面，正文里也没有本地图片", "在 assets/default-cover.png 放一张默认封面");

	const summary = (data.description || data.summary || data.digest || "").trim();
	const book = (data.banner?.book || data.book || bookTitleOf(abs) || "").trim();
	const chapterTitle = title;
	// 书稿文章在公众号标题自动带上书名：「书名 ：章标题」
	if (book && !title.includes(book)) {
		title = `${book} ：${title}`;
	}
	const tags = Array.isArray(data.tags) ? data.tags : data.tags ? [String(data.tags)] : [];
	const category = (data.category || "").trim();
	const seriesOrder = (data.seriesOrder || "").trim();
	const seriesTotal = (data.seriesTotal || "").trim();
	const coverTemplate = (data.coverTemplate || data.cover_template || "").trim().toLowerCase();
	const coverSubtitle = (data.coverSubtitle || data.cover_subtitle || "").trim();
	const coverStatNum = (data.coverStatNum || data.cover_stat_num || "").trim();
	const coverStatCaption = (data.coverStatCaption || data.cover_stat_caption || "").trim();
	const coverStatTag = (data.coverStatTag || data.cover_stat_tag || "").trim();
	const headBase = process.env.WECHAT_HEAD_BASE
		? path.resolve(CWD, process.env.WECHAT_HEAD_BASE)
		: resolveAsset((data.banner?.image || "").trim(), abs) ||
			(fs.existsSync(HEAD_BASE) ? HEAD_BASE : cover);

	const images =
		(body.match(/!\[[^\]]*\]\([^)]+\)/g) || []).length + (body.match(/<img\b/gi) || []).length;
	const inlineSvg = (body.match(/<svg\b/gi) || []).length;
	const mermaid = (body.match(/^```mermaid\b/gm) || []).length;

	if (!/^[^\s/\\]+$/.test(slug)) {
		fail("结构", `slug 不合法：${slug}`, "只写一段，不含空格和路径分隔符");
	}
	const dir = path.join(WORK, slug);
	assertWritable(dir);
	fs.mkdirSync(dir, { recursive: true });

	const lines = [
		"---",
		`title: ${JSON.stringify(title)}`,
		...(cover ? [`cover: ${JSON.stringify(cover)}`] : []),
		`author: ${AUTHOR}`,
		...(sourceUrl ? [`source_url: ${JSON.stringify(sourceUrl)}`] : []),
		"---",
		"",
		body.trimStart(),
	];
	fs.writeFileSync(path.join(dir, "article.md"), lines.join("\n"), "utf8");
	const frontmatterLines = fm ? fm[0].split(/\r?\n/).length - 1 : 0;
	writeJson(path.join(dir, "layout.json"), {
		source: sourceRel.split(path.sep).join("/"),
		mappings: expanded.mappings.map(({ line, rule }) => ({
			line: line + frontmatterLines,
			rule,
		})),
	});
	writeJson(path.join(dir, "meta.json"), {
		source: abs,
		title,
		cover,
		images,
		inlineSvg,
		mermaid,
	});

	return {
		abs,
		dir,
		slug,
		title,
		chapterTitle,
		cover,
		headBase,
		summary,
		book,
		tags,
		category,
		seriesOrder,
		seriesTotal,
		coverTemplate,
		coverSubtitle,
		coverStatNum,
		coverStatCaption,
		coverStatTag,
		sourceUrl,
		images,
		inlineSvg,
		mermaid,
	};
}

// ---------- 样式内联与链接检查 ----------

function restoreSvgHeight(html) {
	return html.replace(/<svg\b[^>]*>/gi, (tag) => {
		if (!/\bheight="(?:\d+(?:\.\d+)?(?:px|vw|%)?)"/i.test(tag)) return tag;
		const style = tag.match(/\bstyle="([^"]*)"/i);
		if (!style) return tag;
		const kept = style[1]
			.split(";")
			.map((part) => part.trim())
			.filter((part) => part && !/^height\s*:/i.test(part));
		return tag.replace(style[0], `style="${kept.join("; ")}"`);
	});
}

function siteUrl() {
	if (process.env.WECHAT_SITE_URL) return process.env.WECHAT_SITE_URL.replace(/\/+$/, "");
	if (!BLOG_ROOT) return "";
	const file = path.join(BLOG_ROOT, "src", "config", "siteConfig.ts");
	let text = "";
	try {
		text = fs.readFileSync(file, "utf8");
	} catch {
		return "";
	}
	const matched = text.match(/^\s*site_url:\s*["']([^"']+)["']/m);
	return matched ? matched[1].replace(/\/+$/, "") : "";
}

function absolutizeLinks(html, url) {
	return html.replace(
		/(<a\b[^>]*?\bhref\s*=\s*)(["'])\/(?!\/)([^"']*)\2/gi,
		(_, head, quote, rest) => `${head}${quote}${url}/${rest}${quote}`,
	);
}

function checkLinkForms(html) {
	const fatal = [];
	const soft = [];
	for (const m of html.matchAll(/<a\b[^>]*?\bhref\s*=\s*(["'])(.*?)\1/gi)) {
		const href = m[2].trim();
		if (/^https?:\/\//i.test(href)) {
			if (/^https?:\/\/mp\.weixin\.qq\.com(\/|$)/i.test(href)) {
				fatal.push([href, "公众号文章地址会返回 45166"]);
			}
			continue;
		}
		if (/^(mailto:|tel:)/i.test(href)) continue;
		if (href.startsWith("#")) {
			fatal.push([href, "锚点会返回 45166"]);
		} else if (href.startsWith("/")) {
			fatal.push([href, "站内相对地址没有被补成绝对地址"]);
		} else {
			soft.push(href || "(空 href)");
		}
	}
	if (fatal.length) {
		const list = fatal
			.slice(0, 5)
			.map(([href, why]) => `${href}（${why}）`)
			.join("；");
		fail(
			"结构",
			`链接形态微信不接受：${list}`,
			"外链写 https:// 完整地址；站内链接要先设 WECHAT_SITE_URL；不要写 #锚点 或 mp.weixin.qq.com 地址",
		);
	}
	if (soft.length) {
		console.error(`提示：微信会把以下链接剥成纯文字，读者无法点击：${soft.slice(0, 5).join("；")}`);
	}
}

function renderArticle(built) {
	const mdPath = path.join(built.dir, "article.md");
	if (!fs.existsSync(mdPath)) {
		fail("结构", `文章源文件不存在：${mdPath}`, "请检查生成流程");
	}
	const rawFile = fs.readFileSync(mdPath, "utf8");
	const mdContent = rawFile.replace(/^---\r?\n[\s\S]*?\r?\n---[ \t]*\r?\n?/, "");
	const rawHtml = md.render(mdContent);
	const themeCss = fs.existsSync(THEME) ? fs.readFileSync(THEME, "utf8") : "";

	const wrappedHtml = `<section class="wx-article-root" id="wx-article">\n${rawHtml}\n</section>`;
	let inlinedHtml = wrappedHtml;
	try {
		inlinedHtml = juice.inlineContent(wrappedHtml, themeCss, {
			inlinePseudoElements: false,
			preserveImportant: true,
		});
	} catch (e) {
		fail("结构", `CSS 样式内联失败：${e.message}`, "请检查 theme.css 语法规范");
	}

	mark("inline-render");
	const site = siteUrl();
	const html = site ? absolutizeLinks(restoreSvgHeight(inlinedHtml), site) : restoreSvgHeight(inlinedHtml);
	checkLinkForms(html);
	fs.writeFileSync(path.join(built.dir, "body.html"), html, "utf8");
	mark("svg-fix-write");
	return html;
}

// ---------- 头图：底图 + 由页面排上去的文字 ----------

const HEAD_W = 1800;
const HEAD_H = 766;

const esc = (s) =>
	String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const BROWSER_CANDIDATES =
	process.platform === "win32"
		? [
				"C:/Program Files/Google/Chrome/Application/chrome.exe",
				"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
				"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
				"C:/Program Files/Microsoft/Edge/Application/msedge.exe",
			]
		: process.platform === "darwin"
			? ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
			: ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser"];

function browserCandidates() {
	const pinned = process.env.WECHAT_CHROME;
	if (pinned) return fs.existsSync(pinned) ? [pinned] : [];
	return BROWSER_CANDIDATES.filter((file) => fs.existsSync(file));
}

async function localizeBase(base, dir) {
	if (!/^https?:/i.test(base)) return base;
	const res = await fetch(base);
	if (!res.ok) fail("图片", `头图底图下载失败 HTTP ${res.status}`, base);
	const file = path.join(dir, "head-base.jpg");
	fs.writeFileSync(file, Buffer.from(await res.arrayBuffer()));
	return file;
}

function headHtml(base, { title, summary, book }) {
	const pad = Math.round(HEAD_W * 0.08);
	const unit = (v) => Math.round(HEAD_W * v);
	return `<!doctype html>
<html><head><meta charset="utf-8"><style>
html,body{margin:0;padding:0;width:${HEAD_W}px;height:${HEAD_H}px;overflow:hidden}
.cover{position:relative;width:${HEAD_W}px;height:${HEAD_H}px;overflow:hidden;background:#007275}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.shade{position:absolute;inset:0;background:rgba(0,114,117,.58)}
.safe{position:absolute;inset:0;padding:${pad}px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between;color:#fff}
.stack{display:flex;flex-direction:column;gap:${unit(0.022)}px;max-width:76%}
.title{margin:0;font-family:"Noto Sans CJK SC","PingFang SC","Microsoft YaHei",sans-serif;font-weight:700;font-size:${unit(0.044)}px;line-height:1.15;letter-spacing:-0.02em;text-wrap:balance}
.summary{display:flex;align-items:flex-start;gap:${unit(0.016)}px}
.rule{flex:none;width:${unit(0.045)}px;height:1px;margin-top:.85em;background:rgba(255,255,255,.45)}
.summary p{margin:0;font-family:"Noto Serif CJK SC","Songti SC",serif;font-size:${unit(0.0215)}px;line-height:1.6}
.book{margin:0;padding-top:${unit(0.016)}px;border-top:1px solid rgba(255,255,255,.32);font-family:"Noto Sans CJK SC","PingFang SC","Microsoft YaHei",sans-serif;font-size:${unit(0.02)}px;line-height:1.2;letter-spacing:.18em}
</style></head><body>
<div class="cover"><img class="bg" src="${pathToFileURL(base).href}" alt="">
<div class="shade"></div>
<div class="safe"><div class="stack"><p class="title" id="t">${esc(title)}</p>${
		summary ? `\n<div class="summary"><span class="rule"></span><p>${esc(summary)}</p></div>` : ""
	}</div>${book ? `<p class="book" id="b">${esc(book)}</p>` : ""}</div></div>
<script>
const safe = document.querySelector(".safe");
const stack = document.querySelector(".stack");
const title = document.getElementById("t");
const bookEl = document.getElementById("b");
const pad = parseFloat(getComputedStyle(safe).paddingTop);
const avail = safe.clientHeight - pad * 2 - (bookEl ? bookEl.offsetHeight + 20 : 0);
let size = parseFloat(getComputedStyle(title).fontSize);
while (stack.scrollHeight > avail && size > 34) {
	size -= 2;
	title.style.fontSize = size + "px";
}
if (stack.scrollHeight > avail) {
	title.style.display = "-webkit-box";
	title.style.webkitLineClamp = "3";
	title.style.overflow = "hidden";
}
document.documentElement.dataset.headSize = String(Math.round(size));
</script></body></html>`;
}

async function buildHeadImage(built) {
	const tplChoice = (built.coverTemplate || process.env.WECHAT_COVER_TEMPLATE || "e").toLowerCase();
	const tplMap = {
		a: "template-a.html",
		b: "template-b.html",
		c: "template-c.html",
		d: "template-d.html",
		e: "template-e.html",
	};
	const tplName = tplMap[tplChoice] || "template-e.html";
	const tplPath = path.join(SKILL_DIR, "templates", tplName);

	const tag = (built.tags && built.tags[0]) || built.category || "ESSAY · 观点";
	const now = new Date();
	const year = String(now.getFullYear());
	const issueDate = `${year}.${String(now.getMonth() + 1).padStart(2, "0")}`;
	const issue = `ISSUE // ${year}.${String(now.getMonth() + 1).padStart(2, "0")}.${String(now.getDate()).padStart(2, "0")}`;

	const siteStats = getSiteStats(BLOG_ROOT);
	const brand = process.env.WECHAT_BRAND || siteStats.brand || "BRAND";
	const brandUpper = brand.toUpperCase();
	const coverAuthor = AUTHOR || brand;
	let siteDomain = process.env.WECHAT_SITE_DOMAIN || "";
	if (!siteDomain) {
		try {
			const u = siteUrl();
			if (u) siteDomain = new URL(u).hostname;
		} catch {}
	}
	if (!siteDomain) siteDomain = "shxuk.cn";

	const isBook = Boolean(built.book);
	const isTool =
		built.category === "工具" ||
		built.tags.some((t) => /工具|开源|CLI|Lab/i.test(t)) ||
		/工具|开源|template|color-system/i.test(built.title);
	const coverMode = isBook ? "book" : isTool ? "tool" : "essay";
	let bookPalette = "墨青";
	if (/GEO|AI-SEO|AI 搜索/i.test(built.book)) bookPalette = "墨蓝";
	else if (/文案|写作|copywriting/i.test(built.book)) bookPalette = "墨色";
	else if (/协作|coding/i.test(built.book)) bookPalette = "暖米";
	const bookTag = /GEO|AI-SEO/i.test(built.book) ? "AI-SEO" : /文案/i.test(built.book) ? "COPY" : "BOOK";

	const spineText = isBook ? `${brandUpper} · 专著` : `${brandUpper} · 深度专题`;
	const eyebrow = isBook ? `BOOK · ${built.book}` : isTool ? "TOOL · 工程与开源" : "ESSAY · 思考与观察";
	const issueShort = built.seriesOrder ? String(built.seriesOrder).padStart(2, "0") : String(now.getMonth() + 1).padStart(2, "0");
	const issueNo =
		process.env.WECHAT_ISSUE ||
		(built.seriesOrder
			? built.seriesTotal
				? `CH. ${Number(built.seriesOrder)}/${built.seriesTotal}`
				: `CH. ${issueShort}`
			: `NO. ${issueShort}`);
	const footerSlogan = isBook ? "独立博客 · 专栏书稿连载" : "独立博客 · 深度长文阅读";
	const coverSubtitle = built.coverSubtitle || built.summary || "";
	const coverStatTag = built.coverStatTag || "KEY SIGNAL";
	const coverStatNum = built.coverStatNum || issueShort;
	const coverStatCaption = built.coverStatCaption || built.title.slice(0, 18);
	const coverHeading = built.chapterTitle || built.title;
	const titleShort = coverHeading.replace(/^[^：:]+[：:]\s*/, "").slice(0, 18);
	const bookOrTag = isBook ? built.book : isTool ? "开源工具 · TOOL" : `观点长文 · ${tag}`;

	let html = "";
	if (fs.existsSync(tplPath)) {
		html = fs
			.readFileSync(tplPath, "utf8")
			.replaceAll("{{TITLE}}", esc(coverHeading))
			.replaceAll("{{TITLE_SHORT}}", esc(titleShort))
			.replaceAll("{{BOOK_OR_TAG}}", esc(bookOrTag))
			.replaceAll("{{BOOK_TITLE}}", esc(built.book || built.title))
			.replaceAll("{{BOOK_TAG}}", esc(bookTag))
			.replaceAll("{{BOOK_PALETTE}}", esc(bookPalette))
			.replaceAll("{{COVER_MODE}}", esc(coverMode))
			.replaceAll("{{TAG}}", esc(tag))
			.replaceAll("{{ISSUE}}", esc(issue))
			.replaceAll("{{ISSUE_DATE}}", esc(issueDate))
			.replaceAll("{{ISSUE_SHORT}}", esc(issueShort))
			.replaceAll("{{YEAR}}", esc(year))
			.replaceAll("{{BRAND}}", esc(brand))
			.replaceAll("{{BRAND_UPPER}}", esc(brandUpper))
			.replaceAll("{{AUTHOR}}", esc(coverAuthor))
			.replaceAll("{{SITE_DOMAIN}}", esc(siteDomain))
			.replaceAll("{{SPINE_TEXT}}", esc(spineText))
			.replaceAll("{{EYEBROW}}", esc(eyebrow))
			.replaceAll("{{ISSUE_NO}}", esc(issueNo))
			.replaceAll("{{FOOTER_SLOGAN}}", esc(footerSlogan))
			.replaceAll("{{COVER_SUBTITLE}}", esc(coverSubtitle))
			.replaceAll("{{COVER_STAT_TAG}}", esc(coverStatTag))
			.replaceAll("{{COVER_STAT_NUM}}", esc(coverStatNum))
			.replaceAll("{{COVER_STAT_CAPTION}}", esc(coverStatCaption))
			.replaceAll("{{WORD_COUNT_LABEL}}", esc(siteStats.wordCountLabel))
			.replaceAll("{{STATUS_LABEL}}", esc(siteStats.statusLabel));
	} else {
		const base = await localizeBase(built.headBase, built.dir);
		html = headHtml(base, built);
	}

	const htmlPath = path.join(built.dir, "head.html");
	const pngPath = path.join(built.dir, "head-1800x766.png");
	if (fs.existsSync(pngPath)) fs.unlinkSync(pngPath);
	fs.writeFileSync(htmlPath, html, "utf8");

	const browsers = browserCandidates();
	if (!browsers.length) {
		fail("结构", "找不到 Chrome 或 Edge，无法生成头图", "安装 Chrome/Edge，或用 WECHAT_CHROME 指向可执行文件");
	}

	let lastStderr = "";
	for (const browser of browsers) {
		const profile = fs.mkdtempSync(path.join(os.tmpdir(), "wechat-head-"));
		const run = spawnSync(
			browser,
			[
				"--headless=new",
				"--disable-gpu",
				"--no-sandbox",
				"--hide-scrollbars",
				"--force-device-scale-factor=1",
				`--window-size=${HEAD_W},${HEAD_H}`,
				"--virtual-time-budget=5000",
				`--user-data-dir=${profile}`,
				`--screenshot=${pngPath}`,
				pathToFileURL(htmlPath).href,
			],
			{ encoding: "utf8", maxBuffer: 8 * 1024 * 1024 },
		);
		fs.rmSync(profile, { recursive: true, force: true });
		if (fs.existsSync(pngPath)) break;
		lastStderr = (run.stderr || "").trim().split(/\r?\n/).slice(-3).join(" ");
	}

	if (!fs.existsSync(pngPath)) {
		fail("结构", "头图没有生成", lastStderr || "检查 Chrome / Edge 是否可执行");
	}

	const squarePngPath = path.join(built.dir, "head-square-500x500.png");
	const squareStdPath = path.join(built.dir, "head-square.png");
	const cropBox =
		tplChoice === "e"
			? "(1250, 133, 1750, 633)"
			: tplChoice === "d"
				? "(1280, 133, 1780, 633)"
				: "(1280, 50, 1780, 550)";
	const pyCode = `from PIL import Image; im = Image.open(r'${pngPath}'); crop = im.crop(${cropBox}); crop.save(r'${squarePngPath}'); crop.save(r'${squareStdPath}')`;
	for (const pyBin of ["python3", "python"]) {
		const r = spawnSync(pyBin, ["-c", pyCode], { encoding: "utf8" });
		if (r.status === 0 && fs.existsSync(squarePngPath)) break;
	}

	return { pngPath, tplChoice };
}

// ---------- 凭证 ----------

function loadCredentials() {
	let appId = process.env.WECHAT_APP_ID || "";
	let secret = process.env.WECHAT_APP_SECRET || "";
	if (appId && secret) return { appId, secret };

	const files = [
		process.env.WECHAT_CREDENTIALS,
		path.join(SKILL_DIR, ".env"),
		path.join(SKILL_DIR, "credentials"),
		path.join(os.homedir(), ".config", "wechat", "credentials"),
	].filter(Boolean);
	for (const file of files) {
		if (!fs.existsSync(file)) continue;
		for (const line of fs.readFileSync(file, "utf8").split(/\r?\n/)) {
			const m = line.match(/^\s*(?:export\s+)?([A-Za-z_]\w*)\s*=\s*(.*?)\s*$/);
			if (!m) continue;
			const value = m[2].replace(/^(['"])(.*)\1$/, "$2");
			if (m[1] === "WECHAT_APP_ID") appId ||= value;
			if (m[1] === "WECHAT_APP_SECRET") secret ||= value;
		}
		if (appId && secret) break;
	}
	if (!appId || !secret) {
		fail(
			"凭证",
			"没有读到 AppID / AppSecret",
			`把凭证写入 ${path.join(SKILL_DIR, "credentials")} 后重跑`,
		);
	}
	return { appId, secret };
}

function wechatError(data, stage) {
	const code = data.errcode;
	const msg = data.errmsg || "";

	if (code === 40164 || /whitelist|invalid ip/i.test(msg)) {
		return new PublishError(
			"白名单",
			`${code} ${msg}`,
			"把当前出口 IP 加入公众号后台「设置与开发 → 基本配置 → IP 白名单」",
		);
	}
	if ([40001, 40013, 40125, 41002, 41004, 42001, 48001].includes(code)) {
		return new PublishError(
			"凭证",
			`${code} ${msg}`,
			"核对 AppID / AppSecret；48001 表示账号未认证或没有草稿箱 / 素材库权限",
		);
	}
	if ([40004, 40005, 40006, 40007, 40009, 40113, 41005, 45001, 45110].includes(code)) {
		return new PublishError(
			"图片",
			`${code} ${msg}`,
			"图片需 JPG / PNG、≤10MB，且 media_id 仍有效",
		);
	}
	if ([44002, 44003, 45002, 45003, 45004, 45166].includes(code)) {
		return new PublishError(
			"结构",
			`${code} ${msg}`,
			"检查标题长度、正文是否为空或超长、media_id 是否失效",
		);
	}
	if ([45009, 45011].includes(code)) {
		return new PublishError("网络", `${code} ${msg}`, "接口频率超限，等几分钟再重试");
	}
	const kind = stage === "token" ? "凭证" : stage === "image" ? "图片" : "结构";
	return new PublishError(kind, `${code} ${msg}`, "按 errcode 查微信官方文档");
}

async function wechatRequest(url, init, stage) {
	let res;
	try {
		res = await fetch(url, init);
	} catch (error) {
		fail("网络", `请求微信接口失败：${error.message}`, "确认本机可访问 api.weixin.qq.com");
	}

	const text = await res.text();
	if (!res.ok) {
		const kind = stage === "token" ? "凭证" : stage === "image" ? "图片" : "结构";
		fail(kind, `HTTP ${res.status} ${res.statusText}：${text.slice(0, 200)}`, "重试一次；持续失败再排查");
	}

	let data;
	try {
		data = JSON.parse(text);
	} catch {
		fail("结构", `微信接口返回的不是 JSON：${text.slice(0, 200)}`, "通常是网关 / 代理拦截，检查出口网络");
	}
	return data;
}

async function getToken(appId, secret) {
	const data = await wechatRequest(
		`${API}/stable_token`,
		{
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				grant_type: "client_credential",
				appid: appId,
				secret,
				force_refresh: false,
			}),
		},
		"token",
	);
	if (data.errcode) throw wechatError(data, "token");
	if (!data.access_token) {
		fail("凭证", "token 接口没有返回 access_token", "确认账号已认证、接口权限已开通");
	}
	return data.access_token;
}

// ---------- 图片 ----------

function sniffMime(buffer) {
	const head = buffer.subarray(0, 12);
	if (head.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) {
		return "image/png";
	}
	if (head[0] === 0xff && head[1] === 0xd8 && head[2] === 0xff) return "image/jpeg";
	if (head.subarray(0, 3).toString() === "GIF") return "image/gif";
	if (head.subarray(0, 4).toString() === "RIFF" && head.subarray(8, 12).toString() === "WEBP") {
		return "image/webp";
	}
	return "";
}

const EXT_BY_MIME = { "image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif" };

function mimeOf(name, buffer) {
	const sniff = sniffMime(buffer);
	if (sniff === "image/webp") {
		fail("图片", `${name} 是 WebP`, "微信不收 WebP，先导出 JPG / PNG");
	}
	if (sniff) return sniff;

	const ext = path.extname(name).toLowerCase();
	if (ext === ".webp") {
		fail("图片", `${name} 是 WebP`, "微信不收 WebP，先导出 JPG / PNG");
	}
	if (ext === ".png") return "image/png";
	if (ext === ".jpg" || ext === ".jpeg") return "image/jpeg";
	if (ext === ".gif") return "image/gif";
	return "";
}

async function uploadImage(buffer, name, token, cache, stats) {
	const hash = crypto.createHash("md5").update(buffer).digest("hex");
	if (cache[hash]) {
		stats.cached++;
		return cache[hash];
	}

	const base = path.basename(name);
	const type = mimeOf(base, buffer);
	if (!type) fail("图片", `不支持的图片类型：${base}`, "只支持 JPG / PNG / GIF");
	if (buffer.length === 0) fail("图片", `图片是空文件：${base}`, "重新导出这张图");
	if (buffer.length > 10 * 1024 * 1024) {
		fail("图片", `${base} ${(buffer.length / 1048576).toFixed(1)}MB，超过 10MB`, "压到 10MB 以内再发");
	}

	const filename = `${path.parse(base).name || "image"}${EXT_BY_MIME[type] || path.extname(base)}`;
	const form = new FormData();
	form.append("media", new Blob([buffer], { type }), filename);
	const data = await wechatRequest(
		`${API}/material/add_material?access_token=${token}&type=image`,
		{ method: "POST", body: form },
		"image",
	);
	if (data.errcode) throw wechatError(data, "image");
	if (!data.media_id || !data.url) {
		fail("图片", `上传 ${base} 没有拿到 media_id / url`, "重试一次；仍失败检查素材库权限");
	}

	const entry = {
		media_id: data.media_id,
		url: data.url.replace(/^http:\/\//i, "https://"),
		size: buffer.length,
	};
	cache[hash] = entry;
	stats.uploaded++;
	return entry;
}

async function readImage(src, sourcePath) {
	if (/^data:/i.test(src)) {
		fail("图片", "正文里有 data: 内联图片", "先存成文件，再用相对 / 绝对路径引用");
	}

	if (/^https?:\/\//i.test(src)) {
		let res;
		try {
			res = await fetch(src);
		} catch (error) {
			fail("图片", `外链图片下载失败：${src}`, error.message);
		}
		if (!res.ok) {
			fail("图片", `外链图片下载失败 HTTP ${res.status}：${src}`, "确认外链可公开访问，或先下载到本地");
		}
		let name = "image.jpg";
		try {
			name = path.basename(decodeURIComponent(new URL(src).pathname)) || name;
		} catch {}
		if (!path.extname(name)) name = `${name}.jpg`;
		return { buffer: Buffer.from(await res.arrayBuffer()), name };
	}

	let decoded = src;
	try {
		decoded = decodeURIComponent(src);
	} catch {}
	const local = path.isAbsolute(decoded)
		? decoded
		: path.resolve(path.dirname(sourcePath), decoded);
	if (!fs.existsSync(local)) {
		fail("图片", `找不到图片：${src}`, `期望路径 ${local}`);
	}
	return { buffer: fs.readFileSync(local), name: path.basename(local) };
}

async function inlineImages(html, sourcePath, token, cache, stats) {
	const attr = /(<img\b[^>]*?\bsrc\s*=\s*)(["'])([^"']*)\2/gi;
	const sources = new Set();
	for (const m of html.matchAll(attr)) sources.add(m[3]);
	if (sources.size === 0) return { html, firstMediaId: "" };

	const mapping = new Map();
	let firstMediaId = "";
	for (const src of sources) {
		if (/^https?:\/\/mmbiz\.(qpic|qlogo)\.cn\//i.test(src)) continue;
		const { buffer, name } = await readImage(src, sourcePath);
		const uploaded = await uploadImage(buffer, name, token, cache, stats);
		mapping.set(src, uploaded.url);
		if (!firstMediaId) firstMediaId = uploaded.media_id;
	}

	let output = html;
	for (const [from, to] of mapping) output = output.split(from).join(to);
	return { html: output, firstMediaId };
}

// ---------- 草稿推送 ----------

async function push(built, html, credentials) {
	const { appId, secret } = credentials;
	const token = await getToken(appId, secret);
	mark("token");

	const uploads = readJson(UPLOADS, {});
	const stats = { uploaded: 0, cached: 0 };
	const { html: content } = await inlineImages(html, built.abs, token, uploads, stats);
	mark("body-images");

	const { pngPath: head, tplChoice } = await buildHeadImage(built);
	mark("head-image");
	const { buffer, name } = await readImage(head, built.abs);
	const thumbImage = await uploadImage(buffer, name, token, uploads, stats);
	const thumb = thumbImage.media_id;
	writeJson(UPLOADS, uploads);
	mark("cover");

	const crop1x1 =
		tplChoice === "e"
			? "0.694444_0.173629_0.972222_0.826371"
			: tplChoice === "d"
				? "0.711111_0.173629_0.988889_0.826371"
				: "0.711111_0.065274_0.988889_0.718016";
	// 微信草稿 digest 上限 120 字符，截取干净的摘要用于分享卡片与列表预览
	const digest = (built.summary || "").replace(/\s+/g, " ").trim().slice(0, 118);

	const article = {
		title: built.title,
		author: AUTHOR,
		...(digest ? { digest } : {}),
		content,
		content_source_url: built.sourceUrl || "",
		thumb_media_id: thumb,
		need_open_comment: 0,
		only_fans_can_comment: 0,
		pic_crop_1_1: crop1x1,
		pic_crop_235_1: "0_0_1_1",
	};

	const drafts = readJson(DRAFTS, {});
	const previous = drafts[built.slug]?.media_id;
	let mode = "新建";

	if (previous) {
		const res = await wechatRequest(
			`${API}/draft/update?access_token=${token}`,
			{
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ media_id: previous, index: 0, articles: article }),
			},
			"draft",
		);
		if (!res.errcode) {
			mode = "更新";
			drafts[built.slug] = {
				media_id: previous,
				title: built.title,
				updated_at: new Date().toISOString(),
			};
			writeJson(DRAFTS, drafts);
		} else if (res.errcode !== 40007) {
			throw wechatError(res, "draft");
		} else {
			console.error("旧 media_id 已失效（草稿被删？），改为新建。");
		}
	}

	if (mode === "新建") {
		const res = await wechatRequest(
			`${API}/draft/add?access_token=${token}`,
			{
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ articles: [article] }),
			},
			"draft",
		);
		if (res.errcode) throw wechatError(res, "draft");
		drafts[built.slug] = {
			media_id: res.media_id,
			title: built.title,
			updated_at: new Date().toISOString(),
		};
		writeJson(DRAFTS, drafts);
	}
	mark("draft");

	const mediaId = drafts[built.slug]?.media_id || previous;
	console.log(`已${mode}草稿（未群发）`);
	console.log(`  标题：${built.title}`);
	console.log(`  原文：${built.sourceUrl || "(未设置)"}`);
	console.log(`  media_id：${mediaId}`);
	console.log(`  图片：新上传 ${stats.uploaded} / 复用 ${stats.cached}（已换成微信地址）`);
	console.log(`  草稿箱：https://mp.weixin.qq.com/`);
}

// ---------- 入口 ----------

async function main() {
	const args = process.argv.slice(2);
	const command = args[0];
	const rest = args.slice(1);
	const sourceUrl = rest.includes("--source-url")
		? rest[rest.indexOf("--source-url") + 1] || ""
		: "";
	const positional = [];
	for (let i = 0; i < rest.length; i++) {
		if (rest[i] === "--source-url") {
			i++;
			continue;
		}
		if (!rest[i].startsWith("--")) positional.push(rest[i]);
	}
	const source = positional[0] || "";

	if (!command || !["gen", "push"].includes(command) || !source) {
		console.error(
			"usage: wechat.mjs <gen|push> <文章.md> [--source-url URL] [--timing]\n" +
				"  gen       按固定模板生成内联 HTML 和 layout.json，不联网\n" +
				"  push      生成 + 换图片地址 + 合成头图 + 新建/更新草稿\n" +
				"  --timing  把每个阶段耗时打到 stderr",
		);
		process.exit(64);
	}

	const built = buildArticle(source, sourceUrl);
	mark("build");
	const credentials = command === "push" ? loadCredentials() : null;
	mark("credentials");
	const html = renderArticle(built);

	if (command === "gen") {
		let headFile = "";
		if (rest.includes("--head")) {
			const res = await buildHeadImage(built);
			headFile = res.pngPath;
		}
		console.log("已生成（未联网、未上传）");
		console.log(`  标题：${built.title}`);
		console.log(`  body.html：${path.join(built.dir, "body.html")}`);
		console.log(`  layout.json：${path.join(built.dir, "layout.json")}`);
		if (headFile) console.log(`  头图：${headFile}`);
		console.log(
			`  封面：${built.cover || "无"} · 正文图片 ${built.images} · SVG ${built.inlineSvg} · Mermaid ${built.mermaid}`,
		);
		printTiming("gen");
		return;
	}

	await push(built, html, credentials);
	printTiming("push");
}

main().catch((error) => {
	if (error instanceof PublishError) {
		console.error(`\n失败（${error.kind}）：${error.message}`);
		if (error.hint) console.error(`  处理：${error.hint}`);
		process.exit(EXIT_CODES[error.kind] || 1);
	}
	console.error(`\n失败（其他）：${error.stack || error.message}`);
	process.exit(1);
});
