/**
 * 样式库 · 原生 SVG + foreignObject 极简展开组件（只展开、不关闭、无透明遮罩）
 * 1. 使用 begin="click" + fill="freeze" 控制 px 绝对高度平滑展开，彻底避免 focusout 回弹；
 * 2. 去掉所有半透明渐隐遮罩，露出完整清晰文字；
 * 3. 底部留有实底「点击展开 ▾」提示栏，点击后立即隐藏（visibility="hidden"），展现全部正文。
 */
import fs from "node:fs";
import path from "node:path";
import MarkdownIt from "markdown-it";
import { cjkStrong, xml } from "./cards.mjs";

const foldMd = new MarkdownIt({ html: true, breaks: true, linkify: false });

/** 从本地 PNG / JPEG / GIF 文件头部读取真实像素宽高（零依赖） */
function getImageDimensions(src, baseDir = process.cwd()) {
	try {
		if (/^https?:/i.test(src)) return null;
		const fullPath = path.isAbsolute(src) ? src : path.resolve(baseDir, src);
		if (!fs.existsSync(fullPath)) return null;
		const buf = fs.readFileSync(fullPath);
		if (buf.length > 24 && buf.readUInt32BE(0) === 0x89504e47) {
			return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
		}
		if (buf.length > 10 && buf.toString("ascii", 0, 3) === "GIF") {
			return { width: buf.readUInt16LE(6), height: buf.readUInt16LE(8) };
		}
		if (buf.length > 4 && buf[0] === 0xff && buf[1] === 0xd8) {
			let offset = 2;
			while (offset < buf.length - 8) {
				if (buf[offset] !== 0xff) break;
				const marker = buf[offset + 1];
				if (marker === 0xc0 || marker === 0xc1 || marker === 0xc2) {
					return {
						height: buf.readUInt16BE(offset + 5),
						width: buf.readUInt16BE(offset + 7),
					};
				}
				const len = buf.readUInt16BE(offset + 2);
				offset += 2 + len;
			}
		}
	} catch {}
	return null;
}

/** 估算内部 HTML 在标准移动端容器（内容净宽约 330px）下的精确渲染高度（px） */
function estimateContentHeightPx(body, title, baseDir) {
	let px = 28; // 上下 padding: 14px * 2
	if (title) {
		const titleUnits = [...title].reduce((acc, ch) => acc + (/[\x00-\xff]/.test(ch) ? 0.56 : 1), 0);
		const titleLines = Math.max(1, Math.ceil(titleUnits / 22.5));
		px += titleLines * 23 + 8;
	}

	const lines = body.split(/\r?\n/);
	let inCode = false;
	let inParagraph = false;

	for (const raw of lines) {
		const trimmed = raw.trim();
		if (trimmed.startsWith("```")) {
			inCode = !inCode;
			px += inCode ? 10 : 16;
			continue;
		}
		if (!trimmed) {
			if (inParagraph) {
				px += 8;
				inParagraph = false;
			}
			continue;
		}
		const imgMatch = trimmed.match(/^!\[[^\]]*\]\(([^)\s]+)\)/);
		if (!inCode && imgMatch) {
			if (inParagraph) {
				px += 8;
				inParagraph = false;
			}
			const dim = getImageDimensions(imgMatch[1], baseDir);
			if (dim && dim.width > 0) {
				const renderedH = Math.round((330 / dim.width) * dim.height);
				px += renderedH + 10;
			} else {
				px += 240;
			}
			continue;
		}

		const charUnits = [...trimmed].reduce((acc, ch) => acc + (/[\x00-\xff]/.test(ch) ? 0.56 : 1), 0);
		const wrapCount = Math.max(1, Math.ceil(charUnits / (inCode ? 36 : 22.5)));
		px += wrapCount * (inCode ? 19 : 24);
		inParagraph = !inCode;
	}

	return Math.max(px + 6, 90);
}

