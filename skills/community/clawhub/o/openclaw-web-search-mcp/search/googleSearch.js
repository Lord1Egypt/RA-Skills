const axios = require("axios");
const cheerio = require("cheerio");


function cleanDuckDuckGoUrl(url) {

  try {

    if (url.startsWith("//duckduckgo.com")) {

      const parsed = new URL("https:" + url);
      const real = parsed.searchParams.get("uddg");

      if (real) return decodeURIComponent(real);
    }

    return url;

  } catch {
    return url;
  }
}

async function searchAll(query) {

  const url = `https://duckduckgo.com/html/?q=${encodeURIComponent(query)}`;

  const res = await axios.get(url, {
    headers: { "User-Agent": "Mozilla/5.0" }
  });

  const $ = cheerio.load(res.data);

  const results = [];

  $(".result").each((i, el) => {

    const title = $(el).find(".result__title a").text();
    const link = $(el).find(".result__title a").attr("href");
    const snippet = $(el).find(".result__snippet").text();

    if (title && link) {
      results.push({
        title,
        url: cleanDuckDuckGoUrl(link),
        snippet
      });
    }
  });

  return results.slice(0, 10);
}





module.exports = { searchAll };