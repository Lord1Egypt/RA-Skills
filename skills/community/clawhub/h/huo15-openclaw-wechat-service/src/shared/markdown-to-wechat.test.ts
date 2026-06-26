import { describe, expect, it } from "vitest";

import {
  renderMarkdownForWechatText,
  truncateForWechatText,
} from "./markdown-to-wechat.js";

describe("renderMarkdownForWechatText", () => {
  it("空字符串返回空", () => {
    expect(renderMarkdownForWechatText("")).toBe("");
  });

  it("纯文本不动", () => {
    expect(renderMarkdownForWechatText("hello world")).toBe("hello world");
  });

  it("# 标题转成 【标题】", () => {
    expect(renderMarkdownForWechatText("# 教程\n正文")).toBe("【教程】\n正文");
    expect(renderMarkdownForWechatText("## 副标题")).toBe("【副标题】");
    expect(renderMarkdownForWechatText("### 三级")).toBe("【三级】");
  });

  it("**bold** / __bold__ 去标记", () => {
    expect(renderMarkdownForWechatText("**重点**说明")).toBe("重点说明");
    expect(renderMarkdownForWechatText("see __this__ first")).toBe("see this first");
  });

  it("*italic* 去标记但保留独立的 *", () => {
    expect(renderMarkdownForWechatText("a *hi* b")).toBe("a hi b");
    expect(renderMarkdownForWechatText("foo *bar* baz")).toBe("foo bar baz");
  });

  it("~~strike~~ 去标记", () => {
    expect(renderMarkdownForWechatText("~~old~~ new")).toBe("old new");
  });

  it("[txt](url) 转成 a 标签", () => {
    const out = renderMarkdownForWechatText("点 [文档](https://docs.x.com/y) 看");
    expect(out).toBe('点 <a href="https://docs.x.com/y">文档</a> 看');
  });

  it("![alt](url) 转成 [图片] 占位", () => {
    expect(renderMarkdownForWechatText("![logo](https://x.com/a.png)")).toBe(
      "[图片] https://x.com/a.png",
    );
  });

  it("无序列表 - * + 转成 •", () => {
    const md = "- 第一\n* 第二\n+ 第三";
    expect(renderMarkdownForWechatText(md)).toBe("• 第一\n• 第二\n• 第三");
  });

  it("有序列表保留", () => {
    expect(renderMarkdownForWechatText("1. 一\n2. 二")).toBe("1. 一\n2. 二");
  });

  it("> 引用转成 ▎", () => {
    expect(renderMarkdownForWechatText("> 注意这条")).toBe("▎ 注意这条");
  });

  it("--- 转成长破折号分隔线", () => {
    expect(renderMarkdownForWechatText("上面\n---\n下面")).toBe(
      "上面\n————————\n下面",
    );
  });

  it("行内 `code` 去反引号", () => {
    expect(renderMarkdownForWechatText("用 `npm install` 装")).toBe("用 npm install 装");
  });

  it("围栏代码块去围栏保留代码", () => {
    const md = "```python\nprint(1)\nprint(2)\n```";
    expect(renderMarkdownForWechatText(md)).toBe("print(1)\nprint(2)");
  });

  it("多余空行折叠为最多两个", () => {
    expect(renderMarkdownForWechatText("a\n\n\n\n\nb")).toBe("a\n\nb");
  });

  it("a*b*c 不被误吃成 italic", () => {
    expect(renderMarkdownForWechatText("a*b*c")).toBe("a*b*c");
  });

  it("综合：模拟 LLM 真实输出", () => {
    const md = [
      "# 入门 Python",
      "",
      "## 第一步",
      "**变量**赋值是这样写的：",
      "",
      "```python",
      "x = 1",
      "```",
      "",
      "更多内容看 [官方教程](https://docs.python.org/zh-cn/3/tutorial/)。",
      "",
      "- 步骤一",
      "- 步骤二",
    ].join("\n");
    const out = renderMarkdownForWechatText(md);
    expect(out).toContain("【入门 Python】");
    expect(out).toContain("【第一步】");
    expect(out).toContain("变量赋值是这样写的：");
    expect(out).toContain("x = 1");
    expect(out).toContain('<a href="https://docs.python.org/zh-cn/3/tutorial/">官方教程</a>');
    expect(out).toContain("• 步骤一");
    expect(out).toContain("• 步骤二");
    expect(out).not.toContain("**");
    expect(out).not.toContain("```");
    expect(out).not.toContain("# ");
  });

  it("超链 url 中的双引号被转义", () => {
    const out = renderMarkdownForWechatText('[x](https://a.com/?q="bad")');
    expect(out).toContain("&quot;");
    expect(out).not.toContain('href="https://a.com/?q=""');
  });
});

