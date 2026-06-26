/**
 * 将 Markdown 内容转换为企业微信 textcard 文本卡片格式。
 *
 * textcard 格式（官方文档）：
 * {
 *   "touser": "USERID",
 *   "msgtype": "textcard",
 *   "agentid": 1,
 *   "textcard": {
 *     "title": "标题",
 *     "description": "<div class=\"gray\">时间</div><div class=\"normal\">描述内容</div><div class=\"highlight\">高亮</div>",
 *     "url": "https://...",
 *     "btntxt": "更多"
 *   }
 * }
 */

export interface TextcardPayload {
  title: string;
  description: string;
  url?: string;
  btntxt?: string;
}

/**
 * 将 Markdown 文本转换为 textcard payload。
 * - 提取第一个 `# 标题` 作为 title（去掉 #）
 * - 剩余内容转为纯文本 description
 * - 图片转为 `[图片]` 文本
 * - 链接保留 `[文字](url)` 显示为 "文字: url"
 * - **粗体** 转为纯文本高亮（在 description 中保留）
 * - description 最大 512 字符
 */
export function toTextcardV1(markdown: string): TextcardPayload {
  if (!markdown) {
    return { title: "通知", description: "" };
  }

  const lines = markdown.split("\n");
  let title = "通知";
  let bodyLines: string[] = [];
  let titleFound = false;

  for (const line of lines) {
    const trimmed = line.trim();

    // 提取第一个 # 标题
    if (!titleFound && /^#\s/.test(trimmed)) {
      title = trimmed.replace(/^#+\s*/, "").trim();
      titleFound = true;
      continue;
    }

    // 跳过 bare | 行（表格分隔行），但保留其他内容
    if (/^\s*\|[-:|\s]+\|\s*$/.test(trimmed)) {
      continue;
    }

    bodyLines.push(line);
  }

  // 处理 body 内容
  let description = processBodyForTextcard(bodyLines.join("\n"));

  // 截断到 512 字符
  const MAX_DESC = 512;
  if (description.length > MAX_DESC) {
    description = description.slice(0, MAX_DESC - 6) + "...(更多)";
  }

  return {
    title,
    description,
    url: "",
    btntxt: "详情",
  };
}

function processBodyForTextcard(text: string): string {
  if (!text) return "";

  // 移除 < > HTML 标签
  let result = text.replace(/<[^>]+>/g, "");

  // 图片: ![alt](url) → [图片]
  result = result.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_, alt) => {
    const safeAlt = alt?.trim() || "图片";
    return `[图片：${safeAlt}]`;
  });
  result = result.replace(/!\[([^\]]*)\]\[[^\]]*\]/g, (_, alt) => {
    const safeAlt = alt?.trim() || "图片";
    return `[图片：${safeAlt}]`;
  });

  // 链接: [文字](url) → 文字: url
  result = result.replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, (_, label, url) => {
    return `${label}: ${url}`;
  });
  // 相对链接保留为纯文字
  result = result.replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1");

  // 粗体 **text** → 保留纯文本
  result = result.replace(/\*\*([^*]+)\*\*/g, "$1");

  // 斜体 *text* → 保留纯文本
  result = result.replace(/\*([^*\n]+)\*/g, "$1");

  // 行内代码 `code` → 保留 code
  result = result.replace(/`([^`\n]+)`/g, "$1");

  // 代码块（ fenced / indented ）→ 移除
  result = result.replace(/```[\s\S]*?```/g, "");
  result = result.replace(/(?:^    .*$\n?)+/gm, "");

  // 引用块 > text → 保留 text
  result = result.replace(/^>\s?/gm, "");

  // 任务列表 - [x] / - [ ] → 移除标记
  result = result.replace(/^(\s*[-*+])\s+\[[x ]\]\s+/gm, "$1 ");

  // 标题 ## / ### 等（首层已用于 title）→ 去掉 # 保留文字
  result = result.replace(/^#{1,6}\s+/gm, "");

  // 水平线 → 移除
  result = result.replace(/^\s*([-*_])\s*\1{2,}\s*$/gm, "");

  // 清理多余空白
  result = result.replace(/\n{3,}/g, "\n\n").trim();

  return result;
}
