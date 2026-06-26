/**
 * 极简 Markdown → HTML 转换
 *
 * 范围：覆盖"聊天写知识库"场景的常见语法，不追求完整 CommonMark。
 *  - 段落（空行分段）
 *  - 标题 # / ## / ### → h3/h4/h5（Odoo 文章内 h1/h2 通常留给结构块）
 *  - 无序列表 - / *
 *  - 有序列表 1. / 2.
 *  - 行内：**bold** *italic* `code` [text](url)
 *  - 换行：单换行 → <br>
 *
 * 若传入看起来已经是 HTML（检测到 `<tag>` 样式），原样返回。
 */

const HTML_LIKE = /<(?:[a-z][\w-]*|!--|\/[a-z])/i;

export function mdToHtml(input: string): string {
  if (!input) return '';
  if (HTML_LIKE.test(input)) return input;

  // 按空行切分段落
  const blocks = input.replace(/\r\n/g, '\n').split(/\n\s*\n/);
  return blocks.map(renderBlock).filter(Boolean).join('\n');
}

function renderBlock(block: string): string {
  const lines = block.split('\n');
  if (lines.length === 0) return '';

  // 标题
  const h = /^(#{1,3})\s+(.+)$/.exec(lines[0]!);
  if (h && lines.length === 1) {
    const level = Math.min(5, h[1]!.length + 2); // # → h3, ## → h4, ### → h5
    return `<h${level}>${renderInline(h[2]!)}</h${level}>`;
  }

  // 有序列表
  if (lines.every(l => /^\s*\d+\.\s+/.test(l))) {
    const items = lines.map(l => `<li>${renderInline(l.replace(/^\s*\d+\.\s+/, ''))}</li>`);
    return `<ol>${items.join('')}</ol>`;
  }

  // 无序列表
  if (lines.every(l => /^\s*[-*]\s+/.test(l))) {
    const items = lines.map(l => `<li>${renderInline(l.replace(/^\s*[-*]\s+/, ''))}</li>`);
    return `<ul>${items.join('')}</ul>`;
  }

  // 普通段落 —— 保留软换行
  const html = lines.map(renderInline).join('<br>');
  return `<p>${html}</p>`;
}

function renderInline(text: string): string {
  let s = escapeHtml(text);
  // 链接必须在 bold/italic 之前，因为 url 里可能含 *
  s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/(?<!\*)\*([^*\s][^*]*)\*(?!\*)/g, '<em>$1</em>');
  return s;
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