/** 将内部 Markdown 渲染为微信安全的内联 <section class="custom-details-content"> HTML */
function renderInnerHtml(body, title) {
	const normalizedLines = body.split(/\r?\n/).map((line) => {
		const ulMatch = line.match(/^\s*[-*]\s+(.+)$/);
		if (ulMatch) return `• ${ulMatch[1]}`;
		return line;
	});

	const preprocessed = normalizedLines.map((l) => cjkStrong(l)).join("\n");
	let html = foldMd.render(preprocessed);

	html = html
		.replace(/<\/?(?:ul|ol)[^>]*>/gi, "")
		.replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, '<p style="margin: 0 0 6px; padding-left: 8px; font-size: 14.5px; line-height: 1.65; color: #111819;">$1</p>')
		.replace(/<p>/g, '<p style="margin: 0 0 8px; font-size: 14.5px; line-height: 1.65; color: #111819;">')
		.replace(/<pre><code([^>]*)>/g, '<pre style="margin: 8px 0; padding: 10px 12px; border-radius: 6px; background: #eef2f3; overflow-x: auto; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; line-height: 1.55; color: #111819;"><code$1 style="font-family: inherit; background: transparent; padding: 0;">')
		.replace(/<code>/g, '<code style="font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.88em; padding: 1px 4px; border-radius: 3px; background: #e8eeee; color: #111819;">')
		.replace(/<img([^>]+)>/g, '<img$1 style="display: block; width: 100%; height: auto; border-radius: 4px; margin: 4px 0;" />')
		.replace(/<strong>/g, '<strong style="font-weight: 700; color: #111819;">')
		.replace(/<table>/g, '<table style="width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 13px;">')
		.replace(/<th>/g, '<th style="padding: 5px 6px; border: 1px solid #d2dbdb; background: #eef4f4; font-weight: 700; text-align: left;">')
		.replace(/<td>/g, '<td style="padding: 5px 6px; border: 1px solid #d2dbdb;">');

	const titleHtml = title
		? `<p style="margin: 0 0 8px; font-size: 14.5px; line-height: 1.6; font-weight: 700; color: #111819;"><strong>${xml(title)}</strong></p>`
		: "";

	return `<section class="custom-details-content" style="padding: 14px 14px; font-size: 14.5px; line-height: 1.65; color: #111819; background: #fafbfc; box-sizing: border-box;">${titleHtml}${html}</section>`;
}

export function renderSvgFold(body, fail, title = "", baseDir = process.cwd()) {
	const totalPx = estimateContentHeightPx(body, title, baseDir);
	const collapsePx = 155;
	const needsFold = totalPx > collapsePx + 30;

	const startH = needsFold ? collapsePx : totalPx;
	const endH = totalPx;

	const innerHtml = renderInnerHtml(body, title);

	// 实底展开提示栏（无透明遮罩，只负责点击展开，展开后立即隐身消失）
	const expandBarInSvg = needsFold
		? `<g visibility="visible">
      <set attributeName="visibility" to="hidden" begin="click" fill="freeze"/>
      <foreignObject x="0" y="114" width="100%" height="41">
        <section style="text-align: center; padding: 7px 0; background: #fafbfc; border-top: 1px dashed #d8dfdf;">
          <span style="display: inline-block; padding: 2px 16px; border: 1px solid #c7d1d1; border-radius: 16px; background: #ffffff; font-size: 12px; font-weight: 600; line-height: 1.4; color: #007275;">点击展开 ▾</span>
        </section>
      </foreignObject>
    </g>`
		: "";

	return `<section class="custom-details-preview-box" style="margin: 14px 0; border: 1px solid #d8dfdf; border-radius: 8px; background: #fafbfc; overflow: hidden;">
<svg class="wx-fold-outer" xmlns="http://www.w3.org/2000/svg" width="100%" height="${startH}px" style="display: block; width: 100%; max-width: 100%; overflow: hidden; background: #fafbfc; outline: none; -webkit-tap-highlight-color: transparent;">
  <animate attributeName="height" attributeType="XML" begin="click" values="${startH}px;${endH}px" dur="0.25s" fill="freeze"/>
  <foreignObject width="100%" height="100%" x="0" y="0">
    ${innerHtml}
  </foreignObject>
  ${expandBarInSvg}
</svg>
</section>`;
}
