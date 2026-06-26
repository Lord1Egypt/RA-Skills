/**
 * query-ticket-status.mjs — 查询订单状态（支付状态和完整订单信息）
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   orderId  {string}  [必填] 订单ID
 *   authKey  {string}  [必填] 用户认证密钥
 *   uuid     {string}  [可选] 设备ID
 *
 * 本地调试示例：
 *   echo '{"orderId":"27357039770"}' | node scripts/query-ticket-status.mjs
 *
 * Output（JSON）：
 *   {
 *     orderId       {string}  订单ID
 *     payStatus     {number}  支付状态: 0-未支付, 1-已支付
 *     uniqueStatus  {number}  订单状态: 0-未支付, 9-已完成等
 *     refundStatus  {number}  退款状态
 *     exchangeStatus {number} 核销状态
 *     order         {object}  完整订单信息
 *     cinema        {object}  影院信息
 *   }
 */
import {
  ERROR_CODES,
  ScriptError,
  readJsonInput,
  requireFields,
  run,
  generateMaoyanHeaders,
  loadSavedToken,
  mapAuthKey,
  CHANNEL_ID,
  DEFAULT_TIMEOUT_MS,
} from "./_shared.mjs";

const MAOYAN_API_BASE = "https://m.maoyan.com/api/mtrade/queryorder/v1/detail.json";

await run(async () => {
  const input = mapAuthKey(await readJsonInput());
  requireFields(input, ["orderId"]);

  const token = loadSavedToken(input.token);

  // 构建带查询参数的 URL
  const queryParams = new URLSearchParams({
    orderId: input.orderId,
    clientType: "touch",
    channelId: CHANNEL_ID,
    yodaReady: "h5",
    csecplatform: "4",
    csecversion: "4.2.0",
  });
  const url = `${MAOYAN_API_BASE}?${queryParams.toString()}`;

  const controller = new AbortController();
  const timer = setTimeout(
    () => controller.abort(),
    DEFAULT_TIMEOUT_MS
  );

  let res;
  try {
    res = await fetch(url, {
      method: "GET",
      headers: generateMaoyanHeaders({
        token,
        uuid: input.uuid,
        channelId: CHANNEL_ID,
        extraHeaders: { "Cache-Control": "no-cache", Origin: "https://m.maoyan.com" },
      }),
      signal: controller.signal,
    });
  } catch (error) {
    if (error.name === "AbortError") {
      throw new ScriptError(ERROR_CODES.TIMEOUT, "请求超时");
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }

  if (!res.ok) {
    throw new ScriptError(
      ERROR_CODES.HTTP_ERROR,
      `猫眼接口请求失败，状态码 ${res.status}`
    );
  }

  const json = await res.json();

  // 检查接口返回的业务错误
  if (json.success === false) {
    throw new ScriptError(
      ERROR_CODES.HTTP_ERROR,
      json.error?.message || json.msg || "查询订单状态失败"
    );
  }

  const orderData = json.data || {};
  const order = orderData.order || {};

  return {
    orderId: order.id || input.orderId,
    payStatus: order.payStatus,
    uniqueStatus: order.uniqueStatus,
    refundStatus: order.refundStatus,
    exchangeStatus: order.exchangeStatus,
    order: order,
    cinema: orderData.cinema || null,
  };
});
