/**
 * **Markdown → 微信公众号客服消息 text 渲染器（v2.3.0+）**
 *
 * 微信公众号 `cgi-bin/message/custom/send` 的 `msgtype=text` content 字段：
 *  - 支持 `\n` 换行
 *  - 支持 emoji（unicode + 微信表情码 `[微笑]`）
 *  - 支持 `<a href="...">text</a>` 超链接（公众号客户端会渲染成可点链接）
 *  - **不支持** markdown 渲染（# / ** / - 这些会以纯字符显示）
 *  - **不支持** `<b>` / `<strong>` / `<i>` 等其他 HTML 标签
 *
 * LLM 输出常常自带 markdown，直接发给粉丝会看到一堆 `**`、`#`、`-` 字符。
 * 这个模块把 LLM 的 markdown 降级渲染为对粉丝友好的纯文本排版。
 *
 * 设计原则：
 *  - 不引入 markdown 解析器 dep（保持插件 install 体积）
 *  - 行级处理，O(n) 单遍
 *  - 失败兜底返回原文（永远不抛错）
 */

const ZERO_WIDTH = /[​-‍﻿]/g;

/**
 * 把 LLM 输出的 markdown 文本渲染成微信公众号 text 客服消息可识别的"轻富文本"。
 *
 * 转换规则：
 *  | 输入                       | 输出                                |
 *  |----------------------------|-------------------------------------|
 *  | `# 标题` / `## 标题`        | `【标题】`                          |
 *  | `**bold**` / `__bold__`     | `bold`（去标记，公众号 text 不支持加粗）|
 *  | `*italic*` / `_italic_`     | `italic`                            |
 *  | `~~strike~~`                | `strike`                            |
 *  | `[txt](url)`                | `<a href="url">txt</a>`             |
 *  | `![alt](url)`               | `[图片] url`                        |
 *  | `- item` / `* item`         | `• item`                            |
 *  | `1. item`                   | `1. item`（保留）                   |
 *  | `> quote`                   | `▎ quote`                           |
 *  | `` `code` ``                | `code`（去反引号）                   |
 *  | ```` ```block``` ````       | `block`（去围栏，保留代码内容）       |
 *  | `---` / `***` / `___`       | `————————`                          |
 *  | 多空行                       | 折叠为最多两个                       |
 */
