import sys
import json
import requests

BASE_URL = "http://10.168.1.162:8000"

ALLOWED_ENDPOINTS = [
    "MoneyStockMeasures",
    "SeasonallyAdjusted",
    "NotSeasonallyAdjusted",
    "exchangeRate",
    "InterestRate",
    "FARBODI",
    "FARBODIC",
    "MI",
    "MDOSLASOAAL",
    "SIOMS",
    "IOPAOCFL",
    "CSOCOAFRB",
    "CSOCOAFRBC",
    "SOCOEFRB",
    "SOCOEFRBC",
    "CHAFRNFRAA",
    "SAALOCBITUSS_ASSET",
    "SAALOCBITUSS_Liabilities",
    "AALOCBITUSS_ASSET",
    "AALOCBITUSS_Liabilities",
    "AALOCBITUSNS_ASSET",
    "AALOCBITUSNS_Liabilities",
    "AALODCCBITUSS_ASSET",
    "AALODCCBITUSS_Liabilities",
    "AALODCCBITUSNS_ASSET",
    "AALODCCBITUSNS_Liabilities",
    "AALOLDCCBITUSS_ASSET",
    "AALOLDCCBITUSS_Liabilities",
    "AALOLDCCBITUSNS_ASSET",
    "AALOLDCCBITUSNS_Liabilities",
    "AALOSDCCBITUSS_ASSET",
    "AALOSDCCBITUSS_Liabilities",
    "AALOSDCCBITUSNS_ASSET",
    "AALOSDCCBITUSNS_Liabilities",
    "AALOFRIITUSS_ASSET",
    "AALOFRIITUSS_Liabilities",
    "AALOFRIITUSNS_ASSET",
    "AALOFRIITUSNS_Liabilities",
    "FER",
    "Loan",
    "USTreasuriesYields",
    "USTreasuriesSize",
    "FBI",
    "PCE",
    "GPDI",
    "NETEXP",
    "COVITGDP",
    "PCGDP",
    "WEI",
    "CPI_PPI"
]

def call_api(endpoint, params=None):
    """调用 API"""
    if endpoint not in ALLOWED_ENDPOINTS:
        print(f"Error: endpoint '{endpoint}' not allowed.")
        sys.exit(1)

    url = f"{BASE_URL}/db/Macroeconomics/table/{endpoint}"

    if params:
        if isinstance(params, dict):
            # JSON 字典参数拼接 query
            for k, v in params.items():
                url += f"?{k}={v}" if "?" not in url else f"&{k}={v}"
        elif isinstance(params, int):
            # 整数作为 limit
            url += f"/limit/{params}"
        elif isinstance(params, str):
            # 字符串作为日期
            url += f"/date/{params}"
        else:
            print("Error: params must be dict, int, or date string (YYYY-MM-DD)")
            sys.exit(1)

    try:
        resp = requests.get(url)
        data = resp.json()
    except Exception as e:
        print(f"Error fetching API: {e}")
        sys.exit(1)

    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python macro_api.py <endpoint> [limit | YYYY-MM-DD | JSON params]")
        sys.exit(1)

    endpoint = sys.argv[1]
    params = None

    if len(sys.argv) >= 3:
        arg = sys.argv[2]
        try:
            # 尝试 JSON
            params = json.loads(arg)
        except:
            try:
                # 尝试整数
                params = int(arg)
            except:
                # 当作日期字符串
                params = arg

    call_api(endpoint, params)