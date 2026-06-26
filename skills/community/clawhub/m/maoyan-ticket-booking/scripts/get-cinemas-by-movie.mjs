/**
 * get-cinemas-by-movie.mjs — 根据影片查询有排片的影院列表（含场次信息）
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   参数均来自上下文，无需业务侧显式传入：
 *   movieId      {string}  [必填] 影片 ID（从 get-hot-movies 返回的 movieId 获取）
 *   showDate     {string}  [必填] 放映日期，格式 YYYY-MM-DD（ctx.showDate 或手动传入）
 *   cityId       {number}  [必填] 城市 ID（通过 get-cities.mjs 获取），如北京=1
 *   ci           {number}  [可选] 城市 ID，同 cityId
 *   lat          {number}  [可选] 纬度（ctx.locate.lat），用于按距离排序，默认 -1
 *   lng          {number}  [可选] 经度（ctx.locate.lng），用于按距离排序，默认 -1
 *   sort         {string}  [可选] 排序方式："distance"（距离）/ "price"（价格），默认 "distance"
 *   offset       {number}  [可选] 分页偏移量，默认 0
 *   limit        {number}  [可选] 每页返回条数，默认 20
 *   districtId   {number}  [可选] 行政区 ID（默认 -1 表示全部）
 *   lineId       {number}  [可选] 地铁线 ID（默认 -1）
 *   areaId       {number}  [可选] 区域 ID（默认 -1）
 *   stationId    {number}  [可选] 地铁站 ID（默认 -1）
 *   brandId      {number}  [可选] 品牌 ID（默认 -1 表示全部）
 *   brandIds     {string}  [可选] 品牌 ID 列表 JSON 字符串（默认 "[-1]"）
 *   hallTypeId   {string}  [可选] 影厅类型 ID（默认 "all" 表示全部）
 *   hallTypeIds  {string}  [可选] 影厅类型 ID 列表 JSON 字符串（默认 '["all"]'）
 *   hallType     {string}  [可选] 影厅类型名称列表 JSON 字符串（当 hallTypeId 不为 "all" 时传，如 '["IMAX"]'）
 *   serviceId    {number}  [可选] 服务 ID（默认 -1 表示全部）
 *   serviceIds   {string}  [可选] 服务 ID 列表 JSON 字符串（默认 "[-1]"）
 *   serve        {string}  [可选] 服务列表 JSON 字符串（当 serviceId 不为 -1 时传，如 "[1]"）
 *   languageId   {string}  [可选] 语言 ID（默认 "all" 表示全部）
 *   languageIds  {string}  [可选] 语言 ID 列表 JSON 字符串（默认 '["all"]'）
 *   lang         {string}  [可选] 语言名称列表 JSON 字符串（当 languageId 不为 "all" 时传，如 '["国语"]'）
 *   dimId        {string}  [可选] 放映类型 ID（默认 "all" 表示全部）
 *   dimIds       {string}  [可选] 放映类型 ID 列表 JSON 字符串（默认 '["all"]'）
 *   dim          {string}  [可选] 放映类型名称列表 JSON 字符串（当 dimId 不为 "all" 时传，如 '["2D"]'）
 *
 * Output（JSON）：
 *   {
 *     total    {number}  影院总数
 *     hasMore  {boolean} 是否还有更多
 *     offset   {number}  当前分页偏移量
 *     cinemas  {Array}   影院列表，每项包含：
 *       cinemaId    {number}   影院 ID
 *       name        {string}   影院名称
 *       addr        {string}   地址
 *       distance    {string}   距离，如"1.8km"
 *       sellPrice   {number}   最低售价（从 priceDesc 解析，如 49.9），无则为 null
 *       priceDesc   {string}   价格原始文本，如"¥49.9"
 *       allowRefund {boolean}  是否支持退票（从标签解析）
 *       endorse     {boolean}  是否支持改签（从标签解析）
 *       snack       {boolean}  是否有小吃（从标签解析）
 *       labels      {Array}    影院服务标签列表，如["可退票","可改签","3D眼镜免费"]
 *       shows       {Array}    该影院当日场次列表（cellShows），每项包含：
 *         seqNo     {string}  场次序列号（用于选座）
 *         showId    {string}  场次 ID
 *         tm        {string}  场次时间，格式 HH:mm
 *         dt        {string}  放映日期
 *         lang      {string}  语言版本
 *         tp        {string}  放映类型，如"2D"/"IMAX"
 *         hallName  {string}  影厅名称
 *         sellPr    {number}  售价，无则为 null
 *         seatSold  {number}  已售座位数
 *         seatTotal {number}  总座位数
 *   }
 */
import {
  CHANNEL_ID,
  normalizeLimit,
  readJsonInput,
  requireFields,
  run,
  ScriptError,
  ERROR_CODES,
  generateMaoyanHeaders,
  DEFAULT_TIMEOUT_MS,
} from "./_shared.mjs";

const MAOYAN_CITIES_URL = "https://m.maoyan.com/dianying/cities.json";

const MAOYAN_API_URL = "https://m.maoyan.com/api/mtrade/mmcs/cinema/movie/cinemas.json";



