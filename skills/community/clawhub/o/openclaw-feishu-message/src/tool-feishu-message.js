import { Type } from '@sinclair/typebox';
import { z } from 'zod';
import { createFeishuClient } from './client.js';
import { resolvePluginConfig, resolveFeishuAccountConfig } from './config.js';
import { normalizeError, messageError } from './errors.js';
import { getCachedContact, putCachedContact } from './cache.js';

const ReceiveIdTypeSchema = z.enum(['open_id', 'user_id', 'union_id', 'email', 'chat_id']);

const MessageActionSchema = z.union([
  z.object({
    action: z.literal('search_employee'),
    account_id: z.string().optional(),
    query: z.string().min(1).optional(),
    email: z.string().email().optional(),
    mobile: z.string().min(3).optional(),
    exact_name: z.string().min(1).optional(),
    verbose: z.boolean().optional(),
    limit: z.number().int().min(1).max(50).optional(),
  }).refine((v) => Boolean(v.query || v.email || v.mobile || v.exact_name), {
    message: 'search_employee requires query, email, mobile, or exact_name',
  }),
  z.object({
    action: z.literal('lookup_employee'),
    account_id: z.string().optional(),
    email: z.string().email().optional(),
    mobile: z.string().min(3).optional(),
    exact_name: z.string().min(1).optional(),
    limit: z.number().int().min(1).max(50).optional(),
  }).refine((v) => Boolean(v.email || v.mobile || v.exact_name), {
    message: 'lookup_employee requires email, mobile, or exact_name',
  }),
  z.object({
    action: z.literal('find_contact'),
    account_id: z.string().optional(),
    query: z.string().min(1),
    limit: z.number().int().min(1).max(50).optional(),
  }),
  z.object({
    action: z.literal('create_p2p_chat'),
    account_id: z.string().optional(),
    user_ids: z.array(z.string().min(1)).min(1),
  }),
  z.object({
    action: z.literal('send_message'),
    account_id: z.string().optional(),
    receive_id: z.string().min(1),
    receive_id_type: ReceiveIdTypeSchema.optional(),
    name: z.string().min(1).optional(),
    email: z.string().email().optional(),
    mobile: z.string().min(3).optional(),
    user_id: z.string().min(1).optional(),
    open_id: z.string().min(1).optional(),
    union_id: z.string().min(1).optional(),
    msg_type: z.enum(['text', 'post']).default('text'),
    content: z.string().min(1),
  }),
  z.object({
    action: z.literal('send_followup'),
    account_id: z.string().optional(),
    target: z.object({
      user_id: z.string().min(1).optional(),
      open_id: z.string().min(1).optional(),
      union_id: z.string().min(1).optional(),
      email: z.string().email().optional(),
      chat_id: z.string().min(1).optional(),
      name: z.string().min(1).optional(),
    }).refine((v) => Boolean(v.user_id || v.open_id || v.union_id || v.email || v.chat_id || v.name), {
      message: 'target requires at least one identifier',
    }),
    work_item: z.string().min(1),
    status_prompt: z.string().optional(),
    polite: z.boolean().optional(),
    signature: z.string().optional(),
    dry_run: z.boolean().optional(),
  }),
  z.object({
    action: z.literal('send_contact_message'),
    account_id: z.string().optional(),
    target: z.object({
      user_id: z.string().min(1).optional(),
      open_id: z.string().min(1).optional(),
      union_id: z.string().min(1).optional(),
      email: z.string().email().optional(),
      chat_id: z.string().min(1).optional(),
      name: z.string().min(1).optional(),
      mobile: z.string().min(3).optional(),
    }).refine((v) => Boolean(v.user_id || v.open_id || v.union_id || v.email || v.chat_id || v.name || v.mobile), {
      message: 'target requires at least one identifier',
    }),
    content: z.string().min(1),
    msg_type: z.enum(['text', 'post']).default('text'),
    dry_run: z.boolean().optional(),
  }),
]);

