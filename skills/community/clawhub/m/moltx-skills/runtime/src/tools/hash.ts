import { keccak256, stringToHex } from "viem";
import { canonicalRequirementJsonString, hashRequirementJson } from "./requirement.js";

function stringifyJson(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

function toRecord(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("tool payload must be a JSON object");
  }

  return Object.fromEntries(Object.entries(value));
}

export async function hashJsonKeccak(args: {
  jsonString: string;
}): Promise<`0x${string}`> {
  return keccak256(stringToHex(args.jsonString));
}

export async function hashTextKeccak(args: { text: string }): Promise<`0x${string}`> {
  return keccak256(stringToHex(args.text));
}

export const hashTools = {
  hash_json_keccak: async (args: unknown): Promise<string> => {
    const record = toRecord(args);
    if (typeof record.jsonString !== "string") {
      throw new Error("hash_json_keccak expects { jsonString: string }");
    }

    return stringifyJson({
      hash: await hashJsonKeccak({ jsonString: record.jsonString }),
    });
  },
  hash_requirement_json: async (args: unknown): Promise<string> => {
    const record = toRecord(args);
    if (record.requirementJson === undefined) {
      throw new Error("hash_requirement_json expects { requirementJson: object }");
    }

    return stringifyJson({
      hash: hashRequirementJson(record.requirementJson),
      canonicalRequirementJson: canonicalRequirementJsonString(record.requirementJson),
    });
  },
  hash_text_keccak: async (args: unknown): Promise<string> => {
    const record = toRecord(args);
    if (typeof record.text !== "string") {
      throw new Error("hash_text_keccak expects { text: string }");
    }

    return stringifyJson({
      hash: await hashTextKeccak({ text: record.text }),
    });
  },
};
