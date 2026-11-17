import assert from "node:assert/strict";
import {spawnSync} from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {fileURLToPath} from "node:url";
import {
  PROFILE_RESOLVED_SCHEMA_ID,
  ProfileResolutionError,
  getProfileDiagnostics,
  loadProfile,
  resolveProfile,
  toSerializableProfileResolution,
} from "../src/config/profile-resolver.mjs";
import {validateProfileResolved} from "../src/config/profile-schema-validator.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const fixtureRoot = path.join(root, "fixtures", "profiles");
const resolverCli = path.join(root, "src", "cli", "resolve-profile.mjs");

function temporaryDirectory(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "profile-resolver-"));
  t.after(() => fs.rmSync(directory, {recursive: true, force: true}));
  return directory;
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), {recursive: true});
  fs.writeFileSync(file, JSON.stringify(value, null, 2));
}

function validatedProvenance(
  projectId = "fixture-project",
  timelineId = "fixture-timeline",
) {
  return {
    projectId,
    validatedTimelineIds: [timelineId],
    validatedTimelineRevisions: {
      [timelineId]: `${timelineId}-revision`,
    },
    validatedSourceRevisions: {
      "fixture-source": "fixture-source-revision",
    },
  };
}

function baseProfile(overrides = {}) {
  return {
    schemaVersion: "2.0.0",
    policyVersion: "1.0.0",
    profileId: "fixture-profile",
    profileVersion: "1.0.0",
    status: "validated",
    provenance: validatedProvenance(),
    timeline: {width: 1920, height: 1080, fps: 30},
    captions: {
      sourceVariant: "original",
      maxCharactersPerLine: 22,
      displayOverridePolicy: {maxReplacementCharacters: 4},
    },
    presenterWindow: {circleDiameterPx: 330},
    audio: {duplicateTrackPolicy: "mute-or-disable"},
    terminologyFile: "terms.json",
    ...overrides,
  };
}

function isResolutionError(code, pointer) {
  return (error) => {
    assert.ok(error instanceof ProfileResolutionError);
    assert.equal(error.code, code);
    if (pointer) assert.equal(error.details.pointer, pointer);
    return true;
  };
}

test("resolves a standalone legacy-compatible profile value", (t) => {
  const directory = temporaryDirectory(t);
  const profileFile = path.join(directory, "profile.json");
  writeJson(profileFile, baseProfile());

  const result = resolveProfile(profileFile);
  const canonicalDirectory = fs.realpathSync(directory);
  assert.equal(result.resolved.$schema, PROFILE_RESOLVED_SCHEMA_ID);
  assert.equal(
    result.resolved.terminologyFile,
    path.join(canonicalDirectory, "terms.json"),
  );
  assert.equal("extends" in result.resolved, false);
  assert.deepEqual(loadProfile(profileFile), result.resolved);
  assert.equal(result.sources["/terminologyFile"].file, "profile.json");
  assert.equal(result.sources["/terminologyFile"].normalizedPath, true);
});

test("migrates anonymous local layers without inheriting trust metadata", () => {
  const profileFile = path.join(
    fixtureRoot,
    "local",
    "profile.source.json",
  );
  const result = resolveProfile(profileFile, {
    allowedRoot: fixtureRoot,
    traceRoot: fixtureRoot,
  });

  assert.equal(result.resolved.schemaVersion, "2.0.0");
  assert.equal(result.resolved.status, "validated");
  assert.equal(result.resolved.provenance.projectId, "fixture-current-project");
  assert.deepEqual(
    result.resolved.provenance.validatedTimelineIds,
    ["fixture-current-timeline"],
  );
  assert.equal(result.resolved.captions.font, "sans-serif");
  assert.equal(result.resolved.captions.maxCharactersPerLine, 20);
  assert.deepEqual(result.resolved.captions.shortCardPolicy.approvedTerms, ["AI"]);
  assert.equal("terminology" in result.resolved, false);
  assert.ok(result.mergeTrace.some(
    (event) => event.operation === "delete" && event.path === "/terminology",
  ));
  assert.equal(
    result.resolved.terminologyFile,
    path.join(fixtureRoot, "base", "terms", "terminology.json"),
  );
  assert.equal(
    result.sources["/terminologyFile"].file,
    "base/profile.source.json",
  );
  assert.equal(
    result.sources["/captions/maxCharactersPerLine"].file,
    "local/profile.source.json",
  );
  assert.ok(result.mergeTrace.some(
    (event) =>
      event.operation === "discard-non-inheritable"
      && event.path === "/status"
      && event.sourceFile === "base/profile.source.json",
  ));
  assert.ok(result.mergeTrace.some(
    (event) =>
      event.operation === "discard-non-inheritable"
      && event.path === "/provenance",
  ));
});

