const { searchAll } = require("./search/googleSearch");
const { extractPage, extractLinks } = require("./extraction/pageExtractor");
const { extractPDF } = require("./extraction/pdfExtractor");
const { getTranscript } = require("./extraction/youtubeTranscript");

const { summarizeText } = require("./ai/summarizer");
const { embedText, semanticSearch } = require("./ai/embeddings");

const { researchTopic } = require("./research/researchAgent");

async function run() {

  const tool = process.argv[2];
  const input = JSON.parse(process.argv[3] || "{}");

  try {

    if (tool === "search")
      return console.log(JSON.stringify(await searchAll(input.query)));

    if (tool === "open_page")
      return console.log(JSON.stringify(await extractPage(input.url)));

    if (tool === "extract_links")
      return console.log(JSON.stringify(await extractLinks(input.url)));

    if (tool === "extract_pdf")
      return console.log(JSON.stringify(await extractPDF(input.url)));

    if (tool === "youtube_transcript")
      return console.log(JSON.stringify(await getTranscript(input.url)));

    if (tool === "summarize")
      return console.log(JSON.stringify(summarizeText(input.text)));

    if (tool === "embed")
      return console.log(JSON.stringify(embedText(input.text)));

    if (tool === "semantic_search")
      return console.log(JSON.stringify(semanticSearch(input.query)));

    if (tool === "research")
      return console.log(JSON.stringify(await researchTopic(input.query)));

  } catch (err) {

    console.error(err);
  }
}

run();