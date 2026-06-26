/**
 * BPM / Activiti：待办列表、条件查询、任务详情、提交(complete)、转办(delegate)、认领/归还(claim/resolve)、跳转(abort/rollback/recovery)、事务(加签等前置)。
 */
import { randomUUID } from 'crypto';
import { bpmFetch, bpmRequest, obtainToken, getTokenInfo, } from './utils/http-client.js';
import { resolveSpaceForm } from './utils/resolve.js';
const ACT = '/activitirest/service';
const KEEP_COMPLETE_VAR_NAMES = new Set([
    'recordId',
    'tempRecordId',
    'formId',
    'spaceId',
    'CURRENT_USER_DIGITALID',
    'CURRENT_USER_NICKNAME',
    'JSESSIONID',
    'serverAddr',
    'jsessionid',
]);
function buildHttpConfig(context) {
    return {
        baseUrl: context.config.BASE_URL,
        username: context.config.USERNAME,
        password: context.config.PASSWORD,
    };
}
/** Activiti 的 assignee/owner/candidate 等为登录名；与抓包、引擎一致。无 username 时用 JWT id。 */
function activitiPrincipal() {
    const i = getTokenInfo();
    if (!i)
        return undefined;
    const s = (i.username || i.userId || '').trim();
    return s || undefined;
}
function findFirstEndEventId(xml) {
    const m = xml.match(/<endEvent\b[^>]*\bid="([^"]+)"/);
    return m ? m[1] : null;
}
function findUserTaskIdByName(xml, taskName) {
    const re = /<userTask\s+([^>]+)>/g;
    let m;
    while ((m = re.exec(xml)) !== null) {
        const attrs = m[1];
        const idM = attrs.match(/\bid="([^"]+)"/);
        const nameM = attrs.match(/\bname="([^"]*)"/);
        if (idM && nameM && nameM[1] === taskName) {
            return idM[1];
        }
    }
    return null;
}
const QUERY_FALLBACK_MAX_SCAN = 300;
const QUERY_FALLBACK_BATCH = 50;
/**
 * 部分环境 POST /query/tasks 返回 415，改用 GET /runtime/tasks 分页 + 内存过滤（与 bpmjs 列表方式一致）。
 */
