#!/usr/bin/env python3
"""
东方财富 API 数据获取

测试东方财富个股数据接口
"""

import requests
import json
from datetime import datetime


def get_eastmoney_quote(symbol):
    """
    从东方财富获取个股行情
    
    Args:
        symbol: 股票代码（如：600519.SH）
    
    Returns:
        dict: 行情数据
    """
    # 转换股票代码为东方财富格式
    if '.SH' in symbol:
        code = symbol.replace('.SH', '')
        secid = f"1.{code}"  # 1=上海
    elif '.SZ' in symbol:
        code = symbol.replace('.SZ', '')
        secid = f"0.{code}"  # 0=深圳
    else:
        return None
    
    url = f"https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        'secid': secid,
        'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f57,f58,f105,f106,f107,f108,f109,f110,f111,f112,f113,f114,f115,f116,f117,f118,f119,f120,f121,f122,f123,f124,f125,f126,f127,f128,f129,f130,f131,f132,f133,f134,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f150,f151,f152,f153,f154,f155,f156,f157,f158,f159,f160,f161,f162,f163,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f193,f194,f195,f196,f197,f198,f199,f200,f201,f202,f203,f204,f205,f206,f207,f208,f209,f210,f211,f212,f213,f214,f215,f216,f217,f218,f219,f220,f221,f222,f223,f224,f225,f226,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f243,f244,f245,f246,f247,f248,f249,f250,f251,f252,f253,f254,f255,f256,f257,f258,f259,f260,f261,f262,f263,f264,f265,f266,f267,f268,f269,f270,f271,f272,f273,f274,f275,f276,f277,f278,f279,f280,f281,f282,f283,f284,f285,f286,f287,f288,f289,f290,f291,f292,f293,f294,f295,f296,f297,f298,f299,f300,f301,f302,f303,f304,f305,f306,f307,f308,f309,f310,f311,f312,f313,f314,f315,f316,f317,f318,f319,f320,f321,f322,f323,f324,f325,f326,f327,f328,f329,f330,f331,f332,f333,f334,f335,f336,f337,f338,f339,f340,f341,f342,f343,f344,f345,f346,f347,f348,f349,f350,f351,f352,f353,f354,f355,f356,f357,f358,f359,f360,f361,f362,f363,f364,f365,f366,f367,f368,f369,f370,f371,f372,f373,f374,f375,f376,f377,f378,f379,f380,f381,f382,f383,f384,f385,f386,f387,f388,f389,f390,f391,f392,f393,f394,f395,f396,f397,f398,f399,f400,f401,f402,f403,f404,f405,f406,f407,f408,f409,f410,f411,f412,f413,f414,f415,f416,f417,f418,f419,f420,f421,f422,f423,f424,f425,f426,f427,f428,f429,f430,f431,f432,f433,f434,f435,f436,f437,f438,f439,f440,f441,f442,f443,f444,f445,f446,f447,f448,f449,f450,f451,f452,f453,f454,f455,f456,f457,f458,f459,f460,f461,f462,f463,f464,f465,f466,f467,f468,f469,f470,f471,f472,f473,f474,f475,f476,f477,f478,f479,f480,f481,f482,f483,f484,f485,f486,f487,f488,f489,f490,f491,f492,f493,f494,f495,f496,f497,f498,f499,f500',
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
        'fltt': '2',
        'invt': '2',
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('data'):
            return None
        
        d = data['data']
        
        return {
            'symbol': symbol,
            'name': d.get('f58', ''),  # 股票名称
            'price': d.get('f43', 0.0) / 100,  # 当前价（需要除以 100）
            'change': d.get('f44', 0.0) / 100,  # 涨跌额
            'change_percent': d.get('f45', 0.0) / 100,  # 涨跌幅%
            'volume': d.get('f47', 0),  # 成交量
            'turnover': d.get('f48', 0.0),  # 成交额
            'high': d.get('f46', 0.0) / 100,  # 最高价
            'low': d.get('f49', 0.0) / 100,  # 最低价
            'open': d.get('f50', 0.0) / 100,  # 开盘价
            'prev_close': d.get('f51', 0.0) / 100,  # 昨收
            'market_cap': d.get('f116', 0.0),  # 总市值
            'pe': d.get('f164', 0.0),  # 市盈率
            'pb': d.get('f165', 0.0),  # 市净率
            'source': 'eastmoney',
            'timestamp': datetime.now().isoformat(),
        }
    except Exception as e:
        print(f"❌ 获取失败：{e}")
        return None


def main():
    """主函数"""
    print("📊 东方财富 API 测试")
    print(f"⏰ 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 测试个股
    print("测试个股数据：")
    print("-" * 50)
    
    test_stocks = ['600519.SH', '000001.SZ', '300750.SZ']
    
    for symbol in test_stocks:
        data = get_eastmoney_quote(symbol)
        if data:
            print(f"✅ {symbol} {data['name']}: ¥{data['price']} ({data['change_percent']}%)")
            print(f"   最高：¥{data['high']}, 最低：¥{data['low']}, 昨收：¥{data['prev_close']}")
            print(f"   成交量：{data['volume']}, 成交额：{data['turnover']}")
        else:
            print(f"❌ {symbol}: 获取失败")
    
    print()
    print("=" * 50)
    print("✅ 测试完成！")


if __name__ == '__main__':
    main()
