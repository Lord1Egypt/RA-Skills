import { baseError } from '../errors.js';

export function normalizeFieldDefinition(field = {}) {
  return {
    field_id: field.field_id || field.id,
    name: field.field_name || field.name,
    type: field.type || field.ui_type || 'unknown',
    required: Boolean(field.required),
    multiple: Boolean(field.multiple),
    writable: isWritableField(field),
    raw: field,
  };
}

export function normalizeSchemaResponse(table = {}, fields = [], views = []) {
  return {
    table: {
      table_id: table.table_id || table.id,
      name: table.name,
    },
    fields: fields.map(normalizeFieldDefinition),
    views,
  };
}

export function resolveField(schema, fieldRef) {
  const normalizedFields = (schema?.fields || []).map(normalizeFieldDefinition);
  const found = normalizedFields.find((field) => field.name === fieldRef || field.field_id === fieldRef);
  if (!found) {
    throw baseError('FIELD_NOT_FOUND', `Field '${fieldRef}' not found`, {
      field: fieldRef,
      available: normalizedFields.map((field) => field.name),
    });
  }
  return found;
}

export function isWritableField(field = {}) {
  const type = field.type || field.ui_type;
  const readOnlyTypes = new Set(['formula', 'lookup', 'rollup', 'created_time', 'modified_time', 'auto_number']);
  return !readOnlyTypes.has(type);
}
