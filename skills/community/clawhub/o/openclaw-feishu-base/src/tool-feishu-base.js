import { Type } from '@sinclair/typebox';
import { z } from 'zod';
import { createFeishuClient } from './client.js';
import { resolvePluginConfig, resolveFeishuAccountConfig } from './config.js';
import { normalizeError } from './errors.js';
import {
  resolveLink,
  listBases,
  listFolder,
  findTable,
  listTables,
  discoverTables,
  createTable,
  renameTable,
  deleteTable,
  createField,
  renameField,
  updateField,
  deleteField,
  getTable,
  getRecord,
  queryRecords,
  createRecords,
  updateRecords,
  upsertRecords,
  deleteRecords,
  uploadAttachment,
  cloneAttachment,
  buildAttachmentFieldValue,
} from './base/service.js';
import { FilterSchema } from './base/filters.js';

const RecordFieldsSchema = z.record(z.string(), z.unknown());
const SortSchema = z.object({ field: z.string().min(1), order: z.enum(['asc', 'desc']).default('asc') });
const CreateRecordSchema = z.object({ fields: RecordFieldsSchema });
const UpdateRecordSchema = z.object({ record_id: z.string().min(1), fields: RecordFieldsSchema });
const LinkFieldSchema = z.object({
  table_id: z.string().min(1).optional(),
  table_name: z.string().min(1).optional(),
  multiple: z.boolean().optional(),
  back_field_name: z.string().min(1).optional(),
}).refine((value) => Boolean(value.table_id || value.table_name), { message: 'link requires table_id or table_name' });

const CreateFieldSchema = z.object({
  field_name: z.string().min(1),
  field_type: z.number().int().min(1),
  property: z.record(z.string(), z.unknown()).optional(),
  link: LinkFieldSchema.optional(),
});

const AttachmentObjectSchema = z.object({
  file_token: z.string().min(1),
  name: z.string().optional(),
  type: z.string().optional(),
  size: z.number().int().nonnegative().optional(),
  url: z.string().optional(),
  tmp_url: z.string().optional(),
});

const BaseActionSchema = z.union([
  z.object({ action: z.literal('resolve_link'), url: z.string().min(1) }),
  z.object({ action: z.literal('list_bases'), account_id: z.string().optional(), app_token: z.string().optional(), query: z.string().optional(), page_size: z.number().int().min(1).max(500).optional(), page_token: z.string().optional() }),
  z.object({ action: z.literal('list_folder'), account_id: z.string().optional(), folder_token: z.string().min(1), page_size: z.number().int().min(1).max(500).optional(), page_token: z.string().optional() }),
  z.object({ action: z.literal('find_table'), account_id: z.string().optional(), base_name: z.string().min(1), table_name: z.string().optional() }),
  z.object({ action: z.literal('list_tables'), account_id: z.string().optional(), app_token: z.string().min(1), page_size: z.number().int().min(1).max(500).optional(), page_token: z.string().optional() }),
  z.object({
    action: z.literal('discover_tables'),
    account_id: z.string().optional(),
    query: z.string().optional(),
    base_query: z.string().optional(),
    app_tokens: z.array(z.string().min(1)).optional(),
    page_size: z.number().int().min(1).max(500).optional(),
  }),
  z.object({ action: z.literal('create_table'), account_id: z.string().optional(), app_token: z.string().min(1), table_name: z.string().min(1), fields: z.array(CreateFieldSchema).optional() }),
  z.object({ action: z.literal('rename_table'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), table_name: z.string().min(1).optional(), new_name: z.string().min(1).optional() }).refine((value) => Boolean(value.table_name || value.new_name), { message: 'rename_table requires table_name or new_name' }),
  z.object({ action: z.literal('delete_table'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1) }),
  z.object({ action: z.literal('create_field'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), field_name: z.string().min(1), field_type: z.number().int().min(1), property: z.record(z.string(), z.unknown()).optional(), link: LinkFieldSchema.optional() }),
  z.object({ action: z.literal('rename_field'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), field_id: z.string().min(1), field_name: z.string().min(1) }),
  z.object({ action: z.literal('update_field'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), field_id: z.string().min(1), field_name: z.string().optional(), field_type: z.number().int().min(1).optional(), property: z.record(z.string(), z.unknown()).optional() }),
  z.object({ action: z.literal('delete_field'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), field_id: z.string().min(1) }),
  z.object({ action: z.literal('get_table'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1) }),
  z.object({ action: z.literal('get_record'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), record_id: z.string().min(1) }),
  z.object({ action: z.literal('query_records'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), view_id: z.string().optional(), filter: FilterSchema.optional(), sort: z.array(SortSchema).optional(), fields: z.array(z.string()).optional(), page_size: z.number().int().min(1).max(500).optional(), page_token: z.string().optional() }),
  z.object({ action: z.literal('create_records'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), records: z.array(CreateRecordSchema).min(1) }),
  z.object({ action: z.literal('update_records'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), records: z.array(UpdateRecordSchema).min(1) }),
  z.object({ action: z.literal('upsert_records'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), match: z.object({ field: z.string().min(1) }), records: z.array(CreateRecordSchema).min(1) }),
  z.object({ action: z.literal('delete_records'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), record_ids: z.array(z.string().min(1)).min(1) }),
  z.object({ action: z.literal('delete_records'), account_id: z.string().optional(), app_token: z.string().min(1), table_id: z.string().min(1), filter: FilterSchema }),
  z.object({ action: z.literal('upload_attachment'), account_id: z.string().optional(), app_token: z.string().min(1), file_path: z.string().optional(), url: z.string().optional(), filename: z.string().optional(), mime_type: z.string().optional(), upload_kind: z.enum(['file', 'media']).optional() }).refine((value) => Boolean(value.file_path || value.url), { message: 'upload_attachment requires file_path or url' }),
  z.object({ action: z.literal('clone_attachment'), account_id: z.string().optional(), app_token: z.string().min(1), file_path: z.string().optional(), url: z.string().optional(), filename: z.string().optional(), mime_type: z.string().optional(), upload_kind: z.enum(['file', 'media']).optional(), source_attachment: AttachmentObjectSchema.optional() }).refine((value) => Boolean(value.file_path || value.url || value.source_attachment?.tmp_url || value.source_attachment?.url), { message: 'clone_attachment requires file_path, url, or source_attachment with tmp_url/url' }),
  z.object({ action: z.literal('build_attachment_field_value'), account_id: z.string().optional(), attachments: z.array(z.union([z.string().min(1), AttachmentObjectSchema])).min(1).optional(), attachment: AttachmentObjectSchema.optional() }).refine((value) => Boolean((value.attachments && value.attachments.length) || value.attachment), { message: 'build_attachment_field_value requires attachments or attachment' }),
]);