async function tryQueryTasksRuntimeFallback(config, filterParams, assignee, filterFormId, filterRecordId, page, pageSize) {
    const hasVarFilter = !!filterFormId;
    const hasTaskShapeFilter = !!(filterParams.taskName ||
        filterParams.taskDefinitionKey ||
        filterParams.processDefinitionKey);
    const simplePage = !hasVarFilter && !hasTaskShapeFilter && !filterParams.processDefinitionName;
    if (simplePage) {
        let qs = `assignee=${encodeURIComponent(assignee)}&sort=createTime&order=desc&start=${(page - 1) * pageSize}&size=${pageSize}`;
        if (filterParams.processDefinitionKey) {
            qs += `&processDefinitionKey=${encodeURIComponent(filterParams.processDefinitionKey)}`;
        }
        const res = await bpmFetch(config, 'GET', `${ACT}/runtime/tasks?${qs}&t=${Date.now()}`);
        if (!res.success) {
            return { success: false, message: res.message, data: res.data };
        }
        const payload = res.data;
        return {
            success: true,
            message: 'ok',
            data: {
                tasks: payload?.data ?? [],
                total: payload?.total ?? 0,
                page,
                pageSize,
                queryFallbackUsed: true,
                queryFallbackNote: '当前环境 POST /activitirest/service/query/tasks 不可用（如 415），已改用 GET /runtime/tasks。',
            },
        };
    }
    const matches = [];
    let start = 0;
    let scanned = 0;
    while (scanned < QUERY_FALLBACK_MAX_SCAN) {
        let qs = `assignee=${encodeURIComponent(assignee)}&sort=createTime&order=desc&start=${start}&size=${QUERY_FALLBACK_BATCH}`;
        if (filterParams.processDefinitionKey) {
            qs += `&processDefinitionKey=${encodeURIComponent(filterParams.processDefinitionKey)}`;
        }
        const res = await bpmFetch(config, 'GET', `${ACT}/runtime/tasks?${qs}&t=${Date.now()}`);
        if (!res.success) {
            return { success: false, message: res.message, data: res.data };
        }
        const payload = res.data;
        const batch = payload?.data ?? [];
        if (batch.length === 0)
            break;
        for (const task of batch) {
            scanned++;
            if (filterParams.taskName && task.name !== filterParams.taskName)
                continue;
            if (filterParams.taskDefinitionKey && task.taskDefinitionKey !== filterParams.taskDefinitionKey) {
                continue;
            }
            if (hasVarFilter) {
                const vr = await bpmFetch(config, 'GET', `${ACT}/runtime/tasks/${encodeURIComponent(task.id)}/variables`);
                if (!vr.success || !Array.isArray(vr.data))
                    continue;
                const map = new Map(vr.data.map((x) => [x.name, x.value != null ? String(x.value) : '']));
                if (map.get('formId') !== filterFormId)
                    continue;
                if (filterRecordId != null &&
                    filterRecordId !== '' &&
                    map.get('recordId') !== String(filterRecordId)) {
                    continue;
                }
            }
            matches.push(task);
        }
        start += QUERY_FALLBACK_BATCH;
    }
    const sliceStart = (page - 1) * pageSize;
    const pageRows = matches.slice(sliceStart, sliceStart + pageSize);
    return {
        success: true,
        message: 'ok',
        data: {
            tasks: pageRows,
            total: matches.length,
            page,
            pageSize,
            queryFallbackUsed: true,
            queryFallbackNote: 'POST /query/tasks 不可用，已 GET 分页拉取并在内存中按任务名/定义 key/formId/recordId 过滤。',
            scannedRuntimeTasks: scanned,
            ...(filterParams.processDefinitionName
                ? {
                    queryFallbackWarning: 'fallback 模式下未按 processDefinitionName 过滤（仅能用 processDefinitionKey 等）。',
                }
                : {}),
        },
    };
}
/** GET /runtime/tasks 分页列表（个人待办 / 组待办 / 委托待办） */
export async function listBpmTasksHandler(params, context) {
    const config = buildHttpConfig(context);
    const mode = params.mode ?? 'assignee';
    if (!['assignee', 'candidate', 'delegated'].includes(mode)) {
        return { success: false, message: 'mode 必须是 assignee（我的待办）、candidate（组待办）或 delegated（委托待办）。' };
    }
    const page = Math.max(1, Number(params.page) || 1);
    const pageSize = Math.min(100, Math.max(1, Number(params.pageSize) || 20));
    const start = (page - 1) * pageSize;
    await obtainToken(config);
    const principal = activitiPrincipal();
    if (!principal) {
        return { success: false, message: 'Token 中无 username/id，无法查询待办。请确认 JWT 返回包含 username 或 id。' };
    }
    let qs = `sort=createTime&order=desc&start=${start}&size=${pageSize}`;
    if (mode === 'assignee') {
        qs += `&assignee=${encodeURIComponent(principal)}`;
    }
    else if (mode === 'candidate') {
        qs += `&unassigned=true&candidateUser=${encodeURIComponent(principal)}`;
    }
    else {
        qs += `&owner=${encodeURIComponent(principal)}&delegationState=pending`;
    }
    if (params.processDefinitionKey) {
        qs += `&processDefinitionKey=${encodeURIComponent(params.processDefinitionKey)}`;
    }
    if (params.descriptionLike) {
        qs += `&descriptionLike=${encodeURIComponent(params.descriptionLike)}`;
    }
    const res = await bpmFetch(config, 'GET', `${ACT}/runtime/tasks?${qs}&t=${Date.now()}`);
    if (!res.success)
        return res;
    const payload = res.data;
    const tasks = payload?.data ?? [];
    const slim = tasks.map((t) => ({
        id: t.id,
        name: t.name,
        description: t.description,
        taskDefinitionKey: t.taskDefinitionKey,
        assignee: t.assignee,
        owner: t.owner,
        delegationState: t.delegationState,
        createTime: t.createTime,
        dueDate: t.dueDate,
        processInstanceId: t.processInstanceId,
        processDefinitionId: t.processDefinitionId,
        priority: t.priority,
    }));
    return {
        success: true,
        message: 'ok',
        data: {
            tasks: slim,
            total: payload?.total ?? slim.length,
            page,
            pageSize,
            mode,
        },
    };
}
/** POST /query/tasks，可按表单/记录/流程名等定位（与 Java MFBPMGETTASK 条件一致） */
export async function queryBpmTasksHandler(params, context) {
    const config = buildHttpConfig(context);
    if ((params.formHint || params.recordId) && !params.formHint?.trim()) {
        return { success: false, message: '按记录定位时请同时提供 formHint（及可选 spaceHint）以解析 formId。' };
    }
    const body = {
        includeProcessVariables: params.includeProcessVariables !== false,
    };
    await obtainToken(config);
    const assignee = params.assigneeUserId?.trim() || activitiPrincipal();
    if (!assignee) {
        return { success: false, message: '无法确定 assignee（可传 assigneeUserId，或 JWT 含 username/id）。' };
    }
    body.assignee = assignee;
    if (params.processDefinitionKey)
        body.processDefinitionKey = params.processDefinitionKey;
    if (params.processDefinitionName)
        body.processDefinitionName = params.processDefinitionName;
    if (params.taskName)
        body.name = params.taskName;
    if (params.taskDefinitionKey)
        body.taskDefinitionKey = params.taskDefinitionKey;
    const pvars = [];
    if (params.formHint?.trim()) {
        const r = await resolveSpaceForm(config, params.formHint, params.spaceHint);
        if (!r.success || !r.formId) {
            return { success: false, message: r.message };
        }
        pvars.push({ name: 'formId', value: r.formId, operation: 'equals' });
    }
    if (params.recordId) {
        pvars.push({ name: 'recordId', value: String(params.recordId), operation: 'equals' });
    }
    if (pvars.length > 0) {
        body.processInstanceVariables = pvars;
    }
    const page = Math.max(1, Number(params.page) || 1);
    const pageSize = Math.min(100, Math.max(1, Number(params.pageSize) || 50));
    body.start = (page - 1) * pageSize;
    body.size = pageSize;
    const res = await bpmRequest(config, 'POST', `${ACT}/query/tasks`, body);
    if (res.success) {
        const d = res.data;
        return {
            success: true,
            message: 'ok',
            data: {
                tasks: d?.data ?? [],
                total: d?.total ?? 0,
                page,
                pageSize,
            },
        };
    }
    if (res.message.includes('415') || res.message.includes('405')) {
        const filterFormId = pvars.find((p) => p.name === 'formId')?.value;
        const filterRecordId = pvars.find((p) => p.name === 'recordId')?.value;
        return tryQueryTasksRuntimeFallback(config, {
            processDefinitionKey: params.processDefinitionKey,
            processDefinitionName: params.processDefinitionName,
            taskName: params.taskName,
            taskDefinitionKey: params.taskDefinitionKey,
        }, assignee, filterFormId, filterRecordId, page, pageSize);
    }
    return res;
}
/** 任务详情 + 变量（定位办理上下文） */
export async function getBpmTaskHandler(params, context) {
    const taskId = params.taskId?.trim();
    if (!taskId) {
        return { success: false, message: '需要 taskId。' };
    }
    const config = buildHttpConfig(context);
    const taskRes = await bpmFetch(config, 'GET', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}`);
    if (!taskRes.success)
        return taskRes;
    const varRes = await bpmFetch(config, 'GET', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}/variables`);
    const variables = varRes.success && Array.isArray(varRes.data) ? varRes.data : varRes.data;
    let recordId;
    let spaceId;
    let formId;
    if (Array.isArray(variables)) {
        for (const v of variables) {
            if (v.name === 'recordId')
                recordId = v.value;
            if (v.name === 'spaceId')
                spaceId = v.value;
            if (v.name === 'formId')
                formId = v.value;
        }
    }
    return {
        success: true,
        message: 'ok',
        data: {
            task: taskRes.data,
            variables,
            hints: { recordId, spaceId, formId },
        },
    };
}
/** 与 BPMCompleteTaskFunc 一致：保留系统变量；POST 回任务时可含 tempRecordId，complete 体中再去掉 */
function buildKeepVariablesForTask(raw) {
    const keep = [];
    for (const v of raw) {
        if (!v || typeof v !== 'object')
            continue;
        const name = v.name;
        if (!KEEP_COMPLETE_VAR_NAMES.has(name))
            continue;
        const copy = { ...v, scope: 'local' };
        keep.push(copy);
    }
    for (const v of keep) {
        if (v.name === 'recordId' || v.name === 'formId' || v.name === 'spaceId') {
            v.scope = 'global';
        }
    }
    return keep;
}
/**
 * 完成任务（提交）：默认按服务端公式逻辑同步变量后 complete；可简化为仅 POST complete。
 */
