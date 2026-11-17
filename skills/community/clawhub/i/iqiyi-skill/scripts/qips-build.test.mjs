/**
 * Golden 与 SKILL.md、references/qips/vtype-recipes.md 中的示例对齐；改文档时请同步更新期望值。
 */
import { describe, it, expect } from "vitest";
import {
  buildQips,
  navigateChannel6,
  navigateChannel7,
  playbackControl6,
  playByTitle6,
  thirdPlayUrlFromJson,
  vodPlay0,
} from "./qips-build.mjs";

describe("buildQips", () => {
  it("encodes values and keeps trailing semicolon", () => {
    expect(
      buildQips([
        { key: "vtype", value: 6 },
        { key: "target", value: 2 },
        { key: "channelid", value: 1 },
      ]),
    ).toBe("qips://vtype=6;target=2;channelid=1;");
  });

  it("rejects unsafe qips keys before building a deeplink", () => {
    expect(() => buildQips([{ key: "vtype;target", value: 6 }])).toThrow("Unsafe qips key");
  });

  it("rejects nested or executable protocol payloads in third_play_url", () => {
    expect(() => navigateChannel6({ channelid: 263, third_play_url: "javascript:alert(1)" })).toThrow(
      "Unsafe third_play_url",
    );
    expect(() => navigateChannel6({ channelid: 263, third_play_url: "qips://vtype=6;target=2;" })).toThrow(
      "Unsafe third_play_url",
    );
  });
});

describe("navigateChannel6", () => {
  it("电影频道（channel-table channelid=1）", () => {
    expect(navigateChannel6({ channelid: 1 })).toBe("qips://vtype=6;target=2;channelid=1;");
  });

  it("电视剧频道 channelid=2", () => {
    expect(navigateChannel6({ channelid: 2 })).toBe("qips://vtype=6;target=2;channelid=2;");
  });

  it("片库 tagName JSON（vtype-recipes §2）", () => {
    const json = thirdPlayUrlFromJson({ tagName: "免费" });
    expect(navigateChannel6({ channelid: 2, third_play_url: json })).toBe(
      "qips://vtype=6;target=2;channelid=2;third_play_url=%7B%22tagName%22%3A%22%E5%85%8D%E8%B4%B9%22%7D;",
    );
  });

  it("片库 tagName JSON 免费专区 302（channel-table FilmLib）", () => {
    const json = thirdPlayUrlFromJson({ tagName: "动漫" });
    expect(navigateChannel6({ channelid: 302, third_play_url: json })).toBe(
      "qips://vtype=6;target=2;channelid=302;third_play_url=%7B%22tagName%22%3A%22%E5%8A%A8%E6%BC%AB%22%7D;",
    );
  });

  it("搜索结果 channelid=115（vtype-recipes §3）", () => {
    expect(navigateChannel6({ channelid: 115, third_play_url: "海贼王" })).toBe(
      "qips://vtype=6;target=2;channelid=115;third_play_url=%E6%B5%B7%E8%B4%BC%E7%8E%8B;",
    );
  });

  it("搜索结果 Ai 搜 JSON（vtype-recipes §3）", () => {
    expect(
      navigateChannel6({
        channelid: 115,
        third_play_url: thirdPlayUrlFromJson({
          fromAiSuggest: true,
          query: "海贼王",
        }),
      }),
    ).toBe(
      "qips://vtype=6;target=2;channelid=115;third_play_url=%7B%22fromAiSuggest%22%3Atrue%2C%22query%22%3A%22%E6%B5%B7%E8%B4%BC%E7%8E%8B%22%7D;",
    );
  });

  it("个人中心 lishi（vtype-recipes §4）", () => {
    expect(
      navigateChannel6({
        channelid: 116,
        third_play_url: thirdPlayUrlFromJson({ tab_id: "lishi" }),
      }),
    ).toBe(
      "qips://vtype=6;target=2;channelid=116;third_play_url=%7B%22tab_id%22%3A%22lishi%22%7D;",
    );
  });

  it("播单 bodanId（vtype-recipes §5 H6 内形态）", () => {
    expect(
      navigateChannel6({
        channelid: 1011,
        third_play_url: thirdPlayUrlFromJson({ bodanId: 7569738292687702 }),
      }),
    ).toBe(
      "qips://vtype=6;target=2;channelid=1011;third_play_url=%7B%22bodanId%22%3A7569738292687702%7D;",
    );
  });

  it("作者 / 明星（vtype-recipes §6）", () => {
    expect(
      navigateChannel6({
        channelid: 1015,
        third_play_url: thirdPlayUrlFromJson({ userId: 1234567890 }),
      }),
    ).toBe(
      "qips://vtype=6;target=2;channelid=1015;third_play_url=%7B%22userId%22%3A1234567890%7D;",
    );
    expect(
      navigateChannel6({
        channelid: 1018,
        third_play_url: thirdPlayUrlFromJson({ starId: 987654321 }),
      }),
    ).toBe(
      "qips://vtype=6;target=2;channelid=1018;third_play_url=%7B%22starId%22%3A987654321%7D;",
    );
  });

  it("短视频 Tab（vtype-recipes §7）", () => {
    expect(
      navigateChannel6({
        channelid: 1012,
        third_play_url: thirdPlayUrlFromJson({ tab: "choice" }),
      }),
    ).toBe(
      "qips://vtype=6;target=2;channelid=1012;third_play_url=%7B%22tab%22%3A%22choice%22%7D;",
    );
  });

  it("内嵌 H5 channelid=263（vtype-recipes §8）", () => {
    expect(
      navigateChannel6({
        channelid: 263,
        third_play_url: "https://www.iqiyi.com/somePromoPage",
      }),
    ).toBe(
      "qips://vtype=6;target=2;channelid=263;third_play_url=https%3A%2F%2Fwww.iqiyi.com%2FsomePromoPage;",
    );
  });

  it("带 s2/s3/s4（vtype-recipes §9，占位换为固定字面量）", () => {
    expect(
      buildQips([
        { key: "vtype", value: 6 },
        { key: "target", value: 2 },
        { key: "channelid", value: 2 },
        { key: "s2", value: "rpage" },
        { key: "s3", value: "block" },
        { key: "s4", value: "rseat" },
      ]),
    ).toBe("qips://vtype=6;target=2;channelid=2;s2=rpage;s3=block;s4=rseat;");
  });
});

