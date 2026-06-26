import { compileFilter } from './filters.js';
import { normalizeSchemaResponse } from './schema.js';
import { normalizeRecordFieldsForWrite } from './values.js';
import { uploadAttachmentAssetApi, cloneAttachmentAssetApi, normalizeAttachmentsForWrite } from './attachments.js';
import { baseError } from '../errors.js';
import {
  resolveLinkApi,
  listBasesApi,
  listDriveFilesApi,
  listTablesApi,
  createTableApi,
  renameTableApi,
  deleteTableApi,
  createFieldApi,
  renameFieldApi,
  updateFieldApi,
  deleteFieldApi,
  listRawFieldsApi,
  getTableApi,
  getRecordApi,
  queryRecordsApi,
  createRecordsApi,
  updateRecordsApi,
  deleteRecordsApi,
} from './api.js';

export async function resolveLink(client, input) {
  return await resolveLinkApi(client, input);
}

export async function listBases(client, input) {
  return await listBasesApi(client, input);
}

function normalizeName(value) {
  return String(value || '').trim().toLowerCase();
}

function splitTerms(value) {
  return normalizeName(value).split(/[_\s-]+/g).filter(Boolean);
}

function tableMatchScore(tableName, query) {
  const name = normalizeName(tableName);
  const q = normalizeName(query);
  if (!q) return 0;
  if (name === q) return 100;
  if (name.includes(q)) return 80;
  const parts = splitTerms(q);
  const hits = parts.reduce((count, p) => count + (name.includes(p) ? 1 : 0), 0);
  if (!hits) return 0;
  return 20 + (hits * 10);
}

export async function listFolder(client, input) {
  return await listDriveFilesApi(client, {
    ...input,
    folder_token: input.folder_token,
    page_size: input.page_size || 100,
  });
}

export async function findTable(client, input) {
  const baseName = normalizeName(input.base_name);
  const tableName = normalizeName(input.table_name);
  const bases = await listBasesApi(client, { ...input, query: input.base_name, page_size: 500 });
  const baseItems = Array.isArray(bases?.items) ? bases.items : [];
  const base = baseItems.find((item) => normalizeName(item.name) === baseName)
    || baseItems.find((item) => normalizeName(item.name).includes(baseName) || baseName.includes(normalizeName(item.name)));

  if (!base) {
    return {
      matched: false,
      reason: 'BASE_NOT_FOUND',
      base_name: input.base_name,
      candidates: baseItems.slice(0, 20).map((item) => ({ app_token: item.app_token, name: item.name })),
    };
  }

  if (!tableName) {
    return {
      matched: true,
      base: { app_token: base.app_token, name: base.name },
    };
  }

  const tables = await listTablesApi(client, { ...input, app_token: base.app_token, page_size: 500 });
  const tableItems = Array.isArray(tables?.items) ? tables.items : [];
  const table = tableItems.find((item) => normalizeName(item.name) === tableName)
    || tableItems.find((item) => normalizeName(item.name).includes(tableName) || tableName.includes(normalizeName(item.name)));

  if (!table) {
    return {
      matched: false,
      reason: 'TABLE_NOT_FOUND',
      base: { app_token: base.app_token, name: base.name },
      table_name: input.table_name,
      candidates: tableItems.slice(0, 50).map((item) => ({ table_id: item.table_id, name: item.name })),
    };
  }

  return {
    matched: true,
    base: { app_token: base.app_token, name: base.name },
    table: { table_id: table.table_id, name: table.name },
  };
}

export async function listTables(client, input) {
  return await listTablesApi(client, input);
}