test("normalizes each terminology path against its declaring profile", (t) => {
  const directory = temporaryDirectory(t);
  const parentDirectory = path.join(directory, "shared", "profile");
  const childDirectory = path.join(directory, "projects", "demo");
  const parentFile = path.join(parentDirectory, "base.json");
  const childFile = path.join(childDirectory, "profile.json");
  writeJson(parentFile, baseProfile({
    profileId: "parent",
    terminologyFile: "../terms/base.json",
  }));
  writeJson(childFile, {
    extends: "../../shared/profile/base.json",
    profileId: "child",
    profileVersion: "1.1.0",
    status: "validated",
    provenance: validatedProvenance("child-project", "child-timeline"),
  });

  const inherited = resolveProfile(childFile, {allowedRoot: directory});
  const canonicalDirectory = fs.realpathSync(directory);
  assert.equal(
    inherited.resolved.terminologyFile,
    path.join(canonicalDirectory, "shared", "terms", "base.json"),
  );

  writeJson(childFile, {
    extends: "../../shared/profile/base.json",
    profileId: "child",
    profileVersion: "1.2.0",
    status: "validated",
    provenance: validatedProvenance("child-project", "child-timeline"),
    terminologyFile: "terms/local.json",
  });
  const overridden = resolveProfile(childFile, {allowedRoot: directory});
  assert.equal(
    overridden.resolved.terminologyFile,
    path.join(canonicalDirectory, "projects", "demo", "terms", "local.json"),
  );
});

test("requires leaf-owned status and complete provenance", (t) => {
  const directory = temporaryDirectory(t);
  const parentFile = path.join(directory, "parent.json");
  const childFile = path.join(directory, "child.json");
  writeJson(parentFile, baseProfile());

  writeJson(childFile, {
    extends: "parent.json",
    provenance: {
      projectId: "child-project",
      validatedTimelineIds: [],
    },
  });
  assert.throws(
    () => resolveProfile(childFile),
    isResolutionError("PROFILE_NON_INHERITABLE_REQUIRED", "/status"),
  );

  writeJson(childFile, {extends: "parent.json", status: "validated"});
  assert.throws(
    () => resolveProfile(childFile),
    isResolutionError("PROFILE_NON_INHERITABLE_REQUIRED", "/provenance"),
  );

  writeJson(childFile, {
    extends: "parent.json",
    status: "validated",
    provenance: {projectId: "child-project"},
  });
  assert.throws(
    () => resolveProfile(childFile),
    isResolutionError("PROFILE_SOURCE_SCHEMA_INVALID"),
  );
});

test("rejects historical statuses on the leaf but permits them on parents", (t) => {
  const directory = temporaryDirectory(t);
  const profileFile = path.join(directory, "profile.json");
  writeJson(profileFile, baseProfile({status: "tested-starting-point"}));
  assert.throws(
    () => resolveProfile(profileFile),
    isResolutionError("PROFILE_INVALID_LEAF_STATUS", "/status"),
  );

  const migrated = resolveProfile(
    path.join(fixtureRoot, "local", "profile.source.json"),
    {allowedRoot: fixtureRoot},
  );
  assert.equal(migrated.resolved.status, "validated");
});