export async function completeBpmTaskHandler(params, context) {
    const taskId = params.taskId?.trim();
    if (!taskId) {
        return { success: false, message: '需要 taskId。' };
    }
    const config = buildHttpConfig(context);
    if (params.simple) {
        if (!Array.isArray(params.variables)) {
            return { success: false, message: 'simple 为 true 时请提供 variables 数组。' };
        }
        await obtainToken(config);
        return bpmRequest(config, 'POST', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}`, {
            action: 'complete',
            variables: params.variables,
        });
    }
    await obtainToken(config);
    const info = getTokenInfo();
    const getV = await bpmFetch(config, 'GET', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}/variables`);
    if (!getV.success)
        return getV;
    let list = Array.isArray(getV.data) ? getV.data : [];
    let keep = buildKeepVariablesForTask(list);
    const hasUser = keep.some((v) => v.name === 'CURRENT_USER_DIGITALID');
    if (!hasUser) {
        const login = (info.username || info.userId || '').trim();
        if (login) {
            keep.push({
                name: 'CURRENT_USER_DIGITALID',
                value: login,
                scope: 'local',
                type: 'string',
            });
        }
    }
    const hasNick = keep.some((v) => v.name === 'CURRENT_USER_NICKNAME');
    if (!hasNick && info.nickname) {
        keep.push({
            name: 'CURRENT_USER_NICKNAME',
            value: info.nickname,
            scope: 'local',
            type: 'string',
        });
    }
    if (Array.isArray(params.variables) && params.variables.length > 0) {
        keep = keep.concat(params.variables);
    }
    const del = await bpmFetch(config, 'DELETE', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}/variables`);
    if (!del.success) {
        return {
            success: false,
            message: `无法清空任务变量: ${del.message}。若服务端要求浏览器会话，可改用 simple:true 并自行传入 variables。`,
            data: del.data,
        };
    }
    const postV = await bpmRequest(config, 'POST', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}/variables`, keep);
    if (!postV.success) {
        return { success: false, message: `回写任务变量失败: ${postV.message}`, data: postV.data };
    }
    const forComplete = keep.filter((v) => v.name !== 'tempRecordId');
    for (const v of forComplete) {
        if (v.name === 'recordId' || v.name === 'formId' || v.name === 'spaceId') {
            v.scope = 'global';
        }
    }
    const upd = await bpmFetch(config, 'POST', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}/updateDesc`, {
        textBody: '',
    });
    if (!upd.success) {
        return { success: false, message: `updateDesc 失败: ${upd.message}`, data: upd.data };
    }
    return bpmRequest(config, 'POST', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}`, {
        action: 'complete',
        variables: forComplete,
    });
}
export async function delegateBpmTaskHandler(params, context) {
    const taskId = params.taskId?.trim();
    const assignee = params.assignee?.trim();
    if (!taskId || !assignee) {
        return { success: false, message: '需要 taskId 与 assignee（被转办人账号 id）。' };
    }
    const config = buildHttpConfig(context);
    return bpmRequest(config, 'POST', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}`, {
        action: 'delegate',
        assignee,
    });
}
export async function claimBpmTaskHandler(params, context) {
    const taskId = params.taskId?.trim();
    if (!taskId) {
        return { success: false, message: '需要 taskId。' };
    }
    const config = buildHttpConfig(context);
    await obtainToken(config);
    const assignee = params.assignee?.trim() || activitiPrincipal();
    if (!assignee) {
        return { success: false, message: '需要 assignee 或 Token 中的用户 id。' };
    }
    return bpmRequest(config, 'POST', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}`, {
        action: 'claim',
        assignee,
    });
}
export async function resolveBpmTaskHandler(params, context) {
    const taskId = params.taskId?.trim();
    if (!taskId) {
        return { success: false, message: '需要 taskId。' };
    }
    const config = buildHttpConfig(context);
    return bpmRequest(config, 'POST', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}`, {
        action: 'resolve',
    });
}
/** abort：默认识别第一个 endEvent；rollback：可按用户任务显示名解析；recovery：必须提供 jumpTargetId */
export async function jumpBpmTaskHandler(params, context) {
    const taskId = params.taskId?.trim();
    const kind = params.kind;
    if (!taskId || !kind) {
        return { success: false, message: '需要 taskId 与 kind（abort | rollback | recovery）。' };
    }
    const config = buildHttpConfig(context);
    let targetId = params.jumpTargetId?.trim();
    const loadBpmnXml = async () => {
        const tres = await bpmFetch(config, 'GET', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}`);
        if (!tres.success)
            return { ok: false, message: tres.message };
        const defId = tres.data?.processDefinitionId;
        if (!defId)
            return { ok: false, message: '无法从任务解析 processDefinitionId。' };
        const xmlres = await bpmFetch(config, 'GET', `${ACT}/repository/process-definitions/${encodeURIComponent(defId)}/resourcedata`);
        if (!xmlres.success)
            return { ok: false, message: xmlres.message };
        const xml = xmlres.data?.xml;
        if (!xml)
            return { ok: false, message: '未获取到流程 BPMN XML。' };
        return { ok: true, xml };
    };
    if (kind === 'abort') {
        if (!targetId) {
            const b = await loadBpmnXml();
            if (!('xml' in b))
                return { success: false, message: b.message };
            targetId = findFirstEndEventId(b.xml) || undefined;
            if (!targetId) {
                return { success: false, message: 'BPMN 中未找到 endEvent 的 id，请手动传 jumpTargetId。' };
            }
        }
    }
    else if (kind === 'rollback') {
        if (!targetId) {
            const name = params.targetTaskName?.trim();
            if (!name) {
                return {
                    success: false,
                    message: 'rollback 需要 jumpTargetId，或提供 targetTaskName（流程图上用户任务的「名称」）。',
                };
            }
            const b = await loadBpmnXml();
            if (!('xml' in b))
                return { success: false, message: b.message };
            targetId = findUserTaskIdByName(b.xml, name) || undefined;
            if (!targetId) {
                return { success: false, message: `未在 BPMN 中找到用户任务「${name}」的 id。` };
            }
        }
    }
    else if (kind === 'recovery') {
        if (!targetId) {
            return { success: false, message: 'recovery 必须提供 jumpTargetId（如 sid-xxxx）。' };
        }
    }
    else {
        return { success: false, message: 'kind 必须是 abort、rollback 或 recovery。' };
    }
    return bpmFetch(config, 'POST', `${ACT}/runtime/tasks/${encodeURIComponent(taskId)}/jump/${encodeURIComponent(targetId)}/${kind}`, {});
}
/**
 * 开启 BPM 事务（如并行加签前），对应 RecordPanel.beforeSaveForBpm。
 * 返回 transactionId，关闭事务时需原样传入 mofang_bpm_close_transaction。
 */
