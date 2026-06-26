/**
 * WeChat handler tests
 * Usage: npx tsx test-wechat.ts [--e2e]
 */

import { execFile } from "node:child_process";
import { promisify } from "node:util";
import {
  extractArticleUrl,
  extractHtmlVar,
  stripWechatHtml,
  extractContentImages,
  formatUnixTimestamp,
  parseWechatHtml,
  convertWechatHtmlToMd,
} from "./wechat.js";
import type { WechatContent } from "./types.js";

const exec = promisify(execFile);

let passed = 0;
let failed = 0;

function assert(condition: boolean, label: string): void {
  if (condition) {
    passed++;
    console.log(`  ✓ ${label}`);
  } else {
    failed++;
    console.log(`  ✗ ${label}`);
  }
}

function assertEqual(actual: unknown, expected: unknown, label: string): void {
  const ok = actual === expected;
  if (!ok) {
    label += ` (got ${JSON.stringify(actual)}, expected ${JSON.stringify(expected)})`;
  }
  assert(ok, label);
}

// ---------------------------------------------------------------------------
// Unit: extractArticleUrl
// ---------------------------------------------------------------------------

function testExtractArticleUrl(): void {
  console.log("\n[extractArticleUrl]");

  const shortUrl = "https://mp.weixin.qq.com/s/AbCdEfGhIjKlMnOp";
  assertEqual(extractArticleUrl(shortUrl), shortUrl, "短链保持不变");

  const longUrl =
    "https://mp.weixin.qq.com/s?__biz=MzA4NzQzMzU4Mg==&mid=12345&idx=1&sn=abc";
  assertEqual(extractArticleUrl(longUrl), longUrl, "长链保持不变");

  let threw = false;
  try {
    extractArticleUrl("https://weibo.com/foo");
  } catch {
    threw = true;
  }
  assert(threw, "非微信链接抛出错误");

  threw = false;
  try {
    extractArticleUrl("not-a-url");
  } catch {
    threw = true;
  }
  assert(threw, "无效 URL 抛出错误");

  threw = false;
  try {
    extractArticleUrl("https://mp.weixin.qq.com/profile?src=3");
  } catch {
    threw = true;
  }
  assert(threw, "非文章页路径抛出错误");
}

// ---------------------------------------------------------------------------
// Unit: extractHtmlVar
// ---------------------------------------------------------------------------

function testExtractHtmlVar(): void {
  console.log("\n[extractHtmlVar]");

  const html = `<script>
var msg_title = "测试文章标题";
var nickname = '公众号名称';
var ct = "1712345678";
var cover = "";
var appmsgtoken = 'tok123';
</script>`;

  assertEqual(extractHtmlVar(html, "msg_title"), "测试文章标题", "双引号字符串");
  assertEqual(extractHtmlVar(html, "nickname"), "公众号名称", "单引号字符串");
  assertEqual(extractHtmlVar(html, "ct"), "1712345678", "数字字符串");
  assertEqual(extractHtmlVar(html, "cover"), "", "空字符串");
  assertEqual(extractHtmlVar(html, "appmsgtoken"), "tok123", "单引号 token");
  assertEqual(extractHtmlVar(html, "nonexistent"), null, "不存在的变量 → null");

  // 变量名含特殊字符不应匹配前缀
  const html2 = `<script>var msg_title_extra = "错误值"; var msg_title = "正确值";</script>`;
  assertEqual(extractHtmlVar(html2, "msg_title"), "正确值", "精确匹配变量名");
}

// ---------------------------------------------------------------------------
// Unit: stripWechatHtml
// ---------------------------------------------------------------------------

function testStripWechatHtml(): void {
  console.log("\n[stripWechatHtml]");

  assertEqual(stripWechatHtml("<p>你好世界</p>"), "你好世界", "去除 p 标签");
  assertEqual(stripWechatHtml("第一行<br/>第二行"), "第一行\n第二行", "br 转换为换行");
  assertEqual(
    stripWechatHtml("<style>.foo { color: red; }</style>内容"),
    "内容",
    "去除 style 标签及内容",
  );
  assertEqual(
    stripWechatHtml("<script>var x = 1;</script>内容"),
    "内容",
    "去除 script 标签及内容",
  );
  assertEqual(
    stripWechatHtml("&lt;strong&gt;&amp;测试&lt;/strong&gt;"),
    "<strong>&测试</strong>",
    "解码 HTML 实体",
  );
  assertEqual(stripWechatHtml("  前后空格  "), "前后空格", "去除首尾空格");

  const withTripleNewlines = stripWechatHtml("<p>段落一</p><p></p><p>段落二</p>");
  assert(!withTripleNewlines.includes("\n\n\n"), "连续换行不超过两个");
}

