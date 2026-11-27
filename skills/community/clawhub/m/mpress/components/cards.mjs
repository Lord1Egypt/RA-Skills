/**
 * 样式库 · 纯 HTML 结构组件（编辑部风 2.0：刊头、导语、数据指标卡、档案卡、双轨对照卡、行动清单、提示块、引文、代码、图注、章节）
 */
export const BOX_KINDS = {
	TIP: "tip",
	NOTE: "note",
	WARNING: "warning",
	IMPORTANT: "important",
};

export const xml = (s) =>
	String(s)
		.replace(/&/g, "&amp;")
		.replace(/</g, "&lt;")
		.replace(/>/g, "&gt;")
		.replace(/"/g, "&quot;");

// 作者会用 &lt;details&gt; 这种实体避开 HTML 解析，展开成组件时要先还原再转义
export const decode = (s) =>
	String(s)
		.replace(/&lt;/g, "<")
		.replace(/&gt;/g, ">")
		.replace(/&quot;/g, '"')
		.replace(/&#39;/g, "'")
		.replace(/&nbsp;/g, " ")
		.replace(/&amp;/g, "&");

/**
 * 将 Markdown `**加粗**` 补全为 `<strong>`
 * 修复 CommonMark 中文/标点边界及加粗内部嵌套行内代码 `code` 导致匹配破裂的问题
 */
export function cjkStrong(text) {
	const codeTokens = [];
	const masked = String(text).replace(/`[^`\n]+`/g, (m) => {
		const idx = codeTokens.length;
		codeTokens.push(m);
		return `\uE000CODE${idx}\uE001`;
	});
	const strongified = masked.replace(
		/\*\*([^\n*]+?)\*\*/g,
		"<strong>$1</strong>",
	);
	return strongified.replace(/\uE000CODE(\d+)\uE001/g, (_, idx) => codeTokens[Number(idx)]);
}

/** 解析键值对行（兼容 **Key：** Val、**Key**：Val、Key：Val） */
export function parseKv(line, maxKeyLen = 20) {
	const clean = line.trim();
	const m = clean.match(/^(?:\*\*)?([^：:*]{1,32}?)(?:\*\*)?[：:]\s*(?:\*\*)?\s*(.+)$/);
	if (m && m[1].length <= maxKeyLen) {
		const key = m[1].replace(/^\*\*|\*\*$/g, "").trim();
		const val = m[2].replace(/^\*\*|\*\*$/g, "").trim();
		return { key, val };
	}
	return null;
}

/** 组件内的行内富文本：还原实体 → 转义 → 处理反引号行内代码与加粗 */
export function compText(s) {
	const escaped = xml(decode(s));
	const withStrong = cjkStrong(escaped);
	return withStrong.replace(/`([^`\n]+)`/g, '<code class="wx-inline-code">$1</code>');
}

export function normalizeRepo(raw) {
	if (!raw) return "";
	return String(raw)
		.trim()
		.replace(/^https?:\/\/github\.com\//i, "")
		.replace(/\.git$/i, "")
		.replace(/\/$/, "");
}

export function compactHtml(html) {
	return html
		.split(/\r?\n/)
		.filter((line) => line.trim())
		.join("\n");
}

/** 刊头元信息条（上方居中引导 AI 总结 + 黑线 + 下方居中书名与章号 CH. X/N） */
export function kickerHtml(lines, inlineArg = "") {
	const raw = (inlineArg || lines.join(" · ")).replace(/\s+/g, " ").trim();
	let main = raw;
	let topSub = "AI搜索我的博客：shxuk.cn让AI帮你总结全文";
	if (raw.includes("|")) {
		const parts = raw.split("|").map((s) => s.trim()).filter(Boolean);
		main = parts[0] || "";
		if (parts[1]) topSub = parts.slice(1).join(" · ");
	} else {
		const m = raw.match(/^(.*?)\s*[·•]\s*((?:访问|AI搜索).*shxuk\.cn.*)$/i);
		if (m) {
			main = m[1].trim();
			topSub = m[2].trim();
		}
	}
	return compactHtml(
		`<section class="wx-kicker"><p class="wx-kicker-series">${compText(main)}</p><p class="wx-kicker-top">${compText(topSub)}</p></section>`,
	);
}

/** 文末永久引导关注组件（shxuk.cn | 个人博客 + 3 条互动引导） */
export function followHtml(lines, title = "") {
	const cleanTitle = (title || "shxuk.cn | 个人博客").trim();
	const bodyLines = lines.map((l) => l.trim()).filter(Boolean);
	const defaultLines = [
		"1. 关注我，或者直接在公众号里发消息，我会收得到；",
		"2. 「阅读原文」直接跳转博客，公众号上会一直发到11月30；",
		"3. 推荐：AI搜索「shxuk.cn」，让AI帮你总结",
	];
	const items = bodyLines.length ? bodyLines : defaultLines;
	const itemsHtml = items.map((line) => `<p class="wx-follow-orig">${compText(line)}</p>`).join("");
	return compactHtml(
		`<section class="wx-follow"><p class="wx-follow-head"><span class="wx-follow-brand">${compText(cleanTitle)}</span></p>${itemsHtml}</section>`,
	);
}

/** 墨青实底导语块（全文唯一实底墨青块，默认标签「字多不看：」） */
export function leadHtml(lines, title = "") {
	const paragraphs = lines
		.join("\n")
		.split(/\n{2,}/)
		.map((p) => p.replace(/\s*\n\s*/g, "").trim())
		.filter(Boolean)
		.map((p) => `<p class="wx-lead-body">${compText(p)}</p>`)
		.join("\n");
	const rawLabel = (title || "").trim();
	const finalLabel = !rawLabel || rawLabel === "核心结论" ? "字多不看：" : rawLabel;
	const label = `<p class="wx-lead-label">${xml(finalLabel)}</p>\n`;
	return compactHtml(`<section class="wx-lead">\n${label}${paragraphs}\n</section>`);
}

/**
 * 大数字指标卡（2~3 栏等宽表格布局，100% 微信兼容）
 * 每行格式：数值 | 指标名 | 补充说明（可选）
 */
export function metricsHtml(lines, title = "") {
	const items = lines
		.map((l) => l.trim())
		.filter((l) => l && !/^---+$/.test(l))
		.map((l) => l.split("|").map((s) => s.trim()))
		.filter((parts) => parts[0]);
	if (!items.length) return "";

	const colWidth = `${Math.floor(100 / items.length)}%`;
	const cells = items
		.map(([num, label = "", sub = ""]) => {
			const subHtml = sub ? `<p class="wx-metric-sub">${compText(sub)}</p>` : "";
			return `<td class="wx-metric-cell" style="width:${colWidth};"><p class="wx-metric-num">${xml(num)}</p><p class="wx-metric-label">${compText(label)}</p>${subHtml}</td>`;
		})
		.join("");

	const header = title ? `<p class="wx-metrics-title">${xml(title)}</p>` : "";
	return compactHtml(
		`<section class="wx-metrics">${header}<table class="wx-metrics-table"><tbody><tr>${cells}</tr></tbody></table></section>`,
	);
}

/**
 * 移动优先编辑部档案卡组（彻底替代手机端拥挤的多列大表格）
 * 用单独一行 `---` 分隔不同卡片；每张卡首行：`标题 | 标签（可选）`，后续每行支持 `小标题：正文`
 */
export function dossierHtml(lines, sectionTitle = "") {
	const rawBlocks = lines
		.join("\n")
		.split(/^\s*-{3,}\s*$/m)
		.map((b) => b.split(/\r?\n/).map((l) => l.trim()).filter(Boolean))
		.filter((b) => b.length);

	const cards = rawBlocks
		.map((block, idx) => {
			const [headRaw, ...rest] = block;
			const parts = headRaw.split("|").map((s) => s.trim());
			let no = String(idx + 1).padStart(2, "0");
			let name = parts[0] || "";
			let badge = parts[1] || "";
			if (parts.length >= 3) {
				if (/^\d{1,2}$/.test(parts[0])) {
					no = parts[0].padStart(2, "0");
					name = parts[1];
					badge = parts.slice(2).join(" | ");
				} else {
					name = parts[0];
					badge = parts[1];
				}
			}
			const badgeHtml = badge ? `<span class="wx-dossier-badge">${xml(badge)}</span>` : "";
			const rows = rest
				.map((line) => {
					const kv = parseKv(line, 16);
					if (kv) {
						return `<p class="wx-dossier-row"><span class="wx-dossier-key">${compText(kv.key)}</span><span class="wx-dossier-val">${compText(kv.val)}</span></p>`;
					}
					return `<p class="wx-dossier-row">${compText(line)}</p>`;
				})
				.join("\n");
			return `<section class="wx-dossier-card"><p class="wx-dossier-head"><span class="wx-dossier-no">${no}</span><span class="wx-dossier-name">${compText(name)}</span>${badgeHtml}</p>\n${rows}</section>`;
		})
		.join("\n");

	const head = sectionTitle ? `<p class="wx-dossier-section-title">${xml(sectionTitle)}</p>\n` : "";
	return compactHtml(`<section class="wx-dossier">\n${head}${cards}\n</section>`);
}

/**
 * 双轨对照实战卡（例如 ToB vs ToC，A 轨墨青 / B 轨墨黑）
 * 用 `---` 分隔左右/上下对照项；首行格式：`标题 | 副标（可选）`
 */
export function versusHtml(lines, sectionTitle = "") {
	const rawBlocks = lines
		.join("\n")
		.split(/^\s*-{3,}\s*$/m)
		.map((b) => b.split(/\r?\n/).map((l) => l.trim()).filter(Boolean))
		.filter((b) => b.length);

	const tracks = rawBlocks
		.map((block, idx) => {
			const [headRaw, ...rest] = block;
			const [title, tag = ""] = headRaw.split("|").map((s) => s.trim());
			const variant = idx % 2 === 0 ? "wx-versus-a" : "wx-versus-b";
			const tagHtml = tag ? `<span class="wx-versus-tag">${xml(tag)}</span>` : "";
			const rows = rest
				.map((line) => {
					const kv = parseKv(line, 16);
					if (kv) {
						return `<p class="wx-versus-row"><strong class="wx-versus-k">${compText(kv.key)}：</strong>${compText(kv.val)}</p>`;
					}
					return `<p class="wx-versus-row">${compText(line)}</p>`;
				})
				.join("\n");
			return `<section class="wx-versus-card ${variant}"><p class="wx-versus-head">${tagHtml}<span class="wx-versus-title">${compText(title)}</span></p><section class="wx-versus-body">\n${rows}\n</section></section>`;
		})
		.join("\n");

	const head = sectionTitle ? `<p class="wx-versus-section-title">${xml(sectionTitle)}</p>\n` : "";
	return compactHtml(`<section class="wx-versus">\n${head}${tracks}\n</section>`);
}

/**
 * 决策行动清单卡（编号方标 + 粗体要点 + 行动阐释，适合文末收藏转发）
 * 每行：`要点标题：详细阐释` 或普通条目（自动剥除前导 `- ` / `1. `）
 */
export function checklistHtml(lines, title = "行动底牌清单") {
	const items = lines
		.map((l) => l.trim().replace(/^(?:[-*]|\d+[.)、])\s*/, ""))
		.filter(Boolean);

	const rows = items
		.map((item, idx) => {
			const no = String(idx + 1).padStart(2, "0");
			const kv = parseKv(item, 28);
			const content = kv
				? `<p class="wx-check-title">${compText(kv.key)}</p><p class="wx-check-desc">${compText(kv.val)}</p>`
				: `<p class="wx-check-desc">${compText(item)}</p>`;
			return `<section class="wx-check-item"><table class="wx-check-table"><tbody><tr><td class="wx-check-no-td"><span class="wx-check-no">${no}</span></td><td class="wx-check-body-td">${content}</td></tr></tbody></table></section>`;
		})
		.join("\n");

	return compactHtml(
		`<section class="wx-checklist"><p class="wx-checklist-head">${xml(title || "行动清单")}</p>\n${rows}\n</section>`,
	);
}

/**
 * 流程步骤 / 阶梯组件 (steps)
 * 支持单行模式（每行：标题 | 标签 | 说明）与多行块模式（用 --- 分隔步骤）
 */
export function stepsHtml(lines, title = "") {
	const hasDivider = lines.some((l) => /^\s*-{3,}\s*$/.test(l));
	let itemsHtml = "";

	if (hasDivider) {
		const blocks = lines
			.join("\n")
			.split(/^\s*-{3,}\s*$/m)
			.map((b) =>
				b
					.split(/\r?\n/)
					.map((l) => l.trim())
					.filter(Boolean),
			)
			.filter((b) => b.length);

		itemsHtml = blocks
			.map((block, idx) => {
				const [headRaw, ...rest] = block;
				const [stepTitle, badge = ""] = headRaw.split("|").map((s) => s.trim());
				const no = String(idx + 1).padStart(2, "0");
				const isWarn = /阴影|警告|坑|避开|风险/.test(stepTitle + badge);
				const badgeHtml = badge
					? `<span class="wx-step-badge${isWarn ? " wx-step-badge-warn" : ""}">${xml(badge)}</span>`
					: "";
				const rows = rest
					.map((line) => {
						const m = line.match(/^([^：:]{1,20})[：:]\s*(.+)$/);
						if (m) {
							return `<p class="wx-step-row"><span class="wx-step-key">${xml(m[1])}</span><span class="wx-step-val">${compText(m[2])}</span></p>`;
						}
						return `<p class="wx-step-row">${compText(line)}</p>`;
					})
					.join("\n");
				return `<section class="wx-step-item${isWarn ? " wx-step-warn" : ""}"><table class="wx-step-table"><tbody><tr><td class="wx-step-no-td"><span class="wx-step-no${isWarn ? " wx-step-no-warn" : ""}">${isWarn ? "!" : no}</span></td><td class="wx-step-body-td"><section class="wx-step-content${isWarn ? " wx-step-content-warn" : ""}"><p class="wx-step-head"><span class="wx-step-title">${compText(stepTitle)}</span>${badgeHtml}</p>\n${rows}</section></td></tr></tbody></table></section>`;
			})
			.join("\n");
	} else {
		const rawRows = lines.map((l) => l.trim()).filter(Boolean);
		// 若存在包含 | 或以编号开头的行与普通说明行混排，自动将紧随其后的说明行归入当前步骤
		const grouped = [];
		for (const line of rawRows) {
			const isStart = line.includes("|") || /^\d+[.)、]\s*/.test(line);
			if (isStart || grouped.length === 0) {
				grouped.push([line]);
			} else {
				grouped[grouped.length - 1].push(line);
			}
		}
		itemsHtml = grouped
			.map((group, idx) => {
				const [headLine, ...extraDesc] = group;
				const cleanHead = headLine.replace(/^\d+[.)、]\s*/, "").trim();
				const parts = cleanHead.split("|").map((s) => s.trim());
				const no = String(idx + 1).padStart(2, "0");
				const stepTitle = parts[0] || "";
				let badge = "";
				let inlineDesc = "";
				if (parts.length >= 3) {
					badge = parts[1];
					inlineDesc = parts.slice(2).join(" · ");
				} else if (parts.length === 2) {
					// 若只有两段且存在后续描述行，第二段即为徽章标签；否则视作描述
					if (extraDesc.length > 0) {
						badge = parts[1];
					} else {
						inlineDesc = parts[1];
					}
				}
				const allDesc = [inlineDesc, ...extraDesc].filter(Boolean);
				const isWarn = /阴影|警告|坑|避开|风险/.test(stepTitle + badge);
				const badgeHtml = badge
					? `<span class="wx-step-badge${isWarn ? " wx-step-badge-warn" : ""}">${xml(badge)}</span>`
					: "";
				const descHtml = allDesc.map((d) => `\n<p class="wx-step-row">${compText(d)}</p>`).join("");
				return `<section class="wx-step-item${isWarn ? " wx-step-warn" : ""}"><table class="wx-step-table"><tbody><tr><td class="wx-step-no-td"><span class="wx-step-no${isWarn ? " wx-step-no-warn" : ""}">${isWarn ? "!" : no}</span></td><td class="wx-step-body-td"><section class="wx-step-content${isWarn ? " wx-step-content-warn" : ""}"><p class="wx-step-head"><span class="wx-step-title">${compText(stepTitle)}</span>${badgeHtml}</p>${descHtml}</section></td></tr></tbody></table></section>`;
			})
			.join("\n");
	}

	const head = title ? `<p class="wx-steps-title">${xml(title)}</p>\n` : "";
	return compactHtml(`<section class="wx-steps">\n${head}${itemsHtml}\n</section>`);
}

/**
 * 金句判词 / 核心结论卡 (verdict)
 */
export function verdictHtml(lines, title = "") {
	const cleaned = lines.map((l) => l.trim()).filter(Boolean);
	if (!cleaned.length) return "";
	const [main, ...subs] = cleaned;
	const labelHtml = title ? `<p class="wx-verdict-label">${xml(title)}</p>\n` : "";
	const subHtml = subs.map((s) => `<p class="wx-verdict-sub">${compText(s)}</p>`).join("\n");
	return compactHtml(
		`<section class="wx-verdict">\n${labelHtml}<p class="wx-verdict-main">${compText(main)}</p>\n${subHtml}\n</section>`,
	);
}

/**
 * 核心拷问 / 问答卡组 (qa)
 */
export function qaHtml(lines, title = "") {
	const blocks = lines
		.join("\n")
		.split(/^\s*-{3,}\s*$/m)
		.map((b) =>
			b
				.split(/\r?\n/)
				.map((l) => l.trim())
				.filter(Boolean),
		)
		.filter((b) => b.length);

	const cards = blocks
		.map((block, idx) => {
			let qText = "";
			const aLines = [];
			for (const line of block) {
				if (!qText && /^[Qq][：:]\s*/.test(line)) {
					qText = line.replace(/^[Qq][：:]\s*/, "").trim();
				} else if (/^[Aa][：:]\s*/.test(line)) {
					aLines.push(line.replace(/^[Aa][：:]\s*/, "").trim());
				} else if (!qText) {
					qText = line;
				} else {
					aLines.push(line);
				}
			}
			const no = String(idx + 1).padStart(2, "0");
			const aInner = aLines.map((l) => `<p class="wx-qa-p">${compText(l)}</p>`).join("\n");
			const aHtml = aLines.length
				? `\n<section class="wx-qa-a"><table class="wx-qa-table"><tbody><tr><td class="wx-qa-badge-td"><span class="wx-qa-badge-a">A</span></td><td class="wx-qa-text-td">${aInner}</td></tr></tbody></table></section>`
				: "";
			return `<section class="wx-qa-card"><table class="wx-qa-table"><tbody><tr><td class="wx-qa-badge-td"><span class="wx-qa-badge-q">Q${no}</span></td><td class="wx-qa-text-td"><p class="wx-qa-qtext">${compText(qText)}</p></td></tr></tbody></table>${aHtml}</section>`;
		})
		.join("\n");

	const head = title ? `<p class="wx-qa-title">${xml(title)}</p>\n` : "";
	return compactHtml(`<section class="wx-qa">\n${head}${cards}\n</section>`);
}

export function boxHtml(kind, bodyLines, title = "") {
	const label = Object.keys(BOX_KINDS).find((k) => BOX_KINDS[k] === kind);
	const body = bodyLines
		.join("\n")
		.split(/\n{2,}/)
		.map((p) => p.replace(/\s*\n\s*/g, "").trim())
		.filter(Boolean)
		.map((p) => `<p class="wx-box-body">${compText(p)}</p>`)
		.join("\n");
	const heading = title ? `<p class="wx-box-title">${compText(title)}</p>\n` : "";
	return `<section class="wx-box wx-box-${kind}"><p class="wx-box-label">${label}</p>\n${heading}${body}</section>`;
}

export function quoteHtml(paragraphs, source) {
	const body = paragraphs
		.join("\n")
		.split(/\n{2,}/)
		.map((p) => p.replace(/\s*\n\s*/g, "").trim())
		.filter(Boolean)
		.map((p) => `<p class="wx-quote-text">${compText(p)}</p>`)
		.join("\n");
	return `<section class="wx-quote">\n${body}\n<p class="wx-quote-source">${xml(source)}</p>\n</section>`;
}

export function codeHtml(lang, lines) {
	const label = lang ? `<p class="wx-pre-lang">${xml(lang.toUpperCase())}</p>\n` : "";
	const body = lines.map((line) => `<p class="wx-pre-line">${xml(line)}</p>`).join("\n");
	return `<section class="wx-pre">\n${label}<section class="wx-pre-body">\n${body}\n</section>\n</section>`;
}

export function figureHtml(alt, src, caption) {
	const figure = `<section class="wx-figure"><img src="${xml(src)}" alt="${xml(alt)}"></section>`;
	return caption ? `${figure}\n<p class="wx-caption">${compText(caption)}</p>` : figure;
}

export function chapterHtml(no, text, isFirst = false) {
	const style = isFirst ? ' style="margin-top: 8px;"' : "";
	return compactHtml(
		`<section class="wx-h2"${style}><table class="wx-h2-table" style="width: auto;"><tbody><tr><td class="wx-h2-no-td" width="34"><span class="wx-h2-no">${xml(no)}</span></td><td class="wx-h2-text-td"><span class="wx-h2-text">${compText(text)}</span></td></tr></tbody></table></section>`,
	);
}

export function blockHtml(cls, textCls, lines) {
	const text = lines.join(" ").replace(/\s+/g, " ").trim();
	const p = textCls ? `<p class="${textCls}">` : "<p>";
	return `<section class="${cls}">${p}${compText(text)}</p></section>`;
}

/** GitHub 仓库引导卡片：严格沿用 wx-box-tip 视觉家族 */
export function githubCardHtml(repo) {
	const cleanRepo = normalizeRepo(repo) || "GitHub 仓库";
	const repoUrl = cleanRepo.includes("/") ? `https://github.com/${cleanRepo}` : "https://github.com";
	return compactHtml(
		`<section class="wx-github-card"><p class="wx-github-card-label">GITHUB</p><p class="wx-github-card-repo">${xml(cleanRepo)}</p><p class="wx-github-card-url">${xml(repoUrl)}</p></section>`,
	);
}

/** 静态 HTML 盒子兜底（仅当模板把某个折叠组件显式设为 html-static 时启用） */
export function staticBoxHtml(badge, title, bodyLines, md) {
	const inner = compactHtml(md.render(bodyLines.map((l) => cjkStrong(l)).join("\n")));
	return compactHtml(
		`<section class="wx-static-box"><section class="wx-static-bar"><span class="wx-static-badge">${xml(badge)}</span><span class="wx-static-title">${compText(title)}</span></section><section class="wx-static-content">\n${inner}\n</section></section>`,
	);
}