export async function discoverTables(client, input) {
  const discoveredBases = [];
  const inaccessibleBases = [];
  const tables = [];
  const appTokens = new Set(Array.isArray(input.app_tokens) ? input.app_tokens.filter(Boolean) : []);

  // Discover candidate bases from Drive-visible bases (optionally filtered by query).
  let pageToken = '';
  let hasMore = true;
  const maxPages = 20;
  let pages = 0;
  while (hasMore && pages < maxPages) {
    pages += 1;
    const basesPage = await listBasesApi(client, {
      page_size: input.page_size || 200,
      page_token: pageToken || undefined,
      query: input.base_query,
    });
    for (const item of basesPage.items || []) {
      if (item?.app_token) {
        appTokens.add(item.app_token);
        discoveredBases.push({ app_token: item.app_token, name: item.name || null });
      }
    }
    hasMore = Boolean(basesPage.has_more);
    pageToken = basesPage.page_token || '';
  }

  for (const appToken of appTokens) {
    try {
      const baseName = discoveredBases.find((b) => b.app_token === appToken)?.name || null;
      const page = await listTablesApi(client, {
        app_token: appToken,
        page_size: input.page_size || 500,
      });
      for (const table of page.items || []) {
        const row = {
          app_token: appToken,
          base_name: baseName,
          table_id: table.table_id,
          table_name: table.name,
        };
        if (!input.query || tableMatchScore(table.name, input.query) > 0) {
          row.match_score = tableMatchScore(table.name, input.query);
        }
        tables.push(row);
      }
    } catch (error) {
      inaccessibleBases.push({
        app_token: appToken,
        message: error?.message || 'Failed to list tables',
      });
    }
  }

  const sorted = input.query
    ? tables.sort((a, b) => (b.match_score || 0) - (a.match_score || 0))
    : tables.sort((a, b) => normalizeName(a.table_name).localeCompare(normalizeName(b.table_name)));

  return {
    query: input.query || null,
    summary: {
      discovered_base_count: appTokens.size,
      accessible_table_count: sorted.length,
      inaccessible_base_count: inaccessibleBases.length,
    },
    tables: sorted,
    inaccessible_bases: inaccessibleBases,
  };
}

export async function createTable(client, input) {
  const created = await createTableApi(client, input);
  const tableId = created?.table?.table_id;
  const requestedFields = Array.isArray(input.fields) ? input.fields : [];

  if (!tableId || requestedFields.length === 0) {
    return created;
  }

  const fields = [];
  for (const field of requestedFields) {
    const createdField = await createFieldApi(client, {
      ...input,
      table_id: tableId,
      field_name: field.field_name,
      field_type: field.field_type,
      property: field.property,
    });
    fields.push(createdField);
  }

  return {
    ...created,
    fields,
  };
}

export async function renameTable(client, input) {
  return await renameTableApi(client, {
    ...input,
    table_name: input.table_name || input.new_name,
  });
}

export async function deleteTable(client, input) {
  if (!input._limits.allowDelete) {
    throw baseError('DELETE_DISABLED', 'delete_table is disabled by plugin config');
  }
  return await deleteTableApi(client, input);
}

export async function createField(client, input) {
  const resolved = { ...input };

  if (resolved.link && typeof resolved.link === 'object') {
    const link = resolved.link;
    let targetTableId = typeof link.table_id === 'string' ? link.table_id.trim() : '';

    if (!targetTableId && typeof link.table_name === 'string' && link.table_name.trim()) {
      const tables = await listTablesApi(client, { app_token: resolved.app_token, page_size: 500 });
      const tableName = normalizeName(link.table_name);
      const tableItems = Array.isArray(tables?.items) ? tables.items : [];
      const matched = tableItems.find((item) => normalizeName(item.name) === tableName)
        || tableItems.find((item) => normalizeName(item.name).includes(tableName) || tableName.includes(normalizeName(item.name)));

      if (!matched?.table_id) {
        throw baseError('LINK_TARGET_TABLE_NOT_FOUND', `Linked field target table '${link.table_name}' not found`, {
          table_name: link.table_name,
          candidates: tableItems.slice(0, 50).map((item) => ({ table_id: item.table_id, name: item.name })),
        });
      }

      targetTableId = matched.table_id;
    }

    if (!targetTableId) {
      throw baseError('INVALID_LINK_FIELD', 'Linked field creation requires link.table_id or link.table_name');
    }

    resolved.property = {
      ...(resolved.property && typeof resolved.property === 'object' ? resolved.property : {}),
      table_id: targetTableId,
      multiple: typeof link.multiple === 'boolean' ? link.multiple : Boolean(resolved.property?.multiple),
    };

    if (typeof link.back_field_name === 'string' && link.back_field_name.trim()) {
      resolved.property.back_field_name = link.back_field_name.trim();
      if (typeof resolved.field_type !== 'number' || resolved.field_type === 18) {
        resolved.field_type = 21;
      }
    }
  }

  return await createFieldApi(client, resolved);
}

export async function renameField(client, input) {
  const rawFields = await listRawFieldsApi(client, input);
  const existing = (rawFields || []).find((field) => field.field_id === input.field_id);
  if (!existing) {
    throw baseError('FIELD_NOT_FOUND', `Field '${input.field_id}' not found`, { field_id: input.field_id });
  }
  return await renameFieldApi(client, {
    ...input,
    field_type: existing.type,
  });
}

