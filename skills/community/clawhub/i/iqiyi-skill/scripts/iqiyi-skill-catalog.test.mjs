import { describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import {
  buildOperationRequest,
  executeOperation,
  formatOperationResponse,
  getClientInstallLink,
  getIqiyiSkillCatalog,
  getRecommendStyleCatalog,
  normalizeRecommendStyles,
} from "./iqiyi-skill-catalog.mjs";
import { navigateChannel6, playbackControl6, playByTitle6 } from "./qips-build.mjs";

describe("iqiyi-skill no-login catalog", () => {
  it("exposes the required no-login operation ids", () => {
    const catalog = getIqiyiSkillCatalog();
    const ids = catalog.operations.map((item) => item.id);

    expect(ids).toEqual([
      "video.search",
      "video.recommend",
      "video.details",
      "star.search",
      "video.related",
      "video.episode",
      "video.play",
      "playback.qips_open_or_control",
      "client.install_check",
      "client.download_link",
      "fallback.h5_play_url",
    ]);
  });

  it("keeps login and membership flows outside the MVP", () => {
    const catalog = getIqiyiSkillCatalog();

    expect(catalog.mvpBoundary.excluded).toContain("account.login_binding");
    expect(catalog.mvpBoundary.excluded).toContain("membership.status_real_auth");
    expect(catalog.mvpBoundary.excluded).toContain("recommend.personalized_login_required");
    expect(catalog.operations.some((item) => /login|member|auth/i.test(item.id))).toBe(false);
  });

  it("documents embedded qips, fixed download link configuration, and H5 fallback", () => {
    const catalog = getIqiyiSkillCatalog();

    expect(catalog.reusedSkills).not.toContain("iqiyi-qips");
    expect(catalog.embeddedCapabilities).toContain("qips");
    expect(getClientInstallLink("mac")).toBe("https://app.iqiyi.com/mac/player/index.html");
    expect(getClientInstallLink("windows")).toBe("https://dl-static.iqiyi.com/hz/IQIYIsetup_skill01.exe");
    expect(getClientInstallLink("uwp")).toBe("https://dl-static.iqiyi.com/hz/IQIYIsetup_skill01.exe");
    expect(getClientInstallLink("windows-uwp")).toBe("https://dl-static.iqiyi.com/hz/IQIYIsetup_skill01.exe");
    expect(catalog.fallback.noClient.strategy).toBe("return_h5_play_url_and_download_tip");
    expect(catalog.operations.find((item) => item.id === "playback.qips_open_or_control").source).toBe(
      "iqiyi-skill.qips",
    );
  });

  it("builds qips deeplinks from iqiyi-skill local helpers", () => {
    expect(navigateChannel6({ channelid: 115, third_play_url: "海贼王" })).toBe(
      "qips://vtype=6;target=2;channelid=115;third_play_url=%E6%B5%B7%E8%B4%BC%E7%8E%8B;",
    );
    expect(playByTitle6({ title: "庆余年", season: 2, episode: 5 })).toBe(
      "qips://vtype=6;action=play;title=%E5%BA%86%E4%BD%99%E5%B9%B4;season=2;episode=5;",
    );
    expect(playbackControl6({ target: 102 })).toBe("qips://vtype=6;target=102;");
  });

  it("prints the catalog as JSON when executed directly", () => {
    const output = execFileSync("node", [".cursor/skills/iqiyi-skill/scripts/iqiyi-skill-catalog.mjs"], {
      encoding: "utf8",
    });
    const parsed = JSON.parse(output);

    expect(parsed.name).toBe("iqiyi-skill");
    expect(parsed.operations).toHaveLength(11);
  });

  it("builds POST JSON requests for search and details operations", () => {
    expect(buildOperationRequest("video.search", { q: "周星驰演的电影", pageNum: 2 })).toEqual({
      method: "POST",
      endpoint: "/video/search",
      url: "https://mesh.if.iqiyi.com/ai/zhipu/video/search",
      headers: {
        "content-type": "application/json",
      },
      body: {
        q: "周星驰演的电影",
        pageNum: 2,
      },
      warnings: [],
    });

    expect(buildOperationRequest("video.details", { title: "飞驰人生", season: 2, year: 2024 })).toMatchObject({
      method: "POST",
      endpoint: "/video/details",
      url: "https://mesh.if.iqiyi.com/ai/zhipu/video/details",
      body: {
        title: "飞驰人生",
        season: 2,
        year: 2024,
      },
    });
  });

  it("builds recommendation requests and downgrades auth-only sources without authorization", () => {
    expect(buildOperationRequest("video.recommend", { type: "TvSeries", style: ["古装", "2024"], kind: "hot" }))
      .toMatchObject({
        method: "POST",
        endpoint: "/video/recommend",
        body: {
          type: "TvSeries",
          style: ["古装", "2024"],
          kind: "hot",
        },
        warnings: [],
      });

    const history = buildOperationRequest("video.recommend", { type: "TvSeries", kind: "history" });

    expect(history.body).toEqual({
      type: "TvSeries",
      kind: "hot",
    });
    expect(history.warnings).toContain("kind=history requires Authorization; downgraded to hot");

    const chineseFavor = buildOperationRequest("video.recommend", { type: "Movie", kind: "收藏" });

    expect(chineseFavor.body).toEqual({
      type: "Movie",
      kind: "hot",
    });
    expect(chineseFavor.warnings).toContain("kind=favor requires Authorization; downgraded to hot");
  });

  it("exposes supported recommendation styles captured from the product filter list", () => {
    const styles = getRecommendStyleCatalog();

    expect(styles.Movie).toEqual(
      expect.arrayContaining(["喜剧", "动画", "动作", "爱情", "家庭", "少儿", "纪录片", "其他"]),
    );
    expect(styles.TvSeries).toEqual(expect.arrayContaining(["古装", "家庭", "都市", "生活", "年代"]));
    expect(styles.Variety).toEqual(expect.arrayContaining(["喜剧", "真人秀", "脱口秀", "访谈"]));
    expect(styles.Comic).toEqual(expect.arrayContaining(["玄幻", "恋爱", "搞笑", "治愈"]));
    expect(styles.Documentary).toEqual(expect.arrayContaining(["自然", "历史", "人文", "美食", "科技"]));
  });

  it("normalizes user wording to supported recommendation styles before building requests", () => {
    expect(normalizeRecommendStyles(["适合全家一起看", "合家欢", "亲子"], "Movie")).toEqual({
      styles: ["家庭"],
      warnings: [
        "style=适合全家一起看 normalized to 家庭",
        "style=合家欢 normalized to 家庭",
        "style=亲子 normalized to 家庭",
      ],
    });

    const request = buildOperationRequest("video.recommend", {
      type: "Movie",
      style: ["适合全家一起看的电影"],
      kind: "suggest",
    });

    expect(request.body).toEqual({
      type: "Movie",
      style: ["家庭"],
      kind: "suggest",
    });
    expect(request.warnings).toContain("style=适合全家一起看的电影 normalized to 家庭");
  });

  it("passes Authorization when caller provides an external token", () => {
    const request = buildOperationRequest(
      "video.recommend",
      { kind: "history" },
      { authorization: "Bearer external-token" },
    );

    expect(request.headers.Authorization).toBe("Bearer external-token");
    expect(request.body.kind).toBe("history");
    expect(request.warnings).toEqual([]);
  });

  it("executes Web API operations against the mesh endpoint and formats returned items", async () => {
    const calls = [];
    const fetchImpl = async (url, init) => {
      calls.push({ url, init });
      return {
        ok: true,
        status: 200,
        async json() {
          return {
            pageNum: 1,
            prompt: "如果用户询问‘下一页’，请把pageNum+1之后传入对应请求参数",
            intent: {
              type: "interact",
              action: "search",
              args: "周星驰演的电影",
              local: false,
            },
            col: [
              {
                id: "90264400",
                title: "九品芝麻官",
                desc: "星爷教你如何打老虎",
                url: "https://static-s.iqiyi.com/pca/uwp/new_web_player/index.html?mode=player&from=uwp&tvid=90264400",
              },
            ],
          };
        },
      };
    };

    const result = await executeOperation(
      "video.search",
      { q: "周星驰演的电影", pageNum: 1 },
      { fetchImpl },
    );

    expect(calls).toHaveLength(1);
    expect(calls[0].url).toBe("https://mesh.if.iqiyi.com/ai/zhipu/video/search");
    expect(calls[0].init).toMatchObject({
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({ q: "周星驰演的电影", pageNum: 1 }),
    });
    expect(result.formatted).toEqual({
      kind: "collection",
      message: undefined,
      prompt: "如果用户询问‘下一页’，请把pageNum+1之后传入对应请求参数",
      intent: {
        type: "interact",
        action: "search",
        args: "周星驰演的电影",
        local: false,
      },
      items: [
        {
          id: "90264400",
          title: "九品芝麻官",
          desc: "星爷教你如何打老虎",
          url: "https://static-s.iqiyi.com/pca/uwp/new_web_player/index.html?mode=player&from=uwp&tvid=90264400",
        },
      ],
      text: "1. 九品芝麻官 - 星爷教你如何打老虎\nhttps://static-s.iqiyi.com/pca/uwp/new_web_player/index.html?mode=player&from=uwp&tvid=90264400",
    });
  });

  it("formats detail-like responses from data when col is absent", () => {
    expect(
      formatOperationResponse({
        message: "已找到影片",
        data: {
          title: "功夫",
          desc: "一支穿云箭千军来相见",
          url: "https://www.iqiyi.com/v_xxx.html",
        },
      }),
    ).toEqual({
      kind: "data",
      message: "已找到影片",
      prompt: undefined,
      intent: undefined,
      data: {
        title: "功夫",
        desc: "一支穿云箭千军来相见",
        url: "https://www.iqiyi.com/v_xxx.html",
      },
      text: "功夫 - 一支穿云箭千军来相见\nhttps://www.iqiyi.com/v_xxx.html",
    });
  });
});