/**
 * 获取城市列表并匹配城市ID
 * @param {string} cityName - 城市名（如"北京市"）
 */
async function getCityIdByName(cityName) {
  if (!cityName) return null;
  
  try {
    const res = await fetch(MAOYAN_CITIES_URL, {
      method: "GET",
      headers: generateMaoyanHeaders({
        extraHeaders: { Accept: "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "jQuery", "M-APPKEY": "fe_canary" },
      }),
    });
    
    if (!res.ok) return null;
    
    const json = await res.json();
    const rawList = json.cts || [];
    
    // 匹配城市名（支持"北京市"匹配"北京"）
    const city = rawList.find((c) => {
      const nm = c.nm || "";
      // 精确匹配或去除"市"后匹配
      return nm === cityName || nm === cityName.replace(/市$/, "");
    });
    
    return city ? city.id : null;
  } catch (error) {
    return null;
  }
}

/**
 * 提取单个场次有用字段
 * 接口实际返回字段在 cellShows 数组中
 */
function normalizeShow(show) {
  const seatStatus = show.seatStatus || {};
  return {
    seqNo: show.seqNo || "",
    showId: show.showId || "",
    tm: show.tm || "",
    dt: show.dt || "",
    lang: show.lang || "",
    tp: show.tp || "",
    hallName: show.hallName || "",
    sellPr: show.sellPr ?? null,
    seatSold: seatStatus.sold ?? 0,
    seatTotal: seatStatus.total ?? 0,
  };
}

/**
 * 提取单个影院有用字段
 * 接口实际返回字段：name(影院名)、cellShows(场次)、priceDesc(价格文本)、cinemaLabelResource(标签)
 */
function normalizeCinema(cinema) {
  // 从 cinemaLabelResource 标签中解析布尔属性
  const labels = (cinema.cinemaLabelResource || []).map((l) => l.desc || "");
  const allowRefund = labels.some((l) => l.includes("退票"));
  const endorse = labels.some((l) => l.includes("改签"));
  const snack = labels.some((l) => l.includes("小食") || l.includes("小吃"));

  // priceDesc 格式为 "¥68"，提取数字部分
  const priceDescRaw = cinema.priceDesc || "";
  const sellPrice = priceDescRaw ? parseFloat(priceDescRaw.replace(/[^0-9.]/g, "")) || null : null;

  return {
    cinemaId: cinema.id,
    name: cinema.name || "",
    addr: cinema.addr || "",
    distance: cinema.distance || "",
    sellPrice,
    priceDesc: priceDescRaw,
    allowRefund,
    endorse,
    snack,
    labels,
    shows: (cinema.cellShows || []).map(normalizeShow),
  };
}

await run(async () => {
  const input = await readJsonInput();
  requireFields(input, ["movieId", "showDate", "cityId"]);

  const limit = normalizeLimit(input.limit, 20);
  const offset = Number(input.offset || 0);

  const token = input.token || "";

  const hallTypeId = input.hallTypeId || "all";
  const languageId = input.languageId || "all";
  const dimId = input.dimId || "all";
  const serviceId = input.serviceId ?? -1;

  const params = new URLSearchParams({
    movieId: input.movieId,
    showDate: input.showDate,
    cityId: input.cityId,
    ci: input.ci ?? input.cityId,
    channelId: input.channelId ?? CHANNEL_ID,
    offset,
    limit,
    lat: input.lat ?? -1,
    lng: input.lng ?? -1,
    sort: input.sort || "distance",
    districtId: input.districtId ?? -1,
    lineId: input.lineId ?? -1,
    areaId: input.areaId ?? -1,
    stationId: input.stationId ?? -1,
    brandId: input.brandId ?? -1,
    brandIds: input.brandIds || "[-1]",
    hallTypeId,
    hallTypeIds: input.hallTypeIds || '["all"]',
    serviceId,
    serviceIds: input.serviceIds || "[-1]",
    languageId,
    languageIds: input.languageIds || '["all"]',
    dimId,
    dimIds: input.dimIds || '["all"]',
    utm_term: "7.5",
    client: "iphone",
  });
  // 筛选条件名称列表：当 ID 不为默认值时才传
  if (hallTypeId !== "all" && input.hallType) params.set("hallType", input.hallType);
  if (String(serviceId) !== "-1" && input.serve) params.set("serve", input.serve);
  if (languageId !== "all" && input.lang) params.set("lang", input.lang);
  if (dimId !== "all" && input.dim) params.set("dim", input.dim);
  if (input.userid) params.set("userid", input.userid);
  if (input.canSellTags) params.set("canSellTags", input.canSellTags);
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
      headers: generateMaoyanHeaders({ token, uuid: input.uuid, channelId: input.channelId ?? CHANNEL_ID }),
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
  const rawList = data.cinemas || [];
  const paging = data.paging || {};

  return {
    total: paging.total ?? rawList.length,
    hasMore: paging.hasMore ?? false,
    offset: paging.offset ?? offset,
    cinemas: rawList.map(normalizeCinema),
  };
});