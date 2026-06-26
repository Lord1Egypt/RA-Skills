import https from 'https';

export function fetchJson(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, (res) => {
      if (res.statusCode < 200 || res.statusCode >= 300) {
        res.resume();
        reject(new Error(`HTTP ${res.statusCode} from ${url}`));
        return;
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`Invalid JSON from ${url}`));
        }
      });
    });
    req.on('error', reject);
    req.setTimeout(5000, () => {
      req.destroy();
      reject(new Error('Request Timeout'));
    });
  });
}

export function calculatePremium(rateData, upbitData, binanceData) {
  const exchangeRate = rateData?.rates?.KRW;
  if (typeof exchangeRate !== 'number' || exchangeRate <= 0) {
    throw new Error('Invalid exchange rate data');
  }

  const upbitPriceKRW = upbitData?.[0]?.trade_price;
  if (typeof upbitPriceKRW !== 'number' || upbitPriceKRW <= 0) {
    throw new Error('Invalid Upbit price data');
  }

  const binancePriceUSD = parseFloat(binanceData?.price);
  if (isNaN(binancePriceUSD) || binancePriceUSD <= 0) {
    throw new Error('Invalid Binance price data');
  }

  const binancePriceKRW = binancePriceUSD * exchangeRate;
  const premiumRate = ((upbitPriceKRW - binancePriceKRW) / binancePriceKRW) * 100;
  const priceDiff = upbitPriceKRW - binancePriceKRW;

  return {
    exchangeRate,
    upbitPriceKRW,
    binancePriceUSD,
    binancePriceKRW,
    premiumRate,
    priceDiff,
  };
}

async function main() {
  try {
    const [rateData, upbitData, binanceData] = await Promise.all([
      fetchJson('https://open.er-api.com/v6/latest/USD'),
      fetchJson('https://api.upbit.com/v1/ticker?markets=KRW-BTC'),
      fetchJson('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
    ]);

    const result = calculatePremium(rateData, upbitData, binanceData);

    console.log(JSON.stringify({
      timestamp: new Date().toLocaleString(),
      exchange_rate: `${result.exchangeRate.toLocaleString()} KRW/USD`,
      upbit_btc: `${result.upbitPriceKRW.toLocaleString()} KRW`,
      binance_btc: `${result.binancePriceUSD.toLocaleString()} USD`,
      kimchi_premium: `${result.premiumRate.toFixed(2)}%`,
      price_diff: `${Math.floor(result.priceDiff).toLocaleString()} KRW`
    }, null, 2));

  } catch (error) {
    console.error(JSON.stringify({ error: error.message }));
  }
}

main();
