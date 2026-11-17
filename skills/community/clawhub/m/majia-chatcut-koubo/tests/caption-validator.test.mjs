import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const validator = path.join(root, "scripts/validate-caption-pages.mjs");

function baseProfile(overrides = {}) {
  return {
    schemaVersion: "2.0.0",
    policyVersion: "1.2.0",
    profileId: "caption-test-profile",
    profileVersion: "1.0.0",
    status: "validated",
    provenance: {
      projectId: "project-1",
      validatedTimelineIds: ["timeline-1"],
      validatedTimelineRevisions: {"timeline-1": "timeline-revision-1"},
      validatedSourceRevisions: {"source-asset-1": "source-revision-1"},
    },
    timeline: {width: 1080, height: 1920, fps: 30},
    captions: {
      sourceVariant: "original",
      maxCharactersPerLine: 22,
      displayOverridePolicy: {maxReplacementCharacters: 4},
    },
    presenterWindow: {},
    audio: {},
    terminologyFile: "terminology.json",
    ...overrides,
  };
}

function baseTerminology() {
  return {
    version: "2.0.0",
    maintainer: "test-fixture",
    entries: [
      {termId: "term-store-count", correct: "500 家门店", wrong: ["50 家门店"], matchMode: "substring"},
      {termId: "term-data-analyst", correct: "数据分析师", wrong: ["数据分析"], matchMode: "substring"},
    ],
    shortCardWhitelist: {approved: ["AI", "BI"]},
  };
}

function page({
  text = "这是完整字幕",
  startFrame = 0,
  endFrame = 30,
  lines = 1,
  index = 1,
  words,
  shortCardEvidence,
  declaredWordCount,
} = {}) {
  return {
    index,
    startFrame,
    endFrame,
    text,
    lines,
    ...(declaredWordCount === undefined ? {} : {declaredWordCount}),
    ...(shortCardEvidence ? {shortCardEvidence} : {}),
    words: words ?? [{
      key: `w-${index}`,
      sourceAssetId: "source-asset-1",
      sourceRevision: "source-revision-1",
      sourceWordKey: `source-w-${index}`,
      sourceText: text,
      text,
      startFrame,
      endFrame,
    }],
  };
}

function sourceBoundWord({
  key = "w-bound",
  sourceWordKey = "source-w-bound",
  sourceText,
  text,
  startFrame = 0,
  endFrame = 30,
  correction,
} = {}) {
  return {
    key,
    sourceAssetId: "source-asset-1",
    sourceRevision: "source-revision-1",
    sourceWordKey,
    sourceText: sourceText ?? text,
    text,
    startFrame,
    endFrame,
    ...(correction ? {correction} : {}),
  };
}

function approvedCorrection(overrides = {}) {
  return {
    approved: true,
    reason: "reviewed against source evidence",
    evidenceRefs: ["transcript:segment-1"],
    reviewedBy: "reviewer-1",
    reviewedAt: "2026-07-24T10:00:00Z",
    ...overrides,
  };
}

function captionDocument(pages, metadata = {}) {
  return {
    "$schema": "https://github.com/maojiebc/majia-chatcut-koubo/schemas/captions.schema.json",
    schemaVersion: "1.0.0",
    metadata: {
      sourceVariant: "original",
      timelineFps: 30,
      automaticWrapAllowed: true,
      pagination: {maxLines: 2, maxCharactersPerLine: 22},
      projectId: "project-1",
      timelineId: "timeline-1",
      timelineRevision: "timeline-revision-1",
      sourceAssetId: "source-asset-1",
      sourceRevision: "source-revision-1",
      ...metadata,
    },
    pages,
  };
}

function run({
  profile = baseProfile(),
  profileText,
  parentProfile,
  terminology = baseTerminology(),
  terminologyText,
  localTerms,
  termsArgument,
  input,
  strict = false,
  extraArgs = [],
}) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "caption-validator-"));
  const profilePath = path.join(directory, "profile.json");
  const terminologyPath = path.join(directory, "terminology.json");
  const inputPath = path.join(directory, typeof input === "string" ? "captions.txt" : "captions.json");
  fs.writeFileSync(profilePath, profileText ?? JSON.stringify(profile));
  if (parentProfile) fs.writeFileSync(path.join(directory, "parent.json"), JSON.stringify(parentProfile));
  fs.writeFileSync(terminologyPath, terminologyText ?? JSON.stringify(terminology));
  fs.writeFileSync(inputPath, typeof input === "string" ? input : JSON.stringify(input));
  const args = [validator, "--profile", profilePath, "--input", inputPath];
  if (termsArgument) {
    args.push("--terms", termsArgument);
  } else if (localTerms) {
    const localTermsPath = path.join(directory, "local-terms.json");
    fs.writeFileSync(localTermsPath, JSON.stringify(localTerms));
    args.push("--terms", localTermsPath);
  }
  if (strict) args.push("--strict");
  args.push(...extraArgs);
  const result = spawnSync(process.execPath, args, {encoding: "utf8"});
  fs.rmSync(directory, {recursive: true, force: true});
  return {...result, output: `${result.stdout}${result.stderr}`};
}

test("accepts a matching legacy declared word count and rejects a mismatch", () => {
  const matching = run({
    input: captionDocument([page({declaredWordCount: 1})]),
  });
  assert.equal(matching.status, 0, matching.output);

  const mismatching = run({
    input: captionDocument([page({declaredWordCount: 2})]),
  });
  assert.equal(mismatching.status, 1, mismatching.output);
  assert.match(mismatching.output, /declares 2 words but parsed 1/);
});

test("resolves profile inheritance before applying release gates", () => {
  const profile = {
    extends: "parent.json",
    status: "validated",
    provenance: {projectId: "project-1", validatedTimelineIds: ["timeline-1"]},
  };
  const result = run({profile, parentProfile: baseProfile(), input: captionDocument([page()])});
  assert.equal(result.status, 0, result.output);
});

