import { baseError } from '../errors.js';

export async function resolveLinkApi(client, input) {
  const resolved = await parseFeishuBaseUrl(client, input.url);
  if (!resolved.app_token) {
    throw baseError('LINK_PARSE_FAILED', 'Could not extract app_token from Feishu Base link', { url: input.url });
  }
  return resolved;
}

export async function listDriveFilesApi(client, input = {}) {
  const response = await client.drive.v1.file.list({
    params: {
      folder_token: input.folder_token,
      page_size: input.page_size || 100,
      page_token: input.page_token,
    },
  }).catch((error) => {
    throw baseError('DRIVE_LIST_FAILED', error?.message || 'Failed to list Feishu Drive files', {
      folder_token: input.folder_token,
    });
  });

  ensureSuccess(response, 'DRIVE_LIST_FAILED');

  const files = response.data?.files || response.data?.items || [];
  return {
    items: files.map((file) => ({
      token: file.token || file.file_token,
      name: file.name,
      type: file.type || file.file_type,
      url: file.url,
      parent_token: file.parent_token,
    })),
    has_more: Boolean(response.data?.has_more),
    page_token: response.data?.next_page_token || response.data?.page_token || '',
  };
}

export async function listBasesApi(client, input) {
  if (input.app_token) {
    const response = await client.bitable.v1.app.get({
      path: { app_token: input.app_token },
    }).catch(() => undefined);

    return {
      items: [normalizeApp(response?.data?.app || { app_token: input.app_token })],
      has_more: false,
      page_token: '',
    };
  }

  const query = String(input.query || '').trim();

  // Discovery fallback: list Drive files and filter bitable/base-like items by name.
  const response = await listDriveFilesApi(client, input);
  const q = query.toLowerCase();
  const items = (response.items || [])
    .filter((file) => {
      const type = String(file.type || '').toLowerCase();
      const name = String(file.name || '').toLowerCase();
      const looksLikeBase = type.includes('bitable') || type.includes('base');
      return looksLikeBase && (!q || name.includes(q));
    })
    .map((file) => ({
      app_token: file.token,
      name: file.name,
      type: file.type,
      url: file.url,
    }));

  return {
    items,
    has_more: response.has_more,
    page_token: response.page_token,
  };
}

export async function listTablesApi(client, input) {
  const response = await client.bitable.v1.appTable.list({
    path: { app_token: input.app_token },
    params: {
      page_size: input.page_size,
      page_token: input.page_token,
    },
  });
  ensureSuccess(response, 'TABLE_LIST_FAILED');
  return {
    items: (response.data?.items || []).map(normalizeTable),
    has_more: Boolean(response.data?.has_more),
    page_token: response.data?.page_token || '',
    total: response.data?.total,
  };
}

export async function createTableApi(client, input) {
  const response = await client.bitable.v1.appTable.create({
    path: { app_token: input.app_token },
    data: {
      table: {
        name: input.table_name,
      },
    },
  });
  ensureSuccess(response, 'TABLE_CREATE_FAILED');
  return {
    table: normalizeTable(response.data?.table || response.data),
  };
}

export async function createFieldApi(client, input) {
  const payload = {
    field_name: input.field_name,
    type: input.field_type,
    property: input.property,
  };

  const response = await client.bitable.v1.appTableField.create({
    path: {
      app_token: input.app_token,
      table_id: input.table_id,
    },
    data: payload,
  }).catch((error) => {
    const responseData = error?.response?.data || error?.data || error?.body || error?.response || null;
    throw baseError('FIELD_CREATE_FAILED', error?.message || 'Failed to create field', {
      field_name: input.field_name,
      field_type: input.field_type,
      property: input.property,
      path: {
        app_token: input.app_token,
        table_id: input.table_id,
      },
      response: responseData,
      sdk_error: {
        message: error?.message,
        name: error?.name,
        code: error?.code,
        status: error?.status,
        response: error?.response,
        data: error?.data,
        body: error?.body,
      },
    });
  });
  ensureSuccess(response, 'FIELD_CREATE_FAILED', {
    field_name: input.field_name,
    field_type: input.field_type,
    property: input.property,
  });
  return normalizeField(response.data?.field || response.data);
}

export async function renameTableApi(client, input) {
  const response = await client.bitable.v1.appTable.patch({
    path: {
      app_token: input.app_token,
      table_id: input.table_id,
    },
    data: {
      name: input.table_name,
    },
  });
  ensureSuccess(response, 'TABLE_RENAME_FAILED');
  return {
    table: normalizeTable(response.data?.table || response.data),
  };
}

