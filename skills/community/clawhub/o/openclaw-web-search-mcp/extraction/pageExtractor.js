const axios = require("axios");
const cheerio = require("cheerio");

async function extractPage(url) {

  const res = await axios.get(url,{headers:{'User-Agent':'Mozilla/5.0'}});

  const $ = cheerio.load(res.data);

  $("script,style,nav,footer,header").remove();

  const text = $("body").text().replace(/\s+/g," ").trim();

  return {
    url,
    title: $("title").text(),
    content: text.substring(0,20000)
  };
}

async function extractLinks(url){

  const res = await axios.get(url);
  const $ = cheerio.load(res.data);

  const links=[];

  $("a").each((i,e)=>{
    const href=$(e).attr("href");
    const text=$(e).text();

    if(href) links.push({text,url:href});
  });

  return links.slice(0,50);
}

module.exports={extractPage,extractLinks};