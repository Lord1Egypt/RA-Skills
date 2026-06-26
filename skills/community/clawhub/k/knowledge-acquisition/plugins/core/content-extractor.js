// 插件元数据
const pluginMeta = {
  name: "content-extractor",
  version: "2.0.0",
  capabilities: ["basic", "advanced"],
  tier: "core",
  supportedPlatforms: ["generic", "xiaohongshu", "zhihu", "bilibili", "github"],
  features: ["content-extraction", "generic-web", "basic-classification"],
  description: "通用网页内容提取器",
  dependencies: ["axios", "cheerio"],
};

// 统一内容提取器 - 快乐小狗项目优化版
const axios = require("axios");
const cheerio = require("cheerio");
const puppeteer = require("puppeteer");
const crypto = require("crypto");
const os = require("os");
const path = require("path");
const fs = require("fs");
const ffmpeg = require("fluent-ffmpeg");

// 平台检测规则
const PLATFORM_REGEX = {
  xhs: /xiaohongshu\.com|xhslink\.com/i,
  wechat: /mp\.weixin\.qq\.com|weixin\.qq\.com/i,
  douyin: /douyin\.com|dyurl\.cn/i,
  zhihu: /zhihu\.com/i,
  bilibili: /bilibili\.com/i,
  github: /github\.com/i,
};

// 知识分类关键词（来自快乐小狗原系统）
const CATEGORY_KEYWORDS = {
  "人工智能（AI）": [
    "ai",
    "人工智能",
    "大模型",
    "机器学习",
    "深度学习",
    "llm",
    "算法",
    "神经网络",
    "agent",
    "rag",
  ],
  产品经理: [
    "产品经理",
    "prd",
    "需求",
    "用户体验",
    "原型",
    "权限设计",
    "产品迭代",
    "mvp",
    "roadmap",
    "埋点",
  ],
  "经济（投资/股票/保险/加密货币）": [
    "股票",
    "基金",
    "投资",
    "保险",
    "加密货币",
    "比特币",
    "以太坊",
    "理财",
    "经济",
    "宏观",
    "资产配置",
  ],
  心理学: ["心理学", "认知", "情绪", "人格", "潜意识", "行为", "共情", "心理", "动机", "压力"],
  商业机会: [
    "创业",
    "商机",
    "商业模式",
    "变现",
    "流量",
    "增长",
    "商业机会",
    "客户开发",
    "渠道",
    "b2b",
    "b2c",
  ],
  灵感: ["灵感", "想法", "创意", "感悟", "备忘", "金句", "启发", "洞察"],
};

class ContentExtractor {
  constructor(options = {}) {
    this.supportedPlatforms = ["generic", "xiaohongshu", "zhihu", "bilibili", "github"];
    this.config = {
      timeout: options.timeout || 15000,
      userAgent:
        options.userAgent || "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
      puppeteer: options.puppeteer || {
        headless: "new",
        args: ["--no-sandbox", "--disable-setuid-sandbox"],
      },
      ...options,
    };
  }

  ensureTempDir(prefix) {
    const id = typeof crypto.randomUUID === "function" ? crypto.randomUUID() : String(Date.now());
    const dir = path.join(os.tmpdir(), `${prefix}-${process.pid}-${id}`);
    fs.mkdirSync(dir, { recursive: true });
    return dir;
  }

  /**
   * 检测平台类型
   */
  detectPlatform(url) {
    for (const [platform, regex] of Object.entries(PLATFORM_REGEX)) {
      if (regex.test(url)) return platform;
    }
    return "web";
  }

  /**
   * 从URL提取内容（统一入口）
   */
  async extractContent(url, options = {}) {
    const platform = this.detectPlatform(url);
    let content;

    switch (platform) {
      case "xhs":
        content = await this.extractXiaohongshu(url);
        break;
      case "zhihu":
        content = await this.extractZhihu(url);
        break;
      case "bilibili":
        content = await this.extractBilibili(url);
        break;
      case "github":
        content = await this.extractGitHub(url);
        break;
      default:
        content = await this.extractGeneric(url);
    }

    const rawText =
      typeof content?.text === "string"
        ? content.text
        : typeof content?.content === "string"
          ? content.content
          : typeof content?.description === "string"
            ? content.description
            : "";

    // 自动分类
    const classification = this.classifyContent(rawText);

    // 生成摘要
    const summary = this.generateSummary(rawText);

    return {
      ...content,
      platform,
      classification,
      summary,
      extractedAt: new Date().toISOString(),
    };
  }