for (const unsafeKey of ["__proto__", "constructor", "prototype"]) {
  test(`rejects unsafe key ${unsafeKey} before merge`, (t) => {
    const directory = temporaryDirectory(t);
    const profileFile = path.join(directory, "profile.json");
    const json = JSON.stringify(baseProfile()).replace(
      '"captions":{',
      `"captions":{"${unsafeKey}":{"polluted":true},`,
    );
    fs.writeFileSync(profileFile, json);

    assert.throws(
      () => resolveProfile(profileFile),
      isResolutionError("PROFILE_UNSAFE_KEY", `/captions/${unsafeKey}`),
    );
    assert.equal({}.polluted, undefined);
  });
}

test("arrays replace while nested profile objects merge", (t) => {
  const directory = temporaryDirectory(t);
  const parentFile = path.join(directory, "parent.json");
  const childFile = path.join(directory, "child.json");
  writeJson(parentFile, baseProfile({
    captions: {
      sourceVariant: "original",
      font: "sans-serif",
      maxCharactersPerLine: 22,
      shortCardPolicy: {
        approvedTerms: ["AI", "BI"],
        requireCompleteSemanticUnit: true,
      },
      displayOverridePolicy: {
        maxReplacementCharacters: 4,
        requireWordLevelAudit: true,
      },
    },
  }));
  writeJson(childFile, {
    extends: "parent.json",
    status: "validated",
    provenance: validatedProvenance("child-project", "child-timeline"),
    captions: {
      shortCardPolicy: {approvedTerms: ["CLI"]},
      displayOverridePolicy: {maxReplacementCharacters: 3},
    },
  });

  const result = resolveProfile(childFile);
  assert.deepEqual(result.resolved.captions.shortCardPolicy, {
    approvedTerms: ["CLI"],
    requireCompleteSemanticUnit: true,
  });
  assert.deepEqual(result.resolved.captions.displayOverridePolicy, {
    maxReplacementCharacters: 3,
    requireWordLevelAudit: true,
  });
  assert.ok(result.mergeTrace.some(
    (event) =>
      event.operation === "replace-array"
      && event.path === "/captions/shortCardPolicy/approvedTerms",
  ));
});

test("detects inheritance cycles using canonical file identities", (t) => {
  const directory = temporaryDirectory(t);
  const first = path.join(directory, "first.json");
  const second = path.join(directory, "second.json");
  writeJson(first, {
    extends: "second.json",
    status: "validated",
    provenance: {projectId: "one", validatedTimelineIds: []},
  });
  writeJson(second, {
    extends: "first.json",
    status: "validated",
    provenance: {projectId: "two", validatedTimelineIds: []},
  });
  assert.throws(
    () => resolveProfile(first),
    isResolutionError("PROFILE_INHERITANCE_CYCLE"),
  );
});

test("safe serialization redacts external absolute paths or rebases them", (t) => {
  const directory = temporaryDirectory(t);
  const profileFile = path.join(directory, "profile.json");
  const reportDirectory = path.join(directory, "reports");
  writeJson(profileFile, baseProfile());
  const result = resolveProfile(profileFile, {tracePathMode: "absolute"});

  const redacted = toSerializableProfileResolution(result, {
    baseDirectory: reportDirectory,
  });
  assert.match(redacted.resolved.terminologyFile, /^<external-path:\d+>$/);
  assert.doesNotMatch(JSON.stringify(redacted), new RegExp(directory));

  const portable = toSerializableProfileResolution(result, {
    baseDirectory: reportDirectory,
    externalPathMode: "relative",
    portableRoot: directory,
  });
  assert.equal(
    portable.resolved.terminologyFile,
    "../terms.json",
  );
  assert.doesNotMatch(
    portable.resolved.terminologyFile,
    /^[/\\]|^[A-Za-z]:/,
  );

  result.resolved.presenterWindow.routePattern = "/hero";
  const semanticSlash = toSerializableProfileResolution(result, {
    baseDirectory: reportDirectory,
  });
  assert.equal(semanticSlash.resolved.presenterWindow.routePattern, "/hero");
});

