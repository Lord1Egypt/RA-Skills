/**
 * get-seat-map.mjs — 获取座位图及推荐座位（合并自 recommend-seats.mjs）
 *
 * Input（JSON，通过命令行参数或 stdin 传入）：
 *   seqNo      {string}  [必填] 场次编号（从 get-showtimes 返回的 plist[].seqNo 获取）
 *   ticketCount {number} [可选] 购票张数，默认 1
 *   authKey    {string}  [可选] 用户认证密钥
 *   ci         {number}  [可选] 城市 ID，默认 1
 *   userid     {string}  [可选] 用户 ID
 *   uuid       {string}  [可选] 设备 UUID
 *   deviceInfoByQQ {string} [可选] QQ设备信息
 */
import {
  CHANNEL_ID,
  ERROR_CODES,
  ScriptError,
  readJsonInput,
  requireFields,
  run,
  generateMaoyanHeaders,
  loadSavedToken,
  mapAuthKey,
  DEFAULT_TIMEOUT_MS,
} from "./_shared.mjs";
import { renderSeatMap } from "./render-seat-map.mjs";

const MAOYAN_API_URL = "https://m.maoyan.com/api/mtrade/seat/v8/show/seats.json";

/**
 * 构建 section 索引表
 */
function buildSectionMap(section) {
  if (!section) return {};
  if (!Array.isArray(section)) return section;

  return section.reduce((map, item) => {
    const sectionId = item?.sectionId == null ? "" : String(item.sectionId);
    if (sectionId) map[sectionId] = item;
    return map;
  }, {});
}

/**
 * 标准化座位数据
 */
function normalizeSeat(seat, sectionMap, priceMap) {
  const sectionId = seat.sectionId == null ? "" : String(seat.sectionId);
  const seatStatus = seat.seatStatus;
  const isAisle = seatStatus === 0;
  const section = !isAisle ? sectionMap?.[sectionId] : undefined;
  const sectionPriceFromTable = !isAisle
    ? (priceMap?.[sectionId]?.seatsPrice?.["1"]?.totalPrice ?? null)
    : null;

  return {
    seatNo: seat.seatNo,
    rowId: seat.rowId,
    columnId: seat.columnId,
    sectionId,
    seatType: seat.seatType || "E",
    seatStatus,
    price: sectionPriceFromTable ?? section?.sectionPrice ?? null,
    sectionName: section?.sectionName ?? null,
  };
}

/**
 * 标准化区域数据
 */
function normalizeRegion(region, sectionMap, priceMap) {
  return {
    regionId: region.regionId,
    regionName: region.regionName,
    rowSize: region.rowSize,
    columnSize: region.columnSize,
    canSell: region.canSell ?? true,
    rows: (region.rows || []).map((row) => ({
      rowId: row.rowId,
      rowNum: row.rowNum,
      seats: (row.seats || []).map((seat) =>
        normalizeSeat(seat, sectionMap, priceMap)
      ),
    })),
  };
}

/**
 * 查找推荐座位
 * 策略：从中间排中间列开始，向两边找 ticketCount 个可售座位
 */
