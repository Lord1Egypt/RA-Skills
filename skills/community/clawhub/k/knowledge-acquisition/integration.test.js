process.env.FEISHU_DISABLED = "true";

const mockExtractorInstance = {
  initialize: jest.fn(async () => undefined),
  detectPlatform: jest.fn((url) => (url.includes("xhslink.com") ? "xiaohongshu" : "wechat")),
  extractContent: jest.fn(async (url) => {
    if (url.includes("xhslink.com")) {
      throw new Error("xhs blocked");
    }
    return {
      platform: "wechat",
      title: "微信文章标题",
      author: "作者",
      publishTime: "2026-04-15",
      sourceUrl: url,
      content: "正文内容",
    };
  }),
};

jest.mock("./lib/dynamic-content-extractor", () => ({
  extractorInstance: mockExtractorInstance,
}));

const { main } = require("./index");

describe("happy-dog-info-organizer 集成流程", () => {
  test("部分链接失败仍可返回结果与告警", async () => {
    const res = await main(
      "http://xhslink.com/o/Ay5yQKu4qjp\nhttps://mp.weixin.qq.com/s/_476kHXL5tmS6ztI_tsfJw",
      {},
    );
    expect(res.includes("✅ 处理完成")).toBe(true);
    expect(res.includes("⚠️ 警告")).toBe(true);
    expect(res.includes("xhs blocked")).toBe(true);
  });
});
