"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.classifyScene = classifyScene;
exports.buildResponse = buildResponse;
exports.emitResponse = emitResponse;
const common_1 = require("./common");
const m01OperationGuide_1 = require("./m01OperationGuide");
const m02PlatformLink_1 = require("./m02PlatformLink");
const productSearch_1 = require("./productSearch");
const recognizePreciseProductSearch_1 = require("./recognizePreciseProductSearch");
const s01Intent_1 = require("./s01Intent");
const SCENE_LABELS = {
    auth_guide: "授权与教程",
    link_rebate: "链接返利",
    search_rebate: "搜索返利",
};
function classifyScene(rawMessage) {
    const message = String(rawMessage || "").trim();
    const s01Match = (0, s01Intent_1.classifyS01Action)(message);
    if (s01Match) {
        const [action, reason] = s01Match;
        return {
            scene: "auth_guide",
            handler: "m01_operation_guide",
            action,
            reason,
        };
    }
    if (message.includes("http://") || message.includes("https://")) {
        return {
            scene: "link_rebate",
            handler: "m02_platform_link",
            action: null,
            reason: "检测到 http(s) 链接",
        };
    }
    return {
        scene: "search_rebate",
        handler: "product_search",
        action: null,
        reason: "无链接，按商品搜索场景处理",
    };
}
async function hasLocalAuthorization() {
    try {
        const machineCode = await (0, common_1.getOrCreateMachineCode)();
        return Boolean((0, common_1.loadLocalOpenidBinding)(machineCode));
    }
    catch {
        return false;
    }
}
async function shouldSavePendingAuthRequest(route, rawMessage) {
    const scene = route.scene;
    if (scene === "link_rebate") {
        return true;
    }
    if (scene !== "search_rebate") {
        return false;
    }
    const cleanedText = (0, recognizePreciseProductSearch_1.normalizeText)(rawMessage || "");
    if (!cleanedText || (0, productSearch_1.looksLikeNonSearchMessage)(cleanedText)) {
        return false;
    }
    try {
        const intent = await (0, productSearch_1.buildProductIntent)(rawMessage);
        return Boolean(intent.query_text);
    }
    catch {
        return false;
    }
}
async function savePendingRouteRequest(route, rawMessage) {
    if (!(await shouldSavePendingAuthRequest(route, rawMessage))) {
        return;
    }
    try {
        (0, common_1.savePendingAuthRequest)(await (0, common_1.getOrCreateMachineCode)(), {
            scene: route.scene,
            handler: route.handler,
            rawMessage,
            reason: route.reason,
        });
    }
    catch {
        return;
    }
}
async function buildResponse(rawMessage) {
    let route = classifyScene(rawMessage);
    if (!(await hasLocalAuthorization()) && route.action !== "confirm_auth") {
        await savePendingRouteRequest(route, rawMessage);
        route = {
            scene: "auth_guide",
            handler: "m01_operation_guide",
            action: "start_auth",
            reason: "当前未授权，需先进入 S01 完成微信授权",
        };
    }
    const resolvedHandler = route.handler;
    const resolvedReason = route.reason;
    let payload;
    let exitCode = 0;
    if (route.scene === "auth_guide") {
        [payload, exitCode] = await (0, m01OperationGuide_1.executeAction)(route.action, rawMessage);
    }
    else if (route.scene === "link_rebate") {
        payload = await (0, m02PlatformLink_1.buildResponse)(rawMessage);
        exitCode = payload.success ? 0 : 1;
    }
    else {
        payload = await (0, productSearch_1.buildResponse)(rawMessage);
        exitCode = payload.success ? 0 : 1;
    }
    return {
        success: payload.success ?? exitCode === 0,
        scene: route.scene,
        scene_label: SCENE_LABELS[route.scene],
        handler: resolvedHandler,
        route_reason: resolvedReason,
        module: payload.module,
        intent: payload.intent,
        next_action: payload.next_action,
        code: payload.code,
        result_type: payload.result_type,
        result_data: payload.result_data,
        error: payload.error,
        user_message: payload.user_message || "",
    };
}
async function emitResponse(rawMessage, outputFormat) {
    const response = await buildResponse(rawMessage);
    if (outputFormat === "json") {
        (0, common_1.printJson)(response);
    }
    else {
        (0, common_1.printUserMessage)(response.user_message || "", { markdown: outputFormat === "md" });
    }
    const handledWithdrawMessage = outputFormat !== "json" && response.result_type === "withdraw" && Boolean(String(response.user_message || "").trim());
    return response.success || handledWithdrawMessage ? 0 : 1;
}