function findRecommendedSeats(rows, ticketCount) {
  if (!rows || rows.length === 0) return [];

  const recommended = [];
  const middleRowIndex = Math.floor(rows.length / 2);

  // 从中间排开始，向上下扩展查找
  for (let offset = 0; offset < rows.length; offset++) {
    const rowIndex =
      offset % 2 === 0
        ? middleRowIndex + Math.floor(offset / 2)
        : middleRowIndex - Math.ceil(offset / 2);

    if (rowIndex < 0 || rowIndex >= rows.length) continue;

    const row = rows[rowIndex];
    const seats = row.seats || [];

    // 找中间列
    const middleColIndex = Math.floor(seats.length / 2);

    // 从中间向两边查找连续的可售座位
    for (let startOffset = 0; startOffset <= seats.length - ticketCount; startOffset++) {
      const startIndex = middleColIndex - Math.floor(ticketCount / 2) + startOffset;
      if (startIndex < 0) continue;
      if (startIndex + ticketCount > seats.length) break;

      const candidateSeats = [];
      let allAvailable = true;

      for (let i = 0; i < ticketCount; i++) {
        const seat = seats[startIndex + i];
        if (!seat || seat.seatStatus !== 1) {
          allAvailable = false;
          break;
        }
        candidateSeats.push({
          rowNum: row.rowNum,
          rowId: row.rowId,
          columnId: seat.columnId,
          seatNo: seat.seatNo,
          price: seat.price,
          sectionName: seat.sectionName,
        });
      }

      if (allAvailable && candidateSeats.length === ticketCount) {
        return candidateSeats;
      }
    }
  }

  // 如果找不到连续的，找分散的可用座位
  for (const row of rows) {
    for (const seat of row.seats || []) {
      if (seat.seatStatus === 1) {
        recommended.push({
          rowNum: row.rowNum,
          rowId: row.rowId,
          columnId: seat.columnId,
          seatNo: seat.seatNo,
          price: seat.price,
          sectionName: seat.sectionName,
        });
        if (recommended.length >= ticketCount) {
          return recommended;
        }
      }
    }
  }

  return recommended;
}

/**
 * 生成价格信息文本
 */
function generatePriceInfo(recommendedSeats) {
  if (!recommendedSeats || recommendedSeats.length === 0) return "";

  const count = recommendedSeats.length;
  const price = recommendedSeats[0].price || "0";
  const total = (parseFloat(price) * count).toFixed(0);

  return `¥${price}/张，${count}张共¥${total}`;
}

await run(async () => {
  const input = mapAuthKey(await readJsonInput());
  requireFields(input, ["seqNo"]);

  const ticketCount = Math.max(1, Math.min(4, input.ticketCount || 1));
  const token = loadSavedToken(input.token);

  const params = new URLSearchParams({
    seqNo: input.seqNo,
    channelId: CHANNEL_ID,
  });
  if (input.ci != null) params.set("ci", input.ci);
  if (input.userid) params.set("userid", input.userid);
  if (input.deviceInfoByQQ) params.set("deviceInfoByQQ", input.deviceInfoByQQ);

  const url = `${MAOYAN_API_URL}?${params.toString()}`;

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
        uuid: input.uuid,
        channelId: CHANNEL_ID,
        extraHeaders: { Origin: "https://m.maoyan.com" },
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
  const data = json.data || json;

  const seat = data.seat || {};
  const sectionMap = buildSectionMap(seat.section);
  const priceMap = data.price || {};
  const regions = (seat.regions || []).map((region) =>
    normalizeRegion(region, sectionMap, priceMap)
  );

  // 获取第一个区域的座位数据（通常只有一个区域）
  const firstRegion = regions[0];
  const rows = firstRegion?.rows || [];

  // 查找推荐座位
  const recommendedSeats = findRecommendedSeats(rows, ticketCount);

  // 检查是否有足够座位
  if (recommendedSeats.length < ticketCount) {
    throw new ScriptError(
      ERROR_CODES.INVALID_INPUT,
      `该场次仅剩 ${recommendedSeats.length} 个可用座位，不足以购买 ${ticketCount} 张票`
    );
  }

  // 生成座位图文本（调用 render-seat-map.mjs 的核心渲染函数）
  const centerSeats = recommendedSeats.map((s) => ({
    rowId: s.rowId,
    columnId: s.columnId,
    mark: "★",
  }));
  const renderResult = renderSeatMap(rows, centerSeats, 3, 5, "推荐座位");
  const seatMapText = renderResult.seatMapText || "";

  // 生成价格信息
  const priceInfo = generatePriceInfo(recommendedSeats);

  return {
    cinema: data.cinema
      ? {
          cinemaId: data.cinema.cinemaId,
          cinemaName: data.cinema.cinemaName,
        }
      : null,
    show: data.show
      ? {
          showDate: data.show.showDate,
          showTime: data.show.showTime,
          movieName: data.show.movieName,
        }
      : null,
    buyNumLimit: data.buyNumLimit ?? 4,
    regions,
    seatMapText,
    recommendedSeats,
    priceInfo,
  };
});
