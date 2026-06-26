"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.classifyS01Action = classifyS01Action;
exports.looksLikeS01Message = looksLikeS01Message;
const DETAILED_TUTORIAL_KEYWORDS = ["详细教程", "查看详细教程"];
const WITHDRAW_TUTORIAL_KEYWORDS = ["提现教程"];
const WITHDRAW_CONFIRM_KEYWORDS = ["确认提现", "确定提现", "确认申请提现", "确定申请提现"];
const AUTH_CONFIRM_KEYWORDS = ["我已授权", "授权完成"];
const START_AUTH_MESSAGES = new Set(["返利", "返利宝", "返利助手", "返利教程", "教程", "使用教程", "使用说明"]);
const ACCOUNT_BALANCE_KEYWORDS = ["余额", "账户余额", "账号余额", "返利余额", "可提现余额", "余额查询"];
const REBATE_DETAILS_KEYWORDS = ["订单", "订单明细", "返利明细", "返利订单", "返利记录", "我的订单"];
const SERVICE_HELP_PATTERNS = [
    /(?:返利宝|返利助手|返利).*(?:怎么用|怎么使用|如何用|如何使用|怎么玩|是什么|有什么用|怎么返利|如何返利|使用教程|使用说明|介绍一下|介绍下|说明一下|说一下|怎么操作|如何操作)/,
    /(?:怎么用|怎么使用|如何用|如何使用|怎么玩|是什么|有什么用|怎么返利|如何返利|使用教程|使用说明|介绍一下|介绍下|说明一下|说一下|怎么操作|如何操作).*(?:返利宝|返利助手|返利|教程)/,
    /(?:返利宝|返利助手|返利).*(?:教程|说明|规则|介绍|帮助|玩法)/,
    /(?:教程|说明|规则|介绍|帮助|玩法).*(?:返利宝|返利助手|返利)/,
    /(?:教程).*(?:怎么用|怎么使用|如何用|如何使用|怎么玩)/,
    /(?:怎么用|怎么使用|如何用|如何使用|怎么玩).*(?:教程)/,
];
const WITHDRAW_HELP_PATTERNS = [
    /(?:返利宝|返利助手|返利).*(?:怎么提现|如何提现|可以提现吗|提现方式|提现规则)/,
    /(?:怎么提现|如何提现|可以提现吗|提现方式|提现规则).*(?:返利宝|返利助手|返利)/,
    /^(?:怎么|如何).*(?:提现|返现)/,
    /(?:提现|返现).*(?:教程|说明|规则|方式|流程|多久到账|到账时间|手续费)/,
    /(?:能提现吗|可以提现吗)/,
];
const ACCOUNT_BALANCE_PATTERNS = [
    /(?:返利宝|返利助手|返利).*(?:余额|账户余额|账号余额|返利余额|可提现余额)/,
    /(?:余额|账户余额|账号余额|返利余额|可提现余额).*(?:返利宝|返利助手|返利)/,
    /(?:查|看|查下|看下|查一下|看一下).*(?:余额|账户余额|账号余额|返利余额|可提现余额)/,
    /(?:余额|账户余额|账号余额|返利余额|可提现余额).*(?:多少|还有多少|有多少)/,
];
const REBATE_DETAILS_PATTERNS = [
    /(?:查|看|查下|看下|查一下|看一下).*(?:订单|订单明细|返利明细|返利订单|返利记录)/,
    /(?:订单|订单明细|返利明细|返利订单|返利记录).*(?:查询|查看|明细|记录|在哪里|在哪|入口|链接)/,
];
const WITHDRAW_APPLY_PATTERNS = [
    /^(?:我要|我想|我需要|帮我|请帮我|麻烦帮我|申请|发起|立即|马上|现在)?\s*(?:全部|全额)?\s*(?:提现|提取)$/,
    /^(?:我要|我想|我需要|帮我|请帮我|麻烦帮我|申请|发起|立即|马上|现在)?\s*(?:提现|提取)\s*(?:金额)?\s*[¥￥]?\s*\d+(?:\.\d+)?\s*(?:元|块|rmb|RMB)?$/,
    /^[¥￥]?\s*\d+(?:\.\d+)?\s*(?:元|块|rmb|RMB)?\s*(?:提现|提取)$/,
    /(?:申请|发起|帮我|请帮我|我要|我想|我需要|立即|马上).*(?:提现|提取)/,
    /(?:提现|提取).*(?:到微信|到零钱|微信红包)/,
];
const WITHDRAW_CONFIRM_PATTERNS = [
    /^(?:确认|确定|确认申请|确定申请|确认提交|确定提交)(?:提现|提取)$/,
];
const AUTH_STATUS_PATTERNS = [
    /(?:返利宝|返利助手|返利).*(?:登录状态|绑定状态|授权状态|注册状态)/,
    /(?:登录状态|绑定状态|授权状态|注册状态)/,
    /(?:我|当前|现在|这里).*(?:登录|绑定|授权|注册).*(?:吗|状态|情况|了没|没有|没)?/,
    /(?:是否|有没有).*(?:登录|绑定|授权|注册)/,
    /(?:登录|绑定|授权|注册).*(?:了吗|没|成功了没|好了没|完成了没)/,
];
const START_AUTH_PATTERNS = [
    /(?:怎么|如何).*(?:登录|注册|授权|绑定).*(?:返利宝|返利助手|返利)?/,
    /(?:返利宝|返利助手|返利).*(?:怎么登录|如何登录|怎么注册|如何注册|怎么授权|如何授权|怎么绑定|如何绑定)/,
    /(?:开始|进入|去).*(?:登录|注册|授权|绑定)/,
    /^(?:登录|注册|授权|绑定)$/,
];
const TRAILING_PUNCTUATION = /[ \t\r\n,，。！？!?；;：:、]+$/;
function containsAny(text, keywords) {
    return keywords.some((keyword) => text.includes(keyword));
}
function matchesAnyPattern(text, patterns) {
    return patterns.some((pattern) => pattern.test(text));
}
function classifyS01Action(rawMessage) {
    let message = String(rawMessage || "").trim().replace(TRAILING_PUNCTUATION, "");
    if (!message) {
        return null;
    }
    if (containsAny(message, DETAILED_TUTORIAL_KEYWORDS)) {
        return ["detailed_tutorial", "命中详细教程关键词"];
    }
    if (containsAny(message, WITHDRAW_CONFIRM_KEYWORDS) || matchesAnyPattern(message, WITHDRAW_CONFIRM_PATTERNS)) {
        return ["withdraw_confirm", "命中提现二次确认表达"];
    }
    if (containsAny(message, WITHDRAW_TUTORIAL_KEYWORDS) || matchesAnyPattern(message, WITHDRAW_HELP_PATTERNS)) {
        return ["withdraw_tutorial", "命中提现说明类表达"];
    }
    if (containsAny(message, ACCOUNT_BALANCE_KEYWORDS) || matchesAnyPattern(message, ACCOUNT_BALANCE_PATTERNS)) {
        return ["account_balance", "命中账户余额类表达"];
    }
    if (containsAny(message, REBATE_DETAILS_KEYWORDS) || matchesAnyPattern(message, REBATE_DETAILS_PATTERNS)) {
        return ["rebate_details", "命中订单/返利明细类表达"];
    }
    if (matchesAnyPattern(message, WITHDRAW_APPLY_PATTERNS)) {
        return ["withdraw_prepare", "命中提现申请类表达"];
    }
    if (containsAny(message, AUTH_CONFIRM_KEYWORDS)) {
        return ["confirm_auth", "命中授权确认关键词"];
    }
    if (matchesAnyPattern(message, AUTH_STATUS_PATTERNS)) {
        return ["binding_status", "命中登录/绑定状态查询表达"];
    }
    if (START_AUTH_MESSAGES.has(message) || matchesAnyPattern(message, START_AUTH_PATTERNS)) {
        return ["start_auth", "命中返利入口/授权入口表达"];
    }
    if (matchesAnyPattern(message, SERVICE_HELP_PATTERNS)) {
        return ["detailed_tutorial", "命中返利宝使用说明类表达"];
    }
    return null;
}
function looksLikeS01Message(rawMessage) {
    return classifyS01Action(rawMessage) !== null;
}
