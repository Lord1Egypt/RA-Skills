process.env.FEISHU_DISABLED = "true";

const mockExtractorInstance = {
  initialize: jest.fn(async () => undefined),
  detectPlatform: jest.fn((url) => (url.includes("mp.weixin.qq.com") ? "wechat" : "generic")),
  extractContent: jest.fn(async (url) => ({
    platform: url.includes("mp.weixin.qq.com") ? "wechat" : "generic",
    title: url.includes("mp.weixin.qq.com") ? "微信文章标题" : "网页标题",
    author: "作者",
    publishTime: "2026-04-15",
    sourceUrl: url,
    content: "正文内容",
  })),
};

jest.mock("./lib/dynamic-content-extractor", () => ({
  extractorInstance: mockExtractorInstance,
}));

const {
  main,
  validateWeChatLink,
  classifyContents,
  generateNotes,
  saveToFeishuCloud,
} = require("./index");

describe("happy-dog-info-organizer（精简后）", () => {
  test("链接识别：支持多链接与去重/去尾标点", async () => {
    const urls = await validateWeChatLink(
      "看这个：https://mp.weixin.qq.com/s/abc。\n以及 https://example.com/a), 再来 https://example.com/a",
    );
    expect(urls).toEqual(["https://mp.weixin.qq.com/s/abc", "https://example.com/a"]);
  });

  test("分类：缺省分类可回退到灵感", async () => {
    const ctx = { trace: [], warnings: [] };
    const classified = await classifyContents(
      [
        { title: "t1", content: "foo" },
        { title: "t2", content: "bar" },
      ],
      ctx,
    );
    expect(classified.length).toBe(2);
    expect(classified[0].classification).toBeTruthy();
    expect(typeof classified[0].classification.category).toBe("string");
  });

  test("笔记生成：产出 markdown 与 fileName", async () => {
    const ctx = { trace: [], warnings: [], traceId: "trace-test" };
    const notes = await generateNotes(
      [
        {
          platform: "wechat",
          title: "微信文章标题",
          author: "作者",
          publishTime: "2026-04-15",
          sourceUrl: "https://mp.weixin.qq.com/s/abc",
          content: "正文内容",
          classification: { category: "灵感", confidence: 60, evidence: ["默认分类"], reason: "x" },
          traceId: "trace-test",
        },
      ],
      ctx,
    );
    expect(notes.length).toBe(1);
    expect(typeof notes[0].markdown).toBe("string");
    expect(notes[0].fileName.endsWith(".md")).toBe(true);
  });

  test("飞书归档：未配置时可跳过并返回占位结果", async () => {
    const ctx = { trace: [], warnings: [] };
    const res = await saveToFeishuCloud(
      [
        {
          content: {
            title: "t",
            classification: { category: "灵感" },
            platform: "wechat",
            publishTime: "2026-04-15",
          },
          markdown: "# t",
          fileName: "t.md",
        },
      ],
      ctx,
    );
    expect(res.length).toBe(1);
    expect(res[0].fileUrl).toBe("（未归档）");
    expect(ctx.warnings.length).toBeGreaterThan(0);
  });

  test("主流程：不配置飞书也能跑通（返回统计 + trace_id）", async () => {
    const res = await main("https://mp.weixin.qq.com/s/abc\nhttps://example.com/a", {});
    expect(res.includes("✅ 处理完成")).toBe(true);
    expect(res.includes("保存成功")).toBe(true);
    expect(res.includes("trace_id:")).toBe(true);
    expect(res.includes("（未归档）")).toBe(true);
  });
});
