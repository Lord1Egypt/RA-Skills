import { describe, expect, it } from "vitest";

import {
  buildImageFailurePlaceholder,
  sanitizeResidualImageMarkdown,
} from "./outbound.js";

describe("buildImageFailurePlaceholder", () => {
  it("uses the alt text and a default suffix when no reason is given", () => {
    expect(buildImageFailurePlaceholder("分析结果")).toBe("⚠️ 图片发送失败：分析结果");
  });

  it("falls back to 图片 when alt is empty or whitespace", () => {
    expect(buildImageFailurePlaceholder("")).toBe("⚠️ 图片发送失败：图片");
    expect(buildImageFailurePlaceholder("   ")).toBe("⚠️ 图片发送失败：图片");
  });

  it("summarizes COS-style signed-URL expiry errors", () => {
    const msg = buildImageFailurePlaceholder(
      "结果图",
      "Failed to download image (status 403): SignatureDoesNotMatch",
    );
    expect(msg).toBe("⚠️ 图片发送失败：结果图（下载链接已过期，请重试）");
  });

  it("summarizes timeout errors", () => {
    const msg = buildImageFailurePlaceholder("图", "AbortError: The operation was aborted");
    expect(msg).toBe("⚠️ 图片发送失败：图（下载超时，请重试）");
  });

  it("truncates unknown reasons to a single short line", () => {
    const reason = "some weirdo error message".padEnd(200, "x");
    const out = buildImageFailurePlaceholder("x", reason);
    expect(out.startsWith("⚠️ 图片发送失败：x（")).toBe(true);
    expect(out.length).toBeLessThan(120);
  });
});

describe("sanitizeResidualImageMarkdown", () => {
  it("replaces a simple ![](url) with a placeholder", () => {
    const input = "前文\n\n![分析图](https://cos.example.com/abc.jpg?sign=xxx)\n\n后文";
    const out = sanitizeResidualImageMarkdown(input);
    expect(out).toContain("⚠️ 图片发送失败：分析图");
    expect(out).not.toContain("cos.example.com");
    expect(out).toContain("前文");
    expect(out).toContain("后文");
  });

  it("uses 图片 when alt is empty", () => {
    const out = sanitizeResidualImageMarkdown("![](https://cos.example.com/x.jpg)");
    expect(out).toBe("⚠️ 图片发送失败：图片");
  });

  it("strips multiple images in one pass", () => {
    const input = "![一](https://a)\n![二](https://b)\nend";
    const out = sanitizeResidualImageMarkdown(input);
    expect(out).not.toContain("https://a");
    expect(out).not.toContain("https://b");
    expect(out).toContain("⚠️ 图片发送失败：一");
    expect(out).toContain("⚠️ 图片发送失败：二");
    expect(out).toContain("end");
  });

  it("handles URLs with unbalanced parens / query chars that the extractor might miss", () => {
    // 这是 extractMarkdownImages 严格正则可能漏的边缘形态：URL 里含 `(` 或 whitespace
    const input = "看图 ![结果](https://cos.example.com/path/file (1).jpg) 下面";
    const out = sanitizeResidualImageMarkdown(input);
    expect(out).not.toContain("cos.example.com");
    expect(out).toContain("⚠️ 图片发送失败：结果");
  });

  it("leaves unrelated markdown text untouched", () => {
    const input = "标题\n\n- 列表项\n- [链接](https://example.com)\n";
    const out = sanitizeResidualImageMarkdown(input);
    expect(out).toBe(input);
  });

  it("returns the input unchanged when falsy", () => {
    expect(sanitizeResidualImageMarkdown("")).toBe("");
  });
});
