/**
 * get-cities.mjs — 获取猫眼电影支持的全量城市列表
 *
 * 注意：该接口返回全量城市（约 1100+ 个），数据基本不变，建议调用方缓存结果，
 * 避免重复请求。可通过 cityId/nm/py 查找目标城市后，将 cityId 传给其他脚本使用。
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   无必填参数
 *   keyword  {string}  [可选] 按城市名称或拼音过滤，如"北京"或"beijing"
 *
 * 本地调试示例：
 *   echo '{}' | node scripts/get-cities.mjs
 *   echo '{"keyword":"北京"}' | node scripts/get-cities.mjs
 *   echo '{"keyword":"bei"}' | node scripts/get-cities.mjs
 *
 * Output（JSON）：
 *   {
 *     total   {number}  城市总数
 *     cities  {Array}   城市列表，每项包含：
 *       cityId  {number}  城市 ID（可传给 get-nearby-cinemas / get-cinemas-by-movie 等脚本）
 *       name    {string}  城市名称，如"北京"
 *       py      {string}  城市拼音，如"beijing"
 *   }
 */
import {
  readJsonInput,
  run,
  ScriptError,
  ERROR_CODES,
  generateMaoyanHeaders,
  DEFAULT_TIMEOUT_MS,
} from "./_shared.mjs";

const MAOYAN_API_URL = "https://m.maoyan.com/dianying/cities.json";

await run(async () => {
  const input = await readJsonInput();
  const keyword = (input.keyword || "").trim().toLowerCase();

  const controller = new AbortController();
  const timer = setTimeout(
    () => controller.abort(),
    DEFAULT_TIMEOUT_MS
  );

  let res;
  try {
    res = await fetch(MAOYAN_API_URL, {
      method: "GET",
      headers: generateMaoyanHeaders({
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
  const rawList = json.cts || [];

  const cities = rawList
    .filter((c) => {
      if (!keyword) return true;
      return (
        (c.nm || "").includes(keyword) ||
        (c.py || "").toLowerCase().includes(keyword)
      );
    })
    .map((c) => ({
      cityId: c.id,
      name: c.nm || "",
      py: c.py || "",
    }));

  return {
    total: cities.length,
    cities,
  };
});