export function renderMarkdownForWechatText(input: string): string {
  if (!input) return "";

  try {
    let text = input.replace(ZERO_WIDTH, "");

    // 0. HTML <br> / <br/> 换行 → \n（LLM 偶尔会输出）
    text = text.replace(/<br\s*\/?>/gi, "\n");

    // 1. 围栏代码块 ``` ```：保留代码内容，去掉围栏行
    text = text.replace(/```[a-zA-Z0-9_-]*\n?([\s\S]*?)```/g, (_, code: string) => {
      return code.replace(/\n+$/, "");
    });

    // 2. 行内代码 `code`
    text = text.replace(/`([^`\n]+)`/g, "$1");

    // 3. 图片占位 ![alt](url) —— 必须在普通链接之前
    text = text.replace(/!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g, (_, _alt, url) => {
      return `[图片] ${url}`;
    });

    // 4. 链接 [txt](url) —— 微信支持原生 a 标签
    text = text.replace(/\[([^\]]+)\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g, (_, txt, url) => {
      const safeUrl = String(url).replace(/"/g, "&quot;").trim();
      return `<a href="${safeUrl}">${txt}</a>`;
    });

    // 5. 行级处理：标题 / 列表 / 引用 / 分隔线 / 表格
    //    GFM 表格 `| col | col |\n|---|---|` 在公众号 text 里没法渲染成网格，
    //    把分隔行（---|---）干掉、数据行 `|` 转成 `｜` 全角分隔保留可读性。
    const lines = text.split(/\r?\n/).map((rawLine) => {
      const line = rawLine.replace(/\s+$/, "");

      // 分隔线
      if (/^\s*(?:-{3,}|\*{3,}|_{3,})\s*$/.test(line)) {
        return "————————";
      }
      // 表格分隔行 |---|---|---|（删除整行）
      if (/^\s*\|?[\s:|-]+\|[\s:|-]+\|?\s*$/.test(line) && /-{3,}/.test(line)) {
        return "__WECHAT_DROP_LINE__";
      }
      // 表格数据行 | a | b | c | → a ｜ b ｜ c
      if (/^\s*\|.*\|\s*$/.test(line) && line.split("|").length >= 3) {
        const cells = line
          .trim()
          .replace(/^\||\|$/g, "")
          .split("|")
          .map((c) => c.trim())
          .filter((c) => c.length > 0);
        if (cells.length > 0) return cells.join("  ｜  ");
      }
      // 标题
      const heading = /^(\s*)(#{1,6})\s+(.*)$/.exec(line);
      if (heading) {
        return `${heading[1]}【${heading[3]?.trim() ?? ""}】`;
      }
      // 引用
      const quote = /^(\s*)>\s?(.*)$/.exec(line);
      if (quote) {
        return `${quote[1]}▎ ${quote[2] ?? ""}`;
      }
      // 无序列表 - / * / +（不能误伤 *italic*）
      const ul = /^(\s*)[-*+]\s+(.+)$/.exec(line);
      if (ul) {
        return `${ul[1]}• ${ul[2]}`;
      }
      // 有序列表保留原样（粉丝看 1. 2. 3. 是 OK 的）
      return line;
    });

    text = lines.filter((l) => l !== "__WECHAT_DROP_LINE__").join("\n");

    // 6. 去掉粗体 / 斜体 / 删除线标记（位置无关，留下文本）
    //    顺序：粗体两符（** __）→ 删除线 → 单符（* _）
    text = text.replace(/\*\*([^*\n]+)\*\*/g, "$1");
    text = text.replace(/__([^_\n]+)__/g, "$1");
    text = text.replace(/~~([^~\n]+)~~/g, "$1");
    // 单符 italic：要求两侧不是字母/数字/_/* 自身（避免吃 a*b*c 这种）
    text = text.replace(/(^|[^*\w])\*([^*\n]+)\*(?=$|[^*\w])/g, "$1$2");
    text = text.replace(/(^|[^_\w])_([^_\n]+)_(?=$|[^_\w])/g, "$1$2");

    // 7. 折叠超过 2 个连续空行为 2 个
    text = text.replace(/\n{3,}/g, "\n\n");

    return text.trim();
  } catch {
    return input;
  }
}

/**
 * **按字节截断（v2.3.5+ 修订）**
 *
 * 微信公众号客服消息 `cgi-bin/message/custom/send` 的 `text.content` 限制是
 * **UTF-8 字节数 2048**（接口返回 `errcode: 45002 content size out of limit`），
 * 不是字符数。
 *
 * 中文 / emoji 在 UTF-8 占 3-4 字节，所以"2000 字符"在中文场景 = 6000+ 字节远超限。
 *
 * 实际可用区间（含 `<a href>` 标签开销）：
 *  - 纯中文：≤ 600 汉字（≈ 1800 字节，留 248 字节安全余量）
 *  - 纯英文：≤ 2000 字符
 *  - 中英混合：取中间
 *
 * 默认 `maxBytes=1900` 留 148 字节余量给微信网关 envelope / `<a href>` 标签等。
 *
 * **保护 `<a href>` 不被截在中间**：截断点落在 `<a href="..."` 内部会导致 XML 报错。
 * 算法：先按字节切，再回扫到最近的"非标签"边界（`>` 之后 或 纯文本字符之间）。
 */
export function truncateForWechatText(text: string, maxBytes = 1900): string {
  const encoder = new TextEncoder();
  const bytes = encoder.encode(text);
  if (bytes.length <= maxBytes) return text;

  // 二分找到最大 char index 使 utf-8 bytes <= maxBytes - 3（留 "…" 的 3 字节）
  const limit = maxBytes - 3;
  let lo = 0;
  let hi = text.length;
  while (lo < hi) {
    const mid = (lo + hi + 1) >>> 1;
    const slice = text.slice(0, mid);
    if (encoder.encode(slice).length <= limit) lo = mid;
    else hi = mid - 1;
  }
  let cut = lo;

  // 把 cut 回扫到最近的"非标签内部"位置：
  //  如果当前位置之前最后一个 `<` 之后没有 `>`，说明截在标签里，回退到 `<` 之前
  const prefix = text.slice(0, cut);
  const lastOpen = prefix.lastIndexOf("<");
  const lastClose = prefix.lastIndexOf(">");
  if (lastOpen > lastClose) {
    cut = lastOpen;
  }

  return text.slice(0, cut) + "…";
}