test("source and resolved schemas expose different inheritance contracts", () => {
  const sourceSchema = JSON.parse(fs.readFileSync(
    path.join(root, "schemas", "profile.source.schema.json"),
    "utf8",
  ));
  const resolvedSchema = JSON.parse(fs.readFileSync(
    path.join(root, "schemas", "profile.resolved.schema.json"),
    "utf8",
  ));
  const compatibilitySchema = JSON.parse(fs.readFileSync(
    path.join(root, "schemas", "profile.schema.json"),
    "utf8",
  ));

  assert.ok(sourceSchema.properties.extends);
  assert.deepEqual(
    resolvedSchema.allOf[1].not.required,
    ["extends"],
  );
  assert.equal(
    compatibilitySchema.$ref,
    sourceSchema.$id,
  );
});

test("resolve-profile CLI emits safe JSON and portable output files", (t) => {
  const directory = temporaryDirectory(t);
  const copiedFixtureRoot = path.join(directory, "profiles");
  fs.cpSync(fixtureRoot, copiedFixtureRoot, {recursive: true});
  const profileFile = path.join(
    copiedFixtureRoot,
    "local",
    "profile.source.json",
  );
  const stdoutRun = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      profileFile,
      "--root",
      copiedFixtureRoot,
      "--format",
      "json",
    ],
    {encoding: "utf8"},
  );
  assert.equal(stdoutRun.status, 0, stdoutRun.stderr);
  const stdoutData = JSON.parse(stdoutRun.stdout);
  assert.equal(stdoutData.ok, true);
  assert.equal(stdoutData.contractStatus, "valid");
  assert.equal("resolved" in stdoutData, false);
  assert.doesNotMatch(stdoutRun.stdout, /\/Users\//);

  const outputFile = path.join(copiedFixtureRoot, "run", "profile.resolved.json");
  const traceFile = path.join(copiedFixtureRoot, "run", "profile.merge-trace.json");
  const fileRun = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      profileFile,
      "--root",
      copiedFixtureRoot,
      "--out",
      outputFile,
      "--trace",
      traceFile,
      "--format",
      "json",
    ],
    {encoding: "utf8"},
  );
  assert.equal(fileRun.status, 0, fileRun.stderr);
  const resolved = JSON.parse(fs.readFileSync(outputFile, "utf8"));
  const trace = fs.readFileSync(traceFile, "utf8");
  assert.equal(resolved.$schema, PROFILE_RESOLVED_SCHEMA_ID);
  assert.equal(path.isAbsolute(resolved.terminologyFile), false);
  assert.equal(
    fs.realpathSync(
      path.resolve(path.dirname(outputFile), resolved.terminologyFile),
    ),
    fs.realpathSync(
      path.join(copiedFixtureRoot, "base", "terms", "terminology.json"),
    ),
  );
  assert.doesNotMatch(trace, /\/Users\//);
});

test("resolve-profile CLI uses non-zero exits and stable error codes", (t) => {
  const directory = temporaryDirectory(t);
  const profileFile = path.join(directory, "profile.json");
  writeJson(profileFile, baseProfile({status: "tested-starting-point"}));
  const run = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      profileFile,
      "--strict",
      "--format",
      "json",
    ],
    {encoding: "utf8"},
  );
  assert.equal(run.status, 1);
  const failure = JSON.parse(run.stderr);
  assert.equal(failure.ok, false);
  assert.equal(failure.error.code, "PROFILE_INVALID_LEAF_STATUS");
  assert.doesNotMatch(run.stderr, new RegExp(directory));
});

