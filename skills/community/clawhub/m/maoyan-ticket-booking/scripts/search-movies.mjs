/**
 * search-movies.mjs — 按关键词搜索猫眼影片
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   keyword   {string}  [必填] 搜索关键词，如"复仇者联盟"
 *   cityId    {number}  [可选] 城市 ID（ctx.locate.id），如北京=1
 *   lat       {number}  [可选] 纬度，如 39.90
 *   lng       {number}  [可选] 经度，如 116.40
 *
 * Output（JSON）：
 *   只返回 showst 为 1（即将上映）、3（正在热映）、4（预售）的影片，其余过滤掉
 *   {
 *     total   {number}  过滤后的影片总数
 *     movies  {Array}   影片列表，每项包含：
 *       movieId       {string}   影片 ID
 *       name          {string}   影片名称
 *       enName        {string}   英文名称，无则为空字符串
 *       img           {string}   海报图片 URL
 *       score         {string}   评分，如"9.8"，无则为空字符串
 *       cat           {string}   类型，如"喜剧,动画"
 *       dir           {string}   导演
 *       star          {string}   主演
 *       rt            {string}   上映时间，如"2025-01-29"
 *       wish          {number}   想看人数
 *       ver           {string}   版本信息，无则为空字符串
 *       showst        {number}   上映状态：1-即将上映（不可购票）/ 3-正在热映（可购票）/ 4-预售（可购票）
 *       movieType     {number}   内容类型：0-电影 / 1-电视剧 / 4-网络电影 / 5-网络剧 / 7-短剧
 *       movieTypeDesc {string}   内容类型描述，如"电影"、"电视剧"
 *       pubDesc       {string}   上映描述，如"2026-02-20 10:00中国大陆上映"
 *   }
 */
import {
  readJsonInput,
  requireFields,
  run,
  ScriptError,
  ERROR_CODES,
  generateMaoyanHeaders,
  DEFAULT_TIMEOUT_MS,
} from "./_shared.mjs";

// 关键词搜索影片接口
const MAOYAN_API_URL =
  "https://m.maoyan.com/apollo/mmdb/search/movie/keyword/list.json";

// 仅保留 movieType 为 0（院线电影）和 4（网络电影）的内容，过滤剧集/短剧等
const MOVIE_TYPES = new Set([0, 4]);

// 仅保留这三种上映状态的影片：
// 1 = 即将上映（不可购票，只能标记想看）
// 3 = 正在热映（可购票）
// 4 = 预售（可购票）
const VALID_SHOWST = new Set([1, 3, 4]);

/**
 * 将搜索结果中每个影片对象提取对 OpenClaw 有用的字段
 */
function normalizeMovie(movie) {
  // rt 格式可能为 "2025-01-29 09:00"，截取日期部分
  const rt = (movie.rt || "").split(" ")[0];
  return {
    movieId: String(movie.id || ""),
    name: movie.nm || "",
    enName: movie.enm || "",
    img: movie.img || "",
    score: movie.sc != null ? String(movie.sc) : "",
    cat: movie.cat || "",
    dir: movie.dir || "",
    star: movie.star || "",
    rt,
    wish: movie.wish ?? 0,
    ver: movie.ver || "",
    showst: movie.showst ?? null,
    movieType: movie.movieType ?? null,
    movieTypeDesc: movie.movieTypeDesc || "",
    pubDesc: movie.pubDesc || "",
  };
}

await run(async () => {
  const input = await readJsonInput();
  requireFields(input, ["keyword"]);

  const token = input.token || "";

  const params = new URLSearchParams({ keyword: input.keyword });
  if (input.cityId != null) params.set("ci", input.cityId);
  if (input.lat != null) params.set("lat", input.lat);
  if (input.lng != null) params.set("lng", input.lng);

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
        extraHeaders: { Referer: "https://m.maoyan.com/apollo/search?searchtype=movie" },
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
  // 接口返回顶层 list 数组
  const rawList = json.list || [];
  // 先过滤非电影类型（只保留 movieType 为 0/4），再过滤 showst
  const movies = rawList
    .filter((m) => MOVIE_TYPES.has(m.movieType))
    .filter((m) => VALID_SHOWST.has(m.showst))
    .map(normalizeMovie);

  return {
    total: movies.length,
    movies,
  };
});
