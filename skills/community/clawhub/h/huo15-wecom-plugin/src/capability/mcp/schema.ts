const GEMINI_UNSUPPORTED_KEYWORDS = new Set([
  "patternProperties",
  "additionalProperties",
  "$schema",
  "$id",
  "$ref",
  "$defs",
  "definitions",
  "examples",
  "minLength",
  "maxLength",
  "minimum",
  "maximum",
  "multipleOf",
  "pattern",
  "format",
  "minItems",
  "maxItems",
  "uniqueItems",
  "minProperties",
  "maxProperties",
]);

export function cleanSchemaForGemini(schema: unknown): unknown {
  if (!schema || typeof schema !== "object") return schema;
  if (Array.isArray(schema)) return schema.map(cleanSchemaForGemini);

  const obj = schema as Record<string, unknown>;
  const defs: Record<string, unknown> = {
    ...(obj.$defs && typeof obj.$defs === "object" ? (obj.$defs as Record<string, unknown>) : {}),
    ...(obj.definitions && typeof obj.definitions === "object"
      ? (obj.definitions as Record<string, unknown>)
      : {}),
  };
  return cleanWithDefs(obj, defs, new Set());
}

function cleanWithDefs(
  schema: unknown,
  defs: Record<string, unknown>,
  refStack: Set<string>,
): unknown {
  if (!schema || typeof schema !== "object") return schema;
  if (Array.isArray(schema)) return schema.map((item) => cleanWithDefs(item, defs, refStack));

  const obj = schema as Record<string, unknown>;
  if (obj.$defs && typeof obj.$defs === "object") {
    Object.assign(defs, obj.$defs as Record<string, unknown>);
  }
  if (obj.definitions && typeof obj.definitions === "object") {
    Object.assign(defs, obj.definitions as Record<string, unknown>);
  }

  if (typeof obj.$ref === "string") {
    const ref = obj.$ref;
    if (refStack.has(ref)) return {};
    const match = ref.match(/^#\/(?:\$defs|definitions)\/(.+)$/);
    if (match?.[1] && defs[match[1]]) {
      const nextStack = new Set(refStack);
      nextStack.add(ref);
      return cleanWithDefs(defs[match[1]], defs, nextStack);
    }
    return {};
  }

  const cleaned: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    if (GEMINI_UNSUPPORTED_KEYWORDS.has(key)) continue;
    if (key === "const") {
      cleaned.enum = [value];
      continue;
    }
    if (key === "properties" && value && typeof value === "object" && !Array.isArray(value)) {
      cleaned[key] = Object.fromEntries(
        Object.entries(value as Record<string, unknown>).map(([propKey, propValue]) => [
          propKey,
          cleanWithDefs(propValue, defs, refStack),
        ]),
      );
      continue;
    }
    if (key === "items" && value) {
      cleaned[key] = Array.isArray(value)
        ? value.map((item) => cleanWithDefs(item, defs, refStack))
        : cleanWithDefs(value, defs, refStack);
      continue;
    }
    if ((key === "anyOf" || key === "oneOf" || key === "allOf") && Array.isArray(value)) {
      const nonNull = value.filter((variant) => {
        if (!variant || typeof variant !== "object") return true;
        return (variant as Record<string, unknown>).type !== "null";
      });
      if (nonNull.length === 1) {
        const single = cleanWithDefs(nonNull[0], defs, refStack);
        if (single && typeof single === "object" && !Array.isArray(single)) {
          Object.assign(cleaned, single as Record<string, unknown>);
        }
      } else {
        cleaned[key] = nonNull.map((variant) => cleanWithDefs(variant, defs, refStack));
      }
      continue;
    }
    cleaned[key] = value;
  }

  return cleaned;
}
