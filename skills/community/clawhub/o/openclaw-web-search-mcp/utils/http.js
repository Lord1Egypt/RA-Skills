const axios = require("axios");

async function fetchHTML(url) {
  const res = await axios.get(url, {
    headers: { "User-Agent": "Mozilla/5.0" },
    timeout: 10000
  });

  return res.data;
}

module.exports = { fetchHTML };