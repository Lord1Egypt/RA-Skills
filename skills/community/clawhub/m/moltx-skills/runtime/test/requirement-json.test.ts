import test from "node:test";
import assert from "node:assert/strict";

import {
  canonicalRequirementJsonString,
  hashRequirementJson,
  normalizeRequirementJson,
  prepareRequirementForTask,
  verifyRequirementHash,
} from "../src/tools/requirement.ts";

test("hash_requirement_json is stable across key order changes", () => {
  const requirementA = {
    description: "Create a user-facing onboarding guide",
    title: "Write onboarding guide",
    deliverables: [{ type: "file", name: "guide.md", meta: { lang: "en", version: 1 } }],
    requirements: ["Use plain English", { sections: ["setup", "usage", "failures"], priority: 1 }],
    contactInfo: { telegram: "@maker", channels: { primary: "telegram", backup: "email" } },
    referenceFiles: [{ label: "Brief", url: "https://example.com/brief" }],
  };

  const requirementB = {
    title: "Write onboarding guide",
    description: "Create a user-facing onboarding guide",
    requirements: ["Use plain English", { priority: 1, sections: ["setup", "usage", "failures"] }],
    deliverables: [{ meta: { version: 1, lang: "en" }, name: "guide.md", type: "file" }],
    referenceFiles: [{ url: "https://example.com/brief", label: "Brief" }],
    contactInfo: { channels: { backup: "email", primary: "telegram" }, telegram: "@maker" },
  };

  assert.equal(hashRequirementJson(requirementA), hashRequirementJson(requirementB));
  assert.equal(
    canonicalRequirementJsonString(requirementA),
    canonicalRequirementJsonString(requirementB),
  );
});

test("prepareRequirementForTask rejects mismatched requirementHash before chain write", () => {
  assert.throws(
    () =>
      prepareRequirementForTask(
        {
          title: "Task",
          description: "Details",
          requirements: [],
          deliverables: [],
          referenceFiles: [],
          contactInfo: {},
        },
        "0x1111111111111111111111111111111111111111111111111111111111111111",
      ),
    /does not match canonical requirementJson/,
  );
});

test("verifyRequirementHash covers match, invalid payload, and mismatch", () => {
  const requirementJson = normalizeRequirementJson({
    title: "Task",
    description: "Details",
    requirements: ["One"],
    deliverables: ["Doc"],
    referenceFiles: [],
    contactInfo: { email: "ops@example.com" },
  });
  const onchainHash = hashRequirementJson(requirementJson);

  assert.deepEqual(
    verifyRequirementHash(onchainHash, requirementJson),
    {
      match: true,
      onchainRequirementHash: onchainHash,
      computedRequirementHash: onchainHash,
      canonicalRequirementJson: canonicalRequirementJsonString(requirementJson),
      reason: undefined,
    },
  );

  assert.deepEqual(
    verifyRequirementHash(onchainHash, {
      title: "Task",
      description: "Details",
      requirements: [],
      deliverables: [],
      referenceFiles: [],
      contactInfo: {},
      notes: "extra",
    }),
    {
      match: false,
      onchainRequirementHash: onchainHash,
      reason: "requirementJson contains unsupported keys: notes",
    },
  );

  const mismatch = verifyRequirementHash(onchainHash, {
    title: "Task",
    description: "Changed",
    requirements: ["One"],
    deliverables: ["Doc"],
    referenceFiles: [],
    contactInfo: { email: "ops@example.com" },
  });
  assert.equal(mismatch.match, false);
  assert.equal(mismatch.reason, "hash mismatch");
});