  /**
   * 小红书内容提取（使用Puppeteer）
   */
  async extractXiaohongshu(url) {
    if (typeof url === "string" && url.includes("xhslink.com")) {
      return await this.extractXiaohongshuWithoutBrowser(url);
    }
    let browser;
    try {
      const userDataDir = this.ensureTempDir("happy-dog-puppeteer-profile");
      const crashDir = this.ensureTempDir("happy-dog-chrome-crashpad");
      const baseArgs = Array.isArray(this.config.puppeteer?.args) ? this.config.puppeteer.args : [];
      const args = [
        ...baseArgs,
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-crash-reporter",
        "--disable-breakpad",
        "--disable-features=Crashpad",
        `--crash-dumps-dir=${crashDir}`,
      ];

      browser = await puppeteer.launch({
        ...this.config.puppeteer,
        userDataDir,
        args,
      });
      const page = await browser.newPage();
      await page.setUserAgent(this.config.userAgent);
      await page.goto(url, { waitUntil: "networkidle2", timeout: this.config.timeout * 2 });

      const content = await page.evaluate(() => {
        return {
          title:
            document.querySelector(".note-content h1")?.textContent ||
            document.querySelector('meta[property="og:title"]')?.content ||
            "小红书笔记",
          author: document.querySelector(".user-name")?.textContent || "未知作者",
          publishTime: document.querySelector(".publish-time")?.textContent || "",
          text:
            document.querySelector(".note-content")?.innerText ||
            document.querySelector("body")?.innerText ||
            "",
          images: Array.from(document.querySelectorAll("img"))
            .map((img) => ({
              url: img.src || img.dataset.src,
              alt: img.alt || "",
            }))
            .filter((img) => img.url),
          likes: document.querySelector(".likes-count")?.textContent || "0",
          collectCount: document.querySelector(".collect-count")?.textContent || "0",
        };
      });

      return content;
    } catch (error) {
      const message = error?.message || String(error);
      if (
        message.includes("Could not find Chrome") ||
        message.includes("Could not find Chromium") ||
        message.includes("Failed to launch the browser process") ||
        message.includes("chrome_crashpad_handler")
      ) {
        return await this.extractXiaohongshuWithoutBrowser(url);
      }
      throw error;
    } finally {
      if (browser) {
        await browser.close().catch(() => {});
      }
    }
  }

  async extractXiaohongshuWithoutBrowser(url) {
    const response = await axios.get(url, {
      timeout: this.config.timeout,
      maxRedirects: 5,
      headers: { "User-Agent": this.config.userAgent },
      validateStatus: (status) => status >= 200 && status < 400,
    });
    const html = response.data || "";
    const $ = cheerio.load(html);

    const title =
      $('meta[property="og:title"]').attr("content") ||
      $('meta[name="twitter:title"]').attr("content") ||
      $("title").text().trim() ||
      "小红书笔记";
    const description =
      $('meta[property="og:description"]').attr("content") ||
      $('meta[name="description"]').attr("content") ||
      "";
    const images = [
      $('meta[property="og:image"]').attr("content") || "",
      $('meta[name="twitter:image"]').attr("content") || "",
    ]
      .filter(Boolean)
      .map((u) => ({ url: u, alt: "" }));

    const bodyText = $("body").text().replace(/\s+/g, " ").trim();
    const text = bodyText ? `${description}\n${bodyText}`.trim() : description;
    return {
      title,
      author: $('meta[name="author"]').attr("content") || "未知作者",
      publishTime: "",
      text,
      images,
    };
  }

  /**
   * 知乎内容提取
   */
  async extractZhihu(url) {
    const response = await axios.get(url, {
      timeout: this.config.timeout,
      headers: { "User-Agent": this.config.userAgent },
    });

    const $ = cheerio.load(response.data);

    const type = url.includes("/answer/") ? "answer" : "question";

    if (type === "answer") {
      return {
        type: "answer",
        title: $(".QuestionHeader-title").text() || "知乎回答",
        author: $(".AuthorInfo-name").text() || "匿名用户",
        content: $(".RichContent-inner").text() || "",
        voteupCount: $(".VoteButton--up span").text() || "0",
        commentCount: $(".ContentItem-actions span").last().text() || "0",
        images: $(".RichContent-inner img")
          .map((_, el) => ({
            url: $(el).attr("src"),
            alt: $(el).attr("alt") || "",
          }))
          .get(),
      };
    } else {
      return {
        type: "question",
        title: $(".QuestionHeader-title").text() || "知乎问题",
        author: "知乎用户",
        content: $(".QuestionHeader-detail").text() || "",
        followCount: $(".NumberBoard-value").eq(0).text() || "0",
        answerCount: $(".NumberBoard-value").eq(1).text() || "0",
        images: [],
      };
    }
  }

  /**
   * B站内容提取
   */
  async extractBilibili(url) {
    const bvMatch = url.match(/(?:BV|bv)([A-Za-z0-9]+)/);
    if (!bvMatch) return null;

    const apiInfo = await axios.get(
      `https://api.bilibili.com/x/web-interface/view?bvid=BV${bvMatch[1]}`,
    );

    if (apiInfo.data.code !== 0) {
      throw new Error("B站API返回错误: " + apiInfo.data.message);
    }

    const video = apiInfo.data.data;

    // 如果是短视频，尝试提取字幕
    let subtitles = [];
    if (video.duration <= 60 && video.cid) {
      try {
        const subtitleApi = `https://api.bilibili.com/x/player/v2?cid=${video.cid}&bvid=BV${bvMatch[1]}`;
        const subtitleData = await axios.get(subtitleApi);
        if (subtitleData.data.data.subtitle?.subtitles?.length > 0) {
          subtitles = await this.parseBilibiliSubtitles(
            subtitleData.data.data.subtitle.subtitles[0].subtitle_url,
          );
        }
      } catch (e) {
        console.warn("获取B站字幕失败:", e.message);
      }
    }

    return {
      type: "video",
      title: video.title,
      author: video.owner.name,
      description: video.desc,
      duration: video.duration,
      viewCount: video.stat.view,
      danmakuCount: video.stat.danmaku,
      likeCount: video.stat.like,
      cover: video.pic,
      subtitles,
      cId: video.cid,
      tags: video.tags?.map((tag) => tag.tag_name) || [],
    };
  }

