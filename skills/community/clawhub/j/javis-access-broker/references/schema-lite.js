'use strict';
// Minimal JSON Schema validator for the subset submit-answer.schema.json uses
// (type, enum, const, required, properties, additionalProperties:false, items,
// minItems/maxItems, minLength/maxLength, pattern, allOf, if/then, not).
// The repo has no npm dependencies, so this stays dependency-free.
// Returns a list of error strings; an empty list means valid.

function typeOf(v) {
  if (v === null) return 'null';
  if (Array.isArray(v)) return 'array';
  if (Number.isInteger(v)) return 'integer';
  return typeof v;
}

function validate(schema, value, at = '$') {
  const errors = [];
  if (schema === true) return errors;
  if (schema === false) return [`${at}: not allowed`];

  if (schema.type) {
    const t = typeOf(value);
    const ok = schema.type === t || (schema.type === 'number' && t === 'integer');
    if (!ok) return [`${at}: expected ${schema.type}, got ${t}`];
  }
  if (schema.enum && !schema.enum.some((e) => e === value)) {
    errors.push(`${at}: ${JSON.stringify(value)} not in ${JSON.stringify(schema.enum)}`);
  }
  if ('const' in schema && schema.const !== value) {
    errors.push(`${at}: expected const ${JSON.stringify(schema.const)}`);
  }
  if (typeof value === 'string') {
    if (schema.minLength !== undefined && [...value].length < schema.minLength) errors.push(`${at}: shorter than ${schema.minLength}`);
    if (schema.maxLength !== undefined && [...value].length > schema.maxLength) errors.push(`${at}: longer than ${schema.maxLength}`);
    if (schema.pattern && !new RegExp(schema.pattern, 'u').test(value)) errors.push(`${at}: does not match ${schema.pattern}`);
  }
  if (Array.isArray(value)) {
    if (schema.minItems !== undefined && value.length < schema.minItems) errors.push(`${at}: fewer than ${schema.minItems} items`);
    if (schema.maxItems !== undefined && value.length > schema.maxItems) errors.push(`${at}: more than ${schema.maxItems} items`);
    if (schema.items) value.forEach((v, i) => errors.push(...validate(schema.items, v, `${at}[${i}]`)));
  }
  if (typeOf(value) === 'object') {
    for (const k of schema.required || []) {
      if (!(k in value)) errors.push(`${at}: missing required ${k}`);
    }
    const props = schema.properties || {};
    for (const [k, v] of Object.entries(value)) {
      if (k in props) errors.push(...validate(props[k], v, `${at}.${k}`));
      else if (schema.additionalProperties === false) errors.push(`${at}: unexpected property ${k}`);
    }
  }
  for (const sub of schema.allOf || []) errors.push(...validate(sub, value, at));
  if (schema.if) {
    const matches = validate(schema.if, value, at).length === 0;
    if (matches && schema.then) errors.push(...validate(schema.then, value, at));
    if (!matches && schema.else) errors.push(...validate(schema.else, value, at));
  }
  if (schema.not && validate(schema.not, value, at).length === 0) {
    errors.push(`${at}: matches a forbidden shape`);
  }
  return errors;
}

module.exports = { validate };
