/**
 * get-showtimes.mjs — 获取指定影院的排片场次信息
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   cinemaId  {string}  [必填] 影院 ID
 *   ci        {number}  [可选] 城市 ID（ctx.locate.id），默认 1
 *   userid    {string}  [可选] 用户 ID（ctx.user.id）
 *   uuid      {string}  [可选] 设备 UUID（ctx.device.uuid）
 *
 * Output（JSON）：
 *   {
 *     cinemaName  {string}   影院名称
 *     sell        {boolean}  是否可售
 *     movies      {Array}    该影院的影片排片列表，每项包含：
 *       movieId        {number}   影片 ID
 *       name           {string}   影片名称
 *       img            {string}   海报图片 URL
 *       desc           {string}   影片描述，如"剧情/120分钟"
 *       score          {number}   评分
 *       dur            {number}   时长（分钟）
 *       globalReleased {boolean}  是否已上映
 *       shows          {Array}    按日期分组的场次，每项包含：
 *         showDate  {string}  场次日期，格式 YYYY-MM-DD
 *         dateShow  {string}  日期展示文本，如"今天 3月25日"
 *         plist     {Array}   该日期下的场次列表，每项包含：
 *           seqNo   {string}  场次序列号
 *           tm      {string}  开始时间，格式 HH:mm
 *           dt      {string}  放映日期
 *           lang    {string}  语言版本
 *           tp      {string}  放映类型，如"2D"
 *   }
 */
import {
  readJsonInput,
  requireFields,
  run,
  ScriptError,
  ERROR_CODES,
  generateMaoyanHeaders,
  mapAuthKey,
  DEFAULT_TIMEOUT_MS,
} from "./_shared.mjs";

const MAOYAN_API_URL =
  "https://m.maoyan.com/mtrade/cinema/cinema/shows.json";

/**
 * 从场次对象中只保留对 OpenClaw 有用的字段（过滤掉 sellPr 等含反爬字体的 HTML 价格字段）
 */
function normalizeShow(show) {
  return {
    showDate: show.showDate,
    dateShow: show.dateShow,
    plist: (show.plist || []).map((p) => ({
      seqNo: p.seqNo,
      tm: p.tm,
      dt: p.dt,
      lang: p.lang,
      tp: p.tp,
    })),
  };
}

/**
 * 从影片对象中提取对 OpenClaw 有用的字段
 */
function normalizeMovie(movie) {
  return {
    movieId: movie.id,
    name: movie.nm,
    img: movie.img,
    desc: movie.desc,
    score: movie.sc,
    dur: movie.dur,
    globalReleased: movie.globalReleased ?? false,
    shows: (movie.shows || []).map(normalizeShow),
  };
}

await run(async () => {
  const input = mapAuthKey(await readJsonInput());
  requireFields(input, ["cinemaId"]);

  const token = input.token || "";

  const params = new URLSearchParams({ cinemaId: input.cinemaId });
  const ci = input.cityId ?? input.ci;
  if (ci != null) params.set("ci", ci);
  if (input.userid) params.set("userid", input.userid);
  if (input.channelId) params.set("channelId", input.channelId);

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
      headers: generateMaoyanHeaders({ token, uuid: input.uuid, channelId: input.channelId }),
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
  const data = json.data || {};

  return {
    cinemaName: data.cinemaName || "",
    sell: data.sell ?? false,
    movies: (data.movies || []).map(normalizeMovie),
  };
});