test("missing leaf-owned provenance is migration-only and strict blocks it", () => {
  const profile = {extends: "parent.json", status: "validated"};
  const input = captionDocument([page()]);
  for (const field of [
    "projectId",
    "timelineId",
    "timelineRevision",
    "sourceAssetId",
    "sourceRevision",
  ]) {
    delete input.metadata[field];
  }
  for (const word of input.pages.flatMap((page_) => page_.words)) {
    delete word.sourceAssetId;
    delete word.sourceRevision;
    delete word.sourceWordKey;
  }
  const normal = run({
    profile,
    parentProfile: baseProfile(),
    input,
  });
  const strict = run({
    profile,
    parentProfile: baseProfile(),
    input,
    strict: true,
  });
  assert.equal(normal.status, 0, normal.output);
  assert.match(normal.output, /PROFILE_MIGRATION_LEAF_PROVENANCE_MISSING/);
  assert.equal(strict.status, 1, strict.output);
  assert.match(strict.output, /strict warning mode/);
});

test("caption CLI rejects unsafe profile keys before merge", () => {
  const profileText = JSON.stringify(baseProfile()).replace(
    '"captions":{',
    '"captions":{"__proto__":{"polluted":true},',
  );
  const result = run({profileText, input: captionDocument([page()])});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /PROFILE_UNSAFE_KEY/);
});

test("loads an inherited terminologyFile within an explicitly authorized profile root", () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "caption-validator-path-"));
  const parentDirectory = path.join(directory, "shared", "profile");
  const termsDirectory = path.join(directory, "shared", "terms");
  const childDirectory = path.join(directory, "projects", "demo");
  fs.mkdirSync(parentDirectory, {recursive: true});
  fs.mkdirSync(termsDirectory, {recursive: true});
  fs.mkdirSync(childDirectory, {recursive: true});

  const parentPath = path.join(parentDirectory, "base.json");
  const childPath = path.join(childDirectory, "profile.json");
  const termsPath = path.join(termsDirectory, "parent-terms.json");
  const inputPath = path.join(childDirectory, "captions.json");
  fs.writeFileSync(parentPath, JSON.stringify(baseProfile({
    terminologyFile: "../terms/parent-terms.json",
  })));
  fs.writeFileSync(childPath, JSON.stringify({
    extends: "../../shared/profile/base.json",
    status: "validated",
    provenance: {projectId: "project-1", validatedTimelineIds: ["timeline-1"]},
  }));
  fs.writeFileSync(termsPath, JSON.stringify({
    version: "1.0.0",
    maintainer: "test-fixture",
    entries: [{termId: "term-parent", correct: "父层正确词", wrong: ["父层错词"], matchMode: "substring"}],
    shortCardWhitelist: {approved: ["AI"]},
  }));
  fs.writeFileSync(inputPath, JSON.stringify(captionDocument([page({text: "这里有父层错词"})])));

  const unscoped = spawnSync(process.execPath, [
    validator,
    "--profile",
    childPath,
    "--input",
    inputPath,
  ], {encoding: "utf8"});
  const unscopedOutput = `${unscoped.stdout}${unscoped.stderr}`;
  assert.equal(unscoped.status, 1, unscopedOutput);
  assert.match(unscopedOutput, /PROFILE_EXTENDS_OUTSIDE_ROOT/);
  assert.equal(unscopedOutput.includes(directory), false, unscopedOutput);

  const result = spawnSync(process.execPath, [
    validator,
    "--profile",
    childPath,
    "--root",
    directory,
    "--input",
    inputPath,
  ], {encoding: "utf8"});
  fs.rmSync(directory, {recursive: true, force: true});
  const output = `${result.stdout}${result.stderr}`;
  assert.equal(result.status, 1, output);
  assert.match(output, /terminology entry 0: forbidden form detected/);
});

test("terminology load failures do not disclose absolute paths", async (t) => {
  await t.test("profile-local paths are relative", () => {
    const profile = baseProfile({terminologyFile: "private/missing.json"});
    const result = run({profile, input: captionDocument([page()])});
    assert.equal(result.status, 2, result.output);
    assert.match(result.output, /TERMINOLOGY_READ_FAILED/);
    assert.equal(result.output.includes(os.tmpdir()), false, result.output);
  });

  await t.test("external --terms paths use a placeholder", () => {
    const externalDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "private-terms-"));
    const externalTerms = path.join(externalDirectory, "home-like", "missing.json");
    const result = run({termsArgument: externalTerms, input: captionDocument([page()])});
    fs.rmSync(externalDirectory, {recursive: true, force: true});
    assert.equal(result.status, 2, result.output);
    assert.match(result.output, /TERMINOLOGY_READ_FAILED/);
    assert.equal(result.output.includes(externalDirectory), false, result.output);
  });
});

test("caption CLI rejects unknown, duplicate, and valueless options with exit 2", async (t) => {
  const cases = [
    ["misspelled option", ["--strcit"]],
    ["equals-form boolean", ["--strict=true"]],
    ["duplicate value option", ["--profile", "duplicate.json"]],
    ["duplicate strict alias", ["--strict", "--strict-warnings"]],
    ["missing option value", ["--terms"]],
  ];
  for (const [name, extraArgs] of cases) {
    await t.test(name, () => {
      const result = run({input: captionDocument([page()]), extraArgs});
      assert.equal(result.status, 2, result.output);
      assert.match(result.output, /invalid arguments|Usage:/);
    });
  }
});

test("accepts a valid structured caption document", () => {
  const result = run({input: captionDocument([page()])});
  assert.equal(result.status, 0, result.output);
});