test("Ajv rejects every invalid source layer before a child can hide it", (t) => {
  const directory = temporaryDirectory(t);
  const parentFile = path.join(directory, "parent.json");
  const childFile = path.join(directory, "child.json");
  writeJson(parentFile, {...baseProfile(), unexpectedLegacyEscape: true});
  writeJson(childFile, {
    extends: "parent.json",
    status: "validated",
    provenance: validatedProvenance("child-project", "child-timeline"),
  });
  assert.throws(
    () => resolveProfile(childFile),
    isResolutionError("PROFILE_SOURCE_SCHEMA_INVALID"),
  );
});

test("Ajv rejects incomplete merged runtime profiles", (t) => {
  const directory = temporaryDirectory(t);
  const profileFile = path.join(directory, "profile.json");
  writeJson(profileFile, {
    schemaVersion: "2.0.0",
    status: "validated",
    provenance: validatedProvenance(),
  });
  assert.throws(
    () => resolveProfile(profileFile),
    isResolutionError("PROFILE_RESOLVED_SCHEMA_INVALID"),
  );
});

test("resolved contract rejects a source-only terminology tombstone", () => {
  const resolved = baseProfile({terminology: null});
  resolved.$schema = PROFILE_RESOLVED_SCHEMA_ID;
  const validation = validateProfileResolved(resolved);
  assert.equal(validation.valid, false);
  assert.ok(validation.errors.some(
    (error) => error.pointer === "/terminology",
  ));
});

test("strict validated trust rejects placeholder evidence identifiers", (t) => {
  const directory = temporaryDirectory(t);
  const profileFile = path.join(directory, "profile.json");
  writeJson(profileFile, baseProfile({
    provenance: {
      ...validatedProvenance(),
      validatedSourceRevisions: {
        "your-source": "REPLACE-revision",
      },
    },
  }));
  assert.throws(
    () => resolveProfile(profileFile),
    isResolutionError("PROFILE_PLACEHOLDER_PROVENANCE", "/provenance"),
  );
});

test("extends cannot leave allowedRoot lexically or through a symlink", (t) => {
  const directory = temporaryDirectory(t);
  const allowedRoot = path.join(directory, "allowed");
  const outside = path.join(directory, "outside.json");
  writeJson(outside, baseProfile());
  const lexical = path.join(allowedRoot, "lexical.json");
  writeJson(lexical, {
    extends: "../outside.json",
    status: "validated",
    provenance: validatedProvenance(),
  });
  assert.throws(
    () => resolveProfile(lexical, {allowedRoot}),
    isResolutionError("PROFILE_EXTENDS_OUTSIDE_ROOT"),
  );

  fs.mkdirSync(allowedRoot, {recursive: true});
  const link = path.join(allowedRoot, "linked-parent.json");
  fs.symlinkSync(outside, link);
  const symlinked = path.join(allowedRoot, "symlinked.json");
  writeJson(symlinked, {
    extends: "linked-parent.json",
    status: "validated",
    provenance: validatedProvenance(),
  });
  assert.throws(
    () => resolveProfile(symlinked, {allowedRoot}),
    isResolutionError("PROFILE_EXTENDS_OUTSIDE_ROOT"),
  );
});

test("terminologyFile cannot leave allowedRoot lexically or through a symlink", (t) => {
  const directory = temporaryDirectory(t);
  const allowedRoot = path.join(directory, "allowed");
  const outsideTerms = path.join(directory, "outside-terms.json");
  fs.writeFileSync(outsideTerms, "{}");
  const profileFile = path.join(allowedRoot, "profile.json");
  writeJson(profileFile, baseProfile({
    terminologyFile: "../outside-terms.json",
  }));
  assert.throws(
    () => resolveProfile(profileFile, {allowedRoot}),
    isResolutionError(
      "PROFILE_REFERENCE_OUTSIDE_ROOT",
      "/terminologyFile",
    ),
  );

  const linkedTerms = path.join(allowedRoot, "linked-terms.json");
  fs.symlinkSync(outsideTerms, linkedTerms);
  writeJson(profileFile, baseProfile({
    terminologyFile: "linked-terms.json",
  }));
  assert.throws(
    () => resolveProfile(profileFile, {allowedRoot}),
    isResolutionError(
      "PROFILE_REFERENCE_OUTSIDE_ROOT",
      "/terminologyFile",
    ),
  );
});

