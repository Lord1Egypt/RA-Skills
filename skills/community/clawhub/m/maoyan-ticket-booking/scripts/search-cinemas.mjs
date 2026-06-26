/**
 * search-cinemas.mjs — 按关键词搜索猫眼影院
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   keyword   {string}  [必填] 搜索关键词，如"万达"
 *   cityId    {number}  [可选] 城市 ID（ctx.locate.id），如北京=1
 *   stype     {number}  [可选] 搜索类型，默认 -1（全部）
 *
 * Output（JSON）：
 *   {
 *     total    {number}  搜索结果总数
 *     cinemas  {Array}   影院列表，每项包含：
 *       cinemaId       {string}   影院 ID
 *       name           {string}   影院名称
 *       addr           {string}   地址
 *       sellPrice      {string}   最低售价，如"55"，无则为空字符串
 *       referencePrice {string}   参考价，无则为空字符串
 *       sell           {boolean}  是否可售票
 *       deal           {boolean}  是否有优惠
 *       hallType       {Array}    特色影厅类型列表，如["IMAX厅","CINITY厅"]
 *       allowRefund    {boolean}  是否支持退票
 *       endorse        {boolean}  是否支持改签
 *       snack          {boolean}  是否支持卖品
 *       vipDesc        {string}   会员描述，无则为空字符串
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

// 统一搜索接口，同时返回影片和影院，这里只取 cinemas 部分
const MAOYAN_API_URL = "https://m.maoyan.com/apollo/ajax/search";

/**
 * 提取影院核心名称，去掉常见后缀
 * 例如："光线电影院" → "光线"，"万达影城" → "万达"
 */
function extractCinemaKeyword(input) {
  if (!input) return "";

  // 常见影院后缀词（按长度降序，优先匹配长的）
  const suffixes = ["电影院", "电影城", "影院", "影城", "影都", "剧院", "剧场"];

  let keyword = input.trim();

  // 去掉常见后缀，保留前面的核心词
  for (const suffix of suffixes) {
    if (keyword.endsWith(suffix) && keyword.length > suffix.length) {
      keyword = keyword.slice(0, keyword.length - suffix.length);
      break; // 只去掉第一个匹配的后缀
    }
  }

  return keyword.trim();
}

/**
 * 将搜索结果中每个影院对象提取对 OpenClaw 有用的字段
 */
function normalizeCinema(cinema) {
  return {
    cinemaId: String(cinema.id || ""),
    name: cinema.nm || "",
    addr: cinema.addr || "",
    sellPrice: cinema.sellPrice != null ? String(cinema.sellPrice) : "",
    referencePrice:
      cinema.referencePrice != null ? String(cinema.referencePrice) : "",
    sell: cinema.sell === 1 || cinema.sell === true,
    deal: cinema.deal === 1 || cinema.deal === true,
    // hallType 可能是数组也可能是字符串，统一为数组
    hallType: Array.isArray(cinema.hallType)
      ? cinema.hallType
      : cinema.hallType
        ? [cinema.hallType]
        : [],
    allowRefund: cinema.allowRefund === 1 || cinema.allowRefund === true,
    endorse: cinema.endorse === 1 || cinema.endorse === true,
    snack: cinema.snack === 1 || cinema.snack === true,
    vipDesc: cinema.vipDesc || "",
  };
}

/**
 * 搜索影院（支持双重搜索：原词 + 截取后的核心词）
 */
async function searchCinemas(keyword, cityId, stype, token, uuid) {
  const params = new URLSearchParams({ kw: keyword });
  if (cityId != null) params.set("cityId", cityId);
  params.set("stype", stype ?? -1);

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
        uuid,
        extraHeaders: { Referer: "https://m.maoyan.com/apollo/search?searchtype=cinema" },
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
  const cinemasData = json.cinemas || {};
  const rawList = cinemasData.list || [];
  const cinemas = rawList.map(normalizeCinema);

  return {
    total: cinemasData.total ?? cinemas.length,
    cinemas,
  };
}

await run(async () => {
  const input = mapAuthKey(await readJsonInput());
  requireFields(input, ["keyword"]);

  const originalKeyword = input.keyword.trim();
  const extractedKeyword = extractCinemaKeyword(originalKeyword);

  const token = input.token || "";

  // 第一次搜索：用原词
  const result1 = await searchCinemas(
    originalKeyword,
    input.cityId,
    input.stype,
    token,
    input.uuid
  );

  // 如果原词和截取后的词不同，进行第二次搜索
  let allCinemas = [...result1.cinemas];
  if (extractedKeyword && extractedKeyword !== originalKeyword) {
    const result2 = await searchCinemas(
      extractedKeyword,
      input.cityId,
      input.stype,
      token,
      input.uuid
    );

    // 合并结果，去重（按 cinemaId）
    const existingIds = new Set(allCinemas.map((c) => c.cinemaId));
    for (const cinema of result2.cinemas) {
      if (!existingIds.has(cinema.cinemaId)) {
        allCinemas.push(cinema);
      }
    }
  }

  return {
    total: allCinemas.length,
    cinemas: allCinemas,
  };
});
