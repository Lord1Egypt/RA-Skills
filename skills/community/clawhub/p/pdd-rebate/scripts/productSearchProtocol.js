"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildSearchRequest = buildSearchRequest;
exports.buildSearchReadyUserMessage = buildSearchReadyUserMessage;
function buildSearchRequest(productSearchIntent) {
    const intent = productSearchIntent || {};
    return {
        ready: Boolean(intent.success),
        intent_mode: intent.intent_mode,
        keyword: String(intent.query_text || "").trim(),
        search_terms: Array.isArray(intent.query_tokens) ? [...intent.query_tokens] : [],
        filters: {
            brand: intent.brand ?? null,
            series: intent.series ?? null,
            model: intent.model ?? null,
            sku: intent.sku ?? null,
            product_name: intent.product_name ?? null,
            category: intent.category ?? null,
            attributes: Array.isArray(intent.attributes) ? [...intent.attributes] : [],
            specs: Array.isArray(intent.specs) ? [...intent.specs] : [],
            price_min: intent.price_min ?? null,
            price_max: intent.price_max ?? null,
            price_target: intent.price_target ?? null,
            crowd: intent.crowd ?? null,
            usage_scene: intent.usage_scene ?? null,
            gift_target: intent.gift_target ?? null,
            platform_hint: intent.platform_hint ?? null,
            sort_hint: intent.sort_hint ?? null,
        },
    };
}
function formatOptionalPriceLine(intent) {
    const priceMin = intent.price_min;
    const priceMax = intent.price_max;
    const priceTarget = intent.price_target;
    if (priceMin !== null && priceMin !== undefined || priceMax !== null && priceMax !== undefined) {
        return `价格范围：${priceMin ?? "无"} - ${priceMax ?? "无"}`;
    }
    if (priceTarget !== null && priceTarget !== undefined) {
        return `目标价格：${priceTarget}`;
    }
    return "价格：无";
}
function buildSearchReadyUserMessage(title, decision, intent, includeNextStep = true) {
    const payload = intent || {};
    const attributes = Array.isArray(payload.attributes) && payload.attributes.length ? payload.attributes.join(" / ") : "无";
    const specs = Array.isArray(payload.specs) && payload.specs.length ? payload.specs.join(" / ") : "无";
    const lines = [
        title,
        "",
        `判定：${decision}`,
        `搜索词：${payload.query_text || "无"}`,
        `商品：${payload.product_name || "无"}`,
        `类目：${payload.category || "无"}`,
        `品牌：${payload.brand || "无"}`,
        `型号：${payload.model || "无"}`,
        `SKU：${payload.sku || "无"}`,
        `属性：${attributes}`,
        `规格：${specs}`,
        formatOptionalPriceLine(payload),
        `人群：${payload.crowd || "无"}`,
        `场景：${payload.usage_scene || "无"}`,
        `送礼对象：${payload.gift_target || "无"}`,
        `平台提示：${payload.platform_hint || "无"}`,
        `排序偏好：${payload.sort_hint || "无"}`,
    ];
    if (includeNextStep) {
        lines.push("下一步：可直接调用商品搜索接口");
    }
    return lines.join("\n");
}
