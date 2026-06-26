const axios = require("axios");
const pdf = require("pdf-parse");

async function extractPDF(url){

  const res = await axios.get(url,{responseType:"arraybuffer"});

  const data = await pdf(res.data);

  return {
    text: data.text.substring(0,20000),
    pages: data.numpages
  };
}

module.exports={extractPDF};