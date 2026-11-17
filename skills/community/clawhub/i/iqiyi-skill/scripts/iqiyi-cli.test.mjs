import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { buildCliRequest, parseIqiyiCliArgs } from "./iqiyi-cli.mjs";

describe("iqiyi-cli", () => {
  it("maps video search syntax to the search operation", () => {
    const parsed = parseIqiyiCliArgs(["video", "search", "--q", "周星驰", "--pageNum", "2", "--dry-run"]);

    expect(parsed).toEqual({
      operationId: "video.search",
      input: {
        q: "周星驰",
        pageNum: 2,
      },
      options: {
        dryRun: true,
        output: "json",
      },
    });
  });

  it("maps star search syntax to the star operation", () => {
    expect(buildCliRequest(["star", "search", "--q", "刘德华", "--dry-run"])).toMatchObject({
      endpoint: "/star/search",
      body: {
        q: "刘德华",
      },
    });
  });

  it("normalizes video recommend styles through CLI syntax", () => {
    const request = buildCliRequest([
      "video",
      "recommend",
      "--type",
      "电影",
      "--style",
      "适合全家一起看的电影",
      "--kind",
      "suggest",
      "--dry-run",
    ]);

    expect(request.body).toEqual({
      type: "Movie",
      style: ["家庭"],
      kind: "suggest",
    });
    expect(request.warnings).toContain("style=适合全家一起看的电影 normalized to 家庭");
  });

  it("maps video play syntax to local qips without building a backend request", () => {
    expect(
      buildCliRequest(["video", "play", "--title", "test-title", "--season", "2", "--episode", "5", "--dry-run"]),
    ).toMatchObject({
      kind: "qips",
      operationId: "video.play",
      qips: "qips://vtype=6;action=play;title=test-title;season=2;episode=5;",
      input: {
        title: "test-title",
        season: 2,
        episode: 5,
      },
      network: false,
    });
  });

  it("prints dry-run request JSON from the CLI executable", () => {
    const output = execFileSync(
      "node",
      [
        ".cursor/skills/iqiyi-skill/scripts/iqiyi-cli.mjs",
        "video",
        "recommend",
        "--type",
        "电影",
        "--style",
        "适合全家一起看的电影",
        "--kind",
        "suggest",
        "--dry-run",
      ],
      { encoding: "utf8" },
    );
    const parsed = JSON.parse(output);

    expect(parsed.endpoint).toBe("/video/recommend");
    expect(parsed.body.style).toEqual(["家庭"]);
  });

  it("declares a package-style bin entry for iqiyi-cli distribution", () => {
    const packageJson = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8"));

    expect(packageJson).toMatchObject({
      name: "iqiyi-skill",
      type: "module",
      bin: {
        "iqiyi-cli": "./scripts/iqiyi-cli.mjs",
      },
    });
    expect(packageJson.files).toEqual(expect.arrayContaining(["SKILL.md", "agents", "docs", "references", "scripts"]));
  });
});