  /**
   * GitHub内容提取
   */
  async extractGitHub(url) {
    // 匹配GitHub仓库
    const repoMatch = url.match(/github\.com\/([^\/]+)\/([^\/\?#]+)/);
    if (!repoMatch) return this.extractGeneric(url);

    const [_, owner, repo] = repoMatch;
    const apiData = await axios.get(`https://api.github.com/repos/${owner}/${repo}`, {
      headers: this.config.token ? { Authorization: `token ${this.config.token}` } : {},
    });

    const repoInfo = apiData.data;

    // 获取README内容
    let readme = "";
    try {
      const readmeData = await axios.get(`https://api.github.com/repos/${owner}/${repo}/readme`, {
        headers: {
          Accept: "application/vnd.github.v3.raw",
          ...(this.config.token ? { Authorization: `token ${this.config.token}` } : {}),
        },
      });
      readme = readmeData.data.substring(0, 1000) + "..."; // 截取前1000字符
    } catch (e) {
      console.warn("获取README失败:", e.message);
    }

    return {
      type: "repository",
      name: repoInfo.name,
      fullName: repoInfo.full_name,
      description: repoInfo.description || "",
      language: repoInfo.language,
      stars: repoInfo.stargazers_count,
      forks: repoInfo.forks_count,
      issues: repoInfo.open_issues_count,
      topics: repoInfo.topics,
      author: repoInfo.owner.login,
      createdAt: repoInfo.created_at,
      updatedAt: repoInfo.updated_at,
      readme,
      url: repoInfo.html_url,
      cloneUrl: repoInfo.clone_url,
    };
  }

  /**
   * 通用网页内容提取
   */
  async extractGeneric(url) {
    const response = await axios.get(url, {
      timeout: this.config.timeout,
      headers: { "User-Agent": this.config.userAgent },
    });

    const $ = cheerio.load(response.data);

    return {
      type: "webpage",
      title: $("title").text() || $('meta[property="og:title"]').attr("content") || "未命名网页",
      author: $('meta[name="author"]').attr("content") || "未知作者",
      description:
        $('meta[property="og:description"]').attr("content") ||
        $('meta[name="description"]').attr("content") ||
        "",
      text: $("article").text() || $("main").text() || $("body").text() || "",
      publishTime: $('meta[property="article:published_time"]').attr("content") || "",
      images: $("img")
        .map((_, el) => ({
          url: $(el).attr("src"),
          alt: $(el).attr("alt") || "",
        }))
        .get()
        .filter((img) => img.url),
      url,
    };
  }

  /**
   * 内容分类（使用快乐小狗的分类系统）
   */
  classifyContent(content) {
    const lower = (content || "").toLowerCase();
    let best = null;
    let bestScore = 0;
    const evidence = {};

    Object.entries(CATEGORY_KEYWORDS).forEach(([category, words]) => {
      const matched = words.filter((word) => lower.includes(word.toLowerCase()));
      const score = matched.length / words.length;
      evidence[category] = matched;
      if (score > bestScore) {
        bestScore = score;
        best = category;
      }
    });

    const confidence = best ? Number(Math.min(99, 70 + bestScore * 200).toFixed(2)) : 0;
    return {
      category: best,
      confidence,
      evidence: evidence[best] || [],
    };
  }

  /**
   * 生成内容摘要
   */
  generateSummary(content) {
    const sentences = content
      .split(/[\n。！？!?]/)
      .map((s) => s.trim())
      .filter((s) => s.length > 10)
      .slice(0, 5);

    return sentences.slice(0, 3).map((s) => s.substring(0, 100) + (s.length > 100 ? "..." : ""));
  }

  /**
   * 解析B站字幕
   */
  async parseBilibiliSubtitles(url) {
    if (!url) return [];
    try {
      const response = await axios.get(url);
      const subtitles = JSON.parse(response.data.replace(/[\u0000-\u001F\u200B-\u200D]/g, ""));

      return (
        subtitles.body?.map((item) => ({
          timestamp: this.formatTime(item.from),
          text: item.content,
        })) || []
      );
    } catch (e) {
      console.error("字幕解析失败:", e);
      return [];
    }
  }

  /**
   * 格式化时间
   */
  formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs.toString().padStart(2, "0")}`;
  }
}

module.exports = ContentExtractor;