export async function deleteTableApi(client, input) {
  const response = await client.bitable.v1.appTable.delete({
    path: {
      app_token: input.app_token,
      table_id: input.table_id,
    },
  });
  ensureSuccess(response, 'TABLE_DELETE_FAILED');
  return {
    deleted: Boolean(response.data?.deleted ?? true),
    table_id: response.data?.table_id || input.table_id,
  };
}

export async function renameFieldApi(client, input) {
  const response = await client.bitable.v1.appTableField.update({
    path: {
      app_token: input.app_token,
      table_id: input.table_id,
      field_id: input.field_id,
    },
    data: {
      field_name: input.field_name,
      type: input.field_type,
      property: input.property,
    },
  });
  ensureSuccess(response, 'FIELD_RENAME_FAILED');
  return normalizeField(response.data?.field || response.data);
}

export async function updateFieldApi(client, input) {
  const data = {};
  if (typeof input.field_name === 'string' && input.field_name.trim()) data.field_name = input.field_name;
  if (typeof input.field_type === 'number') data.type = input.field_type;
  if (input.property && typeof input.property === 'object') data.property = input.property;
  if (Object.keys(data).length === 0) {
    throw baseError('INVALID_FIELD_UPDATE', 'update_field requires at least one of field_name, field_type, or property');
  }
  if (typeof data.field_name !== 'string' || !data.field_name.trim()) {
    throw baseError('INVALID_FIELD_UPDATE', 'update_field requires a resolved field_name');
  }
  if (typeof data.type !== 'number') {
    throw baseError('INVALID_FIELD_UPDATE', 'update_field requires a resolved field_type');
  }

  const response = await client.bitable.v1.appTableField.update({
    path: {
      app_token: input.app_token,
      table_id: input.table_id,
      field_id: input.field_id,
    },
    data,
  });
  ensureSuccess(response, 'FIELD_UPDATE_FAILED');
  return normalizeField(response.data?.field || response.data);
}

export async function deleteFieldApi(client, input) {
  const response = await client.bitable.v1.appTableField.delete({
    path: {
      app_token: input.app_token,
      table_id: input.table_id,
      field_id: input.field_id,
    },
  });
  ensureSuccess(response, 'FIELD_DELETE_FAILED');
  return {
    deleted: Boolean(response.data?.deleted ?? true),
    field_id: response.data?.field_id || input.field_id,
  };
}

export async function listRawFieldsApi(client, input) {
  const response = await client.bitable.v1.appTableField.list({
    path: { app_token: input.app_token, table_id: input.table_id },
    params: { page_size: 500 },
  });
  ensureSuccess(response, 'FIELD_LIST_FAILED');
  return response.data?.items || [];
}

export async function getTableApi(client, input) {
  const [tableResp, fieldResp, viewResp] = await Promise.all([
    client.bitable.v1.appTable.list({ path: { app_token: input.app_token }, params: { page_size: 500 } }),
    client.bitable.v1.appTableField.list({ path: { app_token: input.app_token, table_id: input.table_id }, params: { page_size: 500 } }),
    client.bitable.v1.appTableView.list({ path: { app_token: input.app_token, table_id: input.table_id }, params: { page_size: 500 } }).catch(() => ({ data: { items: [] } })),
  ]);

  ensureSuccess(tableResp, 'TABLE_LIST_FAILED');
  ensureSuccess(fieldResp, 'FIELD_LIST_FAILED');

  const table = (tableResp.data?.items || []).find((item) => item.table_id === input.table_id);
  if (!table) {
    throw baseError('TABLE_NOT_FOUND', `Table '${input.table_id}' not found`, { table_id: input.table_id });
  }

  return {
    table: normalizeTable(table),
    fields: (fieldResp.data?.items || []).map(normalizeField),
    views: (viewResp.data?.items || []).map(normalizeView),
  };
}

export async function getRecordApi(client, input) {
  const response = await client.bitable.v1.appTableRecord.get({
    path: {
      app_token: input.app_token,
      table_id: input.table_id,
      record_id: input.record_id,
    },
    params: {
      user_id_type: 'open_id',
      automatic_fields: true,
    },
  });
  ensureSuccess(response, 'RECORD_GET_FAILED');
  return normalizeRecord(response.data?.record);
}