export async function openBpmTransactionHandler(params, context) {
    const action = params.taskAction?.trim();
    if (!action) {
        return { success: false, message: '需要 taskAction（如 COSIGN 表示加签）。' };
    }
    const config = buildHttpConfig(context);
    const transactionId = randomUUID();
    const extraCookie = `TRANSACTIONID=${transactionId}`;
    const body = {
        _PROCESSKEY: params.processKey ?? '',
        _PROCESSINSTID: params.processInstId ?? '',
        _TASKID: params.taskId ?? '',
        _PROCESSNAME: params.processName ?? '',
        _TASKNAME: params.taskName ?? '',
        _TASKACTION: action,
    };
    const res = await bpmFetch(config, 'POST', '/magicflu/session?type=transaction', {
        jsonBody: body,
        extraCookie,
    });
    if (!res.success)
        return res;
    return {
        success: true,
        message: '事务已开启。办理加签等操作后请调用 mofang_bpm_close_transaction，并传入同一 transactionId。',
        data: { transactionId, ...res.data },
    };
}
export async function closeBpmTransactionHandler(params, context) {
    const tid = params.transactionId?.trim();
    if (!tid) {
        return { success: false, message: '需要 transactionId（与 open 时返回的一致）。' };
    }
    const config = buildHttpConfig(context);
    return bpmFetch(config, 'POST', '/magicflu/session?type=transaction&action=delete', {
        jsonBody: {},
        extraCookie: `TRANSACTIONID=${tid}`,
    });
}
//# sourceMappingURL=bpm.js.map