export async function updateField(client, input) {
  const rawFields = await listRawFieldsApi(client, input);
  const existing = (rawFields || []).find((field) => field.field_id === input.field_id);
  if (!existing) {
    throw baseError('FIELD_NOT_FOUND', `Field '${input.field_id}' not found`, { field_id: input.field_id });
  }
  const resolved = {
    ...input,
    field_name: input.field_name || existing.field_name,
    field_type: typeof input.field_type === 'number' ? input.field_type : existing.type,
  };
  if (input.property && typeof input.property === 'object') {
    resolved.property = input.property;
  }
  return await updateFieldApi(client, resolved);
}

export async function deleteField(client, input) {
  if (!input._limits.allowDelete) {
    throw baseError('DELETE_DISABLED', 'delete_field is disabled by plugin config');
  }
  return await deleteFieldApi(client, input);
}

export async function getTable(client, input) {
  const raw = await getTableApi(client, input);
  return normalizeSchemaResponse(raw.table, raw.fields || [], raw.views || []);
}

export async function getRecord(client, input) {
  return await getRecordApi(client, input);
}

export async function queryRecords(client, input) {
  const compiledFilter = compileFilter(input.filter);
  return await queryRecordsApi(client, { ...input, compiledFilter });
}

export async function createRecords(client, input) {
  const schema = await getTable(client, input);
  if ((input.records || []).length > input._limits.maxBatchWrite) {
    throw baseError('BATCH_LIMIT_EXCEEDED', `create_records exceeds maxBatchWrite=${input._limits.maxBatchWrite}`);
  }
  const records = (input.records || []).map((record) => ({
    fields: normalizeRecordFieldsForWrite(schema, record.fields),
  }));
  return await createRecordsApi(client, { ...input, records });
}

export async function updateRecords(client, input) {
  const schema = await getTable(client, input);
  if ((input.records || []).length > input._limits.maxBatchWrite) {
    throw baseError('BATCH_LIMIT_EXCEEDED', `update_records exceeds maxBatchWrite=${input._limits.maxBatchWrite}`);
  }
  const records = (input.records || []).map((record) => ({
    record_id: record.record_id,
    fields: normalizeRecordFieldsForWrite(schema, record.fields),
  }));
  return await updateRecordsApi(client, { ...input, records });
}

export async function upsertRecords(client, input) {
  const results = [];
  for (const item of input.records || []) {
    const matchValue = item?.fields?.[input.match.field];
    if (matchValue == null) {
      throw baseError('INVALID_FIELD_VALUE', `Missing match field '${input.match.field}' for upsert`);
    }
    const found = await queryRecords(client, {
      ...input,
      action: 'query_records',
      filter: {
        field: input.match.field,
        operator: 'equals',
        value: matchValue,
      },
      page_size: 2,
    });

    const items = found?.items || [];
    if (items.length === 0) {
      const created = await createRecords(client, {
        ...input,
        action: 'create_records',
        records: [{ fields: item.fields }],
      });
      for (const row of created.items || []) results.push({ action: 'created', ...row });
    } else if (items.length === 1) {
      const updated = await updateRecords(client, {
        ...input,
        action: 'update_records',
        records: [{ record_id: items[0].record_id, fields: item.fields }],
      });
      for (const row of updated.items || []) results.push({ action: 'updated', ...row });
    } else {
      throw baseError('AMBIGUOUS_MATCH', `Multiple records matched field '${input.match.field}'`, {
        field: input.match.field,
        value: matchValue,
      });
    }
  }
  return { items: results };
}

export async function deleteRecords(client, input) {
  if (!input._limits.allowDelete) {
    throw baseError('DELETE_DISABLED', 'delete_records is disabled by plugin config');
  }

  let recordIds = input.record_ids || [];
  if ((!recordIds || recordIds.length === 0) && input.filter) {
    const found = await queryRecords(client, {
      ...input,
      action: 'query_records',
      fields: [],
      page_size: input._limits.maxBatchDelete + 1,
    });
    recordIds = (found.items || []).map((item) => item.record_id);
  }

  if (!recordIds.length) {
    throw baseError('INVALID_DELETE_TARGET', 'delete_records requires record_ids or a filter that resolves to at least one record');
  }
  if (recordIds.length > input._limits.maxBatchDelete) {
    throw baseError('BATCH_LIMIT_EXCEEDED', `delete_records exceeds maxBatchDelete=${input._limits.maxBatchDelete}`);
  }

  return await deleteRecordsApi(client, { ...input, record_ids: recordIds });
}

export async function uploadAttachment(client, input) {
  return await uploadAttachmentAssetApi(client, input);
}

export async function cloneAttachment(client, input) {
  return await cloneAttachmentAssetApi(client, input);
}

export async function buildAttachmentFieldValue(_client, input) {
  return normalizeAttachmentsForWrite(input);
}
