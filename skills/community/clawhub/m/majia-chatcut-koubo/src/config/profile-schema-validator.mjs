import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import {
  PROFILE_RESOLVED_SCHEMA_ID,
  PROFILE_SOURCE_SCHEMA_ID,
} from "./profile-resolver-ids.mjs";

const moduleDirectory = path.dirname(fileURLToPath(import.meta.url));
const schemaDirectory = path.resolve(moduleDirectory, "..", "..", "schemas");

function readSchema(name) {
  return JSON.parse(fs.readFileSync(path.join(schemaDirectory, name), "utf8"));
}

const sourceSchema = readSchema("profile.source.schema.json");
const resolvedSchema = readSchema("profile.resolved.schema.json");
const ajv = new Ajv2020({
  allErrors: true,
  allowUnionTypes: true,
  logger: false,
  strict: true,
  strictRequired: false,
});
ajv.addSchema(sourceSchema);
ajv.addSchema(resolvedSchema);

const validateSource = ajv.getSchema(PROFILE_SOURCE_SCHEMA_ID);
const validateResolved = ajv.getSchema(PROFILE_RESOLVED_SCHEMA_ID);
if (typeof validateSource !== "function" || typeof validateResolved !== "function") {
  throw new Error("profile schemas did not compile");
}

function normalizedErrors(errors) {
  return (errors ?? []).map((error) => ({
    keyword: error.keyword,
    pointer: error.instancePath || "/",
    schemaPath: error.schemaPath,
    ...(error.keyword === "required"
      ? {missingProperty: error.params.missingProperty}
      : {}),
    ...(error.keyword === "additionalProperties"
      ? {additionalProperty: error.params.additionalProperty}
      : {}),
  }));
}

function run(validator, value) {
  const valid = validator(value);
  return {
    valid,
    errors: valid ? [] : normalizedErrors(validator.errors),
  };
}

export function validateProfileSource(value) {
  return run(validateSource, value);
}

export function validateProfileResolved(value) {
  return run(validateResolved, value);
}