// ---------------------------------------------------------------------------
// Unit: extractContentImages
// ---------------------------------------------------------------------------

function testExtractContentImages(): void {
  console.log("\n[extractContentImages]");

  const html = `<div id="js_content">
    <img data-src="https://mmbiz.qpic.cn/real1.jpg" src="about:blank"/>
    <img src="https://mmbiz.qpic.cn/direct.jpg"/>
    <img data-src="https://mmbiz.qpic.cn/real2.jpg" src="about:blank"/>
    <img src="https://res.wx.qq.com/icon.png" data-src=""/>
    <img data-src="data:image/gif;base64,R0lGO" src="about:blank"/>
  </div>`;

  const imgs = extractContentImages(html);
  assertEqual(imgs.length, 3, "提取 3 张真实图片");
  assertEqual(imgs[0], "https://mmbiz.qpic.cn/real1.jpg", "优先使用 data-src");
  assertEqual(imgs[1], "https://mmbiz.qpic.cn/direct.jpg", "无 data-src 时使用 src");
  assertEqual(imgs[2], "https://mmbiz.qpic.cn/real2.jpg", "第三张图正确");
}

// ---------------------------------------------------------------------------
// Unit: formatUnixTimestamp
// ---------------------------------------------------------------------------

function testFormatUnixTimestamp(): void {
  console.log("\n[formatUnixTimestamp]");

  assertEqual(formatUnixTimestamp("1712345678"), "2024-04-05", "Unix 时间戳 → YYYY-MM-DD");
  const today = new Date().toISOString().slice(0, 10);
  assertEqual(formatUnixTimestamp("0"), today, "零值 → 今天");
  assertEqual(formatUnixTimestamp("invalid"), today, "无效值 → 今天");
}

// ---------------------------------------------------------------------------
// Unit: parseWechatHtml
// ---------------------------------------------------------------------------

function testParseWechatHtml(): void {
  console.log("\n[parseWechatHtml]");

  const mockHtml = `<!DOCTYPE html><html>
<head>
<meta property="og:image" content="https://og-fallback.jpg"/>
</head>
<script>
var msg_title = "测试文章";
var nickname = "测试公众号";
var ct = "1712345678";
var cover = "https://cover.jpg";
var desc = "这是文章摘要";
</script>
<div id="js_content">
  <p>文章正文第一段</p>
  <img data-src="https://mmbiz.qpic.cn/img1.jpg" src="about:blank"/>
  <p>文章正文第二段</p>
</div>
</html>`;

  const url = "https://mp.weixin.qq.com/s/TestId123";
  const result: WechatContent = parseWechatHtml(mockHtml, url);

  assertEqual(result.platform, "wechat", "platform 为 wechat");
  assertEqual(result.title, "测试文章", "title 来自 msg_title");
  assertEqual(result.author, "测试公众号", "author 来自 nickname");
  assertEqual(result.accountName, "测试公众号", "accountName 来自 nickname");
  assertEqual(result.date, "2024-04-05", "date 由 ct 时间戳转换");
  assertEqual(result.digest, "这是文章摘要", "digest 来自 desc");
  assertEqual(result.coverImage, "https://cover.jpg", "coverImage 来自 cover 变量");
  assert(result.text.includes("文章正文第一段"), "text 包含正文内容");
  assertEqual(result.images.length, 1, "提取 1 张图片");
  assertEqual(result.images[0], "https://mmbiz.qpic.cn/img1.jpg", "图片 URL 正确");
  assertEqual(result.readCount, null, "无 Cookie 时 readCount 为 null");
  assertEqual(result.likeCount, null, "无 Cookie 时 likeCount 为 null");
  assertEqual(result.inLookCount, null, "无 Cookie 时 inLookCount 为 null");
  assertEqual(result.originalUrl, url, "originalUrl 保持原始链接");
  assert(typeof result.fetchedAt === "string", "fetchedAt 存在");
  assertEqual(result.videoUrl, null, "无视频时 videoUrl 为 null");

  // og:image 作为 cover 的回退
  const htmlNoCover = mockHtml.replace(`var cover = "https://cover.jpg";`, `var cover = "";`);
  const result2 = parseWechatHtml(htmlNoCover, url);
  assertEqual(result2.coverImage, "https://og-fallback.jpg", "cover 为空时回退到 og:image");
}

