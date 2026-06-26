"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getBoundOpenid = getBoundOpenid;
exports.requireBoundOpenid = requireBoundOpenid;
exports.normalizeApiPlatform = normalizeApiPlatform;
exports.platformLabel = platformLabel;
exports.searchProductsByKeyword = searchProductsByKeyword;
exports.searchProductByLink = searchProductByLink;
exports.applyAdzoneLease = applyAdzoneLease;
exports.createRebateLink = createRebateLink;
exports.queryAccountBalance = queryAccountBalance;
exports.applyWithdraw = applyWithdraw;
exports.formatPrice = formatPrice;
exports.extractServiceErrorMessage = extractServiceErrorMessage;
exports.buildSearchResultsUserMessage = buildSearchResultsUserMessage;
exports.buildConvertResultUserMessage = buildConvertResultUserMessage;
exports.buildAccountBalanceUserMessage = buildAccountBalanceUserMessage;
const common_1 = require("./common");
const PLATFORM_TO_API = {
    taobao: "tb",
    tb: "tb",
    jd: "jd",
    pdd: "pdd",
};
const API_PLATFORM_LABELS = {
    tb: "淘宝",
    jd: "京东",
    pdd: "拼多多",
};
async function getBoundOpenid() {
    const machineCode = await (0, common_1.getOrCreateMachineCode)();
    const binding = (0, common_1.loadLocalOpenidBinding)(machineCode) || {};
    const openId = String(binding.open_id || "").trim();
    return { machineCode, openId };
}
async function requireBoundOpenid() {
    const { machineCode, openId } = await getBoundOpenid();
    if (!openId) {
        throw new Error("当前未检测到已绑定 openId，请先完成微信授权。");
    }
    return { machineCode, openId };
}
function normalizeApiPlatform(platform) {
    const normalized = String(platform || "").trim().toLowerCase();
    return PLATFORM_TO_API[normalized] || normalized;
}
function platformLabel(platform) {
    const normalized = normalizeApiPlatform(platform);
    return API_PLATFORM_LABELS[normalized] || normalized || "未知";
}
async function searchProductsByKeyword(openid, rawText, platform = "", limit = 5) {
    const payload = {
        openid,
        query_type: "keyword",
        platform: normalizeApiPlatform(platform),
        raw_text: String(rawText || "").trim(),
        limit: Math.max(1, Math.min(Number(limit || 5), 10)),
    };
    const response = await (0, common_1.requestRebateV1Json)("POST", "/v1/product/search", payload);
    return response.data || {};
}
async function searchProductByLink(openid, platform, rawText) {
    const payload = {
        openid,
        query_type: "link",
        platform: normalizeApiPlatform(platform),
        raw_text: String(rawText || "").trim(),
    };
    const response = await (0, common_1.requestRebateV1Json)("POST", "/v1/product/search", payload);
    return response.data || {};
}
async function applyAdzoneLease(openid, platform, leaseTtlSeconds = 86400) {
    const payload = {
        openid,
        platform: normalizeApiPlatform(platform),
        lease_ttl_seconds: Number(leaseTtlSeconds || 86400),
    };
    const response = await (0, common_1.requestRebateV1Json)("POST", "/v1/adzone/lease/apply", payload);
    return response.data || {};
}
async function createRebateLink(openid, leaseId, platform, itemId, rawText) {
    const payload = {
        openid,
        lease_id: String(leaseId),
        platform: normalizeApiPlatform(platform),
        item_id: String(itemId),
        raw_text: String(rawText || "").trim(),
    };
    const response = await (0, common_1.requestRebateV1Json)("POST", "/v1/rebate/link/create", payload);
    return response.data || {};
}
async function queryAccountBalance(openid) {
    const response = await (0, common_1.requestRebateV1Json)("POST", "/v1/account/balance", {
        openid: String(openid || "").trim(),
    });
    return response.data || {};
}
async function applyWithdraw(openid, amount) {
    const response = await (0, common_1.requestRebateV1Json)("POST", "/v1/withdraw/apply", {
        openid: String(openid || "").trim(),
        amount: Number(amount),
    });
    return response.data || {};
}
function formatPrice(value) {
    if (value === null || value === undefined || value === "") {
        return "无";
    }
    if (typeof value === "number" && Number.isFinite(value)) {
        const rendered = value.toFixed(2);
        return rendered.replace(/\.00$/, "").replace(/(\.\d)0$/, "$1");
    }
    return String(value);
}
function formatCouponLine(coupon) {
    if (!coupon) {
        return "优惠券：无";
    }
    const amount = formatPrice(coupon.coupon_amount);
    const startFee = formatPrice(coupon.coupon_start_fee);
    const couponType = platformLabel(coupon.coupon_type || "未知");
    return `优惠券：满${startFee}减${amount}（${couponType}）`;
}
function extractServiceErrorMessage(error, defaultMessage) {
    const rawMessage = String(error instanceof Error ? error.message : error || "").trim();
    if (!rawMessage) {
        return defaultMessage;
    }
    const extractFromJsonText = (text) => {
        const payload = JSON.parse(text);
        const detail = payload.detail || {};
        if (detail && typeof detail === "object") {
            if (detail.message) {
                return String(detail.message);
            }
            if (detail.raw) {
                return String(detail.raw);
            }
        }
        if (payload.message) {
            const message = String(payload.message);
            const nestedJsonStart = message.indexOf("{");
            if (nestedJsonStart >= 0) {
                try {
                    return extractFromJsonText(message.slice(nestedJsonStart)) || message;
                }
                catch {
                    return message;
                }
            }
            return message;
        }
        return null;
    };
    const candidates = [rawMessage];
    const jsonStart = rawMessage.indexOf("{");
    if (jsonStart >= 0) {
        candidates.push(rawMessage.slice(jsonStart));
    }
    for (const candidate of candidates) {
        try {
            const message = extractFromJsonText(candidate);
            if (message) {
                return message;
            }
        }
        catch {
            continue;
        }
    }
    return rawMessage;
}
function buildSearchResultsUserMessage(title, data, maxItems) {
    const items = Array.isArray(data?.items) ? data.items : [];
    const total = Number(data?.total || 0);
    if (!items.length) {
        return [
            title,
            "",
            "暂时没有找到可返利商品。",
            "你可以换个更具体的商品名，或者直接把商品链接发给我。",
        ].join("\n");
    }
    const displayItems = maxItems ? items.slice(0, maxItems) : items;
    const lines = [title, "", `共找到 ${total} 个商品：`];
    displayItems.forEach((item, index) => {
        const coupon = item.coupon;
        lines.push("", `${index + 1}. [${platformLabel(item.platform)}] ${item.title || "未命名商品"}`, `店铺：${item.shop_name || "未知店铺"}`, `品牌：${item.brand_name || "未知"}`, `到手价：${formatPrice(item.final_price)}`, `预计返利：${formatPrice(item.estimated_rebate_amount)}`, formatCouponLine(coupon), coupon?.coupon_link ? `优惠券链接：${coupon.coupon_link}` : "优惠券链接：无", `商品链接：${item.item_link || "无"}`);
    });
    lines.push("", "看中哪个商品，直接把上面的商品链接发给我，我帮你转成返利链接。");
    return lines.join("\n");
}
function buildConvertResultUserMessage(data) {
    const payload = data || {};
    return [
        "已为你生成返利链接",
        "",
        `平台：${platformLabel(payload.platform)}`,
        `商品：${payload.title || "未知商品"}`,
        `原价：${formatPrice(payload.origin_price)}`,
        `到手价：${formatPrice(payload.final_price)}`,
        `预计返利：${formatPrice(payload.estimated_rebate_amount)}`,
        formatCouponLine(payload.coupon),
        `返利链接：${payload.convert_link || "无"}`,
        `返利口令：${payload.convert_token || "无"}`,
        `到账说明：${payload.arrival_text || "无"}`,
    ].join("\n");
}
function buildAccountBalanceUserMessage(data) {
    const payload = data || {};
    return [
        "账户余额查询结果",
        "",
        `累计返利：${formatPrice(payload.total_rebate_amount)}`,
        `可提现余额：${formatPrice(payload.available_amount)}`,
        `冻结金额：${formatPrice(payload.frozen_amount)}`,
        `提现中金额：${formatPrice(payload.withdrawing_amount)}`,
        `已提现金额：${formatPrice(payload.withdrawn_amount)}`,
        `当前是否可提现：${payload.can_withdraw ? "是" : "否"}`,
    ].join("\n");
}
