const { searchAll } = require("../search/googleSearch");
const { extractPage } = require("../extraction/pageExtractor");
const { summarizeText } = require("../ai/summarizer");

function decodeDuckDuckGoUrl(url) {

  try {

    if (url.startsWith("//duckduckgo.com")) {

      const full = "https:" + url;
      const parsed = new URL(full);
      const real = parsed.searchParams.get("uddg");

      if (real) return decodeURIComponent(real);
    }

    return url;

  } catch (err) {
    return url;
  }
}

async function researchTopic(query) {

  const search = await searchAll(query);

  const findings = [];

  for (const r of search.slice(0,5)) {

    try {

      const realUrl = decodeDuckDuckGoUrl(r.url);

      const page = await extractPage(realUrl);

      if (!page.content || page.content.length < 200)
        continue;

      const summary = summarizeText(page.content);

      findings.push({
        title: r.title,
        source: realUrl,
        summary
      });

    } catch (err) {

      console.log("Failed:", r.url);

    }
  }

  return {
    query,
    findings
  };
}

module.exports = { researchTopic };