// ---------------------------------------------------------------------------
// Unit: convertWechatHtmlToMd
// ---------------------------------------------------------------------------

function testConvertWechatHtmlToMd(): void {
  console.log("\n[convertWechatHtmlToMd]");

  // 1. 图片内联在段落之间
  const html1 = `<p>第一段</p><img data-src="https://mmbiz.qpic.cn/img1.jpg" src="about:blank"/><p>第二段</p>`;
  const md1 = convertWechatHtmlToMd(html1);
  assert(md1.includes("第一段"), "文本第一段保留");
  assert(md1.includes("第二段"), "文本第二段保留");
  assert(md1.includes("![](https://mmbiz.qpic.cn/img1.jpg)"), "图片转为 Markdown 格式");
  // 验证顺序：第一段 → 图片 → 第二段
  const pos1 = md1.indexOf("第一段");
  const posImg = md1.indexOf("![](");
  const pos2 = md1.indexOf("第二段");
  assert(pos1 < posImg && posImg < pos2, "图片位置在第一段之后、第二段之前（保持原文顺序）");

  // 2. UI 域名图片被过滤
  const html2 = `<p>内容</p><img src="https://res.wx.qq.com/icon.png"/>`;
  const md2 = convertWechatHtmlToMd(html2);
  assert(!md2.includes("res.wx.qq.com"), "UI 域名图片被过滤");
  assert(md2.includes("内容"), "文本仍保留");

  // 3. 优先使用 data-src
  const html3 = `<img data-src="https://mmbiz.qpic.cn/real.jpg" src="https://mmbiz.qpic.cn/placeholder.jpg"/>`;
  const md3 = convertWechatHtmlToMd(html3);
  assert(md3.includes("real.jpg"), "优先使用 data-src URL");
  assert(!md3.includes("placeholder.jpg"), "src 被 data-src 覆盖，不出现在结果中");

  // 4. 无图片时行为与 stripWechatHtml 一致
  const html4 = `<p>纯文本段落</p>`;
  const md4 = convertWechatHtmlToMd(html4);
  assertEqual(md4, "纯文本段落", "无图片时输出纯文本");

  // 5. 多图片保持各自位置
  const html5 = `<p>A</p><img data-src="https://img.com/1.jpg"/><p>B</p><img data-src="https://img.com/2.jpg"/><p>C</p>`;
  const md5 = convertWechatHtmlToMd(html5);
  const posA = md5.indexOf("A");
  const pos1st = md5.indexOf("1.jpg");
  const posB = md5.indexOf("B");
  const pos2nd = md5.indexOf("2.jpg");
  const posC = md5.indexOf("C");
  assert(posA < pos1st && pos1st < posB && posB < pos2nd && pos2nd < posC,
    "多图片各自保持在对应文本段落之间");
}

// ---------------------------------------------------------------------------
// Unit: parseWechatHtml richContent field
// ---------------------------------------------------------------------------

function testParseWechatHtmlRichContent(): void {
  console.log("\n[parseWechatHtml — richContent]");

  const mockHtml = `<!DOCTYPE html><html>
<script>
var msg_title = "富文本测试";
var nickname = "测试号";
var ct = "1712345678";
var cover = "";
var desc = "";
</script>
<div id="js_content">
  <p>开头段落</p>
  <img data-src="https://mmbiz.qpic.cn/mid.jpg" src="about:blank"/>
  <p>结尾段落</p>
</div>
</html>`;

  const result = parseWechatHtml(mockHtml, "https://mp.weixin.qq.com/s/test");

  assert(typeof result.richContent === "string" && result.richContent!.length > 0,
    "richContent 字段存在且非空");
  assert(result.richContent!.includes("开头段落"), "richContent 包含开头段落");
  assert(result.richContent!.includes("结尾段落"), "richContent 包含结尾段落");
  assert(result.richContent!.includes("![](https://mmbiz.qpic.cn/mid.jpg)"),
    "richContent 包含内联图片 Markdown");

  // 验证图片在两段文字之间
  const rc = result.richContent!;
  const pStart = rc.indexOf("开头段落");
  const pImg = rc.indexOf("![](");
  const pEnd = rc.indexOf("结尾段落");
  assert(pStart < pImg && pImg < pEnd, "图片在两段文字之间（顺序正确）");

  // text 字段仍是纯文本（无图片 Markdown）
  assert(!result.text.includes("![]("), "text 字段不含图片 Markdown（保持原有行为）");
}