export const feishuMessageParameters = Type.Object({
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

function buildTextContent(text) {
  return JSON.stringify({ text });
}

function buildFollowupText({ name, work_item, status_prompt, polite = true, signature }) {
  const greeting = name ? `Hi ${name},` : 'Hi,';
  const ask = status_prompt || `just following up on ${work_item}. Could you share the current status when convenient?`;
  const closing = polite ? 'Thanks.' : '';
  return [greeting, ask, closing, signature || ''].filter(Boolean).join('\n\n');
}

function normalizeSearchItems(payload) {
  const items = payload?.items || payload?.user_list || payload?.users || payload?.employees || payload?.employee_list || [];
  return Array.isArray(items) ? items : [];
}

function pickName(item) {
  return item?.name || item?.en_name || item?.display_name || item?.nickname || null;
}

function pickEmail(item) {
  return item?.email || item?.enterprise_email || item?.email_address || null;
}

function pickMobile(item) {
  return item?.mobile || item?.phone || item?.mobile_phone || null;
}

function exactMatchEmployees(items, { email, mobile, exact_name }) {
  return items.filter((item) => {
    if (email && String(pickEmail(item) || '').toLowerCase() !== String(email).toLowerCase()) return false;
    if (mobile) {
      const left = String(pickMobile(item) || '').replace(/[^+\d]/g, '');
      const right = String(mobile).replace(/[^+\d]/g, '');
      if (!left.includes(right)) return false;
    }
    if (exact_name && String(pickName(item) || '').trim().toLowerCase() !== String(exact_name).trim().toLowerCase()) return false;
    return true;
  });
}

function summarizeEmployee(item) {
  return {
    name: pickName(item),
    open_id: item?.open_id || null,
    user_id: item?.user_id || null,
    union_id: item?.union_id || null,
    email: pickEmail(item),
    mobile: pickMobile(item),
    department_ids: item?.department_ids || item?.department_id || null,
    title: item?.job_title || item?.title || null,
    raw: item,
  };
}

function broadMatchEmployees(items, { query, email, mobile, exact_name }) {
  const q = String(query || '').trim().toLowerCase();
  return items.filter((item) => {
    const name = String(pickName(item) || '').toLowerCase();
    const itemEmail = String(pickEmail(item) || '').toLowerCase();
    const itemMobile = String(pickMobile(item) || '').replace(/[^+\d]/g, '');

    if (email && itemEmail !== String(email).toLowerCase()) return false;
    if (mobile) {
      const right = String(mobile).replace(/[^+\d]/g, '');
      if (!itemMobile.includes(right)) return false;
    }
    if (exact_name && name !== String(exact_name).trim().toLowerCase()) return false;
    if (q && !(name.includes(q) || itemEmail.includes(q) || itemMobile.includes(q.replace(/[^+\d]/g, '')))) return false;
    return true;
  });
}

async function searchEmployees(client, criteria = {}, limit = 10) {
  const attempts = [];

  if (criteria.query || criteria.exact_name || criteria.email || criteria.mobile) {
    attempts.push(async () => {
      if (!client?.directory?.v1?.employee?.search) {
        throw new Error('client.directory.v1.employee.search is unavailable');
      }
      const query = criteria.query || criteria.exact_name || criteria.email || criteria.mobile;
      return await client.directory.v1.employee.search({
        data: {
          query,
          page_request: {
            page_size: Math.min(limit, 50),
          },
          required_fields: [
            'name',
            'en_name',
            'email',
            'mobile',
            'open_id',
            'user_id',
            'union_id',
            'department_ids',
            'job_title'
          ],
        },
      });
    });
  }

  attempts.push(async () => {
    if (!client?.contact?.user?.findByDepartment) {
      throw new Error('client.contact.user.findByDepartment is unavailable');
    }
    return await client.contact.user.findByDepartment({
      params: { department_id: '0', page_size: Math.min(Math.max(limit, 20), 100) },
    });
  });

  attempts.push(async () => {
    if (!client?.contact?.user?.list) {
      throw new Error('client.contact.user.list is unavailable');
    }
    return await client.contact.user.list({
      params: { page_size: Math.min(limit, 50) },
    });
  });

  let lastError;
  for (const attempt of attempts) {
    try {
      const res = await attempt();
      const data = res?.data || res;
      const items = normalizeSearchItems(data);
      const filtered = broadMatchEmployees(items, criteria);
      const hasAbnormals = Array.isArray(data?.abnormals) && data.abnormals.length > 0;

      if (filtered.length === 0 && (hasAbnormals || items.length === 0)) {
        lastError = new Error('Search source returned no usable matches, trying fallback');
        continue;
      }

      return {
        ...data,
        items: filtered,
      };
    } catch (error) {
      lastError = error;
    }
  }

  throw lastError || new Error('Employee search failed');
}

async function createP2PChat(client, userIds) {
  const attempts = [
    async () => await client.im.v1.chat.create({
      data: {
        user_id_list: userIds,
        chat_mode: 'p2p',
      },
    }),
    async () => await client.im.v1.chat.create({
      data: {
        chat_type: 'p2p',
        user_id_list: userIds,
      },
    }),
  ];

  let lastError;
  for (const attempt of attempts) {
    try {
      const res = await attempt();
      return res?.data || res;
    } catch (error) {
      lastError = error;
    }
  }

  throw lastError || new Error('P2P chat creation failed');
}

async function sendMessage(client, { receive_id, receive_id_type, msg_type, content }) {
  const res = await client.im.v1.message.create({
    params: { receive_id_type },
    data: {
      receive_id,
      msg_type,
      content: msg_type === 'text' ? buildTextContent(content) : content,
    },
  });
  return res?.data || res;
}

async function sendMessageWithFallback(client, target, message) {
  try {
    const primary = await sendMessage(client, {
      receive_id: target.receive_id,
      receive_id_type: target.receive_id_type,
      msg_type: message.msg_type,
      content: message.content,
    });
    return {
      sent_via: { receive_id: target.receive_id, receive_id_type: target.receive_id_type },
      result: primary,
    };
  } catch (error) {
    const text = String(error?.message || '');
    const details = JSON.stringify(error?.response?.data || error?.data || error?.body || {});
    const crossApp = /cross app/i.test(text) || /cross app/i.test(details) || /open_id/i.test(details) && /cross/i.test(details);
    if (crossApp && target.user_id && target.receive_id_type === 'open_id') {
      const fallback = await sendMessage(client, {
        receive_id: target.user_id,
        receive_id_type: 'user_id',
        msg_type: message.msg_type,
        content: message.content,
      });
      return {
        sent_via: { receive_id: target.user_id, receive_id_type: 'user_id', fallback_from: 'open_id' },
        result: fallback,
      };
    }
    throw error;
  }
}

function cacheResolvedTarget(target = {}) {
  const existing = getCachedContact({
    open_id: target.receive_id_type === 'open_id' ? target.receive_id : target.open_id,
    user_id: target.receive_id_type === 'user_id' ? target.receive_id : target.user_id,
    union_id: target.receive_id_type === 'union_id' ? target.receive_id : target.union_id,
    email: target.email,
    mobile: target.mobile,
    name: target.name,
  });

  const cacheable = {
    name: target.name || existing?.name || null,
    open_id: target.receive_id_type === 'open_id' ? target.receive_id : (target.open_id || existing?.open_id || null),
    user_id: target.receive_id_type === 'user_id' ? target.receive_id : (target.user_id || existing?.user_id || null),
    union_id: target.receive_id_type === 'union_id' ? target.receive_id : (target.union_id || existing?.union_id || null),
    email: target.email || existing?.email || null,
    mobile: target.mobile || existing?.mobile || null,
  };

  if (cacheable.name || cacheable.open_id || cacheable.user_id || cacheable.union_id || cacheable.email || cacheable.mobile) {
    return putCachedContact(cacheable);
  }
  return null;
}

function pickTargetIdentifier(target, defaultReceiveIdType = 'open_id') {
  if (target.chat_id) return { receive_id: target.chat_id, receive_id_type: 'chat_id', resolvedName: target.name };
  if (target.open_id) return { receive_id: target.open_id, receive_id_type: 'open_id', resolvedName: target.name, open_id: target.open_id };
  if (target.user_id) return { receive_id: target.user_id, receive_id_type: 'user_id', resolvedName: target.name, user_id: target.user_id };
  if (target.union_id) return { receive_id: target.union_id, receive_id_type: 'union_id', resolvedName: target.name, union_id: target.union_id };
  return { receive_id: null, receive_id_type: defaultReceiveIdType, resolvedName: target.name };
}

export function registerFeishuMessageTool(api) {
  const pluginCfg = resolvePluginConfig(api.pluginConfig || {});
  const debugLog = (...args) => {
    if (!pluginCfg.debug) return;
    try {
      console.log(...args);
    } catch {}
  };

  api.registerTool((ctx = {}) => ({
    name: 'feishu_message',
    description: 'Search employees, create Feishu/Lark chats, and send bot follow-up messages.',
    parameters: feishuMessageParameters,
    async execute(_id, params) {
      try {
        if (!pluginCfg.enabled) {
          throw messageError('PLUGIN_DISABLED', 'openclaw-feishu-message is disabled by config');
        }

        const parsed = MessageActionSchema.parse(params);
        const runtimeLike = {
          ...api,
          accountId: ctx?.agentAccountId || ctx?.accountId || api?.accountId,
          account_id: ctx?.agentAccountId || ctx?.account_id || api?.account_id,
          toolContext: ctx,
        };
        const accountCfg = resolveFeishuAccountConfig(runtimeLike, pluginCfg, parsed.account_id);
        const client = createFeishuClient(accountCfg);

        debugLog('[openclaw-feishu-message] execute', JSON.stringify({
          action: parsed.action,
          requestedAccountId: parsed.account_id,
          resolvedAccountId: accountCfg.accountId,
        }));

        let result;
        switch (parsed.action) {
          case 'search_employee': {
            const search = await searchEmployees(client, {
              query: parsed.query,
              email: parsed.email,
              mobile: parsed.mobile,
              exact_name: parsed.exact_name,
            }, parsed.limit || 10);
            const summarizedItems = normalizeSearchItems(search).map(summarizeEmployee);
            if (summarizedItems.length === 1) {
              const cachedItem = putCachedContact(summarizedItems[0]);
              summarizedItems[0] = cachedItem;
            }
            result = {
              ...search,
              count: summarizedItems.length,
              item: summarizedItems.length === 1 ? summarizedItems[0] : null,
              items: summarizedItems,
            };
            break;
          }
          case 'lookup_employee': {
            const cached = getCachedContact({
              email: parsed.email,
              mobile: parsed.mobile,
              name: parsed.exact_name,
            });
            if (cached) {
              result = { count: 1, item: cached, items: [cached], cached: true };
              break;
            }

            const search = await searchEmployees(client, {
              email: parsed.email,
              mobile: parsed.mobile,
              exact_name: parsed.exact_name,
            }, parsed.limit || 10);
            const items = normalizeSearchItems(search).map(summarizeEmployee);
            let singleItem = items.length === 1 ? items[0] : null;
            if (singleItem) {
              singleItem = putCachedContact(singleItem);
              items[0] = singleItem;
            }
            result = {
              count: items.length,
              item: singleItem,
              items,
            };
            break;
          }
          case 'find_contact': {
            const cached = getCachedContact({ name: parsed.query, email: parsed.query, mobile: parsed.query });
            if (cached) {
              result = { count: 1, item: cached, items: [cached], cached: true };
              break;
            }

            const search = await searchEmployees(client, {
              query: parsed.query,
              exact_name: parsed.query,
              email: parsed.query.includes('@') ? parsed.query : undefined,
              mobile: /\d/.test(parsed.query) ? parsed.query : undefined,
            }, parsed.limit || 10);
            const items = normalizeSearchItems(search).map(summarizeEmployee);
            let singleItem = items.length === 1 ? items[0] : null;
            if (singleItem) {
              singleItem = putCachedContact({
                ...singleItem,
                name: singleItem.name || parsed.query,
                email: singleItem.email || (parsed.query.includes('@') ? parsed.query : null),
                mobile: singleItem.mobile || (/\d/.test(parsed.query) ? parsed.query : null),
              });
              items[0] = singleItem;
            }
            result = {
              count: items.length,
              item: singleItem,
              items,
            };
            break;
          }
          case 'create_p2p_chat': {
            result = await createP2PChat(client, parsed.user_ids);
            break;
          }
          case 'send_message': {
            if (!pluginCfg.allowSend) {
              throw messageError('SEND_DISABLED', 'Sending is disabled by plugin config');
            }
            const sendTarget = {
              receive_id: parsed.receive_id,
              receive_id_type: parsed.receive_id_type || pluginCfg.defaultReceiveIdType,
              name: parsed.name,
              email: parsed.email,
              mobile: parsed.mobile,
              user_id: parsed.user_id || (parsed.receive_id_type === 'user_id' ? parsed.receive_id : undefined),
              open_id: parsed.open_id || (parsed.receive_id_type === 'open_id' ? parsed.receive_id : undefined),
              union_id: parsed.union_id || (parsed.receive_id_type === 'union_id' ? parsed.receive_id : undefined),
            };
            const cachedTarget = cacheResolvedTarget(sendTarget);
            result = await sendMessageWithFallback(client, {
              ...sendTarget,
              ...cachedTarget,
            }, {
              msg_type: parsed.msg_type,
              content: parsed.content,
            });
            break;
          }
          case 'send_followup': {
            const { receive_id, receive_id_type, resolvedName, open_id, user_id, union_id } = pickTargetIdentifier(parsed.target, pluginCfg.defaultReceiveIdType);
            let resolved = {
              receive_id,
              receive_id_type,
              name: parsed.target.name || resolvedName,
              open_id,
              user_id,
              union_id,
              email: parsed.target.email,
              mobile: parsed.target.mobile,
            };

            if (!resolved.receive_id && (parsed.target.name || parsed.target.email || parsed.target.mobile)) {
              const search = await searchEmployees(client, {
                query: parsed.target.name || parsed.target.email || parsed.target.mobile,
                exact_name: parsed.target.name,
                email: parsed.target.email,
                mobile: parsed.target.mobile,
              }, 10);
              const items = search?.items || search?.user_list || search?.users || [];
              if (!Array.isArray(items) || items.length === 0) {
                const reason = parsed.target.email
                  ? `email: ${parsed.target.email}`
                  : parsed.target.mobile
                    ? `mobile: ${parsed.target.mobile}`
                    : `name: ${parsed.target.name}`;
                throw messageError('USER_NOT_FOUND', `Could not resolve target by ${reason}`);
              }
              const user = items[0];
              const summarized = summarizeEmployee(user);
              putCachedContact(summarized);
              resolved = {
                receive_id: summarized.open_id || summarized.user_id,
                receive_id_type: summarized.open_id ? 'open_id' : 'user_id',
                name: parsed.target.name || summarized.name,
                open_id: summarized.open_id,
                user_id: summarized.user_id,
                union_id: summarized.union_id,
                email: summarized.email,
                mobile: summarized.mobile,
                matched_user: summarized,
              };
            }

            if (!resolved.receive_id) {
              throw messageError('TARGET_UNRESOLVED', 'Could not determine receive_id for follow-up target');
            }

            const text = buildFollowupText({
              name: resolved.name,
              work_item: parsed.work_item,
              status_prompt: parsed.status_prompt,
              polite: parsed.polite !== false,
              signature: parsed.signature,
            });

            result = {
              resolved_target: resolved,
              preview_text: text,
            };

            if (!parsed.dry_run) {
              if (!pluginCfg.allowSend) {
                throw messageError('SEND_DISABLED', 'Sending is disabled by plugin config');
              }
              cacheResolvedTarget({
                ...resolved,
                email: parsed.target.email,
                mobile: parsed.target.mobile,
              });
              result.message = await sendMessageWithFallback(client, {
                ...resolved,
                user_id: resolved.matched_user?.user_id || resolved.user_id,
              }, {
                msg_type: 'text',
                content: text,
              });
            } else {
              result.note = 'Dry run only. No message sent.';
            }
            break;
          }
          case 'send_contact_message': {
            const { receive_id, receive_id_type, resolvedName, open_id, user_id, union_id } = pickTargetIdentifier(parsed.target, pluginCfg.defaultReceiveIdType);
            let resolved = {
              receive_id,
              receive_id_type,
              name: parsed.target.name || resolvedName,
              open_id,
              user_id,
              union_id,
              email: parsed.target.email,
              mobile: parsed.target.mobile,
            };

            if (!resolved.receive_id && (parsed.target.name || parsed.target.email || parsed.target.mobile)) {
              const search = await searchEmployees(client, {
                query: parsed.target.name || parsed.target.email || parsed.target.mobile,
                exact_name: parsed.target.name,
                email: parsed.target.email,
                mobile: parsed.target.mobile,
              }, 10);
              const items = search?.items || search?.user_list || search?.users || [];
              if (!Array.isArray(items) || items.length === 0) {
                const reason = parsed.target.email
                  ? `email: ${parsed.target.email}`
                  : parsed.target.mobile
                    ? `mobile: ${parsed.target.mobile}`
                    : `name: ${parsed.target.name}`;
                throw messageError('USER_NOT_FOUND', `Could not resolve target by ${reason}`);
              }
              const user = items[0];
              const summarized = summarizeEmployee(user);
              putCachedContact(summarized);
              resolved = {
                receive_id: summarized.open_id || summarized.user_id,
                receive_id_type: summarized.open_id ? 'open_id' : 'user_id',
                name: parsed.target.name || summarized.name,
                open_id: summarized.open_id,
                user_id: summarized.user_id,
                union_id: summarized.union_id,
                email: summarized.email,
                mobile: summarized.mobile,
                matched_user: summarized,
              };
            }

            if (!resolved.receive_id) {
              throw messageError('TARGET_UNRESOLVED', 'Could not determine receive_id for message target');
            }

            result = {
              resolved_target: resolved,
              preview_text: parsed.content,
            };

            if (!parsed.dry_run) {
              if (!pluginCfg.allowSend) {
                throw messageError('SEND_DISABLED', 'Sending is disabled by plugin config');
              }
              cacheResolvedTarget(resolved);
              result.message = await sendMessageWithFallback(client, {
                ...resolved,
                user_id: resolved.matched_user?.user_id || resolved.user_id,
              }, {
                msg_type: parsed.msg_type,
                content: parsed.content,
              });
            } else {
              result.note = 'Dry run only. No message sent.';
            }
            break;
          }
          default:
            throw messageError('UNSUPPORTED_ACTION', `Unsupported action: ${parsed.action}`);
        }

        return {
          content: [{ type: 'text', text: safeStringify(result) }],
        };
      } catch (error) {
        const normalized = normalizeError(error);
        return {
          content: [{
            type: 'text',
            text: safeStringify({
              error: {
                code: normalized.code,
                message: normalized.message,
                details: normalized.details,
              },
            }),
          }],
          isError: true,
        };
      }
    },
  }), { name: 'feishu_message' });
}
