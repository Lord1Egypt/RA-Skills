/**
 * get-nearby-cinemas.mjs — 获取猫眼影院列表
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   参数均来自上下文，无需业务侧显式传入：
 *   lat        {number}  [可选] 纬度（ctx.locate.lat），用于计算距离排序
 *   lng        {number}  [可选] 经度（ctx.locate.lng），用于计算距离排序
 *   cityId     {string}  [可选] 城市 ID（ctx.locate.id 或通过 get-cities.mjs 获取），不传则使用定位城市
 *   movieId    {string}  [可选] 影片 ID，筛选有该影片排片的影院
 *   day        {string}  [可选] 日期，配合 movieId 使用，格式 YYYY-MM-DD
 *   offset     {number}  [可选] 分页偏移量，默认 0
 *   limit      {number}  [可选] 每页返回条数，默认 10
 *
 * 本地调试示例：
 *   echo '{"address":"北京朝阳立水桥","limit":5}' | node scripts/get-nearby-cinemas.mjs
 *   echo '{"cityId":"1","lat":39.9,"lng":116.4,"limit":5}' | node scripts/get-nearby-cinemas.mjs
 *   echo '{"cityId":"1","lat":39.9,"lng":116.4,"limit":10}' | node scripts/get-nearby-cinemas.mjs
 *
 * Output（JSON）：
 *   {
 *     total    {number}  影院总数
 *     hasMore  {boolean} 是否还有更多
 *     offset   {number}  当前分页偏移量
 *     cinemas  {Array}   影院列表，每项包含：
 *       cinemaId      {number}   影院 ID
 *       name          {string}   影院名称
 *       addr          {string}   地址
 *       distance      {string}   距离，如"1.8km"
 *       sellPrice     {string}   最低售价，如"24.9"，无则为空字符串
 *       hallTypes     {Array}    特色影厅列表，如["IMAX厅","杜比全景声厅"]
 *       allowRefund   {boolean}  是否支持退票
 *       endorse       {boolean}  是否支持改签
 *       snack         {boolean}  是否有小吃
 *       vipTag        {string}   折扣卡标签，如"影城卡"，无则为空字符串
 *   }
 */
import {
  normalizeLimit,
  readJsonInput,
  run,
  ScriptError,
  ERROR_CODES,
  generateMaoyanHeaders,
  mapAuthKey,
  DEFAULT_TIMEOUT_MS,
} from "./_shared.mjs";

const MAOYAN_API_URL = "https://m.maoyan.com/ajax/cinemaList";

/**
 * 将 cinemas 中每个影院对象提取对 OpenClaw 有用的字段
 */
function normalizeCinema(cinema) {
  const tag = cinema.tag || {};
  return {
    cinemaId: cinema.id,
    name: cinema.nm,
    addr: cinema.addr,
    distance: cinema.distance,
    sellPrice: cinema.sellPrice || "",
    hallTypes: tag.hallType || [],
    allowRefund: tag.allowRefund === 1,
    endorse: tag.endorse === 1,
    snack: tag.snack === 1,
    vipTag: tag.vipTag || "",
  };
}

await run(async () => {
  const input = mapAuthKey(await readJsonInput());
  const limit = normalizeLimit(input.limit, 10);
  const offset = Number(input.offset || 0);

  const lat = input.lat;
  const lng = input.lng;

  const token = input.token || "";

  const params = new URLSearchParams({ offset, limit });
  if (input.cityId) params.set("cityId", input.cityId);
  if (lat != null) params.set("lat", lat);
  if (lng != null) params.set("lng", lng);
  if (input.movieId) params.set("movieId", input.movieId);
  if (input.day) params.set("day", input.day);
  if (token) params.set("token", token);

  const url = `${MAOYAN_API_URL}?${params.toString()}`;

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
        extraHeaders: { Accept: "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "jQuery", "M-APPKEY": "fe_canary" },
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

  const rawList = json.cinemas || [];
  const paging = json.paging || {};
  const cinemas = rawList.map(normalizeCinema);

  return {
    total: paging.total ?? rawList.length,
    hasMore: paging.hasMore ?? false,
    offset: paging.offset ?? offset,
    cinemas,
  };
});