// ---------------------------------------------------------------------------
// Unit: parseWechatHtml with deeply nested divs (regression for lazy-regex bug)
// ---------------------------------------------------------------------------

function testParseWechatHtmlNestedDivs(): void {
  console.log("\n[parseWechatHtml — nested divs]");

  // WeChat articles commonly wrap content in deeply nested sections/divs.
  // The lazy regex `([\s\S]*?)<\/div>` would stop at the first </div>,
  // losing everything after it. Verify all paragraphs are captured.
  const html = `<html>
<script>
var msg_title = "嵌套测试";
var nickname = "测试号";
var ct = "1712345678";
var cover = "";
var desc = "";
</script>
<div id="js_content">
  <section>
    <div class="outer">
      <div class="inner">
        <p>第一段内容</p>
      </div>
      <div class="inner">
        <p>第二段内容</p>
      </div>
    </div>
  </section>
  <p>第三段在顶层</p>
</div>
</html>`;

  const result = parseWechatHtml(html, "https://mp.weixin.qq.com/s/test");
  assert(result.text.includes("第一段内容"), "嵌套 div 中第一段被提取");
  assert(result.text.includes("第二段内容"), "嵌套 div 中第二段被提取");
  assert(result.text.includes("第三段在顶层"), "js_content 顶层第三段被提取");
}

// ---------------------------------------------------------------------------
// E2E: Full handler pipeline
// ---------------------------------------------------------------------------

async function testE2E(): Promise<void> {
  console.log("\n[E2E] 用真实微信文章链接运行处理器...");

  // 一篇公开可访问的微信文章（公开测试用）
  const testUrl =
    "https://mp.weixin.qq.com/s/5IpMVx0Lk7fBJRN-FXdFsA";

  try {
    const { stdout } = await exec(
      "npx",
      ["tsx", "wechat.ts", testUrl],
      { cwd: import.meta.dirname, timeout: 30_000 },
    );

    let result: Record<string, any>;
    try {
      result = JSON.parse(stdout);
    } catch {
      assert(false, "stdout 是合法 JSON");
      console.log("  Raw stdout:", stdout.slice(0, 200));
      return;
    }

    if (result.error) {
      console.log(`  ⚠ 处理器返回错误: ${result.error} (code: ${result.code})`);
      console.log(`  详情: ${result.details}`);
      // E2E 中网络/认证错误不算测试失败（环境问题）
      if (result.code === "NETWORK" || result.code === "AUTH") {
        console.log("  → 跳过 E2E 断言（网络/认证问题）");
        return;
      }
      assert(false, `处理器成功返回内容（错误: ${result.error}）`);
      return;
    }

    assert(true, "stdout 是合法 JSON");
    assertEqual(result.platform, "wechat", "platform 为 wechat");
    assert(typeof result.author === "string" && result.author.length > 0, "author 非空");
    assert(typeof result.text === "string" && result.text.length > 0, "text 非空");
    assert(typeof result.date === "string" && /\d{4}-\d{2}-\d{2}/.test(result.date), "date 格式正确");
    assert(typeof result.title === "string" && result.title.length > 0, "title 非空");
    assert(typeof result.fetchedAt === "string", "fetchedAt 存在");

    console.log(`  → Author: ${result.author}`);
    console.log(`  → Title: ${result.title}`);
    console.log(`  → Date: ${result.date}`);
    console.log(`  → Images: ${result.images?.length ?? 0}`);
    console.log(`  → Digest: ${(result.digest ?? "").slice(0, 50)}`);
    console.log(`  → Stats: reads=${result.readCount} likes=${result.likeCount} inLooks=${result.inLookCount}`);
  } catch (e: any) {
    assert(false, `处理器正常执行（${e.message}）`);
  }
}

async function run(): Promise<void> {
  const runE2E = process.argv.includes("--e2e");

  console.log("=== WeChat Handler Tests ===");

  testExtractArticleUrl();
  testExtractHtmlVar();
  testStripWechatHtml();
  testExtractContentImages();
  testFormatUnixTimestamp();
  testConvertWechatHtmlToMd();
  testParseWechatHtml();
  testParseWechatHtmlRichContent();
  testParseWechatHtmlNestedDivs();

  if (runE2E) {
    await testE2E();
  } else {
    console.log("\n[E2E] Skipped (pass --e2e to run)");
  }

  console.log(`\n--- Results: ${passed} passed, ${failed} failed ---`);
  if (failed > 0) process.exit(1);
}

run();