describe("renderMarkdownForWechatText — v2.3.1 增强", () => {
  it("<br> / <br/> 换行", () => {
    expect(renderMarkdownForWechatText("行一<br>行二<br/>行三")).toBe(
      "行一\n行二\n行三",
    );
  });

  it("GFM 表格 → 全角分隔可读化", () => {
    const md = "| 列1 | 列2 | 列3 |\n|---|---|---|\n| A | B | C |\n| D | E | F |";
    const out = renderMarkdownForWechatText(md);
    expect(out).toContain("列1  ｜  列2  ｜  列3");
    expect(out).toContain("A  ｜  B  ｜  C");
    expect(out).toContain("D  ｜  E  ｜  F");
    expect(out).not.toContain("---");
  });

  it("幂等：渲染过一次再过一次输出不变", () => {
    const md = "# 标题\n**加粗** [链接](https://x.com)\n- 一\n- 二";
    const once = renderMarkdownForWechatText(md);
    const twice = renderMarkdownForWechatText(once);
    expect(twice).toBe(once);
  });

  it("幂等：a 标签不会被二次解析", () => {
    const once = renderMarkdownForWechatText("[文档](https://x.com/y)");
    expect(once).toBe('<a href="https://x.com/y">文档</a>');
    const twice = renderMarkdownForWechatText(once);
    expect(twice).toBe(once);
  });
});

describe("truncateForWechatText (v2.3.5+ 字节截断)", () => {
  const enc = new TextEncoder();
  const bytes = (s: string) => enc.encode(s).length;

  it("短字符串原样返回", () => {
    expect(truncateForWechatText("hi", 100)).toBe("hi");
  });

  it("纯英文按字节截断 + 省略号", () => {
    const t = truncateForWechatText("a".repeat(2100), 100);
    expect(bytes(t)).toBeLessThanOrEqual(100);
    expect(t.endsWith("…")).toBe(true);
  });

  it("纯中文按字节截断（中文 1 字 = 3 字节）", () => {
    const chinese = "中".repeat(1000); // 3000 字节
    const t = truncateForWechatText(chinese, 100); // ~33 字
    expect(bytes(t)).toBeLessThanOrEqual(100);
    expect(t.endsWith("…")).toBe(true);
    // 33 字 × 3 = 99 字节 + 省略号 3 字节 = 102，留余量后实际约 32 字
    expect(t.length).toBeGreaterThan(20);
    expect(t.length).toBeLessThan(40);
  });

  it("emoji（4 字节 UTF-8）也能正确截", () => {
    const s = "🎉".repeat(50); // 4 字节 × 50 = 200 字节
    const t = truncateForWechatText(s, 50);
    expect(bytes(t)).toBeLessThanOrEqual(50);
    expect(t.endsWith("…")).toBe(true);
  });

  it("默认 maxBytes=1900：600 汉字（1800 字节）原样返回", () => {
    const s = "中".repeat(600);
    const t = truncateForWechatText(s);
    expect(t).toBe(s); // 1800 < 1900
  });

  it("默认 maxBytes=1900：700 汉字（2100 字节）会被截", () => {
    const s = "中".repeat(700);
    const t = truncateForWechatText(s);
    expect(bytes(t)).toBeLessThanOrEqual(1900);
    expect(t.endsWith("…")).toBe(true);
  });

  it("不会截在 <a href> 标签内部（避免 XML 错乱）", () => {
    // 构造一个会刚好截在 a 标签里的情形
    const prefix = "a".repeat(100);
    const link = '<a href="https://www.example.com/very-long-url-that-extends-far-beyond">链接文字</a>';
    const s = prefix + link + "尾巴".repeat(20);
    // 选一个会落在 a 标签内部的 maxBytes
    const t = truncateForWechatText(s, 130);
    // 验证：截断后不应该有不闭合的 <a
    const openCount = (t.match(/<a /g) || []).length;
    const closeCount = (t.match(/<\/a>/g) || []).length;
    expect(openCount).toBe(closeCount);
  });
});
