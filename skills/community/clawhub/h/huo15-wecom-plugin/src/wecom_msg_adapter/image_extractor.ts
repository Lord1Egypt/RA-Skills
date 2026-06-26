/**
 * Markdown 内联图片抽取
 *
 * 背景：企业微信 markdown_v2 虽然支持 `![](url)` 语法,但实际渲染受限
 * (不能渲染跨域外链图片、CDN 资源可能失效、安全策略拦截等)。
 * 更稳妥的方式是把图片从 markdown 里剥离出来,单独以 image 消息/media_id 下发,
 * 正文保留其它格式(标题/表格/链接/代码块),由调用方决定每张图的发送通道。
 */

export interface ExtractedImage {
    /** 图片说明(markdown alt 部分),空时默认"图片" */
    alt: string;
    /** 图片源地址(http/https 或本地 file 路径) */
    url: string;
}

export interface ImageExtractionResult {
    /** 从 markdown 中提取到的图片列表,按出现顺序排序 */
    images: ExtractedImage[];
    /** 去除图片语法后的剩余文本;如果完全由图片组成,则为空字符串 */
    residualText: string;
}

/**
 * 从 markdown 中抽取 `![alt](url)` 形式的内联图片。
 *
 * 规则:
 * - 支持 alt 为空 `![](url)`,自动用"图片"占位
 * - 支持 url 后的 title `![a](url "t")`,title 被忽略
 * - url 不能包含空白(按 markdown 规范)
 * - 引用式 `![alt][ref]` 不支持(企微场景极少用),原样保留
 * - 已经是普通链接 `[...](url)` 不受影响
 * - 移除图片后清理多余空行(避免 markdown 出现大段空白)
 */
export function extractMarkdownImages(markdown: string): ImageExtractionResult {
    const text = String(markdown ?? "");
    if (!text) {
        return { images: [], residualText: "" };
    }

    const images: ExtractedImage[] = [];
    const IMAGE_RE = /!\[([^\]\n]*)\]\(([^)\s]+)(?:\s+(?:"[^"]*"|'[^']*'))?\)/g;

    const stripped = text.replace(IMAGE_RE, (_match, rawAlt: string, rawUrl: string) => {
        const alt = String(rawAlt ?? "").trim() || "图片";
        const url = String(rawUrl ?? "").trim();
        if (!url) {
            // URL 异常时保留原样避免丢内容
            return _match;
        }
        images.push({ alt, url });
        return "";
    });

    // 图片消失后可能留下独占一行的空白或连续空行,收敛一下
    const residualText = stripped
        .split("\n")
        .map(line => (line.trimEnd()))
        .join("\n")
        .replace(/\n{3,}/g, "\n\n")
        .trim();

    return { images, residualText };
}
