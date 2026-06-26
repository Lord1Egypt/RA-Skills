import { baseError } from '../errors.js';
import { resolveField } from './schema.js';

export function normalizeRecordFieldsForWrite(schema, fields) {
  const out = {};
  for (const [key, value] of Object.entries(fields || {})) {
    const field = resolveField(schema, key);
    if (!field.writable) {
      throw baseError('UNSUPPORTED_FIELD_TYPE', `Field '${field.name}' is not writable`, {
        field: field.name,
        type: field.type,
      });
    }
    out[field.name] = normalizeFieldValue(field, value);
  }
  return out;
}

export function normalizeFieldValue(field, value) {
  switch (field.type) {
    case 'text':
    case 'email':
    case 'url':
    case 'phone':
    case 'single_select':
      return value == null ? null : String(value);
    case 'number':
      if (value == null || value === '') return null;
      if (typeof value !== 'number') throw baseError('INVALID_FIELD_VALUE', `Field '${field.name}' expects a number`);
      return value;
    case 'checkbox':
      return Boolean(value);
    case 'multi_select':
      if (!Array.isArray(value)) throw baseError('INVALID_FIELD_VALUE', `Field '${field.name}' expects an array`);
      return value.map((item) => String(item));
    case 'date':
    case 'datetime':
      return value == null ? null : String(value);
    default:
      return value;
  }
}