test("migration mode audits a legacy leaf without inheriting parent trust", (t) => {
  const directory = temporaryDirectory(t);
  const parentFile = path.join(directory, "parent.json");
  const leafFile = path.join(directory, "leaf.json");
  writeJson(parentFile, {
    ...baseProfile({
      schemaVersion: "1.1.0",
      status: "tested-starting-point",
      provenance: {
        projectId: "old-project",
        validatedTimelineIds: ["old-timeline"],
      },
      terminology: {"fixture-term": "legacy"},
    }),
  });
  writeJson(leafFile, {
    extends: "parent.json",
    schemaVersion: "2.0.0",
    profileVersion: "2.1.0",
    status: "validated",
    terminology: null,
  });

  const migration = resolveProfile(leafFile, {trustMode: "migration"});
  assert.equal(migration.resolved.status, "untested-template");
  assert.equal("provenance" in migration.resolved, false);
  assert.equal("terminology" in migration.resolved, false);
  assert.equal(migration.contractStatus, "migration-incomplete");
  assert.ok(migration.warnings.some(
    (warning) => warning.code === "PROFILE_MIGRATION_LEAF_PROVENANCE_MISSING",
  ));
  assert.throws(
    () => resolveProfile(leafFile),
    isResolutionError("PROFILE_NON_INHERITABLE_REQUIRED", "/provenance"),
  );

  const blockedOutput = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      leafFile,
      "--out",
      path.join(directory, "migration.resolved.json"),
      "--format",
      "json",
    ],
    {encoding: "utf8"},
  );
  assert.equal(blockedOutput.status, 1);
  assert.match(blockedOutput.stderr, /PROFILE_CLI_MIGRATION_OUTPUT_BLOCKED/);

  const loaded = loadProfile(leafFile);
  assert.equal(
    getProfileDiagnostics(loaded).contractStatus,
    "migration-incomplete",
  );
});

test("real local legacy chain is migration-readable and strict-failing without leaks", (t) => {
  const configRoot = path.join(
    os.homedir(),
    ".config",
    "majia-chatcut-koubo",
  );
  const profileFile = path.join(
    configRoot,
    "profile",
    "landscape-sea-salt-v2.1.json",
  );
  if (!fs.existsSync(profileFile)) {
    t.skip("local compatibility profile is not installed");
    return;
  }
  const migration = resolveProfile(profileFile, {
    allowedRoot: configRoot,
    trustMode: "migration",
  });
  assert.equal(migration.resolved.status, "untested-template");
  assert.equal("provenance" in migration.resolved, false);
  assert.equal("terminology" in migration.resolved, false);
  assert.equal(migration.contractStatus, "migration-incomplete");

  const normal = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      profileFile,
      "--root",
      configRoot,
      "--format",
      "json",
    ],
    {encoding: "utf8"},
  );
  assert.equal(normal.status, 0, normal.stderr);
  assert.equal(
    JSON.parse(normal.stdout).contractStatus,
    "migration-incomplete",
  );
  assert.equal(normal.stdout.includes(os.homedir()), false);

  const strict = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      profileFile,
      "--root",
      configRoot,
      "--strict",
      "--format",
      "json",
    ],
    {encoding: "utf8"},
  );
  assert.equal(strict.status, 1);
  assert.match(strict.stderr, /PROFILE_NON_INHERITABLE_REQUIRED/);
  assert.equal(strict.stderr.includes(os.homedir()), false);
});