export const feishuBaseParameters = Type.Object({
  action: Type.String(),
}, { additionalProperties: true });

function safeStringify(value) {
  const seen = new WeakSet();
  return JSON.stringify(value, (key, current) => {
    if (typeof current === 'object' && current !== null) {
      if (seen.has(current)) return '[Circular]';
      seen.add(current);
    }
    return current;
  }, 2);
}

export function registerFeishuBaseTool(api) {
  const pluginCfg = resolvePluginConfig(api.pluginConfig || {});
  const debugLog = (...args) => {
    if (!pluginCfg.debug) return;
    try {
      console.log(...args);
    } catch {}
  };
  debugLog('[openclaw-feishu-base] registering feishu_base tool');
  api.registerTool((ctx = {}) => ({
    name: 'feishu_base',
    description: 'Feishu Base/Bitable schema, search, create, update, upsert, and optional delete operations.',
    parameters: feishuBaseParameters,
    async execute(_id, params) {
      try {
        const parsed = BaseActionSchema.parse(params);
        const runtimeLike = {
          ...api,
          accountId: ctx?.agentAccountId || ctx?.accountId || api?.accountId,
          account_id: ctx?.agentAccountId || ctx?.account_id || api?.account_id,
          toolContext: ctx,
        };
        const accountCfg = resolveFeishuAccountConfig(runtimeLike, pluginCfg, parsed.account_id);
        debugLog('[openclaw-feishu-base] execute', JSON.stringify({
          action: parsed.action,
          requestedAccountId: parsed.account_id,
          resolvedAccountId: accountCfg.accountId,
          appId: accountCfg.appId,
          domain: accountCfg.domain,
          agentAccountId: ctx?.agentAccountId,
          contextAccountId: ctx?.accountId,
          debug: accountCfg._debug,
        }));
        const client = createFeishuClient(accountCfg);
        const limits = {
          allowDelete: pluginCfg.allowDelete,
          maxPageSize: pluginCfg.maxPageSize,
          maxBatchWrite: pluginCfg.maxBatchWrite,
          maxBatchDelete: pluginCfg.maxBatchDelete,
        };
        const input = { ...parsed, _limits: limits };

        let result;
        switch (parsed.action) {
          case 'resolve_link': result = await resolveLink(client, input); break;
          case 'list_bases': result = await listBases(client, input); break;
          case 'list_folder': result = await listFolder(client, input); break;
          case 'find_table': result = await findTable(client, input); break;
          case 'list_tables': result = await listTables(client, input); break;
          case 'discover_tables': result = await discoverTables(client, input); break;
          case 'create_table': result = await createTable(client, input); break;
          case 'rename_table': result = await renameTable(client, input); break;
          case 'delete_table': result = await deleteTable(client, input); break;
          case 'create_field': result = await createField(client, input); break;
          case 'rename_field': result = await renameField(client, input); break;
          case 'update_field': result = await updateField(client, input); break;
          case 'delete_field': result = await deleteField(client, input); break;
          case 'get_table': result = await getTable(client, input); break;
          case 'get_record': result = await getRecord(client, input); break;
          case 'query_records': result = await queryRecords(client, input); break;
          case 'create_records': result = await createRecords(client, input); break;
          case 'update_records': result = await updateRecords(client, input); break;
          case 'upsert_records': result = await upsertRecords(client, input); break;
          case 'delete_records': result = await deleteRecords(client, input); break;
          case 'upload_attachment': result = await uploadAttachment(client, input); break;
          case 'clone_attachment': result = await cloneAttachment(client, input); break;
          case 'build_attachment_field_value': result = await buildAttachmentFieldValue(client, input); break;
          default: throw new Error(`Unsupported action: ${parsed.action}`);
        }

        return {
          content: [
            {
              type: 'text',
              text: safeStringify(result),
            },
          ],
        };
      } catch (error) {
        const normalized = normalizeError(error);
        return {
          content: [
            {
              type: 'text',
              text: safeStringify({
                error: {
                  code: normalized.code,
                  message: normalized.message,
                  details: normalized.details,
                },
              }),
            },
          ],
          isError: true,
        };
      }
    },
  }), { name: 'feishu_base' });
}
