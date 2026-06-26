/**
 * create-order.mjs — 创建猫眼订单
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   seqNo         {string}  [必填] 场次号
 *   cityId        {string}  [必填] 城市ID
 *   seats         {object}  [必填] 座位信息，格式：{ count: 1, list: [{ columnId, rowId, seatNo, seatStatus, seatType, sectionId, type, sectionName }] }
 *   authKey       {string}  [必填] 用户认证密钥
 *   uuid          {string}  [可选] 设备ID
 *
 * Output（JSON）：
 *   {
 *     success      {boolean} 是否成功
 *     orderId      {string}  订单ID
 *     ...其他订单信息
 *   }
 */
import {
  ERROR_CODES,
  ScriptError,
  readJsonInput,
  requireFields,
  run,
  generateMaoyanHeaders,
  getOrCreateUuid,
  loadSavedToken,
  mapAuthKey,
  CHANNEL_ID,
  CHANNEL_NAME,
  DEFAULT_TIMEOUT_MS,
} from "./_shared.mjs";

// 真实接口 URL（注意带有 /mtrade/ 路径）
const MAOYAN_API_BASE = "https://m.maoyan.com/api/mtrade/createorder/v14/create.json";

await run(async () => {
  const input = mapAuthKey(await readJsonInput());
  requireFields(input, ["seqNo", "cityId", "seats"]);

  const token = loadSavedToken(input.token);
  // 提前获取持久化 UUID，请求体和 headers 保持一致
  const uuid = getOrCreateUuid(input.uuid);

  // 构建带查询参数的 URL
  const queryParams = new URLSearchParams({
    yodaReady: "h5",
    csecplatform: "4",
    csecversion: "4.2.0",
  });
  const url = `${MAOYAN_API_BASE}?${queryParams.toString()}`;

  // 构建请求体
  const body = new URLSearchParams();
  body.set("realNameMethod", "1");
  body.set("channelId", "40003");
  body.set("extChannelId", CHANNEL_ID);
  body.set("extChannelName", CHANNEL_NAME);
  body.set("clientType", "touch");
  body.set("cityId", input.cityId);
  body.set("seqNo", input.seqNo);
  body.set("seats", JSON.stringify(input.seats));

  // h5Fingerprint（风控参数，可选）
  if (input.h5Fingerprint) {
    body.set("h5Fingerprint", input.h5Fingerprint);
  }

  // 请求体中携带 uuid（与 headers 保持一致）
  body.set("uuid", uuid);
  body.set("location", JSON.stringify({ lat: -1, lng: -1 }));
  body.set("deviceInfoByQQ", JSON.stringify({
    location: { lat: -1, lng: -1 },
    identityInfo: { openid: "" }
  }));

  const controller = new AbortController();
  const timer = setTimeout(
    () => controller.abort(),
    DEFAULT_TIMEOUT_MS
  );

  let res;
  try {
    res = await fetch(url, {
      method: "POST",
      headers: generateMaoyanHeaders({
        token,
        uuid,
        channelId: CHANNEL_ID,
        extraHeaders: { "Content-Type": "application/x-www-form-urlencoded", Origin: "https://m.maoyan.com" },
      }),
      body: body.toString(),
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

  // 检查接口返回的业务错误，透传猫眼原始错误码
  if (json.success === false) {
    const maoyanCode = json.error?.code ?? json.code ?? ERROR_CODES.HTTP_ERROR;
    throw new ScriptError(
      maoyanCode,
      json.error?.message || json.msg || "创建订单失败"
    );
  }

  return {
    orderId: json.data?.orderId,
    status: json.data?.status,
    ...json.data,
  };
});