test("CLI rejects duplicate arguments and unsafe output targets", (t) => {
  const directory = temporaryDirectory(t);
  const profileFile = path.join(directory, "profile.json");
  writeJson(profileFile, baseProfile());

  const duplicate = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      profileFile,
      "--profile",
      profileFile,
    ],
    {encoding: "utf8"},
  );
  assert.equal(duplicate.status, 2);
  assert.match(duplicate.stderr, /PROFILE_CLI_DUPLICATE_ARGUMENT/);

  const unknown = spawnSync(
    process.execPath,
    [
      resolverCli,
      path.join(path.parse(process.cwd()).root, "Users", "SENSITIVE_ARGUMENT_SENTINEL"),
    ],
    {encoding: "utf8"},
  );
  assert.equal(unknown.status, 2);
  assert.match(unknown.stderr, /PROFILE_CLI_UNKNOWN_ARGUMENT/);
  assert.equal(unknown.stderr.includes("SENSITIVE_ARGUMENT_SENTINEL"), false);

  const overwrite = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      profileFile,
      "--out",
      profileFile,
    ],
    {encoding: "utf8"},
  );
  assert.equal(overwrite.status, 1);
  assert.match(overwrite.stderr, /PROFILE_CLI_SOURCE_COLLISION/);

  const referenceCollision = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      profileFile,
      "--out",
      path.join(directory, "terms.json"),
    ],
    {encoding: "utf8"},
  );
  assert.equal(referenceCollision.status, 1);
  assert.match(referenceCollision.stderr, /PROFILE_CLI_REFERENCE_COLLISION/);

  const parentFile = path.join(directory, "parent.json");
  const childFile = path.join(directory, "child.json");
  writeJson(parentFile, baseProfile({profileId: "parent"}));
  writeJson(childFile, {
    extends: "parent.json",
    profileId: "child",
    profileVersion: "1.1.0",
    status: "validated",
    provenance: validatedProvenance("child-project", "child-timeline"),
  });
  const parentCollision = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      childFile,
      "--trace",
      parentFile,
    ],
    {encoding: "utf8"},
  );
  assert.equal(parentCollision.status, 1);
  assert.match(parentCollision.stderr, /PROFILE_CLI_SOURCE_COLLISION/);

  const outside = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      profileFile,
      "--out",
      path.join(path.dirname(directory), "sensitive-output.json"),
    ],
    {encoding: "utf8"},
  );
  assert.equal(outside.status, 1);
  assert.match(outside.stderr, /PROFILE_CLI_OUTPUT_OUTSIDE_ROOT/);
  assert.equal(outside.stderr.includes(directory), false);
});

test("CLI stdout and unknown I/O errors do not reveal profile identifiers or paths", (t) => {
  const directory = temporaryDirectory(t);
  const profileFile = path.join(directory, "profile.json");
  writeJson(profileFile, baseProfile({
    profileId: "SENSITIVE_PROFILE_SENTINEL",
    provenance: validatedProvenance(
      "SENSITIVE_PROJECT_SENTINEL",
      "SENSITIVE_TIMELINE_SENTINEL",
    ),
  }));
  const summary = spawnSync(
    process.execPath,
    [resolverCli, "--profile", profileFile, "--format", "json"],
    {encoding: "utf8"},
  );
  assert.equal(summary.status, 0, summary.stderr);
  assert.equal(summary.stdout.includes("SENSITIVE_"), false);
  assert.equal(summary.stdout.includes(directory), false);

  const blocked = path.join(directory, "blocked");
  fs.writeFileSync(blocked, "not a directory");
  const ioFailure = spawnSync(
    process.execPath,
    [
      resolverCli,
      "--profile",
      profileFile,
      "--out",
      path.join(blocked, "SENSITIVE_PATH_SENTINEL.json"),
    ],
    {encoding: "utf8"},
  );
  assert.equal(ioFailure.status, 2);
  assert.match(ioFailure.stderr, /PROFILE_CLI_IO_ERROR/);
  assert.equal(ioFailure.stderr.includes("SENSITIVE_PATH_SENTINEL"), false);
  assert.equal(ioFailure.stderr.includes(directory), false);
});
