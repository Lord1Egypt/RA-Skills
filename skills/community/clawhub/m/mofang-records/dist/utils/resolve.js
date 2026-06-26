/**
 * 空间/表单解析工具
 * 支持缓存别名、最近使用空间、多空间搜索
 * 被各 handler 内部调用，对外部透明
 */
import { apiRequest } from './http-client.js';
import { getAlias, getLastSpace, addAlias, updateLastSpace, updateLastForm, normalizeAliasKey, } from './cache.js';
function extractSpaces(data) {
    const items = data?.items;
    if (!Array.isArray(items))
        return [];
    return items.map((item) => ({ label: item.label, id: item.id }));
}
function extractForms(data) {
    const entries = data?.feed?.entry;
    if (!Array.isArray(entries))
        return [];
    return entries.map((entry) => ({
        label: entry.content?.form?.label || '',
        id: entry.id,
    }));
}
async function querySpaces(config, spaceLabel) {
    const eqBq = encodeURIComponent(`(label,eq,${spaceLabel})`);
    const eqPath = `/magicflu/service/json/spaces/feed?start=0&limit=10&bq=${eqBq}`;
    const eqResult = await apiRequest(config, 'GET', eqPath);
    if (!eqResult.success)
        return [];
    let spaces = extractSpaces(eqResult.data);
    if (spaces.length === 0) {
        const likeBq = encodeURIComponent(`(label,like_and,${spaceLabel})`);
        const likePath = `/magicflu/service/json/spaces/feed?start=0&limit=10&bq=${likeBq}`;
        const likeResult = await apiRequest(config, 'GET', likePath);
        if (likeResult.success)
            spaces = extractSpaces(likeResult.data);
    }
    return spaces;
}
async function queryForm(config, spaceId, formLabel) {
    const eqBq = encodeURIComponent(`(label,eq,${formLabel})`);
    const eqPath = `/magicflu/service/s/json/${spaceId}/forms/feed?start=0&limit=10&bq=${eqBq}`;
    const eqResult = await apiRequest(config, 'GET', eqPath);
    if (!eqResult.success)
        return [];
    let forms = extractForms(eqResult.data);
    if (forms.length === 0) {
        const likeBq = encodeURIComponent(`(label,like_and,${formLabel})`);
        const likePath = `/magicflu/service/s/json/${spaceId}/forms/feed?start=0&limit=10&bq=${likeBq}`;
        const likeResult = await apiRequest(config, 'GET', likePath);
        if (likeResult.success)
            forms = extractForms(likeResult.data);
    }
    if (forms.length > 0) {
        const exact = forms.filter((f) => f.label === formLabel);
        if (exact.length > 0) {
            forms = exact;
        }
        else {
            const listPath = `/magicflu/service/s/json/${spaceId}/forms/feed?start=0&limit=-1`;
            const listResult = await apiRequest(config, 'GET', listPath);
            if (listResult.success) {
                const allForms = extractForms(listResult.data);
                const allExact = allForms.filter((f) => f.label === formLabel);
                if (allExact.length > 0)
                    forms = allExact;
            }
        }
    }
    if (forms.length === 0) {
        const listPath = `/magicflu/service/s/json/${spaceId}/forms/feed?start=0&limit=-1`;
        const listResult = await apiRequest(config, 'GET', listPath);
        if (listResult.success) {
            const allForms = extractForms(listResult.data);
            const exact = allForms.filter((f) => f.label === formLabel);
            const fuzzy = allForms.filter((f) => f.label.includes(formLabel) || formLabel.includes(f.label));
            forms = exact.length > 0 ? exact : fuzzy;
        }
    }
    return forms;
}
async function listAllSpaces(config) {
    const path = '/magicflu/service/json/spaces/feed?start=0&limit=-1';
    const result = await apiRequest(config, 'GET', path);
    if (!result.success)
        return [];
    return extractSpaces(result.data);
}
function scopedFormAliasKey(spaceHint, formHint) {
    return `space:${normalizeAliasKey(spaceHint)}|form:${normalizeAliasKey(formHint)}`;
}
/**
 * 解析 spaceHint → spaceId（不需要表单）
 */
export async function resolveSpace(config, spaceHint) {
    const hint = normalizeAliasKey(spaceHint);
    if (!hint) {
        return { success: false, message: 'spaceHint 不能为空。' };
    }
    const alias = await getAlias(config.baseUrl, hint);
    if (alias?.spaceId) {
        await updateLastSpace(config.baseUrl, alias.spaceId, alias.spaceLabel || '');
        return {
            success: true,
            message: `从缓存解析空间: ${alias.spaceLabel || ''}`,
            spaceId: alias.spaceId,
            spaceLabel: alias.spaceLabel,
        };
    }
    const spaces = await querySpaces(config, hint);
    if (spaces.length === 0) {
        return { success: false, message: `未找到名称匹配"${hint}"的空间。` };
    }
    const space = spaces[0];
    await updateLastSpace(config.baseUrl, space.id, space.label);
    await addAlias(config.baseUrl, hint, { spaceId: space.id, spaceLabel: space.label });
    return {
        success: true,
        message: `解析空间成功: ${space.label}`,
        spaceId: space.id,
        spaceLabel: space.label,
    };
}
/**
 * 解析 formHint + spaceHint? → spaceId + formId
 * 策略: 缓存别名 → 指定空间查找 → 最近使用空间 → 多空间遍历
 */
