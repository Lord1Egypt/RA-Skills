/**
 * get-hot-movies.mjs — 获取猫眼正在热映的电影列表
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   参数均来自上下文，无需业务侧显式传入：
 *   ct      {string}  [可选] 城市名称（ctx.locate.city）
 *   ci      {string}  [可选] 城市 ID（ctx.locate.id，会根据渠道转换为点评城市 ID）
 *   limit   {number}  [可选] 返回电影条数，默认 10
 *
 * Output（JSON）：
 *   {
 *     total   {number}  热映电影总数
 *     movies  {Array}   电影列表，每项包含：
 *       movieId        {number}   电影 ID
 *       name           {string}   电影名称
 *       img            {string}   海报图片 URL
 *       score          {number}   评分（0 表示暂无评分）
 *       releaseDate    {string}   上映日期，格式 YYYY-MM-DD
 *       star           {string}   主演（逗号分隔）
 *       showInfo       {string}   今日排片概况，如"今天281家影院放映1998场"
 *       wish           {number}   想看人数
 *       version        {string}   版本标签，如"v2d imax"，无则为空字符串
 *       preShow        {boolean}  是否为预售场
 *       globalReleased {boolean}  是否已全面上映
 *       showStateButton {object|null} 购票按钮信息：{ content, color }
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

const MAOYAN_API_URL = "https://m.maoyan.com/ajax/movieOnInfoList";

/**
 * 将 movieList 中每个电影对象提取对 OpenClaw 有用的字段
 */
function normalizeMovie(movie) {
  return {
    movieId: movie.id,
    name: movie.nm,
    img: movie.img,
    score: movie.sc,
    releaseDate: movie.rt,
    star: movie.star,
    showInfo: movie.showInfo,
    wish: movie.wish,
    version: movie.version || "",
    preShow: movie.preShow ?? false,
    globalReleased: movie.globalReleased ?? false,
    showStateButton: movie.showStateButton
      ? {
          content: movie.showStateButton.content,
          color: movie.showStateButton.color,
        }
      : null,
  };
}

await run(async () => {
  const input = mapAuthKey(await readJsonInput());
  const limit = normalizeLimit(input.limit, 10);

  const token = input.token || "";

  const params = new URLSearchParams();
  if (token) params.set("token", token);
  if (input.ct) params.set("ct", input.ct);
  const ci = input.cityId ?? input.ci;
  if (ci != null) params.set("ci", ci);
  if (input.channelId != null) params.set("channelId", input.channelId);
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

  const rawList = json.movieList || [];
  const movies = rawList.slice(0, limit).map(normalizeMovie);

  return {
    total: json.total ?? rawList.length,
    movies,
  };
});
