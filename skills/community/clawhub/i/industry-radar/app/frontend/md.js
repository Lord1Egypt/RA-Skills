/*
 * md.js — 极简 Markdown 渲染器（零依赖、离线可用）。
 * 仅覆盖本系统生成的简报所需语法：标题 / 引用 / 分隔线 / 列表 / 行内代码 / 加粗 / 链接 / 段落。
 * 先做 HTML 转义再解析，且仅放行 http(s) 链接，避免 XSS。
 */
(function (global) {
  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function inline(text) {
    var s = escapeHtml(text);
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (m, label, url) {
      if (!/^https?:\/\//i.test(url)) return label;
      return '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + label + "</a>";
    });
    return s;
  }

  function renderMarkdown(md) {
    var lines = String(md || "").replace(/\r\n/g, "\n").split("\n");
    var out = [];
    var inList = false;
    var inQuote = false;
    var para = [];

    function flushPara() {
      if (para.length) {
        out.push("<p>" + inline(para.join(" ")) + "</p>");
        para = [];
      }
    }
    function closeList() {
      if (inList) { out.push("</ul>"); inList = false; }
    }
    function closeQuote() {
      if (inQuote) { out.push("</blockquote>"); inQuote = false; }
    }

    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].replace(/\s+$/, "");
      if (!line.trim()) { flushPara(); closeList(); closeQuote(); continue; }

      var m;
      if ((m = line.match(/^(#{1,6})\s+(.*)$/))) {
        flushPara(); closeList(); closeQuote();
        var lvl = m[1].length;
        out.push("<h" + lvl + ">" + inline(m[2]) + "</h" + lvl + ">");
        continue;
      }
      if (/^---+$/.test(line.trim())) {
        flushPara(); closeList(); closeQuote();
        out.push("<hr/>");
        continue;
      }
      if ((m = line.match(/^>\s?(.*)$/))) {
        flushPara(); closeList();
        if (!inQuote) { out.push("<blockquote>"); inQuote = true; }
        out.push("<p>" + inline(m[1]) + "</p>");
        continue;
      }
      if ((m = line.match(/^\s*[-*]\s+(.*)$/))) {
        flushPara(); closeQuote();
        if (!inList) { out.push("<ul>"); inList = true; }
        out.push("<li>" + inline(m[1]) + "</li>");
        continue;
      }
      closeList(); closeQuote();
      para.push(line.trim());
    }
    flushPara(); closeList(); closeQuote();
    return out.join("\n");
  }

  global.renderMarkdown = renderMarkdown;
})(window);