test("old policyVersion warns in migration mode and blocks strict release", () => {
  const profile = baseProfile({policyVersion: "1.0.0"});
  const normal = run({profile, input: captionDocument([page()])});
  const strict = run({profile, input: captionDocument([page()]), strict: true});
  assert.equal(normal.status, 0, normal.output);
  assert.match(normal.output, /profile policyVersion=1\.0\.0; expected 1\.2\.0/);
  assert.equal(strict.status, 1, strict.output);
  assert.match(strict.output, /strict warning mode/);
});

test("loads terminologyFile and rejects known wrong forms", () => {
  const result = run({input: captionDocument([page({text: "共有 50 家门店"})])});
  assert.equal(result.status, 1);
  assert.match(result.output, /terminology entry 0: forbidden form detected/);
});

test("malformed terminology entries fail closed instead of skipping wrong forms", () => {
  const terminology = {
    ...baseTerminology(),
    entries: [{termId: "term-malformed", correct: "正确品牌", wrong: "错误品牌", matchMode: "substring"}],
  };
  const result = run({
    terminology,
    input: captionDocument([page({text: "这里写了错误品牌"})]),
  });
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /terminology schema type@\/entries\/0\/wrong/);
});

test("old terminology without termId warns normally and blocks strict release", () => {
  const terminology = baseTerminology();
  for (const entry of terminology.entries) delete entry.termId;
  const input = captionDocument([page()]);
  const normal = run({terminology, input});
  const strict = run({terminology, input, strict: true});
  assert.equal(normal.status, 0, normal.output);
  assert.match(normal.output, /terminology is missing stable termId/);
  assert.equal(strict.status, 1, strict.output);
  assert.match(strict.output, /strict warning mode/);
});

test("new-format terminology is schema-validated before use", () => {
  const terminology = baseTerminology();
  terminology.entries[0].risk = "private-risk-typo";
  const result = run({terminology, input: captionDocument([page()])});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /terminology schema enum@\/entries\/0\/risk/);
  assert.equal(result.output.includes("private-risk-typo"), false, result.output);
});

test("does not report a wrong substring inside its correct term", () => {
  const result = run({input: captionDocument([page({text: "我是数据分析师"})])});
  assert.equal(result.status, 0, result.output);
});

test("detects a wrong term that contains or overlaps the correct term", async (t) => {
  const cases = [
    ["superstring", "OpenAI", "OpenAIi"],
    ["partial overlap", "abc", "bcd"],
  ];
  for (const [name, correct, wrong] of cases) {
    await t.test(name, () => {
      const terminology = {
        version: "2.0.0",
        maintainer: "test-fixture",
        entries: [{
          termId: `term-${name.replaceAll(" ", "-")}`,
          correct,
          wrong: [wrong],
          matchMode: "substring",
        }],
        shortCardWhitelist: {approved: ["AI"]},
      };
      const text = name === "superstring" ? wrong : `a${wrong}`;
      const result = run({
        terminology,
        input: captionDocument([page({text})]),
      });
      assert.equal(result.status, 1, result.output);
      assert.match(
        result.output,
        /terminology entry 0: forbidden form detected/,
      );
    });
  }
});

test("two-line ceiling cannot be weakened by profile data", () => {
  const profile = baseProfile({hardInvariants: {maxLines: 3}});
  const result = run({profile, input: captionDocument([page({lines: 3})], {pagination: {maxLines: 3, maxCharactersPerLine: 22}})});
  assert.equal(result.status, 1);
  assert.match(result.output, /caption schema const@\/metadata\/pagination\/maxLines/);
});

