function pad2(n) {
  return String(n).padStart(2, "0");
}

function formatTime(tsSeconds) {
  const d = new Date(tsSeconds * 1000);
  return (
    `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())} ` +
    `${pad2(d.getHours())}:${pad2(d.getMinutes())}:${pad2(d.getSeconds())}`
  );
}

/**
 * OpenClaw / ClawHub skill entrypoint.
 * @param {Object} event - expected shape: { parameters: { symbol?: string } }
 * @param {Object} context - runtime context (unused)
 * @returns {Promise<Object>} result json
 */
async function handler(event, context) {
  try {
    const params = (event && event.parameters) || {};
    const symbol = params.symbol || "NQ=F";

    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(
      symbol
    )}`;

    const res = await fetch(url, {
      method: "GET",
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        Accept: "application/json",
      },
    });

    if (!res.ok) {
      const text = await res.text().catch(() => "");
      throw new Error(
        `HTTP ${res.status} ${res.statusText}${text ? `: ${text}` : ""}`
      );
    }

    const data = await res.json();
    const result = data?.chart?.result?.[0];
    const meta = result?.meta;

    const regularPrice = meta?.regularMarketPrice;
    const previousClose = meta?.previousClose;

    if (typeof regularPrice !== "number" || typeof previousClose !== "number") {
      throw new Error("解析失败：缺少 regularMarketPrice 或 previousClose。");
    }

    const change = regularPrice - previousClose;
    const changePercent = previousClose === 0 ? 0 : (change / previousClose) * 100;

    const ts = result?.timestamp?.[0];
    const timeStr = typeof ts === "number" ? formatTime(ts) : "";

    return {
      symbol,
      price: regularPrice.toFixed(2),
      change: `${change >= 0 ? "+" : ""}${change.toFixed(2)}`,
      changePercent: `${changePercent >= 0 ? "+" : ""}${changePercent.toFixed(2)}`,
      time: timeStr,
      message: `纳斯达克100期货最新价: $${regularPrice.toFixed(2)} (${change >= 0 ? "+" : ""}${change.toFixed(
        2
      )} / ${changePercent >= 0 ? "+" : ""}${changePercent.toFixed(
        2
      )}%) 数据时间: ${timeStr}`,
    };
  } catch (e) {
    return {
      error: true,
      message: `查询失败: ${e && e.message ? e.message : String(e)}`,
    };
  }
}

module.exports = { handler };

