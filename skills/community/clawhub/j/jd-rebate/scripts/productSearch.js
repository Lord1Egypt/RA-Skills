"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.looksLikeNonSearchMessage = looksLikeNonSearchMessage;
exports.buildProductIntent = buildProductIntent;
exports.buildResponse = buildResponse;
exports.emitResponse = emitResponse;
const common_1 = require("./common");
const m01OperationGuide_1 = require("./m01OperationGuide");
const productSearchProtocol_1 = require("./productSearchProtocol");
const recognizePreciseProductSearch_1 = require("./recognizePreciseProductSearch");
const rebateV1Service_1 = require("./rebateV1Service");
const s01Intent_1 = require("./s01Intent");
const SEARCH_INTENT_SYSTEM_PROMPT = `
你是返利商品搜索意图识别器。

你只能输出一个 JSON 对象，不能输出 markdown，不能输出解释。

你的任务：
1. 判断用户这句话是不是“想搜索商品”的请求。
2. 如果是，提取最适合直接传给搜索接口的 query_text。
3. query_text 要尽量保留用户原句里的商品信息、预算、场景、人群、送礼对象等有效搜索条件。
4. 不要把授权、登录状态、教程、提现、闲聊、系统问题识别成商品搜索。
5. 如果能明确看出平台，platform_hint 只允许输出 tb、jd、pdd 之一，否则输出 null。

输出字段：
- is_product_search: boolean
- confidence: 0 到 1
- query_text: string|null
- platform_hint: "tb"|"jd"|"pdd"|null
- brand: string|null
- model: string|null
- sku: string|null
- product_name: string|null
- category: string|null

要求：
- query_text 必须适合直接做商品搜索，不要编造没说过的信息。
- 如果用户没明确表达要搜什么商品，就返回 is_product_search=false。
`.trim();
const NON_SEARCH_PATTERNS = [/(?:谢谢|你好|在吗|帮忙|什么意思|怎么回事)$/];
const LEADING_RECOMMEND_PATTERNS = [
    /^(?:帮我|麻烦|请|请帮我|给我|替我)?(?:推荐|求推荐)(?:一?个|一?款|一?双|一?件|一下|一下子|一些)?\s*/i,
    /^(?:来个|来款|整个|整点)\s*/i,
];
async function buildStartAuthResponseForSearch(rawMessage) {
    try {
        (0, common_1.savePendingAuthRequest)(await (0, common_1.getOrCreateMachineCode)(), {
            scene: "search_rebate",
            handler: "product_search",
            rawMessage,
            reason: "商品搜索场景执行时发现未授权",
        });
    }
    catch {
        // Best-effort only. Failing to persist pending request should not block auth link generation.
    }
    const [payload] = await (0, m01OperationGuide_1.executeAction)("start_auth");
    return payload;
}
function buildErrorPayload(stage, code, message) {
    return { stage, code, message: String(message || "").trim() };
}
function buildResultData(searchResult, productSearchIntent, searchRequest) {
    const items = Array.isArray(searchResult?.items) ? searchResult?.items : [];
    const result = {
        search_result: searchResult || null,
        items,
        total: searchResult?.total ?? items.length,
    };
    if (productSearchIntent) {
        result.product_search_intent = productSearchIntent;
    }
    if (searchRequest) {
        result.search_request = searchRequest;
    }
    return result;
}
function cleanText(value) {
    if (value === null || value === undefined || typeof value === "boolean") {
        return null;
    }
    const text = String(value).trim();
    return text || null;
}
function parseBool(value, defaultValue = false) {
    if (typeof value === "boolean") {
        return value;
    }
    const lowered = String(value || "").trim().toLowerCase();
    if (["true", "1", "yes"].includes(lowered)) {
        return true;
    }
    if (["false", "0", "no"].includes(lowered)) {
        return false;
    }
    return defaultValue;
}
function parseConfidence(value, defaultValue = 0) {
    const confidence = Number(value);
    if (!Number.isFinite(confidence)) {
        return defaultValue;
    }
    return Math.max(0, Math.min(1, confidence));
}
function normalizePlatformHint(value) {
    const normalized = String(value || "").trim().toLowerCase();
    if (["tb", "taobao", "淘宝"].includes(normalized)) {
        return "tb";
    }
    if (["jd", "京东"].includes(normalized)) {
        return "jd";
    }
    if (["pdd", "拼多多"].includes(normalized)) {
        return "pdd";
    }
    return null;
}
function looksLikeNonSearchMessage(cleanedText) {
    if ((0, s01Intent_1.looksLikeS01Message)(cleanedText)) {
        return true;
    }
    return NON_SEARCH_PATTERNS.some((pattern) => pattern.test(cleanedText || ""));
}
function buildSearchQueryParts(cleanedText, ruleSignals) {
    const budget = (0, recognizePreciseProductSearch_1.extractBudget)(cleanedText);
    const crowd = (0, recognizePreciseProductSearch_1.extractCrowd)(cleanedText);
    const usageScene = (0, recognizePreciseProductSearch_1.extractUsageScene)(cleanedText);
    const giftTarget = (0, recognizePreciseProductSearch_1.extractGiftTarget)(cleanedText);
    const parts = [
        ruleSignals.brand,
        ruleSignals.model,
        ruleSignals.sku,
        ruleSignals.product_name,
        ruleSignals.category,
        ...(ruleSignals.attribute_aliases || []),
        ...(ruleSignals.specs || []),
        crowd,
        usageScene,
        giftTarget,
        budget,
    ].filter(Boolean);
    const deduped = (0, recognizePreciseProductSearch_1.dedupePreserveOrder)(parts);
    const ordered = (0, recognizePreciseProductSearch_1.sortValuesByPosition)(cleanedText, deduped);
    return (0, recognizePreciseProductSearch_1.dedupePreserveOrder)([...ordered, ...deduped.filter((part) => !ordered.includes(part))]);
}
function stripPlatformTerms(text, platformHint) {
    let queryText = String(text || "").trim();
    if (!queryText) {
        return "";
    }
    const platformAliases = {
        taobao: ["淘宝", "tb"],
        tb: ["淘宝", "tb"],
        jd: ["京东", "jd"],
        pdd: ["拼多多", "pdd"],
    };
    for (const alias of platformAliases[platformHint || ""] || []) {
        queryText = queryText.replace(new RegExp(`^\\s*${alias.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}[\\s:：,-]*`, "i"), "");
    }
    return queryText.trim();
}
function stripLeadingRecommendWords(text) {
    let queryText = String(text || "").trim();
    let previous = "";
    while (previous !== queryText) {
        previous = queryText;
        for (const pattern of LEADING_RECOMMEND_PATTERNS) {
            queryText = queryText.replace(pattern, "").trim();
        }
    }
    return queryText;
}
function buildSearchRawText(rawMessage, cleanedText, platformHint, fallbackQuery) {
    let queryText = stripPlatformTerms(cleanedText || rawMessage || "", platformHint);
    queryText = stripLeadingRecommendWords(queryText);
    queryText = queryText.replace(/\s+/g, " ").trim().replace(/^[ ,.:;!?]+|[ ,.:;!?]+$/g, "");
    return queryText || String(fallbackQuery || cleanedText || rawMessage || "").trim();
}
function buildModelSearchUserPrompt(rawMessage, cleanedText, ruleSignals) {
    const heuristicHint = {
        brand: ruleSignals.brand,
        model: ruleSignals.model,
        sku: ruleSignals.sku,
        product_name: ruleSignals.product_name,
        category: ruleSignals.category,
        platform_hint: ruleSignals.platform_hint,
        attributes: ruleSignals.attribute_aliases || [],
        specs: ruleSignals.specs || [],
    };
    return [
        "请判断下面这句话是不是商品搜索意图，并抽取可直接搜索的 query_text。",
        "只返回 JSON 对象。",
        `原始消息: ${rawMessage}`,
        `清洗后消息: ${cleanedText}`,
        `启发式参考(仅供参考，原文优先): ${JSON.stringify(heuristicHint, undefined, 0)}`,
    ].join("\n");
}
async function callModelSearchIntent(rawMessage, cleanedText, ruleSignals) {
    const response = await (0, common_1.requestModelJson)(SEARCH_INTENT_SYSTEM_PROMPT, buildModelSearchUserPrompt(rawMessage, cleanedText, ruleSignals), 0.1, 500);
    const payload = response.json || {};
    return {
        recognized_by: "model",
        model_provider: response.provider,
        model_name: response.model,
        is_product_search: parseBool(payload.is_product_search, false),
        confidence: parseConfidence(payload.confidence, 0),
        query_text: cleanText(payload.query_text),
        platform_hint: normalizePlatformHint(payload.platform_hint),
        brand: cleanText(payload.brand),
        model: cleanText(payload.model),
        sku: cleanText(payload.sku),
        product_name: cleanText(payload.product_name),
        category: cleanText(payload.category),
    };
}
function isRuleBasedSearchCandidate(cleanedText, ruleSignals, priceConstraints, crowd, usageScene, giftTarget) {
    if (!cleanedText || looksLikeNonSearchMessage(cleanedText)) {
        return false;
    }
    if (ruleSignals.sku || ruleSignals.model) {
        return true;
    }
    if (ruleSignals.brand && (ruleSignals.product_name || ruleSignals.category)) {
        return true;
    }
    if ((0, recognizePreciseProductSearch_1.containsFuzzyMarker)(cleanedText)) {
        return true;
    }
    if ([priceConstraints.price_min, priceConstraints.price_max, priceConstraints.price_target].some((value) => value !== null && value !== undefined) && (ruleSignals.product_name || ruleSignals.category)) {
        return true;
    }
    if ([crowd, usageScene, giftTarget].some(Boolean) && (ruleSignals.product_name || ruleSignals.category)) {
        return true;
    }
    const category = cleanText(ruleSignals.category);
    const productName = cleanText(ruleSignals.product_name);
    if (category && cleanedText === category) {
        return true;
    }
    if (productName && cleanedText === productName) {
        return true;
    }
    return false;
}
function compactValue(value) {
    if (value === null || value === undefined) {
        return null;
    }
    if (typeof value === "string") {
        const stripped = value.trim();
        return stripped || null;
    }
    if (Array.isArray(value)) {
        const compacted = value.map((item) => compactValue(item)).filter((item) => item !== null);
        return compacted.length ? compacted : null;
    }
    return value;
}
function compactProductSearchIntent(intent) {
    const source = intent || {};
    const compacted = {
        success: Boolean(source.success),
        intent_mode: source.intent_mode,
        query_text: compactValue(source.query_text) || "",
    };
    for (const key of [
        "platform_hint",
        "product_name",
        "category",
        "brand",
        "model",
        "sku",
        "attributes",
        "specs",
        "price_min",
        "price_max",
        "price_target",
        "crowd",
        "usage_scene",
        "gift_target",
    ]) {
        const value = compactValue(source[key]);
        if (value !== null) {
            compacted[key] = value;
        }
    }
    return compacted;
}
function compactSearchRequest(searchRequest) {
    const source = searchRequest || {};
    const compacted = {
        ready: Boolean(source.ready),
        keyword: compactValue(source.keyword) || "",
    };
    const filters = {};
    for (const [key, value] of Object.entries(source.filters || {})) {
        const compactedValue = compactValue(value);
        if (compactedValue !== null) {
            filters[key] = compactedValue;
        }
    }
    if (Object.keys(filters).length) {
        compacted.filters = filters;
    }
    return compacted;
}
async function buildProductIntent(rawMessage) {
    const cleanedText = (0, recognizePreciseProductSearch_1.normalizeText)(rawMessage || "");
    const ruleSignals = (0, recognizePreciseProductSearch_1.extractRuleSignals)(cleanedText);
    const priceConstraints = (0, recognizePreciseProductSearch_1.extractPriceConstraints)(cleanedText);
    let platformHint = normalizePlatformHint(ruleSignals.platform_hint || (0, recognizePreciseProductSearch_1.extractPlatformHint)(cleanedText));
    const crowd = (0, recognizePreciseProductSearch_1.extractCrowd)(cleanedText);
    const usageScene = (0, recognizePreciseProductSearch_1.extractUsageScene)(cleanedText);
    const giftTarget = (0, recognizePreciseProductSearch_1.extractGiftTarget)(cleanedText);
    const sortHint = (0, recognizePreciseProductSearch_1.extractSortHint)(cleanedText);
    const queryParts = buildSearchQueryParts(cleanedText, ruleSignals);
    const fallbackQuery = queryParts.join(" ").trim();
    const fallbackQueryText = buildSearchRawText(rawMessage, cleanedText, platformHint, fallbackQuery);
    let modelIntent = null;
    try {
        modelIntent = await callModelSearchIntent(rawMessage, cleanedText, ruleSignals);
    }
    catch {
        modelIntent = null;
    }
    let recognizedBy = "none";
    let queryText = "";
    if (modelIntent?.is_product_search && modelIntent.query_text) {
        platformHint = modelIntent.platform_hint || platformHint;
        queryText = buildSearchRawText(modelIntent.query_text, (0, recognizePreciseProductSearch_1.normalizeText)(modelIntent.query_text || ""), platformHint, fallbackQueryText);
        recognizedBy = "model";
    }
    else if (isRuleBasedSearchCandidate(cleanedText, ruleSignals, priceConstraints, crowd, usageScene, giftTarget)) {
        queryText = fallbackQueryText;
        recognizedBy = "rule_fallback";
    }
    const productName = modelIntent?.product_name ||
        modelIntent?.category ||
        ruleSignals.product_name ||
        ruleSignals.category ||
        ruleSignals.model ||
        ruleSignals.sku ||
        (recognizedBy !== "none" ? queryText : null);
    const category = modelIntent?.category || ruleSignals.category || ruleSignals.product_name;
    return (0, recognizePreciseProductSearch_1.buildProductSearchIntent)({
        success: Boolean(queryText && recognizedBy !== "none"),
        intent_mode: "search",
        query_text: queryText,
        query_tokens: queryText ? (queryParts.length ? queryParts : [queryText]) : [],
        brand: modelIntent?.brand || ruleSignals.brand,
        series: null,
        model: modelIntent?.model || ruleSignals.model,
        sku: modelIntent?.sku || ruleSignals.sku,
        product_name: productName,
        category,
        attributes: ruleSignals.attribute_aliases || [],
        specs: ruleSignals.specs || [],
        price_min: priceConstraints.price_min,
        price_max: priceConstraints.price_max,
        price_target: priceConstraints.price_target,
        crowd,
        usage_scene: usageScene,
        gift_target: giftTarget,
        sort_hint: sortHint,
        platform_hint: platformHint,
        confidence: modelIntent && recognizedBy === "model" ? modelIntent.confidence : recognizedBy === "rule_fallback" ? 0.6 : 0,
        evidence: {
            recognized_by: recognizedBy,
            model_provider: modelIntent?.model_provider,
            model_name: modelIntent?.model_name,
        },
    });
}
async function buildResponse(rawMessage) {
    const intent = await buildProductIntent(rawMessage);
    const searchRequest = (0, productSearchProtocol_1.buildSearchRequest)(intent);
    const publicIntent = compactProductSearchIntent(intent);
    const publicSearchRequest = compactSearchRequest(searchRequest);
    if (!intent.query_text) {
        return {
            success: false,
            module: "product-search",
            intent: "search_products",
            next_action: "ask_for_search_query",
            code: "NOT_PRODUCT_SEARCH_INTENT",
            result_type: "product_search",
            result_data: buildResultData(undefined, publicIntent, publicSearchRequest),
            error: buildErrorPayload("recognize_query", "NOT_PRODUCT_SEARCH_INTENT", "这句话里还没明确识别到你要搜索的商品。"),
            intent_mode: "search",
            product_search_intent: publicIntent,
            search_request: publicSearchRequest,
            user_message: "这句话里还没明确识别到你要搜索的商品。请直接告诉我商品名、型号，或像“300 左右的耳机”这样的购物需求。",
        };
    }
    let openId = "";
    try {
        ({ openId } = await (0, rebateV1Service_1.requireBoundOpenid)());
    }
    catch {
        return await buildStartAuthResponseForSearch(rawMessage);
    }
    const platform = intent.platform_hint || "";
    try {
        const searchResult = await (0, rebateV1Service_1.searchProductsByKeyword)(openId, intent.query_text, platform, 5);
        const items = Array.isArray(searchResult.items) ? searchResult.items : [];
        return {
            success: Boolean(items.length),
            module: "product-search",
            intent: "search_products",
            next_action: items.length ? "show_search_results" : "ask_for_refined_query",
            code: items.length ? null : "NO_SEARCH_RESULTS",
            result_type: "product_search",
            result_data: buildResultData(searchResult, publicIntent, publicSearchRequest),
            error: items.length ? null : buildErrorPayload("search_product", "NO_SEARCH_RESULTS", "暂时没有找到可返利商品。"),
            intent_mode: "search",
            product_search_intent: publicIntent,
            search_request: publicSearchRequest,
            search_result: searchResult,
            items,
            total: searchResult.total ?? items.length,
            user_message: (0, rebateV1Service_1.buildSearchResultsUserMessage)("商品搜索结果", searchResult),
        };
    }
    catch (error) {
        return {
            success: false,
            module: "product-search",
            intent: "search_products",
            next_action: "retry_product_search",
            code: "PRODUCT_SEARCH_API_ERROR",
            result_type: "product_search",
            result_data: buildResultData(undefined, publicIntent, publicSearchRequest),
            error: buildErrorPayload("search_product", "PRODUCT_SEARCH_API_ERROR", (0, rebateV1Service_1.extractServiceErrorMessage)(error, "商品搜索失败")),
            intent_mode: "search",
            product_search_intent: publicIntent,
            search_request: publicSearchRequest,
            search_result: null,
            user_message: `商品搜索失败，请稍后重试。\n\n${(0, rebateV1Service_1.extractServiceErrorMessage)(error, "商品搜索失败")}`,
        };
    }
}
async function emitResponse(rawMessage, outputFormat) {
    const response = await buildResponse(rawMessage);
    if (outputFormat === "json") {
        (0, common_1.printJson)(response);
    }
    else {
        (0, common_1.printUserMessage)(response.user_message || "", { markdown: outputFormat === "md" });
    }
    return response.success ? 0 : 1;
}