test("semantic events may use two lines without weakening the per-line budget", async (t) => {
  await t.test("accepts a complete two-line event within 2x budget", () => {
    const text = "这是一个保持完整语义并在画面中自然排成两行的字幕事件";
    const result = run({input: captionDocument([page({text, lines: 2, endFrame: 90})])});
    assert.equal(result.status, 0, result.output);
  });

  await t.test("one-line pages still use the one-line budget", () => {
    const text = "这是一条超过单行字符预算但错误声明为单行的字幕事件";
    const result = run({input: captionDocument([page({text, lines: 1, endFrame: 90})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /chars > 22 \(1 line\(s\) × 22\)/);
  });

  await t.test("two-line pages cannot exceed the two-line budget", () => {
    const text = "字".repeat(45);
    const result = run({input: captionDocument([page({text, lines: 2, endFrame: 120})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /45 chars > 44 \(2 line\(s\) × 22\)/);
  });
});

test("structured captions reject real line breaks but allow semantic slashes", async (t) => {
  for (const text of ["A / B", "速度 10 m/s"]) {
    await t.test(`allows ${text}`, () => {
      const result = run({input: captionDocument([page({text})])});
      assert.equal(result.status, 0, result.output);
    });
  }

  for (const lineBreak of ["\n", "\r", "\r\n"]) {
    await t.test(`rejects ${JSON.stringify(lineBreak)}`, () => {
      const text = `第一行${lineBreak}第二行`;
      const result = run({input: captionDocument([page({text, lines: 1})])});
      assert.equal(result.status, 1, result.output);
      assert.match(result.output, /caption schema pattern@\/pages\/0\/text/);
    });
  }

  await t.test("rejects a line break hidden in word text", () => {
    const words = [{
      key: "w-line-break",
      sourceText: "第一行第二行",
      text: "第一行\n第二行",
      startFrame: 0,
      endFrame: 30,
    }];
    const result = run({input: captionDocument([page({text: "第一行第二行", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /caption schema pattern@\/pages\/0\/words\/0\/text/);
  });
});

test("runtime rejects primitive coercion that the caption schema forbids", async (t) => {
  const cases = [
    ["string page index", page({index: "1"}), /caption schema type@\/pages\/0\/index/],
    ["string line count", page({lines: "1"}), /caption schema type@\/pages\/0\/lines/],
    [
      "numeric page text",
      page({
        text: 123,
        words: [{key: "w-page-type", sourceText: "123", text: "123", startFrame: 0, endFrame: 30}],
      }),
      /caption schema type@\/pages\/0\/text/,
    ],
    [
      "numeric word text",
      page({
        text: "123",
        words: [{key: "w-word-type", sourceText: "123", text: 123, startFrame: 0, endFrame: 30}],
      }),
      /caption schema type@\/pages\/0\/words\/0\/text/,
    ],
  ];

  for (const [name, invalidPage, expected] of cases) {
    await t.test(name, () => {
      const result = run({input: captionDocument([invalidPage])});
      assert.equal(result.status, 1, result.output);
      assert.match(result.output, expected);
    });
  }
});

test("structured caption schema fails fast without dereferencing invalid nodes", async (t) => {
  const cases = [
    ["null page", captionDocument([null]), /caption schema type@\/pages\/0/],
    [
      "null word",
      captionDocument([page({words: [null]})]),
      /caption schema type@\/pages\/0\/words\/0/,
    ],
  ];
  for (const [name, input, expected] of cases) {
    await t.test(name, () => {
      const result = run({input});
      assert.equal(result.status, 1, result.output);
      assert.match(result.output, expected);
      assert.doesNotMatch(result.output, /TypeError|validate-caption-pages\.mjs:\d+/);
    });
  }
});

test("caption schema rejects additional properties without echoing their values", () => {
  const input = captionDocument([page()]);
  input.privateCaptionPayload = "DO_NOT_ECHO_CAPTION_VALUE";
  const result = run({input});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /caption schema additionalProperties@\//);
  assert.equal(result.output.includes("DO_NOT_ECHO_CAPTION_VALUE"), false, result.output);
});

test("caption CLI uses stable privacy-safe exits for profile and input I/O", async (t) => {
  await t.test("missing profile is operational exit 2", () => {
    const secretPath = path.join(os.tmpdir(), "private-profile-path", "missing.json");
    const result = spawnSync(process.execPath, [
      validator,
      "--profile",
      secretPath,
      "--input",
      path.join(os.tmpdir(), "private-input-path", "captions.json"),
    ], {encoding: "utf8"});
    const output = `${result.stdout}${result.stderr}`;
    assert.equal(result.status, 2, output);
    assert.match(output, /PROFILE_READ_ERROR/);
    assert.equal(output.includes(secretPath), false, output);
  });

  await t.test("invalid profile JSON is content exit 1", () => {
    const result = run({
      profileText: '{"privateProfile":"DO_NOT_ECHO_PROFILE"',
      input: captionDocument([page()]),
    });
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /PROFILE_PARSE_ERROR/);
    assert.equal(result.output.includes("DO_NOT_ECHO_PROFILE"), false, result.output);
  });

  await t.test("invalid caption JSON is content exit 1", () => {
    const result = run({
      input: '{"privateCaption":"DO_NOT_ECHO_CAPTION"',
    });
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /INVALID_JSON/);
    assert.equal(result.output.includes("DO_NOT_ECHO_CAPTION"), false, result.output);
    assert.equal(result.output.includes(os.tmpdir()), false, result.output);
  });

  await t.test("invalid terminology JSON is content exit 1", () => {
    const result = run({
      terminologyText: '{"privateTerm":"DO_NOT_ECHO_TERM"',
      input: captionDocument([page()]),
    });
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /TERMINOLOGY_INVALID_JSON/);
    assert.equal(result.output.includes("DO_NOT_ECHO_TERM"), false, result.output);
    assert.equal(result.output.includes(os.tmpdir()), false, result.output);
  });
});

test("short-card whitelist uses exact normalized terms", () => {
  const training = run({input: captionDocument([page({text: "TRAINING", endFrame: 15})])});
  const ai = run({input: captionDocument([page({text: "AI", endFrame: 15})])});
  assert.equal(training.status, 1);
  assert.match(training.output, /not terminology-approved/);
  assert.equal(ai.status, 0, ai.output);
});

test("rejects traditional Chinese characters", () => {
  const result = run({input: captionDocument([page({text: "資料分析"})])});
  assert.equal(result.status, 1);
  assert.match(result.output, /traditional Chinese/);
});

test("requires word-level evidence for every page", () => {
  const result = run({input: captionDocument([page({words: []})])});
  assert.equal(result.status, 1);
  assert.match(result.output, /caption schema minItems@\/pages\/0\/words/);
});

test("uses milliseconds so 30fps and 60fps decisions are equivalent", () => {
  const at30 = run({input: captionDocument([page({text: "AI", endFrame: 15})])});
  const profile60 = baseProfile({timeline: {width: 1080, height: 1920, fps: 60}});
  const page60 = page({text: "AI", endFrame: 30, words: [{key: "w", text: "AI", startFrame: 0, endFrame: 30}]});
  const at60 = run({profile: profile60, input: captionDocument([page60], {timelineFps: 60})});
  assert.equal(at30.status, 0, at30.output);
  assert.equal(at60.status, 0, at60.output);
});

test("rejects a caption frame domain that disagrees with the profile", () => {
  const result = run({input: captionDocument([page()], {timelineFps: 60})});
  assert.equal(result.status, 1);
  assert.match(result.output, /caption timelineFps=60; profile timeline fps=30/);
});

test("missing structured caption provenance warns normally and fails under --strict", () => {
  const input = captionDocument([page()]);
  delete input.metadata.projectId;
  delete input.metadata.timelineId;
  delete input.metadata.timelineRevision;
  delete input.metadata.sourceAssetId;
  delete input.metadata.sourceRevision;
  for (const word of input.pages.flatMap((currentPage) => currentPage.words)) {
    delete word.sourceAssetId;
    delete word.sourceRevision;
    delete word.sourceWordKey;
  }

  const normal = run({input});
  const strict = run({input, strict: true});
  assert.equal(normal.status, 0, normal.output);
  assert.match(normal.output, /caption provenance metadata is missing/);
  assert.equal(strict.status, 1, strict.output);
  assert.match(strict.output, /strict warning mode/);
});

test("structured JSON cannot claim the legacy schemaVersion to bypass provenance", () => {
  const input = captionDocument([page()]);
  input.schemaVersion = "legacy-read-captions";
  delete input.metadata.projectId;
  delete input.metadata.timelineId;
  delete input.metadata.timelineRevision;
  delete input.metadata.sourceAssetId;
  delete input.metadata.sourceRevision;
  const result = run({input, strict: true});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /caption schema const@\/schemaVersion/);
});

test("caption provenance projectId must match the resolved profile", () => {
  const input = captionDocument([page()], {projectId: "another-project"});
  const result = run({input});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /PROVENANCE_PROJECT_MISMATCH/);
});

test("caption provenance timelineId must be validated by the resolved profile", () => {
  const input = captionDocument([page()], {timelineId: "unvalidated-timeline"});
  const result = run({input});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /PROVENANCE_TIMELINE_UNVALIDATED/);
});

test("caption provenance revisions must exactly match profile evidence", async (t) => {
  await t.test("timeline revision mismatch", () => {
    const input = captionDocument([page()], {timelineRevision: "stale-timeline-revision"});
    const result = run({input});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /PROVENANCE_TIMELINE_REVISION_MISMATCH/);
  });

  await t.test("source revision mismatch", () => {
    const input = captionDocument([page()], {sourceRevision: "stale-source-revision"});
    const result = run({input});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /PROVENANCE_SOURCE_REVISION_MISMATCH/);
  });
});

test("caption sourceAssetId must be present in profile validatedSourceRevisions", () => {
  const input = captionDocument([page()], {sourceAssetId: "unvalidated-source-asset"});
  const result = run({input});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /PROVENANCE_SOURCE_UNVALIDATED/);
  assert.equal(result.output.includes("unvalidated-source-asset"), false, result.output);
});

test("missing profile revision evidence warns in migration mode and blocks strict release", () => {
  const profile = baseProfile({
    provenance: {
      projectId: "project-1",
      validatedTimelineIds: ["timeline-1"],
    },
  });
  const input = captionDocument([page()]);
  const normal = run({profile, input});
  const strict = run({profile, input, strict: true});
  assert.equal(normal.status, 0, normal.output);
  assert.match(normal.output, /PROVENANCE_TIMELINE_REVISION_MISSING/);
  assert.match(normal.output, /PROVENANCE_SOURCE_REVISION_MISSING/);
  assert.equal(strict.status, 1, strict.output);
  assert.match(strict.output, /strict warning mode/);
});

test("migration-only revision maps never bypass project provenance matching", () => {
  const profile = baseProfile({
    provenance: {
      projectId: "project-1",
      validatedTimelineIds: ["timeline-1"],
    },
  });
  const input = captionDocument([page()], {projectId: "another-project"});
  const result = run({profile, input});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /PROVENANCE_PROJECT_MISMATCH/);
  assert.match(result.output, /PROVENANCE_TIMELINE_REVISION_MISSING/);
  assert.match(result.output, /PROVENANCE_SOURCE_REVISION_MISSING/);
});

test("word source binding is migration-compatible but strict and exact", async (t) => {
  await t.test("all binding fields missing warns normally and blocks strict", () => {
    const words = [{key: "legacy-word", sourceText: "旧词", text: "旧词", startFrame: 0, endFrame: 30}];
    const input = captionDocument([page({text: "旧词", words})]);
    const normal = run({input});
    const strict = run({input, strict: true});
    assert.equal(normal.status, 0, normal.output);
    assert.match(normal.output, /word evidence is missing source binding/);
    assert.equal(strict.status, 1, strict.output);
    assert.match(strict.output, /strict warning mode/);
  });

  await t.test("partial binding fails schema", () => {
    const words = [{
      key: "partial-word",
      sourceAssetId: "source-asset-1",
      sourceText: "词",
      text: "词",
      startFrame: 0,
      endFrame: 30,
    }];
    const result = run({input: captionDocument([page({text: "词语", words: [
      {...words[0], sourceText: "词语", text: "词语"},
    ]})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /caption schema dependentRequired@\/pages\/0\/words\/0/);
  });

  await t.test("asset and revision must match metadata", () => {
    const words = [sourceBoundWord({
      text: "绑定词",
      sourceWordKey: "source-binding-mismatch",
    })];
    words[0].sourceRevision = "another-source-revision";
    const result = run({input: captionDocument([page({text: "绑定词", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /WORD_SOURCE_REVISION_MISMATCH/);
    assert.equal(result.output.includes("another-source-revision"), false, result.output);
  });

  await t.test("sourceWordKey is document-global unique", () => {
    const words = [
      sourceBoundWord({
        key: "display-word-1",
        sourceWordKey: "private-source-word",
        text: "甲",
        startFrame: 0,
        endFrame: 15,
      }),
      sourceBoundWord({
        key: "display-word-2",
        sourceWordKey: "private-source-word",
        text: "乙",
        startFrame: 15,
        endFrame: 30,
      }),
    ];
    const result = run({input: captionDocument([page({text: "甲乙", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /duplicate sourceWordKey#[a-f0-9]{10}/);
    assert.equal(result.output.includes("private-source-word"), false, result.output);
  });
});

test("caption provenance is all-or-none and every field is non-empty", async (t) => {
  await t.test("partial binding", () => {
    const input = captionDocument([page()]);
    delete input.metadata.sourceRevision;
    const result = run({input});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /caption schema dependentRequired@\/metadata/);
  });

  await t.test("empty revision", () => {
    const input = captionDocument([page()], {timelineRevision: "  "});
    const result = run({input});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /caption schema pattern@\/metadata\/timelineRevision/);
  });
});

test("a fully bound caption provenance passes in strict mode", () => {
  const result = run({input: captionDocument([page()]), strict: true});
  assert.equal(result.status, 0, result.output);
});

test("viewer text must agree with word-level evidence", () => {
  const result = run({input: captionDocument([page({text: "真实字幕", words: [{key: "w", text: "另一句话", startFrame: 0, endFrame: 30}]})])});
  assert.equal(result.status, 1);
  assert.match(result.output, /does not match its word evidence/);
});

test("viewer text preserves high-risk numeric semantics", async (t) => {
  const cases = [
    ["decimal point", "增长 3.14%", "增长 314%"],
    ["negative sign", "下降 -50 元", "下降 50 元"],
    ["percent sign", "增长 10%", "增长 10"],
    ["date separators", "日期 2026-07-24", "日期 20260724"],
    ["unit separator", "速度 10 m/s", "速度 10 ms"],
    ["unit case", "容量 10 MB", "容量 10 Mb"],
  ];

  for (const [name, text, evidence] of cases) {
    await t.test(name, () => {
      const words = [{key: `w-${name}`, text: evidence, startFrame: 0, endFrame: 30}];
      const result = run({input: captionDocument([page({text, words})])});
      assert.equal(result.status, 1, result.output);
      assert.match(result.output, /numeric semantics|does not match its word evidence/);
    });
  }
});

test("non-semantic sentence punctuation may differ from word evidence", () => {
  const words = [{key: "w-punctuation", text: "今天很好", startFrame: 0, endFrame: 30}];
  const result = run({input: captionDocument([page({text: "今天很好。", words})])});
  assert.equal(result.status, 0, result.output);
});

test("numeric semantics survive NFKC normalization and word boundaries", () => {
  const words = [
    {key: "w-prefix", text: "增长", startFrame: 0, endFrame: 10},
    {key: "w-number", text: "3.14", startFrame: 10, endFrame: 20},
    {key: "w-percent", text: "%", startFrame: 20, endFrame: 30},
  ];
  const result = run({input: captionDocument([page({text: "增长３．１４％", words})])});
  assert.equal(result.status, 0, result.output);
});

test("word keys are unique across the whole caption document", () => {
  const pages = [
    page({index: 1, text: "第一句", startFrame: 0, endFrame: 30, words: [{key: "shared-key", text: "第一句", startFrame: 0, endFrame: 30}]}),
    page({index: 2, text: "第二句", startFrame: 30, endFrame: 60, words: [{key: "shared-key", text: "第二句", startFrame: 30, endFrame: 60}]}),
  ];
  const result = run({input: captionDocument(pages)});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /duplicate wordKey#[a-f0-9]{10}/);
});

test("page and word frame intervals require non-negative safe integers", async (t) => {
  await t.test("fractional word frames", () => {
    const words = [{key: "w-half", text: "半帧不合法", startFrame: 0.5, endFrame: 20.5}];
    const result = run({input: captionDocument([page({text: "半帧不合法", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /caption schema type@\/pages\/0\/words\/0\/startFrame/);
  });

  await t.test("fractional page frames", () => {
    const words = [{key: "w-page-half", text: "页面半帧", startFrame: 0.5, endFrame: 30.5}];
    const result = run({input: captionDocument([page({text: "页面半帧", startFrame: 0.5, endFrame: 30.5, words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /caption schema type@\/pages\/0\/startFrame/);
  });

  await t.test("negative word frames", () => {
    const words = [{key: "w-negative", text: "负帧不合法", startFrame: -1, endFrame: 20}];
    const result = run({input: captionDocument([page({text: "负帧不合法", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /caption schema minimum@\/pages\/0\/words\/0\/startFrame/);
  });
});

test("words are monotonic and non-overlapping within each page", async (t) => {
  await t.test("out of order", () => {
    const words = [
      {key: "w-late", text: "甲", startFrame: 15, endFrame: 30},
      {key: "w-early", text: "乙", startFrame: 0, endFrame: 15},
    ];
    const result = run({input: captionDocument([page({text: "甲乙", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /words are not sorted by start frame/);
  });

  await t.test("overlap", () => {
    const words = [
      {key: "w-first", text: "甲", startFrame: 0, endFrame: 20},
      {key: "w-second", text: "乙", startFrame: 15, endFrame: 30},
    ];
    const result = run({input: captionDocument([page({text: "甲乙", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /W2: overlaps W1/);
  });
});

test("Chinese short cards cannot be approved by profile or terminology", async (t) => {
  await t.test("terminology whitelist", () => {
    const terminology = baseTerminology();
    terminology.shortCardWhitelist.approved.push("中文");
    const result = run({terminology, input: captionDocument([page({text: "中文", endFrame: 15})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /terminology schema pattern@\/shortCardWhitelist\/approved\/\d+/);
  });

  await t.test("profile whitelist", () => {
    const profile = baseProfile();
    profile.captions.shortCardPolicy = {approvedTerms: ["中文"]};
    const result = run({profile, input: captionDocument([page({text: "中文", endFrame: 15})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /not policy-eligible/);
  });
});

test("policy-eligible numeric brand cards can still be explicitly approved", () => {
  const terminology = baseTerminology();
  terminology.shortCardWhitelist.approved.push("360");
  const result = run({terminology, input: captionDocument([page({text: "360", endFrame: 15})])});
  assert.equal(result.status, 0, result.output);
  assert.match(result.output, /approved short terminology card/);
});

test("strict short cards require reviewer-backed pixel evidence", async (t) => {
  await t.test("frame evidence passes strict", () => {
    const input = captionDocument([page({
      text: "AI",
      endFrame: 15,
      shortCardEvidence: {
        reviewedBy: "reviewer-1",
        evidenceRefs: ["frame:timeline-1@12"],
      },
    })]);
    const result = run({input, strict: true});
    assert.equal(result.status, 0, result.output);
  });

  await t.test("note-only evidence remains migration warning", () => {
    const input = captionDocument([page({
      text: "AI",
      endFrame: 15,
      shortCardEvidence: {
        reviewedBy: "reviewer-1",
        evidenceRefs: ["note:looks-readable"],
      },
    })]);
    const normal = run({input});
    const strict = run({input, strict: true});
    assert.equal(normal.status, 0, normal.output);
    assert.match(normal.output, /missing reviewer\/pixel evidence/);
    assert.equal(strict.status, 1, strict.output);
    assert.match(strict.output, /strict warning mode/);
  });
});

test("edited words require approved auditable correction records", async (t) => {
  await t.test("missing correction record fails", () => {
    const words = [sourceBoundWord({sourceText: "原词", text: "新词"})];
    const result = run({input: captionDocument([page({text: "新词", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /CORRECTION_RECORD_REQUIRED/);
  });

  await t.test("schema enforces correction record fields", () => {
    const words = [sourceBoundWord({
      sourceText: "原词",
      text: "新词",
      correction: {
        approved: true,
        reason: "reviewed",
        evidenceRefs: ["transcript:segment-1"],
        reviewedBy: "reviewer-1",
      },
    })];
    const result = run({input: captionDocument([page({text: "新词", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /caption schema required@\/pages\/0\/words\/0\/correction/);
  });

  await t.test("low-risk correction with complete record passes strict", () => {
    const words = [sourceBoundWord({
      sourceText: "原词",
      text: "新词",
      correction: approvedCorrection(),
    })];
    const result = run({
      input: captionDocument([page({text: "新词", words})]),
      strict: true,
    });
    assert.equal(result.status, 0, result.output);
  });

  await t.test("numeric semantic change rejects note-only evidence", () => {
    const words = [sourceBoundWord({
      sourceText: "-50",
      text: "50",
      correction: approvedCorrection({evidenceRefs: ["note:manual-review"]}),
    })];
    const result = run({input: captionDocument([page({text: "50", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /CORRECTION_AUDIO_EVIDENCE_REQUIRED/);
    assert.equal(result.output.includes("-50"), false, result.output);
    assert.equal(result.output.includes("note:manual-review"), false, result.output);
  });

  await t.test("numeric semantic change accepts audio evidence", () => {
    const words = [sourceBoundWord({
      sourceText: "-50",
      text: "50",
      correction: approvedCorrection({evidenceRefs: ["audio:source-asset-1#0-1s"]}),
    })];
    const result = run({
      input: captionDocument([page({text: "50", words})]),
      strict: true,
    });
    assert.equal(result.status, 0, result.output);
  });

  await t.test("negation change rejects non-audio evidence", () => {
    const words = [sourceBoundWord({
      sourceText: "不盈利",
      text: "盈利",
      correction: approvedCorrection({evidenceRefs: ["transcript:segment-1"]}),
    })];
    const result = run({input: captionDocument([page({text: "盈利", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /CORRECTION_AUDIO_EVIDENCE_REQUIRED/);
    assert.equal(result.output.includes("不盈利"), false, result.output);
  });

  await t.test("Chinese-number changes reject non-audio evidence", () => {
    const words = [sourceBoundWord({
      sourceText: "五百元",
      text: "五十元",
      correction: approvedCorrection({evidenceRefs: ["transcript:segment-1"]}),
    })];
    const result = run({input: captionDocument([page({text: "五十元", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /CORRECTION_AUDIO_EVIDENCE_REQUIRED/);
    assert.equal(result.output.includes("五百元"), false, result.output);
  });

  await t.test("unit-token changes reject non-audio evidence", () => {
    const words = [sourceBoundWord({
      sourceText: "MB",
      text: "Mb",
      correction: approvedCorrection({evidenceRefs: ["transcript:segment-1"]}),
    })];
    const result = run({input: captionDocument([page({text: "Mb", words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /CORRECTION_AUDIO_EVIDENCE_REQUIRED/);
  });
});

test("terminology-linked corrections require stable termId and risk audio", async (t) => {
  const terminology = baseTerminology();
  terminology.entries = [{
    termId: "term-product-name",
    correct: "正牌",
    wrong: ["误牌"],
    matchMode: "exact",
    risk: "proper-noun",
  }];

  await t.test("matching termId is mandatory", () => {
    const words = [sourceBoundWord({
      sourceText: "误牌",
      text: "正牌",
      correction: approvedCorrection({evidenceRefs: ["audio:clip-1"]}),
    })];
    const result = run({
      terminology,
      input: captionDocument([page({text: "正牌", words})]),
    });
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /CORRECTION_TERM_ID_REQUIRED/);
  });

  await t.test("proper-noun risk requires audio even without requiresAudioEvidence", () => {
    const words = [sourceBoundWord({
      sourceText: "误牌",
      text: "正牌",
      correction: approvedCorrection({
        termId: "term-product-name",
        evidenceRefs: ["transcript:segment-1"],
      }),
    })];
    const result = run({
      terminology,
      input: captionDocument([page({text: "正牌", words})]),
    });
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /CORRECTION_AUDIO_EVIDENCE_REQUIRED/);
  });

  await t.test("mismatched termId fails", () => {
    const words = [sourceBoundWord({
      sourceText: "误牌",
      text: "正牌",
      correction: approvedCorrection({
        termId: "term-data-analyst",
        evidenceRefs: ["audio:clip-1"],
      }),
    })];
    const result = run({
      terminology,
      input: captionDocument([page({text: "正牌", words})]),
    });
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /CORRECTION_TERM_ID_MISMATCH/);
  });

  await t.test("matching termId with audio passes", () => {
    const words = [sourceBoundWord({
      sourceText: "误牌",
      text: "正牌",
      correction: approvedCorrection({
        termId: "term-product-name",
        evidenceRefs: ["audio:clip-1"],
      }),
    })];
    const result = run({
      terminology,
      input: captionDocument([page({text: "正牌", words})]),
      strict: true,
    });
    assert.equal(result.status, 0, result.output);
  });
});

test("display override hard limit cannot be enlarged by a profile", () => {
  const profile = baseProfile();
  profile.captions.displayOverridePolicy.maxReplacementCharacters = 99;
  const text = "超长替换文本";
  const words = [{key: "w-override", sourceText: "原词", text, startFrame: 0, endFrame: 30}];
  const result = run({profile, input: captionDocument([page({text, words})])});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /exceeds 4 characters/);
});

test("a profile may make the display override limit stricter", () => {
  const profile = baseProfile();
  profile.captions.displayOverridePolicy.maxReplacementCharacters = 2;
  const text = "三字符";
  const words = [{key: "w-strict-override", sourceText: "原词", text, startFrame: 0, endFrame: 30}];
  const result = run({profile, input: captionDocument([page({text, words})])});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /exceeds 2 characters/);
});

test("a profile may disable display overrides with a zero limit", () => {
  const profile = baseProfile();
  profile.captions.displayOverridePolicy.maxReplacementCharacters = 0;
  const text = "改";
  const words = [{key: "w-no-override", sourceText: "原", text, startFrame: 0, endFrame: 30}];
  const result = run({profile, input: captionDocument([page({text, words})])});
  assert.equal(result.status, 1, result.output);
  assert.match(result.output, /exceeds 0 characters/);
});

test("sourceText differences enforce override limits even when edited is false or omitted", async (t) => {
  for (const edited of [false, undefined]) {
    await t.test(`edited=${String(edited)}`, () => {
      const text = "超长替换文本";
      const word = {
        key: `w-derived-${String(edited)}`,
        sourceText: "原词",
        text,
        startFrame: 0,
        endFrame: 30,
      };
      if (edited !== undefined) word.edited = edited;
      const result = run({input: captionDocument([page({text, words: [word]})])});
      assert.equal(result.status, 1, result.output);
      assert.match(result.output, /exceeds 4 characters/);
    });
  }
});

test("edited is only a legacy consistency assertion when sourceText exists", async (t) => {
  await t.test("false cannot deny a derived edit", () => {
    const text = "改词";
    const words = [{key: "w-false", sourceText: "原词", text, startFrame: 0, endFrame: 30, edited: false}];
    const result = run({input: captionDocument([page({text, words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /edited assertion disagrees with derived edit state/);
  });

  await t.test("true cannot invent an edit", () => {
    const text = "原词";
    const words = [{key: "w-true", sourceText: text, text, startFrame: 0, endFrame: 30, edited: true}];
    const result = run({input: captionDocument([page({text, words})])});
    assert.equal(result.status, 1, result.output);
    assert.match(result.output, /edited assertion disagrees with derived edit state/);
  });
});

test("missing sourceText is migration-only and strict mode blocks it", () => {
  const text = "旧结构字幕";
  const words = [{key: "w-legacy-source", text, startFrame: 0, endFrame: 30}];
  const input = captionDocument([page({text, words})]);
  const normal = run({input});
  const strict = run({input, strict: true});
  assert.equal(normal.status, 0, normal.output);
  assert.match(normal.output, /word evidence is missing sourceText/);
  assert.equal(strict.status, 1, strict.output);
  assert.match(strict.output, /strict warning mode/);
});

test("--strict turns warnings into a blocking exit status", () => {
  const input = captionDocument([page({text: "AI", endFrame: 15})]);
  const normal = run({input});
  const strict = run({input, strict: true});
  assert.equal(normal.status, 0, normal.output);
  assert.match(normal.output, /WARN .*approved short terminology card/);
  assert.equal(strict.status, 1, strict.output);
  assert.match(strict.output, /strict warning mode/);
});

test("rejects untested profiles and missing validation provenance", () => {
  const profile = baseProfile({status: "untested-template", provenance: {projectId: "REPLACE", validatedTimelineIds: []}});
  const result = run({profile, input: captionDocument([page()])});
  assert.equal(result.status, 1);
  assert.match(result.output, /release requires validated/);
  assert.match(result.output, /no validatedTimelineIds/);
});

test("--terms overrides the profile terminology file (local personal layer)", () => {
  const localTerms = {
    version: "1.0.0",
    maintainer: "test-fixture",
    entries: [{termId: "term-local-brand", correct: "正确品牌", wrong: ["错误品牌"], matchMode: "substring"}],
    shortCardWhitelist: {approved: ["AI"]},
  };
  const hit = run({localTerms, input: captionDocument([page({text: "这里写了错误品牌"})])});
  assert.equal(hit.status, 1);
  assert.match(hit.output, /terminology entry 0: forbidden form detected/);
  const clean = run({localTerms, input: captionDocument([page({text: "这里写了正确品牌"})])});
  assert.equal(clean.status, 0, clean.output);
});

test("legacy parser handles escaped ASCII quotes without truncation", () => {
  const input = [
    "source variant: original",
    "timeline fps: 30",
    "automatic wrap allowed: true",
    "pagination density: maxLines=2 maxCharactersPerLine=22",
    String.raw`[P1] frame=0-30 text="他说这是 \"AI Native\"" lines=1 words=1`,
    String.raw`  - key=w1 text="他说这是 \"AI Native\"" frame=0-30`,
  ].join("\n");
  const result = run({input});
  assert.equal(result.status, 0, result.output);
});