export async function queryRecordsApi(client, input) {
  const useSearch = Boolean(input.compiledFilter || (input.sort && input.sort.length) || (input.fields && input.fields.length));

  if (useSearch) {
    const response = await client.bitable.v1.appTableRecord.search({
      path: {
        app_token: input.app_token,
        table_id: input.table_id,
      },
      params: {
        user_id_type: 'open_id',
        page_size: input.page_size,
        page_token: input.page_token,
      },
      data: {
        view_id: input.view_id,
        field_names: input.fields,
        sort: (input.sort || []).map((item) => ({ field_name: item.field, desc: item.order === 'desc' })),
        filter: input.compiledFilter,
        automatic_fields: true,
      },
    });
    ensureSuccess(response, 'RECORD_SEARCH_FAILED');
    return {
      items: (response.data?.items || []).map(normalizeRecord),
      has_more: Boolean(response.data?.has_more),
      page_token: response.data?.page_token || '',
      total_returned: (response.data?.items || []).length,
      total: response.data?.total,
    };
  }

  const response = await client.bitable.v1.appTableRecord.list({
    path: {
      app_token: input.app_token,
      table_id: input.table_id,
    },
    params: {
      view_id: input.view_id,
      page_size: input.page_size,
      page_token: input.page_token,
      user_id_type: 'open_id',
      automatic_fields: true,
    },
  });
  ensureSuccess(response, 'RECORD_LIST_FAILED');
  return {
    items: (response.data?.items || []).map(normalizeRecord),
    has_more: Boolean(response.data?.has_more),
    page_token: response.data?.page_token || '',
    total_returned: (response.data?.items || []).length,
    total: response.data?.total,
  };
}

export async function createRecordsApi(client, input) {
  const records = input.records || [];
  if (records.length === 1) {
    const response = await client.bitable.v1.appTableRecord.create({
      path: { app_token: input.app_token, table_id: input.table_id },
      params: { user_id_type: 'open_id' },
      data: { fields: records[0].fields },
    });
    ensureSuccess(response, 'RECORD_CREATE_FAILED');
    return { items: [normalizeRecord(response.data?.record)] };
  }

  const response = await client.bitable.v1.appTableRecord.batchCreate({
    path: { app_token: input.app_token, table_id: input.table_id },
    params: { user_id_type: 'open_id' },
    data: { records },
  });
  ensureSuccess(response, 'RECORD_BATCH_CREATE_FAILED');
  return { items: (response.data?.records || []).map(normalizeRecord) };
}

export async function updateRecordsApi(client, input) {
  const records = input.records || [];
  if (records.length === 1) {
    const record = records[0];
    const response = await client.bitable.v1.appTableRecord.update({
      path: { app_token: input.app_token, table_id: input.table_id, record_id: record.record_id },
      params: { user_id_type: 'open_id' },
      data: { fields: record.fields },
    });
    ensureSuccess(response, 'RECORD_UPDATE_FAILED');
    return { items: [normalizeRecord(response.data?.record)] };
  }

  const response = await client.bitable.v1.appTableRecord.batchUpdate({
    path: { app_token: input.app_token, table_id: input.table_id },
    params: { user_id_type: 'open_id' },
    data: { records },
  });
  ensureSuccess(response, 'RECORD_BATCH_UPDATE_FAILED');
  return { items: (response.data?.records || []).map(normalizeRecord) };
}

export async function deleteRecordsApi(client, input) {
  const recordIds = input.record_ids || [];
  if (recordIds.length === 1) {
    const response = await client.bitable.v1.appTableRecord.delete({
      path: {
        app_token: input.app_token,
        table_id: input.table_id,
        record_id: recordIds[0],
      },
    });
    ensureSuccess(response, 'RECORD_DELETE_FAILED');
    return {
      deleted_count: response.data?.deleted ? 1 : 0,
      record_ids: response.data?.record_id ? [response.data.record_id] : recordIds,
    };
  }

  const response = await client.bitable.v1.appTableRecord.batchDelete({
    path: { app_token: input.app_token, table_id: input.table_id },
    data: { records: recordIds },
  });
  ensureSuccess(response, 'RECORD_BATCH_DELETE_FAILED');
  const deleted = (response.data?.records || []).filter((item) => item.deleted).map((item) => item.record_id).filter(Boolean);
  return {
    deleted_count: deleted.length,
    record_ids: deleted,
  };
}

function ensureSuccess(response, fallbackCode) {
  if (!response || typeof response.code === 'number' && response.code !== 0) {
    throw baseError(fallbackCode, response?.msg || 'Feishu API request failed', {
      response: response ? {
        code: response.code,
        msg: response.msg,
        data: response.data,
      } : null,
    });
  }
}

function normalizeApp(app = {}) {
  return {
    app_token: app.app_token,
    name: app.name,
    revision: app.revision,
  };
}

function normalizeTable(table = {}) {
  return {
    table_id: table.table_id,
    name: table.name,
    revision: table.revision,
  };
}

function normalizeField(field = {}) {
  return {
    field_id: field.field_id,
    field_name: field.field_name,
    name: field.field_name,
    type: field.ui_type || field.type,
    ui_type: field.ui_type,
    property: field.property,
    required: false,
    multiple: Boolean(field.property?.multiple),
    is_primary: Boolean(field.is_primary),
    is_hidden: Boolean(field.is_hidden),
  };
}