describe("navigateChannel7", () => {
  it("播单首选形态（vtype-recipes §vtype=7 播单）", () => {
    expect(
      navigateChannel7({
        channelId: 1011,
        query: { bodanId: 7569738292687702 },
      }),
    ).toBe(
      "qips://vtype=7;third_play_url=%3FbodanId%3D7569738292687702%23%2Fchannel%2F1011%2F;",
    );
  });
});

describe("playByTitle6", () => {
  it("SKILL 内联：庆余年 第 2 季", () => {
    expect(playByTitle6({ title: "庆余年", season: 2 })).toBe(
      "qips://vtype=6;action=play;title=%E5%BA%86%E4%BD%99%E5%B9%B4;season=2;",
    );
  });

  it("vtype-recipes：含 episode", () => {
    expect(playByTitle6({ title: "庆余年", season: 2, episode: 5 })).toBe(
      "qips://vtype=6;action=play;title=%E5%BA%86%E4%BD%99%E5%B9%B4;season=2;episode=5;",
    );
  });

  it("rejects empty titles before producing a launchable qips", () => {
    expect(() => playByTitle6({ title: "   " })).toThrow("title is required");
  });
});

describe("playbackControl6", () => {
  it("暂停 target=102（SKILL 内联）", () => {
    expect(playbackControl6({ target: 102 })).toBe("qips://vtype=6;target=102;");
  });

  it("下一集 / 快进（vtype-recipes 播控）", () => {
    expect(playbackControl6({ target: 104 })).toBe("qips://vtype=6;target=104;");
    expect(playbackControl6({ target: 105 })).toBe("qips://vtype=6;target=105;");
  });

  it("rejects playback targets outside the documented safe range", () => {
    expect(() => playbackControl6({ target: 110 })).toThrow("Unsupported playback target");
  });
});

describe("vodPlay0", () => {
  it("最短形（vtype-recipes §vtype=0）", () => {
    expect(vodPlay0({ tvid: "1234567890123" })).toBe("qips://vtype=0;tvid=1234567890123;");
  });

  it("带完整字段（占位 s2/s3/s4 换为字面量）", () => {
    expect(
      vodPlay0({
        tvid: "1234567890123",
        albumid: "98765432101",
        start_pos: 120,
        playrecord: true,
        ischarge: false,
        s2: "rpage",
        s3: "block",
        s4: "rseat",
      }),
    ).toBe(
      "qips://vtype=0;tvid=1234567890123;albumid=98765432101;start_pos=120;playrecord=true;ischarge=false;s2=rpage;s3=block;s4=rseat;",
    );
  });
});

describe("vtype=2 第三方（vtype-recipes 整段 golden）", () => {
  it("matches documented example order", () => {
    const qips = buildQips([
      { key: "vtype", value: 2 },
      { key: "thirdid", value: "1606437380862314" },
      {
        key: "third_play_url",
        value: "https://v.youku.com/v_show/id_XNTkzMTgyNzI5Ng==.html",
      },
      { key: "third_name", value: "护心" },
      { key: "third_docid", value: "b37ef222e4fe0062bf81ba2749ab3fbc" },
      { key: "ischarge", value: false },
      { key: "tvsubname", value: "护心01" },
    ]);
    expect(qips).toBe(
      "qips://vtype=2;thirdid=1606437380862314;third_play_url=https%3A%2F%2Fv.youku.com%2Fv_show%2Fid_XNTkzMTgyNzI5Ng%3D%3D.html;third_name=%E6%8A%A4%E5%BF%83;third_docid=b37ef222e4fe0062bf81ba2749ab3fbc;ischarge=false;tvsubname=%E6%8A%A4%E5%BF%8301;",
    );
  });
});
