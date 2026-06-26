import { keccak256, stringToHex } from "viem";

export type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue };

export type RequirementJson = {
  title: string;
  description: string;
  requirements: JsonValue[];
  deliverables: JsonValue[];
  referenceFiles: JsonValue[];
  contactInfo: { [key: string]: JsonValue };
};

type RequirementVerification = {
  match: boolean;
  onchainRequirementHash: string;
  computedRequirementHash?: `0x${string}`;
  canonicalRequirementJson?: string;
  reason?: string;
};

const REQUIREMENT_KEYS = [
  "title",
  "description",
  "requirements",
  "deliverables",
  "referenceFiles",
  "contactInfo",
] as const;

function jsonValueFromUnknown(value: unknown, key: string): JsonValue {
  if (
    value === null ||
    typeof value === "string" ||
    typeof value === "number" ||
    typeof value === "boolean"
  ) {
    return value;
  }

  if (Array.isArray(value)) {
    return value.map((item, index) => jsonValueFromUnknown(item, `${key}[${index}]`));
  }

  if (typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([entryKey, entryValue]) => [
        entryKey,
        jsonValueFromUnknown(entryValue, `${key}.${entryKey}`),
      ]),
    );
  }

  throw new Error(`${key} must be valid JSON`);
}

function parseRequirementInput(value: unknown): unknown {
  if (typeof value === "string") {
    const trimmed = value.trim();
    if (trimmed === "") {
      throw new Error("requirementJson must be a non-empty object");
    }
    return JSON.parse(trimmed);
  }

  return value;
}

function sortJsonValue(value: JsonValue): JsonValue {
  if (Array.isArray(value)) {
    return value.map(sortJsonValue);
  }

  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, sortJsonValue(value[key])]),
    );
  }

  return value;
}

function canonicalJsonString(value: JsonValue): string {
  if (value === null || typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    return JSON.stringify(value);
  }

  if (Array.isArray(value)) {
    return `[${value.map(canonicalJsonString).join(",")}]`;
  }

  const keys = Object.keys(value).sort();
  return `{${keys.map((key) => `${JSON.stringify(key)}:${canonicalJsonString(value[key])}`).join(",")}}`;
}

export function normalizeRequirementJson(value: unknown): RequirementJson {
  const parsed = parseRequirementInput(value);
  if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error("requirementJson must be an object");
  }

  const record = Object.fromEntries(Object.entries(parsed));
  const extraKeys = Object.keys(record).filter(
    (key) => !REQUIREMENT_KEYS.includes(key as (typeof REQUIREMENT_KEYS)[number]),
  );
  if (extraKeys.length > 0) {
    throw new Error(`requirementJson contains unsupported keys: ${extraKeys.join(", ")}`);
  }

  const missingKeys = REQUIREMENT_KEYS.filter((key) => record[key] === undefined);
  if (missingKeys.includes("title") || missingKeys.includes("description")) {
    throw new Error("requirementJson must include title and description");
  }

  if (typeof record.title !== "string" || record.title.trim() === "") {
    throw new Error("requirementJson.title must be a non-empty string");
  }
  if (typeof record.description !== "string" || record.description.trim() === "") {
    throw new Error("requirementJson.description must be a non-empty string");
  }

  const requirements = record.requirements ?? [];
  const deliverables = record.deliverables ?? [];
  const referenceFiles = record.referenceFiles ?? [];
  const contactInfo = record.contactInfo ?? {};

  if (!Array.isArray(requirements)) {
    throw new Error("requirementJson.requirements must be an array");
  }
  if (!Array.isArray(deliverables)) {
    throw new Error("requirementJson.deliverables must be an array");
  }
  if (!Array.isArray(referenceFiles)) {
    throw new Error("requirementJson.referenceFiles must be an array");
  }
  if (contactInfo === null || typeof contactInfo !== "object" || Array.isArray(contactInfo)) {
    throw new Error("requirementJson.contactInfo must be an object");
  }

  return {
    title: record.title,
    description: record.description,
    requirements: requirements.map((item, index) => sortJsonValue(jsonValueFromUnknown(item, `requirements[${index}]`))),
    deliverables: deliverables.map((item, index) => sortJsonValue(jsonValueFromUnknown(item, `deliverables[${index}]`))),
    referenceFiles: referenceFiles.map((item, index) => sortJsonValue(jsonValueFromUnknown(item, `referenceFiles[${index}]`))),
    contactInfo: sortJsonValue(jsonValueFromUnknown(contactInfo, "contactInfo")) as { [key: string]: JsonValue },
  };
}

export function canonicalRequirementJsonString(value: unknown): string {
  const requirement = normalizeRequirementJson(value);
  return `{${[
    `"title":${JSON.stringify(requirement.title)}`,
    `"description":${JSON.stringify(requirement.description)}`,
    `"requirements":${canonicalJsonString(requirement.requirements)}`,
    `"deliverables":${canonicalJsonString(requirement.deliverables)}`,
    `"referenceFiles":${canonicalJsonString(requirement.referenceFiles)}`,
    `"contactInfo":${canonicalJsonString(requirement.contactInfo)}`,
  ].join(",")}}`;
}

export function hashRequirementJson(value: unknown): `0x${string}` {
  return keccak256(stringToHex(canonicalRequirementJsonString(value)));
}

export function prepareRequirementForTask(value: unknown, expectedHash?: string) {
  const requirementJson = normalizeRequirementJson(value);
  const canonicalRequirementJson = canonicalRequirementJsonString(requirementJson);
  const requirementHash = hashRequirementJson(requirementJson);

  if (expectedHash && expectedHash.toLowerCase() !== requirementHash.toLowerCase()) {
    throw new Error("requirementHash does not match canonical requirementJson");
  }

  return {
    requirementJson,
    canonicalRequirementJson,
    requirementHash,
  };
}

export function verifyRequirementHash(
  onchainRequirementHash: string,
  requirementJson: unknown,
): RequirementVerification {
  if (onchainRequirementHash.trim() === "") {
    return {
      match: false,
      onchainRequirementHash,
      reason: "missing on-chain requirement hash",
    };
  }

  try {
    const prepared = prepareRequirementForTask(requirementJson);
    return {
      match: prepared.requirementHash.toLowerCase() === onchainRequirementHash.toLowerCase(),
      onchainRequirementHash,
      computedRequirementHash: prepared.requirementHash,
      canonicalRequirementJson: prepared.canonicalRequirementJson,
      reason:
        prepared.requirementHash.toLowerCase() === onchainRequirementHash.toLowerCase()
          ? undefined
          : "hash mismatch",
    };
  } catch (error) {
    return {
      match: false,
      onchainRequirementHash,
      reason: error instanceof Error ? error.message : "invalid requirementJson",
    };
  }
}