function normalizeView(view = {}) {
  return {
    view_id: view.view_id,
    name: view.view_name || view.name,
    type: view.view_type,
  };
}

function normalizeRecord(record = {}) {
  return {
    record_id: record.record_id,
    fields: record.fields || {},
  };
}

async function parseFeishuBaseUrl(client, url) {
  let parsed;
  try {
    parsed = new URL(url);
  } catch {
    throw baseError('LINK_PARSE_FAILED', 'Invalid URL', { url });
  }

  const direct = parseBaseTokensFromText(`${parsed.pathname}${parsed.hash}${parsed.search}`);
  if (direct.app_token) {
    return {
      url,
      ...direct,
    };
  }

  const wikiMatch = parsed.pathname.match(/^\/wiki\/([A-Za-z0-9_]+)/);
  if (!wikiMatch) {
    return {
      url,
      ...direct,
    };
  }

  const wiki_token = wikiMatch[1];
  const resolved = await resolveWikiBaseLink(client, wiki_token, url);
  const merged = {
    ...resolved,
    table_id: direct.table_id || resolved.table_id,
    view_id: direct.view_id || resolved.view_id,
  };

  return {
    url,
    wiki_token,
    ...merged,
  };
}

function parseBaseTokensFromText(text) {
  const appTokenMatch = text.match(/\b(?:app|base|bitable)\/([A-Za-z0-9_]+)|\b(bascn[A-Za-z0-9_]+)\b/);
  const tableMatch = text.match(/\b(tbl[A-Za-z0-9_]+)\b/);
  const viewMatch = text.match(/\b(vew[A-Za-z0-9_]+)\b/);

  return {
    app_token: appTokenMatch?.[1] || appTokenMatch?.[2],
    table_id: tableMatch?.[1],
    view_id: viewMatch?.[1],
  };
}

async function resolveWikiBaseLink(client, wikiToken, originalUrl) {
  const attempts = [];
  const candidates = [];

  const addCandidate = (value) => {
    if (!value || typeof value !== 'object') return;
    candidates.push(value);
  };

  try {
    const response = await client.wiki.space.getNode({ params: { token: wikiToken } });
    ensureSuccess(response, 'WIKI_RESOLVE_FAILED');
    addCandidate(response?.data);
    addCandidate(response?.data?.node);
  } catch (error) {
    attempts.push({
      method: 'wiki.space.getNode',
      message: error?.message,
      response: error?.response?.data || error?.data || null,
    });
  }

  try {
    const response = await client.wiki.spaceNode.list({ params: { parent_node_token: wikiToken, page_size: 50 } });
    ensureSuccess(response, 'WIKI_RESOLVE_FAILED');
    for (const item of response?.data?.items || []) addCandidate(item);
  } catch (error) {
    attempts.push({
      method: 'wiki.spaceNode.list',
      message: error?.message,
      response: error?.response?.data || error?.data || null,
    });
  }

  for (const candidate of candidates) {
    const token = extractBaseAppTokenFromWikiCandidate(candidate);
    const ids = parseBaseTokensFromText(JSON.stringify(candidate));
    if (token || ids.app_token) {
      return {
        app_token: token || ids.app_token,
        table_id: ids.table_id,
        view_id: ids.view_id,
        wiki_resolved: true,
      };
    }
  }

  throw baseError('WIKI_RESOLVE_FAILED', 'Could not resolve wiki link to underlying Feishu Base app_token', {
    url: originalUrl,
    wiki_token: wikiToken,
    attempts,
    candidate_count: candidates.length,
  });
}

function extractBaseAppTokenFromWikiCandidate(candidate) {
  const possibleValues = [
    candidate?.obj_token,
    candidate?.token,
    candidate?.app_token,
    candidate?.origin_node_token,
    candidate?.origin_space_id,
    candidate?.url,
    candidate?.obj_url,
    candidate?.node_url,
    candidate?.origin_url,
    candidate?.shortcut?.url,
    candidate?.shortcut?.obj_url,
    candidate?.shortcut?.token,
  ];

  for (const value of possibleValues) {
    const ids = parseBaseTokensFromText(String(value || ''));
    if (ids.app_token) return ids.app_token;
    if (typeof value === 'string' && /^bascn[A-Za-z0-9_]+$/.test(value)) return value;
  }

  const objType = String(candidate?.obj_type || candidate?.type || '').toLowerCase();
  if ((objType.includes('bitable') || objType.includes('base')) && typeof candidate?.obj_token === 'string') {
    return candidate.obj_token;
  }

  return undefined;
}

function escapeDriveQuery(value) {
  return String(value).replace(/\\/g, '\\\\').replace(/\"/g, '\\\"');
}