export async function resolveSpaceForm(config, formHint, spaceHint) {
    const hint = normalizeAliasKey(formHint);
    const sHint = normalizeAliasKey(spaceHint ?? '');
    if (!hint) {
        return { success: false, message: 'formHint 不能为空。' };
    }
    // 1. 查别名表。传入 spaceHint 时只查带空间上下文的 alias，避免同名表单跨空间误命中。
    const aliasKey = sHint ? scopedFormAliasKey(sHint, hint) : hint;
    const alias = await getAlias(config.baseUrl, aliasKey);
    if (alias?.formId) {
        await updateLastSpace(config.baseUrl, alias.spaceId, alias.spaceLabel || '');
        await updateLastForm(config.baseUrl, alias.spaceId, alias.formId, alias.spaceLabel || '', alias.formLabel || '');
        return {
            success: true,
            message: `从缓存解析: ${alias.spaceLabel || ''} / ${alias.formLabel || ''}`,
            spaceId: alias.spaceId,
            formId: alias.formId,
            spaceLabel: alias.spaceLabel,
            formLabel: alias.formLabel,
        };
    }
    // 2. 指定空间
    if (sHint) {
        const spaces = await querySpaces(config, sHint);
        if (spaces.length === 0) {
            return { success: false, message: `未找到名称匹配"${sHint}"的空间。` };
        }
        for (const space of spaces) {
            const forms = await queryForm(config, space.id, hint);
            if (forms.length > 0) {
                const form = forms[0];
                await updateLastSpace(config.baseUrl, space.id, space.label);
                await updateLastForm(config.baseUrl, space.id, form.id, space.label, form.label);
                await addAlias(config.baseUrl, scopedFormAliasKey(sHint, hint), { spaceId: space.id, spaceLabel: space.label, formId: form.id, formLabel: form.label });
                await addAlias(config.baseUrl, scopedFormAliasKey(space.label, hint), { spaceId: space.id, spaceLabel: space.label, formId: form.id, formLabel: form.label });
                return { success: true, message: `解析成功: ${space.label} / ${form.label}`, spaceId: space.id, formId: form.id, spaceLabel: space.label, formLabel: form.label };
            }
        }
        return { success: false, message: `在空间"${spaces[0].label}"中未找到名称匹配"${hint}"的表单。` };
    }
    // 3. 最近使用空间
    const lastSpace = await getLastSpace(config.baseUrl);
    if (lastSpace) {
        const forms = await queryForm(config, lastSpace.spaceId, hint);
        if (forms.length > 0) {
            const form = forms[0];
            await updateLastSpace(config.baseUrl, lastSpace.spaceId, lastSpace.spaceLabel);
            await updateLastForm(config.baseUrl, lastSpace.spaceId, form.id, lastSpace.spaceLabel, form.label);
            await addAlias(config.baseUrl, hint, { spaceId: lastSpace.spaceId, spaceLabel: lastSpace.spaceLabel, formId: form.id, formLabel: form.label });
            await addAlias(config.baseUrl, scopedFormAliasKey(lastSpace.spaceLabel, hint), { spaceId: lastSpace.spaceId, spaceLabel: lastSpace.spaceLabel, formId: form.id, formLabel: form.label });
            return { success: true, message: `解析成功（最近使用空间）: ${lastSpace.spaceLabel} / ${form.label}`, spaceId: lastSpace.spaceId, formId: form.id, spaceLabel: lastSpace.spaceLabel, formLabel: form.label };
        }
    }
    // 4. 多空间遍历
    const allSpaces = await listAllSpaces(config);
    if (allSpaces.length === 0) {
        return { success: false, message: '未找到任何空间。' };
    }
    for (const space of allSpaces) {
        const forms = await queryForm(config, space.id, hint);
        if (forms.length > 0) {
            const form = forms[0];
            await updateLastSpace(config.baseUrl, space.id, space.label);
            await updateLastForm(config.baseUrl, space.id, form.id, space.label, form.label);
            await addAlias(config.baseUrl, hint, { spaceId: space.id, spaceLabel: space.label, formId: form.id, formLabel: form.label });
            await addAlias(config.baseUrl, scopedFormAliasKey(space.label, hint), { spaceId: space.id, spaceLabel: space.label, formId: form.id, formLabel: form.label });
            return { success: true, message: `解析成功（多空间搜索）: ${space.label} / ${form.label}`, spaceId: space.id, formId: form.id, spaceLabel: space.label, formLabel: form.label };
        }
    }
    return { success: false, message: `在所有空间中未找到名称匹配"${hint}"的表单。` };
}
//# sourceMappingURL=resolve.js.map